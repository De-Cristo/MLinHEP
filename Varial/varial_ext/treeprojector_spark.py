"""
Treeprojection with apache spark.
"""
from varial_ext.treeprojector import TreeProjectorBase
import varial_ext.treeprojection_mr_impl as mr
import pyspark
import varial
import os


spark_context = None


def add_histos(a, b):
    c = a.Clone()
    c.Add(b)
    return c


def open_files(args):
    import ROOT
    sample, filename = args
    return sample, filename, ROOT.TFile(os.path.abspath(filename))


def map_projection_spark(args, ssw, params):
    sample, filename, open_file = args
    _, selection, weight = ssw
    params = dict(params)
    params['weight'] = weight[sample] if isinstance(weight, dict) else weight
    params['selection'] = selection
    histos = params['histos'].keys()

    map_iter = (res
                for h in histos
                for res in mr.map_projection(
                    '%s %s %s'%(sample, h, filename), params, open_file))
    result = list(map_iter)

    return result


def wrap_histo(args, section):
    sample_histoname, histo = args
    sample, histoname = sample_histoname.split()
    return varial.wrp.HistoWrapper(
        histo,
        name=str(histoname),
        sample=str(sample),
        in_file_path=str('%s/%s' % (section, histoname)),
    )


############################################################ tree projector ###
class SparkTreeProjector(TreeProjectorBase):
    """
    Project histograms from files with TTrees on SGE with jug.

    Same args as TreeProjectorBase plus:
    :param spark_url:   e.g. spark://localhost:7077.
    :param hot_result:  if True, result wrappers are stored in hot_result member and not to disk.
    """
    def __init__(self, *args, **kws):
        global spark_context
        spark_context = pyspark.SparkContext(
            kws.pop('spark_url', 'local'),
            'SparkTreeProjector/%s' % os.getlogin()
        )
        self.rdd_cache = None
        super(SparkTreeProjector, self).__init__(*args, **kws)

    def run(self):
        os.system('touch ' + self.cwd + 'webcreate_denial')
        self.hot_result = []

        if not self.rdd_cache:
            self.message('INFO initializing root files.')
            inputs = list(
                (sample, f)
                for sample, filenames in self.filenames.iteritems()
                for f in filenames
            )
            rdd = spark_context.parallelize(inputs)
            rdd.cache()
            rdd = rdd.map(open_files)
            self.rdd_cache = rdd

        # do the work
        params = self.params
        for ssw in self.sec_sel_weight:
            section = ssw[0]
            self.message('INFO starting section "%s".' % section)
            rdd = self.rdd_cache.flatMap(lambda args: map_projection_spark(args, ssw, params))
            rdd = rdd.reduceByKey(add_histos)

            if self.use_hot_result:  # just collect and store in self.hot_result
                # rdd = rdd.map(lambda args: wrap_histo(args, section))
                res = rdd.collect()
                res = (wrap_histo(r, section) for r in res)
                self.hot_result += list(res)

            else:  # make rootfiles and aliases
                rdd = rdd.map(lambda x: (x[0].split()[0], x))  #(sample, (sample-histo-name, histo))
                rdd = rdd.groupByKey()
                res = rdd.collect()
                for sample, histo_iter in res:
                    mr.store_sample(sample, section, histo_iter)
                    varial.diskio.write_fileservice(section+'.'+sample, initial_mode='RECREATE')

        if not self.use_hot_result:
            self.put_aliases(lambda w: os.path.basename(w.file_path).split('.')[-2])

from varial.plotter import mk_rootfile_plotter
from varial.main import process_settings_kws
from varial.webcreator import WebCreator
from varial.tools import Runner
import quantitylist
import varial
import string
import shutil
import ast
import os


varial.ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')
SECTION_CHARS = '-_.' + string.ascii_letters + string.digits


class HistoTypeSpecifier(object):
    def __init__(self, signals, data):
        assert isinstance(signals, list)
        assert isinstance(data, list)
        self.signals = signals
        self.data = data

    def __call__(self, wrps):
        return varial.gen.gen_add_wrp_info(
            wrps,
            is_signal=lambda w: w.sample in self.signals,
            is_data=lambda w: w.sample in self.data,
            legend=lambda w: w.sample,
        )


class HistoCache(varial.tools.Tool):
    io = varial.pklio
    no_reset = True

    def __init__(self, hot_result_tool, type_spec, name=None):
        super(HistoCache, self).__init__(name)
        self.hot_result_tool = hot_result_tool
        self.result_dict = {}  # 'section/histoname/sample' -> histo-wrp
        self.type_spec = type_spec
        self.init = False

    def duplicate_section(self, from_name, to_name):
        for key in self.result_dict.keys():
            if key.split('/')[0] == from_name:
                _, histoname, sample = key.split('/')
                wrp = varial.op.copy(self.result_dict[key])
                wrp.in_file_path = '%s/%s' % (to_name, histoname)
                new_key = '%s/%s' % (wrp.in_file_path, sample)
                self.result_dict[new_key] = wrp
        self.fill_result()

    def delete_section(self, name):
        for key in self.result_dict.keys():
            if key.split('/')[0] == name:
                del self.result_dict[key]
        self.fill_result()

    def delete_histo(self, name):
        for key in self.result_dict.keys():
            if key.split('/')[1] == name:
                del self.result_dict[key]
        self.fill_result()

    def fill_result_dict(self, histo_wrps):
        for w in histo_wrps:
            key = '%s/%s' % (w.in_file_path, w.sample)
            self.result_dict[key] = w

    def fill_result(self):
        res_dict = self.result_dict
        self.result = varial.wrp.WrapperWrapper(list(
            res_dict[key]
            for key in sorted(res_dict)
        ))

    def run(self):
        os.system('touch ' + self.cwd + 'webcreate_denial')
        if not self.init:
            self.reuse(True)  # make sure to get stored results on startup
            self.init = True

        if self.result and not self.result_dict:
            self.fill_result_dict(self.result)

        self.fill_result_dict(self.type_spec(self.hot_result_tool.hot_result))
        self.fill_result()


class HQueryBackend(object):
    def __init__(self, kws, q_in, q_out):
        assert 'filenames' in kws, '"filenames" is needed.'
        assert 'treename' in kws, '"treename" is needed.'
        backend = kws.pop('backend', 'local')

        self.q_in = q_in
        self.q_out = q_out

        if not os.path.exists('sections'):
            os.mkdir('sections')
            os.system('touch sections/webcreate_request')

        histos = kws.pop('histos', {})
        for name, tple in histos.iteritems():
            self.check_histo_item(name, tple)
        self.params = dict(histos=histos,
                           treename=kws.pop('treename'),
                           nm1=False)
        self.sel_info = {}
        self.sec_sel_weight = {}  # sec -> (sec, sel, weight)
        weight, msg = kws.pop('weight', ''), 'weight can be str or dict'
        assert isinstance(weight, str) or isinstance(weight, dict), msg

        self.weight = weight
        self.branchname_proc = None

        if backend == 'local':
            from varial_ext.treeprojector import TreeProjector as TP
            self.tp = TP(kws.pop('filenames'),
                         self.params,
                         hot_result=True,
                         name='treeprojector')
        elif backend == 'jug':
            from varial_ext.treeprojector_jug import JugTreeProjector as TP
            self.tp = TP(kws.pop('filenames'),
                         self.params,
                         hot_result=True,
                         name='treeprojector')
        elif backend.startswith('spark://'):
            from varial_ext.treeprojector_spark import SparkTreeProjector as TP
            self.tp = TP(kws.pop('filenames'),
                         self.params,
                         hot_result=True,
                         spark_url=backend,
                         name='treeprojector')
        else:
            assert False, 'backend may be "local", "jug" or a spark url'

        self.hc = HistoCache(
            self.tp,
            HistoTypeSpecifier(
                kws.pop('signal_samples', []),
                kws.pop('data_samples', []),
            ),
            'cache',
        )
        Runner(self.hc)  # initialize cache

        self.wc = WebCreator(name='hQuery', no_tool_check=True)
        self.wc.working_dir = 'sections'
        self.wc.update()

        self.options = {
            'stack': kws.pop('stack', False),
            'dump_python_conf': kws.pop('dump_python_conf', False),
            'integral_info': kws.pop('integral_info', True),
        }
        varial.settings.no_toggles = not self.options['integral_info']

        process_settings_kws(kws)

    def read_settings(self):
        if not os.path.exists('params.py'):
            return False
        with open('params.py') as f:
            self.params, self.sec_sel_weight, self.sel_info = ast.literal_eval(f.read())
        return True

    def write_settings(self):
        with open('params.py', 'w') as f:
            f.write(repr((self.params, self.sec_sel_weight, self.sel_info)))
        if self.options['dump_python_conf']:
            self.write_histos()
            self.write_sec_sel_weight()

    def write_histos(self):
        with open('params_histos.py', 'w') as f:
            f.write(repr(self.params['histos']))

    def write_sec_sel_weight(self):
        with open('params_sec_sel_weight.py', 'w') as f:
            f.write(repr(self.sec_sel_weight))

    def run_webcreator(self):
        self.wc.run()
        self.wc.reset()
        varial.analysis.reset()

    def run_treeprojection(self, section=None, histo=None):
        if section:
            ssw = [self.sec_sel_weight[section]]
        else:
            ssw = list(self.sec_sel_weight.itervalues())

        if not (ssw and self.params['histos']):
            return

        self.q_out.put('Filling histograms in: ' + ', '.join(s[0] for s in ssw))
        self.tp.sec_sel_weight = ssw
        if histo:
            self.tp.params = dict(self.params)
            self.tp.params['histos'] = {histo: self.params['histos'][histo]}
        else:
            self.tp.params = self.params
        Runner(self.tp)
        Runner(self.hc)
        Runner(mk_rootfile_plotter(
            name='sections',
            input_result_path='cache',
            combine_files=True,
            stack=self.options['stack'],
            auto_legend=False,
        ))

    @staticmethod
    def check_histo_item(name, tple):
        assert len(tple) == 4, 'need title,bins,low,high; got %s' % tple
        title, bins, lo, hi = tple
        assert isinstance(name, str), repr(name)
        assert isinstance(title, str), repr(title)
        assert isinstance(bins, int), repr(bins)
        assert isinstance(lo, int) or isinstance(lo, float), repr(lo)
        assert isinstance(hi, int) or isinstance(hi, float), repr(hi)

    def create_new_section(self, name, from_section=None):
        # checks
        if any(c not in SECTION_CHARS for c in name):
            raise RuntimeError(
                'Section names may only contain "%s". Got "%s".'
                % (SECTION_CHARS, name)
            )
        if os.path.exists('sections/' + name):
            raise RuntimeError('Section exists: ' + name)

        if from_section:  # copy
            shutil.copytree('sections/' + from_section, 'sections/' + name)
            sel = self.sec_sel_weight[from_section][1]
            self.sec_sel_weight[name] = (name, sel[:], self.weight)
            self.sel_info[name] = dict(self.sel_info[from_section])
            self.hc.duplicate_section(from_section, name)

        else:  # create from scratch
            os.mkdir('sections/' + name)
            with open('sections/' + name + '/webcreate_request', 'w') as f:
                f.write('(enable webcreation also for empty folders)\n')
            self.sec_sel_weight[name] = (name, [], self.weight)
            self.sel_info[name] = dict(
                (hname, (u'', u''))
                for hname in self.params['histos'].iterkeys()
            )

        self.q_out.put('Section created: ' + name)
        self.run_webcreator()
        self.q_out.put('redirect:/{}/index.html'.format(name))

        if not from_section:  # run treeprojection if not copied
            self.run_treeprojection(name)

    def delete_section(self, name):
        if not os.path.exists('sections/' + name):
            raise RuntimeError('Section does not exists: ' + name)

        shutil.rmtree('sections/' + name)
        del self.sec_sel_weight[name]
        del self.sel_info[name]
        self.hc.delete_section(name)

        self.q_out.put('Section deleted: ' + name)

    def create_histogram(self, kws):
        name = str(kws['hidden_histo_name'] or kws['histo_name'])
        name = name.replace(' ', '')  # remove spaces
        bins, low, high = kws['bins'], kws['low'], kws['high']

        # checks
        assert_msg = 'Either "bins" or "low" *and* "high" needed. Or all.'
        assert bins or (low and high), assert_msg
        assert bool(low) == bool(high), assert_msg
        bins = int(kws['bins'] or 40)
        if not low:
            bins, low, high = bins + 1, -.5, bins + .5
        params = (str(kws['title']), bins, float(low), float(high))
        self.check_histo_item(name, params)

        # run sections with new histo
        self.params['histos'][name] = params
        self.q_out.put('Histogram defined: ' + name)
        try:  # if something goes wrong, the histo must be removed
            self.run_treeprojection(None, name)
        except RuntimeError:
            del self.params['histos'][name]
            raise

        # add empty selection in every section
        for si in self.sel_info.itervalues():
            si[name] = (u'', u'')

        self.q_out.put('redirect:index.html#{}'.format(name))

    def delete_histogram(self, name):
        del self.params['histos'][name]
        for si in self.sel_info.itervalues():
            del si[name]
        names = list(name + tok +'.png' for tok in ('_lin', '_log', ''))
        for section in self.sec_sel_weight:
            p = os.path.join('sections', section)
            for f in os.listdir(p):
                if f in names:
                    os.remove(os.path.join(p, f))
        self.hc.delete_histo(name)

        self.q_out.put('Histogram deleted: ' + name)

    def apply_selection(self, section, kws):
        def pick_sel_str(low, high):
            return (
                '({lo} <= {var} && {var} < {hi})'
                if float(low) <= float(high) else
                '({lo} <= {var} || {var} < {hi})'
            ) if low and high else (
                '{lo} <= {var}'
                if low else (
                    '{var} < {hi}'
                    if high else
                    ''
                )
            )

        def format_sel_str(var, low, high):
            return pick_sel_str(low, high).format(lo=low, hi=high, var=var)

        all_reqs = (
            (var, (kws[var+' low'], kws[var+' high']))
            for var in self.params['histos'].iterkeys()
        )
        all_reqs = list(
            (var, lo_hi, format_sel_str(var, *lo_hi))
            for var, lo_hi in all_reqs
        )
        sel_list = list(
            sel
            for _, _, sel in all_reqs
            if sel
        )
        updates = list(
            sel
            for var, lo_hi, sel in all_reqs
            if self.sel_info[section][var] != lo_hi
        )

        if not updates:
            self.q_out.put('Selection unchanged.')
            return

        self.q_out.put('Selection updated: ' + '; '.join(filter(None, updates)))
        old_sel_list = self.sec_sel_weight[section][1]
        self.sec_sel_weight[section] = (section, sel_list, self.weight)

        # run section with new selection
        try:
            self.run_treeprojection(section)
        except RuntimeError:
            # if something goes wrong, the selection must be removed
            self.sec_sel_weight[section] = (section, old_sel_list, self.weight)
            raise

        self.sel_info[section] = dict((var, lohi) for var, lohi, _ in all_reqs)

    def process_request(self, item):
        varial.monitor.message(
            'HQueryBackend.process_request',
            'INFO got request %s' % repr(item),
        )

        if isinstance(item, tuple) and item and item[0] == 'post':
            _, args, kws = item

            # new section
            if 'create section' in kws:
                self.create_new_section(
                    kws['create section'],
                    args[0] if len(args) == 2 else None
                )

            # delete section
            elif 'delete section' in kws:
                self.delete_section(kws['delete section'])

            # create histo
            elif 'hidden_histo_name' in kws:
                self.create_histogram(kws)

            # delete histo
            elif 'delete histogram' in kws:
                self.delete_histogram(kws['delete histogram'])

            # apply selection
            elif 'selection' in kws:
                self.apply_selection(args[0], kws)

            else:
                raise RuntimeError('Request not understood %s' % repr(item))
        else:
            raise RuntimeError('Request not understood %s' % repr(item))

        self.run_webcreator()
        self.write_settings()

    def start(self):
        self.q_out.put('backend alive')

        if self.hc.type_spec.data:
            filenames = self.tp.filenames[self.hc.type_spec.data[0]]
        else:
            filenames = next(self.tp.filenames.itervalues())
        self.branchname_proc = quantitylist.get_proc(filenames, self.params['treename'])
        if not self.read_settings():
            self.run_treeprojection()
            self.run_webcreator()
            self.write_settings()
        self.q_out.put('task done')

        while True:
            item = None

            # get request item
            try:
                item = self.q_in.get()
            except KeyboardInterrupt:
                exit(0)
            if item == 'terminate':
                exit(0)

            # process request
            try:
                self.process_request(item)
            except (RuntimeError, AssertionError), e:
                msg = 'ERROR: %s' % e.message
                varial.monitor.message('HQueryBackend.process_request', msg)
                self.q_out.put(msg)

            # done and ready for next request
            self.q_out.put('task done')

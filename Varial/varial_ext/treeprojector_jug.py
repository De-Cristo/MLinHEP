"""
Treeprojection on SGE with jug. (https://jug.readthedocs.org)
"""
from varial_ext.treeprojector import TreeProjectorBase
import itertools
import varial
import glob
import time
import os


############################################################ tree projector ###
jug_work_dir_pat = '/nfs/dust/cms/user/{user}/varial_sge_exec'
jug_file_search_pat = jug_work_dir_pat + '/jug_file-*.py'
jug_file_path_pat = jug_work_dir_pat + '/jug_file-{i}-{section}-{sample}.py'

jugfile_content = """
sample = {sample}
section = {section}
params = {params}
files = {files}

inputs = list(
    (sample, f, params)
    for f in files
)

import varial_ext.treeprojection_mr_impl as mr
from jug.compound import CompoundTask
from jug import TaskGenerator
import jug.mapreduce
import cPickle
import os

@TaskGenerator
def finalize(result):
    os.remove(__file__)     # do not let other workers find the task anymore
    import varial           # importing varial is time consuming
    import time
    mr.store_sample(sample, section, result)
    varial.diskio.write_fileservice(__file__.replace('.py', ''), initial_mode='UPDATE')
    os.chmod(__file__.replace('.py', '.root'), 0o0664)
    os.remove(__file__.replace('.py', '.info'))
    os.system('rm -rf %s' % __file__.replace('.py', '.jugdata'))


result = CompoundTask(
    jug.mapreduce.mapreduce,
    mr.reduce_projection_by_two,
    mr.map_projection_per_file,
    inputs,
    map_step=2,
    reduce_step=8,
)
final_task = finalize(result)

jug.options.default_options.execute_wait_cycle_time_secs = 1
jug.options.default_options.execute_nr_wait_cycles = 1
"""


class JugTreeProjector(TreeProjectorBase):
    """
    Project histograms from files with TTrees on SGE with jug.

    Same args as TreeProjectorBase plus:
    :param progress_callback:       function with two args: N(jobs), N(done).
    """
    def __init__(self, *args, **kws):
        super(JugTreeProjector, self).__init__(*args, **kws)

        self.progress_callback = kws.get('progress_callback', 0) or (lambda a, b: None)
        self.jug_tasks = None
        self.iteration = -1
        self.username = os.getlogin()

        # clear directory
        exec_pat = jug_file_search_pat.format(user=self.username).replace('.py', '')
        if glob.glob(exec_pat):
            os.system('rm -rf ' + exec_pat)

        os.umask(2)  # need files to be writable by workers of any user

    def launch_tasks(self, section, selection, weight):
        for sample in self.samples:
            params = self.prepare_params(selection, weight, sample)
            p_jugfile = jug_file_path_pat.format(
                i=self.iteration, user=self.username, section=section, sample=sample)
            p_jugres = os.path.splitext(p_jugfile)[0]

            # write jug_file
            with open(p_jugfile, 'w') as f:
                f.write(jugfile_content.format(
                    section=repr(section),
                    sample=repr(sample),
                    params=repr(params),
                    files=repr(self.filenames[sample]),
                ))

            # load new task
            self.jug_tasks.append((sample, p_jugres))

    def transfer_result(self, p):
        os.system('mv %s.root %s' % (p, self.cwd))
        ws = varial.diskio.generate_aliases(
            self.cwd + os.path.basename(p) + '.root')
        ws = varial.gen.gen_add_wrp_info(ws,
            sample=lambda w: w.file_path.split('-')[-1][:-5])
        return ws

    def process_tasks(self):
        n_jobs = len(self.jug_tasks)
        n_done_prev, n_done = 0, -1
        items_done = [False] * n_jobs
        wrps = []

        while n_done < n_jobs:

            errs = list(p + '.err.txt'
                for (_, p) in self.jug_tasks
                if os.path.exists(p + '.err.txt')
            )
            if errs:
                with open(errs[0]) as f:
                    raise RuntimeError(f.read())

            items_due = list(
                (not d) and os.path.exists(p + '.root')
                for (d, (_, p)) in itertools.izip(items_done, self.jug_tasks)
            )
            items_done = list(
                a or b
                for a, b in itertools.izip(items_done, items_due)
            )
            n_done_prev, n_done = n_done, sum(items_done)

            time.sleep(0.3)  # wait for write  # TODO wait for open exclusively
            if n_done_prev != n_done:
                for d, (_, p) in itertools.izip(items_due, self.jug_tasks):
                    if d:
                        ws = self.transfer_result(p)
                        if self.use_hot_result:
                            self.hot_result += varial.diskio.bulk_load_histograms(ws)
                        else:
                            wrps += ws

                self.message('INFO {}/{} done'.format(n_done, n_jobs))
                self.progress_callback(n_jobs, n_done)

        return wrps

    def run(self):
        os.system('touch ' + self.cwd + 'webcreate_denial')
        self.hot_result = []
        self.iteration += 1

        # clear last round of running (and the ones of 3 iterations ago)
        wd_junk = jug_file_search_pat.format(user=self.username)
        wd_junk = wd_junk.replace('*.py', '%d.*' % (self.iteration - 4))
        wd_junk_files = glob.glob(wd_junk)
        if wd_junk_files:
            os.system('rm ' + ' '.join(wd_junk_files))
        tooldir_junk_files = glob.glob('%s/*.root' % self.cwd)
        if tooldir_junk_files:
            os.system('rm ' + ' '.join(tooldir_junk_files))

        # do the work
        self.jug_tasks = []
        for ssw in self.sec_sel_weight:
            self.launch_tasks(*ssw)
        wrps = self.process_tasks()

        if not self.use_hot_result:
            self.put_aliases(None, wrps)


# TODO option for _not_ copying/moving result back (softlink?)
# TODO: move jug_constants somewhere sensible
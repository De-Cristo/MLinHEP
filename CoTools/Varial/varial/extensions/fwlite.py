"""
Host fwlite jobs in a toolchain. **EXPERIMENTAL!**
"""


import subprocess
import time
from os.path import exists, join

from varial import analysis
from varial import diskio
from varial import monitor
from varial import settings
from varial import toolinterface
from varial import wrappers


class Fwlite(toolinterface.Tool):
    """
    This class hosts a series of fwlite processes.
    """
    def __init__(self,
                 fwlite_exe,
                 name=None):
        super(Fwlite, self).__init__(name)
        self.fwlite_exe = fwlite_exe
        self._proxy = None
        self._not_ask_execute = False

    def wanna_reuse(self, all_reused_before_me):
        samples = analysis.samples()
        proxy = diskio.get('fwlite_proxy')

        if settings.fwlite_force_reuse or settings.only_reload_results:
            self._proxy = proxy
            return True

        # has been working at all?
        if not proxy:
            self._not_ask_execute = True
            return False

        # check if all previous results are available
        if not all(
            exists(join(self.cwd, '%s.info' % res))
            for res in proxy.results
        ):
            self.message('INFO Not all results are found, running again.')
            return False

        # check if all samples are available
        files_done = proxy.files_done
        if not all(name in files_done for name in samples):
            self.message('INFO Not all samples are done, running again.')
            return False

        # check if all files are done
        if not all(
            f in files_done[smp.name]
            for smp in samples.itervalues()
            for f in smp.input_files
        ):
            self.message('INFO Not all files are done, running again.')
            return False
        self._proxy = proxy
        return True

    def reuse(self):
        super(Fwlite, self).reuse()
        self._finalize()

    def run(self):
        if settings.suppress_eventloop_exec:
            self.message(
                self, "INFO settings.suppress_eventloop_exec == True, pass...")
            return

        # prepare proxy file / ask for execution
        self._make_proxy()
        if not (self._not_ask_execute or settings.not_ask_execute or raw_input(
                "Really run fwlite jobs on these samples:\n   "
                + ",\n   ".join(map(str, self._proxy.due_samples))
                + ('\nusing %i cores' % settings.max_num_processes)
                + "\n?? (type 'yes') "
                ) == "yes"):
            return
        diskio.write(self._proxy)

        # start subprocess
        self.message("INFO Starting script: '%s'" % self.fwlite_exe)
        proc = subprocess.Popen(
            ['python', self.fwlite_exe],
            stdout=monitor.MonitorInfo.outstream,
            stderr=subprocess.STDOUT,
            cwd=self.cwd,
        )

        # block while finished
        sig_kill_sent = False
        while None == proc.returncode:
            if settings.recieved_sigint and not sig_kill_sent:
                proc.kill()
                sig_kill_sent = True
            time.sleep(0.2)
            proc.poll()

        # final
        if proc.returncode:
            self.message('FATAL subprocess has non zero returncode')
            raise RuntimeError(
                'FwLite subprocess returned %d' % proc.returncode)
        self._proxy = diskio.read('fwlite_proxy')
        self.result = self._proxy
        self._finalize()

    def _make_proxy(self):
        samples = analysis.samples()

        for smpl in samples.itervalues():
            if not smpl.input_files:
                self.message(
                    self.name,
                    "WARNING input_files seems to be undefined for sample %s."
                    % smpl.name
                )

        self._proxy = diskio.get(
            'fwlite_proxy',
            wrappers.Wrapper(name='fwlite_proxy', files_done={}, results={})
        )
        self._proxy.max_num_processes = settings.max_num_processes
        self._proxy.do_profiling = settings.fwlite_profiling
        self._proxy.event_files = dict(
            (s.name, s.input_files)
            for s in samples.itervalues()
        )

        # if a result was deleted, remove all associated files from files_done
        files_done = self._proxy.files_done
        results = self._proxy.results
        for res in results.keys():
            if not exists(join(self.cwd, '%s.info' % res)):
                del results[res]
                smpl = res.split('!')[0]
                if smpl in files_done:
                    del files_done[smpl]

        due_samples = samples.keys()
        self._proxy.due_samples = due_samples
        for res in results.keys():
            smpl = res.split('!')[0]
            if smpl in due_samples:
                if all(
                    f in files_done[smpl]
                    for f in samples[smpl].input_files
                ):
                    due_samples.remove(smpl)

    def _finalize(self):
        if settings.recieved_sigint:
            return
        for res in self._proxy.results:
            samplename = res.split('!')[0]
            if samplename not in analysis.all_samples:
                continue
            analysis.fs_aliases += list(
                alias for alias in diskio.generate_fs_aliases(
                    join(self.cwd, '%s.root' % res),
                    analysis.all_samples[samplename]
                )
            )
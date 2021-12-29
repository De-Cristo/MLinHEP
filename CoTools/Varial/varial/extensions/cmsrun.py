"""
Host cmsRun processes in a toolchain.
"""

import glob
import json
import subprocess
import time
import os
join = os.path.join

from varial import analysis
from varial import diskio
from varial import monitor
from varial import settings
from varial import toolinterface
from varial import wrappers


class CmsRunProcess(object):
    """
    This class hosts a cmsRun process.

    cmsRun output is streamed into a logfile.
    """

    def __init__(self, sample_inst, try_reuse_data, cfg_filename):
        super(CmsRunProcess, self).__init__()

        assert isinstance(sample_inst, Sample)
        name = sample_inst.name
        self.sample             = sample_inst
        self.name               = name
        self.cfg_filename       = cfg_filename
        self.log_file           = None
        self.log_filename       = join(analysis.cwd, 'logs', name) + '.log'
        self.conf_filename      = join(analysis.cwd, 'confs', name) + '.py'
        self.service_filename   = join(analysis.cwd, 'fs', name) + '.root'
        self.jobinfo_filename   = join(analysis.cwd, 'report', name) + '.ini'
        self.try_reuse_data     = try_reuse_data
        self.subprocess         = None
        self.time_start         = None
        self.time_end           = None
        self.message = monitor.connect_object_with_messenger(self)

    def __str__(self):
        return "CmsRunProcess(" + self.name + ")"

    def __repr__(self):
        return str(self)

    def prepare_run_conf(self,
                         use_file_service,
                         output_module_name,
                         common_builtins):
        #"""
        #Takes all infos about the cmsRun to be started and builds a
        #configuration file with python code, which is passed to cmsRun on
        #calling start().
        #"""

        # collect lines to write out at once.
        conf_lines = [
            "# generated",
            "# on " + time.ctime(),
            "# by cmsrunprocess.py",
            ""
        ]

        # set __builtin__ variables
        smpl = self.sample
        builtin_dict = {
            "lumi"      : smpl.lumi,
            "is_data"   : smpl.is_data,
            "legend"    : smpl.legend,
            "sample"    : smpl.name
        }
        builtin_dict.update(common_builtins)
        builtin_dict.update(smpl.cmsRun_builtin)

        # builtin, imports
        conf_lines += [
            "import __builtin__",
            "__builtin__.cms_var = %s" % repr(builtin_dict),
            "",
            "from " + self.cfg_filename + " import *",
            "",

        ]

        # do input filename statements
        conf_lines.append("process.source.fileNames = [")
        if not smpl.input_files:
            self.message(
                self.name,
                "WARNING input_files seems to be undefined for sample %s."
                % smpl.name
            )
        for in_file in smpl.input_files:
            if in_file[:5] == "file:":
                files_in_dir = glob.glob(in_file[5:])
                if not files_in_dir:
                    self.message(
                        "WARNING: no input files globbed for "+in_file[5:]
                    )
                    conf_lines.append("    '" + in_file.strip() + "',")
                else:
                    for fid in files_in_dir:
                        conf_lines.append("    'file:" + fid + "',")
            else:
                conf_lines.append("    '" + in_file.strip() + "',")
        conf_lines.append("]")

        # do output filename statements
        if smpl.output_file:
            filename = smpl.output_file
            if filename[-5:] != ".root":
                filename += self.name + ".root"
            conf_lines.append(
                "process."
                + output_module_name
                + ".fileName = '"
                + filename.strip()
                + "'"
            )

        # fileService statement
        if use_file_service:
            conf_lines.append(
                "process.TFileService.fileName = '"
                + self.service_filename
            )
            conf_lines.append("")

        # custom code
        conf_lines += smpl.cmsRun_add_lines

        # write out file
        with open(self.conf_filename, "w") as conf_file:
            for line in conf_lines:
                conf_file.write(line + "\n")

    def write_job_info(self, exit_code):
        if settings.recieved_sigint:
            return

        with open(self.jobinfo_filename, "w") as info_file:
            json.dump(
                {
                    "startTime": self.time_start,
                    "endTime": self.time_end,
                    "exitCode": str(exit_code),
                },
                info_file
            )

    def check_reuse_possible(self, check_for_file_service):
        if not self.try_reuse_data:
            return False
        if not os.path.exists(self.log_filename):
            return False
        if not os.path.exists(self.conf_filename):
            return False
        if (check_for_file_service and
                not os.path.exists(self.service_filename)):
            return False
        if not os.path.exists(self.jobinfo_filename):
            return False
        with open(self.jobinfo_filename) as info_file:
            info = json.load(info_file)
            if type(info) == dict and not int(info.get("exitCode", 255)):
                return True

    def successful(self):
        return (
            self.time_end
            and self.subprocess.returncode == 0
            and not settings.recieved_sigint
        )

    def finalize(self):
        self.time_end = time.ctime()
        if self.subprocess:
            if self.subprocess.returncode == 0 and self.log_file:
                self.log_file.close()
                self.log_file = None
                with open(self.log_filename, "r") as f:
                    if 'Exception ------' in "".join(f.readlines()):
                        self.subprocess.returncode = -1
        if self.log_file:
            self.log_file.close()
            self.log_file = None
            self.write_job_info(self.subprocess.returncode)

    def start(self):
        self.time_start = time.ctime()

        # delete jobinfo file
        if os.path.exists(self.jobinfo_filename):
            os.remove(self.jobinfo_filename)

        # aaand go for it!
        self.log_file = open(self.log_filename, "w")
        self.subprocess = subprocess.Popen(
            ["cmsRun", self.conf_filename]+self.sample.cmsRun_args,
            stdout=self.log_file,
            stderr=subprocess.STDOUT
        )

    def terminate(self):
        self.subprocess.terminate()


class CmsRun(toolinterface.Tool):
    """
    Tool to embed cmsRun execution into varial toolchains.

    For every job, a seperate CMSSW config is writen, that imports the given
    main config file.

    :param cfg_filename:        str, path to cmsRun-config,
                                e.g. `MySubSystem.MyPackage.config_cfg'`
    :param use_file_service:    bool, fileservice in CMSSW config?
                                default: ``True``
    :param output_module_name:  str, name of output module in CMSSW config
                                default: ``out``
    :param common_builtings:    dict, write to ``__builtin__`` section of the
                                config
                                default: ``None``
    :param name:                str, tool name
    """
    def __init__(self,
                 cfg_filename,
                 use_file_service=True,
                 output_module_name="out",
                 common_builtins=None,
                 name=None):
        super(CmsRun, self).__init__(name)
        self.waiting_pros = []
        self.running_pros = []
        self.finished_pros = []
        self.failed_pros = []
        self.cfg_filename = cfg_filename
        self.use_file_service = use_file_service
        self.output_module_name = output_module_name
        self.common_builtins = common_builtins or {}
        self.try_reuse = settings.try_reuse_results

    def wanna_reuse(self, all_reused_before_me):
        self._setup_processes()

        if settings.only_reload_results:
            return True

        return not bool(self.waiting_pros)

    def reuse(self):
        super(CmsRun, self).reuse()
        self._finalize()

    def run(self):
        if settings.suppress_eventloop_exec:
            self.message(
                self, "INFO settings.suppress_eventloop_exec == True, pass...")
            return
        if not (settings.not_ask_execute or raw_input(
                "Really run these cmsRun jobs:\n   "
                + ",\n   ".join(map(str, self.waiting_pros))
                + ('\nusing %i cores' % settings.max_num_processes)
                + "\n?? (type 'yes') "
                ) == "yes"):
            return

        self._handle_processes()
        sig_term_sent = False
        while self.running_pros:
            if settings.recieved_sigint and not sig_term_sent:
                self.abort_all_processes()
                sig_term_sent = True
            time.sleep(0.2)
            self._handle_processes()

        self.result = wrappers.Wrapper(
            finished_procs=list(p.name for p in self.finished_pros))
        self._finalize()

    def _setup_processes(self):
        for d in ('logs', 'confs', 'fs', 'report'):
            path = join(self.cwd, d)
            if not os.path.exists(path):
                os.mkdir(path)

        for name, smpl in analysis.all_samples.iteritems():
            process = CmsRunProcess(smpl, self.try_reuse, self.cfg_filename)
            if process.check_reuse_possible(self.use_file_service):
                self.finished_pros.append(process)
            else:
                self.waiting_pros.append(process)
                monitor.proc_enqueued(process)

    def _handle_processes(self):
        # start processing
        if (len(self.running_pros) < settings.max_num_processes
                and self.waiting_pros):
            process = self.waiting_pros.pop(0)
            process.prepare_run_conf(
                self.use_file_service,
                self.output_module_name,
                self.common_builtins
            )
            process.start()
            monitor.proc_started(process)
            self.running_pros.append(process)

        # finish processes
        for process in self.running_pros[:]:
            process.subprocess.poll()
            if None == process.subprocess.returncode:
                continue

            self.running_pros.remove(process)
            process.finalize()
            if process.successful():
                self.finished_pros.append(process)
                monitor.proc_finished(process)
            else:
                self.failed_pros.append(process)
                monitor.proc_failed(process)

    def _finalize(self):
        if settings.recieved_sigint:
            return
        if not self.use_file_service:
            return
        for process in self.finished_pros:
            analysis.fs_aliases += list(
                alias for alias in diskio.generate_fs_aliases(  # TODO fix i/o
                    process.service_filename,
                    process.sample
                )
            )

    def abort_all_processes(self):
        self.waiting_pros = []
        for process in self.running_pros:
            process.terminate()


#################################################################### Sample ###
import collections
import itertools
import inspect

class Sample(wrappers.WrapperBase):
    """
    Collect information about a sample.

    Either 'lumi' or 'x_sec' and 'n_events' must be given

    :param name:        str
    :param is_data:     bool (default: False)
    :param is_signal:   bool (default: False)
    :param lumi:        float
    :param x_sec:       float
    :param n_events:    int
    :param legend:      str (used to group samples as well, default: name)
    :param n_events:    int
    :param input_files: list of str

    Optional parameters for cmsRun configs:
    :param output_file:     str (event content out)
    :param cmsRun_builtin:  dict (variable to be attact to builtin of a config)
    :param cmsRun_add_lines: list of str (appended to cmsRun config)
    :param cmsRun_args:     list of str (command line arguments for cmsRun)
    """

    def __init__(self, **kws):
        self.__dict__.update({
            'is_data': False,
            'is_signal': False,
            'x_sec': 0.,
            'n_events': 0,
            'lumi': 0.,
            'legend': '',
            'input_files': [],
            'output_file': '',
            'cmsRun_builtin': {},
            'cmsRun_add_lines': [],
            'cmsRun_args': [],
        })
        self.__dict__.update(kws)
        # check/correct input
        assert(not(self.is_data and self.is_signal))  # both is forbidden!
        if not getattr(self, 'name', 0):
            self.name = self.__class__.__name__
        assert isinstance(self.cmsRun_add_lines, list)
        assert isinstance(self.cmsRun_args, list)
        assert isinstance(self.cmsRun_builtin, dict)
        assert (isinstance(self.input_files, list)
                or isinstance(self.input_files, tuple))
        if self.x_sec and self.n_events:
            self.lumi = self.n_events / float(self.x_sec)
        if not self.lumi:
            monitor.message(
                self.name,
                'WARNING lumi or (x_sec and n_events) seems to be undefined.'
            )
        if not self.legend:
            self.legend = self.name


def _check_n_load(field):
    if inspect.isclass(field) and issubclass(field, Sample):
        smp = field()
        if hasattr(smp, 'enable'):
            if smp.enable:
                return {smp.name: smp}
        elif settings.default_enable_sample:
            return {smp.name: smp}
    return {}


def load_samples(module):
    """
    Get sample instances from a module.

    :param module: modules to import samples from
    :type  module: module
    :returns:      dict of sample classes
    """
    samples = {}
    if isinstance(module, collections.Iterable):
        for mod in module:
            samples.update(load_samples(mod))
    else:
        for name in dir(module):
            if name[0] == '_':
                continue
            field = getattr(module, name)
            try:                    # handle iterable
                for f in field:
                    samples.update(_check_n_load(f))
            except TypeError:       # not an iterable
                samples.update(_check_n_load(field))
    return samples


def generate_samples(in_filenames, in_path='', out_path=''):
    """
    Generates samples for analysis.all_samples.

    The input filename without suffix will be taken as sample name.

    :param in_filenames:    names of inputfiles
    :param in_path:         input path
    :param out_path:        output path
    :returns:               dict of sample classes
    """
    if type(in_filenames) is str:
        in_filenames = [in_filenames]
    samples = {}
    for fname in in_filenames:
        basename    = os.path.basename(fname)
        samplename  = os.path.splitext(basename)[0]
        class sample_subclass(Sample):
            name = samplename
            lumi = 1.
            input_files = in_path + fname
            output_file = out_path
        samples[samplename] = sample_subclass
    return samples


def generate_samples_glob(glob_path, out_path):
    """Globs for files and creates according samples."""
    in_filenames = glob.glob(glob_path)
    in_filenames = itertools.imap(
        lambda t: 'file:' + t,  # prefix with 'file:' for cmssw
        in_filenames
    )
    return generate_samples(
        in_filenames,
        '',
        out_path
    )


########################################################## SampleNormalizer ###
from varial.toolinterface import Tool
from varial import generators as gen
from varial import analysis


class SampleNormalizer(Tool):
    """
    Normalize MC cross sections.

    With this tool all MC cross-section can be normalized to data, using one
    specific distribution. *Before* and *after* plots are stored as plots. The
    resulting factor is stored as result of this tool.

    :param filter_keyfunc:  lambda, keyfunction with one argument
    :param x_range_tuple:
    :param name:            str, tool name
    """
    can_reuse = False

    def __init__(self, filter_keyfunc, x_range_tuple, name=None):
        super(SampleNormalizer, self).__init__(name)
        self.filter_keyfunc = filter_keyfunc
        self.x_range = x_range_tuple

    def get_histos_n_factor(self):
        mcee, data = next(gen.fs_mc_stack_n_data_sum(
            self.filter_keyfunc
        ))
        dh, mh = data.histo, mcee.histo
        bins = tuple(dh.FindBin(x) for x in self.x_range)
        factor = dh.Integral(*bins) / mh.Integral(*bins)
        canv = next(gen.canvas(
            ((mcee, data),),
            default_decorators  # TODO rendering not using decorators anymore
        ))
        return factor, canv

    def run(self):
        # before
        factor, canv = self.get_histos_n_factor()
        next(gen.save_canvas_lin_log([canv], lambda _: 'before'))

        # alter samples
        for s in analysis.mc_samples().itervalues():
            s.lumi /= factor
            s.x_sec /= factor
        for a in analysis.fs_aliases:
            a.lumi /= factor

        # after
        _, canv = self.get_histos_n_factor()
        next(gen.save_canvas_lin_log([canv], lambda _: 'after'))

        self.result = wrappers.FloatWrapper(
            factor,
            name='Lumi factor'
        )


# TODO think about multiprocessing, in a dedicated light process
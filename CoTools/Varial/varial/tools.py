"""
All standard tools and toolschains accessible from this module.

Here's a breakdown of tools and utility methods:

=========================== =================================================
:ref:`toolinterface-module`
Tool                        baseclass for tools
ToolChain                   simple chain of Tool
ToolChainIndie              as ToolChain, will always reuse tools if possible
ToolChainVanilla            reset state of :ref:`analysis-module` at end
ToolChainParallel           parallel execution of independent tools
=========================== =================================================
:ref:`plotter-module`
Plotter                     generic plotter
RootFilePlotter             dump rootfile into plots (:ref:`plotter-module`)
mk_rootfile_plotter         function to create RootFilePlotter from path
=========================== =================================================
:ref:`webcreator-module`
Webcreator                  generate websites
=========================== =================================================
:ref:`tools-module`
Runner                      run a tool or toolchain ad-hoc.
PrintToolTree               print the tree of tools that has been run so far
UserInteraction             halt execution / get user input
HistoLoader                 load histograms from rootfiles or analysis
CopyTool                    copy/rsync disk content
=========================== =================================================
"""

from ast import literal_eval
import itertools
import shutil
import glob
import os

import generators as gen
import analysis
import wrappers
import pklio

from toolinterface import \
    Tool, \
    ToolChain, \
    ToolChainIndie, \
    ToolChainVanilla, \
    ToolChainParallel
from plotter import \
    Plotter, \
    RootFilePlotter, \
    mk_rootfile_plotter
from webcreator import \
    WebCreator


class Runner(ToolChain):
    """Runs tools upon instanciation (including proper folder creation)."""
    def __init__(self, tool, default_reuse=None):
        super(Runner, self).__init__(None, [tool], default_reuse)
        analysis.reset()
        self.run()
        if self._reuse:
            self.message('WARNING Finished reusing the last step '
                         '(please remove the folder of the first tool that should be rerun).')


class PrintToolTree(Tool):
    """Calls analysis.print_tool_tree()"""
    can_reuse = False

    def run(self):
        analysis.print_tool_tree()


class UserInteraction(Tool):
    def __init__(self,
                 prompt='Hit enter to continue. Kill me otherwise.',
                 eval_result=False,
                 can_reuse=True,
                 name=None):
        super(UserInteraction, self).__init__(name)
        self.prompt = prompt
        self.eval_result = eval_result
        self.can_reuse = can_reuse

    def run(self):
        if self.eval_result:
            self.message('INFO Input will be evaluated as python code.')
        if self.can_reuse:
            self.message('INFO Input might be reused.')
        res = raw_input(self.prompt+' ')
        if self.eval_result:
            res = literal_eval(res)
        self.result = wrappers.Wrapper(input=res)


class HistoLoader(Tool):
    """
    Loads histograms from any rootfile or from fileservice.

    :param name:                str, tool name
    :param pattern:             str, pattern for filesearch, e.g. ``*.root``,
                                default: None (load from fileservice)
    :param filter_keyfunc:      lambda, keyfunction with one argument,
                                default: ``None`` (load all histograms)
    :param hook_loaded_histos:  generator to be applied after loading,
                                default: ``None``
    :param io:                  io module,
                                default: ``dbio``
    """
    def __init__(self,
                 pattern=None,
                 input_result_path=None,
                 filter_keyfunc=None,
                 hook_loaded_histos=None,
                 raise_on_empty_result=True,
                 io=pklio,
                 name=None):
        super(HistoLoader, self).__init__(name)
        if pattern and input_result_path:
            raise RuntimeError(
                'ERROR either "pattern" or "input_result_path" must be None.')
        self.pattern = pattern
        self.input_result_path = input_result_path
        self.filter_keyfunc = filter_keyfunc
        self.hook_loaded_histos = hook_loaded_histos
        self.raise_on_empty_result = raise_on_empty_result
        self.io = io

    def run(self):
        if self.pattern:
            wrps = gen.dir_content(self.pattern)
            wrps = itertools.ifilter(self.filter_keyfunc, wrps)
            wrps = gen.load(wrps)
        elif self.input_result_path:
            wrps = self.lookup_result(self.input_result_path, [])
            if not wrps:
                raise RuntimeError(
                    'ERROR no histograms on path: ' + self.input_result_path)
            wrps = itertools.ifilter(self.filter_keyfunc, wrps)
        else:
            wrps = gen.fs_filter_active_sort_load(self.filter_keyfunc)

        if self.hook_loaded_histos:
            wrps = self.hook_loaded_histos(wrps)
        self.result = list(wrps)

        if not self.result:
            if self.raise_on_empty_result:
                raise RuntimeError('ERROR No histograms found.')
            else:
                self.message('ERROR No histograms found.')


class CopyTool(Tool):
    """
    Copy contents of a directory. Preserves .htaccess files.

    :param dest:            str, destination path
    :param src:             str, source path,
                            default: ``''`` (copy everything in same directory)
    :param ignore:          list,
                            default:
                            ``("*.root", "*.pdf", "*.eps", "*.log", "*.info")``
    :param wipe_dest_dir:   bool, default: ``True``
    :param name:            str, tool name
    """
    def __init__(self, dest, src='',
                 ignore=('*.root', '*.pdf', '*.eps', '*.log', '*.info', '*.pkl',
                         '*.db', '*.cfg', '*.tex', 'aliases.in.*', '.svn',
                         'webcreate_*',),
                 wipe_dest_dir=True,
                 name=None,
                 use_rsync=False):
        super(CopyTool, self).__init__(name)
        self.dest = dest.replace('~', os.getenv('HOME'))
        self.src = src.replace('~', os.getenv('HOME'))
        self.ignore = ignore
        self.wipe_dest_dir = wipe_dest_dir
        self.use_rsync = use_rsync

    def def_copy(self, src_objs, dest, ignore):
        ign_pat = shutil.ignore_patterns(*ignore)
        for src in src_objs:
            self.message('INFO Copying: ' + src)
            if os.path.isdir(src):
                f = os.path.basename(src)
                shutil.copytree(
                    src,
                    os.path.join(dest, f),
                    ignore=ign_pat,
                )
            else:
                shutil.copy2(src, dest)

    def run(self):
        if self.use_rsync:
            self.wipe_dest_dir = False
            self.ignore = list('--exclude='+w for w in self.ignore)
            cp_func = lambda w, x, y: os.system(
                'rsync -qavz --delete {0} {1} {2}'.format(
                    ' '.join(w), x, ' '.join(y)))
            dest = self.dest
        else:
            cp_func = self.def_copy
            dest = os.path.abspath(self.dest)

        if self.src:
            if self.src.startswith('..'):
                src = os.path.join(self.cwd, self.src)
            else:
                src = os.path.abspath(self.src)
            src_objs = glob.glob(src)
        elif self.cwd:
            src = os.path.abspath(os.path.join(self.cwd, '..'))
            src_objs = glob.glob(src + '/*')
        else:
            src = os.getcwd()
            src_objs = glob.glob(src + '/*')

        # check for htaccess and copy it to src dirs
        htaccess = os.path.join(dest, '.htaccess')
        if os.path.exists(htaccess):
            for src in src_objs:
                for path, _, _ in os.walk(src):
                    shutil.copy2(htaccess, path)

        # clean dest dir
        if self.wipe_dest_dir:
            src_basenames = list(os.path.basename(p) for p in src_objs)
            for f in glob.glob(dest + '/*'):
                if os.path.isdir(f) and os.path.basename(f) in src_basenames:
                    self.message('INFO Deleting: ' + f)
                    shutil.rmtree(f, True)

        # copy
        cp_func(src_objs, dest, self.ignore)

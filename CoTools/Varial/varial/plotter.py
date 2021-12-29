import collections
import itertools
import ROOT
import glob
import os

import generators as gen
import toolinterface
import rendering
import analysis
import settings
import sparseio
import monitor
import util


def rename_th2(wrps):
    for wrp in wrps:
        if 'TH2' in wrp.type:
            wrp.name += '_' + wrp.sample
            wrp.in_file_path += '_' + wrp.sample
        yield wrp


def plot_grouper_single_plots(wrps):
    for w in wrps:
        yield (w,)


def plot_grouper_by_name(wrps, separate_th2=True):
    if separate_th2:
        wrps = rename_th2(wrps)
    key = lambda w: w.name
    wrps = sorted(wrps, key=key)
    return gen.group(wrps, key_func=key)


def plot_grouper_by_in_file_path(wrps, separate_th2=True):
    if separate_th2:
        wrps = rename_th2(wrps)
    return gen.group(wrps, key_func=lambda w: w.in_file_path)


def plot_grouper_by_number_of_plots(wrps, n_per_group):
    class GroupKey(object):
        def __init__(self, n_per_group):
            self.n_th_obj = -1
            self.n_per_group = n_per_group
        def __call__(self, _):
            self.n_th_obj += 1
            return self.n_th_obj / self.n_per_group
    return gen.group(wrps, GroupKey(n_per_group))


def overlay_colorizer(wrps, colors=None):
    wrps = gen.apply_linecolor(wrps, colors)
    for w in wrps:
        w.histo.SetFillStyle(0)
        yield w


def default_plot_colorizer(grps, colors=None):
    grps = (gen.apply_linecolor(ws, colors) for ws in grps)
    grps = (gen.apply_markercolor(ws, colors) for ws in grps)
    return grps


def save_by_name(wrp):
    return wrp.name


def save_by_name_with_hash(wrp):
    return wrp.name + '_' + hex(hash(str(wrp.history)))[-6:]


class Plotter(toolinterface.Tool):
    """
    A plotter. Makes stacks and overlays data by default.

    Overriding set_up_content and setting self.stream_content lets
    Default attributes, that can be overwritten by init keywords:

    If both defaults for ``plot_grouper`` and ``save_name_func`` are kept, the
    latter is replaced with ``save_by_name_with_hash``.

    >>> defaults_attrs = {
    ...     'input_result_path': None,
    ...     'filter_keyfunc': None,
    ...     'load_func': gen.fs_filter_active_sort_load,
    ...     'hook_loaded_histos': None,
    ...
    ...     'stack': False,
    ...     'stack_grouper': plot_grouper_by_in_file_path,
    ...     'stack_setup': lambda w: gen.mc_stack_n_data_sum(w, None, True),
    ...     'plot_grouper': plot_grouper_single_plots,
    ...     'plot_setup': default_plot_colorizer,
    ...
    ...     'y_axis_scale': 'linlog',  # can be 'lin', 'log', or 'linlog'
    ...     'keep_content_as_result': False,
    ...     'save_name_func': save_by_name,
    ...     'canvas_post_build_funcs': (
    ...         settings.canvas_post_build_funcs
    ...         or rendering.post_build_funcs
    ...     ),    ... }
    """
    defaults_attrs = {
        'input_result_path': None,
        'filter_keyfunc': None,
        'load_func': gen.fs_filter_active_sort_load,
        'hook_loaded_histos': None,

        'stack': False,
        'stack_grouper': plot_grouper_by_in_file_path,
        'stack_setup': lambda w: gen.mc_stack_n_data_sum(w, None, True),
        'plot_grouper': plot_grouper_single_plots,
        'plot_setup': default_plot_colorizer,

        'y_axis_scale': 'linlog',  # can be 'lin', 'log', or 'linlog'
        'keep_content_as_result': False,
        'save_name_func': save_by_name,
        'canvas_post_build_funcs': (
            settings.canvas_post_build_funcs
            or rendering.post_build_funcs
        ),
    }

    class NoFilterDictError(Exception):
        pass

    def __init__(self, name=None, **kws):
        super(Plotter, self).__init__(name)
        defaults = dict(self.defaults_attrs)
        defaults.update(self.__dict__)  # do not overwrite user stuff
        defaults.update(kws)            # add keywords
        self.__dict__.update(defaults)  # set attributes in place
        self.stream_content = None

        assert(self.y_axis_scale in ('lin', 'log', 'linlog'))

        if self.stack:
            self.plot_setup = self.stack_setup
            self.plot_grouper = self.stack_grouper

        if (self.plot_grouper == plot_grouper_single_plots
            and self.save_name_func == save_by_name):
            self.save_name_func = save_by_name_with_hash

    def configure(self):
        pass

    def load_content(self):
        if self.input_result_path:
            if isinstance(self.input_result_path, str):
                wrps = self.lookup_result(self.input_result_path)
            elif isinstance(self.input_result_path, collections.Iterable):
                wrps = (w
                        for p in self.input_result_path
                        for w in self.lookup_result(p))
            else:
                raise RuntimeError(
                    'ERROR I do not understand input_result_path:%s'%
                    self.input_result_path)
            if not wrps:
                raise RuntimeError(
                    'ERROR Input not found: "%s"' % self.input_result_path)
        else:
            wrps = self.lookup_result('../HistoLoader')
        if wrps:
            if self.filter_keyfunc:
                wrps = itertools.ifilter(self.filter_keyfunc, wrps)
        else:
            wrps = self.load_func(self.filter_keyfunc)
        if self.hook_loaded_histos:
            wrps = self.hook_loaded_histos(wrps)
            if not wrps:
                raise RuntimeError('ERROR hook_loaded_histos returned None.')
        self.stream_content = list(wrps)
        if not self.stream_content:
            self.message('WARNING Could not load histogram content!')

    def group_content(self):
        wrps = self.stream_content
        if self.plot_grouper:
            wrps = list(self.plot_grouper(wrps))
        self.stream_content = list(wrps)
        if not self.stream_content:
            self.message('WARNING Could not group histogram content!')

    def setup_content(self):
        wrps = self.stream_content
        if self.plot_setup:
            wrps = self.plot_setup(wrps)
        self.stream_content = list(wrps)
        if not self.stream_content:
            self.message('WARNING Could not setup histogram content!')

    def store_content_as_result(self):
        if self.keep_content_as_result:
            self.stream_content = list(self.stream_content)
            self.result = list(
                itertools.chain.from_iterable(self.stream_content))

    def make_canvases(self):
        cnvs = gen.canvas(
            self.stream_content,
            post_build_funcs=self.canvas_post_build_funcs,
        )
        cnvs = gen.add_sample_integrals(cnvs)
        self.stream_content = cnvs

    def save_canvases(self):
        if self.y_axis_scale == 'log':
            self.stream_content = gen.switch_log_scale(self.stream_content)
        self.stream_content = sparseio.bulk_write(
            self.stream_content,
            self.save_name_func,
            linlog=(self.y_axis_scale == 'linlog')
        )
        count = gen.consume_n_count(self.stream_content)
        level = "INFO" if count else "WARNING"
        self.message("%s %s produced %d canvases." % (level, self.name, count))

    def run(self):
        self.configure()
        self.load_content()
        self.group_content()
        self.setup_content()
        self.store_content_as_result()
        self.make_canvases()
        self.save_canvases()


class RootFilePlotter(toolinterface.ToolChainParallel):
    """
    Plots all histograms in a rootfile.

    **NOTE: please use the** ``tools.mk_rootfile_plotter`` **function!**

    :param pattern:             str, search pattern for rootfiles
    :param plotter_factory:     factory function for RootFilePlotter
                                default: ``None``
    :param flat:                bool, flatten the rootfile structure
                                default: ``False``
    :param name:                str, tool name
    """
    def _setup_aliases(self, pattern, filter_keyfunc):
        aliases = gen.dir_content(pattern)
        if not aliases:
            self.message('WARNING Could not create aliases for plotting.')
        else:
            aliases = itertools.ifilter(
                lambda a: isinstance(a.type, str) and (
                    a.type.startswith('TH') or a.type == 'TProfile'
                ),
                aliases
            )
            aliases = itertools.ifilter(filter_keyfunc, aliases)
            aliases = sorted(
                aliases,
                key=lambda a: a.in_file_path
            )
        self.aliases = aliases

    def _setup_gen_legend(self, pattern, legendnames=None):
        if not legendnames:
            legendnames = util.setup_legendnames_from_files(pattern)

        # update colors (sorting needed, since dict is unsorted, and parallel
        # plotters should have the same result.
        for l in sorted(legendnames.itervalues()):
            analysis.get_color(l)

        legendnames = dict((os.path.basename(p), l)
                           for p, l in legendnames.iteritems())
        self.message(
            'INFO Legend names that I will use if not overwritten:\n'
            + '\n'.join('%32s: %s' % (v, k) for k, v in legendnames.iteritems())
        )

        def gen_apply_legend(wrps):
            for w in wrps:
                if not w.legend:
                    w.legend = legendnames[os.path.basename(w.file_path)]
                yield w
        return gen_apply_legend

    def _mk_flat_plotter(self, plotter_factory, load_func, gen_apply_legend):
        self._private_plotter = plotter_factory(
            name=self.name,
            load_func=lambda _: gen_apply_legend(load_func(gen.fs_content())),
            plot_grouper=plot_grouper_by_in_file_path,
            plot_setup=lambda ws: gen.mc_stack_n_data_sum(ws, lambda w: '', True),
            save_name_func=lambda w: w._renderers[0].in_file_path.replace('/', '_'),
        )

    def _mk_deep_plotter(self, plotter_factory, load_func, gen_apply_legend):
        all_in_file_paths = set(
            '/'.join(a.in_file_path.split('/')[:-1])  # drop histo name
            for a in self.aliases
        )
        for path in all_in_file_paths:
            rfp = self  # start for basedir
            path = path.split('/')

            # walk over path elements and create RootFilePlotter instances
            for folder in path:
                if not folder:
                    continue
                if folder not in rfp.tool_names:
                    rfp.add_tool(RootFilePlotter(None, None, plotter_factory, name=folder))
                rfp = rfp.tool_names[folder]

            # This function creates a separate namespace for p
            # (the last reference to p would be lost otherwise)
            def _mk_private_loader(p):
                if p == ['']:
                    p = []  # for the base-folder, w.in_file_path.split('/')[:-1] will be []
                def loader(filter_keyfunc):
                    filter_keyfunc = filter_keyfunc or (lambda w: True)
                    wrps = analysis.fs_aliases
                    wrps = itertools.ifilter(
                        lambda w: w.in_file_path.split('/')[:-1] == p and filter_keyfunc(w),
                        wrps
                    )
                    wrps = load_func(wrps)
                    wrps = gen_apply_legend(wrps)
                    return wrps
                return loader

            # make private plotter instance if not done already
            # private plotters are needed, as RootFilePlotter is a subclass
            # of ToolChain, not Tool itself.
            rfp._private_plotter = plotter_factory(
                name=rfp.name,
                plot_grouper=plot_grouper_by_in_file_path,
                load_func=_mk_private_loader(path),
                save_name_func=lambda w: w.name,
            )

    def __init__(self,
                 pattern=None,
                 input_result_path=None,
                 plotter_factory=None,
                 flat=False,
                 name=None,
                 filter_keyfunc=lambda w: True,
                 auto_legend=True,
                 legendnames=None):
        super(RootFilePlotter, self).__init__(name)

        # initialization for all instances
        self._private_plotter = None
        self._is_base_instance = bool(pattern or input_result_path)
        if not self._is_base_instance:
            return

        # initialization for base instance only
        assert(bool(pattern) != bool(input_result_path)), 'only one possible!'
        ROOT.gROOT.SetBatch()
        if not plotter_factory:
            plotter_factory = Plotter

        if input_result_path:
            wrps = self.lookup_result(input_result_path)
            if not wrps:
                analysis.print_tool_tree()
                raise RuntimeError(
                    'no input found for input_result_path "%s". (Check tool tree above)'
                    % input_result_path)
            self.aliases = list(w for w in wrps if filter_keyfunc(w))
            load_func = lambda wrps: wrps  # histograms are already loaded
        else:
            self._setup_aliases(pattern, filter_keyfunc)
            load_func = gen.load  # will load histogram for given alias

        if auto_legend and pattern:
            gen_apply_legend = self._setup_gen_legend(pattern, legendnames)
        else:
            gen_apply_legend = lambda wrps: wrps

        if flat:
            # either print all in one dir
            self._mk_flat_plotter(plotter_factory, load_func, gen_apply_legend)
        else:
            # or resemble dirs of the root file
            self._mk_deep_plotter(plotter_factory, load_func, gen_apply_legend)

    def run(self):
        old_aliases = analysis.fs_aliases
        if self._is_base_instance:
            analysis.fs_aliases = self.aliases
        super(RootFilePlotter, self).run()
        if self._private_plotter:
            logfile = '%s/.pltr_done' % analysis.cwd
            if self._reuse and os.path.exists(logfile):
                self.message('INFO reusing...')
            else:
                self._reuse = False
                if os.path.exists(logfile):
                    os.remove(logfile)
                self._private_plotter.run()
                self._private_plotter._write_result()
                with open(logfile, 'w') as f:
                    f.write('plotter done.\n')
        if self._is_base_instance:
            analysis.fs_aliases = old_aliases


def mk_rootfile_plotter(name="RootFilePlots",
                        pattern=None,
                        input_result_path=None,
                        flat=False,
                        plotter_factory=None,
                        combine_files=False,
                        filter_keyfunc=lambda w: True,
                        auto_legend=True,
                        legendnames=None,
                        **kws):
    """
    Make a plotter chain that plots all content of all rootfiles in cwd.

    Additional keywords are forwarded to the plotter instanciation.
    For running the plotter(s), use a Runner.

    :param name:                str, name of the folder in which the output is
                                stored
    :param pattern:             str, search pattern for rootfiles,
                                default: ``*.root``
    :param flat:                bool, flatten the rootfile structure
                                default: ``False``
    :param plotter_factory:     factory function for RootFilePlotter
                                default: ``None``
    :param combine_files:       bool, plot same histograms across rootfiles
                                into the same canvas. Does not work together
                                with ``flat`` option,
                                default: ``False``
    """
    def plotter_factory_kws(**kws_fctry):
        kws_fctry.update(kws)
        if plotter_factory:
            return plotter_factory(**kws_fctry)
        else:
            return Plotter(**kws_fctry)

    if kws:
        new_plotter_factory = plotter_factory_kws
    else:
        new_plotter_factory = plotter_factory

    if combine_files:
        tc = RootFilePlotter(
            pattern,
            input_result_path,
            new_plotter_factory,
            flat,
            name,
            filter_keyfunc,
            auto_legend,
            legendnames
        )
    else:
        plotters = list(
            RootFilePlotter(
                f,
                input_result_path,
                new_plotter_factory,
                flat,
                f[:-5].split('/')[-1],
                filter_keyfunc,
                auto_legend,
                legendnames
            )
            for f in glob.iglob(pattern)
        )
        if not plotters:
            monitor.message('plotter.mk_rootfile_plotter',
                            'WARNING no plotters generated for pattern: %s'
                            % pattern)
        tc = toolinterface.ToolChainParallel(name, plotters)
    return tc


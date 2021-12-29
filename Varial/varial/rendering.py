"""
From histogram data to graphical plots.

The members of this package make plots from histograms or other wrapped
ROOT-objects. The 'Renderers' extend the functionality of wrappers for drawing.
"""


################################################################# renderers ###
import collections
import wrappers
import ROOT
from math import sqrt


class Renderer(object):
    """
    Baseclass for rendered wrappers.
    """
    def __init__(self, wrp):
        self.val_x_min = 0.
        self.val_x_max = 0.
        self.val_y_min = 0.
        self.val_y_max = 0.
        self.__dict__.update(wrp.__dict__)

    def x_min(self):
        return self.val_x_min

    def x_max(self):
        return self.val_x_max

    def y_min(self):
        return self.val_y_min

    def y_max(self):
        return self.val_y_max

    def y_min_gr_zero(self):
        return self.y_min()

    def draw(self, option=''):
        pass


class HistoRenderer(Renderer, wrappers.HistoWrapper):
    """
    Extend HistoWrapper for drawing.
    """
    def __init__(self, wrp):
        super(HistoRenderer, self).__init__(wrp)

        if self.histo_sys_err:                          # calculate total error
            nom, sys, tot = self.histo, self.histo_sys_err, self.histo.Clone()
            for i in xrange(tot.GetNbinsX()+2):
                nom_val = nom.GetBinContent(i)
                nom_err = nom.GetBinError(i) or 1e-10   # prevent 0-div-error
                sys_val = sys.GetBinContent(i)
                sys_err = sys.GetBinError(i) or 1e-10   # prevent 0-div-error
                nom_wei = nom_err**2 / (nom_err**2 + sys_err**2)
                sys_wei = sys_err**2 / (nom_err**2 + sys_err**2)

                # weighted mean of values and quadratic sum of errors
                tot.SetBinContent(i, nom_wei*nom_val + sys_wei*sys_val)
                tot.SetBinError(i, (nom_err**2 + sys_err**2)**.5)

            self.histo_tot_err = tot
            settings.sys_error_style(self.histo_sys_err)
            settings.tot_error_style(self.histo_tot_err)

        if getattr(wrp, 'draw_option', 0):
            self.draw_option = wrp.draw_option
        elif 'TH2' in wrp.type:
            self.draw_option = 'colz'
        elif self.is_data or self.is_pseudo_data:
            self.draw_option = 'E0X0'
            self.draw_option_legend = 'p'
            if self.is_pseudo_data:
                wrp.histo.SetMarkerStyle(4)
        else:
            self.draw_option = 'hist'

    def x_min(self):
        return self.val_x_min or self.histo.GetXaxis().GetXmin()

    def x_max(self):
        return self.val_x_max or self.histo.GetXaxis().GetXmax()

    def y_min(self):
        # > 0 cuts away half numbers
        return self.val_y_min or 1e-10

    def y_max(self):
        return self.val_y_max or self.histo.GetMaximum()

    def y_min_gr_zero(self, histo=None):
        if not histo:
            histo = self.histo
        nbins = histo.GetNbinsX()
        min_val = histo.GetMinimum()  # min on y axis
        if min_val < 1e-10 < histo.GetMaximum():  # should be greater than zero
            try:
                min_val = min(
                    histo.GetBinContent(i)
                    for i in xrange(nbins + 1)
                    if histo.GetBinContent(i) > 1e-10
                )
            except ValueError:
                min_val = 1e-10
        return min_val

    def draw(self, option=''):
        obj = getattr(self, 'graph_draw', self.histo)
        obj.Draw(self.draw_option + option)


class StackRenderer(HistoRenderer, wrappers.StackWrapper):
    """
    Extend StackWrapper for drawing.
    """
    def __init__(self, wrp):
        super(StackRenderer, self).__init__(wrp)
        settings.stat_error_style(self.histo)
        self.draw_option = getattr(wrp, 'draw_option', 'hist')
        self.draw_option_sum = getattr(wrp, 'draw_option_sum', 'sameE2')

    def y_min_gr_zero(self, histo=None):
        return super(StackRenderer, self).y_min_gr_zero(
            self.stack.GetHists()[0]
        )

    def y_max(self):
        if self.histo_sys_err:
            return self.val_y_max or self.histo_tot_err.GetMaximum()
        else:
            return super(StackRenderer, self).y_max()

    def draw(self, option=''):
        for h in self.stack.GetHists():
            h.SetLineColor(ROOT.kGray)
        self.stack.Draw(self.draw_option + option)
        self.stack.GetXaxis().SetTitle(self.histo.GetXaxis().GetTitle())
        self.stack.GetYaxis().SetTitle(self.histo.GetYaxis().GetTitle())
        if self.histo_sys_err:
            self.histo_tot_err.Draw(self.draw_option_sum)
            # self.histo_sys_err.Draw(self.draw_option_sum)
        else:
            self.histo.Draw(self.draw_option_sum)


class GraphRenderer(Renderer, wrappers.GraphWrapper):
    """
    Extend GraphWrapper for drawing.
    """
    def __init__(self, wrp):
        super(GraphRenderer, self).__init__(wrp)
        if hasattr(wrp, 'draw_option'):
            self.draw_option = wrp.draw_option
        else:
            self.draw_option = 'P'

    def x_min(self):
        return self.val_x_min or self.graph.GetXaxis().GetXmin()

    def x_max(self):
        return self.val_x_max or self.graph.GetXaxis().GetXmax()

    def y_min(self):
        # > 0 cuts away half numbers
        return self.val_y_min or self.graph.GetYaxis().GetXmin() + 1e-10

    def y_max(self):
        return self.val_y_max or self.graph.GetYaxis().GetXmax()

    def draw(self, option=''):
        if 'same' in option:
            option.replace('same', '')
        else:
            option += 'A'
        self.graph.Draw(self.draw_option + option)


################################################# canvas-building functions ###
import settings
import history
import util


def _renderize(wrp):
    if isinstance(wrp, Renderer):
        return wrp
    if isinstance(wrp, wrappers.GraphWrapper):
        return GraphRenderer(wrp)
    if isinstance(wrp, wrappers.StackWrapper):
        return StackRenderer(wrp)
    if isinstance(wrp, wrappers.HistoWrapper):
        return HistoRenderer(wrp)


def _renderize_iter(wrps):
    rnds = []
    for wrp in wrps:
        rnds.append(_renderize(wrp))
    return rnds


def _track_canvas_history(rnds, kws):
    list_of_histories = []
    for rnd in rnds:
        list_of_histories.append(rnd.history)
    hstry = history.History('build_canvas')
    hstry.add_args(list_of_histories)
    hstry.add_kws(kws)
    return hstry


def setup(wrps, kws):
    """Scan ROOT-objects for x and y bounds."""
    pbfs = kws.pop('post_build_funcs', [])

    if not isinstance(wrps, collections.Iterable):
        raise RuntimeError('setup wants iterable of wrps!')

    # only one stack, which should be one first place
    wrps = sorted(wrps, key=lambda r: not isinstance(r, wrappers.StackWrapper))
    if len(wrps) > 1 and isinstance(wrps[1], wrappers.StackWrapper):
        raise RuntimeError('At most one StackWrapper allowed, it must be in first place.')

    # instanciate..
    rnds = list(_renderize_iter(wrps))
    canvas = ROOT.TCanvas(
        rnds[0].name + '_' + util.random_hex_str(),
        rnds[0].title,
        settings.canvas_size_x,
        settings.canvas_size_y,
    )

    # collect info
    info = rnds[0].all_info()  # TODO only common info
    for attr in ('is_signal', 'is_data', 'is_pseudo_data'):
        if attr in info:
            del info[attr]
    info.update(kws)
    info.update({
        'name'        : rnds[0].name,
        'title'       : rnds[0].title,
        'in_file_path': rnds[0].in_file_path,
        'main_pad'    : canvas,
        'second_pad'  : None,
        'legend'      : None,
        'first_obj'   : None,
        'x_bounds'    : None,
        'y_bounds'    : None,
        'y_min_gr_0'  : 1e-10,
        'history'     : _track_canvas_history(rnds, kws),
        '_renderers'  : rnds,
    })
    wrp = wrappers.CanvasWrapper(canvas, **info)

    for sf in pbfs:
        if getattr(sf, 'setup', 0):
            sf.setup(wrp, kws)
    return wrp


def find_x_y_bounds(wrp, _):
    """Scan ROOT-objects for x and y bounds."""
    rnds = wrp._renderers
    x_min = min(r.x_min() for r in rnds)
    x_max = max(r.x_max() for r in rnds)
    wrp.x_bounds = x_min, x_max
    y_min = min(r.y_min() for r in rnds)
    y_max = max(r.y_max() for r in rnds)
    wrp.y_bounds = y_min, y_max
    wrp.y_min_gr_0 = min(r.y_min_gr_zero() for r in rnds)
    return wrp


def draw_content(wrp, _):
    for i, rnd in enumerate(wrp._renderers):
        if not i:
            first_obj = rnd.obj
            first_obj.SetTitle('')
            rnd.draw('')
            settings.apply_axis_style(first_obj, wrp.y_bounds)
            wrp.first_obj = first_obj
        else:
            rnd.draw('same')

    return wrp


##################################################### canvas customizations ###
import operations as op


class PostBuildFuncWithSetup(object):
    def __init__(self, func, setup_funcs):
        self.func = func
        self.setup_funcs = setup_funcs

    def __call__(self, *args, **kws):
        return self.func(*args, **kws)

    def setup(self, *args, **kws):
        for f in self.setup_funcs:
            f(*args, **kws)


def mk_tobject_draw_func(tobject, *draw_opts):
    """
    Draw any TObject. Like a TLatex.

    e.g:
    ``rendering.post_build_funcs += [rendering.mk_tobject_draw_func(``
    ``    ROOT.TLatex(0.5, 0.5, 'My Box')``
    ``)]``
    """
    assert isinstance(tobject, ROOT.TObject), '"tobject" arg must be a TObject'

    def tobject_draw_func(wrp, _):
        tobject.Draw(*draw_opts)
        return wrp

    return tobject_draw_func


def mk_titlebox_func(text):
    """
    Draws title-box with TPaveText above canvas window.

    e.g:
    ``rendering.post_build_funcs += [rendering.mk_titlebox_func('my text')]``
    """
    assert isinstance(text, str), '"text" arg must be a string'

    def titlebox_func(wrp, _):
        titlebox = ROOT.TPaveText(0.5, 0.90, 0.98, 1.0, 'brNDC')
        titlebox.AddText(text)
        titlebox.SetTextSize(0.042)
        titlebox.SetFillStyle(0)
        titlebox.SetBorderSize(0)
        titlebox.SetTextAlign(31)
        titlebox.SetMargin(0.0)
        titlebox.SetFillColor(0)
        wrp.canvas.cd()
        titlebox.Draw('SAME')
        wrp.main_pad.cd()
        wrp.titlebox = titlebox
        return wrp

    return titlebox_func


def mk_legend_func(**outer_kws):
    """
    Adds a legend to the main_pad.

    Takes entries from ``self.main_pad.BuildLegend()`` .
    The box height is adjusted by the number of legend entries.
    No border and no shadow is printed.

    You can set ``draw_option_legend`` on a wrapper. If it evaluates to
    ``False`` (like an empty string), the item will be removed from the legend.

    All default settings in ``settings.defaults_Legend`` can be overwritten by
    providing an argument with the same name, e.g. ``mk_legend_func(x_pos=0.2)``.
    """
    def make_entry_tupels(rnds, legend, par):
        entries = []
        for entry in legend.GetListOfPrimitives():
            obj = entry.GetObject()
            label = entry.GetLabel()
            draw_opt = par['opt']
            for rnd in rnds:

                # match legend entries to renderers
                if getattr(rnd, 'graph_draw', rnd.obj) is not obj:
                    continue

                if isinstance(rnd, StackRenderer):
                    continue

                if rnd.is_data:
                    draw_opt = par['opt_data']
                else:
                    draw_opt = 'l'

                if hasattr(rnd, 'legend'):
                    label = rnd.legend
                if hasattr(rnd, 'draw_option_legend'):
                    draw_opt = rnd.draw_option_legend
                break

            if draw_opt:  # empty string -> no legend entry
                entries.append((obj, label, draw_opt))
        return entries

    def calc_bounds(n_entries, par):
        if 'xy_coords' in par:
            xy = par['xy_coords']
            assert len(xy) == 4 and all(isinstance(z, float) for z in xy)
            return xy
        else:
            x_pos   = par['x_pos']
            y_pos   = par['y_pos']
            width   = par['label_width']
            height  = par['label_height'] * n_entries
            if y_pos + height/2. > 1.:
                y_pos = 1 - height/2. # do not go outside canvas
            return (
                x_pos - width/2.,
                y_pos - height/2.,
                x_pos + width/2.,
                y_pos + height/2.,
            )

    def legend_func(wrp, kws):
        par = dict(settings.defaults_Legend)
        par.update(outer_kws)
        par.update(kws)

        # get legend entry objects
        tmp_leg = wrp.main_pad.BuildLegend(0.1, 0.6, 0.5, 0.8)
        entries = make_entry_tupels(wrp._renderers, tmp_leg, par)
        tmp_leg.Clear()
        wrp.main_pad.GetListOfPrimitives().Remove(tmp_leg)
        tmp_leg.Delete()

        # create a new legend
        bounds = calc_bounds(len(entries), par)
        legend = ROOT.TLegend(*bounds)
        legend.SetBorderSize(0)
        legend.SetTextSize(
            par.get('text_size', settings.box_text_size))
        if 'text_font' in par:
            legend.SetTextFont(par['text_font'])
        if par['reverse']:
            entries.reverse()
        for obj, label, draw_opt in entries:
            legend.AddEntry(obj, label, draw_opt)
        wrp.canvas.cd()
        legend.Draw()
        wrp.main_pad.cd()
        wrp.legend = legend
        return wrp

    return legend_func


def bottom_plot_canv_ok(wrp, *_):
    # prioritize on cached result
    is_ok = getattr(wrp, '_bottom_plot_canv_check_ok', -1)
    if is_ok == -1:
        wrp._bottom_plot_canv_check_ok = (
            len(wrp._renderers) > 1 and
            isinstance(wrp._renderers[0], wrappers.HistoWrapper) and
            isinstance(wrp._renderers[1], wrappers.HistoWrapper) and
            'TH2' not in wrp._renderers[0].type
        )
        return wrp._bottom_plot_canv_check_ok
    else:
        return is_ok


def bottom_plot_canv_ok_data(wrp, _):
    is_ok = bottom_plot_canv_ok(wrp)
    if is_ok and sum(w.is_data for w in wrp._renderers) == 1:
        return True
    else:
        wrp._bottom_plot_canv_check_ok = False
        return False


def _bottom_plot_make_pad(wrp):
    if not bottom_plot_canv_ok(wrp):
        return False

    if wrp.second_pad:
        return True

    name = wrp.name
    wrp.second_pad = ROOT.TPad(
        'bottom_pad_' + name,
        'bottom_pad_' + name,
        0, 0, 1, 0.25
    )
    settings.apply_split_pad_styles(wrp)
    wrp.canvas.cd()
    wrp.second_pad.Draw()
    wrp.main_pad.cd()
    return True


def _bottom_plot_y_bounds(wrp, bottom_obj, par):
    y_min, y_max = par['y_min'], par['y_max']

    if par['force_y_range']:
        bottom_obj.GetYaxis().SetRangeUser(y_min, y_max)

    elif isinstance(bottom_obj, ROOT.TH1):
        n_bins = bottom_obj.GetNbinsX()
        mini = min(bottom_obj.GetBinContent(i+1)
                   - bottom_obj.GetBinError(i+1) for i in xrange(n_bins)) - .1
        maxi = max(bottom_obj.GetBinContent(i+1)
                   + bottom_obj.GetBinError(i+1) for i in xrange(n_bins)) + .1
        if mini < y_min or maxi > y_max:
            y_min, y_max = max(y_min, mini), min(y_max, maxi)
            bottom_obj.GetYaxis().SetRangeUser(y_min, y_max)

    wrp.y_min_max = y_min, y_max


def _bottom_plot_fix_bkg_err_values(wrp, histo):
    # errors are not plottet, if the bin center is out of the y bounds.
    # this function fixes it.
    y_min, y_max = wrp.y_min_max
    for i in xrange(1, histo.GetNbinsX() + 1):
        val = histo.GetBinContent(i)
        new_val = 0
        if val <= y_min:
            new_val = y_min * 0.99
        elif val >= y_max:
            new_val = y_max * 0.99
        if new_val:
            new_err = histo.GetBinError(i) - abs(new_val - val)
            new_err = max(new_err, 0)  # may not be negative
            histo.SetBinContent(i, new_val)
            histo.SetBinError(i, new_err)
    settings.set_bottom_plot_general_style(histo)
    histo.GetYaxis().SetRangeUser(y_min, y_max)


def bottom_plot_prep_main_pad(wrp, _):
    if not bottom_plot_canv_ok(wrp) or wrp.main_pad != wrp.canvas:
        return

    # make separate main pad
    main_pad = ROOT.TPad(
        'main_pad_' + wrp._renderers[0].name,
        'main_pad_' + wrp._renderers[0].name,
        0, 0, 1, 1
    )
    wrp.canvas.cd()
    main_pad.Draw()
    main_pad.cd()
    wrp.main_pad = main_pad


def bottom_plot_get_div_hists(rnds):
    data_rnds = list(r for r in rnds if r.is_data or r.is_pseudo_data)
    if data_rnds:
        assert len(data_rnds) == 1, 'can only have one data histogram if ratio is used.'
        bkg_rnds = list(r for r in rnds if r.is_background)
        assert len(bkg_rnds) == 1, 'can only have one background histogram if ratio is used.'
        return bkg_rnds + data_rnds
    else:
        return rnds[1], rnds[0]


def mk_ratio_plot_func(**outer_kws):
    """
    Ratio of first and second histogram in canvas.
    """
    def make_bottom_hist(cnv_wrp, kws):
        if not bottom_plot_canv_ok(cnv_wrp):
            return cnv_wrp

        par = dict(settings.defaults_BottomPlot)
        par.update(outer_kws)
        par.update(kws)
        cnv_wrp._par_mk_ratio_plot_func = par

        rnds = cnv_wrp._renderers
        div_wrp = op.div(bottom_plot_get_div_hists(rnds))
        div_wrp.histo.SetYTitle(par['y_title'] or (
            '#frac{Data}{MC}' if rnds[1].is_data else 'Ratio'))

        cnv_wrp.bottom_hist = div_wrp.histo
        settings.set_bottom_plot_general_style(cnv_wrp.bottom_hist)
        settings.set_bottom_plot_ratio_style(cnv_wrp.bottom_hist)
        _bottom_plot_y_bounds(cnv_wrp, cnv_wrp.bottom_hist, par)

    def ratio_plot_func(cnv_wrp, _):
        if not _bottom_plot_make_pad(cnv_wrp):
            return cnv_wrp

        par = cnv_wrp._par_mk_ratio_plot_func
        del cnv_wrp._par_mk_ratio_plot_func

        # draw histo
        cnv_wrp.second_pad.cd()
        cnv_wrp.bottom_hist.Draw(par['draw_opt'])
        cnv_wrp.main_pad.cd()
        return cnv_wrp

    return PostBuildFuncWithSetup(
        ratio_plot_func,
        (bottom_plot_prep_main_pad, make_bottom_hist)
    )


# util functions for err_ratio_plot_func's:
def _err_ratio_util_mk_bkg_errors(histo, ref_histo):
    for i in xrange(1, histo.GetNbinsX() + 1):
        val = histo.GetBinContent(i)
        ref_val = ref_histo.GetBinContent(i)
        err = histo.GetBinError(i)
        histo.SetBinContent(i, (val-ref_val)/(ref_val or 1e20))
        histo.SetBinError(i, err/(ref_val or 1e20))
    return histo

def _err_ratio_util_mk_sys_tot_histos(cnv_wrp, mcee_rnd):
    sys_histo = mcee_rnd.histo_sys_err.Clone()
    _err_ratio_util_mk_bkg_errors(sys_histo, mcee_rnd.histo)
    settings.sys_error_style(sys_histo)
    _bottom_plot_fix_bkg_err_values(cnv_wrp, sys_histo)

    tot_histo = mcee_rnd.histo_tot_err.Clone()
    _err_ratio_util_mk_bkg_errors(tot_histo, mcee_rnd.histo)
    settings.tot_error_style(tot_histo)
    _bottom_plot_fix_bkg_err_values(cnv_wrp, tot_histo)

    cnv_wrp.bottom_hist_stt_err = None
    cnv_wrp.bottom_hist_sys_err = sys_histo
    cnv_wrp.bottom_hist_tot_err = tot_histo

def _err_ratio_util_mk_stat_histo(cnv_wrp, mcee_rnd):
    stt_histo = mcee_rnd.histo.Clone()
    _err_ratio_util_mk_bkg_errors(stt_histo, stt_histo)
    settings.stat_error_style(stt_histo)
    _bottom_plot_fix_bkg_err_values(cnv_wrp, stt_histo)

    cnv_wrp.bottom_hist_stt_err = stt_histo
    cnv_wrp.bottom_hist_sys_err = None
    cnv_wrp.bottom_hist_tot_err = None

def _err_ratio_util_mk_sys_stt_histos(cnv_wrp, mcee_rnd):
    if mcee_rnd.histo_sys_err:                      # w/ sys uncerts
        _err_ratio_util_mk_sys_tot_histos(cnv_wrp, mcee_rnd)
    else:                                           # w/o sys uncerts
        _err_ratio_util_mk_stat_histo(cnv_wrp, mcee_rnd)

def _err_ratio_util_plot_sys_stt_histos(cnv_wrp, par):
    h = cnv_wrp.bottom_hist_stt_err or cnv_wrp.bottom_hist_tot_err
    h.Draw('sameE2')
    h.GetYaxis().SetTitle(par['y_title'])
    if par.get('draw_sys_sep', 0):
        cnv_wrp.bottom_hist_sys_err.Draw('sameE2')


def mk_split_err_ratio_plot_func(**outer_kws):
    """
    Ratio of stack and *data* with uncertainties split up.
    """

    def mk_poisson_errs_graph(cnv_wrp, data_rnd, div_hist, mc_histo_no_err, par):
        data_hist = data_rnd.histo
        data_hist.SetBinErrorOption(ROOT.TH1.kPoisson)  # TODO: poisson erros for main histo
        data_hist.Sumw2(False)                          # should be set elsewhere!
        gtop = ROOT.TGraphAsymmErrors(data_hist)
        gbot = ROOT.TGraphAsymmErrors(div_hist)
        for i in xrange(mc_histo_no_err.GetNbinsX(), 0, -1):
            mc_val = mc_histo_no_err.GetBinContent(i)
            if mc_val:
                e_up = data_hist.GetBinErrorUp(i)
                e_lo = data_hist.GetBinErrorLow(i)
                gtop.SetPointError(i - 1, 0., 0., e_lo, e_up)
                gbot.SetPointError(i - 1, 0., 0., e_lo/mc_val, e_up/mc_val)
            else:
                gtop.RemovePoint(i - 1)
                gbot.RemovePoint(i - 1)

        data_hist.Sumw2()
        data_rnd.graph_draw = gtop
        data_rnd.draw_option = '0P'
        par['draw_opt'] = '0P'
        h_x_ax, g_x_ax = div_hist.GetXaxis(), gbot.GetXaxis()
        g_x_ax.SetTitle(h_x_ax.GetTitle())
        g_x_ax.SetRangeUser(h_x_ax.GetXmin(), h_x_ax.GetXmax())
        settings.set_bottom_plot_ratio_style(gbot)
        cnv_wrp.bottom_graph = gbot
        return gbot

    def make_bottom_hist(cnv_wrp, kws):
        if not bottom_plot_canv_ok(cnv_wrp):
            return cnv_wrp

        par = dict(settings.defaults_BottomPlot)
        par.update(outer_kws)
        par.update(kws)
        par['y_title'] = par.get('y_title', '') or '#frac{Data-MC}{MC}'
        cnv_wrp._par_mk_split_err_ratio_plot_func = par


        rnds = cnv_wrp._renderers
        mcee_rnd, data_rnd = bottom_plot_get_div_hists(rnds)

        # overlaying ratio histogram
        mc_histo_no_err = mcee_rnd.histo.Clone()
        mc_histo_no_err.GetXaxis().SetCanExtend(0)
        data_hist = data_rnd.histo
        div_hist = data_hist.Clone()
        div_hist.GetXaxis().SetCanExtend(0)
        div_hist.Sumw2()
        for i in xrange(1, mc_histo_no_err.GetXaxis().GetNbins()+1):
            mc_histo_no_err.SetBinError(i, 0.)
            if not div_hist.GetBinContent(i):
                div_hist.SetBinError(i, 1.)
        div_hist.Add(mc_histo_no_err, -1)
        div_hist.Divide(mc_histo_no_err)

        settings.set_bottom_plot_ratio_style(div_hist)
        _bottom_plot_y_bounds(cnv_wrp, div_hist, par)
        cnv_wrp.bottom_hist = div_hist

        # underlying error bands
        _err_ratio_util_mk_sys_stt_histos(cnv_wrp, mcee_rnd)

        # poisson errs or not..
        if par['poisson_errs']:
            mk_poisson_errs_graph(cnv_wrp, data_rnd, div_hist, mc_histo_no_err, par)

        # ugly fix: move zeros out of range
        for i in xrange(1, mc_histo_no_err.GetNbinsX()+1):
            if not (div_hist.GetBinContent(i) or div_hist.GetBinError(i)):
                div_hist.SetBinContent(i, -500)

    def ratio_plot_func(cnv_wrp, _):
        if not _bottom_plot_make_pad(cnv_wrp):
            return cnv_wrp

        par = cnv_wrp._par_mk_split_err_ratio_plot_func
        del cnv_wrp._par_mk_split_err_ratio_plot_func

        # draw bottom histos
        cnv_wrp.second_pad.cd()
        _err_ratio_util_plot_sys_stt_histos(cnv_wrp, par)
        if par['poisson_errs']:
            cnv_wrp.bottom_graph.Draw('same' + par['draw_opt'])
        else:
            cnv_wrp.bottom_hist.Draw('same' + par['draw_opt'])
        cnv_wrp.main_pad.cd()
        return cnv_wrp

    return PostBuildFuncWithSetup(
        ratio_plot_func,
        (bottom_plot_canv_ok_data, bottom_plot_prep_main_pad, make_bottom_hist)
    )


def mk_split_err_multi_ratio_plot_func(**outer_kws):
    """
    Ratio for many histograms with uncertainties split up.
    """

    def make_bottom_hists(cnv_wrp, par):
        if not bottom_plot_canv_ok(cnv_wrp):
            return cnv_wrp

        rnds = cnv_wrp._renderers
        bkg_rnd, sig_rnds = rnds[0], rnds[1:]

        # overlaying ratio histogram
        mc_histo_no_err = bkg_rnd.histo.Clone()
        mc_histo_no_err.GetXaxis().SetCanExtend(0)
        for i in xrange(1, mc_histo_no_err.GetXaxis().GetNbins()+1):
            mc_histo_no_err.SetBinError(i, 0.)

        div_hists = list(sr.histo.Clone() for sr in sig_rnds)
        cnv_wrp._bottom_hist_overlay = div_hists
        for div_hist in div_hists:
            div_hist.GetXaxis().SetCanExtend(0)
            div_hist.Sumw2()

            for i in xrange(1, mc_histo_no_err.GetXaxis().GetNbins()+1):
                if not div_hist.GetBinContent(i):
                    div_hist.SetBinError(i, 1.)
            div_hist.Add(mc_histo_no_err, -1)
            div_hist.Divide(mc_histo_no_err)
            for i in xrange(1, mc_histo_no_err.GetXaxis().GetNbins()+1):
                if not div_hist.GetBinContent(i):
                    div_hist.SetBinContent(i, -500.)

            _bottom_plot_y_bounds(cnv_wrp, div_hist, par)

        # underlying error bands
        _err_ratio_util_mk_sys_stt_histos(cnv_wrp, bkg_rnd)

        return div_hists

    def ratio_plot_func(cnv_wrp, kws):
        if not _bottom_plot_make_pad(cnv_wrp):
            return cnv_wrp
        par = dict(settings.defaults_BottomPlot)
        par.update(outer_kws)
        par.update(kws)
        par['y_title'] = par.get('y_title', '') or '#frac{Sig-bkg}{bkg}'

        # make bottom histos
        div_hists = make_bottom_hists(cnv_wrp, par)

        # draw bottom histos
        cnv_wrp.second_pad.cd()
        _err_ratio_util_plot_sys_stt_histos(cnv_wrp, par)
        for hist in div_hists:
            hist.SetMarkerSize(hist.GetMarkerSize()*0.8)
            hist.Draw('same' + par['draw_opt_multi_line'])

        cnv_wrp.main_pad.cd()
        return cnv_wrp

    return PostBuildFuncWithSetup(
        ratio_plot_func,
        (bottom_plot_canv_ok, bottom_plot_prep_main_pad)  # make_bottom_hist is called later
    )


def mk_pull_plot_func(**outer_kws):
    """
    Ratio of first and second histogram in canvas.
    """
    def make_bottom_hist(cnv_wrp, kws):
        if not bottom_plot_canv_ok(cnv_wrp):
            return cnv_wrp

        par = dict(settings.defaults_BottomPlot)
        par.update(outer_kws)
        par.update(kws)
        cnv_wrp._par_mk_pull_plot_func = par

        rnds = cnv_wrp._renderers
        mcee_rnd, data_rnd = bottom_plot_get_div_hists(rnds)
        y_title = par['y_title'] or (
            '#frac{Data-MC}{#sigma}' if data_rnd.is_data else '#frac{Sig-bkg}{bkg}')

        # produce pull histogram
        mc_histo = mcee_rnd.histo
        data_hist = data_rnd.histo                      # NO CLONE HERE!
        sigma_histo = mcee_rnd.histo.Clone()
        data_hist.SetBinErrorOption(ROOT.TH1.kPoisson)
        mc_histo.SetBinErrorOption(ROOT.TH1.kPoisson)
        for i in xrange(mc_histo.GetNbinsX()+2):
            sigma_histo.SetBinError(i, 0.)
            # pm stands for plusminus
            pm = 1. if data_hist.GetBinContent(i) > mc_histo.GetBinContent(i) else -1.
            mc_sig_stat = mc_histo.GetBinErrorUp(i) if pm > 0 else mc_histo.GetBinErrorLow(i)
            data_sig_stat = data_hist.GetBinErrorLow(i) if pm > 0 else data_hist.GetBinErrorUp(i)
            if not data_hist.GetBinContent(i):
                data_sig_stat = 1.8
            if not mc_histo.GetBinContent(i):
                mc_sig_stat = 1.8
            mc_sig_syst = 0.
            if mcee_rnd.histo_sys_err:
                mc_sys_hist = mcee_rnd.histo_sys_err
                mc_sig_syst = mc_sys_hist.GetBinError(i) + pm*abs(
                                        mc_histo.GetBinContent(i) - mc_sys_hist.GetBinContent(i))
            sqr_quad = sqrt(mc_sig_stat**2+data_sig_stat**2+mc_sig_syst**2) or 1e-10
            sigma_histo.SetBinContent(i, sqr_quad)

        div_hist = data_hist.Clone()                    # NOW CLONING!
        div_hist.Add(mc_histo, -1)
        div_hist.Divide(sigma_histo)
        div_hist.SetYTitle(y_title)

        cnv_wrp.bottom_hist = div_hist
        settings.set_bottom_plot_general_style(cnv_wrp.bottom_hist)
        settings.set_bottom_plot_pull_style(div_hist)
        _bottom_plot_y_bounds(cnv_wrp, cnv_wrp.bottom_hist, par)
        par['draw_opt'] = 'hist'

    def ratio_plot_func(cnv_wrp, _):
        if not _bottom_plot_make_pad(cnv_wrp):
            return cnv_wrp

        par = cnv_wrp._par_mk_pull_plot_func
        del cnv_wrp._par_mk_pull_plot_func

        # draw histo
        cnv_wrp.second_pad.cd()
        cnv_wrp.bottom_hist.Draw(par['draw_opt'])
        cnv_wrp.main_pad.cd()
        return cnv_wrp

    return PostBuildFuncWithSetup(
        ratio_plot_func,
        (bottom_plot_prep_main_pad, make_bottom_hist)
    )


############################################################# canvas "main" ###
build_funcs = [
    setup,
    find_x_y_bounds,
    draw_content,
]
post_build_funcs = [
    mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
    mk_legend_func(),
]


def build_canvas(wrps,
                 build_funcs=build_funcs,
                 post_build_funcs=post_build_funcs,
                 **kws):
    kws['post_build_funcs'] = post_build_funcs
    for func_list in (build_funcs, post_build_funcs):
        for bf in func_list:
            # after setup a CanvasWrapper is passed instead of a list of wrps
            wrps = bf(wrps, kws) or wrps  # using "or wrps" for non-returning functions
    return wrps


# TODO use WrapperWrapper info on construction
# TODO make a setting for choosing the default bottom plot??

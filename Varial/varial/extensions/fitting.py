"""
Tools from former analyses. **EXPERIMENTAL!**
"""

import itertools
import os
import ROOT

import varial.analysis
import varial.dbio
import varial.tools
import varial.history
import varial.generators as gen
import varial.operations as op

try:
    import pymc
    import numpy
except ImportError:
    pymc = None
    numpy = None

try:
    import theta_auto
    theta_auto.config.theta_dir = os.environ["CMSSW_BASE"] + "/theta"
except ImportError:
    theta_auto = None


varial.settings.store_mcmc = False


####################################################### Core Fitter Classes ###
class Fitter(object):
    def __init__(self):
        self.x_min = 0.
        self.x_max = 0.
        self.fit_func = None
        self.fitted = None
        self.tmplts = None
        self.ndf = 0
        self.val_err = []

    def build_fit_function(self, fitted, tmplts, x_min, x_max):
        templates = [tw.histo for tw in tmplts]
        size = len(templates)
        self.x_min, self.x_max = x_min, x_max
        self.fitted = fitted
        self.tmplts = tmplts

        def fit_func(x, par):
            value = 0.
            for j, hist in enumerate(templates):
                value += par[j] * hist.GetBinContent(hist.FindBin(x[0]))
            return value

        self.fit_func = ROOT.TF1(
            "MyFitFunc",
            fit_func,
            x_min,
            x_max,
            size
        )
        for i in xrange(0, size):
            self.fit_func.SetParameter(i, 1.)

    def do_the_fit(self):
        self.fitted.histo.Fit(
            self.fit_func, "WL M N", "", self.x_min, self.x_max
        )
        self.val_err = list(
            (self.fit_func.GetParameter(i_par),
             self.fit_func.GetParError(i_par))
            for i_par in xrange(len(self.tmplts))
        )
        self.ndf = self.fit_func.GetNDF()

    def scale_templates_to_fit(self, templates):
        for i in range(0, len(templates)):
            val, _ = self.get_val_err(i)
            templates[i].histo.Scale(val)

    def get_val_err(self, i_par):
        return self.val_err[i_par]

    def get_ndf(self):
        return self.ndf

    def get_chi2(self):
        return 0.

    def get_total_fit_err(self, mc_integrals):
        return 0.

    def make_fit_result(self, result_wrp, tmplts):
        r = result_wrp
        r.Chi2 = self.get_chi2() or gen.op.chi2(
            (gen.op.sum(tmplts), self.fitted),
        ).float
        r.NDF = self.get_ndf()
        r.FitProb = ROOT.TMath.Prob(r.Chi2, r.NDF)
        r.legend = []
        r.value = []
        r.error = []
        r.binIntegralMC = []
        r.binIntegralScaled = []
        r.binIntegralScaledError = []
        for i, tmplt in enumerate(tmplts):
            r.legend.append(tmplt.legend)
            val, err = self.get_val_err(i)
            r.value.append(val)
            r.error.append(err)
            r.binIntegralMC.append(tmplt.histo.Integral() / r.value[-1])
            r.binIntegralScaled.append(tmplt.histo.Integral())
            r.binIntegralScaledError.append(
                r.binIntegralScaled[-1] * r.error[-1] / r.value[-1]
            )
        r.dataIntegral = self.fitted.histo.Integral()
        r.dataIntegralSqrt = r.dataIntegral**.5
        r.totalIntegralFitErr = self.get_total_fit_err(r.binIntegralMC)


class ThetaFitter(Fitter):
    def __init__(self, model_callback=None):
        super(ThetaFitter, self).__init__()
        self.model = None
        self.fit_res = None
        self.model_callback = model_callback

    def _store_histos_for_theta(self, wrp):
        filename = os.path.join(varial.analysis.cwd, wrp.name + ".root")
        f = ROOT.TFile.Open(filename, "RECREATE")
        f.cd()
        for key, value in wrp.__dict__.iteritems():
            if isinstance(value, ROOT.TH1):
                value.SetName(key)
                value.Write()
        f.Close()

    def build_fit_function(self, fitted, tmplts, x_min, x_max):
        self.x_min, self.x_max = x_min, x_max
        self.fitted = fitted
        self.tmplts = tmplts

        theta_root_wrp = varial.wrappers.Wrapper(name="ThetaHistos")
        if fitted:
            setattr(theta_root_wrp, 'histo__DATA', fitted.histo)
        self.template_names = []
        signal_procs = []
        for i, tmplt in enumerate(tmplts):
            name = 'template%02d' % (i + 1)
            self.template_names.append(name)
            setattr(theta_root_wrp, 'histo__' + name, tmplt.histo)
            if tmplt.is_signal:
                signal_procs.append(name)
        self._store_histos_for_theta(theta_root_wrp)
        theta_auto.config.workdir = varial.analysis.cwd
        theta_auto.config.report = theta_auto.html_report(os.path.join(
            varial.analysis.cwd, 'theta.html'
        ))
        plt_dir = os.path.join(varial.analysis.cwd, 'plots')
        if not os.path.exists(plt_dir):
            os.mkdir(plt_dir)
        self.model = theta_auto.build_model_from_rootfile(
            os.path.join(varial.analysis.cwd, "ThetaHistos.root"),
            include_mc_uncertainties=True
        )
        self.model.fill_histogram_zerobins()
        self.model.set_signal_processes(signal_procs)
        if self.model_callback:
            self.model_callback(self.model)
        #for tmplt_name in self.template_names[:-1]:
        #    self.model.get_coeff(
        #        "histo", tmplt_name).add_factor(
        #            'id', parameter='bg_' + tmplt_name)
        #    self.model.distribution.set_distribution(
        #        'bg_' + tmplt_name,
        #        'gauss', 1.0, theta_auto.inf, [0.0, theta_auto.inf]
        #    )
        # TODO: get ndf from theta directly
        self.ndf = tmplts[0].histo.GetNbinsX() - len(self.template_names)

    def do_the_fit(self):
        options = theta_auto.Options()
        options.set('minimizer', 'strategy', 'robust')
        #self.fit_res = theta_auto.mle(
        #    self.model,
        #    "data",
        #    1,
        #    chi2=True,
        #    options=options,
        #    with_covariance=True,
        #)[self.template_names[-1]]
        #self.fit_res = theta_auto.bayesian_limits(self.model, what='expected')
        self.fit_res = theta_auto.asymptotic_cls_limits(self.model) #, what='expected')
        print self.fit_res

        par_values = {
            "beta_signal": self.fit_res["beta_signal"][0][0],
        }
        for tmplt_name in self.template_names[:-1]:
            bg_name = "bg_" + tmplt_name
            par_values[bg_name] = self.fit_res[bg_name][0][0]

        self.val_err = []
        for tmplt_name in self.template_names[:-1]:
            val = self.model.get_coeff("histo", tmplt_name).get_value(
                par_values)
            err = self.fit_res["bg_" + tmplt_name][0][1]
            self.val_err.append((val, err))
        self.val_err.append((
            self.fit_res["beta_signal"][0][0],
            abs(self.fit_res["beta_signal"][0][1])
        ))

    def get_chi2(self):
        return self.fit_res['__chi2'][0]

    def get_total_fit_err(self, mc_integrals):
        vec = mc_integrals
        vec = vec[-1:] + vec[:-1]  # sort signal to front
        vec = numpy.array(vec)

        cov = self.fit_res['__cov'][0]
        return numpy.dot(numpy.dot(vec, cov), vec)**.5


class PyMCFitter(Fitter):
    def build_fit_function(self, fitted, tmplts, x_min, x_max):
        self.x_min, self.x_max = x_min, x_max
        self.fitted = fitted
        self.tmplts = tmplts

        # convert to numpy arrays
        fitted_cont = numpy.fromiter(
            (fitted.histo.GetBinContent(i)
             for i in xrange(fitted.histo.GetNbinsX())),
            dtype=float,
            count=fitted.histo.GetNbinsX()
        )
        tmplts_cont = list(numpy.fromiter(
            (mc_t.histo.GetBinContent(i)
             for i in xrange(mc_t.histo.GetNbinsX())),
            dtype=float,
            count=mc_t.histo.GetNbinsX()
        ) for mc_t in tmplts)
        tmplts_errs = list(numpy.fromiter(
            (mc_t.histo.GetBinError(i) or 1e-7
             for i in xrange(mc_t.histo.GetNbinsX())),
            dtype=float,
            count=mc_t.histo.GetNbinsX()
        ) for mc_t in tmplts)

        # remove entries without prediction
        all_mc = sum(tmplts_cont)
        mask = numpy.nonzero(all_mc)
        fitted_cont = fitted_cont[mask]
        tmplts_cont = list(d[mask] for d in tmplts_cont)
        tmplts_errs = list(d[mask] for d in tmplts_errs)

        # model
        n_tmplts = len(tmplts)
        n_datapoints = len(fitted_cont)
        tmplts = pymc.Container(list(
            pymc.Normal(('MC_%02d' % i),
                        v[0],                                       # value
                        numpy.vectorize(lambda x: x**-2)(v[1]),     # precision
                        value=v[0],
                        size=n_datapoints)
            for i, v in enumerate(itertools.izip(tmplts_cont,
                                                 tmplts_errs))
        ))
        mc_factors = pymc.Container(list(
            pymc.Lognormal('factor_%02d' % i, 1., 1e-10, value=1.)
            for i in xrange(n_tmplts)
        ))

        @pymc.deterministic
        def fit_func(ts=tmplts, factors=mc_factors):
            return sum(
                f * tmplt
                for f, tmplt in itertools.izip(factors, ts)
            )

        fitted = pymc.Poisson('fitted', fit_func, fitted_cont,
                              size=n_datapoints, observed=True)
        self.model = pymc.Model([fitted, mc_factors, tmplts])

        # for later reference
        self.n_tmplts, self.n_datapoints = n_tmplts, n_datapoints
        self.ndf = n_datapoints - n_tmplts

    def do_the_fit(self):

        pymc.MAP(self.model).fit(method='fmin_powell')

        if varial.settings.store_mcmc:
            mcmc = pymc.MCMC(self.model, db='pickle',
                             dbname=varial.analysis.cwd + '/mcmc.pickle')
        else:
            mcmc = pymc.MCMC(self.model)

        mcmc.sample(100000, 50000, 4)

        self.val_err = list(
            (trace.mean(), trace.var()**.5)
            for trace in (mcmc.trace('factor_%02d' % i)[:, None]
                          for i in xrange(self.n_tmplts))
        )

        if varial.settings.store_mcmc:
            mcmc.db.close()


##################################################### convenience functions ###
def find_x_range(data_hist):
    x_min = data_hist.GetXaxis().GetXmin()
    x_max = data_hist.GetXaxis().GetXmax()
    for i in xrange(data_hist.GetNbinsX()):
        if data_hist.GetBinContent(i):
            x_min = data_hist.GetXaxis().GetBinLowEdge(i)
            break
    for i in xrange(data_hist.GetNbinsX(), 0, -1):
        if data_hist.GetBinContent(i):
            x_max = data_hist.GetXaxis().GetBinUpEdge(i)
            break
    return x_min - 1e-10, x_max + 1e-10


def fix_ratio_histo_name(cnvs):
    for c in cnvs:
        d = c.get_decorator(varial.rendering.BottomPlotRatioSplitErr)
        d.dec_par["y_title"] = "Fit residual"
        yield c


def set_no_exp(cnvs):
    for c in cnvs:
        c.first_drawn.GetYaxis().SetNoExponent()
        c.bottom_hist.GetYaxis().SetTitleSize(0.14)
        c.canvas.Modified()
        c.canvas.Update()
        yield c


################################################################## Fit Tool ###
class TemplateFitTool(varial.tools.Plotter):
    def __init__(self,
                 template_result_path,
                 fitted_result_path='',
                 fitter=Fitter(),
                 fitbox_bounds=(0.6, 0.9, 0.6),
                 save_name_lambda=lambda w: w.name,
                 name=None):
        super(TemplateFitTool, self).__init__(name)
        self.template_result_path = template_result_path
        self.fitted_result_path = fitted_result_path
        self.tmplts = None
        self.fitted = None
        self.fitbox_bounds = fitbox_bounds
        self.result = varial.wrappers.Wrapper()
        self.n_templates = 0
        self.fitter = fitter
        self.x_min = 0.
        self.x_max = 0.
        self.save_name_lambda = save_name_lambda
        self.hook_pre_canvas_build = fix_ratio_histo_name
        self.hook_post_canvas_build = set_no_exp

    def make_fit_textbox(self):
        res = self.result
        x1, x2, y2 = self.fitbox_bounds
        y1 = y2 - ((len(res.legend) + 1) * 0.04)

        textbox = ROOT.TPaveText(x1, y1, x2, y2, "brNDC")
        textbox.SetBorderSize(1)
        textbox.SetLineColor(0)
        textbox.SetLineStyle(1)
        textbox.SetLineWidth(0)
        textbox.SetFillColor(0)
        textbox.SetFillStyle(1001)
        textbox.SetTextSize(varial.settings.box_text_size)
        textbox.AddText(
            "#chi^{2} / NDF = %d / %i" % (round(res.Chi2, 2), res.NDF)
        )

        text = []
        for i, legend in enumerate(res.legend):
            text.append(
                "N_{%s} = %d #pm %d" % (
                    legend,
                    res.binIntegralScaled[i],
                    res.binIntegralScaledError[i]
                )
            )
        for txt in reversed(text):
            textbox.AddText(txt)
        return textbox

    def load_content(self):
        pass

    def set_up_content(self):
        self.result.fitter = self.fitter.__class__.__name__

        self.tmplts = self.lookup_result(self.template_result_path)
        if self.fitted_result_path == self.template_result_path:
            self.fitted = self.tmplts.pop(0)
        elif self.fitted_result_path:
            self.fitted = self.lookup_result(self.fitted_result_path)[0]
        self.n_templates = len(self.tmplts)

        # do fit procedure
        self.x_min, self.x_max = find_x_range(
            self.fitted.histo if self.fitted else self.tmplts[0].histo
        )
        self.fitter.build_fit_function(
            self.fitted, self.tmplts, self.x_min, self.x_max
        )
        self.fitter.do_the_fit()
        self.fitter.scale_templates_to_fit(self.tmplts)
        self.fitter.make_fit_result(self.result, self.tmplts)

        fit_textbox = self.make_fit_textbox()
        self.canvas_decorators.append(
            varial.rendering.TextBox(
                None,
                textbox=fit_textbox
            )
        )

        tmplt_stack = op.stack(self.tmplts)
        self.stream_content = [filter(None, (tmplt_stack, self.fitted))]

        del self.fitter



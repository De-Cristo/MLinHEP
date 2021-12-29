#!/usr/bin/env python

import sys
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

if len(sys.argv) < 2:
    print """
Usage:
varial_plotter.py <signal-files>
                  [--bkg <background-files>]
                  [--dat <data-files>]
                  [--psu <pseudodata-files>]

The given files are plotted with these styles:
    - signal files are plotted as lines
    - background files are stacked and plotted as filled histograms
    - data files are plotted as filled circles
    - pseudo-data files are plotted as empty circles

For more control over plotting, a script needs to be implemented.
The varial_plotter.py executable in the /bin directory is probably
the best starting point. Also, check the examples e01 and e02 in
the varial_example module.

Options:
--norm          normalize all input histograms to integral
--rebin         rebin histograms to have a maximum of 42 bins
--theta_file    plot systematic uncertainties from a theta-file
--pdf           produces pdf files as well
"""
    exit(-1)

# grab filenames and options
norm_to_int = False
theta_file = False
n_bins_max = 0
add_pdf = False
sig, bkg, dat, psu = [], [], [], []
args = sys.argv[:]
args.pop(0)
current_coll = sig
for a in args:
    if a == '--bkg':
        current_coll = bkg
    elif a == '--dat':
        current_coll = dat
    elif a == '--psu':
        current_coll = psu
    elif a == '--norm':
        norm_to_int = True
    elif a == '--rebin':
        n_bins_max = 42
    elif a == '--pdf':
        add_pdf = True
    elif a == '--theta_file':
        theta_file = True
    else:
        current_coll.append(a)
all_input = sig + bkg + dat + psu

print 'signal-files:        ', sig
print 'background-files:    ', bkg
print 'data files:          ', dat
print 'pseudo-data files:   ', psu
if n_bins_max:
    print '- rebinning to a maximum of 42 bins'
if norm_to_int:
    print '- normalizing to integral'

# setup varial
import varial.tools
varial.settings.box_text_size = 0.03
varial.settings.try_reuse_results = False
varial.settings.defaults_Legend.update({
    'x_pos': 0.85,
    'y_pos': 0.5,
    'label_width': 0.28,
    'label_height': 0.04,
    'opt': 'f',
    'opt_data': 'p',
    'reverse': True
})
varial.settings.canvas_size_x = 550
varial.settings.canvas_size_y = 400
varial.settings.root_style.SetPadRightMargin(0.3)
varial.settings.rootfile_postfixes = ['.root', '.png']
if add_pdf:
    varial.settings.rootfile_postfixes += ['.pdf']

sample_names = varial.util.setup_legendnames_from_files(all_input)


def label_axes(wrps):
    for w in wrps:
        if 'TH1' in w.type and w.histo.GetXaxis().GetTitle() == '':
            w.histo.GetXaxis().SetTitle(w.histo.GetTitle())
            w.histo.GetYaxis().SetTitle('events')
            w.histo.SetTitle('')
        yield w


def theta_tokenizer(w):
    orig_name = w.name
    tokens = orig_name.split('__')
    if len(tokens) == 2:
        w.name, w.sample = tokens
        if tokens[1] == 'DATA':
            w.sample = 'Data'
            w.is_data = True
    elif len(tokens) == 4:
        w.name, w.sample, sys1, sys2 = tokens
        w.sys_info = '%s__%s' % (sys1, sys2)
    else:
        raise RuntimeError("Don't understand name in thetafile: " + orig_name)

    w.legend = w.sample
    w.in_file_path = w.in_file_path[0:-len(orig_name)] + w.name

    return w


# this function processes histograms after loading
def post_load_hook(wrps):
    if n_bins_max:
        wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, n_bins_max)
    wrps = label_axes(wrps)
    if theta_file:
        wrps = (theta_tokenizer(w) for w in wrps)
    else:
        wrps = varial.gen.gen_add_wrp_info(
            wrps,
            sample=lambda w: sample_names[w.file_path],
            is_signal=lambda w: w.file_path in sig,
            is_data=lambda w: w.file_path in dat,
            is_pseudo_data=lambda w: w.file_path in psu,
        )
    wrps = sorted(wrps, key=lambda w: w.in_file_path + '___' + w.file_path)
    wrps = varial.gen.gen_make_th2_projections(wrps)
    if norm_to_int:
        wrps = varial.gen.gen_noex_norm_to_integral(wrps)
    return wrps


def make_plotter(**kws):
    filter_keyfunc = kws.pop('filter_keyfunc', None)

    def plotter_factory(**f_kws):
        f_kws.update(kws)
        hook_loaded_histos = f_kws.pop('hook_loaded_histos', None)
        if hook_loaded_histos:     # if present, then post_load_hook should be run before
            f_kws['hook_loaded_histos'] = lambda ws: hook_loaded_histos(post_load_hook(ws))
        else:
            f_kws['hook_loaded_histos'] = post_load_hook
        f_kws['save_lin_log_scale'] = True
        f_kws['stack'] = True
        return varial.tools.Plotter(**f_kws)

    return varial.tools.mk_rootfile_plotter(
        pattern=all_input,
        name='varial_plotter',
        plotter_factory=plotter_factory,
        combine_files=True,
        filter_keyfunc=filter_keyfunc,
    )


def run(**kws):
    plotter = make_plotter(**kws)
    varial.tools.Runner(plotter)
    varial.tools.WebCreator().run()

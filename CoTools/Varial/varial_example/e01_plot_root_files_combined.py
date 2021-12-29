#!/usr/bin/env python

"""
Just as e01_plot_root_files, but plots same hists into same canvases.

Also normalizes histograms to integral.
See the mk_rootfile_plotter call below.
"""

outdir = 'MyPlottedRootFilesCombined'

# set root to batch mode (it opens an x-connection otherwise)
import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

# import the tools module
import varial.tools

# plotter factory adds a hook for normalizing to hists
def plotter_factory(**kws):
    kws['hook_loaded_histos'] = varial.generators.gen_norm_to_integral
    return varial.tools.Plotter(**kws)


if __name__ == '__main__':

    # get a plotter instance and run it (all arguments are optional)
    pltr = varial.tools.mk_rootfile_plotter(
        name=outdir,                        # output folder name
        plotter_factory=plotter_factory,    # use own factory
        combine_files=True                  # YES to combine_files!!!
    )

    pltr.run()                          # run the plotter
    varial.tools.WebCreator().run()     # run the WebCreator


def dummy_func():
    """This is a dummy to get a [source] link in the docs."""
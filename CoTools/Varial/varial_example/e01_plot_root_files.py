#!/usr/bin/env python

"""
Simple script that dumps any rootfile in the same directory into a website.

This script plots all rootfiles in the current working directory into a folder
named *MyPlottedRootFiles*. It will reproduce the folder structure it finds in
the rootfiles. Last, it creates a crosslinked website with all the plots. Open
index.html to view.
"""

outdir = 'MyPlottedRootFiles'

# set root to batch mode (it opens an x-connection otherwise)
import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

# import the tools module
import varial.tools


if __name__ == '__main__':

    # get a plotter instance and run it (all arguments are optional)
    pltr = varial.tools.mk_rootfile_plotter(
        name=outdir,        # output folder name
        pattern='*.root',   # file matching pattern
        flat=False          # recreate directory struction in rootfile
    )

    pltr.run()                          # run the plotter
    varial.tools.WebCreator().run()     # run the WebCreator


def dummy_func():
    """This is a dummy to get a [source] link in the docs."""
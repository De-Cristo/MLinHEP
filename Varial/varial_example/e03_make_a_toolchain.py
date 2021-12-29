"""
Example on making a toolchain.

Originally taken from https://github.com/HeinAtCERN/BTagDeltaR/blob/master/Analysis/python/varial_analysis.py
"""

import os
import varial.diskio
import varial.tools
import e02_make_a_tool
from varial.extensions.fwlite import Fwlite

# You can make a fwlite job like this:
fwlite = Fwlite('path/to/script.py'),

# Load the files in the test fileservice directory
loader = varial.tools.HistoLoader(
    pattern='../varial/test/fileservice/*.root',
    filter_keyfunc=lambda w: w.name == 'deltaErel',
    io=varial.diskio  # store on disk so one can examine the hists
)

# plot all loaded histograms
# (Plotter looks automaticly for '../HistoLoader' input)
plot_plain = varial.tools.Plotter(
    name='PlainHistPlots',

    # a bit complicated here: reuse the original filename
    save_name_func= \
        lambda w: os.path.basename(w._renderers[0].file_path)[:-5]
)

# use the histo normalizer example
normalizer = e02_make_a_tool.MyHistoNormalizer(
    pattern='../varial/test/fileservice/*.root',
    filter_keyfunc=lambda w: w.name == 'deltaErel'
)

# plot all loaded histograms
plot_norm = varial.tools.Plotter(
    name='NormHistPlots',
    input_result_path='../MyHistoNormalizer',

    # a bit complicated here: reuse the original filename
    save_name_func= \
        lambda w: os.path.basename(w._renderers[0].file_path)[:-5]
)

# website output
websitetool = varial.tools.WebCreator()

# copy webcontent to a place where the webserver can find it
copytool = varial.tools.CopyTool(os.path.join(os.environ['HOME'], 'www/ana/'))


# setup the base toolchain
# (the constructor takes a name string and a list of tools)
tc = varial.tools.ToolChain(
    "EXAMPLE_ANALYSIS",
    [
        # fwlite,
        loader,
        plot_plain,
        normalizer,
        plot_norm,
        websitetool,
        # copytool,
    ]
)


def dummy_func():
    """
    This is just a dummy to include a [source] link in the doc.
    """

"""
Settings example from an analysis.

Taken from https://github.com/HeinAtCERN/BTagDeltaR/blob/master/Analysis/python/ttdilep_samples.py
"""

import ROOT
from varial import settings


# Postfixes. All canvases are stored with all filetypes.
# Default is ['.root', '.png']
settings.rootfile_postfixes += [".eps"]


# Defines the order in which samples are stacked. Use legend names.
settings.stacking_order = [
    'Di-boson',
    'Single top',
    'DY + jets',
    'W + jets',
    'TTbar',
    'TTbar (no match)',
    'TTbar (1 match)',
    'TTbar (B+D match)',
    'TTbar (2 matches)',
]

# Coloring of filled histograms. Again with legend names.
# See also histotools.generators.apply_fillcolor(...)
settings.colors = {
    'Di-boson': ROOT.kYellow,
    'Single top': ROOT.kMagenta,
    'DY + jets': ROOT.kBlue,
    'W + jets': ROOT.kOrange,
    'TTbar': ROOT.kRed,
    'TTbar (no match)': ROOT.kRed + 3,
    'TTbar (1 match)': ROOT.kRed + 1,
    'TTbar (B+D match)': ROOT.kPink - 2,
    'TTbar (2 matches)': ROOT.kRed - 9,
}


def dummy_func():
    """
    This is just a dummy to include a [source] link in the doc.
    """

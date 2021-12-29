"""
Operations on Wrappers.

All of them take one ore more wrappers and return a wrapper. Every wrapper has
a ``history`` member in which all applied operations are stored.
Furthermore, all operations are present in the form of a generator in the
generator module. Below, an example is given for every operation.
"""

import settings  # init ROOT first

from ROOT import THStack, TGraphAsymmErrors
import collections
import __builtin__
import wrappers
import history
import ctypes
import array
import ROOT
import math


class OperationError(RuntimeError): pass
class TooFewWrpsError(OperationError): pass
class TooManyWrpsError(OperationError): pass
class WrongInputError(OperationError): pass
class NoLumiMatchError(OperationError): pass
class WrongIntegralError(OperationError): pass


def iterableize(obj):
    if isinstance(obj, collections.Iterable):
        return obj
    else:
        return [obj]


def add_wrp_info(wrp, **kw_funcs):
    """
    Updates wrapper with values from keyfunctions.

    Example: Set the legend to the filename like this:

    >>> import os
    >>> w1 = wrappers.Wrapper(name='a_name', file_path='/path/to/my_file.root')
    >>> w1 = add_wrp_info(w1, legend=lambda w: os.path.basename(w.file_path)[:-5])
    >>> w1.legend
    'my_file'
    """
    # evaluate
    kw_args = {}
    for k, f in kw_funcs.iteritems():
        val = f(wrp)
        kw_args[k] = val
        setattr(wrp, k, val)

    # (need to track history manually)
    if isinstance(wrp, wrappers.Wrapper):
        h = history.History('add_wrp_info')
        h.add_args([wrp.history])
        h.add_kws(kw_args)
        wrp.history = h

    return wrp


@history.track_history
def stack(wrps):
    """
    Applies only to HistoWrappers. Returns StackWrapper.
    Checks lumi to be equal among all wrappers.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 4.5)
    >>> h1.Fill(1,4)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> h2 = TH1I("h2", "", 2, .5, 4.5)
    >>> h2.Fill(1,3)
    1
    >>> h2.Fill(3,6)
    2
    >>> w2 = wrappers.HistoWrapper(h2, lumi=2.)
    >>> w3 = stack([w1, w2])
    >>> w3.histo.Integral()
    13.0
    >>> w3.lumi
    2.0
    """
    wrps    = iterableize(wrps)
    stk_wrp = None
    lumi    = 0.
    info    = None
    sample  = ""
    for wrp in wrps:
        if not isinstance(wrp, wrappers.HistoWrapper):          # histo check
            raise WrongInputError(
                "stack accepts only HistoWrappers. wrp: "
                + str(wrp)
            )
        if not stk_wrp:                                         # stack init
            stk_wrp = THStack(wrp.name, wrp.title)
            lumi = wrp.lumi
            info = wrp.all_info()
            sample = wrp.sample
        elif lumi != wrp.lumi:                                  # lumi check
            raise NoLumiMatchError(
                "stack needs lumis to match. (%f != %f)" % (lumi, wrp.lumi)
            )
        if sample != wrp.sample:                                # add to stack
            sample = ""
        if wrp.legend:
            wrp.histo.SetTitle(wrp.legend)
        stk_wrp.Add(wrp.histo)
    if not info:
        raise TooFewWrpsError(
            "At least one Wrapper must be provided."
        )
    if not sample:
        del info["sample"]
    return wrappers.StackWrapper(stk_wrp, **info)


@history.track_history
def sum(wrps):
    """
    Applies only to HistoWrappers. Returns HistoWrapper. Adds lumi up.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 4.5)
    >>> h1.Fill(1)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> h2 = TH1I("h2", "", 2, .5, 4.5)
    >>> h2.Fill(1)
    1
    >>> h2.Fill(3)
    2
    >>> w2 = wrappers.HistoWrapper(h2, lumi=3.)
    >>> w3 = sum([w1, w2])
    >>> w3.histo.Integral()
    3.0
    >>> w3.lumi
    5.0
    >>> w4 = sum([w3])  # one item is enough
    >>> w4.lumi
    5.0
    """
    wrps = list(iterableize(wrps))
    if len(wrps) == 1 and isinstance(wrps[0], wrappers.HistoWrapper):
        return wrps[0]
    histo = None
    lumi = 0.
    info = None
    for wrp in wrps:
        if not isinstance(wrp, wrappers.HistoWrapper):
            raise WrongInputError(
                "sum accepts only HistoWrappers. wrp: "
                + str(wrp)
            )
        if histo:
            histo.Add(wrp.histo)
        else:
            histo = wrp.histo.Clone()
            info = wrp.all_info()
        lumi += wrp.lumi
    if not info:
        raise TooFewWrpsError(
            "At least one Wrapper must be provided."
        )
    info["lumi"] = lumi
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def diff(wrps):
    """
    Applies only to HistoWrappers. Returns HistoWrapper. Takes lumi from first.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 4.5)
    >>> h1.Fill(1, 2)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> h2 = TH1I("h2", "", 2, .5, 4.5)
    >>> h2.Fill(1)
    1
    >>> w2 = wrappers.HistoWrapper(h2, lumi=3.)
    >>> w3 = diff([w1, w2])
    >>> w3.histo.Integral()
    1.0
    >>> w3.lumi
    2.0
    """
    wrps = iterableize(wrps)
    histo = None
    lumi = 0.
    info = None
    for wrp in wrps:
        if not isinstance(wrp, wrappers.HistoWrapper):
            raise WrongInputError(
                "diff accepts only HistoWrappers. wrp: "
                + str(wrp)
            )
        if histo:
            histo.Add(wrp.histo, -1.)
        else:
            histo = wrp.histo.Clone()
            info = wrp.all_info()
            lumi = wrp.lumi
    if not info:
        raise TooFewWrpsError(
            "At least one Wrapper must be provided."
        )
    info["lumi"] = lumi
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def merge(wrps):
    """
    Applies only to HistoWrapper. Returns HistoWrapper. Normalizes histos to lumi.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1,4)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> h2 = TH1I("h2", "", 2, .5, 2.5)
    >>> h2.Fill(1,3)
    1
    >>> h2.Fill(2,6)
    2
    >>> w2 = wrappers.HistoWrapper(h2, lumi=3.)
    >>> w3 = merge([w1, w2])
    >>> w3.histo.Integral()
    5.0
    >>> w3.lumi
    1.0
    """
    wrps = list(iterableize(wrps))
    if (len(wrps) == 1
        and isinstance(wrps[0], wrappers.HistoWrapper)
        and wrps[0].lumi == 1.
    ):
        return wrps[0]
    histo = None
    info = None
    for wrp in wrps:
        if not isinstance(wrp, wrappers.HistoWrapper):
            raise WrongInputError(
                "merge accepts only HistoWrappers. wrp: "
                + str(wrp)
            )
        if histo:
            histo.Add(wrp.histo, 1. / wrp.lumi)
        else:
            histo = wrp.histo.Clone()
            histo.Scale(1. / wrp.lumi)
            info = wrp.all_info()
    if not info:
        raise TooFewWrpsError(
            "At least one Wrapper must be provided."
        )
    info["lumi"] = 1.
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def prod(wrps):
    """
    Applies to HistoWrapper and FloatWrapper. Returns HistoWrapper. Takes lumi from first.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2, history="w1")
    >>> h2 = TH1I("h2", "", 2, .5, 2.5)
    >>> h2.Fill(1)
    1
    >>> h2.Fill(2)
    2
    >>> w2 = wrappers.HistoWrapper(h2, lumi=3)
    >>> w3 = prod([w1, w2])
    >>> w3.histo.Integral()
    1.0
    >>> w3.lumi
    1.0
    >>> w4 = wrappers.FloatWrapper(2.)
    >>> w5 = prod([w1, w4])
    >>> w5.histo.Integral()
    2.0
    """
    wrps = list(iterableize(wrps))
    if len(wrps) == 1 and isinstance(wrps[0], wrappers.HistoWrapper):
        return wrps[0]
    histo = None
    info = None
    lumi = 1.
    for wrp in wrps:
        if histo:
            if isinstance(wrp, wrappers.HistoWrapper):
                histo.Multiply(wrp.histo)
                lumi = 1.
            elif not isinstance(wrp, wrappers.FloatWrapper):
                raise WrongInputError(
                    "prod accepts only HistoWrappers and FloatWrappers. wrp: "
                    + str(wrp)
                )
            else:
                histo.Scale(wrp.float)
                lumi *= wrp.float
        else:
            if not isinstance(wrp, wrappers.HistoWrapper):
                raise WrongInputError(
                    "prod expects first argument to be of type HistoWrapper. wrp: "
                    + str(wrp)
                )
            histo = wrp.histo.Clone()
            info = wrp.all_info()
            lumi = wrp.lumi
    if not info:
        raise TooFewWrpsError(
            "At least one Wrapper must be provided."
        )
    info["lumi"] = lumi
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def div(wrps):
    """
    Applies to HistoWrapper and FloatWrapper. Returns HistoWrapper. Takes lumi from first.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1,4)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2)
    >>> h2 = TH1I("h2", "", 2, .5, 2.5)
    >>> h2.Fill(1,2)
    1
    >>> w2 = wrappers.HistoWrapper(h2, lumi=3)
    >>> w3 = div([w1, w2])
    >>> w3.histo.Integral()
    2.0
    >>> w4 = wrappers.FloatWrapper(2., history="w4")
    >>> w5 = div([w1, w4])
    >>> w5.histo.Integral()
    2.0
    """
    wrps = iterableize(wrps)
    wrps = iter(wrps)
    try:
        nominator = next(wrps)
        denominator = next(wrps)
    except StopIteration:
        raise TooFewWrpsError("div needs exactly two Wrappers.")
    try:
        wrps.next()
        raise TooManyWrpsError("div needs exactly two Wrappers.")
    except StopIteration:
        pass
    if not isinstance(nominator, wrappers.HistoWrapper):
        raise WrongInputError(
            "div needs nominator to be of type HistoWrapper. nominator: "
            + str(nominator)
        )
    if not (isinstance(denominator, wrappers.HistoWrapper) or
            isinstance(denominator, wrappers.FloatWrapper)):
        raise WrongInputError(
            "div needs denominator to be of type HistoWrapper or FloatWrapper. denominator: "
            + str(denominator)
        )

    histo = nominator.histo.Clone()
    lumi = nominator.lumi
    if isinstance(denominator, wrappers.HistoWrapper):
        histo.Divide(denominator.histo)
        lumi = 1.
    else:
        histo.Scale(1. / denominator.float)
        lumi /= denominator.float
    info = nominator.all_info()
    info["lumi"] = lumi
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def lumi(wrp):
    """
    Requires ``lumi`` to be defined on wrp. Returns FloatWrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> w2 = lumi(w1)
    >>> w2.float
    2.0
    """
    if not hasattr(wrp, 'lumi'):
        raise WrongInputError(
            "lumi needs ``lumi`` to be defined on wrp. wrp: "
            + str(wrp)
        )
    info = wrp.all_info()
    return wrappers.FloatWrapper(wrp.lumi, **info)


@history.track_history
def norm_to_lumi(wrp):
    """
    Applies to HistoWrapper. Returns HistoWrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1, 4)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> w1.histo.Integral()
    4.0
    >>> w2 = norm_to_lumi(w1)
    >>> w2.histo.Integral()
    2.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "norm_to_lumi needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    if wrp.lumi == 1.:
        return wrp

    histo = wrp.histo.Clone()
    histo.Scale(1. / wrp.lumi)
    info = wrp.all_info()
    info["lumi"] = 1.
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def norm_to_integral(wrp, use_bin_width=False):
    """
    Applies to HistoWrapper. Returns HistoWrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1, 4)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> w1.histo.Integral()
    4.0
    >>> w2 = norm_to_integral(w1)
    >>> w2.histo.Integral()
    1.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "norm_to_integral needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    option = "width" if use_bin_width else ""
    integr = wrp.histo.Integral(option) or 1.
    if integr == 1.:
        return wrp

    histo = wrp.histo.Clone()
    histo.Scale(1. / integr)
    info = wrp.all_info()
    info["lumi"] /= integr
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def norm_to_max_val(wrp):
    """
    Applies to HistoWrapper. Returns HistoWrapper.

    >>> from ROOT import TH1F
    >>> h1 = TH1F("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1, 4)
    1
    >>> h1.Fill(2, 2)
    2
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> w1.histo.Integral()
    6.0
    >>> w2 = norm_to_max_val(w1)
    >>> w2.histo.Integral()
    1.5
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "norm_to_max_val needs argument of type HistoWrapper. wrp: "
            + str(wrp)
        )
    max_val = wrp.histo.GetBinContent(wrp.histo.GetMaximumBin()) or 1.
    if max_val == 1.:
        return wrp

    histo = wrp.histo.Clone()
    histo.Scale(1. / max_val)
    info = wrp.all_info()
    info["lumi"] /= max_val
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def copy(wrp):
    """
    Applies to HistoWrapper and GraphWrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1, 4)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> w2=copy(w1)
    >>> w2.histo.GetName()
    'h1'
    >>> w1.name == w2.name
    True
    >>> w1.histo.Integral() == w2.histo.Integral()
    True
    >>> w1.histo != w2.histo
    True
    """
    if isinstance(wrp, wrappers.HistoWrapper):
        return wrappers.HistoWrapper(
            wrp.histo.Clone(),
            **wrp.all_info()
        )
    elif isinstance(wrp, wrappers.GraphWrapper):
        return wrappers.GraphWrapper(
            wrp.graph.Clone(),
            **wrp.all_info()
        )
    else:
        raise WrongInputError(
            "copy needs argument of type HistoWrapper or GraphWrapper. wrp: "
            + str(wrp)
        )


@history.track_history
def rebin(wrp, bin_bounds, norm_by_bin_width=False):
    """
    Applies to HistoWrapper. Returns Histowrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 4, .5, 4.5)
    >>> h1.Fill(1)
    1
    >>> h1.Fill(2)
    2
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> w2=rebin(w1, [.5, 2.5, 4.5])
    >>> w1.histo.GetNbinsX()
    4
    >>> w2.histo.GetNbinsX()
    2
    >>> w2.histo.GetBinContent(1)
    2.0
    >>> w2.histo.GetBinContent(2)
    0.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "rebin needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    if len(bin_bounds) < 2:
        raise OperationError(
            "Number of bins < 2, must include at least one bin!"
        )
    bin_bounds = array.array("d", bin_bounds)
    orig_bin_width = wrp.histo.GetBinWidth(1)
    histo = wrp.histo.Rebin(
        len(bin_bounds) - 1,
        wrp.name,
        bin_bounds
    )
    if norm_by_bin_width:
        for i in xrange(histo.GetNbinsX()+1):
            factor = histo.GetBinWidth(i) / orig_bin_width
            histo.SetBinContent(i, histo.GetBinContent(i) / factor)
            histo.SetBinError(i, histo.GetBinError(i) / factor)
    info = wrp.all_info()
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def rebin_nbins_max(wrp, nbins_max):
    """
    Applies to HistoWrapper. Returns Histowrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 4, .5, 4.5)
    >>> h1.Fill(1)
    1
    >>> h1.Fill(2)
    2
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2.)
    >>> w2=rebin_nbins_max(w1, 2)
    >>> w1.histo.GetNbinsX()
    4
    >>> w2.histo.GetNbinsX()
    2
    >>> w2.histo.GetBinContent(1)
    2.0
    >>> w2.histo.GetBinContent(2)
    0.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "rebin_nbins_max needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    if isinstance(wrp.histo, ROOT.TH2) or isinstance(wrp.histo, ROOT.TH3):
        raise WrongInputError(
            "rebin_nbins_max needs histograms of type TH1. histo: "
            + str(wrp)
        )

    nbins = wrp.obj.GetNbinsX()
    if nbins <= nbins_max:
        return wrp

    n_bins_to_one = math.ceil(float(nbins) / nbins_max)
    histo = wrp.histo.Rebin(int(n_bins_to_one), wrp.name)
    info = wrp.all_info()
    return wrappers.HistoWrapper(histo, **info)


@history.track_history
def trim(wrp, left=True, right=True):
    """
    Applies to HistoWrapper. Returns Histowrapper.

    If left / right are set to values, these are applied. Otherwise empty bins
    are cut off.

    >>> from ROOT import TH1I
    >>> w1 = wrappers.HistoWrapper(TH1I("h1", "", 10, .5, 10.5))
    >>> w1.histo.Fill(5)
    5
    >>> w2 = trim(w1)
    >>> w2.histo.GetNbinsX()
    1
    >>> w2.histo.GetXaxis().GetXmin()
    4.5
    >>> w2.histo.GetXaxis().GetXmax()
    5.5
    >>> w2 = trim(w1, 3.5, 7.5)
    >>> w2.histo.GetNbinsX()
    4
    >>> w2.histo.GetXaxis().GetXmin()
    3.5
    >>> w2.histo.GetXaxis().GetXmax()
    7.5
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "trim needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )

    # find left / right values if not given
    histo = wrp.histo
    axis = histo.GetXaxis()
    n_bins = histo.GetNbinsX()
    if type(left) == bool:
        if left:
            for i in xrange(n_bins+1):
                if histo.GetBinContent(i):
                    left = axis.GetBinLowEdge(i)
                    break
        else:
            left = axis.GetXmin()
    if type(right) == bool:
        if right:
            for i in xrange(n_bins+1, 0, -1):
                if histo.GetBinContent(i):
                    right = axis.GetBinUpEdge(i)
                    break
        else:
            right = axis.GetXmax()
    if left >= right:
        raise OperationError("bounds: left >= right")

    # create new bin_bounds
    index = 0
    while axis.GetBinLowEdge(index) < left:
        index += 1
    bin_bounds = [axis.GetBinLowEdge(index)]
    while axis.GetBinUpEdge(index) <= right:
        bin_bounds.append(axis.GetBinUpEdge(index))
        index += 1

    return rebin(wrp, bin_bounds)


@history.track_history
def mv_in(wrp, overflow=True, underflow=True):
    """
    Moves under- and/or overflow bin into first/last bin.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 4.5)
    >>> h1.Fill(0)
    -1
    >>> h1.Fill(5,3)
    -1
    >>> w1 = wrappers.HistoWrapper(h1)
    >>> w1.histo.Integral()
    0.0
    >>> w2 = mv_in(w1, False, False)
    >>> w2.histo.Integral()
    0.0
    >>> w3 = mv_in(w1, True, False)
    >>> w3.histo.Integral()
    3.0
    >>> w4 = mv_in(w1, False, True)
    >>> w4.histo.Integral()
    1.0
    >>> w5 = mv_in(w1, True, True)
    >>> w5.histo.Integral()
    4.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "mv_in needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    histo = wrp.histo.Clone()
    nbins = histo.GetNbinsX()
    if underflow:
        firstbin = histo.GetBinContent(0)
        firstbin += histo.GetBinContent(1)
        histo.SetBinContent(1, firstbin)
        histo.SetBinContent(0, 0.)
    if overflow:
        lastbin = histo.GetBinContent(nbins + 1)
        lastbin += histo.GetBinContent(nbins)
        histo.SetBinContent(nbins, lastbin)
        histo.SetBinContent(histo.GetNbinsX() + 1, 0.)
    return wrappers.HistoWrapper(histo, **wrp.all_info())


@history.track_history
def integral(wrp, use_bin_width=False):
    """
    Integral. Applies to HistoWrapper. Returns FloatWrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 4.5)
    >>> h1.Fill(1)
    1
    >>> h1.Fill(3,3)
    2
    >>> w1 = wrappers.HistoWrapper(h1)
    >>> w2 = integral(w1)
    >>> w2.float
    4.0
    >>> w3 = integral(w1, True)
    >>> w3.float
    8.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "integral needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    option = "width" if use_bin_width else ""
    info = wrp.all_info()
    return wrappers.FloatWrapper(wrp.histo.Integral(option), **info)


@history.track_history
def int_l(wrp, use_bin_width=False):
    """
    Left-sided integral. Applies to HistoWrapper. Returns HistoWrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 4.5)
    >>> h1.Fill(1)
    1
    >>> h1.Fill(3,2)
    2
    >>> w1 = wrappers.HistoWrapper(h1)
    >>> w2 = int_l(w1)
    >>> w2.histo.GetBinContent(1)
    1.0
    >>> w2.histo.GetBinContent(2)
    3.0
    >>> w2 = int_l(w1, True)
    >>> w2.histo.GetBinContent(1)
    2.0
    >>> w2.histo.GetBinContent(2)
    6.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "int_l needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    int_histo = wrp.histo.Clone()
    option = "width" if use_bin_width else ""
    for i in xrange(int_histo.GetNbinsX(), 0, -1):
        error = ctypes.c_double()
        value = int_histo.IntegralAndError(1, i, error, option)
        int_histo.SetBinContent(i, value)
        int_histo.SetBinError(i, error.value)
    info = wrp.all_info()
    return wrappers.HistoWrapper(int_histo, **info)


@history.track_history
def int_r(wrp, use_bin_width=False):
    """
    Applies to HistoWrapper. Returns HistoWrapper.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 4.5)
    >>> h1.Fill(1)
    1
    >>> h1.Fill(3,2)
    2
    >>> w1 = wrappers.HistoWrapper(h1)
    >>> w2 = int_r(w1)
    >>> w2.histo.GetBinContent(1)
    3.0
    >>> w2.histo.GetBinContent(2)
    2.0
    >>> w2 = int_r(w1, True)
    >>> w2.histo.GetBinContent(1)
    6.0
    >>> w2.histo.GetBinContent(2)
    4.0
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "int_r needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )
    int_histo = wrp.histo.Clone()
    option = "width" if use_bin_width else ""
    n_bins = int_histo.GetNbinsX()
    for i in xrange(1, 1 + n_bins):
        error = ctypes.c_double()
        value = int_histo.IntegralAndError(i, n_bins, error, option)
        int_histo.SetBinContent(i, value)
        int_histo.SetBinError(i, error.value)
    info = wrp.all_info()
    return wrappers.HistoWrapper(int_histo, **info)


@history.track_history
def chi2(wrps, x_min=0, x_max=0):
    """
    Expects two Histowrappers. Returns FloatWrapper.
    """
    wrps = iterableize(wrps)
    wrps = iter(wrps)
    try:
        first, second = next(wrps), next(wrps)
    except StopIteration:
        raise TooFewWrpsError("chi2 needs exactly two HistoWrappers.")
    try:
        wrps.next()
        raise TooManyWrpsError("chi2 needs exactly two HistoWrappers.")
    except StopIteration:
        pass
    for w in (first, second):
        if not isinstance(w, wrappers.HistoWrapper):
            raise WrongInputError(
                "chi2 needs type HistoWrapper. w: "
                + str(w)
            )
    if first.histo.GetNbinsX() != second.histo.GetNbinsX():
        raise WrongInputError(
            "chi2 needs histos with same number of bins."
        )
    if not x_max:
        x_max = int(first.histo.GetNbinsX() - 1)

    def get_weight_for_bin(i):
        val = (first.histo.GetBinContent(i+1)
               - second.histo.GetBinContent(i+1))**2
        err1 = first.histo.GetBinError(i+1)
        err2 = second.histo.GetBinError(i+1)
        if err1 and err2:
            return val / (err1**2 + err2**2)
        else:
            return 0.

    chi2_val = __builtin__.sum(
        get_weight_for_bin(i)
        for i in xrange(x_min, x_max)
    )
    info = second.all_info()
    info.update(first.all_info())
    return wrappers.FloatWrapper(
        chi2_val,
        **info
    )


@history.track_history
def eff(wrps, option='cl=0.683 b(1,1) mode'):
    """
    Applies to HistoWrappers only. Returns GraphWrapper. Takes lumi from first.

    >>> from ROOT import TH1I
    >>> h1 = TH1I("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1)
    1
    >>> h1.Fill(1)
    1
    >>> w1 = wrappers.HistoWrapper(h1, lumi=2)
    >>> h2 = TH1I("h2", "", 2, .5, 2.5)
    >>> h2.Sumw2()
    >>> h2.Fill(1)
    1
    >>> h2.Fill(1)
    1
    >>> h2.Fill(1)
    1
    >>> h2.Fill(2)
    2
    >>> w2 = wrappers.HistoWrapper(h2, lumi=3)
    >>> w3 = eff([w1, w2])
    >>> w3.graph.GetN()
    2
    >>> hi = w3.graph.GetErrorYhigh(0)
    >>> lo = w3.graph.GetErrorYlow(0)
    >>> abs(hi - 0.189572034007) < 1e-10
    True
    >>> abs(lo - 0.236650832868) < 1e-10
    True
    """
    wrps = iterableize(wrps)
    wrps = iter(wrps)
    try:
        nominator = next(wrps)
        denominator = next(wrps)
    except StopIteration:
        raise TooFewWrpsError("eff needs exactly two Wrappers.")
    try:
        wrps.next()
        raise TooManyWrpsError("eff needs exactly two Wrappers.")
    except StopIteration:
        pass
    if not isinstance(nominator, wrappers.HistoWrapper):
        raise WrongInputError(
            "eff needs nominator to be of type HistoWrapper. nominator: "
            + str(nominator)
        )
    if not isinstance(denominator, wrappers.HistoWrapper):
        raise WrongInputError(
            "eff needs denominator to be of type HistoWrapper. denominator: "
            + str(denominator)
        )

    graph = TGraphAsymmErrors(nominator.histo, denominator.histo, option)
    graph.GetXaxis().SetTitle(nominator.histo.GetXaxis().GetTitle())
    graph.GetYaxis().SetTitle('efficiency')
    info = nominator.all_info()
    return wrappers.GraphWrapper(graph, **info)


@history.track_history
def th2_projection(wrp, projection,
                   name='_p', firstbin=0, lastbin=-1, option='eo'):
    """
    Applies to HistoWrapper with TH2 type. Returns HistoWrapper.

    >>> from ROOT import TH2I
    >>> h1 = TH2I("h1", "", 2, -.5, 1.5, 2, -.5, 1.5)
    >>> h1.Fill(0,1)
    9
    >>> h1.Fill(1,1,2)
    10
    >>> h1.Fill(1,0,3)
    6
    >>> w1 = wrappers.HistoWrapper(h1)
    >>> w2 = th2_projection(w1, 'x')
    >>> w2.histo.GetBinContent(1)
    1.0
    >>> w2.histo.GetBinContent(2)
    5.0
    >>> w2 = th2_projection(w1, 'y')
    >>> w2.histo.GetBinContent(1)
    3.0
    >>> w2.histo.GetBinContent(2)
    3.0
    """
    projection = projection.lower()
    if projection not in ('x', 'y'):
        raise WrongInputError(
            'th2d_projection needs ``projection`` argument to be one of '
            '("x", "y"). projection: ' + str(projection)
        )
    if not (isinstance(wrp, wrappers.HistoWrapper) and 'TH2' in wrp.type):
        raise WrongInputError(
            'th2d_projection needs argument of type HistoWrapper with TH2 type '
            'histo. Histo: ' + str(wrp)
        )
    name += projection
    th2 = wrp.histo
    if projection == 'x':
        histo = th2.ProjectionX(name, firstbin, lastbin, option)
    else:
        histo = th2.ProjectionY(name, firstbin, lastbin, option)
    histo.SetDirectory(0)
    info = wrp.all_info()
    info['name'] += name
    histo.SetName(info['name'])
    info['in_file_path'] += '_p' + projection
    return wrappers.HistoWrapper(histo, **info)


def th2_projection_x(wrp, name='_p', firstbin=0, lastbin=-1, option='eo'):
    """Proxy for th2_projection."""
    return th2_projection(wrp, 'x', name, firstbin, lastbin, option)


def th2_projection_y(wrp, name='_p', firstbin=0, lastbin=-1, option='eo'):
    """Proxy for th2_projection."""
    return th2_projection(wrp, 'y', name, firstbin, lastbin, option)


@history.track_history
def squash_sys_sq(wrps):
    """
    Calculates systematic uncertainty with sum of squares.
    :param wrps:    iterable of histowrappers, where the
                    first item is taken as the nominal histogram.
    >>> from ROOT import TH1F
    >>> h0 = TH1F("h0", "", 2, .5, 2.5)
    >>> h0.Fill(1, 10)
    1
    >>> h0 = wrappers.HistoWrapper(h0)
    >>> h1_sys = TH1F("h1_sys", "", 2, .5, 2.5)
    >>> h1_sys.Fill(1, 10.5)
    1
    >>> h1_sys.SetBinError(1, 4.5)
    >>> h1_sys = wrappers.HistoWrapper(h1_sys)
    >>> h2_sys = TH1F("h2_sys", "", 2, .5, 2.5)
    >>> h2_sys.Fill(1, 14.5)
    1
    >>> h2_sys.SetBinError(1, 7.5)
    >>> h2_sys = wrappers.HistoWrapper(h2_sys)
    >>> w2 = squash_sys_sq([h0, h1_sys, h2_sys])
    >>> w2.obj.GetBinContent(1)
    10.0
    >>> w2.histo_sys_err.GetBinContent(1)
    14.0
    >>> w2.histo_sys_err.GetBinError(1)
    9.0
    """
    n_sys_hists = 0
    nominal = None
    sys_hist = None
    sum_of_sq_errs_up = None
    sum_of_sq_errs_down = None
    min_errs = None
    info = None

    def get_err_hist(h, err_factor):
        w_err = h.Clone()
        for i in xrange(w_err.GetNbinsX()+2):
            w_err.SetBinContent(i, h.GetBinContent(i)
                + h.GetBinError(i)*err_factor)
        return w_err

    def add_del_sq(sys_h, err_sign):
        delta = nominal.Clone()
        delta.Add(get_err_hist(sys_h, err_sign), -1)
        delta.Multiply(delta)  # square
        delta.Add(min_errs)
        return delta

    def get_sqr_hist(hist):
        for i in xrange(hist.GetNbinsX()+2):
            hist.SetBinContent(i, hist.GetBinContent(i)**.5)

    for w in wrps:                                              # histo check
        if not (isinstance(w, wrappers.HistoWrapper) and 'TH1' in w.type):
            raise WrongInputError(
                "squash_sys_sq accepts only HistoWrappers. wrp: "
                + str(w)
            )

        if not nominal:                                         # init
            info = w.all_info()
            nominal = w.histo.Clone()
            sys_hist = w.histo.Clone()
            sys_hist.Reset()
            sum_of_sq_errs_up = sys_hist.Clone()
            sum_of_sq_errs_down = sys_hist.Clone()
            min_errs = sys_hist.Clone()
            for i in xrange(sys_hist.GetNbinsX()+2):
                min_errs.SetBinContent(i, 1e-10)  # make non-zero

        else:                                                   # collect
            n_sys_hists += 1
            sum_of_sq_errs_up.Add(add_del_sq(w.histo, +1))
            sum_of_sq_errs_down.Add(add_del_sq(w.histo, -1))

    assert n_sys_hists, 'At least one systematic histogram needed.'

    get_sqr_hist(sum_of_sq_errs_up)
    get_sqr_hist(sum_of_sq_errs_down)
    sum_of_sq_errs_up.Add(nominal)
    sum_of_sq_errs_down.Add(nominal, -1)
    sum_of_sq_errs_down.Scale(-1)

    # average and assign errors
    # sys_hist.Scale(1./n_sys_hists)
    for i in xrange(sys_hist.GetNbinsX()+2):
        sys_hist.SetBinContent(i, (sum_of_sq_errs_up.GetBinContent(i)
            + sum_of_sq_errs_down.GetBinContent(i))/2.)
        sys_hist.SetBinError(i, (sum_of_sq_errs_up.GetBinContent(i)
            - sum_of_sq_errs_down.GetBinContent(i))/2.)

    info['histo_sys_err'] = sys_hist
    return wrappers.HistoWrapper(nominal, **info)


@history.track_history
def squash_sys_env(wrps):
    """
    Calculates envelope of systematic uncertainties.

    If any of the 'histo_sys_err' is set on the inputs, these systematic
    histograms are used for the envelope, including their uncertainties, and the
    result is stored in histo_sys_err of the returned wrp. Here, the histogram
    from the first wrp is returned as the nominal one.

    Otherwise, the envelope is built around the nominal values of the
    histograms (wrp.histo) and also stored returned in wrp.histo, and
    histo_sys_err stays unset.

    :param wrps:    iterable of histowrappers

    >>> from ROOT import TH1F
    >>> h1 = TH1F("h1", "", 2, .5, 2.5)
    >>> h2 = TH1F("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1, 2)
    1
    >>> h2.Fill(1, 4)
    1
    >>> ws = list(wrappers.HistoWrapper(h) for h in [h1, h2])
    >>> w1 = squash_sys_env(ws)
    >>> w1.histo_sys_err  # Should be None
    >>> w1.obj.GetBinContent(1)
    3.0
    >>> w1.obj.GetBinError(1)
    1.0
    """
    wrps = list(wrps)
    assert len(wrps) > 1, 'At least 2 wrps are needed.'

    for w in wrps:                                              # histo check
        if not (isinstance(w, wrappers.HistoWrapper) and 'TH1' in w.type):
            raise WrongInputError(
                "squash_sys_env accepts only HistoWrappers. wrp: "
                + str(w)
            )

    nominal = wrps[0].histo.Clone()
    sys_hist = wrps[0].histo.Clone()

    def get_err(w, i, err_factor):
        if w.histo_sys_err:
            return (w.histo_sys_err.GetBinContent(i)
                    + w.histo_sys_err.GetBinError(i)*err_factor)
        else:
            return w.histo.GetBinContent(i)

    for i in xrange(nominal.GetNbinsX()+2):
        mini = min(get_err(w, i, -1) for w in wrps)
        maxi = max(get_err(w, i, +1) for w in wrps)
        avg, err = (mini + maxi)/2., (maxi - mini)/2.
        sys_hist.SetBinContent(i, avg)
        sys_hist.SetBinError(i, err)

    info = wrps[0].all_info()
    if any(w.histo_sys_err for w in wrps):
        info['histo_sys_err'] = sys_hist
    else:
        nominal = sys_hist
    return wrappers.HistoWrapper(nominal, **info)


@history.track_history
def squash_sys_stddev(wrps):
    """
    Calculates standard deviation for systematic uncertainties.

    Result is stored in wrp.histo_sys_err, and wrp.histo is from the first wrp.

    >>> from ROOT import TH1F
    >>> h1 = TH1F("h1", "", 2, .5, 2.5)
    >>> h2 = TH1F("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1, 2)
    1
    >>> h2.Fill(1, 4)
    1
    >>> ws = list(wrappers.HistoWrapper(h) for h in [h1, h2])
    >>> w1 = squash_sys_stddev(ws)
    >>> w1.histo.GetBinContent(1)
    2.0
    >>> w1.histo_sys_err.GetBinContent(1)
    3.0
    >>> w1.histo_sys_err.GetBinError(1)
    1.0
    """
    import numpy
    wrps = list(wrps)
    assert len(wrps) > 1, 'At least 2 wrps are needed.'

    for w in wrps:                                              # histo check
        if not (isinstance(w, wrappers.HistoWrapper) and 'TH1' in w.type):
            raise WrongInputError(
                "squash_sys_stddev accepts only HistoWrappers. wrp: "
                + str(w)
            )

    histos = list(w.histo for w in wrps)
    histo = histos[0].Clone()
    histo_sys_err = histos[0].Clone()
    for i in xrange(histo.GetNbinsX()+2):
        x = numpy.array(list(h.GetBinContent(i) for h in histos))
        histo_sys_err.SetBinContent(i, x.mean())
        histo_sys_err.SetBinError(i, x.var()**.5)

    info = wrps[0].all_info()
    info['histo_sys_err'] = histo_sys_err
    return wrappers.HistoWrapper(histo, **info)


def get_sys_int(wrp, use_bin_width=False):
    """
    Calculates standard deviation for systematic uncertainties.

    Result is stored in wrp.histo_sys_err, and wrp.histo is from the first wrp.

    >>> from ROOT import TH1F
    >>> h1 = TH1F("h1", "", 2, .5, 2.5)
    >>> h2 = TH1F("h1", "", 2, .5, 2.5)
    >>> h1.Fill(1, 2)
    1
    >>> h2.Fill(1, 3)
    1
    >>> h2.SetBinError(1, 2)
    >>> w = wrappers.HistoWrapper(h1)
    >>> w.histo_sys_err = h2
    >>> get_sys_int(w)
    (3.0, -1.0)
    """
    if not isinstance(wrp, wrappers.HistoWrapper):
        raise WrongInputError(
            "get_sys_int needs argument of type HistoWrapper. histo: "
            + str(wrp)
        )

    if not wrp.histo_sys_err:
        raise WrongInputError(
            "get_sys_int needs histo with systematic uncertainty."
        )

    nom_hist = wrp.histo
    sys_up = wrp.histo_sys_err.Clone()
    sys_down = wrp.histo_sys_err.Clone()

    for i in xrange(sys_up.GetNbinsX()+2):
        sys_up.SetBinContent(i, sys_up.GetBinContent(i)+sys_up.GetBinError(i))
        sys_down.SetBinContent(i, sys_down.GetBinContent(i)-sys_down.GetBinError(i))

    option = "width" if use_bin_width else ""
    up_uncert = sys_up.Integral(option) - nom_hist.Integral(option)
    down_uncert = sys_down.Integral(option) - nom_hist.Integral(option)

    if up_uncert < 0 or down_uncert > 0:
        raise WrongIntegralError(
            "Uncertainty integrals with wrong sign: %s %s" % (up_uncert, down_uncert)
        )

    return up_uncert, down_uncert


if __name__ == "__main__":
    import ROOT
    ROOT.TH1.AddDirectory(False)
    import doctest
    doctest.testmod()


# TODO remove all special errors and replace with simple assert statements
# TODO def squash_info_data(list_of_info_dicts) => fix is_signal, ...

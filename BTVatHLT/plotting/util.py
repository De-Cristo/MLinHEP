import numpy as np
import awkward as ak
import matplotlib.pyplot as plt
import uproot as u
from train_vars import *
import os
import sys
import argparse

import boost_histogram as bh
import mplhep as hep

from matplotlib.ticker import AutoMinorLocator

def plot_manager(args):
    print(args[1])
    data = ak.flatten(args[0].array(), axis=None)
    plot_histo(args[1], data, args[2])

def save_plot_batch( plot_str ):
    plt.savefig(plot_str)
    plt.show()
    plt.close()

def plot_histo(var, data, outDir):
    plt.style.use(hep.style.ROOT)
    
    n, binning, patch = plt.hist(data,
             color='r', 
             alpha=0.5, 
             bins = plot_configs[var]["bins"],
             log = plot_configs[var]["log"],
             histtype='stepfilled', 
             density=True,
             label='{}'.format(var))
    scale = len(data) / sum(n)
    err   = np.sqrt(n * scale) / scale
    width = (binning[1] - binning[0])
    center = (binning[:-1] + binning[1:]) / 2
    plt.errorbar(center, n, yerr=err, fmt='o', c='r', alpha = 0.8)
        
    plt.legend(loc='best',frameon=True,edgecolor='blue',facecolor='blue') 
    plt.legend()
    plt.xlabel('{}'.format(var),fontsize=16)
    plt.ylabel("Arbitrary Units [Events = {}]".format(len(data)),fontsize=16)
    save_plot_batch('{0}/{1}.png'.format(outDir,var))
    
def plot_comparison_manager(args): #arguement = [array1, array2, _var, ourDir]
    var = args [2]
    outDir = args [3]
    print(var)
    
    plt.style.use(hep.style.ROOT)
    
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.subplots_adjust(hspace=0)
    
    data = args[0]
    label1 = args[4]
    n1, binning, patch = ax[0].hist(data,
             color='r', 
             alpha=0.5, 
             bins = plot_configs[var]["bins"],
             log = plot_configs[var]["log"],
             histtype='stepfilled', 
             density=True,
             label='{}'.format(label1))
    scale = len(data) / sum(n1)
    err1   = np.sqrt(n1 * scale) / scale
    width = (binning[1] - binning[0])/2
    center = (binning[:-1] + binning[1:]) / 2
    ax[0].errorbar(center, n1, yerr=err1, fmt='o', c='r', alpha = 0.8)
    
    data = args[1]
    label2 = args[5]
    n2, binning, patch = ax[0].hist(data,
             color='b', 
             alpha=0.5, 
             bins = plot_configs[var]["bins"],
             log = plot_configs[var]["log"],
             histtype='stepfilled', 
             density=True,
             label='{}'.format(label2))
    scale = len(data) / sum(n2)
    err2   = np.sqrt(n2 * scale) / scale
    width = (binning[1] - binning[0])/2
    center = (binning[:-1] + binning[1:]) / 2
    ax[0].errorbar(center, n2, yerr=err2, fmt='o', c='b', alpha = 0.8)
    
    ax[0].legend(loc='best',frameon=True,edgecolor='blue',facecolor='blue') 
    ax[0].legend()
    ax[0].set_xlabel('{}'.format(var),fontsize=16)
    ax[0].set_ylabel("Arbitrary Units; [{0} = {1}; {2} = {3}] ".format(label1,len(args[0]),label2,len(args[1])),fontsize=16)
    
    ratio = n2/(n1+1e-9)
    ratio_error = np.sqrt(err2**2+err1**2)
    ax[1].errorbar(
        center,
        ratio,
        xerr=width,
        yerr=ratio_error,
        color="black",
        ecolor="r",
        linestyle="None",
        marker=None,
    )
    ax[1].axhline(y=1.0, linestyle="dashed", color="grey", alpha=0.5)
    ax[1].xaxis.set_minor_locator(AutoMinorLocator())
    ax[1].tick_params(which='minor', length=4, color='black')
    ax[1].set_ylabel(
        "$\\frac{{{0}}}{{{1}}}$".format(args[5], args[4])
    )
    ax[1].set_xlabel('{}'.format(var),fontsize=16)
    save_plot_batch('{0}/{1}.png'.format(outDir,var))
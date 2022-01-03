#!/usr/bin/env python
# coding: utf-8
# Author: Licheng ZHANG [licheng.zhang@cern.ch]
# # Demonstration of distribution reweighting
# 
#     requirements:
#     xgboost
#     numpy
#     matplotlib
#     sklearn
#     pandas
#     ROOT 6
#     IF ROOT 6.20+ RDataFrame can directly generate Numpy Array with AsNumpy()
#     More general, following packages can be used.
#     uproot (using python 3, download root_numpy from official web and install by hand)
#     root_numpy (using python 2.7, download root_numpy from official web and install by hand) if uproot is not avaliable

# In[1]:

from __future__ import division
import xgboost as xgb 
from xgboost import plot_importance
from xgboost import plot_tree
from xgboost import XGBClassifier

import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
import pandas as pd

import uproot
# dihiggs = uproot.concatenate(f"{basedir}/hh2b2w.root:tree",library="pd")
# ttbar = uproot.concatenate(f"{basedir}/ttbar.root:tree",library="pd")
# import root_numpy
# from array import array
import ROOT as R
from ROOT import TCut
import time as timer

from Tools.util import *
import sys
import os
import argparse

R.gROOT.SetBatch(True)
time_start=timer.time()

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--MultThread",dest="MT",  type=int, default=16,   help="How many threads will be used (default = 16)" )
parser.add_argument("-v", "--Verbose",   dest="verb",type=int, default=0,    help="different verbose level (default = 0)" )
parser.add_argument("-d", "--Direction", dest="dir", type=str, default='../Tools/Pre_SlimmedSignal', help="Direction of the training samples (default = ../Tools/Pre_SlimmedSignal)")
parser.add_argument("-lc", "--LowCoupling", dest="LC", type=str, default='0', help="Low Coupling value (default = 0)")
parser.add_argument("-hc", "--HighCoupling",dest="HC", type=str, default='10',help="High Coupling value (default = 10")
args = parser.parse_args()

if args.MT != 0:
    R.EnableImplicitMT(args.MT)
    print('using ' + str(args.MT) + ' threads in MT Mode!')
else:
    print('Disable MT Mode!')

path = os.path.abspath(args.dir)
os.system('mkdir -p C2V_Variables_Plots')
plot_path = os.path.abspath('./C2V_Variables_Plots')

sample_pool = os.listdir(path)
for _sample in sample_pool:
    if 'C2V_{}_0'.format(args.LC) in _sample and 'new_weight' in _sample:
        low_coupling_key = path+'/'+_sample
        print(low_coupling_key)
#     elif 'C2V_{}_0'.format(args.HC) in _sample and 'new_sample' in _sample:
    elif 'new_sample' in _sample:
        high_coupling_key = path+'/'+_sample
        print(high_coupling_key)
    else:
        continue

rdf_dict['LC'] = R.RDataFrame('Events',low_coupling_key)
rdf_dict['HC'] = R.RDataFrame('Events',high_coupling_key)

variable("VHH_V_H2_dPhi", ";#Delta #Phi(V,H2);", [20, 0., 3.5])

for key, items in variables.items():
    plot_vars_as_ROOT_ML('LC','HC',key,items,plot_path)
    

time_end=timer.time()
print('totally cost',time_end-time_start)
exit(0)


# np_rdf_dict['LC'] = rdf_dict['LC'].AsNumpy()
# np_rdf_dict['HC'] = rdf_dict['HC'].AsNumpy()

# print(np_rdf_dict['LC'])
# pds = pd.DataFrame(np_rdf_dict['LC'])
# print(pds)



for keys,item in variables.items():
    print(keys)
    print(variables[keys].title)


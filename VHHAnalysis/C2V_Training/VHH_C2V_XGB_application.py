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
import pylab as pl
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
# from pandarallel import pandarallel
# pandarallel.initialize(nb_workers=4)

import uproot
# dihiggs = uproot.concatenate(f"{basedir}/hh2b2w.root:tree",library="pd")
# ttbar = uproot.concatenate(f"{basedir}/ttbar.root:tree",library="pd")
# import root_numpy
# from array import array
import ROOT as R
from ROOT import TCut
import time as timer

from Tools.util import *
from Tools.analysis_branch import *
import sys
import os
import argparse

from multiprocessing import Pool

def plotter(_arg):
    print('\033[1;33m Variable :: {} Checked \033[0m'.format(_arg[0]))
    plot_vars_as_ROOT_ML('LC','HC',_arg[0],_arg[1],_arg[2])
    
R.gROOT.SetBatch(True)
time_start=timer.time()

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--MultThread",dest="MT",    type=int, default=16,   help="How many threads will be used (default = 16)" )
parser.add_argument("-d", "--Direction", dest="dir",   type=str, default='./Application_Samples/', help="Direction of the training samples (default = ./Application_Samples/)")
args = parser.parse_args()

if args.MT != 0:
    R.EnableImplicitMT(args.MT)
    print('using ' + str(args.MT) + ' threads in MT Mode!')
else:
    print('Disable MT Mode!')

path = os.path.abspath(args.dir)
_file_pool = os.listdir(path)
file_pool = []

# for _file in _file_pool:
#     if _file in file_list_all:
#         for _root in os.listdir(path+'/'+_file):
#             if '.root' in _root:
#                 file_pool.append(path+'/'+_file+'/'+_root)
#     #endif
# #endloop

for _file in _file_pool:
    if '.root' in _file:
        file_pool.append(path+'/'+_file)
    #endif
#endloop
    
XGBmodel = './XGB_Model/C2V_bdt.json'

xgbc = XGBClassifier()
xgbc.load_model(XGBmodel)
print('\033[1;33m {} models loaded \033[0m'.format(XGBmodel))

def apply_c2v_bdt(file):
    print(file)
    rdf_loop = R.RDataFrame('Events',file)
    np_rdf_loop = rdf_loop.AsNumpy()
    pd_rdf_loop = pd.DataFrame(np_rdf_loop)
    
    train_var = ['VHH_H2H1_pt_ratio','selLeptons_pt_1', 'VHH_Vreco4j_HT',\
                 'VHH_V_H2_dPhi', 'VHH_V_HH_dPhi', 'VHH_V_HH_pT_Ratio',\
                 'VHH_H1_BJet_dR', 'VHH_H2_BJet_dR', \
                 'VHH_H2_e',\
                 'VHH_HH_m', 'VHH_HH_dR', \
                ]
    X = pd_rdf_loop[train_var]
    score_xgb = xgbc.predict_proba(X)[:,1]
        
    data={"xgb_c2v_bdt_score" : score_xgb}
    pd_score_xgb = pd.DataFrame(data)

    post_pd_rdf_loop = pd.concat([pd_rdf_loop,pd_score_xgb],axis=1)
    
    data = post_pd_rdf_loop.to_dict('list')
        
    for _key,_list in data.items():
        data[_key] = np.array(_list,dtype='float')
            
    post_rdf_loop = R.RDF.MakeNumpyDataFrame(data)
    post_rdf_loop.Snapshot('Events',file+'.dat')
    
    cmd = 'mv {0} {0}.bak'.format(file)
    os.system(cmd)
    
    cmd = 'mv {0}.dat {0}'.format(file)
    os.system(cmd)
#end

# apply_c2v_bdt(file_pool[0])

# exit(0)

with Pool(args.MT) as p:
    p.map(apply_c2v_bdt, file_pool)

# for file in file_pool:
#     rdf_loop = R.RDataFrame('Events',file)
#     np_rdf_loop = rdf_loop.AsNumpy()
#     pd_rdf_loop = pd.DataFrame(np_rdf_loop)
    
#     train_var = ['VHH_H2H1_pt_ratio','selLeptons_pt_1', 'VHH_Vreco4j_HT',\
#                  'VHH_V_H2_dPhi', 'VHH_V_HH_dPhi', 'VHH_V_HH_pT_Ratio',\
#                  'VHH_H1_BJet_dR', 'VHH_H2_BJet_dR', \
#                  'VHH_H2_e',\
#                  'VHH_HH_m', 'VHH_HH_dR', \
#                 ]
    
#     X = pd_rdf_loop[train_var]
#     score_xgb = xgbc.predict_proba(X)[:,1]
        
#     data={"xgb_c2v_bdt_score" : score_xgb}
#     pd_score_xgb = pd.DataFrame(data)

#     post_pd_rdf_loop = pd.concat([pd_rdf_loop,pd_score_xgb],axis=1)
    
#     data = post_pd_rdf_loop.to_dict('list')
#     for _key,_list in data.items():
#         data[_key] = np.array(_list)
            
#     post_rdf_loop = R.RDF.MakeNumpyDataFrame(data)
#     post_rdf_loop.Snapshot('Events',file+'.dat')
# #endloop

time_end=timer.time()
print('\033[1;34m totally cost {} seconds. \033[0m'.format(str(time_end-time_start)))
exit(0)

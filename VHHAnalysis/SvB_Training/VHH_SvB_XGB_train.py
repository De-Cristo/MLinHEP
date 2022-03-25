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
import sys
import os
import argparse

from multiprocessing import Pool

def plotter(_arg):
    print('\033[1;33m Variable :: {} Checked \033[0m'.format(_arg[0]))
    plot_vars_as_ROOT_ML('sea','target', _arg[0], _arg[1], _arg[2])
    
R.gROOT.SetBatch(True)
time_start=timer.time()

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--MultThread",dest="MT",    type=int, default=16,   help="How many threads will be used (default = 16)" )
parser.add_argument("-d", "--Direction", dest="dir",   type=str, default='/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple', help="Direction of the training samples (default = /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple)")
parser.add_argument("-s", "--eventSignal", dest="signal", type=str, default='ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0', help="Low Coupling value (default = ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0)")
args = parser.parse_args()

if args.MT != 0:
    R.EnableImplicitMT(args.MT)
    print('using ' + str(args.MT) + ' threads in MT Mode!')
else:
    print('Disable MT Mode!')

bkg_list = ['TT', 'TTBB', 'DY', 'Other']

path = os.path.abspath(args.dir)
os.system('mkdir -p SvB_Variables_Plots_{0}'.format(args.signal))
plot_path = os.path.abspath('./RwT_Variables_Plots_{0}'.format(args.signal))
if args.signal == 1:
    signal_name = 'ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0'
else if args.signal == 10:
    signal_name = 'ZHHTo4B_CV_1_0_C2V_10_0_C3_1_0'
else:
    print('ERROR:: Signal Type should be 1 or 10. EXITTING...')
    exit(0)

print('\033[1;34m Reading Data... \033[0m')

years = ['2016Pre','2016Post','2017','2018']
signal_pool = []
background_pool = []
for _y in years:
    for _file in os.listdir(path+'/'+_y+'/'):
        if signal_name in _file:
            signal_pool.append(os.listdir(path+'/'+_y+'/'+_file))
        else:
            if 'Data' in _file:
                continue
            else:
                background_pool.append(os.listdir(path+'/'+_y+'/'+_file))
            #endif
        #endif
    #endloop
#endloop

rdf_dict['signal'] = R.RDataFrame('Events',sea_events_key)
rdf_dict['background'] = R.RDataFrame('Events',target_events_key)


variable("VHH_H1_BJet1_pT", ";pT(H1,B1) [GeV];",     [20, 0., 500])
variable("VHH_H1_BJet2_pT", ";pT(H1,B2) [GeV];",     [20, 0., 500])

variable("VHH_Vreco4j_HT", ";HT(llbbbb) [GeV];",     [25, 0., 2000])

variable("VHH_H1_pT",       ";pT (H1bb);",             [20, 0., 600.])
variable("VHH_HH_pT",       ";pT (bbbb);",             [20, 0., 800.])
variable("V_pt",            ";pT_V(ll/MET) [GeV];",    [20, 0., 500])

variable("VHH_H1_m",        ";Mass(H1) [GeV];",      [20, 0., 800.])
variable("VHH_HH_m",        ";Mass_HH(jjjj) [GeV];",   [20, 0., 1600])
variable("V_mass",          ";Mass_V(ll/MET) [GeV];",  [20, 0., 600])

variable("VHH_H1_e",        ";Energy(H1bb) [GeV];",      [20, 0., 1500.])
variable("VHH_HH_e",        ";Energy(HHbbbb) [GeV];",    [20, 0., 2000.])

variable("VHH_HH_dR",       ";#Delta R (H1,H2);",      [20, 0., 5.])
variable("VHH_V_H1_dPhi",     ";#Delta #Phi(V,H1);",     [20, 0., 3.2])
variable("VHH_V_HH_dPhi",     ";#Delta #Phi(V,HH);",     [20, 0., 3.2])
variable("VHH_HH_deta",     ";#Delta #Eta (H1,H2);",   [20, 0., 3.])
print('\033[1;34m Plotting Variables... \033[0m')

arg_list = []
for key, items in variables.items():
    arg_list.append([key, items, plot_path])

with Pool(args.MT) as p:
    p.map(plotter, arg_list)
    
print('\033[1;34m Preparing training matrix... \033[0m')

np_rdf_dict['target'] = rdf_dict['target'].AsNumpy()
np_rdf_dict['sea'] = rdf_dict['sea'].AsNumpy()

pd_rdf_dict['target'] = pd.DataFrame(np_rdf_dict['target'])
pd_rdf_dict['sea'] = pd.DataFrame(np_rdf_dict['sea'])

pd_rdf_dict['target'].loc[:, "isSig"] = True
pd_rdf_dict['target'].loc[:, "isBkg"] = False
pd_rdf_dict['sea'].loc[:, "isSig"] = False
pd_rdf_dict['sea'].loc[:, "isBkg"] = True

all_data = pd.concat([pd_rdf_dict['target'],pd_rdf_dict['sea']],axis=0)

train_var = ['VHH_H1_BJet1_pT', 'VHH_H1_BJet2_pT', 'VHH_Vreco4j_HT', \
             'VHH_H1_pT', 'VHH_HH_pT', 'V_pt', \
             'VHH_H1_m', 'VHH_HH_m', 'V_mass', \
             'VHH_H1_e','VHH_HH_e',\
             'VHH_HH_dR','VHH_V_H1_dPhi','VHH_V_HH_dPhi','VHH_HH_deta', \
             'weight'
]

corr_test_var = ['VHH_H1_BJet1_pT', 'VHH_H1_BJet2_pT', 'VHH_Vreco4j_HT', \
             'VHH_H1_pT', 'VHH_HH_pT', 'V_pt', \
             'VHH_H1_m', 'VHH_HH_m', 'V_mass', \
             'VHH_H1_e','VHH_HH_e',\
             'VHH_HH_dR','VHH_V_H1_dPhi','VHH_V_HH_dPhi','VHH_HH_deta', \
             'isSig'
]

corr_test = all_data[corr_test_var]
_bkg = corr_test.loc[corr_test["isSig"] == False]
_sig = corr_test.loc[corr_test["isSig"] == True]

correlations(_bkg.drop('isSig',axis=1), 'bkg')
correlations(_sig.drop('isSig',axis=1), 'sig')
del corr_test, _bkg, _sig

X = all_data[train_var]
y = all_data[['isSig','isBkg']]

test_size=0.1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
w_train = X_train['weight']
w_test = X_test['weight']

pos_scale_count = dict(y_train['isSig'].value_counts())
print(pos_scale_count)
pos_scale = pos_scale_count[False]/pos_scale_count[True]
print('pos_scale = '+str(pos_scale))

X_train.drop('weight',axis=1,inplace=True)
X_test.drop('weight',axis=1,inplace=True)

print('\033[1;33m Splitting train : test = {0} : {1} \033[0m'.format(str(1-test_size),str(test_size)))
print('\033[1;33m Start training : \033[0m')

xgbc = XGBClassifier(
    max_depth=2,
    n_estimators=5000,
    learning_rate =0.002,
    nthread=args.MT,
    scale_pos_weight=pos_scale,
)

eval_set = [(X_train, y_train), (X_test, y_test)]
xgbc.fit(
    X=X_train, y=y_train['isSig'], 
    sample_weight=w_train.map(lambda x: x if x>0 else 0),
#     eval_set = eval_set,
    eval_metric=["error", "logloss"], 
    verbose=True
)

test_score_xgb = xgbc.predict_proba(X_test)
test_score_xgb_sig = test_score_xgb[y_test['isSig']][:,1]
test_score_xgb_bkg = test_score_xgb[y_test['isBkg']][:,1]

train_score_xgb = xgbc.predict_proba(X_train)
train_score_xgb_sig = train_score_xgb[y_train['isSig']][:,1]
train_score_xgb_bkg = train_score_xgb[y_train['isBkg']][:,1]

print('\033[1;33m Plotting supporting figures \033[0m')
w_train_score_sig = w_train[y_train['isSig']].values
w_train_score_bkg = w_train[y_train['isBkg']].values
w_test_score_sig = w_test[y_test['isSig']].values
w_test_score_bkg = w_test[y_test['isBkg']].values

decisions = []
decisions += [test_score_xgb_sig,test_score_xgb_bkg,train_score_xgb_sig,train_score_xgb_bkg]

low = min(np.min(d) for d in decisions)
high = max(np.max(d) for d in decisions)
low_high = (low,high)
bins = 15

plt.hist(train_score_xgb_sig,weights=w_train_score_sig,
         color='r', alpha=0.5, range=low_high, bins=bins,
         histtype='stepfilled', density=True,
         label='target (train)'
)
plt.hist(train_score_xgb_bkg,weights=w_train_score_bkg,
         color='b', alpha=0.5, range=low_high, bins=bins,
         histtype='stepfilled', density=True,
         label='sea (train)'
)

hist, bins = np.histogram(test_score_xgb_sig, weights=w_test_score_sig, bins=bins, range=low_high, density=True)
scale = len(test_score_xgb_sig) / sum(hist)
err   = np.sqrt(hist * scale) / scale
width = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='target (test)')

hist, bins = np.histogram(test_score_xgb_bkg, weights=w_test_score_bkg, bins=bins, range=low_high, density=True)
scale = len(test_score_xgb_bkg) / sum(hist)
err   = np.sqrt(hist * scale) / scale
width = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='sea (test)')

plt.legend(loc='best',frameon=True,edgecolor='blue',facecolor='blue') 
plt.legend()
plt.xlabel("BDT output")
plt.ylabel("Arbitrary units")
# plt.xlim(0,1)
save_plot_batch('./Test_Distribution_{0}_{1}.png'.format(args.bkg,args.target))

plot_importance(xgbc)
save_plot_batch('./Variable_importance_{0}_{1}.png'.format(args.bkg,args.target))

fpr_xgb, tpr_xgb, _thres = metrics.roc_curve(y_test['isSig'],test_score_xgb[:,1])

auc = 0.
for _p in range(1,len(tpr_xgb)):
    auc = auc+tpr_xgb[_p]
auc = auc/len(tpr_xgb)

f, ax = plt.subplots(figsize=(8, 8))
ax.plot(np.linspace(0, 1, 1000), np.linspace(0, 1, 1000), '--', label='random')
ax.plot(fpr_xgb, tpr_xgb, label='XGBoost Classifier')
plt.text(0.6,0.1,'AUC = {:0.3f}'.format(auc),fontsize=18)
ax.set_yscale('linear'); ax.set_xlim(0, 1); ax.set_ylim(1e-3, 1)
ax.set_xlabel('target efficiency', ha='right', x=1.0); ax.set_ylabel('sea efficiency', ha='right', y=1.0)
ax.legend()
save_plot_batch('./ROC_curve_{0}_{1}.png'.format(args.bkg,args.target))

os.system('mkdir -p XGB_Model')
xgbc.save_model('XGB_Model/RwT_bdt_{0}_{1}.json'.format(args.bkg,args.target))
print('\033[1;33m Saving models to XGB_Model \033[0m')

time_end=timer.time()
print('\033[1;34m totally cost {} seconds. \033[0m'.format(str(time_end-time_start)))
exit(0)
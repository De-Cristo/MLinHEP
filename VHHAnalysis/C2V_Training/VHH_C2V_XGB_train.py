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
    plot_vars_as_ROOT_ML('LC','HC',_arg[0],_arg[1],_arg[2])
    
R.gROOT.SetBatch(True)
time_start=timer.time()

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--MultThread",dest="MT",    type=int, default=16,   help="How many threads will be used (default = 16)" )
parser.add_argument("-d", "--Direction", dest="dir",   type=str, default='../Tools/Pre_SlimmedSignal', help="Direction of the training samples (default = ../Tools/Pre_SlimmedSignal)")
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

print('\033[1;34m Reading Data... \033[0m')
sample_pool = os.listdir(path)
for _sample in sample_pool:
    if 'C2V_{}_0'.format(args.LC) in _sample and '_new_' in _sample:
        low_coupling_key = path+'/'+_sample
        print(low_coupling_key)
#     elif 'C2V_{}_0'.format(args.HC) in _sample and '_new_sample_by_7' in _sample:
#         high_coupling_key = path+'/'+_sample
#         print(high_coupling_key)
    elif 'C3_20_0'.format(args.HC) in _sample and '_new_sample' in _sample:
        high_coupling_key = path+'/'+_sample
        print(high_coupling_key)
    else:
        continue

rdf_dict['LC'] = R.RDataFrame('Events',low_coupling_key)
rdf_dict['HC'] = R.RDataFrame('Events',high_coupling_key)

variable("VHH_H1_BJet1_pT", ";pT(H1,B1) [GeV];",     [20, 0., 500])
variable("VHH_H1_BJet_dR",  ";#Delta R(H1B1,H1B2);", [20, 0., 5.])
variable("VHH_H2_BJet_dR",  ";#Delta R(H2B1,H2B2);", [20, 0., 5.])

variable("VHH_V_H2_dPhi", ";#Delta #Phi(V,H2);",   [20, 0., 3.2])
variable("VHH_HH_m",      ";mass_HH(jjjj) [GeV];", [20, 0., 1600])
variable("V_pt",          ";pT_V(ll/MET) [GeV];",  [20, 0., 1000])
variable("selLeptons_pt_0", ";pT_Lep1 [GeV];",     [20, 0., 450])
variable("selLeptons_pt_1", ";pT_Lep2 [GeV];",     [20, 0., 450])
variable("VHH_H2H1_pt_ratio",    ";H2_pT/H1_pT;",  [20, 0., 1.])

print('\033[1;34m Plotting Variables... \033[0m')

arg_list = []
for key, items in variables.items():
    arg_list.append([key, items, plot_path])

# with Pool(args.MT) as p:
#     p.map(plotter, arg_list)

print('\033[1;34m Preparing training matrix... \033[0m')

np_rdf_dict['LC'] = rdf_dict['LC'].AsNumpy()
np_rdf_dict['HC'] = rdf_dict['HC'].AsNumpy()

pd_rdf_dict['LC'] = pd.DataFrame(np_rdf_dict['LC'])
pd_rdf_dict['HC'] = pd.DataFrame(np_rdf_dict['HC'])

pd_rdf_dict['LC'].loc[:, "isSig"] = True
pd_rdf_dict['LC'].loc[:, "isBkg"] = False
pd_rdf_dict['LC'].loc[pd_rdf_dict['LC'].isSig==True,'components'] = 1.0
pd_rdf_dict['HC'].loc[:, "isSig"] = False
pd_rdf_dict['HC'].loc[:, "isBkg"] = True
pd_rdf_dict['HC'].loc[pd_rdf_dict['HC'].isBkg==True,'components'] = 1.0

all_data = pd.concat([pd_rdf_dict['LC'],pd_rdf_dict['HC']],axis=0)
# all_data.insert(0, 'Event_ID', range(0, len(all_data)))

# train_var = [
# 'VHH_H1_BJet1_e','VHH_H1_BJet1_pT','VHH_H1_BJet1_phi','VHH_H1_BJet2_e','VHH_H1_BJet2_pT','VHH_H1_BJet2_phi','VHH_H1_BJet_dR',\
#              'VHH_H1_pT', 'VHH_H1_e', 'VHH_H1_eta', 'VHH_H1_m', 'VHH_H1_phi',\
    
#              'VHH_H2_BJet1_e','VHH_H2_BJet1_pT','VHH_H2_BJet1_phi','VHH_H2_BJet2_e','VHH_H2_BJet2_pT','VHH_H2_BJet2_phi','VHH_H2_BJet_dR',\
#              'VHH_H2_pT', 'VHH_H2_e', 'VHH_H2_eta', 'VHH_H2_m', 'VHH_H2_phi',\
    
#              'VHH_HH_m', 'VHH_HH_e', 'VHH_HH_eta','VHH_HH_deta', 'VHH_HH_dR', 'VHH_HH_dphi', 'VHH_HH_pT', 'VHH_HH_phi',\
    
#              'V_pt','V_mass','V_phi','V_mt',\
#              'VHH_V_e', 'VHH_V_m', 'VHH_V_phi',\
    
#              'selLeptons_eta_0', 'selLeptons_eta_1', 'selLeptons_mass_0', 'selLeptons_mass_1', \
#              'selLeptons_pdgId_0', 'selLeptons_pdgId_1',\
#              'selLeptons_phi_0', 'selLeptons_phi_1', 'selLeptons_pt_0', 'selLeptons_pt_1', 
    
#              'VHH_V_H1_dPhi', 'VHH_V_H2_dPhi', 'VHH_V_HH_dPhi','VHH_V_HH_pT_Ratio',\
    
#              'VHH_H2H1_pt_ratio','VHH_Vreco4j_HT', 'VHH_mass',\
#              'components'
# ]
train_var = [
             'VHH_H1_BJet1_pT','VHH_H1_BJet_dR','VHH_H2_BJet_dR',\
             'VHH_V_H2_dPhi','VHH_HH_m','selLeptons_pt_0','selLeptons_pt_1', 'VHH_H2H1_pt_ratio',\
             'components'
]

corr_test_var = [
             'VHH_H1_BJet1_pT','VHH_H1_BJet_dR','VHH_H2_BJet_dR',\
             'VHH_V_H2_dPhi','VHH_HH_m','selLeptons_pt_0','selLeptons_pt_1', 'VHH_H2H1_pt_ratio',\
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
w_train = X_train['components']
w_test = X_test['components']

pos_scale_count = dict(y_train['isSig'].value_counts())
print(pos_scale_count)
pos_scale = pos_scale_count[False]/pos_scale_count[True]
print('pos_scale = '+str(pos_scale))
    
X_train.drop('components',axis=1,inplace=True)
X_test.drop('components',axis=1,inplace=True)

print('\033[1;33m Splitting train : test = {0} : {1} \033[0m'.format(str(1-test_size),str(test_size)))
print('\033[1;33m Start training : \033[0m')

xgbc = XGBClassifier(
    max_depth=3,
    n_estimators=600,
    learning_rate =0.08,
    nthread=args.MT,
    scale_pos_weight=pos_scale,
)

eval_set = [(X_train, y_train), (X_test, y_test)]
xgbc.fit(
    X=X_train, y=y_train['isSig'], 
#     sample_weight=w_train,
    sample_weight=w_train.map(lambda x: x if x>0 else 0),
#     eval_set = eval_set,
    eval_metric=["error", "logloss"], 
    verbose=True)

# exit(0)
test_score_xgb = xgbc.predict_proba(X_test)
test_score_xgb_sig = test_score_xgb[y_test['isSig']][:,1]
test_score_xgb_bkg = test_score_xgb[y_test['isBkg']][:,1]

# y_pred = xgbc.predict(X_test)
# print(y_pred)
# accuracy = accuracy_score(y_test['isSig'],y_pred)
# print('accuracy: %2.f%%'%(accuracy*100))

train_score_xgb = xgbc.predict_proba(X_train)
train_score_xgb_sig = train_score_xgb[y_train['isSig']][:,1]
train_score_xgb_bkg = train_score_xgb[y_train['isBkg']][:,1]

print('\033[1;33m Plotting supporting figures \033[0m')
# results = xgbc.evals_result()

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
         label='S (train)')
plt.hist(train_score_xgb_bkg,weights=w_train_score_bkg,
         color='b', alpha=0.5, range=low_high, bins=bins,
         histtype='stepfilled', density=True,
         label='B (train)')

hist, bins = np.histogram(test_score_xgb_sig, weights=w_test_score_sig, bins=bins, range=low_high, density=True)
scale = len(test_score_xgb_sig) / sum(hist)
err   = np.sqrt(hist * scale) / scale
width = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')

hist, bins = np.histogram(test_score_xgb_bkg, weights=w_test_score_bkg, bins=bins, range=low_high, density=True)
scale = len(test_score_xgb_bkg) / sum(hist)
err   = np.sqrt(hist * scale) / scale
width = (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

# plt.hist(test_score_xgb_bkg, weights=w_test_score_bkg, label="BKG_test", histtype="stepfilled", alpha=0.5, bins = np.linspace(0,1,15),density=True)
# plt.hist(test_score_xgb_sig, weights=w_test_score_sig, label="SIG_test", histtype="stepfilled", alpha=0.5, bins = np.linspace(0,1,15),density=True)
# plt.hist(train_score_xgb_bkg, weights=w_train_score_bkg, label="BKG_train", histtype="step", bins = np.linspace(0,1,15),density=True)
# plt.hist(train_score_xgb_sig,  weights=w_train_score_sig, label="SIG_train", histtype="step", bins = np.linspace(0,1,15),density=True)

plt.legend()
plt.xlabel("BDT output")
plt.ylabel("Arbitrary units")
# plt.xlim(0,1)
save_plot_batch('./Test_Distribution.png')

plot_importance(xgbc)
save_plot_batch('./Variable_importance.png')

fpr_xgb, tpr_xgb, _thres = metrics.roc_curve(y_test['isSig'],test_score_xgb[:,1])

auc = 0.
for _p in range(1,len(tpr_xgb)):
    auc = auc+tpr_xgb[_p]
auc = auc/len(tpr_xgb)

f, ax = plt.subplots(figsize=(8, 8))
ax.plot(np.linspace(0, 1, 1000), np.linspace(0, 1, 1000), '--', label='random')
ax.plot(fpr_xgb, tpr_xgb, label='XGBoost Classifier')
plt.text(0.8,0.1,'AUC = {:0.3f}'.format(auc),fontsize=18)
ax.set_yscale('linear'); ax.set_xlim(0, 1); ax.set_ylim(1e-3, 1)
ax.set_xlabel('SM Coupling efficiency', ha='right', x=1.0); ax.set_ylabel('High C2V efficiency', ha='right', y=1.0)
ax.legend()
save_plot_batch('./ROC_curve.png')

os.system('mkdir -p XGB_Model')
xgbc.save_model('XGB_Model/C2V_bdt.json')
print('\033[1;33m Saving models to XGB_Model \033[0m')

time_end=timer.time()
print('\033[1;34m totally cost {} seconds. \033[0m'.format(str(time_end-time_start)))
exit(0)

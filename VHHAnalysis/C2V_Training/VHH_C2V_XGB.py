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
    if 'C2V_{}_0'.format(args.LC) in _sample:
        low_coupling_key = path+'/'+_sample
        print(low_coupling_key)
    elif 'C2V_{}_0'.format(args.HC) in _sample:
        high_coupling_key = path+'/'+_sample
        print(high_coupling_key)
    else:
        continue

rdf_dict['LC'] = R.RDataFrame('Events',low_coupling_key)
rdf_dict['HC'] = R.RDataFrame('Events',high_coupling_key)

variable("VHH_V_H2_dPhi", ";#Delta #Phi(V,H2);",   [20, 0., 3.2])
variable("VHH_HH_m",      ";mass_HH(jjjj) [GeV];", [20, 0., 1600])
variable("V_pt",          ";pT_V(ll/MET) [GeV];",  [20, 0., 1000])

print('\033[1;34m Plotting Variables... \033[0m')
for key, items in variables.items():
    print('\033[1;33m Variable :: {} Checked \033[0m'.format(key))
    plot_vars_as_ROOT_ML('LC','HC',key,items,plot_path)
#end

print('\033[1;34m Preparing training matrix... \033[0m')
np_rdf_dict['LC'] = rdf_dict['LC'].AsNumpy()
np_rdf_dict['HC'] = rdf_dict['HC'].AsNumpy()

pd_rdf_dict['LC'] = pd.DataFrame(np_rdf_dict['LC'])
pd_rdf_dict['HC'] = pd.DataFrame(np_rdf_dict['HC'])

pd_rdf_dict['LC'].loc[:, "isSig"] = True
pd_rdf_dict['LC'].loc[:, "isBkg"] = False
pd_rdf_dict['HC'].loc[:, "isSig"] = False
pd_rdf_dict['HC'].loc[:, "isBkg"] = True

all_data = pd.concat([pd_rdf_dict['LC'],pd_rdf_dict['HC']],axis=0)
all_data.insert(0, 'Event_ID', range(0, len(all_data)))

train_var = ['VHH_H2_e', 'VHH_V_H2_dPhi', 'VHH_HH_m', 'V_pt', 'weight']
# train_var = ['VHH_H2_e', 'VHH_V_H2_dPhi', 'VHH_HH_m', 'V_pt']
corr_test_var = ['VHH_H2_e', 'VHH_V_H2_dPhi', 'VHH_HH_m', 'V_pt', 'isSig']

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

X_train.drop('weight',axis=1,inplace=True)
X_test.drop('weight',axis=1,inplace=True)


print('\033[1;33m Splitting train : test = {0} : {1} \033[0m'.format(str(1-test_size),str(test_size)))
print('\033[1;33m Start training : \033[0m')

xgbc = XGBClassifier(
    max_depth=4,
    n_estimators=200,
    learning_rate =0.1,
#     eval_metric='logloss',
    nthread=args.MT
)
eval_set = [(X_train, y_train), (X_test, y_test)]
xgbc.fit(
    X=X_train, y=y_train['isSig'], 
#     sample_weight=w_train,
    sample_weight=w_train.map(lambda x: x*10e5 if x*10e5>10e-5 else 0),
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

# pl.hist(test_score_xgb_bkg, weights=w_test_score_bkg, histtype="stepfilled", bins = np.linspace(0,1,15))
# plt.hist(test_score_xgb_bkg, weights=w_test_score_bkg, "BKG_test", histtype="stepfilled", alpha=0.5, bins = np.linspace(0,1,15),density=True)
plt.hist(test_score_xgb_bkg, weights=w_test_score_bkg, label="BKG_test", histtype="stepfilled", alpha=0.5, bins = np.linspace(0,1,15),density=True)
plt.hist(test_score_xgb_sig, weights=w_test_score_sig, label="SIG_test", histtype="stepfilled", alpha=0.5, bins = np.linspace(0,1,15),density=True)
plt.hist(train_score_xgb_bkg, weights=w_train_score_bkg, label="BKG_train", histtype="step", bins = np.linspace(0,1,15),density=True)
plt.hist(train_score_xgb_sig,  weights=w_train_score_sig, label="SIG_train", histtype="step", bins = np.linspace(0,1,15),density=True)
plt.legend()
plt.xlim(0,1)
save_plot_batch('./Test_Distribution.png')

plot_importance(xgbc)
save_plot_batch('./Variable_importance.png')

fpr_xgb, tpr_xgb, _thres = metrics.roc_curve(y_test['isSig'],test_score_xgb[:,1])

f, ax = plt.subplots(figsize=(8, 8))
ax.plot(np.linspace(0, 1, 1000), np.linspace(0, 1, 1000), '--', label='random')
# ax.plot(tpr_clf, fpr_clf, label='Logistic Regression')
ax.plot(tpr_xgb, fpr_xgb, label='XGBoost Classifier')

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

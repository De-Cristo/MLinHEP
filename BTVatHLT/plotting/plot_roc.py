print("start import")
import os
import matplotlib
matplotlib.use('Agg')
from sklearn.metrics import roc_curve, roc_auc_score
from scipy.interpolate import InterpolatedUnivariateSpline
from pdb import set_trace
from itertools import chain
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import root_numpy
# from root_numpy import full_hist
import ROOT
from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TH2F, TH1F, RDataFrame
print("finish import")

def spit_out_roc(disc,truth_array,selection_array):

    newx = np.logspace(-3.5, 0, 100)
    tprs = pd.DataFrame()
    truth = truth_array[selection_array]*1
    disc = disc[selection_array]
    tmp_fpr, tmp_tpr, _ = roc_curve(truth, disc)
    coords = pd.DataFrame()
    coords['fpr'] = tmp_fpr
    coords['tpr'] = tmp_tpr
    clean = coords.drop_duplicates(subset=['fpr'])
    spline = InterpolatedUnivariateSpline(clean.fpr, clean.tpr,k=1)
    tprs = spline(newx)
    return tprs, newx

pred = []
isDeepJet = True
if isDeepJet:
    listbranch = ['prob_isB', 'prob_isBB','prob_isLeptB', 'prob_isC','prob_isUDS','prob_isG','isB', 'isBB', 'isLeptB', 'isC','isUDS','isG','jet_pt', 'jet_eta']
else:
    listbranch = ['prob_isB', 'prob_isBB', 'prob_isC','prob_isUDSG','isB', 'isBB', 'isC','isUDSG','jet_pt', 'jet_eta']

dirz = '/data/pubfs/zhanglic/workspace/newbox/MLinHEP/BTVatHLT/plotting/output_0620/'
truthfile = open( dirz+'outfiles.txt','r')
print("opened text file")
rfile1 = ROOT.TChain("tree")
count = 0

for line in truthfile:
    count += 1
    if len(line) < 1: continue
    file1name=str(dirz+line.split('\n')[0])
    rfile1.Add(file1name)

print("added files")
rdf = RDataFrame(rfile1)
mpdel_probB = ("vetoc_B","probB",100,0.0,1.0)
histo_vetoc_B_deepjet  = rdf.Filter('isC!=1 && jet_pt>30').Filter('isB || isBB || isLeptB').Define('probB','prob_isB+prob_isBB+prob_isLeptB').Histo1D(mpdel_probB, 'probB')

mpdel_probB = ("vetoc_NB","probB",100,0.0,1.0)
histo_vetoc_NB_deepjet = rdf.Filter('isC!=1 && jet_pt>30').Filter('!(isB || isBB || isLeptB)').Define('probB','prob_isB+prob_isBB+prob_isLeptB').Histo1D(mpdel_probB, 'probB')

mpdel_probB = ("vetoudsg_B","probB",100,0.0,1.0)
histo_vetoudsg_B_deepjet = rdf.Filter('isUDS!=1 && isG!=1 && jet_pt>30').Filter('isB || isBB || isLeptB').Define('probB','prob_isB+prob_isBB+prob_isLeptB').Histo1D(mpdel_probB, 'probB')

mpdel_probB = ("vetoudsg_NB","probB",100,0.0,1.0)
histo_vetoudsg_NB_deepjet = rdf.Filter('isUDS!=1 && isG!=1 && jet_pt>30').Filter('!(isB || isBB || isLeptB)').Define('probB','prob_isB+prob_isBB+prob_isLeptB').Histo1D(mpdel_probB, 'probB')

## PLOTS
c = TCanvas()
ROOT.gStyle.SetOptStat(0000)
histo_vetoc_B_deepjet.SetFillColorAlpha(ROOT.kRed, 0.6)
histo_vetoc_NB_deepjet.SetFillColorAlpha(ROOT.kBlue, 0.6)
histo_vetoc_B_deepjet.DrawNormalized()
histo_vetoc_NB_deepjet.DrawNormalized("SAME")
lg = ROOT.TLegend(0.1,0.7,0.9,0.9)
lg.AddEntry('vetoc_B','B Jets','f')
lg.AddEntry('vetoc_NB','No B Jets (veto C)','f')
lg.SetFillColorAlpha(1,0.1)
lg.SetLineColorAlpha(1,0.0)
lg.Draw("SAME")
c.SaveAs('veto_C.pdf')

c = TCanvas()
ROOT.gStyle.SetOptStat(0000)
histo_vetoudsg_B_deepjet.SetFillColorAlpha(ROOT.kRed, 0.6)
histo_vetoudsg_NB_deepjet.SetFillColorAlpha(ROOT.kBlue, 0.6)
histo_vetoudsg_B_deepjet.DrawNormalized()
histo_vetoudsg_NB_deepjet.DrawNormalized("SAME")
lg = ROOT.TLegend(0.1,0.7,0.9,0.9)
lg.AddEntry('vetoudsg_B','B Jets','f')
lg.AddEntry('vetoudsg_NB','No B Jets (veto UDSG)','f')
lg.SetFillColorAlpha(1,0.1)
lg.SetLineColorAlpha(1,0.0)
lg.Draw("SAME")
c.SaveAs('veto_UDSG.pdf')

ndf = rdf.AsNumpy(columns=listbranch)
# df = root_numpy.tree2array(rfile1, branches = listbranch)
df = pd.DataFrame(ndf)
print("converted to root")

if isDeepJet:
    b_jets = df['isB']+df['isBB']+df['isLeptB']
    disc = df['prob_isB']+df['prob_isBB']+df['prob_isLeptB']
    summed_truth = df['isB']+df['isBB']+df['isLeptB']+df['isC']+df['isUDS']+df['isG']
    veto_c = (df['isC'] != 1) & ( df['jet_pt'] > 30) & (summed_truth != 0)
    veto_udsg = (df['isUDS'] != 1) & (df['isG'] != 1) & ( df['jet_pt'] > 30) & (summed_truth != 0)
else:
    b_jets = df['isB']+df['isBB']
    disc = df['prob_isB']+df['prob_isBB']
    summed_truth = df['isB']+df['isBB']+df['isC']+df['isUDSG']
    veto_c = (df['isC'] != 1) & ( df['jet_pt'] > 30) & (summed_truth != 0)
    veto_udsg = (df['isUDSG'] != 1) & ( df['jet_pt'] > 30) & (summed_truth != 0)


f = ROOT.TFile("ROCS_DeepJet.root", "recreate")

x1, y1 = spit_out_roc(disc,b_jets,veto_c)
x2, y2 = spit_out_roc(disc,b_jets,veto_udsg)

gr1 = TGraph( 100, x1, y1 )
gr1.SetName("roccurve_0")
gr2 = TGraph( 100, x2, y2 )
gr2.SetName("roccurve_1")
gr1.Write()
gr2.Write()
f.Write()

c = TCanvas()
c.SetGridx()
c.SetGridy()
c.SetLogy()

gr1.SetLineColor(ROOT.kRed)
gr2.SetLineColor(ROOT.kGreen)

gr1.SetLineWidth(2)
gr2.SetLineWidth(2)

gr1.Draw()
gr2.Draw("SAME")
lg = ROOT.TLegend(0.1,0.7,0.9,0.9)
lg.AddEntry(gr1,'veto C','l')
lg.AddEntry(gr2,'veto UDSG','l')
lg.SetFillColorAlpha(1,0.1)
lg.SetLineColorAlpha(1,0.0)
lg.Draw("SAME")
c.SaveAs("ROC_logy.pdf")

c.SetLogy(0)
gr1.Draw()
gr2.Draw("SAME")
lg = ROOT.TLegend(0.1,0.7,0.9,0.9)
lg.AddEntry(gr1,'veto C','l')
lg.AddEntry(gr2,'veto UDSG','l')
lg.SetFillColorAlpha(1,0.1)
lg.SetLineColorAlpha(1,0.0)
lg.Draw("SAME")
c.SaveAs("ROC.pdf")

#!/usr/bin/env python
import sys
import os
import re
from array import array
import ctypes
import ROOT
from ROOT import gROOT, THStack, TString, TH1D, TObjArray, TList, TFile, TH2D, TFractionFitter, TLatex, TLegend, TCanvas, TH1
from math import fabs, sqrt

#error     = sys.argv[1]
year      = sys.argv[1]
outputdir = sys.argv[2]
fit_type  = sys.argv[3]
F_DATA    = sys.argv[4]
F_TRUE    = sys.argv[5]
F_FAKE    = sys.argv[6]

os.system("mkdir -p " + outputdir)
def cal_fraction(year, outputdir, eORb, pt_down, pt_up, fit_type, fdata, ftrue, ffake):
    sieie_cut = 0
    if eORb == "barrel":
        sieie_cut = 0.01015
    if eORb == "endcap":
        sieie_cut = 0.0272

    lumi =0
    if year == "2016":
        lumi = 35.92

    if year == "2017":
        lumi = 41.50

    if year == "2018":
        lumi = 59.74

    histname = "hist_" + eORb + "_" + str(pt_down) + "to" + str(pt_up)
    hdata = fdata.Get(histname) 
    htrue = ftrue.Get(histname)                      
    hfake = ffake.Get(histname)              
    c1 = TCanvas( histname, histname, 1000, 700)

    htrue.Scale(lumi)
    if fit_type  == 'closureTEST':
        hdata.Scale(lumi)
        hfake.Scale(lumi)

    for i in range(hdata.GetNbinsX() + 2) :
        if hdata.GetBinContent(i) < 0 :
            hdata.SetBinContent(i, 0)
        
        if htrue.GetBinContent(i) < 0 :
            htrue.SetBinContent(i, 0)
        
        if hfake.GetBinContent(i) < 0 :
            hfake.SetBinContent(i, 0);
        
    

    mc = TObjArray(2)
    mc.Add(htrue)
    mc.Add(hfake)

    fit = TFractionFitter(hdata, mc)
    fit.Constrain(1, 0.0, 1.0)
    status = fit.Fit()
    val0, err0, val1, err1 = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    n_data_total = hdata.Integral()
    fit.GetResult(0, val0, err0)
    fit.GetResult(1, val1, err1)

    # get fake rate
    nbin  = hdata.FindFixBin(sieie_cut) - 1
    nbins = hdata.GetNbinsX()
    fake_err_in_window, fake_err_total, data_err_in_window, data_err_total = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    n_hfake_in_window = hfake.IntegralAndError(1, nbin, fake_err_in_window)
    n_hfake_total     = hfake.IntegralAndError(1, nbins, fake_err_total)
    sector1           = n_hfake_in_window / n_hfake_total

    n_hdata_in_window = hdata.IntegralAndError(1, nbin, data_err_in_window)
    n_hdata_total     = hdata.IntegralAndError(1, nbins, data_err_total)
    sector2           = n_hdata_in_window / n_hdata_total
    fakerate = val1 * sector1 / sector2

    err_sector1  = sqrt((sector1)**2 * ((fake_err_in_window / n_hfake_in_window)**2 + (fake_err_total / n_hfake_total)**2))
    err_sector2  = sqrt((sector2)**2 * ((data_err_in_window / n_hdata_in_window)**2 + (data_err_total / n_hdata_total)**2))
    tmp          = val1 * sector1
    tmp_err      = sqrt((val1 * sector1)**2 * ((err_sector1 / sector1)**2 + (err1 / val1)**2))
    fakerate_err = sqrt((tmp / sector2)**2 * ((tmp_err / tmp)**2 + (err_sector2 / sector2)**2))

    result = fit.GetPlot()
    hdata.Draw("p e");
    hdata.GetYaxis().SetTitle("Events/bin")
    hdata.GetYaxis().SetTitleOffset(1.45)
    hdata.GetXaxis().SetTitle("#sigma_{i#etai#eta}")
    hdata.SetStats(0)
    hdata.SetLineColor(1)
    hdata.SetMarkerStyle(20)
    result.Draw("HIST same")
    result.SetLineColor(8)
    result.SetLineWidth(2)
    result.SetStats(0)

    htrue.SetLineColor(2)
    htrue.SetLineWidth(2)
    htrue.SetStats(0)
    htrue.DrawNormalized("HIST e same", val0 * n_data_total)
    hfake.SetLineColor(4)
    hfake.SetLineWidth(2)
    hfake.SetStats(0)
    hfake.DrawNormalized("HIST e same", val1 * n_data_total)

    maximum = 1.3 * hdata.GetMaximum()
    hdata.SetMaximum(maximum)

    leg = TLegend(0.53, 0.48, 0.88, 0.88,"brNDC");
    leg.SetFillStyle(0);
    leg.SetLineColor(0);
    leg.SetFillColor(10);
    leg.SetBorderSize(0);
    leg.SetHeader(str(pt_down) + "GeV<p_{T}^{#gamma}<"+ str(pt_up) + "GeV")#, "c");
    leg.AddEntry(hdata, "Data", "LPE");
    leg.AddEntry(result, "Template prediction", "LPE");
    leg.AddEntry(htrue, "True template from W#gamma", "LPE");
    leg.AddEntry(hfake, "Fake template from Data", "LPE");
    leg.Draw("same");

    statusStr = "fit status: " + str(int(status))
    chi2 = fit.GetChisquare()
    ndf = fit.GetNDF()
    chi2ToNDF = chi2 / ndf
    chiInt  = (100 * chi2ToNDF)
    strChi  = "#chi^{2}/ndf = " + str(round(chiInt / 100, 3)) #+ '.' + str(round(chiInt % 100,3))

    FRInt = (10000 * fakerate)
    FRErrInt = (10000 * fakerate_err)  
    strFR = "fake rate = (" + str(round(FRInt / 100,3)) + '#pm' + str(round(FRErrInt / 100,3)) + '%)'

    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.03)
    latex.SetLineWidth(1)
    latex.DrawLatex(0.75, 0.90, eORb)
    latex.DrawLatex(0.55, 0.44, statusStr)
    latex.DrawLatex(0.55, 0.38, strChi)
    latex.DrawLatex(0.55, 0.34, strFR)

    PNG_name = outputdir + '/' +str(year) + '_' +histname + '.png' 
    c1.SaveAs(PNG_name)
 
    return fakerate, fakerate_err



f_data   = TFile.Open(F_DATA)
f_true   = TFile.Open(F_TRUE)
f_fake   = TFile.Open(F_FAKE)

outCSVfile = open(outputdir + "/fraction.csv", 'w')
outfile = TFile( outputdir + '/fraction.root', 'RECREATE' )
edges  = array('d',[25, 30, 40, 50, 70, 100, 135, 400])
barrel_fraction = TH1D("barrel_fraction", "barrel_fraction", 7, edges)
barrel_fraction_error = TH1D("barrel_fraction_error", "barrel_fraction_error", 7, edges)
endcap_fraction = TH1D("endcap_fraction", "endcap_fraction", 7, edges)
endcap_fraction_error = TH1D("endcap_fraction_error", "endcap_fraction_error", 7, edges)
photon_pt_bin = [25, 30, 40, 50, 70, 100, 135, 400]

outCSVfile.write(year + ', barrel, endcap' + '\n')
for i in range(len(photon_pt_bin) -1):
    fr_b, er_b = cal_fraction(year, outputdir, "barrel", photon_pt_bin[i], photon_pt_bin[i+1], fit_type, f_data, f_true, f_fake)
    fr_e, er_e = cal_fraction(year, outputdir, "endcap", photon_pt_bin[i], photon_pt_bin[i+1], fit_type, f_data, f_true, f_fake)

    barrel_fraction.SetBinContent(barrel_fraction.FindBin((photon_pt_bin[i] + photon_pt_bin[i+1])/2.),fr_b)
    barrel_fraction_error.SetBinContent(barrel_fraction_error.FindBin((photon_pt_bin[i] + photon_pt_bin[i+1])/2.),er_b)
    endcap_fraction.SetBinContent(endcap_fraction.FindBin((photon_pt_bin[i] + photon_pt_bin[i+1])/2.),fr_e)
    endcap_fraction_error.SetBinContent(endcap_fraction_error.FindBin((photon_pt_bin[i] + photon_pt_bin[i+1])/2.),er_e)
    outCSVfile.write(str(photon_pt_bin[i]) + ' GeV < photon pt < ' + str(photon_pt_bin[i+1]) + ' GeV, ' + str(fr_b) + ' +- ' + str(er_b) + ', ' + str(fr_e) + ' +- ' + str(er_e) + '\n')
    print(fr_b, fr_e)

outfile.cd()
barrel_fraction.Write()
barrel_fraction_error.Write()
endcap_fraction.Write()
endcap_fraction_error.Write()
outfile.Close()
outCSVfile.close()

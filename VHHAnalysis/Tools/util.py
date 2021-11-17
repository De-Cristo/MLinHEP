import ROOT as R
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
import sys
import array
from ctypes import *

dict_th1    = dict()
dict_canv   = dict()
dict_leg    = dict()

canvas_list = ['VHH_HH_m', 'VHH_HH_pT', 'VHH_HH_eta', 'VHH_HH_phi', 'VHH_HH_e',\
               'VHH_H1_m', 'VHH_H1_pT', 'VHH_H1_eta', 'VHH_H1_phi', 'VHH_H1_e',\
               'VHH_H2_m', 'VHH_H2_pT', 'VHH_H2_eta', 'VHH_H2_phi', 'VHH_H2_e',\
               'VHH_HH_dR','VHH_HH_deta','VHH_HH_dphi','VHH_rHH', 'VHH_nBJets']

sample_compare_list = ['VHH_HH_m', 'VHH_HH_pT', 'VHH_HH_eta', 'VHH_HH_phi', 'VHH_HH_e',\
                       'VHH_H1_m', 'VHH_H1_pT', 'VHH_H1_eta', 'VHH_H1_phi', 'VHH_H1_e',\
                       'VHH_H2_m', 'VHH_H2_pT', 'VHH_H2_eta', 'VHH_H2_phi', 'VHH_H2_e',\
                       'VHH_HH_dR','VHH_HH_deta','VHH_HH_dphi','VHH_rHH', 'VHH_nBJets']

def th1_gev     ( name, title, xmin, xmax ):
    dict_th1[name] = R.TH1F( name, title, int((xmax-xmin)/10), xmin, xmax )
#end

def th1         ( name, title, nbin, xmin, xmax ):
    dict_th1[name] = R.TH1F( name, title, nbin, xmin, xmax )
#end

def canv        ( name, Lep_Num , lep_cha ):
    dict_canv[name] = R.TCanvas()
    dict_canv[name] . SetLogy()
    
    dict_th1[name+str(2)].SetLineColor(R.kViolet)
    dict_th1[name+str(3)].SetLineColor(R.kBlue)
    dict_th1[name+str(4)].SetLineColor(R.kRed)
    dict_th1[name + lep_cha].SetLineColor(R.kGreen)

    dict_th1[name+str(2)].SetLineWidth(2)
    dict_th1[name+str(3)].SetLineWidth(2)
    dict_th1[name+str(4)].SetLineWidth(2)
    dict_th1[name + lep_cha].SetLineWidth(2)
    
    dict_th1[name+str(2)].Sumw2()
    dict_th1[name+str(3)].Sumw2()
    dict_th1[name+str(4)].Sumw2()
    
    dict_th1[name+str(2)].DrawNormalized()
    dict_th1[name+str(3)].DrawNormalized('same')
    dict_th1[name + lep_cha].DrawNormalized('same')
    dict_th1[name+str(4)].DrawNormalized('same')
    
    dict_leg[name] = R.TLegend(0.75,0.85,0.95,0.95)
    dict_leg[name].AddEntry(dict_th1[name+'2'],'Bjets tagged 2')
    dict_leg[name].AddEntry(dict_th1[name+'3'],'Bjets tagged 3')
    dict_leg[name].AddEntry(dict_th1[name+'4'],'Bjets tagged 4')
    dict_leg[name].AddEntry(dict_th1[name + lep_cha], lep_cha + ' MC Signal')

    dict_leg[name].Draw('same')
    
    dict_canv[name].SaveAs(name+ Lep_Num +'.pdf')
#end

def canv_sample_compare        ( name, lep_cha_1 , lep_cha_2 ):
    dict_canv[name] = R.TCanvas()
    dict_canv[name] . SetLogy()

    dict_th1[name + lep_cha_1].SetLineColor(R.kBlue)
    dict_th1[name + lep_cha_2].SetLineColor(R.kRed)

    dict_th1[name + lep_cha_1].SetLineWidth(2)
    dict_th1[name + lep_cha_2].SetLineWidth(2)

    dict_th1[name + lep_cha_1].DrawNormalized()
    dict_th1[name + lep_cha_2].DrawNormalized('same')
    
    dict_leg[name] = R.TLegend(0.75,0.85,0.95,0.95)
    dict_leg[name].AddEntry(dict_th1[name + lep_cha_1], lep_cha_1 + ' MC Signal')
    dict_leg[name].AddEntry(dict_th1[name + lep_cha_2], lep_cha_2 + ' MC Signal')
    dict_leg[name].Draw('same')
    
    dict_canv[name].SaveAs(name + lep_cha_1 + 'VS' + lep_cha_2 +'.pdf')
#end

th1    ('VHH_nBJets1',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJets2',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJets3',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJets4',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJetsZll',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJetsZnn',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJetsZll_LooseBWP',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJetsZnn_LooseBWP',           'number of b-jets',         5,      0,      5)
th1    ('VHH_nBJetsWln',           'number of b-jets',         5,      0,      5)

th1    ('VHH_HH_m2',             'M(jjjj) [GeV]',            60,    0,      2000)
th1    ('VHH_HH_m3',             'M(jjjj) [GeV]',            60,    0,      2000)
th1    ('VHH_HH_m4',             'M(jjjj) [GeV]',            60,    0,      2000)
th1    ('VHH_HH_mZll',             'M(jjjj) [GeV]',            60,    0,      2000)
th1    ('VHH_HH_mZnn',             'M(jjjj) [GeV]',            60,    0,      2000)
th1    ('VHH_HH_mWln',             'M(jjjj) [GeV]',            60,    0,      2000)

th1    ('VHH_HH_pT2',            'p_{T}(jjjj) [GeV]',        50,    0,      1000)
th1    ('VHH_HH_pT3',            'p_{T}(jjjj) [GeV]',        50,    0,      1000)
th1    ('VHH_HH_pT4',            'p_{T}(jjjj) [GeV]',        50,    0,      1000)
th1    ('VHH_HH_pTZll',            'p_{T}(jjjj) [GeV]',        50,    0,      1000)
th1    ('VHH_HH_pTZnn',            'p_{T}(jjjj) [GeV]',        50,    0,      1000)
th1    ('VHH_HH_pTWln',            'p_{T}(jjjj) [GeV]',        50,    0,      1000)

th1    ('VHH_HH_eta2',           '#eta(HH)',                 90,    -4.5,    4.5)
th1    ('VHH_HH_eta3',           '#eta(HH)',                 90,    -4.5,    4.5)
th1    ('VHH_HH_eta4',           '#eta(HH)',                 90,    -4.5,    4.5)
th1    ('VHH_HH_etaZll',           '#eta(HH)',                 90,    -4.5,    4.5)
th1    ('VHH_HH_etaZnn',           '#eta(HH)',                 90,    -4.5,    4.5)
th1    ('VHH_HH_etaWln',           '#eta(HH)',                 90,    -4.5,    4.5)

th1    ('VHH_HH_phi2',           '#phi(HH)',                 64,    -3.2,   3.2)
th1    ('VHH_HH_phi3',           '#phi(HH)',                 64,    -3.2,   3.2)
th1    ('VHH_HH_phi4',           '#phi(HH)',                 64,    -3.2,   3.2)
th1    ('VHH_HH_phiZll',           '#phi(HH)',                 64,    -3.2,   3.2)
th1    ('VHH_HH_phiZnn',           '#phi(HH)',                 64,    -3.2,   3.2)
th1    ('VHH_HH_phiWln',           '#phi(HH)',                 64,    -3.2,   3.2)

th1    ('VHH_HH_e2',             'E(jjjj) [GeV]',            50,    0,      3500)
th1    ('VHH_HH_e3',             'E(jjjj) [GeV]',            50,    0,      3500)
th1    ('VHH_HH_e4',             'E(jjjj) [GeV]',            50,    0,      3500)
th1    ('VHH_HH_eZll',             'E(jjjj) [GeV]',            50,    0,      3500)
th1    ('VHH_HH_eZnn',             'E(jjjj) [GeV]',            50,    0,      3500)
th1    ('VHH_HH_eWln',             'E(jjjj) [GeV]',            50,    0,      3500)

th1    ('VHH_H1_m2',             'M1(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H1_m3',             'M1(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H1_m4',             'M1(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H1_mZll',             'M1(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H1_mZnn',             'M1(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H1_mWln',             'M1(jj) [GeV]',             150,    0,      1500)

th1    ('VHH_H1_pT2',            'p_{T}1(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H1_pT3',            'p_{T}1(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H1_pT4',            'p_{T}1(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H1_pTZll',            'p_{T}1(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H1_pTZnn',            'p_{T}1(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H1_pTWln',            'p_{T}1(jj) [GeV]',         100,    0,      1000)

th1    ('VHH_H1_eta2',           '#eta(H1)',                 90,    -4.5,     4.5)
th1    ('VHH_H1_eta3',           '#eta(H1)',                 90,    -4.5,     4.5)
th1    ('VHH_H1_eta4',           '#eta(H1)',                 90,    -4.5,     4.5)
th1    ('VHH_H1_etaZll',           '#eta(H1)',                 90,    -4.5,     4.5)
th1    ('VHH_H1_etaZnn',           '#eta(H1)',                 90,    -4.5,     4.5)
th1    ('VHH_H1_etaWln',           '#eta(H1)',                 90,    -4.5,     4.5)

th1    ('VHH_H1_phi2',           '#phi(H1)',                 64,    -3.2,     3.2)
th1    ('VHH_H1_phi3',           '#phi(H1)',                 64,    -3.2,     3.2)
th1    ('VHH_H1_phi4',           '#phi(H1)',                 64,    -3.2,     3.2)
th1    ('VHH_H1_phiZll',           '#phi(H1)',                 64,    -3.2,     3.2)
th1    ('VHH_H1_phiZnn',           '#phi(H1)',                 64,    -3.2,     3.2)
th1    ('VHH_H1_phiWln',           '#phi(H1)',                 64,    -3.2,     3.2)

th1    ('VHH_H1_e2',             'E1(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H1_e3',             'E1(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H1_e4',             'E1(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H1_eZll',             'E1(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H1_eZnn',             'E1(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H1_eWln',             'E1(jj) [GeV]',             175,    0,       3500)

th1    ('VHH_H2_m2',             'M2(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H2_m3',             'M2(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H2_m4',             'M2(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H2_mZll',             'M2(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H2_mZnn',             'M2(jj) [GeV]',             150,    0,      1500)
th1    ('VHH_H2_mWln',             'M2(jj) [GeV]',             150,    0,      1500)

th1    ('VHH_H2_pT2',            'p_{T}2(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H2_pT3',            'p_{T}2(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H2_pT4',            'p_{T}2(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H2_pTZll',            'p_{T}2(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H2_pTZnn',            'p_{T}2(jj) [GeV]',         100,    0,      1000)
th1    ('VHH_H2_pTWln',            'p_{T}2(jj) [GeV]',         100,    0,      1000)

th1    ('VHH_H2_eta2',           '#eta(H2)',                 90,    -4.5,     4.5)
th1    ('VHH_H2_eta3',           '#eta(H2)',                 90,    -4.5,     4.5)
th1    ('VHH_H2_eta4',           '#eta(H2)',                 90,    -4.5,     4.5)
th1    ('VHH_H2_etaZll',           '#eta(H2)',                 90,    -4.5,     4.5)
th1    ('VHH_H2_etaZnn',           '#eta(H2)',                 90,    -4.5,     4.5)
th1    ('VHH_H2_etaWln',           '#eta(H2)',                 90,    -4.5,     4.5)

th1    ('VHH_H2_phi2',           '#phi(H2)',                 64,    -3.2,     3.2)
th1    ('VHH_H2_phi3',           '#phi(H2)',                 64,    -3.2,     3.2)
th1    ('VHH_H2_phi4',           '#phi(H2)',                 64,    -3.2,     3.2)
th1    ('VHH_H2_phiZll',           '#phi(H2)',                 64,    -3.2,     3.2)
th1    ('VHH_H2_phiZnn',           '#phi(H2)',                 64,    -3.2,     3.2)
th1    ('VHH_H2_phiWln',           '#phi(H2)',                 64,    -3.2,     3.2)

th1    ('VHH_H2_e2',             'E2(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H2_e3',             'E2(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H2_e4',             'E2(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H2_eZll',             'E2(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H2_eZnn',             'E2(jj) [GeV]',             175,    0,       3500)
th1    ('VHH_H2_eWln',             'E2(jj) [GeV]',             175,    0,       3500)

th1    ('VHH_HH_dphi2',          '#Delta#phi(H1, H2)',       32,     0,      3.2)
th1    ('VHH_HH_dphi3',          '#Delta#phi(H1, H2)',       32,     0,      3.2)
th1    ('VHH_HH_dphi4',          '#Delta#phi(H1, H2)',       32,     0,      3.2)
th1    ('VHH_HH_dphiZll',          '#Delta#phi(H1, H2)',       32,     0,      3.2)
th1    ('VHH_HH_dphiZnn',          '#Delta#phi(H1, H2)',       32,     0,      3.2)
th1    ('VHH_HH_dphiWln',          '#Delta#phi(H1, H2)',       32,     0,      3.2)

th1    ('VHH_HH_deta2',          '#Delta#eta(H1, H2)',       45,     0,      4.5)
th1    ('VHH_HH_deta3',          '#Delta#eta(H1, H2)',       45,     0,      4.5)
th1    ('VHH_HH_deta4',          '#Delta#eta(H1, H2)',       45,     0,      4.5)
th1    ('VHH_HH_detaZll',          '#Delta#eta(H1, H2)',       45,     0,      4.5)
th1    ('VHH_HH_detaZnn',          '#Delta#eta(H1, H2)',       45,     0,      4.5)
th1    ('VHH_HH_detaWln',          '#Delta#eta(H1, H2)',       45,     0,      4.5)

th1    ('VHH_HH_dR2',            '#Delta#R(H1, H2)',         65,     0,      6.5)
th1    ('VHH_HH_dR3',            '#Delta#R(H1, H2)',         65,     0,      6.5)
th1    ('VHH_HH_dR4',            '#Delta#R(H1, H2)',         65,     0,      6.5)
th1    ('VHH_HH_dRZll',            '#Delta#R(H1, H2)',         65,     0,      6.5)
th1    ('VHH_HH_dRZnn',            '#Delta#R(H1, H2)',         65,     0,      6.5)
th1    ('VHH_HH_dRWln',            '#Delta#R(H1, H2)',         65,     0,      6.5)

th1    ('VHH_rHH2',              '#DeltaM(jjjj) [GeV]',      50,     0,      500)
th1    ('VHH_rHH3',              '#DeltaM(jjjj) [GeV]',      50,     0,      500)
th1    ('VHH_rHH4',              '#DeltaM(jjjj) [GeV]',      50,     0,      500)
th1    ('VHH_rHHZll',              '#DeltaM(jjjj) [GeV]',      50,     0,      500)
th1    ('VHH_rHHZnn',              '#DeltaM(jjjj) [GeV]',      50,     0,      500)
th1    ('VHH_rHHWln',              '#DeltaM(jjjj) [GeV]',      50,     0,      500)

def convert_coupling_diagramweight(coupling_nx3):
    # coupling_nx3 is (cv, c2v, kl)
    nrow=len(coupling_nx3[:,0])
    cv = coupling_nx3[:,0].reshape(nrow,1)
    c2v = coupling_nx3[:,1].reshape(nrow,1)
    kl = coupling_nx3[:,2].reshape(nrow,1)
    weights = np.matrix(np.zeros(nrow*6).reshape((nrow,6)),dtype=np.float64)
    weights[:,0] = np.power(np.multiply(cv,kl),2)
    weights[:,1] = np.power(cv,4)
    weights[:,2] = np.power(c2v,2)
    weights[:,3] = np.multiply(np.power(cv,3),kl)
    weights[:,4] = np.multiply(np.multiply(cv,c2v),kl)
    weights[:,5] = np.multiply(np.power(cv,2),c2v)
    return weights



def convert_coupling_diagramweight_cv1(coupling_nx3):
    # coupling_nx3 is (cv, c2v, kl)
    nrow=len(coupling_nx3[:,0])
    cv = 1
    c2v = coupling_nx3[:,0].reshape(nrow,1)
    kl = coupling_nx3[:,1].reshape(nrow,1)
    weights = np.matrix(np.zeros(nrow*6).reshape((nrow,6)),dtype=np.float64)
    weights[:,0] = np.power(np.multiply(cv,kl),2)
    weights[:,1] = np.power(cv,4)
    weights[:,2] = np.power(c2v,2)
    weights[:,3] = np.multiply(np.power(cv,3),kl)
    weights[:,4] = np.multiply(np.multiply(cv,c2v),kl)
    weights[:,5] = np.multiply(np.power(cv,2),c2v)
    return weights
    
def convert_coupling_diagramweight_c2v1(coupling_nx3):
    # coupling_nx3 is (cv, c2v, kl)
    nrow=len(coupling_nx3[:,0])
    cv = coupling_nx3[:,0].reshape(nrow,1)
    c2v = 1 #coupling_nx3[:,0].reshape(nrow,1)
    kl = coupling_nx3[:,1].reshape(nrow,1)
    weights = np.matrix(np.zeros(nrow*6).reshape((nrow,6)),dtype=np.float64)
    weights[:,0] = np.power(np.multiply(cv,kl),2)
    weights[:,1] = np.power(cv,4)
    weights[:,2] = np.power(c2v,2)
    weights[:,3] = np.multiply(np.power(cv,3),kl)
    weights[:,4] = np.multiply(np.multiply(cv,c2v),kl)
    weights[:,5] = np.multiply(np.power(cv,2),c2v)
    return weights
    
def convert_coupling_diagramweight_kl1(coupling_nx3):
    # coupling_nx3 is (cv, c2v, kl)
    nrow=len(coupling_nx3[:,0])
    cv = coupling_nx3[:,0].reshape(nrow,1)
    c2v = coupling_nx3[:,1].reshape(nrow,1)
    kl = 1
    weights = np.matrix(np.zeros(nrow*6).reshape((nrow,6)),dtype=np.float64)
    weights[:,0] = np.power(np.multiply(cv,kl),2)
    weights[:,1] = np.power(cv,4)
    weights[:,2] = np.power(c2v,2)
    weights[:,3] = np.multiply(np.power(cv,3),kl)
    weights[:,4] = np.multiply(np.multiply(cv,c2v),kl)
    weights[:,5] = np.multiply(np.power(cv,2),c2v)
    return weights

def convert_coupling_diagramweight_cv1_kl1(coupling_nx3):
    # coupling_nx3 is (cv, c2v, kl)
    nrow=len(coupling_nx3[:,0])
    cv = 1
    c2v = coupling_nx3[:,0].reshape(nrow,1)
    kl = 1
    weights = np.matrix(np.zeros(nrow*6).reshape((nrow,6)),dtype=np.float64)
    weights[:,0] = np.power(np.multiply(cv,kl),2)
    weights[:,1] = np.power(cv,4)
    weights[:,2] = np.power(c2v,2)
    weights[:,3] = np.multiply(np.power(cv,3),kl)
    weights[:,4] = np.multiply(np.multiply(cv,c2v),kl)
    weights[:,5] = np.multiply(np.power(cv,2),c2v)
    return weights

def convert_coupling_diagramweight_cv1_c2v1(coupling_nx3):
    # coupling_nx3 is (cv, c2v, kl)
    nrow=len(coupling_nx3[:,0])
    cv = 1
    c2v = 1
    kl = coupling_nx3[:,0].reshape(nrow,1)
    weights = np.matrix(np.zeros(nrow*6).reshape((nrow,6)),dtype=np.float64)
    weights[:,0] = np.power(np.multiply(cv,kl),2)
    weights[:,1] = np.power(cv,4)
    weights[:,2] = np.power(c2v,2)
    weights[:,3] = np.multiply(np.power(cv,3),kl)
    weights[:,4] = np.multiply(np.multiply(cv,c2v),kl)
    weights[:,5] = np.multiply(np.power(cv,2),c2v)
    return weights

def Save_Temp_Components(tree_in, bak_file, weight):
    print("weighting the trees..." + str(weight))
    tree_in.SetBranchStatus('*', 1);
    tout1 = tree_in.CloneTree()
    tout1.SetWeight(weight)
    tout1.Write()
    del tout1
#END

def NormHisto(histo_name, norm):
    scale = 1/histo_name.Integral()
    histo_name.Scale(scale)

def DF_HISTO1D(_rdf, _jet_filter, _other_filters, _name, _describe, _nbins, _xmin, _xmax, _branch_name, _Xtitle, _Batch):
    
    _histo_name = _rdf.Filter(_jet_filter+' && '+_other_filters).Histo1D((_name, _describe, _nbins, _xmin, _xmax), _branch_name)
    
    _histo_with2bjets = _rdf.Filter('VHH_nBJets == 2 && '+ _other_filters).Histo1D((_name+'2b', _describe+'2b', _nbins, _xmin, _xmax), _branch_name)
    
    _histo_weight = R.TH1D(_name+'_weight', _describe+'_weight', _nbins, _xmin, _xmax)
    
    inclusiveBinningP = np.array([0, 200, 350, 1000],dtype = float) #FIXME
    _nbins = len(inclusiveBinningP)
    
    _histo_name = _histo_name.Rebin(_nbins,_name,inclusiveBinningP)
    _histo_with2bjets = _histo_with2bjets.Rebin(_nbins, _name, inclusiveBinningP)
    _histo_weight = _histo_weight.Rebin(_nbins, _name+'_weight', inclusiveBinningP)

    NormHisto(_histo_name,1)
    NormHisto(_histo_with2bjets,1)
    
    for i in range(0, _nbins):
        if _histo_name.GetBinContent(i)!= 0:
            _histo_weight.SetBinContent(i,_histo_with2bjets.GetBinContent(i)/float(_histo_name.GetBinContent(i)))
        else:
            _histo_weight.SetBinContent(i,0)
    if _Batch :
        _canvas_histo_name = R.TCanvas()
    #     R.gstyle.SetLogy()
    #     R.gStyle.SetOptStat(0000)

        upper_pad = R.TPad("upper_pad", "", 0, 0.35, 1, 1)
        lower_pad = R.TPad("lower_pad", "", 0, 0, 1, 0.35)
        for p in [upper_pad, lower_pad]:
            p.SetLeftMargin(0.14)
            p.SetRightMargin(0.05)
            p.SetTickx(False)
            p.SetTicky(False)
        upper_pad.SetBottomMargin(0)
        lower_pad.SetTopMargin(0)
        lower_pad.SetBottomMargin(0.3)

        upper_pad.Draw()
        lower_pad.Draw()
        upper_pad.cd()
    #     dict_th1[_histo_name].SetStats(0)
    #     dict_th1[_histo_name+'_2b'].SetStats(0)

        _histo_with2bjets.GetXaxis().SetTitle(_Xtitle)
        _histo_with2bjets.GetYaxis().SetTitle('Yields')

        _histo_name.SetMarkerStyle(20)
        _histo_name.SetMarkerSize(1)

        _histo_with2bjets.SetFillColor(R.kBlue-5)
        _histo_with2bjets.SetLineColor(R.kBlue-5)

        _histo_with2bjets.Draw()
        _histo_name.Draw('SAME')
        lower_pad.cd()
        _histo_weight.SetStats(0)
        _histo_weight.Draw()

    #     dict_legend[_histo_name] = R.TLegend(0.7,0.8,0.9,0.9)
    #     dict_legend[_histo_name].AddEntry(dict_th1[_histo_name])
    #     dict_legend[_histo_name].AddEntry(dict_th1[_histo_name+'_2b'], "bkg")
    #     dict_legend[_histo_name].Draw('SAME')

        _canvas_histo_name.SaveAs(str(_histo_name)+'.pdf')
    else:
        print('No Figures can be saved in batch mode.')
    
    return _histo_weight
#END
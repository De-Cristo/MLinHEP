import sys
import os
import math
import argparse
import ROOT as R
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--inputDirectory",          dest="ind",   default="test_0908_catfirst_bdt_30bins/",   help="input directory" )
parser.add_argument("-o", "--output",          dest="out",   default="",   help="output name" )
args = parser.parse_args()

if args.ind != 0:
    path = str(args.ind)+'/'

import os
data_outDir = args.out
if data_outDir is not '' :
    if not os.path.isdir( data_outDir ) :
        os.makedirs( data_outDir )

syst = {}
addtional = ''

procs = ["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","TT_FailReweight","TTB_FailReweight","data_obs", 'VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb']

data_obs = {}#"data_obs"}

signal_procs = ["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb",'VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb']

plots_proce = ["TT_FailReweight","TTB_FailReweight","VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb"]
plots_proce = ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb"]
#bkg_procs = {"TT_FailReweight","TTB_FailReweight"}

VHHfiles = [i for i in os.listdir(path) if i.endswith(".root")]


procs = ["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","TT","TTB","data_obs", 'VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb','s_Top','ttH','TTV']
plots_proce = ["TT","TTB","VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb",'s_Top']
bkg_procs = {"TT","TTB"}

year='2018'
syst_un=[  "CMS_pileup_"+year,
           "CMS_btag_HF_2016_2017_2018","CMS_btag_LF_2016_2017_2018","CMS_btag_cferr1_2016_2017_2018","CMS_btag_cferr2_2016_2017_2018","CMS_btag_hfstats1_"+year,"CMS_btag_hfstats2_"+year,"CMS_btag_lfstats1_"+year,"CMS_btag_lfstats2_"+year,"CMS_btag_jes_"+year,
           "CMS_PNet_"+year,
           "CMS_eff_m_"+year, #'CMS_eff_MET_'+year,
           'CMS_BRewError1_'+year,'CMS_BRewError2_'+year,

           "CMS_res_j_"+year,"CMS_scale_j_Abs","CMS_scale_j_Abs_"+year,"CMS_scale_j_BBEC1",
           "CMS_scale_j_BBEC1_"+year,"CMS_scale_j_EC2","CMS_scale_j_EC2_"+year,"CMS_scale_j_FlavQCD",
           "CMS_scale_j_HF","CMS_scale_j_HF_"+year,"CMS_scale_j_RelBal","CMS_scale_j_RelSample_"+year,"CMS_MSD_JMS_"+year,"CMS_MSD_JMR_"+year,"CMS_unclusteredEnergy_"+year
        ]

procs_addunc = []
for isys in procs:
    #print(isys)
    procs_addunc.append(isys)
    if isys == 'data_obs': continue
    for isys2 in syst_un:
        #print(isys2)
        if ('TT'!=isys and 'TTB' !=isys) and 'BRewError' in isys2: continue
        procs_addunc.append(isys+'_'+isys2+'Up')
        procs_addunc.append(isys+'_'+isys2+'Down')
print(procs_addunc)

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


listOfCouplings0 = np.array([[0.5,1,1],[1,0,1], [1,1,0],[1,1,1],[1,1,2],[1,2,1],[1.5,1,1]])
CrossSec0 = np.array([0.0001715,9.42E-05,0.0001588,0.0002701,0.0004333,0.0006957,0.0005908])


listOfNewCouplings = np.array([[1,1,20]])
Coupling0 = convert_coupling_diagramweight(listOfCouplings0)
CouplingInv0=np.linalg.pinv(Coupling0)
print('pinv', CouplingInv0)
NewCoupling = convert_coupling_diagramweight(listOfNewCouplings)
composition = np.matmul(NewCoupling, CouplingInv0)
print('composition ',composition)
#
matrix_ele = np.matmul(CouplingInv0, CrossSec0)
newXsec = np.matmul(NewCoupling,matrix_ele.reshape(6,1))
print("---------------------------- print new Xsec:")
print(newXsec)
#

colorb = [R.kRed,R.kBlue,R.kGreen,R.kBlack,R.kCyan,R.kOrange,R.kViolet,R.kGray,R.kPink]

def getcomposition(listOfCouplings0, listOfNewCouplings):
    Coupling0 = convert_coupling_diagramweight(listOfCouplings0)
    CouplingInv0=np.linalg.pinv(Coupling0)
    NewCoupling = convert_coupling_diagramweight(listOfNewCouplings)
    composition = np.matmul(NewCoupling, CouplingInv0)
    return composition

def plot_datacardswithdifferentcombination(rebin=False,plt_svb=False,drawStack=True):
    #all
    #listOfCouplings0 = np.array([[0.5,1,1],[1,0,1],[1,1,1],[1,1,2],[1,2,1],[1.5,1,1],[1,1,0],[1,1,20]])
    signalorder=["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb",'VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb']
    componame=['comb1', 'comb2', '7samples','8samples']#,'No_cv1.5_SM','No_cv1.5','No_cv0.5']
    #comb1
    #listOfCouplings0 = np.array([[0.5,1,1],[1,0,1],[1,1,0], [1,1,1],[1,1,2],[1,2,1],[1.5,1,1],[1,1,20]])
    listOfNewCouplings = np.array([[1,1,20]])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['comb1'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],0,0 ] , ]
    ##comb2
    #listOfCouplings0 = np.array([[0.5,1,1],[1,0,1],[1,1,1],[1,1,2],[1.5,1,1], [1,1,0] ])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['comb2'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],0,composition[0,4],composition[0,5],0 ] ,
    #                   #[composition[1,0],composition[1,1], composition[1,2],composition[1,3],0,composition[1,5],composition[1,4],0 ]
    #                 ]
    ##7samples
    #listOfCouplings0 = np.array([[0.5,1,1],[1,0,1],[1,1,1],[1,1,2],[1,2,1],[1.5,1,1],[1,1,0]])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['7samples'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],0 ] ,
    #                   #[composition[1,0],composition[1,1], composition[1,2],composition[1,3],composition[1,4],composition[1,5],composition[1,6],0 ]
    #                 ]
    #8samples
    compo={}
    componame=['Signal C_{V},C_{2V}=1,k_{#lambda}=20', 'Signal C_{V},C_{2V}=1,k_{#lambda}=50','Signal C_{V},k_{#lambda}=1,C_{2V}=20']#'8samples','No_cv1.5_SM','No_cv1.5']
    componame=['Signal C_{V},C_{2V}=1,k_{#lambda}=-20','Signal C_{V},C_{2V}=1,k_{#lambda}=-10','Signal C_{V},C_{2V}=1,k_{#lambda}=-5','Signal C_{V},C_{2V}=1,k_{#lambda}=5','Signal C_{V},C_{2V}=1,k_{#lambda}=10','Signal C_{V},C_{2V}=1,k_{#lambda}=20']
    componame=['Signal C_{V},C_{2V}=1,k_{#lambda}=20']
    listOfCouplings0 = np.array([[0.5,1,1],[1,0,1],[1,1,1],[1,1,2],[1,2,1],[1.5,1,1],[1,1,0],[1,1,20]])
#    listOfNewCouplings = np.array([[1,1,20]])
#    composition=getcomposition(listOfCouplings0, listOfNewCouplings)
#    compo['Signal C_{V},C_{2V}=1,k_{#lambda}=20'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]
#    listOfNewCouplings = np.array([[1,1,50]])
#    composition=getcomposition(listOfCouplings0, listOfNewCouplings)
#    compo['Signal C_{V},C_{2V}=1,k_{#lambda}=50'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]
#    listOfNewCouplings = np.array([[1,20,1]])
#    composition=getcomposition(listOfCouplings0, listOfNewCouplings)
#    compo['Signal C_{V},k_{#lambda}=1,C_{2V}=20'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]


    #listOfNewCouplings = np.array([[1,1,-20]])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['Signal C_{V},C_{2V}=1,k_{#lambda}=-20'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]
    #listOfNewCouplings = np.array([[1,1,-10]])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['Signal C_{V},C_{2V}=1,k_{#lambda}=-10'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]
    #listOfNewCouplings = np.array([[1,1,-5]])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['Signal C_{V},C_{2V}=1,k_{#lambda}=-5'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]
    #listOfNewCouplings = np.array([[1,1,5]])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['Signal C_{V},C_{2V}=1,k_{#lambda}=5'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]
    #listOfNewCouplings = np.array([[1,1,10]])
    #composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    #compo['Signal C_{V},C_{2V}=1,k_{#lambda}=10'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]
    listOfNewCouplings = np.array([[1,1,20]])
    composition=getcomposition(listOfCouplings0, listOfNewCouplings)
    compo['Signal C_{V},C_{2V}=1,k_{#lambda}=20'] = [ [composition[0,0], composition[0,1], composition[0,2],composition[0,3],composition[0,4],composition[0,5],composition[0,6],composition[0,7] ] ]

    for ifile in VHHfiles:
        #first load all histgrams
        procs=['TT','TTB',"VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","data_obs", 'VHH_CV_1_C2V_1_kl_0_hbbhbb',"VHH_CV_1_C2V_1_kl_20_hbbhbb","s_Top"]
        #procs=["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","TT_FailReweight","TTB_FailReweight","data_obs", 'VHH_CV_1_C2V_1_kl_0_hbbhbb',"VHH_CV_1_C2V_1_kl_20_hbbhbb"]
        signal_procs=["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb"]
        plots_proce=[]#"TT_FailReweight","TTB_FailReweight"]
        plots_proce=["data_obs","TT","TTB"]
        plots_proce=["TT","TTB","s_Top"]
        hsample = {}
        hsvb = {}
        fin = R.TFile.Open('{0}'.format(path+ifile),'READ')
        #Get all plots
        MAX_ = 0
        Min_ = 1
        MaxX_ = 0
        MinX_ = 0
        NX_ = 0
        for iprocs in procs:
            fin.cd()
            if rebin:
                print(iprocs)
                htemplte = fin.Get(iprocs).Clone()
                NX_=htemplte.GetNbinsX()
                hsample[iprocs] = R.TH1F(iprocs,iprocs,NX_,1,1+NX_)
                for i in range(1,NX_+1):
                    hsample[iprocs].SetBinContent(i,htemplte.GetBinContent(i))
                    hsample[iprocs].SetBinError(i,htemplte.GetBinError(i))
                MinX_=hsample[iprocs].GetBinCenter(1) - hsample[iprocs].GetBinWidth(1)/2.0
                MaxX_=hsample[iprocs].GetBinCenter(NX_) + hsample[iprocs].GetBinWidth(NX_)/2.0
                MAX_ = hsample[iprocs].GetMaximum() if hsample[iprocs].GetMaximum() > MAX_ else MAX_

                if ('TT' in iprocs and 'TTV' not in iprocs): Min_ = hsample[iprocs].GetMinimum() if (hsample[iprocs].GetMinimum()>0 and hsample[iprocs].GetMinimum() < Min_) else Min_
                #if iprocs in signal_procs:
                #    MAX_ = hsample[iprocs].GetMaximum() if hsample[iprocs].GetMaximum() > MAX_ else MAX_
            else:
                hsample[iprocs] = fin.Get(iprocs).Clone()
                NX_=hsample[iprocs].GetNbinsX()
                MinX_=hsample[iprocs].GetBinCenter(1) - hsample[iprocs].GetBinWidth(1)/2.0
                MaxX_=hsample[iprocs].GetBinCenter(NX_) + hsample[iprocs].GetBinWidth(NX_)/2.0
                MAX_ = hsample[iprocs].GetMaximum() if hsample[iprocs].GetMaximum() > MAX_ else MAX_
                Min_ = hsample[iprocs].GetMinimum() if (hsample[iprocs].GetMinimum()>0 and hsample[iprocs].GetMinimum() < Min_) else Min_
            #if iprocs in signal_procs:
            #    MAX_ = hsample[iprocs].GetMaximum()*100000 if hsample[iprocs].GetMaximum()*100000 > MAX_ else MAX_
        if plt_svb:
            #hbkg=0
            #for ibkg in ['TT','TTB']:
            #    if hbkg==0:
            #        hbkg=hsample[ibkg].Clone()
            #    else:
            #        hbkg.Add(hsample[ibkg])
            for compon in componame:
                print(compon)
                print(compo[compon][0])
                hsample[compon] = R.TH1F(compon,compon,NX_,MinX_,MaxX_)
                for isignal in range(8):
                    if compo[compon][0][isignal]!=0:
                        hsample[compon].Add(hsample[signalorder[isignal]],compo[compon][0][isignal])
                #print(hsample[compon].Integral())
                #hsample[compon].Divide(hsample['VHH_CV_1_C2V_1_kl_20_hbbhbb'])
                #print(hsample[compon].Integral())
                #exit()
                MAX_ = hsample[compon].GetMaximum() if hsample[compon].GetMaximum() > MAX_ else MAX_
                #Min_ = hsample[iprocs].GetMinimum() if (hsample[iprocs].GetMinimum()>0 and hsample[iprocs].GetMinimum() < Min_) else Min_
                print(hsample[compon].Integral())
                signal_procs.append(compon)
                plots_proce.append(compon)
                procs.append(compon)
        #make plots
        c=R.TCanvas()
        c.SetFillColor(0)
        c.SetBorderMode(0)
        c.SetBorderSize(2)
        c.SetFrameBorderMode(0)
        frame_4fa51a0__1 = R.TH1D("frame_4fa51a0__1","",NX_,MinX_,MaxX_)
        frame_4fa51a0__1.GetXaxis().SetTitle("transformed BDT variable");
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(0.8);
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetTitle("");
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetRangeUser(Min_*0.1,MAX_*20)
        frame_4fa51a0__1.Draw("AXISSAME");
        R.gStyle.SetOptStat(0)
        c.SetLogy()
        leg = R.TLegend(0.45,0.6,0.85,0.85);
        leg.SetBorderSize(0);
        leg.SetLineStyle(1);
        leg.SetLineWidth(1);
        i=0
        if '_FailReweight' in iprocs:
            hsample[iprocs].SetName(iprocs.replace('_FailReweight',''))
            hsample[iprocs].SetTitle(iprocs.replace('_FailReweight',''))
        if drawStack:
            hs = R.THStack("hs","");
            for iprocs in ['TT','TTB']:
                hsample[iprocs].SetLineColor(colorb[i])
                hsample[iprocs].SetMarkerStyle(8)
                hsample[iprocs].SetMarkerColor(colorb[i])
                hsample[iprocs].SetFillColor(colorb[i])
                if iprocs=='TT': hsample[iprocs].Scale(scalelist[ifile][1])
                else: hsample[iprocs].Scale(scalelist[ifile][0])
                hs.Add(hsample[iprocs])
                #hsample[iprocs].Draw("same p")
                entry=leg.AddEntry(iprocs,iprocs.replace('_hbbhbb','') if '_hbbhbb' in iprocs else iprocs ,"l");
                entry.SetFillStyle(1001);
                entry.SetMarkerStyle(8);
                entry.SetMarkerSize(1.5);
                entry.SetLineStyle(1);
                entry.SetLineWidth(3);
                entry.SetLineColor(colorb[i]);
                entry.SetTextFont(42);
                entry.SetTextSize(0.04);
                i+=1
            iprocs='data_obs'
            hsample[iprocs].SetLineColor(colorb[i])
            hsample[iprocs].SetFillColor(colorb[i])
            hsample[iprocs].SetMarkerStyle(8)
            hsample[iprocs].SetMarkerColor(colorb[i])
            entry=leg.AddEntry(iprocs,iprocs.replace('_hbbhbb','') if '_hbbhbb' in iprocs else iprocs ,"l");
            entry.SetFillStyle(1001);
            entry.SetMarkerStyle(8);
            entry.SetMarkerSize(1.5);
            entry.SetLineStyle(1);
            entry.SetLineWidth(3);
            entry.SetLineColor(colorb[i]);
            entry.SetTextFont(42);
            entry.SetTextSize(0.04);
            hs.Draw("same HIST")
            hsample[iprocs].Draw("same p")
        else:
            for iprocs in plots_proce:
                #hsample[iprocs].SetName('h'+str(i))
                hsample[iprocs].SetLineColor(colorb[i])
                hsample[iprocs].SetMarkerStyle(8)
                hsample[iprocs].SetMarkerColor(colorb[i])
                hsample[iprocs].Draw("same p")
                entry=leg.AddEntry(iprocs,iprocs.replace('_hbbhbb','') if '_hbbhbb' in iprocs else iprocs ,"lp");
                entry.SetFillStyle(1001);
                entry.SetMarkerStyle(8);
                entry.SetMarkerSize(1.5);
                entry.SetLineStyle(1);
                entry.SetLineWidth(3);
                entry.SetTextFont(42);
                entry.SetTextSize(0.04);
                i+=1
        #calculate sVb
        print(plots_proce)
#['TT', 'TTB', 'Signal C_{V},C_{2V}=1,k_{#lambda}=20', 'Signal C_{V},C_{2V}=1,k_{#lambda}=50', 'Signal C_{V},k_{#lambda}=1,C_{2V}=20']
        #print('Integral: TT ', hsample['TT'].Integral(), ' TTB ', hsample['TTB'].Integral(), ' Signal C_{V},C_{2V}=1,k_{#lambda}=50 ', hsample['Signal C_{V},C_{2V}=1,k_{#lambda}=50'].Integral() )
        svbvalue1=0
        svbvalue2=0
        svbvalue3=0
        #for ib in range(1,hsample['TT'].GetNbinsX()+1):
        #    #print(ib)
        #    if (hsample['TT'].GetBinContent(ib)+hsample['TTB'].GetBinContent(ib)) !=0:
        #        svbvalue1 = svbvalue1 + (hsample['Signal C_{V},C_{2V}=1,k_{#lambda}=-10'].GetBinContent(ib)**2/(hsample['TT'].GetBinContent(ib)+hsample['TTB'].GetBinContent(ib)))
        #        svbvalue2 = svbvalue2 + (hsample['Signal C_{V},C_{2V}=1,k_{#lambda}=-5'].GetBinContent(ib)**2/(hsample['TT'].GetBinContent(ib)+hsample['TTB'].GetBinContent(ib)))
        #        svbvalue3 = svbvalue3 + (hsample['Signal C_{V},C_{2V}=1,k_{#lambda}=5'].GetBinContent(ib)**2/(hsample['TT'].GetBinContent(ib)+hsample['TTB'].GetBinContent(ib)))
#       #         svbvalue = svbvalue + (hsample['Signal C_{V},C_{2V}=1,k_{#lambda}=50'].GetBinContent(ib)**2/(hsample['TT'].GetBinContent(ib)+hsample['TTB'].GetBinContent(ib)))
        #print('s/sqrt(b) value', R.TMath.Sqrt(svbvalue1), R.TMath.Sqrt(svbvalue2), R.TMath.Sqrt(svbvalue3))

        leg.Draw()
        c.SaveAs("%s%s%s_gr.png"%(path,addtional,ifile[0:-5]) )
        #c.SaveAs("%s%s%s_gr.pdf"%(path,addtional,ifile[0:-5]) )
        #c.SaveAs("%s%s%s_gr.C"%(path,addtional,ifile[0:-5]) )
        input('next .. ')


def plot_syst():
    year = '2018'
    for ifile in VHHfiles:
        syst_un=['CMS_scale_j_Abs']
        syst_un=[]
        nickname = { 
            "CMS_pileup_"+year:"pileup",
            "CMS_btag_HF_2016_2017_2018":"btag_HF",
            "CMS_btag_LF_2016_2017_2018":"btag_LF",
            "CMS_btag_cferr1_2016_2017_2018":"btag_cferr1",
            "CMS_btag_cferr2_2016_2017_2018":"btag_cferr2",
            "CMS_btag_hfstats1_"+year:"btag_hfstats1",
            "CMS_btag_hfstats2_"+year:"btag_hfstats2",
            "CMS_btag_lfstats1_"+year:"btag_lfstats1",
            "CMS_btag_lfstats2_"+year:"btag_lfstats2",
            "CMS_btag_jes_"+year: "btag_JES",
            "CMS_res_j_"+year:"JER",
            "CMS_BRewError1_2018":"RewError1",
            "CMS_BRewError2_2018":"RewError2",
            "CMS_scale_j_Abs":"JES_abs",
            "CMS_scale_j_Abs_"+year:"JES_abs_"+year,
            "CMS_scale_j_BBEC1":"JES_BBEC1",
            "CMS_scale_j_BBEC1_"+year:"JES_BBEC1_"+year,
            "CMS_scale_j_EC2":"JES_EC2",
            "CMS_scale_j_EC2_"+year:"JES_EC2_"+year,
            "CMS_scale_j_FlavQCD":"JES_FlavQCD",
            "CMS_scale_j_HF":"JES_HF",
            "CMS_scale_j_HF_"+year:"JES_HF"+year,
            "CMS_scale_j_RelBal":"JES_RelBal",
            "CMS_scale_j_RelSample_"+year:"JES_RelSample",
            "CMS_MSD_JMS_"+year:"JES_JMS",
            "CMS_MSD_JMR_"+year:"JES_JMR",
            "CMS_PNet_"+year:"PNet",
            "CMS_unclusteredEnergy_"+year: "unclusteredEnergy",
            "CMS_eff_m_"+year: "Lep_SF",
            "CMS_eff_MET_"+year: "MET_Trigger",
            "CMS_eff_e_"+year: "Lep_SF",
        }

        for isys in nickname.keys():
            syst_un.append(isys)
        for isys in syst_un:
            if ( 'Znn' in ifile or 'znn' in ifile) and ( 'eff_m' in isys or 'eff_e' in isys ):
                continue
            if ('wen' in ifile or 'Wen' in ifile) and  ('eff_m' in isys or 'MET' in isys):
                continue
            if ('mn' in ifile or 'wmun' in ifile or 'Wmun' in ifile) and ( 'eff_e' in isys or 'MET' in isys):
                continue
            if '_R' in ifile and 'RewError' in isys:
                continue
            procs=["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","TT","TTB", 'VHH_CV_1_C2V_1_kl_0_hbbhbb',"VHH_CV_1_C2V_1_kl_20_hbbhbb"]
            procs=["VHH_CV_1_C2V_1_kl_1_hbbhbb",'TTB']
            plots_proce=["VHH_CV_1_C2V_1_kl_1_hbbhbb",'TTB']
            #procs=["TT"]
            #plots_proce=["TT"]
            hsample = {}
            hsample_r = {}
            print(isys,' from ', ifile)
            #Get all plots
            MAX_ = 0
            Min_ = 0
            MaxX_ = 0
            MinX_ = 0
            NX_ = 0
            fin = R.TFile.Open('{0}'.format(path+ifile),'READ')
            minratio=1
            maxratio=0
            for iprocs in procs:
                if 'RewError' in isys and ('TT' not in iprocs): continue
                if 'RewError' in isys and ('TTV' in iprocs): continue
                fin.cd()
                htemplte = fin.Get(iprocs).Clone()
                print(iprocs+'_'+isys+'Up')
                htemplte_u = fin.Get(iprocs+'_'+isys+'Up').Clone()
                htemplte_d = fin.Get(iprocs+'_'+isys+'Down').Clone()
                NX_=htemplte.GetNbinsX()
                hsample[iprocs] = R.TH1F(iprocs,iprocs,NX_,1,1+NX_)
                hsample[iprocs+'_'+isys+'Up'] = R.TH1F(iprocs+'_'+isys+'Up',iprocs+'_'+isys+'Up',NX_,1,1+NX_)
                hsample[iprocs+'_'+isys+'Down'] = R.TH1F(iprocs+'_'+isys+'Down',iprocs+'_'+isys+'Down',NX_,1,1+NX_)
                for i in range(1,NX_+1):
                    hsample[iprocs].SetBinContent(i,htemplte.GetBinContent(i))
                    hsample[iprocs].SetBinError(i,htemplte.GetBinError(i))
                    hsample[iprocs+'_'+isys+'Up'].SetBinContent(i,htemplte_u.GetBinContent(i))
                    hsample[iprocs+'_'+isys+'Up'].SetBinError(i,htemplte_u.GetBinError(i))
                    hsample[iprocs+'_'+isys+'Down'].SetBinContent(i,htemplte_d.GetBinContent(i))
                    hsample[iprocs+'_'+isys+'Down'].SetBinError(i,htemplte_d.GetBinError(i))
                MinX_=hsample[iprocs].GetBinCenter(1) - hsample[iprocs].GetBinWidth(1)/2.0
                MaxX_=hsample[iprocs].GetBinCenter(NX_) + hsample[iprocs].GetBinWidth(NX_)/2.0
                MAX_ = hsample[iprocs].GetMaximum() if hsample[iprocs].GetMaximum() > MAX_ else MAX_
                Min_ = hsample[iprocs].GetMinimum() if hsample[iprocs].GetMinimum() < MAX_ and hsample[iprocs].GetMinimum()>0 else Min_
                hsample_r[iprocs+'_'+isys+'Up'] = hsample[iprocs+'_'+isys+'Up'].Clone()
                hsample_r[iprocs+'_'+isys+'Up'].Divide(hsample[iprocs])
                hsample_r[iprocs+'_'+isys+'Down'] = hsample[iprocs+'_'+isys+'Down'].Clone()
                hsample_r[iprocs+'_'+isys+'Down'].Divide(hsample[iprocs])
                maxratio = hsample_r[iprocs+'_'+isys+'Up'].GetMaximum() if hsample[iprocs+'_'+isys+'Up'].GetMaximum() > maxratio else maxratio
                maxratio = hsample_r[iprocs+'_'+isys+'Down'].GetMaximum() if hsample[iprocs+'_'+isys+'Down'].GetMaximum() > maxratio else maxratio
                minratio = hsample_r[iprocs+'_'+isys+'Up'].GetMinimum() if hsample_r[iprocs+'_'+isys+'Up'].GetMinimum() < minratio else minratio
                minratio = hsample_r[iprocs+'_'+isys+'Down'].GetMinimum() if hsample_r[iprocs+'_'+isys+'Down'].GetMinimum() < minratio else minratio
                print(minratio, maxratio)
                #make plots
                basecan=R.TCanvas("basecan", "A ratio example",10,32,700,500)
                R.gStyle.SetOptStat(0)
                basecan.SetHighLightColor(2)
                basecan.Range(0,0,1,1)
                basecan.SetFillColor(0)
                basecan.SetBorderMode(0)
                basecan.SetBorderSize(2)
                basecan.SetTicky(1)
                basecan.SetFrameBorderMode(0)
                pad = R.TPad("pad", "",0.0025,0.3,0.9975,0.9975)
                pad.Draw()
                pad.cd()
                pad.SetFillColor(0)
                pad.SetBorderMode(0)
                pad.SetBorderSize(2)
                pad.SetBottomMargin(0.05)
                pad.SetFrameBorderMode(0)
                pad.SetFrameBorderMode(0)
                pad.SetLogy()
                frame_4fa51a0__1 = R.TH1D("frame_4fa51a0__1","",NX_,MinX_,MaxX_)
                frame_4fa51a0__1.GetXaxis().SetTitle("transformed BDT variable")
                frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
                frame_4fa51a0__1.GetXaxis().SetTitleOffset(0.8);
                frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
                frame_4fa51a0__1.GetYaxis().SetTitle("");
                frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
                frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
                frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
                frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
                frame_4fa51a0__1.GetYaxis().SetRangeUser(Min_*0.5,MAX_*2)
                frame_4fa51a0__1.GetYaxis().SetRangeUser(Min_*0.005,MAX_*200)
                frame_4fa51a0__1.Draw("AXISSAME");
                R.gStyle.SetOptStat(0)
                leg = R.TLegend(0.15,0.6,0.55,0.85);
                leg.SetBorderSize(0);
                leg.SetLineStyle(1);
                leg.SetLineWidth(1);
                i=0
            #Draw top
            leg = R.TLegend(0.35,0.6,0.75,0.85);
            leg.SetBorderSize(0);
            leg.SetLineStyle(1);
            leg.SetLineWidth(1);
            i=0
            for iprocs in plots_proce:
                if 'RewError' in isys and 'TT' not in iprocs: continue
                if 'RewError' in isys and 'TTV' in iprocs: continue
                hsample[iprocs].SetLineColor(colorb[i])
                hsample[iprocs].SetLineWidth(3)
                hsample[iprocs].SetMarkerStyle(8)
                hsample[iprocs].SetMarkerColor(colorb[i])
                hsample[iprocs].Draw("same HIST")
                entry=leg.AddEntry(iprocs,iprocs.replace('_hbbhbb','') if '_hbbhbb' in iprocs else iprocs ,"l");
                entry.SetFillStyle(1001);
                entry.SetMarkerStyle(8);
                entry.SetMarkerSize(1.5);
                entry.SetLineStyle(1);
                entry.SetLineWidth(3);
                entry.SetTextFont(42);
                entry.SetTextSize(0.04);
                for iv in ['Up','Down']:
                    i+=1
                    hsample[iprocs+'_'+isys+iv].SetLineColor(colorb[i])
                    hsample[iprocs+'_'+isys+iv].SetLineWidth(2)
                    hsample[iprocs+'_'+isys+iv].Draw("same HIST")
                    hsample[iprocs+'_'+isys+iv].SetMarkerStyle(8)
                    hsample[iprocs+'_'+isys+iv].SetLineStyle(9)
                    hsample[iprocs+'_'+isys+iv].SetMarkerColor(colorb[i])
                    hsample[iprocs+'_'+isys+iv].SetName(iprocs+'_'+isys+iv)
                    hsample[iprocs+'_'+isys+iv].SetTitle(iprocs+'_'+isys+iv)
                    entry=leg.AddEntry(iprocs+'_'+isys+iv,iprocs.replace('_hbbhbb','')+'_'+nickname[isys]+iv if '_hbbhbb' in iprocs else iprocs+'_'+nickname[isys]+iv ,"l");
                    entry.SetFillStyle(1001);
                    entry.SetMarkerStyle(8);
                    entry.SetMarkerSize(1.5);
                    #entry.SetLineStyle(9);
                    entry.SetLineWidth(3);
                    entry.SetTextFont(42);
                    entry.SetTextSize(0.04);
                i+=1
            leg.Draw()
            basecan.cd()
            ##bootom
            bpad = R.TPad("bpad", "",0.0025,0.0025,0.9975,0.33)
            bpad.Draw()
            bpad.cd()
            bpad.SetFillColor(0)
            bpad.SetBorderMode(0)
            bpad.SetBorderSize(2)
            bpad.SetTopMargin(0.05)
            bpad.SetBottomMargin(0.3)
            bpad.SetFrameBorderMode(0)
            bpad.SetFrameBorderMode(0)
            frame_4fa51a0__2 = R.TH1D("frame_4fa51a0__2","",NX_,MinX_,MaxX_)
            frame_4fa51a0__2.GetXaxis().SetTitle("transformed BDT variable")
            frame_4fa51a0__2.GetYaxis().SetTitle("")
            frame_4fa51a0__2.GetXaxis().SetTitleSize(0.15)
            frame_4fa51a0__2.GetYaxis().SetNdivisions(3)
            frame_4fa51a0__2.GetXaxis().SetTitleOffset(0.8)
            frame_4fa51a0__2.GetXaxis().SetTitleFont(42)
            frame_4fa51a0__2.GetXaxis().SetLabelSize(0.1)
            frame_4fa51a0__2.GetYaxis().SetLabelFont(42)
            frame_4fa51a0__2.GetYaxis().SetLabelSize(0.1)
            frame_4fa51a0__2.GetYaxis().SetTitleSize(0.10)
            frame_4fa51a0__2.GetYaxis().SetTitleOffset(0.14)
            frame_4fa51a0__2.GetYaxis().SetTitleFont(42)
            frame_4fa51a0__2.GetYaxis().SetRangeUser(0.9,1.1)
            frame_4fa51a0__2.GetYaxis().SetRangeUser(0.5,1.5)
            if maxratio>1.5 or minratio<0.5:
                frame_4fa51a0__2.GetYaxis().SetRangeUser(0,2)
            elif maxratio>1.2 or minratio<0.8:
                frame_4fa51a0__2.GetYaxis().SetRangeUser(0.5,1.5)
            else:
                frame_4fa51a0__2.GetYaxis().SetRangeUser(0.8,1.2)
            frame_4fa51a0__2.Draw("AXISSAME")
            #Draw bootom
            i=0
            for iprocs in plots_proce:
                if 'RewError' in isys and 'TT' not in iprocs: continue
                if 'RewError' in isys and 'TTV' in iprocs: continue
                for iv in ['Up','Down']:
                    i+=1
                    hsample_r[iprocs+'_'+isys+iv].SetLineColor(colorb[i])
                    hsample_r[iprocs+'_'+isys+iv].SetLineWidth(2)
                    hsample_r[iprocs+'_'+isys+iv].Draw("same HIST")
                    hsample_r[iprocs+'_'+isys+iv].SetMarkerStyle(8)
                    hsample_r[iprocs+'_'+isys+iv].SetLineStyle(9)
                    hsample_r[iprocs+'_'+isys+iv].SetMarkerColor(colorb[i])
                    hsample_r[iprocs+'_'+isys+iv].SetName(iprocs+'_'+isys+iv)
                    hsample_r[iprocs+'_'+isys+iv].SetTitle(iprocs+'_'+isys+iv)
                i+=1
            basecan.cd()
            pad.cd()
            leg.Draw()
            tex = R.TLatex(0.14,0.95,"CMS")
            tex.SetNDC()
            tex.SetTextAlign(13)
            tex.SetTextSize(0.064)
            tex.SetLineWidth(2)
            tex.Draw()
            tex1 = R.TLatex(0.22,0.95,"Simulation Work in Progress")
            tex1.SetNDC()
            tex1.SetTextAlign(13)
            tex1.SetTextFont(52)
            tex1.SetTextSize(0.05)
            tex1.SetLineWidth(2)
            tex1.Draw()
            #basecan.SaveAs("%s%s%s%s.png"%(path,addtional,ifile[0:-5],nickname[isys]) )
            #basecan.SaveAs("%s%s%s%s.pdf"%(path,addtional,ifile[0:-5],nickname[isys]) )
            #basecan.SaveAs("%s%s%s%s.C"%(path,addtional,ifile[0:-5],nickname[isys]) )
            input()


import glob
def plot_datacards(rebin=False,plt_svb=False):
    FriendDir = 'test_220131_testRewUnc_nonpara/'
    pltrew=False
    for ifile in VHHfiles:
        procs=["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb","TT","TTB", 'VHH_CV_1_C2V_1_kl_0_hbbhbb',"VHH_CV_1_C2V_1_kl_20_hbbhbb"]
        procs=["TT","TTB","VHH_CV_1_C2V_1_kl_20_hbbhbb"]
        plots_proce=["TT","TTB","VHH_CV_1_C2V_1_kl_20_hbbhbb"]
        procs=["TTB",'TTB_CMS_BRewError2_13TeV_2018Down','TTB_CMS_BRewError2_13TeV_2018Up']
        plots_proce=["TTB",'TTB_CMS_BRewError2_13TeV_2018Down','TTB_CMS_BRewError2_13TeV_2018Up']
        hsample = {}
        hsamplefriend = {}
        hsvb = {}
        #Get all plots
        MAX_ = 0
        MaxX_ = 0
        MinX_ = 0
        NX_ = 0
        for ifri in glob.glob(FriendDir+'/*root'):
            if ifile in ifri:
                pltrew=True
                print("Need to plot BBDT reweight")
                finfriend = R.TFile.Open('{0}'.format(ifri),'READ')
                for iprocs in procs:
                    finfriend.cd()
                    if rebin:
                        print(iprocs)
                        htemplte = finfriend.Get(iprocs).Clone()
                        NX_=htemplte.GetNbinsX()
                        hsamplefriend[iprocs] = R.TH1F(iprocs,iprocs,NX_,1,1+NX_)
                        for i in range(1,NX_+1):
                            hsamplefriend[iprocs].SetBinContent(i,htemplte.GetBinContent(i))
                            hsamplefriend[iprocs].SetBinError(i,htemplte.GetBinError(i))
                        MinX_=hsamplefriend[iprocs].GetBinCenter(1) - hsamplefriend[iprocs].GetBinWidth(1)/2.0
                        MaxX_=hsamplefriend[iprocs].GetBinCenter(NX_) + hsamplefriend[iprocs].GetBinWidth(NX_)/2.0
                        MAX_ = hsamplefriend[iprocs].GetMaximum() if hsamplefriend[iprocs].GetMaximum() > MAX_ else MAX_
                    else:
                        hsamplefriend[iprocs] = fin.Get(iprocs).Clone()
                        NX_=hsamplefriend[iprocs].GetNbinsX()
                        MinX_=hsamplefriend[iprocs].GetBinCenter(1) - hsamplefriend[iprocs].GetBinWidth(1)/2.0
                        MaxX_=hsamplefriend[iprocs].GetBinCenter(NX_) + hsamplefriend[iprocs].GetBinWidth(NX_)/2.0
                        MAX_ = hsamplefriend[iprocs].GetMaximum() if hsamplefriend[iprocs].GetMaximum() > MAX_ else MAX_


        fin = R.TFile.Open('{0}'.format(path+ifile),'READ')
        print(procs)
        for iprocs in procs:
            fin.cd()
            if rebin:
                print(iprocs)
                htemplte = fin.Get(iprocs).Clone()
                NX_=htemplte.GetNbinsX()
                hsample[iprocs] = R.TH1F(iprocs,iprocs,NX_,1,1+NX_)
                for i in range(1,NX_+1):
                    hsample[iprocs].SetBinContent(i,htemplte.GetBinContent(i))
                    hsample[iprocs].SetBinError(i,htemplte.GetBinError(i))
                MinX_=hsample[iprocs].GetBinCenter(1) - hsample[iprocs].GetBinWidth(1)/2.0
                MaxX_=hsample[iprocs].GetBinCenter(NX_) + hsample[iprocs].GetBinWidth(NX_)/2.0
                MAX_ = hsample[iprocs].GetMaximum() if hsample[iprocs].GetMaximum() > MAX_ else MAX_
            else:
                hsample[iprocs] = fin.Get(iprocs).Clone()
                NX_=hsample[iprocs].GetNbinsX()
                MinX_=hsample[iprocs].GetBinCenter(1) - hsample[iprocs].GetBinWidth(1)/2.0
                MaxX_=hsample[iprocs].GetBinCenter(NX_) + hsample[iprocs].GetBinWidth(NX_)/2.0
                MAX_ = hsample[iprocs].GetMaximum() if hsample[iprocs].GetMaximum() > MAX_ else MAX_

        print(plots_proce)
        print(NX_,MinX_,MaxX_)
        #make plots
        c=R.TCanvas()
        c.SetFillColor(0)
        c.SetBorderMode(0)
        c.SetBorderSize(2)
        c.SetFrameBorderMode(0)
        frame_4fa51a0__1 = R.TH1D("frame_4fa51a0__1","",NX_,MinX_,MaxX_)
        frame_4fa51a0__1.GetXaxis().SetTitle("transformed BDT variable");
        #frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
        #frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(0.8);
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetTitle("");
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetRangeUser(1e-3,MAX_*2)
        frame_4fa51a0__1.Draw("AXISSAME");
        R.gStyle.SetOptStat(0)
        c.SetLogy()
        leg = R.TLegend(0.15,0.2,0.55,0.45);
        leg.SetBorderSize(0);
        leg.SetLineStyle(1);
        leg.SetLineWidth(1);
        i=0
        if '_FailReweight' in iprocs:
            hsample[iprocs].SetName(iprocs.replace('_FailReweight',''))
            hsample[iprocs].SetTitle(iprocs.replace('_FailReweight',''))
        for iprocs in plots_proce:
            print(iprocs)
            hsample[iprocs].SetLineColor(colorb[i])
            hsample[iprocs].SetMarkerStyle(8)
            hsample[iprocs].SetMarkerColor(colorb[i])
            hsample[iprocs].Draw("same p")
            iprocsleng = iprocs
            if pltrew and 'TT' in iprocs:
                iprocsleng = iprocs.replace('_hbbhbb','')+'_Para.' if '_hbbhbb' in iprocs else iprocs+'_Para.'
            iprocsleng = iprocsleng.replace('CMS_BRewError2_13TeV_2018','')
            entry=leg.AddEntry(iprocs,iprocsleng,"lp")
            entry.SetFillStyle(1001);
            entry.SetMarkerStyle(8);
            entry.SetMarkerSize(1.5);
            entry.SetLineStyle(1);
            entry.SetLineWidth(3);
            entry.SetTextFont(42);
            entry.SetTextSize(0.04);
            if pltrew and 'TT' in iprocs and "Error" not in iprocs:
                hsamplefriend[iprocs].SetLineColor(colorb[i])
                #hsamplefriend[iprocs].SetLineStyle(9)
                hsamplefriend[iprocs].Draw("same HIST")
                hsamplefriend[iprocs].SetMarkerStyle(8)
                hsamplefriend[iprocs].SetMarkerColor(colorb[i])
                hsamplefriend[iprocs].SetName(iprocs+'_Pass')
                hsamplefriend[iprocs].SetTitle(iprocs+'_Pass')
                hsample[iprocs].SetName(iprocs+'_FailRew')
                hsample[iprocs].SetTitle(iprocs+'_FailRew')
                #entry=leg.AddEntry(iprocs+'_Pass',iprocs.replace('_hbbhbb','')+'_Pass' if '_hbbhbb' in iprocs else iprocs+'_Pass' ,"l");
                entry=leg.AddEntry(iprocs+'_Pass',iprocs.replace('_hbbhbb','') if '_hbbhbb' in iprocs else iprocs ,"l");
                entry.SetFillStyle(1001);
                entry.SetMarkerStyle(8);
                entry.SetMarkerSize(1.5);
                #entry.SetLineStyle(9);
                entry.SetLineWidth(3);
                entry.SetTextFont(42);
                entry.SetTextSize(0.04);
            i+=1
        leg.Draw()
        addtional='TTB_'
        c.SaveAs("%s%s%s.png"%(path,addtional,ifile[0:-5]) )
        c.SaveAs("%s%s%s.pdf"%(path,addtional,ifile[0:-5]) )
        c.SaveAs("%s%s%s.C"%(path,addtional,ifile[0:-5]) )
        #input() 
 
def merge_emptyBins():
    for ifile in VHHfiles:
        hsample = {}
        hout={}
        fin = R.TFile.Open('{0}'.format(path+ifile),'READ')
        hbkgstack = fin.Get('data_obs').Clone()
        hbkgstack.Reset()
        EMPTYN=0
        EMPTYX=[]
        for iprocs in bkg_procs:
            fin.cd()
            hbkgstack = fin.Get(iprocs)
            #hbkgstack.Add( fin.Get(iprocs) )
            for i in range(1,hbkgstack.GetNbinsX()+1):
                if hbkgstack.GetBinContent(i) <=0 and i not in EMPTYX:
                    print(' in ', path+ifile)
                    print("bkg = 0 at ",hbkgstack.GetBinCenter(i), " ", ifile)
                    EMPTYN+=1
                    EMPTYX.append(i)
        fout = R.TFile.Open('{0}/{1}{2}'.format(args.out,addtional,ifile),'RECREATE')
        #copy and merge 0 bins
        #for iprocs in procs:
        for iprocs in procs_addunc:
            print(ifile)
            if ( 'Znn' in ifile or 'znn' in ifile) and 'eff_m' in iprocs:
                iprocs = iprocs.replace('eff_m','eff_MET') 
            if 'wenu' in ifile or 'Wenu' in ifile or 'Wen' in ifile:
                iprocs = iprocs.replace('eff_m','eff_e')
            if '_B' not in ifile and 'BRewError' in iprocs:
                continue
            print(iprocs, ' in ', path+ifile)
            fin.cd()
            print(iprocs)
            hsample[iprocs] = fin.Get(iprocs).Clone()
            hout[iprocs] = R.TH1F(iprocs,iprocs,hsample[iprocs].GetNbinsX()-EMPTYN, 1, hsample[iprocs].GetNbinsX()+1-EMPTYN)
            if iprocs in data_obs:
                print("skip data")
            else:
                ireal=0
                for i in range(1,hsample[iprocs].GetNbinsX()+1):
                    ireal+=1
                    if i in EMPTYX: 
                        ireal-=1
                        merged = hout[iprocs].GetBinContent(ireal) + hsample[iprocs].GetBinContent(i)
                        merged_err = math.sqrt(hout[iprocs].GetBinError(ireal)**2 + hsample[iprocs].GetBinError(i)**2)
                        print(i, 'is 0',hout[iprocs].GetBinContent(ireal), ' and ', hsample[iprocs].GetBinContent(i),' merge to ', merged)
                        print(i, 'is 0',hout[iprocs].GetBinError(ireal), ' and ', hsample[iprocs].GetBinError(i),' merge to ', merged_err)
                        hout[iprocs].SetBinContent(ireal,merged)
                        hout[iprocs].SetBinError(ireal,merged_err)
                    else:
                        hout[iprocs].SetBinContent(ireal,hsample[iprocs].GetBinContent(i))
                        hout[iprocs].SetBinError(ireal,hsample[iprocs].GetBinError(i))
            fout.cd()
            if '_FailReweight' in iprocs:
                hout[iprocs].SetName(iprocs.replace('_FailReweight',''))
                hout[iprocs].SetTitle(iprocs.replace('_FailReweight',''))
            hout[iprocs].Write()

def cuthist(setdata0=False):
    for ifile in VHHfiles:
        if 'HMP_B' in ifile: continue
        hsample = {}
        hout={}
        fin = R.TFile.Open('{0}'.format(path+ifile),'READ')
        for iprocs in procs:
            hsample[iprocs] = fin.Get(iprocs).Clone()
        print('total length is ', hsample['data_obs'].GetNbinsX())
        #svb=0
        #for ibin in range(1,(hsample['data_obs'].GetNbinsX()+1)):
        #    #svb += hsample['VHH_CV_1_C2V_2_kl_1_hbbhbb'].GetBinContent(ibin)**2/(hsample['TT'].GetBinContent(ibin)+hsample['TTB'].GetBinContent(ibin))
        #    svb += hsample['VHH_CV_1_C2V_1_kl_1_hbbhbb'].GetBinContent(ibin)**2/(hsample['TT'].GetBinContent(ibin)+hsample['TTB'].GetBinContent(ibin)+hsample['s_Top'].GetBinContent(ibin))
        #    print(ibin,'%0.6f'%math.sqrt(svb))
        #print('The total svb for ',ifile, ' is ', math.sqrt(svb) )
        #input("")
        #continue
        Nbinnumber=0
        if 'Wen_High_R' in ifile: Nbinnumber=8
        if 'Wen_Low_R' in ifile: Nbinnumber=12
        if 'Wmn_High_R' in ifile: Nbinnumber=8
        if 'Wmn_Low_R' in ifile: Nbinnumber=13
        if 'Znn_High_R' in ifile: Nbinnumber=4
        if 'Znn_Low_R' in ifile: Nbinnumber=5
        if 'Wen_LP_B' in ifile: Nbinnumber=5
        if 'Wmn_LP_B' in ifile: Nbinnumber=5
        if 'Znn_LP_B' in ifile: Nbinnumber=3
        fout = R.TFile.Open('{0}/{1}'.format(args.out,ifile),'RECREATE')
        #for iprocs in procs:
        print(ifile)
        for iprocs in procs_addunc:
            if ( 'Znn' in ifile or 'znn' in ifile) and 'eff_m' in iprocs:
                iprocs = iprocs.replace('eff_m','eff_MET')
            if 'wenu' in ifile or 'Wenu' in ifile or 'Wen' in ifile:
                print('replace eff_m')
                iprocs = iprocs.replace('eff_m','eff_e')
            if 'Znn' in ifile and ('eff_m' in iprocs or 'eff_e' in iprocs): continue
            if 'Wen' in ifile and 'eff_m' in iprocs: continue
            if 'Wmn' in ifile and 'eff_e' in iprocs: continue
            if '_R' in ifile and 'BRewError' in iprocs: continue
            print(iprocs)
            fin.cd()
            hsample[iprocs] = fin.Get(iprocs).Clone()
            if setdata0:
                hout[iprocs] = hsample[iprocs].Clone()
                if 'data_obs' == iprocs:
                    for ibin in range(Nbinnumber+1,hsample[iprocs].GetNbinsX()+1):
                        hout[iprocs].SetBinContent(ibin, 0)
                        hout[iprocs].SetBinError(ibin, 0)
                fout.cd()
                hout[iprocs].Write()
            else:
                hout[iprocs] = R.TH1F(iprocs,iprocs,Nbinnumber, 1, Nbinnumber+1)
                for ibin in range(Nbinnumber+1):
                    hout[iprocs].SetBinContent(ibin, hsample[iprocs].GetBinContent(ibin))
                    hout[iprocs].SetBinError(ibin, hsample[iprocs].GetBinError(ibin))
                fout.cd()
                hout[iprocs].Write()

VHHfiles = ['sum_hists_2018_Wen_High_R.root','sum_hists_2018_Wen_Low_R.root',
            'sum_hists_2018_Wmn_High_R.root','sum_hists_2018_Wmn_Low_R.root',
            'sum_hists_2018_Znn_High_R.root','sum_hists_2018_Znn_Low_R.root',
            'sum_hists_2018_Wen_HMP_B.root','sum_hists_2018_Wen_LP_B.root',
            'sum_hists_2018_Wmn_HMP_B.root','sum_hists_2018_Wmn_LP_B.root',
            'sum_hists_2018_Znn_HMP_B.root','sum_hists_2018_Znn_LP_B.root',
           ]
#cuthist(setdata0=False)
#cuthist(setdata0=True)
merge_emptyBins()
exit()

#VHHfiles = ['sum_hists_2018_Wen_High_R.root']#,'sum_hists_2018_Wen_Low_R.root','sum_hists_2018_Wmn_High_R.root','sum_hists_2018_Wmn_Low_R.root','sum_hists_2018_Wen_LP_B.root','sum_hists_2018_Wmn_LP_B.root']

# TTB, TT
#scalelist = {
#'sum_hists_2018_Wen_High_R.root':[1.3,0.82],'sum_hists_2018_Wen_Low_R.root':[1.1,0.86],'sum_hists_2018_Wmn_High_R.root':[1.39, 0.93],'sum_hists_2018_Wmn_Low_R.root':[1.88,0.95],'sum_hists_2018_Znn_High_R.root':[2.15, 0.65],'sum_hists_2018_Znn_Low_R.root':[3.96, 0.45],
#'sum_hists_2018_Znn_LP_B.root':[2.68231,0.815169],'sum_hists_2018_Wen_LP_B.root':[4.21331,0],'sum_hists_2018_Wmn_LP_B.root':[5.69034,0.108359],
#}
#scalelist = {
#    'sum_hists_2018_Wen_High_R.root':[1.,1],'sum_hists_2018_Wen_Low_R.root':[1.,1],'sum_hists_2018_Wmn_High_R.root':[1., 1],'sum_hists_2018_Wmn_Low_R.root':[1.,1],'sum_hists_2018_Znn_High_R.root':[1, 1],'sum_hists_2018_Znn_Low_R.root':[1, 1],
#    'sum_hists_2018_Znn_LP_B.root':[1,1],'sum_hists_2018_Wen_LP_B.root':[1,1],'sum_hists_2018_Wmn_LP_B.root':[1,1],
#}
#
#znnscale = [2.01,0.68]
#scalelist = {
#    'sum_hists_2018_Znn_High_R.root':znnscale,'sum_hists_2018_Znn_Low_R.root':znnscale,'sum_hists_2018_Znn_LP_B.root':znnscale,
#}
##VHHfiles = ['sum_hists_2018_Znn_High_R.root','sum_hists_2018_Znn_Low_R.root','sum_hists_2018_Znn_LP_B.root']
##scalelist = {
##    'sum_hists_2018_Wen_High_R.root':[2.29843,1.32842],'sum_hists_2018_Wen_Low_R.root':[2.29843,1.32842],'sum_hists_2018_Wmn_High_R.root':[2.29843,1.32842],'sum_hists_2018_Wmn_Low_R.root':[2.29843,1.32842],
##    'sum_hists_2018_Wen_LP_B.root':[2.29843,1.32842],'sum_hists_2018_Wmn_LP_B.root':[2.29843,1.32842],
##}
#wlnscale = [2.16, 1.14]
#scalelist = {
#    'sum_hists_2018_Wen_High_R.root':wlnscale,'sum_hists_2018_Wen_Low_R.root':wlnscale,'sum_hists_2018_Wen_LP_B.root':wlnscale,
#    'sum_hists_2018_Wmn_High_R.root':wlnscale,'sum_hists_2018_Wmn_Low_R.root':wlnscale,'sum_hists_2018_Wmn_LP_B.root':wlnscale,
#}
VHHfiles = ['sum_hists_2018_Wen_High_R.root','sum_hists_2018_Wen_Low_R.root',
            'sum_hists_2018_Wmn_High_R.root','sum_hists_2018_Wmn_Low_R.root',
            'sum_hists_2018_Znn_High_R.root','sum_hists_2018_Znn_Low_R.root',
            'sum_hists_2018_Wen_HMP_B.root','sum_hists_2018_Wen_LP_B.root',
            'sum_hists_2018_Wmn_HMP_B.root','sum_hists_2018_Wmn_LP_B.root',
            'sum_hists_2018_Znn_HMP_B.root','sum_hists_2018_Znn_LP_B.root',
           ]
#VHHfiles = ['sum_hists_2018_Wen_High_R.root']
plot_datacardswithdifferentcombination(rebin=True,plt_svb=False,drawStack=False)
#plot_datacards(rebin=True,plt_svb=True)   # plot the comparison of BBDT pass and fail reweight
#plot_syst()

exit()



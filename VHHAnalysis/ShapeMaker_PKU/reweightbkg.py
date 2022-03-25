from rootpy.plotting import Hist
from rootpy.io import File
import numpy as np
from Dictionaries.VHH4b_channelDict import channelDict
from rootpy.tree import Tree, TreeChain
from glob import glob
import ROOT as R
from array import *
from condor_config import indir as ntuple_path

#ntuple_path = '/eos/home-y/yilai/VHH4bAnalysisNtuples/TEST_220108_2016pre/'
#ntuple_path = '/eos/home-y/yilai/VHH4bAnalysisNtuples/TEST_1218_2017/'
#ntuple_path = '/eos/user/y/yilai/VHH4bAnalysisNtuples/clean_bdt_tool_oct22/TEST_1116_updatebtagSF_boosted/'
#ntuple_path = '/eos/user/y/yilai/VHH4bAnalysisNtuples/clean_bdt_tool_22jan17/TEST_220122_2018_boosted_skim/'
ntuple_path = '2018_skim_keepboosted_BDTv2/'

#VHH_ttbkg = ['TT_AllHadronic','TT_DiLep_NoPSWeights','TT_SingleLep','ttbb_AllHadronic','ttbb_DiLep','ttbb_SingleLep']
#VHH_ttbkg = ['TT_AllHadronic','TT_DiLep_NoPSWeights','TT_SingleLep','TTBB_AllHadronic','TTBB_DiLep','TTBB_SingleLep']
VHH_ttbkg = {
    'TT':['TT_AllHadronic','TT_DiLep_NoPSWeights','TT_SingleLep'],
    'TTB':['TTBB_AllHadronic','TTBB_DiLep','TTBB_SingleLep']
    #'All':['TTBB_AllHadronic','TTBB_DiLep','TTBB_SingleLep','TT_AllHadronic','TT_DiLep_NoPSWeights','TT_SingleLep']
}
#VHH_ttbkg = ['WHHTo4B_CV_0_5_C2V_1_0_C3_1_0','WHHTo4B_CV_1_0_C2V_0_0_C3_1_0','WHHTo4B_CV_1_0_C2V_1_0_C3_0_0','WHHTo4B_CV_1_0_C2V_1_0_C3_1_0','WHHTo4B_CV_1_0_C2V_2_0_C3_1_0','WHHTo4B_CV_1_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0','ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0','ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0','ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0','WHHTo4B_CV_1_0_C2V_1_0_C3_20_0','WHHTo4B_CV_1_0_C2V_1_0_C3_2_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0']

doskim=False
if doskim:
    # Skim files if it's too large
    import os
    def createDir(OutDir):
        if OutDir is not None :
            if not os.path.isdir( OutDir ) :
                os.makedirs( OutDir )
    from root_numpy import root2array, rec2array, array2root
    newdir='2018_skim_keepboosted_BDTv2'
    createDir(newdir)
    doBoost=True
    branch_names = [
                'VHH_H1_m','VHH_H1_pT','VHH_H1_eta','VHH_H1_phi','VHH_H1_e',
                'VHH_H2_m','VHH_H2_pT','VHH_H2_eta','VHH_H2_phi','VHH_H2_e',
                'VHH_HH_m','VHH_HH_pT','VHH_HH_eta','VHH_HH_phi','VHH_HH_e',
                'VHH_H1_BJet1_btag','VHH_H1_BJet2_btag','VHH_H2_BJet1_btag','VHH_H2_BJet2_btag',
                'j1_btagcat','j2_btagcat','j3_btagcat','j4_btagcat',
                'lepMetDPhi','sampleIndex',
                'VHH_HH_dphi','VHH_HH_deta','VHH_HH_dR','VHH_rHH','VHH_HT','IsttB',
                'VHH_mass','VHH_Vreco4j_HT','VHH_vsptmassRatio','VHH_H2H1_pt_ratio','VHH_V_HH_dPhi','VHH_V_H1_dPhi','VHH_V_H2_dPhi',
                'VHH_V_phi','VHH_V_m','VHH_V_e','VHH_nBJets','VHH_nBJets_loose','VHH_nBJets_tight','MET_Pt','MET_Phi','V_pt',
                'weight','isZnn','isZmm','isZee','selLeptons_pt_0','selLeptons_phi_0','selLeptons_eta_0',
                'isWenu','isWmunu',
                'isResolved','isBoosted',
                'VHHFatJet1_Msoftdrop','VHHFatJet1_Pt','VHHFatJet1_eta','VHHFatJet1_phi','VHHFatJet1_e',
                'VHHFatJet2_Msoftdrop','VHHFatJet2_Pt','VHHFatJet2_eta','VHHFatJet2_phi','VHHFatJet2_e',
                'VHHFatJet_mjj','VHHFatJet_HHPt','VHHFatJet_HHe',
                'VHHFatJet1VdPhi','VHHFatJet2VdPhi','VHHFatH1H2dPhi',
                'VHHFatJet1_ParticleNetMD_bbvsQCD','VHHFatJet2_ParticleNetMD_bbvsQCD',
                'VHHFatJet_HHdR','VHHFatJet_HHeta','VHHFatJet1VdEta',
                'h1_pnetcat','h2_pnetcat','Pass_nominal','VHH_nFatJet','controlSample',
                #'wlnBBDT_rew_HMP','wlnBBDT_rew_LP','wlnBBDT_svb_HMP','wlnBBDT_svb_LP',
                #'wlnRBDT_cate_kl20VSkl0','RBDT_svb_Highscore','RBDT_svb_Lowscore',
                #'RBDT_cate_kl20VSkl0','wlnRBDT_svb_Highscore','wlnRBDT_svb_Lowscore',
                'wlnBBDT_SvB_lep_HMP_v2','wlnBBDT_SvB_lep_LP_v2','wlnBBDT_SvB_v_HMP_v2','wlnBBDT_SvB_v_LP_v2',
                'wlnBBDT_rew_lep_HMP_v2','wlnBBDT_rew_lep_LP_v2','wlnBBDT_rew_v_HMP_v2','wlnBBDT_rew_v_LP_v2',
                'wlnRBDT_cate_kl20VSkl0_v2','wlnRBDT_svb_lep_Highscore_v2','wlnRBDT_svb_lep_Lowscore_v2','wlnRBDT_svb_v_Highscore_v2','wlnRBDT_svb_v_Lowscore_v2',
                'znnBBDT_SvB_HMP_v2','znnBBDT_SvB_LP_v2','znnBBDT_rew_HMP_v2','znnBBDT_rew_LP_v2','znnRBDT_cate_kl20VSkl0_v2','znnRBDT_svb_Highscore_v2','znnRBDT_svb_Lowscore_v2'

                ]
    for iDic in VHH_ttbkg:
        createDir(newdir+'/'+iDic)
        if doBoost:
            sample_paths = glob(ntuple_path+'/'+iDic+'/*root') 
            sample_paths1D = [sample_glob for sample_glob in sample_paths]
            for ifile in sample_paths1D:
                print(ifile,newdir+'/'+iDic+'/'+ifile.split('/')[-1])
                inputfile=ifile
                outstring=newdir+'/'+iDic+'/'+ifile.split('/')[-1]
                ttbbstitch='&&IsttB==0'
                if 'TTBB' in ifile: ttbbstitch='&&IsttB>0'
                test = root2array(inputfile, "Events", branches=branch_names, selection='isBoosted'+ttbbstitch)
                array2root(test, outstring,treename='Events', mode='recreate')
    
    exit()


# Set target branch 
# get the weight to make TTB fail similar to TTB pass
# if doReweight, plot 2D and get weight from this file apply it to 2D and profile it

#for a given channel in the channel dict, get the selection and plot variable and compute the flattened signal, nbins
def getFlatBinning4BKG(files,selection,failselection,variable,xlow,xhigh, bins):
    values = []
    fail_values = []
    for f in files:
        tree = File(f,"read").get("Events")
        tarray = tree.to_array([variable,"weight"],selection=selection)
        values.append(tarray)
        tfailarray = tree.to_array([variable,"weight"],selection=failselection)
        fail_values.append(tfailarray)
    values = np.concatenate(values)
    fail_values = np.concatenate(fail_values)
    s_tot = values["weight"].sum()
    print("Pass total: ", s_tot, ' fail total: ', fail_values["weight"].sum())
    values = np.sort(values)
    cumu = np.cumsum(values["weight"])
    targets = [n*s_tot/bins for n in range(1,bins)]
    workingPoints = []
    for target in targets:
        index = np.argmax(cumu>target)
        workingPoints.append(values[index][variable])
    return values, fail_values, [float(xlow)]+workingPoints+[float(xhigh)]

def getFlatBinning4Sig(files,selection,variable,xlow,xhigh, bins):
    values = []
    for f in files:
        tree = File(f,"read").get("Events")
        tarray = tree.to_array([variable,"weight"],selection=selection)
        values.append(tarray)
    values = np.concatenate(values)
    s_tot = values["weight"].sum()
    print("Pass total: ", s_tot)
    values = np.sort(values)
    cumu = np.cumsum(values["weight"])
    targets = [n*s_tot/bins for n in range(1,bins)]
    workingPoints = []
    for target in targets:
        index = np.argmax(cumu>target)
        workingPoints.append(values[index][variable])
    return values, [float(xlow)]+workingPoints+[float(xhigh)]

def plot_BDTreweight(VHHfiles, procs):
    legname=['Pass','Fail','weight']
    for ifile in VHHfiles:
        hsample = {}
        fin = R.TFile.Open('{0}'.format(ifile),'READ')
        #Get all plots
        MAX_ = 0
        MaxX_ = 0
        MinX_ = 0
        NX_ = 0
        Min_ = 0
        print('procs contains ',procs)
        for iprocs in procs:
            fin.cd()
            htmp = fin.Get(iprocs).Clone()
            NX_=htmp.GetNbinsX()
            MinX_=htmp.GetBinCenter(1) - htmp.GetBinWidth(1)/2.0
            MaxX_=htmp.GetBinCenter(NX_) + htmp.GetBinWidth(NX_)/2.0
            MAX_ = htmp.GetMaximum() if htmp.GetMaximum() > MAX_ else MAX_
            Min_ = htmp.GetMinimum() if htmp.GetMinimum() < Min_ else Min_
            hsample[iprocs] = R.TH1F(iprocs,iprocs,NX_,1,1+NX_)
            for i in range(1,NX_+1):
                hsample[iprocs].SetBinContent(i,htmp.GetBinContent(i))
                hsample[iprocs].SetBinError(i,htmp.GetBinError(i))
        print(NX_,MinX_,MaxX_)
        c=R.TCanvas()
        c.SetFillColor(0)
        c.SetBorderMode(0)
        c.SetBorderSize(2)
        c.SetFrameBorderMode(0)
        histframe = R.TH1D("histframe","",NX_,1,1+NX_)
        histframe.GetXaxis().SetTitle("transformed BDT variable")
        histframe.GetXaxis().SetTitleSize(0.05)
        histframe.GetXaxis().SetTitleOffset(0.8)
        histframe.GetXaxis().SetTitleFont(42)
        histframe.GetYaxis().SetTitle("")
        histframe.GetYaxis().SetLabelFont(42)
        histframe.GetYaxis().SetLabelSize(0.05)
        histframe.GetYaxis().SetTitleSize(0.05)
        histframe.GetYaxis().SetTitleFont(42)
        histframe.GetYaxis().SetRangeUser(Min_*0.7,MAX_*1.3)
        histframe.Draw("AXISSAME")
        R.gStyle.SetOptStat(0)
        #c.SetLogy()
        leg = R.TLegend(0.6,0.6,0.85,0.8)
        leg.SetBorderSize(0)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        i=0
        for iprocs in procs:
            print(iprocs)
            hsample[iprocs].SetLineColor(i+2)
            hsample[iprocs].SetLineWidth(2)
            hsample[iprocs].SetMarkerColor(i+2)
            hsample[iprocs].Draw("same HIST")
            entry=leg.AddEntry(iprocs,legname[i] ,"lp")
            entry.SetFillStyle(1001)
            entry.SetMarkerStyle(8)
            entry.SetMarkerSize(1.5)
            entry.SetLineStyle(1)
            entry.SetLineWidth(3)
            entry.SetTextFont(42)
            entry.SetTextSize(0.06)
            i+=1
        leg.Draw()
        tex = R.TLatex(0.14,0.95,"CMS")
        tex.SetNDC()
        tex.SetTextAlign(13)
        tex.SetTextSize(0.048)
        tex.SetLineWidth(2)
        tex.Draw()
        tex1 = R.TLatex(0.22,0.95,"Simulation Work in Progress")
        tex1.SetNDC()
        tex1.SetTextAlign(13)
        tex1.SetTextFont(52)
        tex1.SetTextSize(0.03648)
        tex1.SetLineWidth(2)
        tex1.Draw()
        c.SaveAs("test.png")
        input("exit...")

#plot_BDTreweight(['wenuBBDT_v_svb_HMP_TT_weight.root'], ['histspass','histsfail','histsweight'])
#exit()

binsDict = {}
binsvalueDict = {}
binserrorDict = {}
for key in channelDict:
    if "doReweight" in channelDict[key].keys():
        if channelDict[key]["doReweight"]==1:
            print(key)
            print("it's reweighting time, make sure failcutstring, rewvarNames exist")
            binsDict[key] = {}
            binsvalueDict[key] = {}
            binserrorDict[key] = {}
            for iT in VHH_ttbkg.keys():
                binsvalueDict[key][iT] = []
                binserrorDict[key][iT] = []
                samples = VHH_ttbkg[iT]
                sample_paths = [glob(ntuple_path+'/'+sample+'/*root') for sample in samples]
                sample_paths1D = [path for sample_glob in sample_paths for path in sample_glob]
                print('get binning and weight for Rew.BDT ')
                nbins = 20
                if iT == 'TTB': nbins = 10
                passbkg_values, fail_values, binning = getFlatBinning4BKG(sample_paths1D,channelDict[key]["cutstring"],channelDict[key]["failcutstring"],channelDict[key]["rewvarNames"][0],channelDict[key]["xlow"],channelDict[key]["xhigh"],nbins)
                binsDict[key][iT] = binning
                histspass = R.TH1F("histspass","bkg pass",nbins,-1,1)
                histsfail = R.TH1F("histsfail","bkg fail",nbins,-1,1)
                runArray = array('d',binning)
                print('flat binning for bkg is ',binning)
                print('make histogram, find the weight ')
                histspass.SetBins(len(runArray)-1, runArray)
                histsfail.SetBins(len(runArray)-1, runArray)
                for i in range(len(passbkg_values)):
                    histspass.Fill(passbkg_values[i][channelDict[key]["rewvarNames"][0]],passbkg_values[i]["weight"])
                for i in range(len(fail_values)):
                    histsfail.Fill(fail_values[i][channelDict[key]["rewvarNames"][0]],fail_values[i]["weight"])
                histsweight = histspass.Clone()
                histsweight.Divide(histsfail)
                histsweight.SetTitle("histsweight")
                histsweight.SetName("histsweight")
                for i in range(1,histsweight.GetNbinsX()+1):
                    binsvalueDict[key][iT].append(histsweight.GetBinContent(i))
                    binserrorDict[key][iT].append(histsweight.GetBinError(i))
                print("======>")
                print(binsDict,binsvalueDict,binserrorDict)
                fout = R.TFile.Open(key+'_'+iT+'_weight.root','RECREATE')
                fout.cd()
                histspass.Write()
                histsfail.Write()
                histsweight.Write()
                fout.Close()

outputFile = open("Dictionaries/VHH4b_reweightDict.py","w")
content = "reweightDict = "
content += str(binsDict).replace('],','],\n')+'\n'
content += "reweightValueDict = "
content += str(binsvalueDict).replace('],','],\n')+'\n'
content += "reweightErrorDict = "
content += str(binserrorDict).replace('],','],\n')+'\n'
outputFile.write(content)
outputFile.close()

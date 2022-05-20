#from Dictionaries.VHH4b_reweightDict_para_shift7 import reweightDict,reweightValueDict,reweightErrorDict
# from Dictionaries.VHH4b_reweightDict_para_shift7 import reweightDict,reweightValueDict,reweightError1Dict,reweightError2Dict
from Dictionaries.VHH4b_reweightDict import reweightDict,reweightValueDict
from Dictionaries.VHH4b_binsDict_rwt import binsDict
import os, sys
from array import array

histfiles = [i for i in os.listdir('.') if i.startswith("hists_") and i.endswith(".root")]
out = 'DL_2018_rwt'
os.system("mkdir -p "+out)
done = []

scaleFactorforAll = 137.0/137.0
#2*137/36.6
#2*137/41.53
#2*137/58.8

VHHfiles = [i for i in os.listdir('.') if i.startswith("hists_")  and "VHH_CV_1_C2V_1_kl_1_hbbhbb_idx-1" in i]

channel_list = ['hists_2018_R_Zll_Klbdt_SM_3b_bin_SR_Z', 'hists_2018_R_Zll_Klbdt_High_3b_bin_SR_Z',\
                'hists_2018_R_Zll_Klbdt_SM_4b_bin_SR_Z', 'hists_2018_R_Zll_Klbdt_High_4b_bin_SR_Z']

# channel_list = ['hists_2017_R_Zll_Klbdt_SM_3b_bin_SR_Z', 'hists_2017_R_Zll_Klbdt_High_3b_bin_SR_Z',\
#                 'hists_2017_R_Zll_Klbdt_SM_4b_bin_SR_Z', 'hists_2017_R_Zll_Klbdt_High_4b_bin_SR_Z']

# channel_list = ['hists_2016_R_Zll_Klbdt_SM_3b_bin_SR_Z', 'hists_2016_R_Zll_Klbdt_High_3b_bin_SR_Z',\
#                 'hists_2016_R_Zll_Klbdt_SM_4b_bin_SR_Z', 'hists_2016_R_Zll_Klbdt_High_4b_bin_SR_Z']

for fl in VHHfiles:
    if not (fl.split("_VHH_CV_1_C2V_1_kl_1_hbbhbb_idx-1")[0] in channel_list):
        channel_list.append(fl.split("_VHH_CV_1_C2V_1_kl_1_hbbhbb_idx-1")[0])
print("channel_list: ", channel_list)

exe = open(out+'/VHH.sh', 'w')
for fl in channel_list:
    if "2016" in fl:
        if "pre" in fl:
            cmd = "hadd -f "+out+"/sum_%s_raw.root %s_*"%(fl.replace("pre",""),fl.replace("pre","*"))
            exe.write('VHHcard  '+fl.replace("pre","") +' '+out+'/sum_%s.root \n'%(fl.replace("pre","")))
            print "Running command:", cmd
            os.system(cmd)
            done.append(out+"/sum_%s_raw.root"%(fl.replace("pre","")))
        elif "post" in fl:
            cmd = "hadd -f "+out+"/sum_%s_raw.root %s_*"%(fl.replace("post",""),fl.replace("post","*"))
            exe.write('VHHcard  '+fl.replace("post","") +' '+out+'/sum_%s.root \n'%(fl.replace("post","")))
            print "Running command:", cmd
            os.system(cmd)
            done.append(out+"/sum_%s_raw.root"%(fl.replace("post","")))
        else:
            cmd = "hadd -f "+out+"/sum_%s_raw.root %s_*"%(fl,fl)
            exe.write('VHHcard  '+fl +' '+out+'/sum_%s.root \n'%(fl))
            print "Running command:", cmd
            os.system(cmd)
            done.append(out+"/sum_%s_raw.root"%(fl))
    else:
        cmd = "hadd -f "+out+"/sum_%s_raw.root %s_*"%(fl,fl)
        exe.write('VHHcard  '+fl +' '+out+'/sum_%s.root \n'%(fl))
        print "Running command:", cmd
        os.system(cmd)
        done.append(out+"/sum_%s_raw.root"%(fl))

import ROOT as r
for d in done:
    f = r.TFile(d, "update")
    h = f.Get("VHH_CV_1_C2V_1_kl_1_hbbhbb")
    binname=''    
    doboost=False
    for ibin in binsDict.keys():
        if ibin in d:
            print('find this bin', ibin,len(binsDict[ibin]), binsDict[ibin])
            binning = binsDict[ibin]
            if ibin in reweightValueDict.keys(): 
                print("====> And this is for boosted topo!")
                doboost=True
                rewbinning = reweightDict[ibin]
                rewvalue = reweightValueDict[ibin]
                rewerror1 = reweightError1Dict[ibin]
                rewerror2 = reweightError2Dict[ibin]
            binname=ibin
            continue
    if ibin=='': 
        print("can't find the binning, check Dictionaries/VHH4b_binsDict.py")
    hnames = {}
    key = f.GetListOfKeys()
    key2=[]
    for i in range(len(key)):
        key2.append(key[i].GetName())
        print(' add ====> ', key[i].GetName())
        h = key[i].ReadObj()
        if h.ClassName() == 'TH1D' or h.ClassName() == 'TH1F':
            hnames[key[i].GetName()]=h.Clone()
#             #mark!!!
            if '2018' in d:
                f_zll_rwt_err = R.TFile("./2018_histo_of_RwT_err.root","READ")
                if 'SM_3b' in d:
                    if "DY" in key[i].GetName():
                        err_hist = 
                        
            
#             if "DY" in key[i].GetName():
#                 print("===================== DY2016 scale factor used ========================")
#                 hnames[key[i].GetName()].Scale(1.4)
            if "data" in key[i].GetName():
                hnames[key[i].GetName()].Scale(0)
        #Boosted
        elif  h.ClassName() == 'TH2D' and doboost :
            rewvalue2 =[]
            rewerror1_ =[]
            rewerror2_ =[]
            rewbinning2 =[]
            print(rewvalue)
            if 'TTB' in key[i].GetName(): 
                if len(rewvalue['TTB'])!=h.GetNbinsY(): 
                    print('Error!')
                    exit()
                else: 
                    rewvalue2 = rewvalue['TTB']
                    rewerror1_ = rewerror1['TTB']
                    rewerror2_ = rewerror2['TTB']
                    rewbinning2 = rewbinning['TTB']
            elif 'TT' in key[i].GetName(): 
                if len(rewvalue['TT'])!=h.GetNbinsY(): 
                    print('Error!')
                    exit()
                else: 
                    rewvalue2 = rewvalue['TT']
                    rewerror1_ = rewerror1['TT']
                    rewerror2_ = rewerror2['TT']
                    rewbinning2 = rewbinning['TT']
            else: exit()
            ifAddRewUnc = True
            # For TT or TTB, Let's add another 2 BDT reweight uncertainty
            if ifAddRewUnc and ('TTB' == key[i].GetName() or 'TT' == key[i].GetName()):
                #CMS_BRewError1_13TeV_2018 up down
                sysname = 'CMS_BRewError1_2018'
                key2.append(key[i].GetName()+'_'+sysname+'Up')
                key2.append(key[i].GetName()+'_'+sysname+'Down')
                hnames[key[i].GetName()+'_'+sysname+'Up']=r.TH2D(key[i].GetName()+'_'+sysname+'Up', sysname+'Up',len(binning)-1,array('d',binning), len(rewbinning2)-1,array('d',rewbinning2))
                hnames[key[i].GetName()+'_'+sysname+'Down']=r.TH2D(key[i].GetName()+'_'+sysname+'Down', sysname+'Down',len(binning)-1,array('d',binning), len(rewbinning2)-1,array('d',rewbinning2))
                for iby in range(1,h.GetNbinsY()+1):
                    for ibx in range(1,h.GetNbinsX()+1):
                        hnames[key[i].GetName()+'_'+sysname+'Up'].SetBinContent(ibx,iby,h.GetBinContent(ibx,iby)*(rewerror1_['Up'][iby-1]))
                        hnames[key[i].GetName()+'_'+sysname+'Up'].SetBinError(ibx,iby,h.GetBinError(ibx,iby)*(rewerror1_['Up'][iby-1]))
                        hnames[key[i].GetName()+'_'+sysname+'Down'].SetBinContent(ibx,iby,h.GetBinContent(ibx,iby)*(rewerror1_['Down'][iby-1]))
                        hnames[key[i].GetName()+'_'+sysname+'Down'].SetBinError(ibx,iby,h.GetBinError(ibx,iby)*(rewerror1_['Down'][iby-1]))
                hnames[key[i].GetName()+'_'+sysname+'Up']=hnames[key[i].GetName()+'_'+sysname+'Up'].ProjectionX()
                hnames[key[i].GetName()+'_'+sysname+'Down']=hnames[key[i].GetName()+'_'+sysname+'Down'].ProjectionX()
                hnames[key[i].GetName()+'_'+sysname+'Up'].SetName(key[i].GetName()+'_'+sysname+'Up')
                hnames[key[i].GetName()+'_'+sysname+'Down'].SetName(key[i].GetName()+'_'+sysname+'Down')
                #CMS_BRewError2_13TeV_2018 left right
                sysname = 'CMS_BRewError2_2018'
                key2.append(key[i].GetName()+'_'+sysname+'Up')
                key2.append(key[i].GetName()+'_'+sysname+'Down')
                hnames[key[i].GetName()+'_'+sysname+'Up']=r.TH2D(key[i].GetName()+'_'+sysname+'Up', sysname+'Up',len(binning)-1,array('d',binning), len(rewbinning2)-1,array('d',rewbinning2))
                hnames[key[i].GetName()+'_'+sysname+'Down']=r.TH2D(key[i].GetName()+'_'+sysname+'Down', sysname+'Down',len(binning)-1,array('d',binning), len(rewbinning2)-1,array('d',rewbinning2))
                for iby in range(1,h.GetNbinsY()+1):
                    for ibx in range(1,h.GetNbinsX()+1):
                        hnames[key[i].GetName()+'_'+sysname+'Up'].SetBinContent(ibx,iby,h.GetBinContent(ibx,iby)*(rewerror2_['Up'][iby-1]))
                        hnames[key[i].GetName()+'_'+sysname+'Up'].SetBinError(ibx,iby,h.GetBinError(ibx,iby)*(rewerror2_['Up'][iby-1]))
                        hnames[key[i].GetName()+'_'+sysname+'Down'].SetBinContent(ibx,iby,h.GetBinContent(ibx,iby)*(rewerror2_['Down'][iby-1]))
                        hnames[key[i].GetName()+'_'+sysname+'Down'].SetBinError(ibx,iby,h.GetBinError(ibx,iby)*(rewerror2_['Down'][iby-1]))
                hnames[key[i].GetName()+'_'+sysname+'Up']=hnames[key[i].GetName()+'_'+sysname+'Up'].ProjectionX()
                hnames[key[i].GetName()+'_'+sysname+'Down']=hnames[key[i].GetName()+'_'+sysname+'Down'].ProjectionX()
                hnames[key[i].GetName()+'_'+sysname+'Up'].SetName(key[i].GetName()+'_'+sysname+'Up')
                hnames[key[i].GetName()+'_'+sysname+'Down'].SetName(key[i].GetName()+'_'+sysname+'Down')

            # Do reweighting for normal
            for iby in range(1,h.GetNbinsY()+1):
                for ibx in range(1,h.GetNbinsX()+1):
                    h.SetBinContent(ibx,iby,h.GetBinContent(ibx,iby)*rewvalue2[iby-1])
                    h.SetBinError(ibx,iby,h.GetBinError(ibx,iby)*rewvalue2[iby-1])
            hnames[key[i].GetName()] = h.ProjectionX()
            hnames[key[i].GetName()].SetName(key[i].GetName())
            print(key[i].GetName())

    fout = r.TFile(d.replace('_raw',''), "RECREATE")
    fout.cd()
    for i in range(len(key2)):
        #print(i,key2[i])
        hnames[key2[i]].Scale(scaleFactorforAll)
        hnames[key2[i]].Write("",r.TFile.kOverwrite)
    if 'data_obs' not in hnames.keys():
        #h0 = r.TH1D("data_obs", "nominal",1,0,1)
        h0 = r.TH1D("data_obs", "nominal",len(binning)-1,array('d',binning))
        h0.Write()
    fout.Close()

os.system("rm "+out+'/*_raw.root')



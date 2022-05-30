from condor_config import doResolved, doBoosted, doSemiBoosted, giveOverlapToBoosted, year, doVZ, doMjj2016, doMjj2017, doMjj2018

resolvedSplit = "&&fourResolvedJets"
boostedSplit = "&&twoMergedJet"
semiboostedSplit = "&&oneMergedJet"

channelDict = {}

topo0 = "&&isResolved&&!isBoosted&&!isSemiBoosted" # Resolved only
topo2 = "&&isSemiBoosted&&!isResolved" # SemiBoosted only
topo4 = "&&isBoosted&&!isResolved" # Boosted only
topo02 = "&&isResolved&&!isBoosted" # Resolved

#######################
#       Resolved      #
#######################

Zmasswindow = ' && (V_mass>75 && V_mass<105)'
Zmasswindow_TT_CR = ' && !(V_mass>75 && V_mass<105)'

KlBDT_SMcouplingbin = " && CMS_vhh_zll_bdt_Kl_cat_13TeV>0.0"
KlBDT_Strongcouplingbin = " && CMS_vhh_zll_bdt_Kl_cat_13TeV<-0.0"

cate_bdt_High = "RBDT_cate_kl20VSkl0>0"
cate_bdt_Low = "RBDT_cate_kl20VSkl0<=0"
cate_bdt_High = "wlnRBDT_cate_kl20VSkl0>0"
cate_bdt_Low = "wlnRBDT_cate_kl20VSkl0<=0"
topology_sel = 'isResolved&&!isBoosted'
topology_sel2 = ' && isResolved'

SR_3b = '&&VHH_rHH<25'
SR_4b = '&&VHH_rHH<25'

Resolved_channel = {
    
#     "R_Zll_Klbdt_SM_3b_bin_SR_Z": {
#         "channelName": "Zll",
#         "cutstring": "(isZee || isZmm) " + SR_3b +topology_sel2 + Zmasswindow + KlBDT_SMcouplingbin,
#         "doEven": 1, 
#         "doRebin": 1, 
#         "doVV": 0, 
#         "drawFromNom": 1, 
#         "nBins": 9, 
#         "varNames": ["(CMS_vhh_bdt_Kl_SM_SvB_13TeV+1)/2"],
#         "xlow": "0",
#         "xhigh": "1",
#     },
    
#     "R_Zll_Klbdt_High_3b_bin_SR_Z": {
#         "channelName": "Zll",
#         "cutstring": "(isZee || isZmm) " + SR_3b + topology_sel2 + Zmasswindow + KlBDT_Strongcouplingbin,
#         "doEven": 1,
#         "doRebin": 1,
#         "doVV": 0, 
#         "drawFromNom": 1, 
#         "nBins": 5, 
#         "varNames": ["(CMS_vhh_bdt_Kl_High_SvB_13TeV+1)/2"],
#         "xlow": "0",
#         "xhigh": "1",
#     },
    
#     "R_Zll_Klbdt_SM_4b_bin_SR_Z": {
#         "channelName": "Zll",
#         "cutstring": "(isZee || isZmm) " + SR_4b +topology_sel2 + Zmasswindow + KlBDT_SMcouplingbin,
#         "doEven": 1, 
#         "doRebin": 1, 
#         "doVV": 0, 
#         "drawFromNom": 1, 
#         "nBins": 5, 
#         "varNames": ["(CMS_vhh_bdt_Kl_SM_SvB_13TeV+1)/2"],
#         "xlow": "0",
#         "xhigh": "1",
#     },
    
    "R_Zll_Klbdt_High_4b_bin_SR_Z": {
        "channelName": "Zll",
        "cutstring": "(isZee || isZmm) " + SR_4b + topology_sel2 + Zmasswindow + KlBDT_Strongcouplingbin,
        "doEven": 1, 
        "doRebin": 1, 
        "doVV": 0, 
        "drawFromNom": 1, 
        "nBins": 3, 
        "varNames": ["(CMS_vhh_bdt_Kl_High_SvB_13TeV+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
}




#######################
#       Boosted      #
#######################

HP = 'VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.98&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.98'
MP = 'VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.94&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.94 && !(VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.98&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.98)'
LP = 'VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.9&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.9 && !(VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.94&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.94)'
VR = 'VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.8&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.8 && !(VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.9&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.9)'
OT = '!(VHHFatJetCand_ParticleNetMD_bbvsQCD[0]>=0.8&&VHHFatJetCand_ParticleNetMD_bbvsQCD[1]>=0.8)'

Boost_cut = '&&(VHHFatJet_mjj>=300)&& (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9)'

Boosted_channel = {
    "wenuBBDT_svb_HMP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_HMP+1)/2"],
        "cutstring": "isWenu&& isBoosted&& VHHFatJet_mjj>=300 && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWenu&& isBoosted&& VHHFatJet_mjj>=300 && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.90 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(wlnBBDT_svb_HMP+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "wmunuBBDT_svb_HMP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_HMP+1)/2"],
        "cutstring": "isWmunu&& isBoosted&& VHHFatJet_mjj>=300 && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWmunu&& isBoosted&& VHHFatJet_mjj>=300 && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.90 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(wlnBBDT_svb_HMP+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "wenuBBDT_svb_LP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_LP+1)/2"],
        "cutstring": "isWenu&& isBoosted&& VHHFatJet_mjj>=300 && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWenu&& isBoosted&& VHHFatJet_mjj>=300 && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.90 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(wlnBBDT_svb_LP+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "wmunuBBDT_svb_LP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_LP+1)/2"],
        "cutstring": "isWmunu&& isBoosted&& VHHFatJet_mjj>=300 && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWmunu&& isBoosted&& VHHFatJet_mjj>=300 && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.90 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(wlnBBDT_svb_LP+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
}


if doResolved:
    channelDict.update(Resolved_channel)

if doBoosted:
    channelDict.update(Boosted_channel) 








from condor_config import doResolved, doBoosted, doSemiBoosted, giveOverlapToBoosted, year, doVZ, doMjj2016, doMjj2017, doMjj2018



channelDict = {}

topo0 = "&&isResolved&&!isBoosted&&!isSemiBoosted" # Resolved only
topo2 = "&&isSemiBoosted&&!isResolved" # SemiBoosted only
topo4 = "&&isBoosted&&!isResolved" # Boosted only
topo02 = "&&isResolved&&!isBoosted" # Resolved

#######################
#       Resolved      #
#######################

#Wln Resolved 
SR = '&&VHH_rHH<25 && VHH_nBJets>2'
CR = '&&VHH_rHH>=25 && VHH_rHH<50&&VHH_rHH>=0 && VHH_nBJets>2'

cate_bdt_High = "RBDT_cate_kl20VSkl0>0"
cate_bdt_Low = "RBDT_cate_kl20VSkl0<=0"
topology_sel = 'isResolved'

Resolved_channel = {
    "RBDT_Wenu_High": {
        "channelName": "Wln",
        "cutstring": "isWenu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20", 
        "varNames": ["(wlnRBDT_svb_Highscore+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Wenu_Low": {
        "channelName": "Wln",
        "cutstring": "isWenu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(wlnRBDT_svb_Lowscore+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Wmunu_High": {
        "channelName": "Wln",
        "cutstring": "isWmunu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(wlnRBDT_svb_Highscore+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Wmunu_Low": {
        "channelName": "Wln",
        "cutstring": "isWmunu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(wlnRBDT_svb_Lowscore+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Znn_High": {
        "channelName": "Znn",
        "cutstring": "isZnn&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(znnRBDT_svb_Highscore+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Znn_Low": {
        "channelName": "Znn",
        "cutstring": "isZnn&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 1,
        "nBins": "20",
        "varNames": ["(znnRBDT_svb_Lowscore+1)/2"],
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






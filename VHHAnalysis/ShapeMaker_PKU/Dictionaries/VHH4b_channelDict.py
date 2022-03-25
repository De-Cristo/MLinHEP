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

cate_bdt_High = "wlnRBDT_cate_kl20VSkl0_v2>0"
cate_bdt_Low = "wlnRBDT_cate_kl20VSkl0_v2<=0"
topology_sel = 'isResolved&&!isBoosted&&weight_PU<9000'
cate_bdt_High_znn = "znnRBDT_cate_kl20VSkl0_v2>0"
cate_bdt_Low_znn = "znnRBDT_cate_kl20VSkl0_v2<=0"


Resolved_channel = {
    "RBDT_Wenu_High": {
        "channelName": "Wln",
        "cutstring": "isWenu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "20", 
        "varNames": ["(wlnRBDT_svb_v_Highscore_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Wenu_Low": {
        "channelName": "Wln",
        "cutstring": "isWenu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "20",
        "varNames": ["(wlnRBDT_svb_v_Lowscore_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Wmunu_High": {
        "channelName": "Wln",
        "cutstring": "isWmunu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "20",
        "varNames": ["(wlnRBDT_svb_v_Highscore_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Wmunu_Low": {
        "channelName": "Wln",
        "cutstring": "isWmunu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "20",
        "varNames": ["(wlnRBDT_svb_v_Lowscore_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },


#    "RBDT_lep_Wenu_High": {
#        "channelName": "Wln",
#        "cutstring": "isWenu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High,
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnRBDT_svb_lep_Highscore_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "RBDT_lep_Wenu_Low": {
#        "channelName": "Wln",
#        "cutstring": "isWenu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low,
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnRBDT_svb_lep_Lowscore_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "RBDT_lep_Wmunu_High": {
#        "channelName": "Wln",
#        "cutstring": "isWmunu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High,
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnRBDT_svb_lep_Highscore_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "RBDT_lep_Wmunu_Low": {
#        "channelName": "Wln",
#        "cutstring": "isWmunu&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low,
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnRBDT_svb_lep_Lowscore_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },

    "RBDT_Znn_High": {
        "channelName": "Znn",
        "cutstring": "isZnn&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_High_znn,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(znnRBDT_svb_Highscore_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "RBDT_Znn_Low": {
        "channelName": "Znn",
        "cutstring": "isZnn&&"+topology_sel+"&&VHH_rHH<50&&VHH_rHH>=0&&VHH_nBJets>2&&"+cate_bdt_Low_znn,
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(znnRBDT_svb_Lowscore_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },

}




#######################
#       Boosted      #
#######################

HP = 'VHHFatJet1_ParticleNetMD_bbvsQCD>=0.98&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.98'
MP = 'VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94 && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.98&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.98)'
HMP = 'VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94'
LP = 'VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9 && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)'
VR = 'VHHFatJet1_ParticleNetMD_bbvsQCD>=0.8&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8 && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9)'
OT = '!(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.8&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)'


topology_sel = 'isBoosted&& VHHFatJet_mjj>=300&&weight_PU<9000'
# FailReweight and Bpriority
Boosted_channel = {

#    "wenuBBDT_lep_svb_HMP": {
#        "channelName": "Wln",
#        "doReweight": 1,
#        "rewvarNames": ["(wlnBBDT_rew_lep_HMP_v2+1)/2"],
#        "cutstring": "isWenu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWenu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_lep_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "wenuBBDT_lep_svb_LP": {
#        "channelName": "Wln",
#        "doReweight": 1,
#        "rewvarNames": ["(wlnBBDT_rew_lep_LP_v2+1)/2"],
#        "cutstring": "isWenu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWenu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_lep_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "wmunuBBDT_lep_svb_HMP": {
#        "channelName": "Wln",
#        "doReweight": 1,
#        "rewvarNames": ["(wlnBBDT_rew_lep_HMP_v2+1)/2"],
#        "cutstring": "isWmunu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWmunu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_lep_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "wmunuBBDT_lep_svb_LP": {
#        "channelName": "Wln",
#        "doReweight": 1,
#        "rewvarNames": ["(wlnBBDT_rew_lep_LP_v2+1)/2"],
#        "cutstring": "isWmunu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWmunu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_lep_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },


    "wenuBBDT_v_svb_HMP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_v_HMP_v2+1)/2"],
        "cutstring": "isWenu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWenu&& "+topology_sel+"&& !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(wlnBBDT_SvB_v_HMP_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "wenuBBDT_v_svb_LP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_v_LP_v2+1)/2"],
        "cutstring": "isWenu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWenu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(wlnBBDT_SvB_v_LP_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "wmunuBBDT_v_svb_HMP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_v_HMP_v2+1)/2"],
        "cutstring": "isWmunu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWmunu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(wlnBBDT_SvB_v_HMP_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "wmunuBBDT_v_svb_LP": {
        "channelName": "Wln",
        "doReweight": 1,
        "rewvarNames": ["(wlnBBDT_rew_v_LP_v2+1)/2"],
        "cutstring": "isWmunu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isWmunu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(wlnBBDT_SvB_v_LP_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },

    "znnBBDT_svb_HMP": {
        "channelName": "Znn",
        "doReweight": 1,
        "rewvarNames": ["(znnBBDT_rew_HMP_v2+1)/2"],
        "cutstring": "isZnn&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isZnn&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(znnBBDT_SvB_HMP_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
    "znnBBDT_svb_LP": {
        "channelName": "Znn",
        "doReweight": 1,
        "rewvarNames": ["(znnBBDT_rew_LP_v2+1)/2"],
        "cutstring": "isZnn&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
        "failcutstring": "isZnn&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
        "doEven": 0,
        "doRebin": 1,
        "doVV": 0,
        "drawFromNom": 0,
        "nBins": "10",
        "varNames": ["(znnBBDT_SvB_LP_v2+1)/2"],
        "xlow": "0",
        "xhigh": "1",
    },
}

# Passed and Bpriority
#Boosted_channel = {
#    "wenuBBDT_v_svb_HMP": {
#        "channelName": "Wln",
#        "doReweight": 0,
#        "rewvarNames": ["(wlnBBDT_rew_v_HMP_v2+1)/2"],
#        "cutstring": "isWenu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWenu&& "+topology_sel+"&& !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_v_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "wenuBBDT_v_svb_LP": {
#        "channelName": "Wln",
#        "doReweight": 0,
#        "rewvarNames": ["(wlnBBDT_rew_v_LP_v2+1)/2"],
#        "cutstring": "isWenu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWenu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_v_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "wmunuBBDT_v_svb_HMP": {
#        "channelName": "Wln",
#        "doReweight": 0,
#        "rewvarNames": ["(wlnBBDT_rew_v_HMP_v2+1)/2"],
#        "cutstring": "isWmunu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWmunu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_v_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "wmunuBBDT_v_svb_LP": {
#        "channelName": "Wln",
#        "doReweight": 0,
#        "rewvarNames": ["(wlnBBDT_rew_v_LP_v2+1)/2"],
#        "cutstring": "isWmunu&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isWmunu&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(wlnBBDT_SvB_v_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#
#    "znnBBDT_svb_HMP": {
#        "channelName": "Znn",
#        "doReweight": 0,
#        "rewvarNames": ["(znnBBDT_rew_HMP_v2+1)/2"],
#        "cutstring": "isZnn&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isZnn&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(znnBBDT_SvB_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "znnBBDT_svb_LP": {
#        "channelName": "Znn",
#        "doReweight": 0,
#        "rewvarNames": ["(znnBBDT_rew_LP_v2+1)/2"],
#        "cutstring": "isZnn&& "+topology_sel+" && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.94&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.94)", # passcutstring
#        "failcutstring": "isZnn&& "+topology_sel+" && !(VHHFatJet1_ParticleNetMD_bbvsQCD>=0.9&&VHHFatJet2_ParticleNetMD_bbvsQCD>=0.9) && (VHHFatJet1_ParticleNetMD_bbvsQCD>=0.80 || VHHFatJet2_ParticleNetMD_bbvsQCD>=0.8)",
#        "doEven": 0,
#        "doRebin": 1,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "20",
#        "varNames": ["(znnBBDT_SvB_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#}

# Passed and R priority
#topology_sel = 'isBoosted&&!isResolved&& VHHFatJet_mjj>=300&&weight_PU<9000'
#
#Boosted_channel = {
### Boosted counting
#    "BBDT_Znn_HMP_1bin": {
#        "channelName": "Znn",
#        "cutstring": "isZnn&&"+topology_sel+"&&"+HMP,
#        "doEven": 0,
#        "doRebin": 0,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "1",
#        "varNames": ["(znnBBDT_SvB_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "BBDT_Znn_LP_1bin": {
#        "channelName": "Znn",
#        "cutstring": "isZnn&&"+topology_sel+"&&"+LP,
#        "doEven": 0,
#        "doRebin": 0,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "1",
#        "varNames": ["(znnBBDT_SvB_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "BBDT_Wenu_HMP_1bin": {
#        "channelName": "Wln",
#        "cutstring": "isWenu&&"+topology_sel+"&&"+HMP,
#        "doEven": 0,
#        "doRebin": 0,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "1",
#        "varNames": ["(wlnBBDT_SvB_v_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "BBDT_Wenu_LP_1bin": {
#        "channelName": "Wln",
#        "cutstring": "isWenu&&"+topology_sel+"&&"+LP,
#        "doEven": 0,
#        "doRebin": 0,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "1",
#        "varNames": ["(wlnBBDT_SvB_v_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "BBDT_Wmunu_HMP_1bin": {
#        "channelName": "Wln",
#        "cutstring": "isWmunu&&"+topology_sel+"&&"+HMP,
#        "doEven": 0,
#        "doRebin": 0,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "1",
#        "varNames": ["(wlnBBDT_SvB_v_HMP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#    "BBDT_Wmunu_LP_1bin": {
#        "channelName": "Wln",
#        "cutstring": "isWmunu&&"+topology_sel+"&&"+LP,
#        "doEven": 0,
#        "doRebin": 0,
#        "doVV": 0,
#        "drawFromNom": 0,
#        "nBins": "1",
#        "varNames": ["(wlnBBDT_SvB_v_LP_v2+1)/2"],
#        "xlow": "0",
#        "xhigh": "1",
#    },
#}

if doResolved:
    channelDict.update(Resolved_channel)

if doBoosted:
    channelDict.update(Boosted_channel)






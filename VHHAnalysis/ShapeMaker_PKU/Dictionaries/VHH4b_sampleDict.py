import sys
sys.path.append('..')
from condor_config import year,doJEROnly

All_sampleDict = {
    "CMS_pileup_"+year: ["shape","1.0","weight_PU", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]], # Pileup
#     "CMS_res_j_"+year: ["shape","1.0","1.0","JER", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]], # JER
    # JES
#     "CMS_scale_j_Abs": ["shape","1.0","1.0","MergedAbsolute", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_Abs_"+year: ["shape","1.0","1.0","MergedAbsolute_"+year,["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_BBEC1": ["shape","1.0","1.0","MergedBBEC1",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_BBEC1_"+year: ["shape","1.0","1.0","MergedBBEC1_"+year,["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_EC2": ["shape","1.0","1.0","MergedEC2",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_EC2_"+year: ["shape","1.0","1.0","MergedEC2_"+year,["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_FlavQCD": ["shape","1.0","1.0","MergedFlavorQCD",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_HF": ["shape","1.0","1.0","MergedHF",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_HF_"+year: ["shape","1.0","1.0","MergedHF_"+year,["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_RelBal": ["shape","1.0","1.0","MergedRelativeBal",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_scale_j_RelSample_"+year: ["shape","1.0","1.0","MergedRelativeSample_"+year,["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    # MSD JMS/JMR
#     "CMS_MSD_JMS_"+year: ["shape","1.0","1.0","MSD_JMS", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
#     "CMS_MSD_JMR_"+year: ["shape","1.0","1.0","MSD_JMR", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],

    # B-tag SF uncertainties
    # Correlate across years:
    "CMS_btag_HF_2016_2017_2018":["shape","1.0","bTagWeight_HF",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_btag_LF_2016_2017_2018":["shape","1.0","bTagWeight_LF",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_btag_cferr1_2016_2017_2018":["shape","1.0","bTagWeight_cErr1",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_btag_cferr2_2016_2017_2018":["shape","1.0","bTagWeight_cErr2",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    # Decorrelated:
    "CMS_btag_hfstats1_"+year:["shape","1.0","bTagWeight_HFStats1",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_btag_hfstats2_"+year:["shape","1.0","bTagWeight_HFStats2",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_btag_lfstats1_"+year:["shape","1.0","bTagWeight_LFStats1",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_btag_lfstats2_"+year:["shape","1.0","bTagWeight_LFStats2",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_btag_jes_"+year:["shape","1.0","bTagWeight_JES",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_PNet_"+year:["shape","1.0","PNetWeight",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
}

Zll_sampleDict = {
    "CMS_DYNLO_P0_": ["shape","1.0","VJetsNLOvsLOWeight_p0",["DY"]],
    "CMS_DYNLO_P1_": ["shape","1.0","VJetsNLOvsLOWeight_p1",["DY"]],
    "CMS_eff_m_"+year: ["shape","1.0","Lep_SF",["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
}

Znn_sampleDict = {
    "CMS_unclusteredEnergy_"+year: ["shape","1.0","1.0","unclustEn", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_eff_MET_"+year: ["shape","1.0","weight_mettrigSF", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
}

Wln_sampleDict = {
    "CMS_unclusteredEnergy_"+year: ["shape","1.0","1.0","unclustEn", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
    "CMS_eff_m_"+year: ["shape","1.0","Lep_SF", ["VHH_CV_1_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_20_hbbhbb","VHH_CV_1_C2V_1_kl_2_hbbhbb","VHH_CV_0p5_C2V_1_kl_1_hbbhbb","VHH_CV_1p5_C2V_1_kl_1_hbbhbb","VHH_CV_1_C2V_0_kl_1_hbbhbb","VHH_CV_1_C2V_2_kl_1_hbbhbb","VHH_CV_1_C2V_1_kl_0_hbbhbb","DY","s_Top","TT","TTB","TTV","ttH"]],
}

for sampleDict in All_sampleDict.keys():
    Zll_sampleDict[sampleDict] = All_sampleDict[sampleDict]
    Znn_sampleDict[sampleDict] = All_sampleDict[sampleDict]
    Wln_sampleDict[sampleDict] =All_sampleDict[sampleDict]

if doJEROnly:
    for sampleDict in [Znn_sampleDict,Wln_sampleDict,Zll_sampleDict]:
        for syst in sampleDict.keys():
            sampleDict.pop(syst)




analysis_branches = {
    'isZee','isZmm','isZnn','IsttB', 'VHH_nBJets',\
    'VHH_H1_pT', 'VHH_H2_e','VHH_H2_eta',\
    'VHH_H2_e','VHH_H2_eta',\
    'VHH_HH_m', 'VHH_HH_e', 'VHH_HH_eta',\
    'V_pt','V_mass',\
    'VHH_V_H2_dPhi', 'VHH_V_HH_dPhi',\
    'VHH_HH_deta', 'VHH_HH_dR',\
    'weight','VHH_rHH','VHH_H1_BJet1_btag','VHH_H1_BJet2_btag','VHH_H2_BJet1_btag','VHH_H2_BJet2_btag','intWeight','benPlusHTWeight'
}

file_list_for_TT      = ['TT_AllHadronic','TT_DiLep_NoPSWeights','TT_SingleLep']
file_list_for_ttbb    = ['ttbb_AllHadronic','ttbb_DiLep','ttbb_SingleLep']

file_list_DY          = ['DYToLL_M10-50_Inc_madgraph','DYToLL_M-50_Inc_madgraph',\
                         'DYToLL_M-50_HT70to100_madgraph','DYToLL_M-50_HT100to200_madgraph',\
                         'DYToLL_M-50_HT200to400_madgraph','DYToLL_M-50_HT400to600_madgraph',\
                         'DYToLL_M-50_HT600to800_madgraph','DYToLL_M-50_HT800to1200_madgraph',\
                         'DYToLL_M-50_HT1200to2500_madgraph','DYToLL_M-50_HT2500toInf_madgraph']

file_list_DY_NLO      = ['DYToLL_M-50_amcatnloFXFX','DYToLL_M-50_Pt-100To250_amcatnloFXFX',\
                         'DYToLL_M-50_Pt-250To400_amcatnloFXFX','DYToLL_M-50_Pt-400To650_amcatnloFXFX',\
                         'DYToLL_M-50_Pt-650ToInf_amcatnloFXFX','DYToLL_M-50_Pt-50To100_amcatnloFXFX']

file_list_ZHH         = ['ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0',\
                         'ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0','ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0',\
                         'ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0']

file_list_Other       = ['ST_s-c_4f_lep','ST_t-channel_eleDecays','ST_t-channel_muDecays',\
                         'ST_t-channel_tauDecays','ST_tW_antitop_5f_noFullHad',\
                         'ST_tW_top_5f_noFullHad',\
                         'ttHTobb_M125','TTWLNuJets','TTWQQJets','TTZLLNuNuJets','TTZQQJets']

file_list_Data        = ['Run2018_DoubleMu_ReMiniAOD','Run2018_EG_ReMiniAOD','Run2018_MET_MiniAOD']

rHH_region_dict = {
        'rHH_SR' : "VHH_rHH<25",
        'rHH_CR' : "VHH_rHH>25 && VHH_rHH<50",
        'rHH_SB' : "VHH_rHH>50",
}

Zmass_region_dict = {
        'TT_CR'   : "V_mass<75 || V_mass>105",
        'Z_mass'  : "V_mass>75 && V_mass<105",
}

btag_multiplicity_dict = {
        'two_btag'   : "VHH_nBJets == 2",
        'three_btag' : "VHH_nBJets == 3",
        'four_btag'  : "VHH_nBJets == 4",
}

lepton_channel_dict = {
        'Zll'   : "(isZee || isZmm)",
        'Znn'   : "isZnn",
}

TT_MEb_dict = {
    'IsttB_TT'      : "IsttB == 0",
    'IsttB_TTB'     : "IsttB > 0",
}

# These path names are defined manually.

VHH_Sample_path = 'Pre_SlimmedSample_temp'
VHH_Signal_path = 'Pre_SlimmedSignal'

VBF_Sample_path = ''
VBF_Signal_path = ''

GGF_Sample_path = ''
GGF_Signal_path = ''

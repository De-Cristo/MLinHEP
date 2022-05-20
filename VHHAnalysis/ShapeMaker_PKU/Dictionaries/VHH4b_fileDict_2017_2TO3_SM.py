# Scale factor doesn't work here

DY_fileDict = {
    "DYToLL_M-50_Inc_madgraph": [
        ["DY", "(sampleIndex/100)==120&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_Inc_madgraph"]
    ],
    
    "DYToLL_M-50_HT70to100_madgraph": [
        ["DY", "(sampleIndex/100)==110&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT70to100_madgraph"]
    ],
    
    "DYToLL_M-50_HT100to200_madgraph": [
        ["DY", "(sampleIndex/100)==111&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT100to200_madgraph"]
    ], 
    
    "DYToLL_M-50_HT200to400_madgraph": [
        ["DY", "(sampleIndex/100)==112&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT200to400_madgraph"]
    ],
    
    "DYToLL_M-50_HT400to600_madgraph": [
        ["DY", "(sampleIndex/100)==113&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT400to600_madgraph"]
    ],
    
    "DYToLL_M-50_HT600to800_madgraph": [
        ["DY", "(sampleIndex/100)==114&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT600to800_madgraph"]
    ],
    
    "DYToLL_M-50_HT800to1200_madgraph": [
        ["DY", "(sampleIndex/100)==115&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT800to1200_madgraph"]
    ],
    
    "DYToLL_M-50_HT1200to2500_madgraph": [
        ["DY", "(sampleIndex/100)==116&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT1200to2500_madgraph"]
    ],
    
    "DYToLL_M-50_HT2500toInf_madgraph": [
        ["DY", "(sampleIndex/100)==117&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M-50_HT2500toInf_madgraph"]
    ],
    
    "DYToLL_M10-50_Inc_madgraph": [
        ["DY", "(sampleIndex/100)==119&&weight>0&&VHH_nBJets==2", 1.254 * 148.178/1394.181 , "DYToLL_M10-50_Inc_madgraph"]
    ]
}

top_fileDict = {
    "ST_t-channel_eleDecays": [
        ["s_Top", "sampleIndex==19&&weight>0&&VHH_nBJets==3", 1.0, "ST_t-channel_eleDecays"]
    ], 
    "ST_t-channel_muDecays": [
        ["s_Top", "sampleIndex==18&&weight>0&&VHH_nBJets==3", 1.0, "ST_t-channel_muDecays"]
    ], 
    "ST_t-channel_tauDecays": [
        ["s_Top", "sampleIndex==17&&weight>0&&VHH_nBJets==3", 1.0, "ST_t-channel_tauDecays"]
    ], 
    "ST_tW_antitop_5f_noFullHad": [
        ["s_Top", "sampleIndex==21&&weight>0&&VHH_nBJets==3", 1.0, "ST_tW_antitop_5f_noFullHad"]
    ],
    "ST_tW_top_5f_noFullHad": [
        ["s_Top", "sampleIndex==20&&weight>0&&VHH_nBJets==3", 1.0, "ST_tW_top_5f_noFullHad"]
    ],
    "ST_s-c_4f_lep": [
        ["s_Top", "sampleIndex==16&&weight>0&&VHH_nBJets==3", 1.0, "ST_s-c_4f_lep"]
    ],
    

    "TT_AllHadronic": [
        ["TT", "sampleIndex==212&&IsttB==0&&weight>0&&VHH_nBJets==2 ", 0.749 * 261.143/3005.955, "TT_AllHadronic"]
    ], 
    "TT_DiLep_NoPSWeights": [
        ["TT", "sampleIndex==202&&IsttB==0&&weight>0&&VHH_nBJets==2 ", 0.749 * 261.143/3005.955, "TT_DiLep_NoPSWeights"]
    ], 
    "TT_SingleLep": [
        ["TT", "sampleIndex==203&&IsttB==0&&weight>0&&VHH_nBJets==2 ", 0.749 * 261.143/3005.955, "TT_SingleLep"]
    ],

    "TTBB_AllHadronic": [
        ["TTB", "sampleIndex==26&&IsttB>0&&weight>0&&VHH_nBJets==2 ", 0.749 * 86.075/94.784, "TTBB_AllHadronic"]
    ], 
    "TTBB_DiLep": [
        ["TTB", "sampleIndex==25&&IsttB>0&&weight>0&&VHH_nBJets==2 ", 0.749 * 86.075/94.784, "TTBB_DiLep"]
    ], 
    "TTBB_SingleLep": [
        ["TTB", "sampleIndex==24&&IsttB>0&&weight>0&&VHH_nBJets==2 ", 0.749 * 86.075/94.784, "TTBB_SingleLep"]
    ],
        
    "TTWLNuJets": [
        ["TTV","sampleIndex==205&&weight>0&&VHH_nBJets==3" , 1.0, "TTWLNuJets"]
    ], 
    "TTWQQJets": [
        ["TTV","sampleIndex==215&&weight>0&&VHH_nBJets==3" , 1.0, "TTWQQJets"]
    ],    
    "TTZLLNuNuJets": [
        ["TTV","sampleIndex==216&&weight>0&&VHH_nBJets==3" , 1.0, "TTZLLNuNuJets"]
    ], 
    "TTZQQJets": [
        ["TTV","sampleIndex==217&&weight>0&&VHH_nBJets==3" , 1.0, "TTZQQJets"]
    ],    
    "ttHTobb_M125": [
        ["ttH","sampleIndex==22&&weight>0&&VHH_nBJets==3" , 1.0, "ttHTobb_M125"]
    ], 

}
 
WJets_fileDict = {
}
from condor_config import doMjj2016,doMjj2017,doMjj2018
if not (doMjj2016==True or doMjj2017==True or doMjj2018==True):
    print("doMjj201x")

else:
    WHH4b_fileDict={
        "WHHTo4BNLO_CV_1_0_C2V_1_0_C3_1_0": [
                ["VHH_CV_1_C2V_1_kl_1_hbbhbb", "sampleIndex==-3101010", 1.0, "WHHTo4BNLO_CV_1_0_C2V_1_0_C3_1_0"]
            ],
        "WHHTo4B_CV_1_0_C2V_1_0_C3_1_0": [
                ["VHH_CV_1_C2V_1_kl_1_hbbhbb", "sampleIndex==-1101010", 1.0, "WHHTo4B_CV_1_0_C2V_1_0_C3_1_0"] 
            ], 
        "WHHTo4B_CV_0_5_C2V_1_0_C3_1_0": [
                ["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "sampleIndex==-1051010", 1.0, "WHHTo4B_CV_0_5_C2V_1_0_C3_1_0"] 
            ],
        "WHHTo4B_CV_1_5_C2V_1_0_C3_1_0": [
                ["VHH_CV_1p5_C2V_1_kl_1_hbbhbb", "sampleIndex==-1151010", 1.0, "WHHTo4B_CV_1_5_C2V_1_0_C3_1_0"] 
            ],
        "WHHTo4B_CV_1_0_C2V_0_0_C3_1_0": [
                ["VHH_CV_1_C2V_0_kl_1_hbbhbb", "sampleIndex==-1100010", 1.0, "WHHTo4B_CV_1_0_C2V_0_0_C3_1_0"] 
            ],
        "WHHTo4B_CV_1_0_C2V_2_0_C3_1_0": [
                ["VHH_CV_1_C2V_2_kl_1_hbbhbb", "sampleIndex==-1102010", 1.0, "WHHTo4B_CV_1_0_C2V_2_0_C3_1_0"] 
            ],
        "WHHTo4B_CV_1_0_C2V_1_0_C3_0_0": [
                ["VHH_CV_1_C2V_1_kl_0_hbbhbb", "sampleIndex==-1101000", 1.0, "WHHTo4B_CV_1_0_C2V_1_0_C3_0_0"] 
            ],
        "WHHTo4B_CV_1_0_C2V_1_0_C3_2_0": [
                ["VHH_CV_1_C2V_1_kl_2_hbbhbb", "sampleIndex==-1101020", 1.0, "WHHTo4B_CV_1_0_C2V_1_0_C3_2_0"] 
            ],
        "WHHTo4B_CV_1_0_C2V_1_0_C3_20_0": [
                ["VHH_CV_1_C2V_1_kl_20_hbbhbb", "sampleIndex==-11010200", 1.0, "WHHTo4B_CV_1_0_C2V_1_0_C3_20_0"]
            ],
    }
    ZHH4b_fileDict={
        "ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0": [
                ["VHH_CV_1_C2V_1_kl_1_hbbhbb", "sampleIndex==-2101010&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0"] 
            ], 
        "ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0": [
                ["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "sampleIndex==-2051010&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0": [
                ["VHH_CV_1p5_C2V_1_kl_1_hbbhbb", "sampleIndex==-2151010&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0": [
                ["VHH_CV_1_C2V_0_kl_1_hbbhbb", "sampleIndex==-2100010&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0": [
                ["VHH_CV_1_C2V_2_kl_1_hbbhbb", "sampleIndex==-2102010&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0": [
                ["VHH_CV_1_C2V_1_kl_0_hbbhbb", "sampleIndex==-2101000&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0": [
                ["VHH_CV_1_C2V_1_kl_2_hbbhbb", "sampleIndex==-2101020&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0": [
                ["VHH_CV_1_C2V_1_kl_20_hbbhbb", "sampleIndex==-21010200&&weight>0&&VHH_nBJets==3 ", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0"] 
            ],
    }

Zll_fileDict={
}

Zll_fileDict.update(DY_fileDict)
Zll_fileDict.update(top_fileDict)
Zll_fileDict.update(WHH4b_fileDict)
Zll_fileDict.update(ZHH4b_fileDict)

Wln_fileDict = {}
#Wln_fileDict.update(ZnnJets_fileDict)
#Wln_fileDict.update(DY_fileDict)
#Wln_fileDict.update(WJets_fileDict)
Wln_fileDict.update(top_fileDict)
Wln_fileDict.update(WHH4b_fileDict)
Wln_fileDict.update(ZHH4b_fileDict)
#
Znn_fileDict = {}
Znn_fileDict.update(top_fileDict)
Znn_fileDict.update(WHH4b_fileDict)
Znn_fileDict.update(ZHH4b_fileDict)

#Znn_fileDict.update(ZnnJets_fileDict)
#Znn_fileDict.update(WJets_fileDict)
#Znn_fileDict.update(DY_fileDict)
#Znn_fileDict.update(top_fileDict)
#Znn_fileDict.update(QCD_fileDict)
#Znn_fileDict.update(VV_fileDict)
#Znn_fileDict.update(WHbb_fileDict)
#Znn_fileDict.update(ZnnHbb_fileDict)

import sys
sys.path.append('..')
from condor_config import year
YearSpecific_fileDict = {
    "2016":{   
        "Run2016pre_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_Ele_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_DoubleEle_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_MET_MiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_Ele_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_DoubleEle_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_MET_MiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
    },
    "2016pre":{   
        "Run2016pre_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_Ele_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_DoubleEle_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016pre_MET_MiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
    },
    
    "2016post":{   
        "Run2016post_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_Ele_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_DoubleEle_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016post_MET_MiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
    },
    
    "2017":{
        "Run2017_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_DoubleEle_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_Ele_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_MET_MiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
    },
    "2018":{
        "Run2018_EG_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2018_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2018_MET_MiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2018_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
    }
}

Wln_fileDict.update(YearSpecific_fileDict[year])
Znn_fileDict.update(YearSpecific_fileDict[year])
Zll_fileDict.update(YearSpecific_fileDict[year])

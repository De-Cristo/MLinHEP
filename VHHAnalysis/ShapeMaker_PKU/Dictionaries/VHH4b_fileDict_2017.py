# Scale factor doesn't work here

DY_fileDict = {
    "DYBJets-Pt100To200": [
        ["Zj0b_udsg", "(sampleIndex/100)==121&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "DYBJetsPt-100to200_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==121&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "DYBJetsPt-100to200_c"],
        ["Zj1b", "(sampleIndex/100)==121&&nGenStatus2bHadFinalAccept==1", 1.0, "DYBJetsPt-100to200_b"],
        ["Zj2b", "(sampleIndex/100)==121&&nGenStatus2bHadFinalAccept>1", 1.0, "DYBJetsPt-100to200_bb"],
    ],  
    "DYBJets-Pt200ToInf": [
        ["Zj0b_udsg", "(sampleIndex/100)==122&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "DYBJetsPt-200toInf_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==122&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "DYBJetsPt-200toInf_c"],
        ["Zj1b", "(sampleIndex/100)==122&&nGenStatus2bHadFinalAccept==1", 1.0, "DYBJetsPt-200toInf_b"],
        ["Zj2b", "(sampleIndex/100)==122&&nGenStatus2bHadFinalAccept>1", 1.0, "DYBJetsPt-200toInf_bb"],
    ],  
    "DYJets-BGenFilter-Pt100To200": [
        ["Zj0b_udsg", "(sampleIndex/100)==141&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "DYJets-BGenFilterPt-100to200_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==141&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "DYJets-BGenFilterPt-100to200_c"],
        ["Zj1b", "(sampleIndex/100)==141&&nGenStatus2bHadFinalAccept==1", 1.0, "DYJets-BGenFilterPt-100to200_b"],
        ["Zj2b", "(sampleIndex/100)==141&&nGenStatus2bHadFinalAccept>1", 1.0, "DYJets-BGenFilterPt-100to200_bb"],
    ],  
    "DYJets-BGenFilter-Pt200ToInf": [
        ["Zj0b_udsg", "(sampleIndex/100)==142&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "DYJets-BGenFilterPt-200toInf_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==142&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "DYJets-BGenFilterPt-200toInf_c"],
        ["Zj1b", "(sampleIndex/100)==142&&nGenStatus2bHadFinalAccept==1", 1.0, "DYJets-BGenFilterPt-200toInf_b"],
        ["Zj2b", "(sampleIndex/100)==142&&nGenStatus2bHadFinalAccept>1", 1.0, "DYJets-BGenFilterPt-200toInf_bb"],
    ],
    "DYToLL_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==110&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==110&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c"],
        ["Zj1b", "(sampleIndex/100)==110&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b"],
        ["Zj2b", "(sampleIndex/100)==110&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb"],
    ],
    "DYToLL_HT70to100_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==118&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT70To100"],
        ["Zj0b_c", "(sampleIndex/100)==118&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT70To100"],
        ["Zj1b", "(sampleIndex/100)==118&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT70To100"],
        ["Zj2b", "(sampleIndex/100)==118&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT70To100"],
    ],
    "DYToLL_HT100to200_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT100To200"],
        ["Zj0b_c", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT100To200"],
        ["Zj1b", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT100To200"],
        ["Zj2b", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT100To200"],
    ],  
    "DYToLL_HT1200to2500_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT1200To2500"],
        ["Zj0b_c", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT1200To2500"],
        ["Zj1b", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT1200To2500"],
        ["Zj2b", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT1200To2500"],
    ],
    "DYToLL_HT200to400_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT200To400"],
        ["Zj0b_c", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT200To400"],
        ["Zj1b", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT200To400"],
        ["Zj2b", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT200To400"],
    ],
    "DYToLL_HT2500toInf_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT2500ToInf"],
        ["Zj0b_c", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT2500ToInf"],
        ["Zj1b", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT2500ToInf"],
        ["Zj2b", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT2500ToInf"],
    ],
    "DYToLL_HT400to600_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT400To600"],
        ["Zj0b_c", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT400To600"],
        ["Zj1b", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT400To600"],
        ["Zj2b", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT400To600"],
    ],
    "DYToLL_HT600to800_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT600To800"],
        ["Zj0b_c", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT600To800"],
        ["Zj1b", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT600To800"],
        ["Zj2b", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT600To800"],
    ],
    "DYToLL_HT800to1200_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT800To1200"],
        ["Zj0b_c", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT800To1200"],
        ["Zj1b", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT800To1200"],
        ["Zj2b", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT800To1200"],
    ],
    "DYToLL_M4to50_HT100to200_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==125&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_LowMHT100To200"],
        ["Zj0b_c", "(sampleIndex/100)==125&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_LowMHT100To200"],
        ["Zj1b", "(sampleIndex/100)==125&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_LowMHT100To200"],
        ["Zj2b", "(sampleIndex/100)==125&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_LowMHT100To200"],
    ], 
    "DYToLL_M4to50_HT200to400_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==126&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_LowMHT200To400"],
        ["Zj0b_c", "(sampleIndex/100)==126&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_LowMHT200To400"],
        ["Zj1b", "(sampleIndex/100)==126&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_LowMHT200To400"],
        ["Zj2b", "(sampleIndex/100)==126&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_LowMHT200To400"],
    ], 
    "DYToLL_M4to50_HT400to600_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==127&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_LowMHT400To600"],
        ["Zj0b_c", "(sampleIndex/100)==127&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_LowMHT400To600"],
        ["Zj1b", "(sampleIndex/100)==127&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_LowMHT400To600"],
        ["Zj2b", "(sampleIndex/100)==127&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_LowMHT400To600"],
    ], 
    "DYToLL_M4to50_HT600toInf_madgraph": [
        ["Zj0b_udsg", "(sampleIndex/100)==128&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_LowMHT600ToInf"],
        ["Zj0b_c", "(sampleIndex/100)==128&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_LowMHT600ToInf"],
        ["Zj1b", "(sampleIndex/100)==128&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_LowMHT600ToInf"],
        ["Zj2b", "(sampleIndex/100)==128&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_LowMHT600ToInf"],
    ]
}

top_fileDict = {
    "ST_t-channel_eleDecays": [
        ["s_Top", 21, 1.0, "TToe_t"]
    ], 
    "ST_t-channel_muDecays": [
        ["s_Top", 20, 1.0, "TTomu_t"]
    ], 
    "ST_t-channel_tauDecays": [
        ["s_Top", 19, 1.0, "TTotau_t"]
    ], 

    "TT_AllHadronic": [
        ["TT", "sampleIndex==212&&IsttB==0", 1.0, "TT_AllHadronic"]
    ], 
    "TT_DiLep_NoPSWeights": [
        ["TT", "sampleIndex==202&&IsttB==0", 1.0, "TT_DiLep_NoPSWeights"]
    ], 
    "TT_SingleLep": [
        ["TT", "sampleIndex==203&&IsttB==0", 1.0, "TT_SingleLep"]
    ],
    "TTBB_AllHadronic": [
        ["TTB", "sampleIndex==26&&IsttB>0", 1.0, "TTBB_AllHadronic"]
    ], 
    "TTBB_DiLep": [
        ["TTB", "sampleIndex==25&&IsttB>0", 1.0, "TTBB_DiLep"]
    ], 
    "TTBB_SingleLep": [
        ["TTB", "sampleIndex==24&&IsttB>0", 1.0, "TTBB_SingleLep"]
    ],
    "TTWLNuJets": [
        ["TTV",205 , 1.0, "TTWLNuJets"]
    ], 
    "TTWQQJets": [
        ["TTV",215 , 1.0, "TTWQQJets"]
    ],    
    "TTZLLNuNuJets": [
        ["TTV",216 , 1.0, "TTZLLNuNuJets"]
    ], 
    "TTZQQJets": [
        ["TTV",217 , 1.0, "TTZQQJets"]
    ],    
    "ttHTobb_M125": [
        ["ttH",22 , 1.0, "ttHTobb_M125"]
    ], 


}
 
WJets_fileDict = {
    "WBJets-Pt100To200": [
        ["Wj0b_udsg", "(sampleIndex/100)==50&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_b100to200"], 
        ["Wj0b_c", "(sampleIndex/100)==50&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_b100to200"], 
        ["Wj1b", "(sampleIndex/100)==50&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_b100to200"], 
        ["Wj2b", "(sampleIndex/100)==50&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_b100to200"], 
    ], 
    "WBJets-Pt200ToInf": [
        ["Wj0b_udsg", "(sampleIndex/100)==51&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_b200toInf"],
        ["Wj0b_c", "(sampleIndex/100)==51&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_b200toInf"],     
        ["Wj1b", "(sampleIndex/100)==51&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_b200toInf"],                               
        ["Wj2b", "(sampleIndex/100)==51&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_b200toInf"],                               
    ], 
    "WJets_madgraph": [
        ["Wj0b_udsg", "(sampleIndex/100)==40&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg"],
        ["Wj0b_c", "(sampleIndex/100)==40&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c"],
        ["Wj1b", "(sampleIndex/100)==40&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b"],
        ["Wj2b", "(sampleIndex/100)==40&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb"],
    ], 
    "WJets-HT100To200": [
        ["Wj0b_udsg", "(sampleIndex/100)==41&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT100To200"],
        ["Wj0b_c", "(sampleIndex/100)==41&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT100To200"],     
        ["Wj1b", "(sampleIndex/100)==41&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT100To200"],                               
        ["Wj2b", "(sampleIndex/100)==41&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT100To200"],                               
    ], 
    "WJets-HT70To100": [
        ["Wj0b_udsg", "(sampleIndex/100)==48&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT70To100"],
        ["Wj0b_c", "(sampleIndex/100)==48&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT70To100"],
        ["Wj1b", "(sampleIndex/100)==48&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT70To100"],
        ["Wj2b", "(sampleIndex/100)==48&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT70To100"],
    ],
    "WJets-HT1200To2500": [
        ["Wj0b_udsg", "(sampleIndex/100)==46&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT1200To2500"],
        ["Wj0b_c", "(sampleIndex/100)==46&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT1200To2500"],     
        ["Wj1b", "(sampleIndex/100)==46&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT1200To2500"],                               
        ["Wj2b", "(sampleIndex/100)==46&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT1200To2500"],                               
    ], 
    "WJets-HT200To400": [
        ["Wj0b_udsg", "(sampleIndex/100)==42&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT200To400"],
        ["Wj0b_c", "(sampleIndex/100)==42&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT200To400"],     
        ["Wj1b", "(sampleIndex/100)==42&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT200To400"],                               
        ["Wj2b", "(sampleIndex/100)==42&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT200To400"],                               
    ], 
    "WJets-HT2500ToInf": [
        ["Wj0b_udsg", "(sampleIndex/100)==47&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT2500ToInf"],
        ["Wj0b_c", "(sampleIndex/100)==47&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT2500ToInf"],     
        ["Wj1b", "(sampleIndex/100)==47&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT2500ToInf"],                               
        ["Wj2b", "(sampleIndex/100)==47&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT2500ToInf"],                               
    ], 
    "WJets-HT400To600": [
        ["Wj0b_udsg", "(sampleIndex/100)==43&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT400To600"],
        ["Wj0b_c", "(sampleIndex/100)==43&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT400To600"],
        ["Wj1b", "(sampleIndex/100)==43&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT400To600"],                               
        ["Wj2b", "(sampleIndex/100)==43&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT400To600"],                               
    ], 
    "WJets-HT600To800": [
        ["Wj0b_udsg", "(sampleIndex/100)==44&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT600To800"],
        ["Wj0b_c", "(sampleIndex/100)==44&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT600To800"],
        ["Wj1b", "(sampleIndex/100)==44&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT600To800"],
        ["Wj2b", "(sampleIndex/100)==44&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT600To800"],
    ], 
    "WJets-HT800To1200": [
        ["Wj0b_udsg", "(sampleIndex/100)==45&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_HT800To1200"],
        ["Wj0b_c", "(sampleIndex/100)==45&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_HT800To1200"],
        ["Wj1b", "(sampleIndex/100)==45&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_HT800To1200"],
        ["Wj2b", "(sampleIndex/100)==45&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_HT800To1200"],
    ], 
    "WJets_BGenFilter-Pt100To200": [
        ["Wj0b_udsg", "(sampleIndex/100)==53&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_bgen100to200"],
        ["Wj0b_c", "(sampleIndex/100)==53&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_bgen100to200"],
        ["Wj1b", "(sampleIndex/100)==53&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_bgen100to200"],
        ["Wj2b", "(sampleIndex/100)==53&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_bgen100to200"],
    ], 
    "WJets_BGenFilter-Pt200ToInf": [
        ["Wj0b_udsg", "(sampleIndex/100)==54&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "W_udsg_bgen200toInf"],
        ["Wj0b_c", "(sampleIndex/100)==54&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "W_c_bgen200toInf"],
        ["Wj1b", "(sampleIndex/100)==54&&nGenStatus2bHadFinalAccept==1", 1.0, "W_b_bgen200toInf"],
        ["Wj2b", "(sampleIndex/100)==54&&nGenStatus2bHadFinalAccept>1", 1.0, "W_bb_bgen200toInf"],
    ]
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
                ["VHH_CV_1_C2V_1_kl_1_hbbhbb", "sampleIndex==-2101010", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0"] 
            ], 
        "ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0": [
                ["VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "sampleIndex==-2051010", 1.0, "ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0": [
                ["VHH_CV_1p5_C2V_1_kl_1_hbbhbb", "sampleIndex==-2151010", 1.0, "ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0": [
                ["VHH_CV_1_C2V_0_kl_1_hbbhbb", "sampleIndex==-2100010", 1.0, "ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0": [
                ["VHH_CV_1_C2V_2_kl_1_hbbhbb", "sampleIndex==-2102010", 1.0, "ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0": [
                ["VHH_CV_1_C2V_1_kl_0_hbbhbb", "sampleIndex==-2101000", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0": [
                ["VHH_CV_1_C2V_1_kl_2_hbbhbb", "sampleIndex==-2101020", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0"] 
            ],
        "ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0": [
                ["VHH_CV_1_C2V_1_kl_20_hbbhbb", "sampleIndex==-21010200", 1.0, "ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0"]
            ],
    }


VV_fileDict = {
    "WZ_1L1Nu2Q_nlo": [
        ["VVHF", 3202, 1.0, "WZ_1L1Nu2Q_bb"], 
        ["VVLF", 3200, 1.0, "WZ_1L1Nu2Q_lf"], 
        ["VVHF", 3201, 1.0, "WZ_1L1Nu2Q_b"]
    ],
    "WW_1L1Nu2Q_nlo": [
        ["VVHF", 3401, 1.0, "WW_1L1Nu2Q_b"], 
        ["VVLF", 3400, 1.0, "WW_1L1Nu2Q_lf"], 
        ["VVHF", 3402, 1.0, "WW_1L1Nu2Q_bb"]
    ] 
} 
QCD_fileDict={
    "QCD_HT50to100": [
        ["QCD", 2, 1.0, "QCDHT50To100"]
    ],
    "QCD_HT100to200": [
        ["QCD", 2, 1.0, "QCDHT100To200"]
    ],
    "QCD_HT1000to1500": [
        ["QCD", 6, 1.0, "QCDHT1000To1500"]
    ], 
    "QCD_HT1500to2000": [
        ["QCD", 7, 1.0, "QCDHT1500To2000"]
    ], 
    "QCD_HT2000toInf": [
        ["QCD", 8, 1.0, "QCDHT2000ToInf"]
    ], 
    "QCD_HT200to300": [
        ["QCD", 2, 1.0, "QCDHT200To300"]
    ], 
    "QCD_HT300to500": [
        ["QCD", 3, 1.0, "QCDHT300To500"]
    ], 
    "QCD_HT500to700": [
        ["QCD", 4, 1.0, "QCDHT500To700"]
    ], 
    "QCD_HT700to1000": [
        ["QCD", 5, 1.0, "QCDHT700To1000"]
    ]
}


ZnnJets_fileDict = {
    "ZBJetsToNuNu_Pt-100to200": [
        ["Zj0b_udsg", "(sampleIndex/100)==160&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "ZBJetsToNuNu_Pt-100to200_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==160&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "ZBJetsToNuNu_Pt-100to200_c"],
        ["Zj1b", "(sampleIndex/100)==160&&nGenStatus2bHadFinalAccept==1", 1.0, "ZBJetsToNuNu_Pt-100to200_b"],
        ["Zj2b", "(sampleIndex/100)==160&&nGenStatus2bHadFinalAccept>1", 1.0, "ZBJetsToNuNu_Pt-100to200_bb"],
    ],
    "ZBJetsToNuNu_Pt-200toInf": [
        ["Zj0b_udsg", "(sampleIndex/100)==161&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "ZBJetsToNuNu_Pt-200toInf_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==161&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "ZBJetsToNuNu_Pt-200toInf_c"],
        ["Zj1b", "(sampleIndex/100)==161&&nGenStatus2bHadFinalAccept==1", 1.0, "ZBJetsToNuNu_Pt-200toInf_b"],
        ["Zj2b", "(sampleIndex/100)==161&&nGenStatus2bHadFinalAccept>1", 1.0, "ZBJetsToNuNu_Pt-200toInf_bb"],
    ],
    "ZJetsToNuNu_BGenFilter_Pt-100to200": [
        ["Zj0b_udsg", "(sampleIndex/100)==162&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "ZJetsToNuNu_BGenFilter_Pt-100to200_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==162&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "ZJetsToNuNu_BGenFilter_Pt-100to200_c"],
        ["Zj1b", "(sampleIndex/100)==162&&nGenStatus2bHadFinalAccept==1", 1.0, "ZJetsToNuNu_BGenFilter_Pt-100to200_b"],
        ["Zj2b", "(sampleIndex/100)==162&&nGenStatus2bHadFinalAccept>1", 1.0, "ZJetsToNuNu_BGenFilter_Pt-100to200_bb"],
    ],
    "ZJetsToNuNu_BGenFilter_Pt-200toInf": [
        ["Zj0b_udsg", "(sampleIndex/100)==163&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "ZJetsToNuNu_BGenFilter_Pt-200toInf_udsg"],
        ["Zj0b_c", "(sampleIndex/100)==163&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "ZJetsToNuNu_BGenFilter_Pt-200toInf_c"],
        ["Zj1b", "(sampleIndex/100)==163&&nGenStatus2bHadFinalAccept==1", 1.0, "ZJetsToNuNu_BGenFilter_Pt-200toInf_b"],
        ["Zj2b", "(sampleIndex/100)==163&&nGenStatus2bHadFinalAccept>1", 1.0, "ZJetsToNuNu_BGenFilter_Pt-200toInf_bb"],
    ],
    "ZJetsToNuNu_HT100To200": [
        ["Zj0b_udsg", "(sampleIndex/100)==150&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT100To200"],
        ["Zj0b_c", "(sampleIndex/100)==150&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT100To200"],
        ["Zj1b", "(sampleIndex/100)==150&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT100To200"],
        ["Zj2b", "(sampleIndex/100)==150&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT100To200"],
    ],
    "ZJetsToNuNu_HT1200To2500": [
        ["Zj0b_udsg", "(sampleIndex/100)==155&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT1200To2500"],
        ["Zj0b_c", "(sampleIndex/100)==155&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT1200To2500"],
        ["Zj1b", "(sampleIndex/100)==155&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT1200To2500"],
        ["Zj2b", "(sampleIndex/100)==155&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT1200To2500"],
    ],
    "ZJetsToNuNu_HT200To400": [
        ["Zj0b_udsg", "(sampleIndex/100)==151&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT200To400"],
        ["Zj0b_c", "(sampleIndex/100)==151&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT200To400"],
        ["Zj1b", "(sampleIndex/100)==151&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT200To400"],
        ["Zj2b", "(sampleIndex/100)==151&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT200To400"],
    ],
    "ZJetsToNuNu_HT2500ToInf": [
        ["Zj0b_udsg", "(sampleIndex/100)==156&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT2500ToInf"],
        ["Zj0b_c", "(sampleIndex/100)==156&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT2500ToInf"],
        ["Zj1b", "(sampleIndex/100)==156&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT2500ToInf"],
        ["Zj2b", "(sampleIndex/100)==156&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT2500ToInf"],
    ],
    "ZJetsToNuNu_HT400To600": [
        ["Zj0b_udsg", "(sampleIndex/100)==152&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT400To600"],
        ["Zj0b_c", "(sampleIndex/100)==152&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT400To600"],
        ["Zj1b", "(sampleIndex/100)==152&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT400To600"],
        ["Zj2b", "(sampleIndex/100)==152&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT400To600"],
    ],
    "ZJetsToNuNu_HT600To800": [
        ["Zj0b_udsg", "(sampleIndex/100)==153&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT600To800"],
        ["Zj0b_c", "(sampleIndex/100)==153&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT600To800"],
        ["Zj1b", "(sampleIndex/100)==153&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT600To800"],
        ["Zj2b", "(sampleIndex/100)==153&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT600To800"],
    ],
    "ZJetsToNuNu_HT800To1200": [
        ["Zj0b_udsg", "(sampleIndex/100)==154&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT800To1200"],
        ["Zj0b_c", "(sampleIndex/100)==154&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT800To1200"],
        ["Zj1b", "(sampleIndex/100)==154&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT800To1200"],
        ["Zj2b", "(sampleIndex/100)==154&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT800To1200"],
    ]
}

Zll_fileDict={
    "ZZ_2L2Q_nlo": [
        ["VVLF", 3600, 1.0, "ZZ_2L2Q_nlo_lf"], 
        ["VVHF", 3601, 1.0, "ZZ_2L2Q_nlo_b"], 
        ["VVHF", 3602, 1.0, "ZZ_2L2Q_nlo_bb"]
    ], 
}

#Zll_fileDict.update(DY_fileDict)
#Zll_fileDict.update(top_fileDict)
#Zll_fileDict.update(VV_fileDict)
#Zll_fileDict.update(ZllHbb_fileDict)

Wln_fileDict = {}
#Wln_fileDict.update(ZnnJets_fileDict)
#Wln_fileDict.update(DY_fileDict)
#Wln_fileDict.update(WJets_fileDict)
Wln_fileDict.update(top_fileDict)
Wln_fileDict.update(WHH4b_fileDict)
Wln_fileDict.update(ZHH4b_fileDict)

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


YearSpecific_fileDict = {
    "2016":{   
        "Run2016BToG_DoubleEle_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016BToG_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016BToG_Ele_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016BToG_MET_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2016BToG_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "TToLeptons_s": [ 
            ["s_Top", 16, 1.0, "TToLeptons_s"]
        ],
        "TBarToLeptons_t": [
            ["s_Top", 19, 1.0, "TBarToLeptons_t"]
        ],
        "TToLeptons_t_powheg": [ 
            ["s_Top", 18, 1.0, "TToLeptons_t"]
        ],
        "Tbar_tW": [
            ["s_Top", 21, 1.0, "Tbar_tW"]
        ],
        "T_tW": [
            ["s_Top", 20, 1.0, "T_tW"]
        ],
        "TT_powheg": [
            ["TT", 200, 1.0, "TT_AllHadronic"]
        ],
        "DYToLL_HT100to200": [
            ["Zj0b_udsg", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT100To200"],
            ["Zj0b_c", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT100To200"],
            ["Zj1b", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT100To200"],
            ["Zj2b", "(sampleIndex/100)==111&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT100To200"],
        ],
        "DYToLL_HT1200to2500": [
            ["Zj0b_udsg", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT1200To2500"],
            ["Zj0b_c", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT1200To2500"],
            ["Zj1b", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT1200To2500"],
            ["Zj2b", "(sampleIndex/100)==116&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT1200To2500"],
        ],
        "DYToLL_HT200to400": [
            ["Zj0b_udsg", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT200To400"],
            ["Zj0b_c", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT200To400"],
            ["Zj1b", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT200To400"],
            ["Zj2b", "(sampleIndex/100)==112&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT200To400"],
        ],
        "DYToLL_HT2500toInf": [
            ["Zj0b_udsg", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT2500ToInf"],
            ["Zj0b_c", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT2500ToInf"],
            ["Zj1b", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT2500ToInf"],
            ["Zj2b", "(sampleIndex/100)==117&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT2500ToInf"],
        ],
        "DYToLL_HT400to600": [
            ["Zj0b_udsg", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT400To600"],
            ["Zj0b_c", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT400To600"],
            ["Zj1b", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT400To600"],
            ["Zj2b", "(sampleIndex/100)==113&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT400To600"],
        ],
        "DYToLL_HT600to800": [
            ["Zj0b_udsg", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT600To800"],
            ["Zj0b_c", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT600To800"],
            ["Zj1b", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT600To800"],
            ["Zj2b", "(sampleIndex/100)==114&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT600To800"],
        ],
        "DYToLL_HT800to1200": [
            ["Zj0b_udsg", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept==0", 1.0, "Z_udsg_HT800To1200"],
            ["Zj0b_c", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept==0&&nGenStatus2DHadFinalAccept>0", 1.0, "Z_c_HT800To1200"],
            ["Zj1b", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept==1", 1.0, "Z_b_HT800To1200"],
            ["Zj2b", "(sampleIndex/100)==115&&nGenStatus2bHadFinalAccept>1", 1.0, "Z_bb_HT800To1200"],
        ],
    },
    "2017":{
        "Run2017_DoubleEle_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_DoubleMu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_Ele_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_MET_MiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2017_Mu_ReMiniAOD": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
    },
    "2018":{
        "Run2018_DoubleEle": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2018_DoubleMu": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2018_Ele": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2018_MET": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "Run2018_Mu": [
            ["data_obs", 0, 1.0, "data_obs"]
        ],
        "ST_tW_top_5f_inc": [
            ["s_Top", 20, 1.0, "T_tW"]
        ],
        "TT_DiLep_NoPSWeights": [
            ["TT", 202, 1.0, "TT_DiLep"]
        ], 
        "ST_s-c_4f_lep": [
            ["s_Top", 16, 1.0, "TToLeptons_s"]
        ],
    }
}
import sys
sys.path.append('..')
from condor_config import year
YearSpecific_fileDict = {
    "2016post":{
        "Run2016post_Ele_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2016post_MET_MiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2016post_Mu_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
    },
    "2016pre":{
        "Run2016pre_Ele_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2016pre_MET_MiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2016pre_Mu_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
    },
    "2017":{
        "Run2017_Ele_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2017_MET_MiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2017_Mu_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
    },
    "2018":{
        "Run2018_EG_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2018_MET_MiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
        "Run2018_Mu_ReMiniAOD": [
            ["data_obs", "1==1", 1.0, "data_obs"]
        ],
    },
}
Wln_fileDict.update(YearSpecific_fileDict[year])
Znn_fileDict.update(YearSpecific_fileDict[year])

#Wln_fileDict.update(YearSpecific_fileDict[year])
#Zll_fileDict.update(YearSpecific_fileDict[year])
#Znn_fileDict.update(YearSpecific_fileDict[year])

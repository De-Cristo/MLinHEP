import ROOT as R
import os
import ctypes
from array import array

method_name = "BDTG method"
xml_model = "./TMVA_weight_model/bdt_tmva_Kl_SM_Zll.weights.xml"
data_name = './TEST_SAMPLE/Other_Zll_rHH_SB_three_btag'

dilep_dPhi = array('f', [0])
dilep_dEta = array('f', [0])
ptl1OVERptl0 = array('f', [0])
ptl0OVERV_mass = array('f', [0])
VHH_Vreco4j_HT = array('f', [0])
VHH_HH_dR = array('f', [0])
VHH_V_HH_pT_Ratio = array('f', [0])
V_mass = array('f', [0])
VHH_H1_pT = array('f', [0])
VHH_HH_pT = array('f', [0])
V_pt = array('f', [0])
VHH_H1_m = array('f', [0])
VHH_HH_m = array('f', [0])
VHH_H1_e = array('f', [0])
VHH_HH_e = array('f', [0])
VHH_V_H1_dPhi = array('f', [0])
VHH_V_HH_dPhi = array('f', [0])
VHH_HH_deta = array('f', [0])
No3_btag_pt = array('f', [0])
No4_btag_pt = array('f', [0])

train_var = {
    'dilep_dPhi' : dilep_dPhi,
    'dilep_dEta' : dilep_dEta,
    'ptl1OVERptl0' : ptl1OVERptl0,
    'ptl0OVERV_mass' : ptl0OVERV_mass,
    'VHH_Vreco4j_HT' : VHH_Vreco4j_HT,
    'VHH_HH_dR' : VHH_HH_dR,
    'VHH_V_HH_pT_Ratio' : VHH_V_HH_pT_Ratio,
    'V_mass' : V_mass,
    'VHH_H1_pT' : VHH_H1_pT,
    'VHH_HH_pT' : VHH_HH_pT,
    'V_pt' : V_pt,
    'VHH_H1_m' : VHH_H1_m,
    'VHH_HH_m' : VHH_HH_m,
    'VHH_H1_e' : VHH_H1_e,
    'VHH_HH_e' : VHH_HH_e,
    'VHH_V_H1_dPhi' : VHH_V_H1_dPhi,
    'VHH_V_HH_dPhi' : VHH_V_HH_dPhi,
    'VHH_HH_deta' : VHH_HH_deta,
    'No3_btag_pt' : No3_btag_pt,
    'No4_btag_pt' : No4_btag_pt,    
}


# VHH_H2H1_pt_ratio = array('f', [0])
# VHH_HH_m = array('f', [0])
# selLeptons_pt_0 = array('f', [0])
# dilep_dPhi = array('f', [0])
# dilep_dEta = array('f', [0])
# ptl1OVERptl0 = array('f', [0])
# ptl0OVERV_mass = array('f', [0])
# VHH_V_H2_dPhi = array('f', [0])
# VHH_HH_dR = array('f', [0])
# VHH_H1_pT = array('f', [0])
# V_pt = array('f', [0])
# VHH_H1_BJet_dR = array('f', [0])
# VHH_H2_BJet_dR = array('f', [0])

# train_var = {
#     'VHH_H2H1_pt_ratio' : VHH_H2H1_pt_ratio,
#     'VHH_HH_m' : VHH_HH_m,
#     'selLeptons_pt_0' : selLeptons_pt_0,
#     'dilep_dPhi' : dilep_dPhi,
#     'dilep_dEta' : dilep_dEta,
#     'ptl1OVERptl0' : ptl1OVERptl0,
#     'ptl0OVERV_mass' : ptl0OVERV_mass,
#     'VHH_V_H2_dPhi' : VHH_V_H2_dPhi,
#     'VHH_HH_dR' : VHH_HH_dR,
#     'VHH_H1_pT' : VHH_H1_pT,
#     'V_pt' : V_pt,
#     'VHH_H1_BJet_dR' : VHH_H1_BJet_dR,
#     'VHH_H2_BJet_dR' : VHH_H2_BJet_dR,
# }

R.TMVA.Tools.Instance()
reader = R.TMVA.Reader()

for key,item in train_var.items():
    reader.AddVariable(key,item)
#end loop

reader.BookMVA(method_name, xml_model)

print(data_name+'.root')

test_data_file = R.TFile.Open(data_name+'.root',"READ")
test_data = test_data_file.Get('Events')

target_file = R.TFile(data_name+"_TMVA.root","RECREATE")
target_data = test_data.CloneTree(0)

for key,item in train_var.items():
    test_data.SetBranchAddress(key,item)
#end loop

BDTG_score = array('f', [0])
target_data.Branch('local_SvB_SM_score',BDTG_score,'local_SvB_SM_score/F')

sw = R.TStopwatch()
sw.Start()

for evt in range(0,test_data.GetEntries()):
    if evt%1000==0 :
        print(evt)
    test_data.GetEntry(evt)
    BDTG_score[0] = reader.EvaluateMVA(method_name)
    target_data.Fill()
#end loop
sw.Stop()

target_data.Write()
target_file.Close()

test_data_file.Close()
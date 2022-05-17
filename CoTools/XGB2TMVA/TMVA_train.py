import ROOT as R
import os
import ctypes
from array import array

R.EnableImplicitMT()
R.TMVA.Tools.Instance()
R.TMVA.PyMethodBase.PyInitialize()

sig_file_name  = "./RwT_Training/Train_Sample/DY_SB_4b.root"
bkg_file_name  = "./RwT_Training/Train_Sample/DY_SB_2b.root"
outfileName    = "./TMVA_middle_RwT_DY_2TO4_model.root"

input_sig_file = R.TFile(sig_file_name, "CACHEREAD")
input_bkg_file = R.TFile(bkg_file_name, "CACHEREAD")

input_sig_tree = input_sig_file.Get("Events")
input_bkg_tree = input_bkg_file.Get("Events")

outputFile     = R.TFile(outfileName, "RECREATE")

factory        = R.TMVA.Factory("TMVAClassification", outputFile,\
"!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification")

dataloader     = R.TMVA.DataLoader("dataset")

# train_var = [('dilep_dPhi','F'),('dilep_dEta','F'), ('ptl1OVERptl0','F'), ('ptl0OVERV_mass','F'),\
#              ('VHH_Vreco4j_HT','F'), ('VHH_HH_dR','F'), ('VHH_V_HH_pT_Ratio','F'),('V_mass','F'),\
#              ('VHH_H1_pT','F'), ('VHH_HH_pT','F'), ('V_pt','F'), \
#              ('VHH_H1_m','F'),('VHH_HH_m','F'), \
#              ('VHH_H1_e','F'),('VHH_HH_e','F'), \
#              ('VHH_V_H1_dPhi','F'), ('VHH_V_HH_dPhi','F'), ('VHH_HH_deta','F'), \
#              ('No3_btag_pt','F'), ('No4_btag_pt','F') \
#             ]
# train_var = [('V_mass','F'),('VHH_H1_m','F'), ('VHH_Vreco4j_HT','F'), ('VHH_HH_m','F'),\
#              ('VHH_HH_pT','F'), ('No3_btag_pt','F'), ('VHH_H1_pT','F'),('VHH_V_HH_pT_Ratio','F')\
#             ]

# dataloader.AddVariable("VHH_H2H1_pt_ratio", "VHH_H2H1_pt_ratio", "units", 'F' )
# dataloader.AddVariable("VHH_HH_m", "VHH_HH_m", "units", 'F' )
# dataloader.AddVariable("selLeptons_pt_0", "selLeptons_pt_0", "units", 'F' )
# dataloader.AddVariable("dilep_dPhi", "dilep_dPhi", "units", 'F' )
# dataloader.AddVariable("dilep_dEta", "dilep_dEta", "units", 'F' )
# dataloader.AddVariable("ptl1OVERptl0", "ptl1OVERptl0", "units", 'F' )
# dataloader.AddVariable("ptl0OVERV_mass", "ptl0OVERV_mass", "units", 'F' )
# dataloader.AddVariable("VHH_V_H2_dPhi", "VHH_V_H2_dPhi", "units", 'F' )
# dataloader.AddVariable("VHH_HH_dR", "VHH_HH_dR", "units", 'F' )
# dataloader.AddVariable("VHH_H1_pT", "VHH_H1_pT", "units", 'F' )
# dataloader.AddVariable("V_pt", "V_pt", "units", 'F' )
# dataloader.AddVariable("VHH_H1_BJet_dR", "VHH_H1_BJet_dR", "units", 'F' )
# dataloader.AddVariable("VHH_H2_BJet_dR", "VHH_H2_BJet_dR", "units", 'F' )

dataloader.AddVariable("dilep_dPhi", "dilep_dPhi", "units", 'F' )
dataloader.AddVariable("dilep_dEta", "dilep_dEta", "units", 'F' )
dataloader.AddVariable("ptl1OVERptl0", "ptl1OVERptl0", "units", 'F' )
dataloader.AddVariable("ptl0OVERV_mass", "ptl0OVERV_mass", "units", 'F' )
dataloader.AddVariable("VHH_Vreco4j_HT", "VHH_Vreco4j_HT", "units", 'F' )
dataloader.AddVariable("VHH_HH_dR", "VHH_HH_dR", "units", 'F' )
dataloader.AddVariable("VHH_V_HH_pT_Ratio", "VHH_V_HH_pT_Ratio", "units", 'F' )
dataloader.AddVariable("V_mass", "V_mass", "units", 'F' )
dataloader.AddVariable("VHH_H1_pT", "VHH_H1_pT", "units", 'F' )
dataloader.AddVariable("VHH_HH_pT", "VHH_HH_pT", "units", 'F' )
dataloader.AddVariable("V_pt", "V_pt", "units", 'F' )
dataloader.AddVariable("VHH_H1_m", "VHH_H1_m", "units", 'F' )
dataloader.AddVariable("VHH_HH_m", "VHH_HH_m", "units", 'F' )
dataloader.AddVariable("VHH_H1_e", "VHH_H1_e", "units", 'F' )
dataloader.AddVariable("VHH_HH_e", "VHH_HH_e", "units", 'F' )
dataloader.AddVariable("VHH_V_H1_dPhi", "VHH_V_H1_dPhi", "units", 'F' )
dataloader.AddVariable("VHH_V_HH_dPhi", "VHH_V_HH_dPhi", "units", 'F' )
dataloader.AddVariable("VHH_HH_deta", "VHH_HH_deta", "units", 'F' )
dataloader.AddVariable("No3_btag_pt", "No3_btag_pt", "units", 'F' )
dataloader.AddVariable("No4_btag_pt", "No4_btag_pt", "units", 'F' )

signalWeight     = 1.0
backgroundWeight = 1.0

dataloader.AddSignalTree    ( input_sig_tree,     signalWeight )
dataloader.AddBackgroundTree( input_bkg_tree,     backgroundWeight )

dataloader.SetSignalWeightExpression    ("weight")
dataloader.SetBackgroundWeightExpression("weight")

cuta = R.TCut()
cutb = R.TCut()

cuta = " "
cutb = " "

dataloader.PrepareTrainingAndTestTree(R.TCut("weight<10"), "nTrain_Signal=3500:nTrain_Background=300000:nTest_Signal=500:nTest_Background=40000:SplitMode=Random:NormMode=None:!V")

factory.BookMethod(dataloader, R.TMVA.Types.kBDT, "BDTG", "!H:!V:NTrees=200:MinNodeSize=5%:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost:BaggedSampleFraction=0.7:nCuts=10:MaxDepth=3")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

outputFile.Close()

del factory
del dataloader
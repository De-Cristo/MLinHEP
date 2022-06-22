import ROOT as R
import os
import ctypes
from array import array

R.EnableImplicitMT()
R.TMVA.Tools.Instance()
R.TMVA.PyMethodBase.PyInitialize()

sig_file_name  = "./Sample/zmerged.root"
bkg_file_name  = "./Sample/zmerged.root"
outfileName    = "./zmerged_middle_TMVA.root"

input_sig_file = R.TFile(sig_file_name, "CACHEREAD")
input_bkg_file = R.TFile(bkg_file_name, "CACHEREAD")

input_sig_tree = input_sig_file.Get("Events")
input_bkg_tree = input_bkg_file.Get("Events")

outputFile     = R.TFile(outfileName, "RECREATE")

factory        = R.TMVA.Factory("TMVAClassification", outputFile,\
"!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification")

dataloader     = R.TMVA.DataLoader("dataset")

dataloader.AddVariable("deta_2mu2bj", "deta_2mu2bj", "units", 'F' )
dataloader.AddVariable("pt2bj_ov_m2bj", "pt2bj_ov_m2bj", "units", 'F' )
dataloader.AddVariable("pt2bj_ov_mbbmm", "pt2bj_ov_mbbmm", "units", 'F' )
dataloader.AddVariable("pt2mu_ov_m2mu", "pt2mu_ov_m2mu", "units", 'F' )
dataloader.AddVariable("scalar_hh_pt", "scalar_hh_pt", "units", 'F' )

signalWeight     = 1.0
backgroundWeight = 1.0

dataloader.AddSignalTree    ( input_sig_tree,     signalWeight )
dataloader.AddBackgroundTree( input_bkg_tree,     backgroundWeight )

dataloader.SetSignalWeightExpression    ("weight")
dataloader.SetBackgroundWeightExpression("weight")

cuts = R.TCut("dsid==002")
cutb = R.TCut("dsid>215&&dsid<225")

dataloader.PrepareTrainingAndTestTree(cuts, cutb, "nTrain_Signal=90000:nTrain_Background=500000:nTest_Signal=5650:nTest_Background=39005:SplitMode=Random:NormMode=None:!V")

factory.BookMethod(dataloader, R.TMVA.Types.kBDT, "BDTG", "!H:!V:NTrees=200:MinNodeSize=5%:BoostType=Grad:Shrinkage=0.1:UseBaggedBoost:BaggedSampleFraction=0.7:nCuts=10:MaxDepth=3")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

outputFile.Close()

del factory
del dataloader
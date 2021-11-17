// Train BDT for VHH analysis
// written by Licheng Modified from ROOT TMVA tutorial codes

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"

int LocalBDT_TMVA( TString myMethodList = "" ){
    
    TMVA::Tools::Instance(); //load library
    
    std::map<std::string,int> Use; // Default MVA methods to be trained + tested
    
    // Boosted Decision Trees
    Use["BDT"]             = 1; // uses Adaptive Boost
    Use["BDTG"]            = 0; // uses Gradient Boost
    Use["BDTB"]            = 0; // uses Bagging
    Use["BDTD"]            = 0; // decorrelation + Adaptive Boost
    Use["BDTF"]            = 0; // allow usage of fisher discriminant for node splitting
    // ---------------------------------------------------------------------------------------------------
    
    std::cout << std::endl;
    std::cout << "==> Start TMVAClassification" << std::endl;
    
    // Select methods (don't look at this code - not of interest)
    if (myMethodList != "") {
        for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;
        
        std::vector<TString> mlist = TMVA::gTools().SplitString( myMethodList, ',' );
        for (UInt_t i=0; i<mlist.size(); i++) {
            std::string regMethod(mlist[i]);
            if (Use.find(regMethod) == Use.end()){
                std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
                for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
                std::cout << std::endl;
                return 1;
            }
            Use[regMethod] = 1;
        }
    }
    // ---------------------------------------------------------------------------------------------------
    // Here the preparation phase begins
    
    // Read training and test data  // (it is also possible to use ASCII format as input -> see TMVA Users Guide)
    TFile *input_sig(0);
    TFile *input_bkg(0);
    TString fname_sig = "./VHH_BDT_Signal.root";
    TString fname_bkg = "./VHH_BDT_Background.root";
    if (!gSystem->AccessPathName( fname_sig ) && !gSystem->AccessPathName( fname_bkg )) {
      input_sig = TFile::Open( fname_sig ); // check if file in local directory exists
      input_bkg = TFile::Open( fname_bkg ); // check if file in local directory exists
    }
    else {
      TFile::SetCacheFileDir(".");
//       input = TFile::Open("http://root.cern.ch/files/tmva_class_example.root", "CACHEREAD");
      input_sig = TFile::Open("/eos/user/l/lichengz/VHH4bAnalysisNtuples/LocalBDT/VHH_BDT_Signal.root", "CACHEREAD");
      input_bkg = TFile::Open("/eos/user/l/lichengz/VHH4bAnalysisNtuples/LocalBDT/VHH_BDT_Background.root", "CACHEREAD");
    }
    if (!input_sig || !input_bkg) {
      std::cout << "ERROR: could not open data file" << std::endl;
      exit(1);
    }
    std::cout << "--- TMVAClassification       : Using input file: " << input_sig->GetName() << " and " << input_bkg->GetName() << std::endl;
    
    // Register the training and test trees
    TTree *signalTree     = (TTree*)input_sig->Get("TreeS");
    TTree *background     = (TTree*)input_bkg->Get("TreeB");
    
    // Create a ROOT output file where TMVA will store ntuples, histograms, etc.
    TString outfileName( "TMVA_middle.root" );
    TFile* outputFile = TFile::Open( outfileName, "RECREATE" );
    
    // ---------------------------------------------------------------------------------------------------
    // Create the factory object. The factory is the only TMVA object you have to interact with.
    // The first argument is the base of the name of all the weightfiles in the directory weight.
    // The second argument is the output file for the training results .
    // All TMVA output can be suppressed by removing the "!" (not) in front of the "Silent" argument in the option string
    
    TMVA::Factory *factory = new TMVA::Factory( "TMVAClassification", outputFile,
                                                "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );
    
    TMVA::DataLoader *dataloader=new TMVA::DataLoader("dataset");
    // If you wish to modify default settings
    // (please check "src/Config.h" to see all available global options)
    
    //    (TMVA::gConfig().GetVariablePlotting()).fTimesRMS = 8.0;
    //    (TMVA::gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory";
    
    // Define the input variables that shall be used for the MVA training
    // note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
    // [all types of expressions that can also be parsed by TTree::Draw( "expression" )]
    
    //dataloader->AddVariable( "myvar1 := var1+var2", 'F' );
    //dataloader->AddVariable( "myvar2 := var1-var2", "Expression 2", "", 'F' );
//     dataloader->AddVariable( "var1",                "Variable 1", "units", 'F' );
//     dataloader->AddVariable( "var2",                "Variable 2", "units", 'F' );
    //dataloader insert point!!!
    
    // You can add so-called "Spectator variables", which are not used in the MVA training,
    // but will appear in the final "TestTree" produced by TMVA. This TestTree will contain the
    // input variables, the response values of all trained MVAs, and the spectator variables
    
//     dataloader->AddSpectator( "spec1 := var1*2",  "Spectator 1", "units", 'F' );
//     dataloader->AddSpectator( "spec2 := var1*3",  "Spectator 2", "units", 'F' );
    
    // global event weights per tree (see below for setting event-wise weights)
    Double_t signalWeight     = 1.0;
    Double_t backgroundWeight = 1.0;
    
    // You can add an arbitrary number of signal or background trees
    dataloader->AddSignalTree    ( signalTree,     signalWeight );
    dataloader->AddBackgroundTree( background, backgroundWeight );
    
    dataloader->SetSignalWeightExpression    ("weight");
    dataloader->SetBackgroundWeightExpression("weight");
    // To give different trees for training and testing, do as follows:
    //
    //     dataloader->AddSignalTree( signalTrainingTree, signalTrainWeight, "Training" );
    //     dataloader->AddSignalTree( signalTestTree,     signalTestWeight,  "Test" );
    
    // Use the following code instead of the above two or four lines to add signal and background
    // training and test events "by hand"
    // NOTE that in this case one should not give expressions (such as "var1+var2") in the input
    // variable definition, but simply compute the expression before adding the event
    // ```cpp
    // // --- begin ----------------------------------------------------------
    // std::vector<Double_t> vars( 4 ); // vector has size of number of input variables
    // Float_t  treevars[4], weight;
    //
    // // Signal
    // for (UInt_t ivar=0; ivar<4; ivar++) signalTree->SetBranchAddress( Form( "var%i", ivar+1 ), &(treevars[ivar]) );
    // for (UInt_t i=0; i<signalTree->GetEntries(); i++) {
    //     signalTree->GetEntry(i);
    //    for (UInt_t ivar=0; ivar<4; ivar++) vars[ivar] = treevars[ivar];
    //    // add training and test events; here: first half is training, second is testing
    //    // note that the weight can also be event-wise
    //    if (i < signalTree->GetEntries()/2.0) dataloader->AddSignalTrainingEvent( vars, signalWeight );
    //    else                              dataloader->AddSignalTestEvent    ( vars, signalWeight );
    // }
    
    // // Background (has event weights)
    // background->SetBranchAddress( "weight", &weight );
    // for (UInt_t ivar=0; ivar<4; ivar++) background->SetBranchAddress( Form( "var%i", ivar+1 ), &(treevars[ivar]) );
    // for (UInt_t i=0; i<background->GetEntries(); i++) {
    //    background->GetEntry(i);
    //    for (UInt_t ivar=0; ivar<4; ivar++) vars[ivar] = treevars[ivar];
    //    // add training and test events; here: first half is training, second is testing
    //    // note that the weight can also be event-wise
    //    if (i < background->GetEntries()/2) dataloader->AddBackgroundTrainingEvent( vars, backgroundWeight*weight );
    //    else                                dataloader->AddBackgroundTestEvent    ( vars, backgroundWeight*weight );
    // }
    // // --- end ------------------------------------------------------------
    // ```
    // End of tree registration
    
    // Set individual event weights (the variables must exist in the original TTree)
    // -  for signal    : `dataloader->SetSignalWeightExpression    ("weight1*weight2");`
    // -  for background: `dataloader->SetBackgroundWeightExpression("weight1*weight2");`
    
    //dataloader->SetBackgroundWeightExpression( "weight" );
    //DO WE USE REAL WEIGHT? licheng
    
    // Apply additional cuts on the signal and background samples (can be different)
    TCut mycuts = ""; // for example: TCut mycuts = "abs(var1)<0.5 && abs(var2-0.5)<1";
    TCut mycutb = ""; // for example: TCut mycutb = "abs(var1)<0.5";
    
    // Tell the dataloader how to use the training and testing events
    //
    // If no numbers of events are given, half of the events in the tree are used
    // for training, and the other half for testing:
    //
    //    dataloader->PrepareTrainingAndTestTree( mycut, "SplitMode=random:!V" );
    //
    // To also specify the number of testing events, use:
    //
    //    dataloader->PrepareTrainingAndTestTree( mycut,
    //         "NSigTrain=3000:NBkgTrain=3000:NSigTest=3000:NBkgTest=3000:SplitMode=Random:!V" );
    dataloader->PrepareTrainingAndTestTree( mycuts, mycutb,
                                           "nTrain_Signal=1000:nTrain_Background=1000:SplitMode=Random:NormMode=NumEvents:!V" );
    
    // ### Book MVA methods
    // it is possible to preset ranges in the option string in which the cut optimisation should be done:
    // "...:CutRangeMin[2]=-1:CutRangeMax[2]=1"...", where [2] is the third input variable
    
    // Boosted Decision Trees
    if (Use["BDTG"]) // Gradient Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTG",
                           "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" );

    if (Use["BDT"])  // Adaptive Boost!!!
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT",
                           "!H:!V:NTrees=500:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" );

    if (Use["BDTB"]) // Bagging
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTB",
                           "!H:!V:NTrees=400:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20" );

    if (Use["BDTD"]) // Decorrelation + Adaptive Boost
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTD",
                           "!H:!V:NTrees=400:MinNodeSize=5%:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate" );

    if (Use["BDTF"])  // Allow Using Fisher discriminant in node splitting for (strong) linearly correlated variables
      factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDTF",
                           "!H:!V:NTrees=50:MinNodeSize=2.5%:UseFisherCuts:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" );
    
    // For an example of the category classifier usage, see: TMVAClassificationCategory
    // What are the following?
    // --------------------------------------------------------------------------------------------------
    //  Now you can optimize the setting (configuration) of the MVAs using the set of training events
    // STILL EXPERIMENTAL and only implemented for BDT's !
    //
    //     factory->OptimizeAllMethods("SigEffAt001","Scan");
    //     factory->OptimizeAllMethods("ROCIntegral","FitGA");
    //
    // --------------------------------------------------------------------------------------------------

    // Now you can tell the factory to train, test, and evaluate the MVAs
    //
    // Train MVAs using the set of training events
    
    factory->TrainAllMethods();
    // Evaluate all MVAs using the set of test events
    factory->TestAllMethods();
    // Evaluate and compare performance of all configured MVAs
    factory->EvaluateAllMethods();
    
    // --------------------------------------------------------------------------------------------------
    
    // Save the output
    outputFile->Close();
    
    std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
    std::cout << "==> TMVAClassification is done!" << std::endl;
    
    delete factory;
    delete dataloader;
    
    // --------------------------------------------------------------------------------------------------
    // Launch the GUI for the root macros
    if (!gROOT->IsBatch()) TMVA::TMVAGui( outfileName );
    
    return 0;
}

int main( int argc, char** argv )
{
   // Select methods
   TString methodList;
   for (int i=1; i<argc; i++) {
      TString regMethod(argv[i]);
      if(regMethod=="-b" || regMethod=="--batch") continue;
      if (!methodList.IsNull()) methodList += TString(",");
      methodList += regMethod;
   }
   return LocalBDT_TMVA(methodList);
}
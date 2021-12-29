// Train BDT for VHH analysis
// written by Licheng based on ROOT TMVA tutorial codes /// \author Andreas Hoecker

#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"

#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"

using namespace TMVA;

void LocalBDT_Coupling_Application( TString myMethodList = "" ){
    //---------------------------------------------------------------
    TMVA::Tools::Instance();
    
    std::map<std::string,int> Use;
    
//     ROOT::EnableImplicitMT();
    
//     (TMVA::gConfig().GetVariablePlotting()).fNbins1D = 200;
    
    // Boosted Decision Trees
    Use["BDT"]             = 0; // uses Adaptive Boost
    Use["BDTG"]            = 1; // uses Gradient Boost
    Use["BDTB"]            = 0; // uses Bagging
    Use["BDTD"]            = 0; // decorrelation + Adaptive Boost
    Use["BDTF"]            = 0; // allow usage of fisher discriminant for node splitting
    
    std::cout << std::endl;
    std::cout << "==> Start TMVAClassificationApplication" << std::endl;
    
    // ---------------------------------------------------------------------------------------------------
    if (myMethodList != "") {
        for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;
        
        std::vector<TString> mlist = gTools().SplitString( myMethodList, ',' );
        for (UInt_t i=0; i<mlist.size(); i++) {
            std::string regMethod(mlist[i]);
            if (Use.find(regMethod) == Use.end()) {
                std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
                std::cout << it->first << " ";
            }
            std::cout << std::endl;
            return;
         }
         Use[regMethod] = 1;
        }
    }
    // ---------------------------------------------------------------------------------------------------
    
    // Create the Reader object
    TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );
    //#insert variables
    Float_t V_e, V_pt, H1_e, H1_pt, H1_eta, H2_e, H2_eta, HH_e, HH_m, HH_eta, dEta_H1_H2, dPhi_H1_H2, dPhi_V_H2, dR_H1_H2, pt_ratio;
    
    reader->AddVariable( "V_pt", &V_pt );
    reader->AddVariable( "H1_e", &H1_e );
    reader->AddVariable( "H1_pt", &H1_pt );
    reader->AddVariable( "H1_eta", &H1_eta );
    reader->AddVariable( "H2_e", &H2_e );
    reader->AddVariable( "H2_eta", &H2_eta );
    reader->AddVariable( "HH_e", &HH_e );
    reader->AddVariable( "HH_m", &HH_m );
    reader->AddVariable( "HH_eta", &HH_eta );
    reader->AddVariable( "dEta_H1_H2", &dEta_H1_H2 );
    reader->AddVariable( "dPhi_H1_H2", &dPhi_H1_H2 );
    reader->AddVariable( "dPhi_V_H2", &dPhi_V_H2 );
    reader->AddVariable( "dR_H1_H2", &dR_H1_H2 );
    reader->AddVariable( "pt_ratio", &pt_ratio );

    // Spectator variables declared in the training have to be added to the reader, too
//     Float_t spec1,spec2;
//     reader->AddSpectator( "spec1 := var1*2",   &spec1 );
//     reader->AddSpectator( "spec2 := var1*3",   &spec2 );
    
//     Float_t Category_cat1, Category_cat2, Category_cat3;
//     if (Use["Category"]){
//         // Add artificial spectators for distinguishing categories
//         reader->AddSpectator( "Category_cat1 := var3<=0",             &Category_cat1 );
//         reader->AddSpectator( "Category_cat2 := (var3>0)&&(var4<0)",  &Category_cat2 );
//         reader->AddSpectator( "Category_cat3 := (var3>0)&&(var4>=0)", &Category_cat3 );
//     }
    
    // Book the MVA methods
    TString dir    = "dataset/weights/";
    TString prefix = "TMVAClassification";
    
    // Book method(s)TMVAClassification_BDT_c2v_model.weights.xml
    for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
        if (it->second) {
            TString methodName = TString(it->first) + TString(" method");
            TString weightfile = dir + prefix + TString("_") + TString(it->first) + TString(".weights.xml");
            reader->BookMVA( methodName, weightfile );
        }
    }
    
    // Book output histograms DEFAULT FIXME

    
    // Book example histogram for probability (the other methods are done similarly) //See if useful
//     TH1F *probHistBDT(0), *rarityHistBDT(0);
//     if (Use["BDT"]) {
//       probHistBDT   = new TH1F( "MVA_BDT_Proba",  "MVA_BDT_Proba",  nbin, 0, 1 );
//       rarityHistBDT = new TH1F( "MVA_BDT_Rarity", "MVA_BDT_Rarity", nbin, 0, 1 );
//     }
    
    // Prepare input tree (this must be replaced by your data source)
    // In this test only use signal sample (because signals are different)? licheng
    TFile *input_sig(0);
    TFile *input_bkg(0);
    
//     TString fname_sig = "./VHH_BDT_Signal_Test.root";
    TString fname_sig = "./TrainSamples/VHH_10_kl.root";
    TString fname_bkg = "./no.root";
        
    if (!gSystem->AccessPathName( fname_sig ) && !gSystem->AccessPathName( fname_bkg )) {
        input_sig = TFile::Open( fname_sig ); // check if file in local directory exists
        input_bkg = TFile::Open( fname_bkg ); // check if file in local directory exists
        std::cout << "--- TMVAClassificationApp    : Using signal input file: " << input_sig->GetName() << std::endl;
        std::cout << "--- TMVAClassificationApp    : Using background input file: " << input_bkg->GetName() << std::endl;
    }
    else if (!gSystem->AccessPathName( fname_sig ) && gSystem->AccessPathName( fname_bkg )){
        input_sig = TFile::Open( fname_sig ); // check if file in local directory exists
        std::cout << "--- TMVAClassificationApp    : Using signal input file: " << input_sig->GetName() << std::endl;
    }
    else {
        TFile::SetCacheFileDir(".");
        input_sig = TFile::Open("/eos/user/l/lichengz/VHH4bAnalysisNtuples/LocalBDT/VHH_BDT_Signal_Test.root", "CACHEREAD");
        input_bkg = TFile::Open("/eos/user/l/lichengz/VHH4bAnalysisNtuples/LocalBDT/VHH_BDT_Background_Test.root", "CACHEREAD");
        std::cout << "--- TMVAClassificationApp    : Using signal input file: " << input_sig->GetName() << std::endl;
        std::cout << "--- TMVAClassificationApp    : Using background input file: " << input_bkg->GetName() << std::endl;
    }
    if (!input_sig) {
      std::cout << "ERROR: could not open data file" << std::endl;
      exit(1);
    }
    
    // ---------------------------------------------------------------------------------------------------
    
    
    // ---------------------------------------------------------------------------------------------------
    // Prepare the event tree
    // Using variables above will be slightly faster?
    
    TFile *target  = new TFile( "TMVApp_c2v_couping_14vars_10_0_kl.root","RECREATE" );
    

    //#insert user variables sig
    Float_t user_V_e, user_V_pt, user_H1_e, user_H1_pt, user_H1_eta, user_H2_e, user_H2_eta, user_HH_e, user_HH_m, user_HH_eta, user_dEta_H1_H2, user_dPhi_H1_H2, user_dPhi_V_H2, user_dR_H1_H2, user_pt_ratio, user_BDT, user_BDTG, user_BDTB, user_BDTD, user_BDTF;

    std::cout << "--- Select signal sample" << std::endl;
    TTree* theTree_sig = (TTree*)input_sig->Get("TreeS");
    TTree* theTree_sig_out = new TTree("Tree_sig", "Tree_sig");
    
    std::cout << "--- Processing: " << theTree_sig->GetEntries() << "signal events" << std::endl;
    
    if (Use["BDT"])           theTree_sig_out->Branch("user_BDT", &user_BDT);
    if (Use["BDTG"])          theTree_sig_out->Branch("user_BDTG_c2v", &user_BDTG);
    if (Use["BDTB"])          theTree_sig_out->Branch("user_BDTB", &user_BDTB);
    if (Use["BDTD"])          theTree_sig_out->Branch("user_BDTD", &user_BDTD);
    if (Use["BDTF"])          theTree_sig_out->Branch("user_BDTF", &user_BDTF);

    //#link user variables sig
    theTree_sig->SetBranchAddress( "V_pt", &V_pt );
    theTree_sig->SetBranchAddress( "H1_e", &H1_e );
    theTree_sig->SetBranchAddress( "H1_pt", &H1_pt );
    theTree_sig->SetBranchAddress( "H1_eta", &H1_eta );
    theTree_sig->SetBranchAddress( "H2_e", &H2_e );
    theTree_sig->SetBranchAddress( "H2_eta", &H2_eta );
    theTree_sig->SetBranchAddress( "HH_e", &HH_e );
    theTree_sig->SetBranchAddress( "HH_m", &HH_m );
    theTree_sig->SetBranchAddress( "HH_eta", &HH_eta );
    theTree_sig->SetBranchAddress( "dEta_H1_H2", &dEta_H1_H2 );
    theTree_sig->SetBranchAddress( "dPhi_H1_H2", &dPhi_H1_H2 );
    theTree_sig->SetBranchAddress( "dPhi_V_H2", &dPhi_V_H2 );
    theTree_sig->SetBranchAddress( "dR_H1_H2", &dR_H1_H2 );
    theTree_sig->SetBranchAddress( "pt_ratio", &pt_ratio );
    
    theTree_sig_out->Branch( "V_pt", &user_V_pt );
    theTree_sig_out->Branch( "H1_e", &user_H1_e );
    theTree_sig_out->Branch( "H1_pt", &user_H1_pt );
    theTree_sig_out->Branch( "H1_eta", &user_H1_eta );
    theTree_sig_out->Branch( "H2_e", &user_H2_e );
    theTree_sig_out->Branch( "H2_eta", &user_H2_eta );
    theTree_sig_out->Branch( "HH_e", &user_HH_e );
    theTree_sig_out->Branch( "HH_m", &user_HH_m );
    theTree_sig_out->Branch( "HH_eta", &user_HH_eta );
    theTree_sig_out->Branch( "dEta_H1_H2", &user_dEta_H1_H2 );
    theTree_sig_out->Branch( "dPhi_H1_H2", &user_dPhi_H1_H2 );
    theTree_sig_out->Branch( "dPhi_V_H2", &user_dPhi_V_H2 );
    theTree_sig_out->Branch( "dR_H1_H2", &user_dR_H1_H2 );
    theTree_sig_out->Branch( "pt_ratio", &user_pt_ratio );
    
    TStopwatch sw;
    sw.Start();
    
    for (Long64_t ievt=0; ievt<theTree_sig->GetEntries(); ievt++) {
        if (ievt%1000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
        theTree_sig->GetEntry(ievt);
        
        //#looping variables sig
        user_V_pt = V_pt;
        user_H1_e = H1_e;
        user_H1_pt = H1_pt;
        user_H1_eta = H1_eta;
        user_H2_e = H2_e;
        user_H2_eta = H2_eta;
        user_HH_e = HH_e;
        user_HH_m = HH_m;
        user_HH_eta = HH_eta;
        user_dEta_H1_H2 = dEta_H1_H2;
        user_dPhi_H1_H2 = dPhi_H1_H2;
        user_dPhi_V_H2 = dPhi_V_H2;
        user_dR_H1_H2 = dR_H1_H2;
        user_pt_ratio = pt_ratio;
        
        // Return the MVA outputs and fill into histograms
        if (Use["BDT"])           {
            if (reader->EvaluateMVA( "BDT method"            )<0.8 && reader->EvaluateMVA( "BDT method"            )>-0.8){user_BDT  = reader->EvaluateMVA( "BDT method"            ); }
            else{user_BDT = -0.9;}
        }
        if (Use["BDTG"])          {user_BDTG = reader->EvaluateMVA( "BDTG method"           ); }
        if (Use["BDTB"])          {user_BDTB = reader->EvaluateMVA( "BDTB method"           ); }
        if (Use["BDTD"])          {user_BDTD = reader->EvaluateMVA( "BDTD method"           ); }
        if (Use["BDTF"])          {user_BDTF = reader->EvaluateMVA( "BDTF method"           ); }
        
        theTree_sig_out->Fill();
    }
    
    // Get elapsed time
    sw.Stop();
    std::cout << "--- End of signal event loop: "; sw.Print();
    theTree_sig_out ->Write();
    
    
    TTree* theTree_bkg_out = new TTree("Tree_bkg", "Tree_bkg");
    if (input_bkg) {
        Float_t user_V_e_B, user_V_pt_B, user_H1_e_B, user_H1_pt_B, user_H1_eta_B, user_H2_e_B, user_H2_eta_B, user_HH_e_B, user_HH_m_B, user_HH_eta_B, user_dEta_H1_H2_B, user_dPhi_H1_H2_B, user_dPhi_V_H2_B, user_dR_H1_H2_B, user_pt_ratio_B, user_BDT_B, user_BDTG_B, user_BDTB_B, user_BDTD_B, user_BDTF_B;
        
        if (Use["BDT"])           theTree_bkg_out->Branch("user_BDT_c2v", &user_BDT_B);
        if (Use["BDTG"])          theTree_bkg_out->Branch("user_BDTG_c2v", &user_BDTG_B);
        if (Use["BDTB"])          theTree_bkg_out->Branch("user_BDTB", &user_BDTB_B);
        if (Use["BDTD"])          theTree_bkg_out->Branch("user_BDTD", &user_BDTD_B);
        if (Use["BDTF"])          theTree_bkg_out->Branch("user_BDTF", &user_BDTF_B);
        
        std::cout << "--- Select background sample" << std::endl;
        TTree* theTree_bkg = (TTree*)input_bkg->Get("TreeB");
        std::cout << "--- Processing: " << theTree_bkg->GetEntries() << "background events" << std::endl;
        //#link user variables bkg
        theTree_bkg->SetBranchAddress( "V_e", &V_e );
        theTree_bkg->SetBranchAddress( "V_pt", &V_pt );
        theTree_bkg->SetBranchAddress( "H1_e", &H1_e );
        theTree_bkg->SetBranchAddress( "H1_pt", &H1_pt );
        theTree_bkg->SetBranchAddress( "H1_eta", &H1_eta );
        theTree_bkg->SetBranchAddress( "H2_e", &H2_e );
        theTree_bkg->SetBranchAddress( "H2_eta", &H2_eta );
        theTree_bkg->SetBranchAddress( "HH_e", &HH_e );
        theTree_bkg->SetBranchAddress( "HH_m", &HH_m );
        theTree_bkg->SetBranchAddress( "HH_eta", &HH_eta );
        theTree_bkg->SetBranchAddress( "dEta_H1_H2", &dEta_H1_H2 );
        theTree_bkg->SetBranchAddress( "dPhi_H1_H2", &dPhi_H1_H2 );
        theTree_bkg->SetBranchAddress( "dPhi_V_H2", &dPhi_V_H2 );
        theTree_bkg->SetBranchAddress( "dR_H1_H2", &dR_H1_H2 );
        theTree_bkg->SetBranchAddress( "pt_ratio", &pt_ratio );

        theTree_bkg_out->Branch( "V_e", &user_V_e_B  );
        theTree_bkg_out->Branch( "V_pt", &user_V_pt_B  );
        theTree_bkg_out->Branch( "H1_e", &user_H1_e_B  );
        theTree_bkg_out->Branch( "H1_pt", &user_H1_pt_B  );
        theTree_bkg_out->Branch( "H1_eta", &user_H1_eta_B  );
        theTree_bkg_out->Branch( "H2_e", &user_H2_e_B  );
        theTree_bkg_out->Branch( "H2_eta", &user_H2_eta_B  );
        theTree_bkg_out->Branch( "HH_e", &user_HH_e_B  );
        theTree_bkg_out->Branch( "HH_m", &user_HH_m_B  );
        theTree_bkg_out->Branch( "HH_eta", &user_HH_eta_B  );
        theTree_bkg_out->Branch( "dEta_H1_H2", &user_dEta_H1_H2_B  );
        theTree_bkg_out->Branch( "dPhi_H1_H2", &user_dPhi_H1_H2_B  );
        theTree_bkg_out->Branch( "dPhi_V_H2", &user_dPhi_V_H2_B  );
        theTree_bkg_out->Branch( "dR_H1_H2", &user_dR_H1_H2_B  );
        theTree_bkg_out->Branch( "pt_ratio", &user_pt_ratio_B  );
        
        sw.Start();
        for (Long64_t ievt=0; ievt<theTree_bkg->GetEntries(); ievt++) {
            if (ievt%1000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
            theTree_bkg->GetEntry(ievt);
            
            //#looping variables bkg
            user_V_e_B = V_e;
            user_V_pt_B = V_pt;
            user_H1_e_B = H1_e;
            user_H1_pt_B = H1_pt;
            user_H1_eta_B = H1_eta;
            user_H2_e_B = H2_e;
            user_H2_eta_B = H2_eta;
            user_HH_e_B = HH_e;
            user_HH_m_B = HH_m;
            user_HH_eta_B = HH_eta;
            user_dEta_H1_H2_B = dEta_H1_H2;
            user_dPhi_H1_H2_B = dPhi_H1_H2;
            user_dPhi_V_H2_B = dPhi_V_H2;
            user_dR_H1_H2_B = dR_H1_H2;
            user_pt_ratio = pt_ratio;

            theTree_bkg_out->Fill();

            // Return the MVA outputs and fill into histograms
            if (Use["BDT"])           {user_BDT_B  = reader->EvaluateMVA( "BDT method"            ); }
            if (Use["BDTG"])          {user_BDTG_B = reader->EvaluateMVA( "BDTG method"           ); }
            if (Use["BDTB"])          {user_BDTB_B = reader->EvaluateMVA( "BDTB method"           ); }
            if (Use["BDTD"])          {user_BDTD_B = reader->EvaluateMVA( "BDTD method"           ); }
            if (Use["BDTF"])          {user_BDTF_B = reader->EvaluateMVA( "BDTF method"           ); }
        }
        sw.Stop();
        std::cout << "--- End of background event loop: "; sw.Print();
        theTree_bkg_out ->Write();
    }

    target->Close();
    
    std::cout << "--- Created root file: \"TMVApp.root\" containing the MVA output histograms" << std::endl;
    delete reader;
    std::cout << "==> TMVAClassificationApplication is done!" << std::endl << std::endl;
}

int main( int argc, char** argv )
{
   TString methodList;
   for (int i=1; i<argc; i++) {
      TString regMethod(argv[i]);
      if(regMethod=="-b" || regMethod=="--batch") continue;
      if (!methodList.IsNull()) methodList += TString(",");
      methodList += regMethod;
   }
   LocalBDT_Coupling_Application(methodList);
   return 0;
}
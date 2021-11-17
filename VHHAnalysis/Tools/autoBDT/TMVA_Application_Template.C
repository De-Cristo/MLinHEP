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

void LocalBDT_TMVA_Application( TString myMethodList = "" ){
    //---------------------------------------------------------------
    TMVA::Tools::Instance();
    
    std::map<std::string,int> Use;
    
//     (TMVA::gConfig().GetVariablePlotting()).fNbins1D = 200;
    
    // Boosted Decision Trees
    Use["BDT"]             = 1; // uses Adaptive Boost
    Use["BDTG"]            = 0; // uses Gradient Boost
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
    #insert variables
    Float_t VHH_HH_m, VHH_HH_dR, VHH_HH_deta, VHH_HH_e, VHH_HH_eta, VHH_HH_pT, VHH_Vreco4j_HT, VHH_mass, VHH_vsptmassRatio, V_pt, VHH_V_phi, V_mass, VHH_H1_BJet1_e, VHH_H1_BJet1_eta, VHH_H1_BJet1_pT, VHH_H1_BJet1_phi, VHH_H1_e, VHH_H1_eta, VHH_H1_m, VHH_H1_pT, VHH_H1_phi, VHH_V_H1_dPhi, VHH_V_H2_dPhi, VHH_V_HH_dPhi, weight;
    
    reader->AddVariable( "VHH_HH_m", &VHH_HH_m );
    reader->AddVariable( "VHH_HH_dR", &VHH_HH_dR );
    reader->AddVariable( "VHH_HH_deta", &VHH_HH_deta );
    reader->AddVariable( "VHH_HH_e", &VHH_HH_e );
    reader->AddVariable( "VHH_HH_eta", &VHH_HH_eta );
    reader->AddVariable( "VHH_HH_pT", &VHH_HH_pT );
    reader->AddVariable( "VHH_Vreco4j_HT", &VHH_Vreco4j_HT );
    reader->AddVariable( "VHH_mass", &VHH_mass );
    reader->AddVariable( "VHH_vsptmassRatio", &VHH_vsptmassRatio );
    reader->AddVariable( "V_pt", &V_pt );
    reader->AddVariable( "VHH_V_phi", &VHH_V_phi );
    reader->AddVariable( "V_mass", &V_mass );
    reader->AddVariable( "VHH_H1_BJet1_e", &VHH_H1_BJet1_e );
    reader->AddVariable( "VHH_H1_BJet1_eta", &VHH_H1_BJet1_eta );
    reader->AddVariable( "VHH_H1_BJet1_pT", &VHH_H1_BJet1_pT );
    reader->AddVariable( "VHH_H1_BJet1_phi", &VHH_H1_BJet1_phi );
    reader->AddVariable( "VHH_H1_e", &VHH_H1_e );
    reader->AddVariable( "VHH_H1_eta", &VHH_H1_eta );
    reader->AddVariable( "VHH_H1_m", &VHH_H1_m );
    reader->AddVariable( "VHH_H1_pT", &VHH_H1_pT );
    reader->AddVariable( "VHH_H1_phi", &VHH_H1_phi );
    reader->AddVariable( "VHH_V_H1_dPhi", &VHH_V_H1_dPhi );
    reader->AddVariable( "VHH_V_H2_dPhi", &VHH_V_H2_dPhi );
    reader->AddVariable( "VHH_V_HH_dPhi", &VHH_V_HH_dPhi );

    
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
    
    // Book method(s)
    for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
        if (it->second) {
            TString methodName = TString(it->first) + TString(" method");
            TString weightfile = dir + prefix + TString("_") + TString(it->first) + TString(".weights.xml");
            reader->BookMVA( methodName, weightfile );
        }
    }
    
    // Book output histograms DEFAULT FIXME
//     UInt_t nbin = 100;
//     TH1F *histBdt_S(0);
//     TH1F *histBdtG_S(0);
//     TH1F *histBdtB_S(0);
//     TH1F *histBdtD_S(0);
//     TH1F *histBdtF_S(0);
    
//     TH1F *histBdt_B(0);
//     TH1F *histBdtG_B(0);
//     TH1F *histBdtB_B(0);
//     TH1F *histBdtD_B(0);
//     TH1F *histBdtF_B(0);
    
//     if (Use["BDT"])           histBdt_S     = new TH1F( "MVA_BDT_S",           "MVA_BDT_S",           nbin, -0.8, 0.8 );
//     if (Use["BDTG"])          histBdtG_S    = new TH1F( "MVA_BDTG_S",          "MVA_BDTG_S",          nbin, -1.0, 1.0 );
//     if (Use["BDTB"])          histBdtB_S    = new TH1F( "MVA_BDTB_S",          "MVA_BDTB_S",          nbin, -1.0, 1.0 );
//     if (Use["BDTD"])          histBdtD_S    = new TH1F( "MVA_BDTD_S",          "MVA_BDTD_S",          nbin, -0.8, 0.8 );
//     if (Use["BDTF"])          histBdtF_S    = new TH1F( "MVA_BDTF_S",          "MVA_BDTF_S",          nbin, -1.0, 1.0 );
    
//     if (Use["BDT"])           histBdt_B     = new TH1F( "MVA_BDT_B",           "MVA_BDT_B",           nbin, -0.8, 0.8 );
//     if (Use["BDTG"])          histBdtG_B    = new TH1F( "MVA_BDTG_B",          "MVA_BDTG_B",          nbin, -1.0, 1.0 );
//     if (Use["BDTB"])          histBdtB_B    = new TH1F( "MVA_BDTB_B",          "MVA_BDTB_B",          nbin, -1.0, 1.0 );
//     if (Use["BDTD"])          histBdtD_B    = new TH1F( "MVA_BDTD_B",          "MVA_BDTD_B",          nbin, -0.8, 0.8 );
//     if (Use["BDTF"])          histBdtF_B    = new TH1F( "MVA_BDTF_B",          "MVA_BDTF_B",          nbin, -1.0, 1.0 );
    
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
    TString fname_sig = "./VHH_BDT_Signal_Test.root";
    TString fname_bkg = "./VHH_BDT_Background_Test.root";
        
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
    
    TFile *target  = new TFile( "TMVApp.root","RECREATE" );
    
    #insert user variables sig
    Float_t user_VHH_HH_m, user_VHH_HH_dR, user_VHH_HH_deta, user_VHH_HH_e, user_VHH_HH_eta, user_VHH_HH_pT, user_VHH_Vreco4j_HT, user_VHH_mass, user_VHH_vsptmassRatio, user_V_pt, user_VHH_V_phi, user_V_mass, user_VHH_H1_BJet1_e, user_VHH_H1_BJet1_eta, user_VHH_H1_BJet1_pT, user_VHH_H1_BJet1_phi, user_VHH_H1_e, user_VHH_H1_eta, user_VHH_H1_m, user_VHH_H1_pT, user_VHH_H1_phi, user_VHH_V_H1_dPhi, user_VHH_V_H2_dPhi, user_VHH_V_HH_dPhi, user_weight, user_BDT, user_BDTG, user_BDTB, user_BDTD, user_BDTF;

    std::cout << "--- Select signal sample" << std::endl;
    TTree* theTree_sig = (TTree*)input_sig->Get("TreeS");
    TTree* theTree_sig_out = new TTree("Tree_sig", "Tree_sig");
    
    std::cout << "--- Processing: " << theTree_sig->GetEntries() << "signal events" << std::endl;
    
    if (Use["BDT"])           theTree_sig_out->Branch("user_BDT", &user_BDT);
    if (Use["BDTG"])          theTree_sig_out->Branch("user_BDTG", &user_BDTG);
    if (Use["BDTB"])          theTree_sig_out->Branch("user_BDTB", &user_BDTB);
    if (Use["BDTD"])          theTree_sig_out->Branch("user_BDTD", &user_BDTD);
    if (Use["BDTF"])          theTree_sig_out->Branch("user_BDTF", &user_BDTF);
    
    #link user variables sig
    theTree_sig->SetBranchAddress( "VHH_HH_m", &VHH_HH_m );
    theTree_sig->SetBranchAddress( "VHH_HH_dR", &VHH_HH_dR );
    theTree_sig->SetBranchAddress( "VHH_HH_deta", &VHH_HH_deta );
    theTree_sig->SetBranchAddress( "VHH_HH_e", &VHH_HH_e );
    theTree_sig->SetBranchAddress( "VHH_HH_eta", &VHH_HH_eta );
    theTree_sig->SetBranchAddress( "VHH_HH_pT", &VHH_HH_pT );
    theTree_sig->SetBranchAddress( "VHH_Vreco4j_HT", &VHH_Vreco4j_HT );
    theTree_sig->SetBranchAddress( "VHH_mass", &VHH_mass );
    theTree_sig->SetBranchAddress( "VHH_vsptmassRatio", &VHH_vsptmassRatio );
    theTree_sig->SetBranchAddress( "V_pt", &V_pt );
    theTree_sig->SetBranchAddress( "VHH_V_phi", &VHH_V_phi );
    theTree_sig->SetBranchAddress( "V_mass", &V_mass );
    theTree_sig->SetBranchAddress( "VHH_H1_BJet1_e", &VHH_H1_BJet1_e );
    theTree_sig->SetBranchAddress( "VHH_H1_BJet1_eta", &VHH_H1_BJet1_eta );
    theTree_sig->SetBranchAddress( "VHH_H1_BJet1_pT", &VHH_H1_BJet1_pT );
    theTree_sig->SetBranchAddress( "VHH_H1_BJet1_phi", &VHH_H1_BJet1_phi );
    theTree_sig->SetBranchAddress( "VHH_H1_e", &VHH_H1_e );
    theTree_sig->SetBranchAddress( "VHH_H1_eta", &VHH_H1_eta );
    theTree_sig->SetBranchAddress( "VHH_H1_m", &VHH_H1_m );
    theTree_sig->SetBranchAddress( "VHH_H1_pT", &VHH_H1_pT );
    theTree_sig->SetBranchAddress( "VHH_H1_phi", &VHH_H1_phi );
    theTree_sig->SetBranchAddress( "VHH_V_H1_dPhi", &VHH_V_H1_dPhi );
    theTree_sig->SetBranchAddress( "VHH_V_H2_dPhi", &VHH_V_H2_dPhi );
    theTree_sig->SetBranchAddress( "VHH_V_HH_dPhi", &VHH_V_HH_dPhi );
    theTree_sig->SetBranchAddress( "weight", &weight );
    
    theTree_sig_out->SetBranchAddress( "VHH_HH_m", &user_VHH_HH_m );
    theTree_sig_out->SetBranchAddress( "VHH_HH_dR", &user_VHH_HH_dR );
    theTree_sig_out->SetBranchAddress( "VHH_HH_deta", &user_VHH_HH_deta );
    theTree_sig_out->SetBranchAddress( "VHH_HH_e", &user_VHH_HH_e );
    theTree_sig_out->SetBranchAddress( "VHH_HH_eta", &user_VHH_HH_eta );
    theTree_sig_out->SetBranchAddress( "VHH_HH_pT", &user_VHH_HH_pT );
    theTree_sig_out->SetBranchAddress( "VHH_Vreco4j_HT", &user_VHH_Vreco4j_HT );
    theTree_sig_out->SetBranchAddress( "VHH_mass", &user_VHH_mass );
    theTree_sig_out->SetBranchAddress( "VHH_vsptmassRatio", &user_VHH_vsptmassRatio );
    theTree_sig_out->SetBranchAddress( "V_pt", &user_V_pt );
    theTree_sig_out->SetBranchAddress( "VHH_V_phi", &user_VHH_V_phi );
    theTree_sig_out->SetBranchAddress( "V_mass", &user_V_mass );
    theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_e", &user_VHH_H1_BJet1_e );
    theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_eta", &user_VHH_H1_BJet1_eta );
    theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_pT", &user_VHH_H1_BJet1_pT );
    theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_phi", &user_VHH_H1_BJet1_phi );
    theTree_sig_out->SetBranchAddress( "VHH_H1_e", &user_VHH_H1_e );
    theTree_sig_out->SetBranchAddress( "VHH_H1_eta", &user_VHH_H1_eta );
    theTree_sig_out->SetBranchAddress( "VHH_H1_m", &user_VHH_H1_m );
    theTree_sig_out->SetBranchAddress( "VHH_H1_pT", &user_VHH_H1_pT );
    theTree_sig_out->SetBranchAddress( "VHH_H1_phi", &user_VHH_H1_phi );
    theTree_sig_out->SetBranchAddress( "VHH_V_H1_dPhi", &user_VHH_V_H1_dPhi );
    theTree_sig_out->SetBranchAddress( "VHH_V_H2_dPhi", &user_VHH_V_H2_dPhi );
    theTree_sig_out->SetBranchAddress( "VHH_V_HH_dPhi", &user_VHH_V_HH_dPhi );
    theTree_sig_out->SetBranchAddress( "weight", &user_weight );
    
    TStopwatch sw;
    sw.Start();
    
    for (Long64_t ievt=0; ievt<theTree_sig->GetEntries(); ievt++) {
        if (ievt%100 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
        theTree_sig->GetEntry(ievt);
        
        #looping variables sig
        user_VHH_HH_m = VHH_HH_m;
        user_VHH_HH_dR = VHH_HH_dR;
        user_VHH_HH_deta = VHH_HH_deta;
        user_VHH_HH_e = VHH_HH_e;
        user_VHH_HH_eta = VHH_HH_eta;
        user_VHH_HH_pT = VHH_HH_pT;
        user_VHH_Vreco4j_HT = VHH_Vreco4j_HT;
        user_VHH_mass = VHH_mass;
        user_VHH_vsptmassRatio = VHH_vsptmassRatio;
        user_V_pt = V_pt;
        user_VHH_V_phi = VHH_V_phi;
        user_V_mass = V_mass;
        user_VHH_H1_BJet1_e = VHH_H1_BJet1_e;
        user_VHH_H1_BJet1_eta = VHH_H1_BJet1_eta;
        user_VHH_H1_BJet1_pT = VHH_H1_BJet1_pT;
        user_VHH_H1_BJet1_phi = VHH_H1_BJet1_phi;
        user_VHH_H1_e = VHH_H1_e;
        user_VHH_H1_eta = VHH_H1_eta;
        user_VHH_H1_m = VHH_H1_m;
        user_VHH_H1_pT = VHH_H1_pT;
        user_VHH_H1_phi = VHH_H1_phi;
        user_VHH_V_H2_dPhi = VHH_V_H2_dPhi;
        user_VHH_V_HH_dPhi = VHH_V_HH_dPhi;
        user_weight = weight;
        
        theTree_sig_out->Fill();
        
        // Return the MVA outputs and fill into histograms
        if (Use["BDT"])           {user_BDT  = reader->EvaluateMVA( "BDT method"            ); }
        if (Use["BDTG"])          {user_BDTG = reader->EvaluateMVA( "BDTG method"           ); }
        if (Use["BDTB"])          {user_BDTB = reader->EvaluateMVA( "BDTB method"           ); }
        if (Use["BDTD"])          {user_BDTD = reader->EvaluateMVA( "BDTD method"           ); }
        if (Use["BDTF"])          {user_BDTF = reader->EvaluateMVA( "BDTF method"           ); }
    }
    
    // Get elapsed time
    sw.Stop();
    std::cout << "--- End of signal event loop: "; sw.Print();
    theTree_sig_out ->Write();
    
    
    TTree* theTree_bkg_out = new TTree("Tree_bkg", "Tree_bkg");
    if (input_bkg) {
        if (Use["BDT"])           theTree_bkg_out->Branch("user_BDT", &user_BDT_B);
        if (Use["BDTG"])          theTree_bkg_out->Branch("user_BDTG", &user_BDTG_B);
        if (Use["BDTB"])          theTree_bkg_out->Branch("user_BDTB", &user_BDTB_B);
        if (Use["BDTD"])          theTree_bkg_out->Branch("user_BDTD", &user_BDTD_B);
        if (Use["BDTF"])          theTree_bkg_out->Branch("user_BDTF", &user_BDTF_B);
        
        std::cout << "--- Select background sample" << std::endl;
        TTree* theTree_bkg = (TTree*)input_bkg->Get("TreeB");
        std::cout << "--- Processing: " << theTree_bkg->GetEntries() << "background events" << std::endl;
        #link user variables bkg
        theTree_bkg->SetBranchAddress( "VHH_HH_m", &VHH_HH_m );
        theTree_bkg->SetBranchAddress( "VHH_HH_dR", &VHH_HH_dR );
        theTree_bkg->SetBranchAddress( "VHH_HH_deta", &VHH_HH_deta );
        theTree_bkg->SetBranchAddress( "VHH_HH_e", &VHH_HH_e );
        theTree_bkg->SetBranchAddress( "VHH_HH_eta", &VHH_HH_eta );
        theTree_bkg->SetBranchAddress( "VHH_HH_pT", &VHH_HH_pT );
        theTree_bkg->SetBranchAddress( "VHH_Vreco4j_HT", &VHH_Vreco4j_HT );
        theTree_bkg->SetBranchAddress( "VHH_mass", &VHH_mass );
        theTree_bkg->SetBranchAddress( "VHH_vsptmassRatio", &VHH_vsptmassRatio );
        theTree_bkg->SetBranchAddress( "V_pt", &V_pt );
        theTree_bkg->SetBranchAddress( "VHH_V_phi", &VHH_V_phi );
        theTree_bkg->SetBranchAddress( "V_mass", &V_mass );
        theTree_bkg->SetBranchAddress( "VHH_H1_BJet1_e", &VHH_H1_BJet1_e );
        theTree_bkg->SetBranchAddress( "VHH_H1_BJet1_eta", &VHH_H1_BJet1_eta );
        theTree_bkg->SetBranchAddress( "VHH_H1_BJet1_pT", &VHH_H1_BJet1_pT );
        theTree_bkg->SetBranchAddress( "VHH_H1_BJet1_phi", &VHH_H1_BJet1_phi );
        theTree_bkg->SetBranchAddress( "VHH_H1_e", &VHH_H1_e );
        theTree_bkg->SetBranchAddress( "VHH_H1_eta", &VHH_H1_eta );
        theTree_bkg->SetBranchAddress( "VHH_H1_m", &VHH_H1_m );
        theTree_bkg->SetBranchAddress( "VHH_H1_pT", &VHH_H1_pT );
        theTree_bkg->SetBranchAddress( "VHH_H1_phi", &VHH_H1_phi );
        theTree_bkg->SetBranchAddress( "VHH_V_H1_dPhi", &VHH_V_H1_dPhi );
        theTree_bkg->SetBranchAddress( "VHH_V_H2_dPhi", &VHH_V_H2_dPhi );
        theTree_bkg->SetBranchAddress( "VHH_V_HH_dPhi", &VHH_V_HH_dPhi );
        theTree_bkg->SetBranchAddress( "weight", &weight );

        theTree_sig_out->SetBranchAddress( "VHH_HH_m", &user_VHH_HH_m );
        theTree_sig_out->SetBranchAddress( "VHH_HH_dR", &user_VHH_HH_dR );
        theTree_sig_out->SetBranchAddress( "VHH_HH_deta", &user_VHH_HH_deta );
        theTree_sig_out->SetBranchAddress( "VHH_HH_e", &user_VHH_HH_e );
        theTree_sig_out->SetBranchAddress( "VHH_HH_eta", &user_VHH_HH_eta );
        theTree_sig_out->SetBranchAddress( "VHH_HH_pT", &user_VHH_HH_pT );
        theTree_sig_out->SetBranchAddress( "VHH_Vreco4j_HT", &user_VHH_Vreco4j_HT );
        theTree_sig_out->SetBranchAddress( "VHH_mass", &user_VHH_mass );
        theTree_sig_out->SetBranchAddress( "VHH_vsptmassRatio", &user_VHH_vsptmassRatio );
        theTree_sig_out->SetBranchAddress( "V_pt", &user_V_pt );
        theTree_sig_out->SetBranchAddress( "VHH_V_phi", &user_VHH_V_phi );
        theTree_sig_out->SetBranchAddress( "V_mass", &user_V_mass );
        theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_e", &user_VHH_H1_BJet1_e );
        theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_eta", &user_VHH_H1_BJet1_eta );
        theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_pT", &user_VHH_H1_BJet1_pT );
        theTree_sig_out->SetBranchAddress( "VHH_H1_BJet1_phi", &user_VHH_H1_BJet1_phi );
        theTree_sig_out->SetBranchAddress( "VHH_H1_e", &user_VHH_H1_e );
        theTree_sig_out->SetBranchAddress( "VHH_H1_eta", &user_VHH_H1_eta );
        theTree_sig_out->SetBranchAddress( "VHH_H1_m", &user_VHH_H1_m );
        theTree_sig_out->SetBranchAddress( "VHH_H1_pT", &user_VHH_H1_pT );
        theTree_sig_out->SetBranchAddress( "VHH_H1_phi", &user_VHH_H1_phi );
        theTree_sig_out->SetBranchAddress( "VHH_V_H1_dPhi", &user_VHH_V_H1_dPhi );
        theTree_sig_out->SetBranchAddress( "VHH_V_H2_dPhi", &user_VHH_V_H2_dPhi );
        theTree_sig_out->SetBranchAddress( "VHH_V_HH_dPhi", &user_VHH_V_HH_dPhi );
        theTree_sig_out->SetBranchAddress( "weight", &user_weight );
        
        sw.Start();
        for (Long64_t ievt=0; ievt<theTree_bkg->GetEntries(); ievt++) {
            if (ievt%100 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
            theTree_bkg->GetEntry(ievt);
            
            #looping variables bkg
            user_VHH_HH_m = VHH_HH_m;
            user_VHH_HH_dR = VHH_HH_dR;
            user_VHH_HH_deta = VHH_HH_deta;
            user_VHH_HH_e = VHH_HH_e;
            user_VHH_HH_eta = VHH_HH_eta;
            user_VHH_HH_pT = VHH_HH_pT;
            user_VHH_Vreco4j_HT = VHH_Vreco4j_HT;
            user_VHH_mass = VHH_mass;
            user_VHH_vsptmassRatio = VHH_vsptmassRatio;
            user_V_pt = V_pt;
            user_VHH_V_phi = VHH_V_phi;
            user_V_mass = V_mass;
            user_VHH_H1_BJet1_e = VHH_H1_BJet1_e;
            user_VHH_H1_BJet1_eta = VHH_H1_BJet1_eta;
            user_VHH_H1_BJet1_pT = VHH_H1_BJet1_pT;
            user_VHH_H1_BJet1_phi = VHH_H1_BJet1_phi;
            user_VHH_H1_e = VHH_H1_e;
            user_VHH_H1_eta = VHH_H1_eta;
            user_VHH_H1_m = VHH_H1_m;
            user_VHH_H1_pT = VHH_H1_pT;
            user_VHH_H1_phi = VHH_H1_phi;
            user_VHH_V_H2_dPhi = VHH_V_H2_dPhi;
            user_VHH_V_HH_dPhi = VHH_V_HH_dPhi;
            user_weight = weight;

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
   LocalBDT_TMVA_Application(methodList);
   return 0;
}
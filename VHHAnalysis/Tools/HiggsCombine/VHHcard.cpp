#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;

int main(int argc, char *argv[]) {

  if(argc!=3){
    cerr << "Invalid arguments provided, correct format is: ./main channel inputhist\n";
    exit(0);
  }

  string channelname = argv[1];
  string inputhist = argv[2];

  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/MyWorkArea/";

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  ch::Categories cats = {
      {1, "VHH"}
    };
  // ch::Categories is just a typedef of vector<pair<int, string>>
  //! [part1]


  //! [part2]
  vector<string> masses = ch::MassesFromRange("120-135:5");
  // Or equivalently, specify the mass points explicitly:
  //    vector<string> masses = {"120", "125", "130", "135"};
  //! [part2]

  //! [part3]
  cb.AddObservations({""}, {""}, {""}, {""}, cats);
  //! [part3]

  //! [part4]
  //vector<string> sig_procs = {"morphsignaltestCV8"};
  vector<string> sig_procs = {"VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_0_hbbhbb", "VHH_CV_1_C2V_1_kl_20_hbbhbb"};
  cb.AddProcesses({""}, {""}, {""}, {""}, sig_procs, cats, true);

  vector<string> bkg_procs;
  if(inputhist.find("Wenu")!=string::npos || inputhist.find("Wmunu")!=string::npos || inputhist.find("wenu")!=string::npos || inputhist.find("wmunu")!=string::npos)
    bkg_procs = {"TT", "TTB", "s_Top"};
  else if(inputhist.find("VhadHH")!=string::npos)
    bkg_procs = {"multijet_background", "ttbar_background"};
  else if(inputhist.find("Zmm")!=string::npos || inputhist.find("Zee")!=string::npos || inputhist.find("Zll")!=string::npos)
    bkg_procs = {"TT", "TTB", "DY", "s_Top", "ttH", "TTV"};
//     bkg_procs = {"TT", "TTB", "DY"};
  else if(inputhist.find("Znn")!=string::npos || inputhist.find("znn")!=string::npos)  
    bkg_procs = {"TT", "TTB", "s_Top"};
  cb.AddProcesses({""}, {""}, {""}, {""}, bkg_procs, cats, false);
  //! [part4]


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::SystMapAsymm;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;


 
  if(inputhist.find("Wenu")!=string::npos || inputhist.find("Wmunu")!=string::npos || inputhist.find("Znn")!=string::npos || inputhist.find("wenu")!=string::npos || inputhist.find("wmunu")!=string::npos || inputhist.find("znn")!=string::npos) {
    cb.cp().AddSyst(cb, "lumi_13TeV_2018", "lnN", SystMap<>::init(1.025));
    cb.cp().AddSyst(cb, "BR_hbb", "lnN", SystMapAsymm<>::init(0.9747, 1.0248));

    cb.cp().signals().AddSyst(cb, "pdf_Higgs_VHH", "lnN", SystMap<>::init(1.028));
    cb.cp().signals().AddSyst(cb, "QCDscale_VHH", "lnN", SystMapAsymm<>::init(0.973, 1.034));

    cb.cp().AddSyst(cb, "CMS_pileup_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_HF_2016_2017_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_LF_2016_2017_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_cferr1_2016_2017_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_cferr2_2016_2017_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_hfstats1_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_hfstats2_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_lfstats1_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_lfstats2_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_btag_jes_2018", "shape", SystMap<>::init(1.00));
    cb.cp().AddSyst(cb, "CMS_PNet_2018", "shape", SystMap<>::init(1.00));
    if(inputhist.find("Wenu")!=string::npos || inputhist.find("wenu")!=string::npos)
      cb.cp().AddSyst(cb, "CMS_eff_e_2018", "shape", SystMap<>::init(1.00));
    if(inputhist.find("Wmunu")!=string::npos || inputhist.find("wmunu")!=string::npos)
      cb.cp().AddSyst(cb, "CMS_eff_m_2018", "shape", SystMap<>::init(1.00));
    if(inputhist.find("BBDT")!=string::npos ) {
      //cb.cp().process({"TT", "TTB"}).AddSyst(cb, "CMS_BRewError1_2018", "shape", SystMap<>::init(1.00));
      cb.cp().process({"TT", "TTB"}).AddSyst(cb, "CMS_BRewError2_2018", "shape", SystMap<>::init(1.00));
    }

  } else if (inputhist.find("Zmm")!=string::npos || inputhist.find("Zee")!=string::npos || inputhist.find("Zll")!=string::npos) {
      if (inputhist.find("2018")!=string::npos){
        cb.cp().AddSyst(cb, "lumi_13TeV_2018", "lnN", SystMap<>::init(1.015));
        cb.cp().AddSyst(cb, "lumi_13TeV_1718", "lnN", SystMap<>::init(1.002));
        cb.cp().AddSyst(cb, "lumi_13TeV_correlated", "lnN", SystMap<>::init(1.020));
        cb.cp().AddSyst(cb, "BR_hbb", "lnN", SystMapAsymm<>::init(0.9747, 1.0248));

        cb.cp().signals().AddSyst(cb, "pdf_Higgs_VHH", "lnN", SystMap<>::init(1.028));
        cb.cp().signals().AddSyst(cb, "QCDscale_VHH", "lnN", SystMapAsymm<>::init(0.973, 1.034));

        cb.cp().AddSyst(cb, "CMS_pileup_2018", "shape", SystMap<>::init(1.00));
          
        cb.cp().AddSyst(cb, "CMS_btag_HF_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_LF_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_cferr1_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_cferr2_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_hfstats1_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_hfstats2_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_lfstats1_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_lfstats2_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_jes_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_PNet_2018", "shape", SystMap<>::init(1.00));

        cb.cp().AddSyst(cb, "CMS_res_j_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_Abs", "shape", SystMap<>::init(1.00));
        
        cb.cp().AddSyst(cb, "CMS_scale_j_Abs_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_BBEC1", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_BBEC1_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_EC2", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_EC2_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_FlavQCD", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_HF", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_HF_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_RelBal", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_RelSample_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_MSD_JMS_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_MSD_JMR_2018", "shape", SystMap<>::init(1.00));
        cb.cp().process(sig_procs).AddSyst(cb, "CMS_ZHHNNLO", "shape", SystMap<>::init(1.00));
          
        cb.cp().AddSyst(cb, "CMS_eff_m_2018", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DYNLO_P0_", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DYNLO_P1_", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DY_RwT", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).AddSyst(cb, "CMS_TT_RwT", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTB"}).AddSyst(cb, "CMS_TTB_RwT", "shape", SystMap<>::init(1.00));
        float TT_prefit=1.0;
        float DY_prefit=1.0;
        cb.cp().process({"TT","TTB"}).AddSyst(cb, "CMS_TT_norm_2016_2017_2018", "rateParam", SystMap<>::init(TT_prefit));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DY_norm_2016_2017_2018", "rateParam", SystMap<>::init(DY_prefit));
      }
      else if (inputhist.find("2017")!=string::npos){
        cb.cp().AddSyst(cb, "lumi_13TeV_2017", "lnN", SystMap<>::init(1.020));
        cb.cp().AddSyst(cb, "lumi_13TeV_1718", "lnN", SystMap<>::init(1.006));
        cb.cp().AddSyst(cb, "lumi_13TeV_correlated", "lnN", SystMap<>::init(1.009));
        cb.cp().AddSyst(cb, "BR_hbb", "lnN", SystMapAsymm<>::init(0.9747, 1.0248));

        cb.cp().signals().AddSyst(cb, "pdf_Higgs_VHH", "lnN", SystMap<>::init(1.028));
        cb.cp().signals().AddSyst(cb, "QCDscale_VHH", "lnN", SystMapAsymm<>::init(0.973, 1.034));

        cb.cp().AddSyst(cb, "CMS_pileup_2017", "shape", SystMap<>::init(1.00));
          
        cb.cp().AddSyst(cb, "CMS_btag_HF_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_LF_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_cferr1_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_cferr2_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_hfstats1_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_hfstats2_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_lfstats1_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_lfstats2_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_jes_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_PNet_2017", "shape", SystMap<>::init(1.00));

        cb.cp().AddSyst(cb, "CMS_res_j_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_Abs", "shape", SystMap<>::init(1.00));
        
        cb.cp().AddSyst(cb, "CMS_scale_j_Abs_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_BBEC1", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_BBEC1_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_EC2", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_EC2_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_FlavQCD", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_HF", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_HF_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_RelBal", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_RelSample_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_MSD_JMS_2017", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_MSD_JMR_2017", "shape", SystMap<>::init(1.00));
        cb.cp().process(sig_procs).AddSyst(cb, "CMS_ZHHNNLO", "shape", SystMap<>::init(1.00));
          
        cb.cp().AddSyst(cb, "CMS_eff_m_2017", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DYNLO_P0_", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DYNLO_P1_", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DY_RwT", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).AddSyst(cb, "CMS_TT_RwT", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTB"}).AddSyst(cb, "CMS_TTB_RwT", "shape", SystMap<>::init(1.00));
        float TT_prefit=1.0;
        float DY_prefit=1.0;
        cb.cp().process({"TT","TTB"}).AddSyst(cb, "CMS_TT_norm_2016_2017_2018", "rateParam", SystMap<>::init(TT_prefit));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DY_norm_2016_2017_2018", "rateParam", SystMap<>::init(DY_prefit));
      }
      else if (inputhist.find("2016")!=string::npos){
        cb.cp().AddSyst(cb, "lumi_13TeV_2016", "lnN", SystMap<>::init(1.010));
        cb.cp().AddSyst(cb, "lumi_13TeV_correlated", "lnN", SystMap<>::init(1.006));
        cb.cp().AddSyst(cb, "BR_hbb", "lnN", SystMapAsymm<>::init(0.9747, 1.0248));

        cb.cp().signals().AddSyst(cb, "pdf_Higgs_VHH", "lnN", SystMap<>::init(1.028));
        cb.cp().signals().AddSyst(cb, "QCDscale_VHH", "lnN", SystMapAsymm<>::init(0.973, 1.034));

        cb.cp().AddSyst(cb, "CMS_pileup_2016", "shape", SystMap<>::init(1.00));
          
        cb.cp().AddSyst(cb, "CMS_btag_HF_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_LF_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_cferr1_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_cferr2_2016_2017_2018", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_hfstats1_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_hfstats2_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_lfstats1_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_lfstats2_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_btag_jes_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_PNet_2016", "shape", SystMap<>::init(1.00));

        cb.cp().AddSyst(cb, "CMS_res_j_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_Abs", "shape", SystMap<>::init(1.00));
        
        cb.cp().AddSyst(cb, "CMS_scale_j_Abs_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_BBEC1", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_BBEC1_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_EC2", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_EC2_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_FlavQCD", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_HF", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_HF_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_RelBal", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_scale_j_RelSample_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_MSD_JMS_2016", "shape", SystMap<>::init(1.00));
        cb.cp().AddSyst(cb, "CMS_MSD_JMR_2016", "shape", SystMap<>::init(1.00));
        cb.cp().process(sig_procs).AddSyst(cb, "CMS_ZHHNNLO", "shape", SystMap<>::init(1.00));
          
        cb.cp().AddSyst(cb, "CMS_eff_m_2016", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DYNLO_P0_", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DYNLO_P1_", "shape", SystMap<>::init(1.00));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DY_RwT", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TT"}).AddSyst(cb, "CMS_TT_RwT", "shape", SystMap<>::init(1.00));
        cb.cp().process({"TTB"}).AddSyst(cb, "CMS_TTB_RwT", "shape", SystMap<>::init(1.00));
        float TT_prefit=1.0;
        float DY_prefit=1.0;
        cb.cp().process({"TT","TTB"}).AddSyst(cb, "CMS_TT_norm_2016_2017_2018", "rateParam", SystMap<>::init(TT_prefit));
        cb.cp().process({"DY"}).AddSyst(cb, "CMS_DY_norm_2016_2017_2018", "rateParam", SystMap<>::init(DY_prefit));
      }
    

  } else if(inputhist.find("VhadHH")!=string::npos) {

    cb.cp().AddSyst(cb, "lumi_13TeV_2018", "lnN", SystMap<>::init(1.025));
    cb.cp().AddSyst(cb, "BR_hbb", "lnN", SystMapAsymm<>::init(0.9747, 1.0248));

    cb.cp().signals().AddSyst(cb, "pdf_Higgs_VHH", "lnN", SystMap<>::init(1.028));
    cb.cp().signals().AddSyst(cb, "QCDscale_VHH", "lnN", SystMapAsymm<>::init(0.973, 1.034));

  }

  //! [part7]
  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + inputhist,
      "$PROCESS",
      "$PROCESS_$SYSTEMATIC"
      );
  cb.cp().signals().ExtractShapes(
      aux_shapes + inputhist,
      "$PROCESS",
      "$PROCESS_$SYSTEMATIC"
      );
  //! [part7]

  //! [part8]
  auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.1)
    .SetFixNorm(true);

  //bbb.AddBinByBin(cb.cp().backgrounds(), cb);

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
  TFile output(("shapefile_"+channelname+".root").c_str(), "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  //for (auto b : bins) {
    //for (auto m : masses) {
      //cout << ">> Writing datacard for bin: " << b << " and mass: " << m << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().WriteDatacard("card_"+channelname+".txt", output);
    //}
  //}
  //! [part9]

}
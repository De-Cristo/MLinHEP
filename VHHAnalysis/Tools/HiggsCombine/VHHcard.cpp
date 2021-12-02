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
      {1, "hadronic"}
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
  vector<string> sig_procs = {"VHH_CV_0p5_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_0_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_1_hbbhbb", "VHH_CV_1_C2V_1_kl_2_hbbhbb", "VHH_CV_1_C2V_2_kl_1_hbbhbb", "VHH_CV_1p5_C2V_1_kl_1_hbbhbb"};
  cb.AddProcesses({""}, {""}, {""}, {""}, sig_procs, cats, true);

  vector<string> bkg_procs;
  if(inputhist.find("nu_S")!=string::npos)
    bkg_procs = {"ttbb", "ttbar", "WplusB", "Wplusudsg", "ZplusB", "Zplusudsg", "ttHbb"};
  else if(inputhist.find("hadrhist")!=string::npos)
    bkg_procs = {"multijet_background", "ttbar_background"};
  else if(inputhist.find("Znn")!=string::npos)
    bkg_procs = {"TT","TTB"}; //{"TT", "ttHTobb", "DYBJets", "DYToLL", "DYJets_BGenFilter"};
  else if(inputhist.find("Zee")!=string::npos)
    bkg_procs = {"TT", "TTB", "DY"}; //{"TT", "ttHTobb", "DYBJets", "DYToLL", "DYJets_BGenFilter"};
  else if(inputhist.find("Zmm")!=string::npos)
    bkg_procs = {"TT", "TTB", "DY"}; //{"DY", "TT", "ST"};
  else if(inputhist.find("Zll")!=string::npos)
    bkg_procs = {"TT", "TTB", "DY"}; //{"DY", "TT", "ST"};
  else if(inputhist.find("WHH_")!=string::npos)
    bkg_procs = {"ttbb", "ttbar", "ttHbb"};
  cb.AddProcesses({""}, {""}, {""}, {""}, bkg_procs, cats, false);
  //! [part4]


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;


  //! [part5]
  //cb.cp().signals().AddSyst(cb, "lumi", "lnN", SystMap<>::init(1.02));
  //! [part5]

  //! [part6]
/*  cb.cp().process({"ggH"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.097));

  cb.cp().process(ch::JoinStr({sig_procs, {"ZTT", "TT"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp()
      .AddSyst(cb,
        "CMS_scale_j_$ERA", "lnN", SystMap<era, bin_id, process>::init
        ({"8TeV"}, {1},     {"ggH"},        1.04)
        ({"8TeV"}, {1},     {"qqH"},        0.99)
        ({"8TeV"}, {2},     {"ggH"},        1.10)
        ({"8TeV"}, {2},     {"qqH"},        1.04)
        ({"8TeV"}, {2},     {"TT"},         1.05));

  cb.cp().process(ch::JoinStr({sig_procs, {"ZTT"}}))
      .AddSyst(cb, "CMS_scale_t_mutau_$ERA", "shape", SystMap<>::init(1.00));
*/
  //! [part6]


  //! [part7]
  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + inputhist,
      "$PROCESS",
      "$PROCESS"
      );
  cb.cp().signals().ExtractShapes(
      aux_shapes + inputhist,
      "$PROCESS",
      "$PROCESS"
      );
  //! [part7]

/*  //! [part8]
  auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.1)
    .SetFixNorm(true);

  bbb.AddBinByBin(cb.cp().backgrounds(), cb);

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]
*/
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

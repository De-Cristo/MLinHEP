void temp(){
    TFile * fin = new TFile("reco.root","read");
    TTree * tin = (TTree*)fin->Get("Events");
    int nevent = tin->GetEntries();
    std::cout<< nevent <<std::endl;
}
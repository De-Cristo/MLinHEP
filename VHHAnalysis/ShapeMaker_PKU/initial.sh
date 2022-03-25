export ORIG_DIR=$PWD
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_11_0_0_pre6
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd $ORIG_DIR

# python VHH4b_shapeMaker.py -samp WHHTo4B_CV_1_0_C2V_1_0_C3_1_0 --skipsysts --multithread

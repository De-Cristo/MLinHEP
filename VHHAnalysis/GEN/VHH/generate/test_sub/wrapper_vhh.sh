#!/bin/bash

# export X509_USER_PROXY=$1
# voms-proxy-info -all
# voms-proxy-info -all -file $1

#download gridpack
wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_gridpack/ZHH_CV_1_0_C2V_10_0_C3_1_0_13TeV-madgraph_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"


#################=================================#########################################
#step 1 GEN

wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_script/HIG-RunIISummer20UL18wmLHEGEN-02886_pri.sh"

source HIG-RunIISummer20UL18wmLHEGEN-02886_pri.sh $2

sed -i "s/\/cvmfs\/cms.cern.ch\/phys_generator\/gridpacks\/UL\/13TeV\/madgraph\/V5_2.6.5\/ZHH_CV_1_0_C2V_1_0_C3_20_0_13TeV-madgraph\/v1\/ZHH_CV_1_0_C2V_1_0_C3_20_0_13TeV-madgraph_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/..\/ZHH_CV_1_0_C2V_10_0_C3_1_0_13TeV-madgraph_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/g" HIG-RunIISummer20UL18wmLHEGEN-02886_1_cfg.py

# Run generated config
REPORT_NAME=HIG-RunIISummer20UL18wmLHEGEN-02886_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIISummer20UL18wmLHEGEN-02886_1_cfg.py || exit $? ;

rm -rfv HIG-RunIISummer20UL18wmLHEGEN-02886_inLHE.root HIG-RunIISummer20UL18wmLHEGEN-02886_1_cfg.py HIG-RunIISummer20UL18wmLHEGEN-02886_pri.sh


#################=================================#########################################
#step 2 SIM

wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_script/HIG-RunIISummer20UL18SIM-02326_pri.sh"

source HIG-RunIISummer20UL18SIM-02326_pri.sh

# Run generated config
REPORT_NAME=HIG-RunIISummer20UL18SIM-02326_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIISummer20UL18SIM-02326_1_cfg.py || exit $? ;

rm -rfv HIG-RunIISummer20UL18SIM-02326_1_cfg.py HIG-RunIISummer20UL18wmLHEGEN-02886.root


#################=================================#########################################
#step 3 DIGIPremix

wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_script/HIG-RunIISummer20UL18DIGIPremix-02307_pri.sh"

source HIG-RunIISummer20UL18DIGIPremix-02307_pri.sh

# Run generated config
REPORT_NAME=HIG-RunIISummer20UL18DIGIPremix-02307_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIISummer20UL18DIGIPremix-02307_1_cfg.py || exit $? ;

rm -rfv HIG-RunIISummer20UL18DIGIPremix-02307_1_cfg.py HIG-RunIISummer20UL18SIM-02326.root 

#################=================================#########################################
#step 4 HLT

wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_script/HIG-RunIISummer20UL18HLT-02326_pri.sh"

source HIG-RunIISummer20UL18HLT-02326_pri.sh

# Run generated config
REPORT_NAME=HIG-RunIISummer20UL18HLT-02326_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIISummer20UL18HLT-02326_1_cfg.py || exit $? ;

rm -rfv HIG-RunIISummer20UL18HLT-02326_1_cfg.py HIG-RunIISummer20UL18DIGIPremix-02307.root


#################=================================#########################################
#step 5 RECO

wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_script/HIG-RunIISummer20UL18RECO-02326_pri.sh"

source HIG-RunIISummer20UL18RECO-02326_pri.sh

# Run generated config
REPORT_NAME=HIG-RunIISummer20UL18RECO-02326_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIISummer20UL18RECO-02326_1_cfg.py || exit $? ;

rm -rfv HIG-RunIISummer20UL18RECO-02326_1_cfg.py HIG-RunIISummer20UL18HLT-02326.root


#################=================================#########################################
#step 6 MINIAOD

wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_script/HIG-RunIISummer20UL18MiniAOD-01364_pri.sh"

source HIG-RunIISummer20UL18MiniAOD-01364_pri.sh

# Run generated config
REPORT_NAME=HIG-RunIISummer20UL18MiniAOD-01364_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIISummer20UL18MiniAOD-01364_1_cfg.py || exit $? ;

rm -rfv HIG-RunIISummer20UL18MiniAOD-01364_1_cfg.py HIG-RunIISummer20UL18RECO-02326.root


#################=================================#########################################
#step 7 NANOAOD

wget --no-check-certificate --progress=bar "https://lichengz.web.cern.ch/lichengz/private_generation/private_script/HIG-RunIISummer20UL18NanoAODv2-00415_pri.sh"

source HIG-RunIISummer20UL18NanoAODv2-00415_pri.sh

# Run generated config
REPORT_NAME=HIG-RunIISummer20UL18NanoAODv2-00415_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIISummer20UL18NanoAODv2-00415_1_cfg.py || exit $? ;

rm -rfv HIG-RunIISummer20UL18NanoAODv2-00415_1_cfg.py HIG-RunIISummer20UL18MiniAOD-01364.root


#################=================================#########################################
#step 8 EndJob

echo 'Ending Job...'
rm -rf CMSSW_* *.tar.xz *.py

echo 'Closing...'
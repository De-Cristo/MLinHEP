#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_28/src ] ; then
  echo release CMSSW_10_6_28 already exists
else
  scram p CMSSW CMSSW_10_6_28
fi
cd CMSSW_10_6_28/src
eval `scram runtime -sh`

# Download fragment from McM
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIISummer20UL18wmLHEGEN-02886 --retry 3 --create-dirs -o Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-02886-fragment.py
[ -s Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-02886-fragment.py ] || exit $?;

scram b
cd ../..

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 2.1141s
# Threads for each sequence: 1
# Time per event for single thread for each sequence: 1 * 2.1141s = 2.1141s
# Which adds up to 2.1141s per event
# Single core events that fit in validation duration: 20160s / 2.1141s = 9535
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 9535 and 10000, but more than 0 -> 9535
# It is estimated that this validation will produce: 9535 * 1.0000 = 9535 events
EVENTS=$1

cmsDriver.py Configuration/GenProduction/python/HIG-RunIISummer20UL18wmLHEGEN-02886-fragment.py --python_filename HIG-RunIISummer20UL18wmLHEGEN-02886_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:HIG-RunIISummer20UL18wmLHEGEN-02886.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" --step LHE,GEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n $EVENTS || exit $? ;

#END!!

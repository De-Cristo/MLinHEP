#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_17_patch1/src ] ; then
  echo release CMSSW_10_6_17_patch1 already exists
else
  scram p CMSSW CMSSW_10_6_17_patch1
fi
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

scram b
cd ../..

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 2.4300s
# Threads for each sequence: 4
# Time per event for single thread for each sequence: 4 * 2.4300s = 9.7200s
# Which adds up to 9.7200s per event
# Single core events that fit in validation duration: 20160s / 9.7200s = 2074
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 2074 and 10000, but more than 0 -> 2074
# It is estimated that this validation will produce: 2074 * 1.0000 = 2074 events
EVENTS=-1

# cmsDriver command
cmsDriver.py  --python_filename HIG-RunIISummer20UL18SIM-02326_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:HIG-RunIISummer20UL18SIM-02326.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --filein file:HIG-RunIISummer20UL18wmLHEGEN-02886.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;

#END!!!
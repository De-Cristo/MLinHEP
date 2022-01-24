#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_16_UL/src ] ; then
  echo release CMSSW_10_2_16_UL already exists
else
  scram p CMSSW CMSSW_10_2_16_UL
fi
cd CMSSW_10_2_16_UL/src
eval `scram runtime -sh`

scram b
cd ../..

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 3.0991s
# Threads for each sequence: 4
# Time per event for single thread for each sequence: 4 * 3.0991s = 12.3964s
# Which adds up to 12.3964s per event
# Single core events that fit in validation duration: 20160s / 12.3964s = 1626
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 1626 and 10000, but more than 0 -> 1626
# It is estimated that this validation will produce: 1626 * 1.0000 = 1626 events
EVENTS=-1

# cmsDriver command
cmsDriver.py  --python_filename HIG-RunIISummer20UL18HLT-02326_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:HIG-RunIISummer20UL18HLT-02326.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2018v32 --geometry DB:Extended --filein file:HIG-RunIISummer20UL18DIGIPremix-02307.root --era Run2_2018 --no_exec --mc -n $EVENTS || exit $? ;

#END!!!
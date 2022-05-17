#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_19_patch2/src ] ; then
  echo release CMSSW_10_6_19_patch2 already exists
else
  scram p CMSSW CMSSW_10_6_19_patch2
fi
cd CMSSW_10_6_19_patch2/src
eval `scram runtime -sh`

scram b
cd ../..

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 0.4300s
# Threads for each sequence: 4
# Time per event for single thread for each sequence: 4 * 0.4300s = 1.7200s
# Which adds up to 1.7200s per event
# Single core events that fit in validation duration: 20160s / 1.7200s = 11720
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 11720 and 10000, but more than 0 -> 10000
# It is estimated that this validation will produce: 10000 * 1.0000 = 10000 events
EVENTS=-1

# cmsDriver command
cmsDriver.py  --python_filename HIG-RunIISummer20UL18NanoAODv2-00415_1_cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv2-00415.root --conditions 106X_upgrade2018_realistic_v15_L1v1 --step NANO --filein file:HIG-RunIISummer20UL18MiniAOD-01364.root --era Run2_2018,run2_nanoAOD_106Xv1 --no_exec --mc -n $EVENTS || exit $? ;

#END!!!
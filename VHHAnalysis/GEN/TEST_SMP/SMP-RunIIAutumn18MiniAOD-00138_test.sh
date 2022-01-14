#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_5/src ] ; then
  echo release CMSSW_10_2_5 already exists
else
  scram p CMSSW CMSSW_10_2_5
fi
cd CMSSW_10_2_5/src
eval `scram runtime -sh`

scram b
cd ../..

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 0.6700s
# Threads for each sequence: 8
# Time per event for single thread for each sequence: 8 * 0.6700s = 5.3600s
# Which adds up to 5.3600s per event
# Single core events that fit in validation duration: 20160s / 5.3600s = 3761
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 3761 and 10000, but more than 0 -> 3761
# It is estimated that this validation will produce: 3761 * 1.0000 = 3761 events
EVENTS=-1


# cmsDriver command
cmsDriver.py  --python_filename SMP-RunIIAutumn18MiniAOD-00138_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:SMP-RunIIAutumn18MiniAOD-00138.root --conditions 102X_upgrade2018_realistic_v15 --step PAT --geometry DB:Extended --filein file:SMP-RunIIAutumn18DRPremix-00138.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;

# Run generated config
# Run the cmsRun
#cmsRun -e -j $REPORT_NAME SMP-RunIIAutumn18MiniAOD-00138_1_cfg.py || exit $? ;

# End of SMP-RunIIAutumn18MiniAOD-00138_test.sh file

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
# Time per event for each sequence: 0.9940s, 1.1987s
# Threads for each sequence: 8, 8
# Time per event for single thread for each sequence: 8 * 0.9940s = 7.9520s, 8 * 1.1987s = 9.5896s
# Which adds up to 17.5416s per event
# Single core events that fit in validation duration: 20160s / 17.5416s = 1149
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 1149 and 10000, but more than 0 -> 1149
# It is estimated that this validation will produce: 1149 * 1.0000 = 1149 events
EVENTS=-1


# cmsDriver command
cmsDriver.py  --python_filename SMP-RunIIAutumn18DRPremix-00138_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:SMP-RunIIAutumn18DRPremix-00138_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" --conditions 102X_upgrade2018_realistic_v15 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --geometry DB:Extended --filein file:SMP-RunIIFall18wmLHEGS-00112.root --datamix PreMix --era Run2_2018 --no_exec --mc -n $EVENTS || exit $? ;

# Run generated config
# Run the cmsRun
#cmsRun -e -j $REPORT_NAME SMP-RunIIAutumn18DRPremix-00138_1_cfg.py || exit $? ;

# cmsDriver command
cmsDriver.py  --python_filename SMP-RunIIAutumn18DRPremix-00138_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:SMP-RunIIAutumn18DRPremix-00138.root --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --filein file:SMP-RunIIAutumn18DRPremix-00138_0.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;

# Run generated config
# Run the cmsRun
#cmsRun -e -j $REPORT_NAME SMP-RunIIAutumn18DRPremix-00138_2_cfg.py || exit $? ;

# Parse values from SMP-RunIIAutumn18DRPremix-00138_report.xml report

# End of SMP-RunIIAutumn18DRPremix-00138_test.sh file

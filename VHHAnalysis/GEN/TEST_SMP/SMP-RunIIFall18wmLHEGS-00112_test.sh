#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_11_patch1/src ] ; then
  echo release CMSSW_10_2_11_patch1 already exists
else
  scram p CMSSW CMSSW_10_2_11_patch1
fi
cd CMSSW_10_2_11_patch1/src
eval `scram runtime -sh`

# Download fragment from McM
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SMP-RunIIFall18wmLHEGS-00112 --retry 3 --create-dirs -o Configuration/GenProduction/python/SMP-RunIIFall18wmLHEGS-00112-fragment.py
[ -s Configuration/GenProduction/python/SMP-RunIIFall18wmLHEGS-00112-fragment.py ] || exit $?;
scram b
cd ../..

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 26.8472s
# Threads for each sequence: 8
# Time per event for single thread for each sequence: 8 * 26.8472s = 214.7778s
# Which adds up to 214.7778s per event
# Single core events that fit in validation duration: 20160s / 214.7778s = 93
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 93 and 10000, but more than 0 -> 93
# It is estimated that this validation will produce: 93 * 1.0000 = 93 events
EVENTS=$1

# Random seed between 1 and 100 for externalLHEProducer
SEED=$(($(date +%s) % 100 + 1))


# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/SMP-RunIIFall18wmLHEGS-00112-fragment.py --python_filename SMP-RunIIFall18wmLHEGS-00112_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:SMP-RunIIFall18wmLHEGS-00112.root --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n $EVENTS || exit $? ;

# End of SMP-RunIIFall18wmLHEGS-00112_test.sh file

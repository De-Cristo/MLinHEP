#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_16_patch1/src ] ; then
  echo release CMSSW_10_2_16_patch1 already exists
else
  scram p CMSSW CMSSW_10_2_16_patch1
fi
cd CMSSW_10_2_16_patch1/src
eval `scram runtime -sh`

# Download fragment from McM
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIIFall18wmLHEGS-02890 --retry 3 --create-dirs -o Configuration/GenProduction/python/HIG-RunIIFall18wmLHEGS-02890-fragment.py
[ -s Configuration/GenProduction/python/HIG-RunIIFall18wmLHEGS-02890-fragment.py ] || exit $?;

scram b
cd ../..

cp ../../randomizeSeeds.py Configuration/GenProduction/python/

EVENTS=$1

cmsDriver.py Configuration/GenProduction/python/HIG-RunIIFall18wmLHEGS-02890-fragment.py \
    --python_filename HIG-RunIIFall18wmLHEGS-02890_1_cfg.py \
    --eventcontent RAWSIM,LHE \
    --customise Configuration/DataProcessing/Utils.addMonitoring,Configuration/GenProduction/randomizeSeeds.randomizeSeeds \
    --datatier GEN-SIM,LHE --fileout file:HIG-RunIIFall18wmLHEGS-02890.root \
    --conditions 102X_upgrade2018_realistic_v11 \
    --beamspot Realistic25ns13TeVEarly2018Collision \
#     --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})"\\nprocess.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" \
    --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)"
    --step LHE,GEN,SIM \
    --geometry DB:Extended \
    --era Run2_2018 \
    --no_exec --mc -n $EVENTS || exit $? ;

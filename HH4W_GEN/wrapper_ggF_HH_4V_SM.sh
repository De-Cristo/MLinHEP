#!/bin/bash

#################=================================#########################################
#step 1 GEN

source HIG-RunIIFall18wmLHEGS-02890.sh $1

# Run generated config
REPORT_NAME=HIG-RunIIFall18wmLHEGS-02890_report.xml
# Run the cmsRun
cmsRun -e -j $REPORT_NAME HIG-RunIIFall18wmLHEGS-02890_1_cfg.py || exit $? ;

# rm ...

# Followed by ZHH UL setups
#################=================================#########################################
#step 2 SIM
# ...


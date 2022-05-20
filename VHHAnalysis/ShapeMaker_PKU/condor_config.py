#indir = "/eos/home-y/yilai/VHH4bAnalysisNtuples/TEST_220108_2016pre"
#indir = "/eos/cms/store/group/phys_higgs/hbb/ntuples/VHH4bNanov8/VHH4bAnalysisNtuples/TEST_1116_updatebtagSF/"
# indir = "/eos/cms/store/group/phys_higgs/hbb/ntuples/VHH4bPostNanov8/VHH4bAnalysisNtuples/TEST_220210_2018/"
#indir = "/eos/home-y/yilai/VHH4bAnalysisNtuples/clean_bdt_tool_oct22/TEST_1116_updatebtagSF_resolved_realbtag"
#indir = "/eos/user/y/yilai/VHH4bAnalysisNtuples/clean_bdt_tool_22jan17/TEST_220116_2018_skim_add_RBDT_cate/"
#indir = '/eos/user/y/yilai/VHH4bAnalysisNtuples/clean_bdt_tool_22jan17/TEST_220122_2018_boosted_skim/'
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/0425_2022/TEST_2018_TMVAv2_0418_hadd/"
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/0425_2022/TEST_2017_TMVAv2_0425_hadd/"
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/0425_2022/TEST_2016_TMVAv2_0425_hadd/"
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2018"
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2017"
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2016"
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2016Pre"
# indir = "/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2016Post"
indir = "/eos/user/b/boguo/licheng/TEST_220506_2018_Full/"

vptcut = ""                             # "" for none, "300" for 300 GeV
nChannelsPerJob = 20 #was 14
condorDir = "condor"
sizeperbunch = 4*4*1024*1024*1024       # O(3.5 GiB) data per job
#sizeperbunch = 3.5*1024*1024*1024       # O(3.5 GiB) data per job
#isSL6 = True                            # Anaconda with ROOT and rootpy must be installed. Edit condapath.
isSL6 = False
#isIRB = True
isIRB = False

#doVZ = True
doVZ = False

doMjj2016 = False
doMjj2017 = False
doMjj2018 = True

year = "2018"
doResolved = True
doBoosted = False
doSemiBoosted = False
giveOverlapToBoosted = False
addHists = False
doJEROnly = False
separateWZ = False
skipList = [""]#sum_WW_0.root","sum_WW_1.root","sum_WW_2.root","sum_WW_3.root","sum_WZ_0.root","sum_WZ_1.root","sum_ZZ_0.root"]
skipString = 'nothing'#'Run2018'                    # Files with this string in the filename will be skipped

subText = '''universe = vanilla
Executable     =  condor_runscript.sh
Should_Transfer_Files     = YES
on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)
Notification     = never
transfer_input_files = condor_config.py, VHH4b_shapeMaker.py, Dictionaries/VHH4b_binsDict_addShapes.py,Dictionaries/VHH4b_reweightDict.py,Dictionaries/VHH4b_binsDict.py, Dictionaries/VHH4b_fileDict.py, Dictionaries/VHH4b_channelDict.py, Dictionaries/VHH4b_sampleDict.py, Dictionaries/__init__.py
#+MaxRuntime = 2*60*60
WhenToTransferOutput=On_Exit
requirements = OpSysAndVer == "CentOS7"
#request_cpus = 2
'''

#+JobFlavour = "longlunch"
#subText = '''universe = vanilla
#Executable     =  condor_runscript.sh
#Should_Transfer_Files     = YES
#on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)
#Notification     = never
#transfer_input_files = VHH4b_shapeMaker.py, nano_samples_2017stxs.py, VHH4b_binsDict.py, makeChannelDict.py, makeFileBasedSampleList.py, makeSampleBasedSystList.py, runCards_CR_VH_bdt_Wln.sh, runCards_CR_VH_bdt_Znn.sh, runCards_SR_VH_bdt_Zll.sh, runCards_CR_VH_bdt_Zll.sh, runCards_SR_VH_bdt_Wln.sh, runCards_SR_VH_bdt_Znn.sh, systematics_Zllshapes2017STXS.txt, systematics_Znnshapes2017STXS.txt, systematics_Wlnshapes2017STXS.txt
#+JobFlavour = "workday"
#WhenToTransferOutput=On_Exit
#requirements = OpSysAndVer == "CentOS7"
##request_cpus = 2
#'''


logFileText = '''\nOutput     = CONDORDIR/log_$(Cluster)_$(Process).stdout
Error      = CONDORDIR/log_$(Cluster)_$(Process).stderr
Log        = CONDORDIR/log_$(Cluster)_$(Process).log
'''

if not isSL6:
#    # SL7 settings    
    runscrText='''#!/bin/bash
export ORIG_DIR=$PWD
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_10_6_0/src/
source     /cvmfs/cms.cern.ch/cmsset_default.sh
eval     `scramv1 runtime -sh`
cd $ORIG_DIR
mkdir Dictionaries
cp *Dict.py Dictionaries/
cp VHH4b_binsDict_addShapes.py Dictionaries/
cp __init__.py Dictionaries/
'''

else:
    # SL6 compatibility for ROOT RDFs
    subText = subText.replace("requirements =","#requirements =")
    if isIRB:
        runscrText='''#!/bin/bash
source /STORE/ferencek/anaconda2/etc/profile.d/conda.sh
conda activate vhbb
mkdir Dictionaries
mv *Dict.py Dictionaries/
mv VHH4b_binsDict_addShapes.py Dictionaries/
mv __init__.py Dictionaries/
'''
    else:
        condapath = "/nfs/dust/cms/user/spmondal/anaconda2"
        runscrText="export PATH=\"CONDAPATH/bin:$PATH\"".replace("CONDAPATH",condapath)


#runscrText += "\npython VHH4b_shapeMaker.py -i $1 -n $2 -io $3 -d $4 VPTCUT"
runscrText += "\npython VHH4b_shapeMaker.py -samp $1 -i $2 -n $3 -io $4 -d $5 -o $6 VPTCUT"
#sample, files, The max. number of output files, The index of the first output, 


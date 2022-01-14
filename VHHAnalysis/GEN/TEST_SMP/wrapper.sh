#download gridpack
wget --no-check-certificate --progress=bar "https://jipeng.web.cern.ch/jipeng/AQGC/WAJJToLNuAJJ_EWK_5f_LOaQGC_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"
#step 1 GEN SIM
wget --no-check-certificate --progress=bar "https://jipeng.web.cern.ch/jipeng/AQGC/SMP-RunIIFall18wmLHEGS-00112_test.sh"
source SMP-RunIIFall18wmLHEGS-00112_test.sh $1
sed -i "s/\/cvmfs\/cms.cern.ch\/phys_generator\/gridpacks\/2017\/13TeV\/madgraph\/V5_2.6.0\/AnomalousCouplings_SMP\/WAJJToLNuAJJ_EWK_5f_LOaQGC\/WAJJToLNuAJJ_EWK_5f_LOaQGC_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz/..\/WAJJToLNuAJJ_EWK_5f_LOaQGC_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz/g" *py
cmsRun SMP-RunIIFall18wmLHEGS-00112_1_cfg.py
rm SMP-RunIIFall18wmLHEGS-00112_inLHE.root
#step 2 DR
wget --no-check-certificate --progress=bar "https://jipeng.web.cern.ch/jipeng/AQGC/SMP-RunIIAutumn18DRPremix-00138_test.sh"
source SMP-RunIIAutumn18DRPremix-00138_test.sh
cmsRun SMP-RunIIAutumn18DRPremix-00138_1_cfg.py
rm SMP-RunIIFall18wmLHEGS-00112.root
cmsRun SMP-RunIIAutumn18DRPremix-00138_2_cfg.py
rm SMP-RunIIAutumn18DRPremix-00138_0.root
#step 3 MINIAOD
wget --no-check-certificate --progress=bar "https://jipeng.web.cern.ch/jipeng/AQGC/SMP-RunIIAutumn18MiniAOD-00138_test.sh"
source SMP-RunIIAutumn18MiniAOD-00138_test.sh
cmsRun SMP-RunIIAutumn18MiniAOD-00138_1_cfg.py
rm SMP-RunIIAutumn18DRPremix-00138.root
##delete
rm -rf CMSSW*

export VHH_RunII_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/*/*.txt | sed 's/ /,/g')"
export VHH_DL_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/DL/*.txt | sed 's/ /,/g')"
export VHH_SL_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/SL/*.txt | sed 's/ /,/g')"
export VHH_MET_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/MET/*.txt | sed 's/ /,/g')"
export VHH_FH_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/FH/*.txt | sed 's/ /,/g')"

find * -name "card*.txt" -type f -exec sh -c "echo '* autoMCStats 0' >> {}" \;
CMS_TTB_norm2016               rateParam  *          TTB        1
CMS_TT_norm2016                rateParam  *          TT         1
CMS_DY_norm2016                rateParam  *          DY         1

CMS_DY_norm_2018               rateParam  *          DY         1
CMS_TT_norm_2018               rateParam  *          TT         1
CMS_TT_norm_2018               rateParam  *          TTB        1

combineCards.py card_VhadHH_VHH_2016_kl=FH/card_VhadHH_VHH_2016_kl.txt card_VhadHH_VHH_2017_kl=FH/card_VhadHH_VHH_2017_kl.txt card_VhadHH_VHH_2018_kl=FH/card_VhadHH_VHH_2018_kl.txt card_VhadHH_VHH_2016_kVV=FH/card_VhadHH_VHH_2016_kVV.txt card_VhadHH_VHH_2017_kVV=FH/card_VhadHH_VHH_2017_kVV.txt card_VhadHH_VHH_2018_kVV=FH/card_VhadHH_VHH_2018_kVV.txt vhh4b_Wen_5_13TeV2016=SL/vhh4b_Wen_5_13TeV2016.txt vhh4b_Wen_5_13TeV2017=SL/vhh4b_Wen_5_13TeV2017.txt vhh4b_Wen_5_13TeV2018=SL/vhh4b_Wen_5_13TeV2018.txt vhh4b_Wen_6_13TeV2016=SL/vhh4b_Wen_6_13TeV2016.txt vhh4b_Wen_6_13TeV2017=SL/vhh4b_Wen_6_13TeV2017.txt vhh4b_Wen_6_13TeV2018=SL/vhh4b_Wen_6_13TeV2018.txt vhh4b_Wen_7_13TeV2016=SL/vhh4b_Wen_7_13TeV2016.txt vhh4b_Wen_7_13TeV2017=SL/vhh4b_Wen_7_13TeV2017.txt vhh4b_Wen_7_13TeV2018=SL/vhh4b_Wen_7_13TeV2018.txt vhh4b_Wen_8_13TeV2016=SL/vhh4b_Wen_8_13TeV2016.txt vhh4b_Wen_8_13TeV2017=SL/vhh4b_Wen_8_13TeV2017.txt vhh4b_Wen_8_13TeV2018=SL/vhh4b_Wen_8_13TeV2018.txt vhh4b_Wmn_9_13TeV2016=SL/vhh4b_Wmn_9_13TeV2016.txt vhh4b_Wmn_9_13TeV2017=SL/vhh4b_Wmn_9_13TeV2017.txt vhh4b_Wmn_9_13TeV2018=SL/vhh4b_Wmn_9_13TeV2018.txt vhh4b_Wmn_10_13TeV2016=SL/vhh4b_Wmn_10_13TeV2016.txt vhh4b_Wmn_10_13TeV2017=SL/vhh4b_Wmn_10_13TeV2017.txt vhh4b_Wmn_10_13TeV2018=SL/vhh4b_Wmn_10_13TeV2018.txt vhh4b_Wmn_11_13TeV2016=SL/vhh4b_Wmn_11_13TeV2016.txt vhh4b_Wmn_11_13TeV2017=SL/vhh4b_Wmn_11_13TeV2017.txt vhh4b_Wmn_11_13TeV2018=SL/vhh4b_Wmn_11_13TeV2018.txt vhh4b_Wmn_12_13TeV2016=SL/vhh4b_Wmn_12_13TeV2016.txt vhh4b_Wmn_12_13TeV2017=SL/vhh4b_Wmn_12_13TeV2017.txt vhh4b_Wmn_12_13TeV2018=SL/vhh4b_Wmn_12_13TeV2018.txt vhh4b_Znn_1_13TeV2016=MET/vhh4b_Znn_1_13TeV2016.txt vhh4b_Znn_1_13TeV2017=MET/vhh4b_Znn_1_13TeV2017.txt vhh4b_Znn_1_13TeV2018=MET/vhh4b_Znn_1_13TeV2018.txt vhh4b_Znn_2_13TeV2016=MET/vhh4b_Znn_2_13TeV2016.txt vhh4b_Znn_2_13TeV2017=MET/vhh4b_Znn_2_13TeV2017.txt vhh4b_Znn_2_13TeV2018=MET/vhh4b_Znn_2_13TeV2018.txt vhh4b_Znn_3_13TeV2016=MET/vhh4b_Znn_3_13TeV2016.txt vhh4b_Znn_3_13TeV2017=MET/vhh4b_Znn_3_13TeV2017.txt vhh4b_Znn_3_13TeV2018=MET/vhh4b_Znn_3_13TeV2018.txt vhh4b_Znn_4_13TeV2016=MET/vhh4b_Znn_4_13TeV2016.txt vhh4b_Znn_4_13TeV2017=MET/vhh4b_Znn_4_13TeV2017.txt vhh4b_Znn_4_13TeV2018=MET/vhh4b_Znn_4_13TeV2018.txt card_hists_2018_R_Zll_Klbdt_High_3b_bin_SR_Z=DL/card_hists_2018_R_Zll_Klbdt_High_3b_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_High_4b_bin_SR_Z=DL/card_hists_2018_R_Zll_Klbdt_High_4b_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_SM_3b_bin_SR_Z=DL/card_hists_2018_R_Zll_Klbdt_SM_3b_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_SM_4b_bin_SR_Z=DL/card_hists_2018_R_Zll_Klbdt_SM_4b_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_High_3b_bin_SR_Z=DL/card_hists_2017_R_Zll_Klbdt_High_3b_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_High_4b_bin_SR_Z=DL/card_hists_2017_R_Zll_Klbdt_High_4b_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_SM_3b_bin_SR_Z=DL/card_hists_2017_R_Zll_Klbdt_SM_3b_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_SM_4b_bin_SR_Z=DL/card_hists_2017_R_Zll_Klbdt_SM_4b_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_High_3b_bin_SR_Z=DL/card_hists_2016_R_Zll_Klbdt_High_3b_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_High_4b_bin_SR_Z=DL/card_hists_2016_R_Zll_Klbdt_High_4b_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_SM_3b_bin_SR_Z=DL/card_hists_2016_R_Zll_Klbdt_SM_3b_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_SM_4b_bin_SR_Z=DL/card_hists_2016_R_Zll_Klbdt_SM_4b_bin_SR_Z.txt > vhh4b_All.txt

combineCards.py card_VhadHH_VHH_2016_kl=FH/card_VhadHH_VHH_2016_kl.txt card_VhadHH_VHH_2017_kl=FH/card_VhadHH_VHH_2017_kl.txt card_VhadHH_VHH_2018_kl=FH/card_VhadHH_VHH_2018_kl.txt card_VhadHH_VHH_2016_kVV=FH/card_VhadHH_VHH_2016_kVV.txt card_VhadHH_VHH_2017_kVV=DL/card_VhadHH_VHH_2017_kVV.txt card_VhadHH_VHH_2018_kVV=FH/card_VhadHH_VHH_2018_kVV.txt > vhh4b_All.txt

combineCards.py card_hists_2018_R_Zll_Klbdt_High_3b_ee_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_High_3b_ee_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_High_4b_ee_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_High_4b_ee_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_SM_3b_ee_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_SM_3b_ee_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_SM_4b_ee_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_SM_4b_ee_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_High_3b_ee_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_High_3b_ee_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_High_4b_ee_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_High_4b_ee_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_SM_3b_ee_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_SM_3b_ee_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_SM_4b_ee_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_SM_4b_ee_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_High_3b_ee_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_High_3b_ee_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_High_4b_ee_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_High_4b_ee_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_SM_3b_ee_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_SM_3b_ee_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_SM_4b_ee_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_SM_4b_ee_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_High_3b_mm_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_High_3b_mm_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_High_4b_mm_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_High_4b_mm_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_SM_3b_mm_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_SM_3b_mm_bin_SR_Z.txt card_hists_2018_R_Zll_Klbdt_SM_4b_mm_bin_SR_Z=card_hists_2018_R_Zll_Klbdt_SM_4b_mm_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_High_3b_mm_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_High_3b_mm_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_High_4b_mm_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_High_4b_mm_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_SM_3b_mm_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_SM_3b_mm_bin_SR_Z.txt card_hists_2017_R_Zll_Klbdt_SM_4b_mm_bin_SR_Z=card_hists_2017_R_Zll_Klbdt_SM_4b_mm_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_High_3b_mm_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_High_3b_mm_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_High_4b_mm_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_High_4b_mm_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_SM_3b_mm_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_SM_3b_mm_bin_SR_Z.txt card_hists_2016_R_Zll_Klbdt_SM_4b_mm_bin_SR_Z=card_hists_2016_R_Zll_Klbdt_SM_4b_mm_bin_SR_Z.txt > vhh4b_Zll.txt

combineCards.py card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_SR_Z.txt card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_SR_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_SR_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_SR_Z.txt > vhh4b_Zll.txt

text2workspace.py vhh4b_Zll.txt
combineTool.py -M Impacts -d vhh4b_Zll.root -t -1 --expectSignal=1 --doInitialFit --allPars -m 1 -n t0 --cminDefaultMinimizerStrategy 0 --rMin -40 --rMax 40
combineTool.py -M Impacts -d vhh4b_Zll.root -o impacts_t0.json -t -1 --expectSignal=1 --doFits -m 1 -n t0 --parallel 20 --task-name t0 --cminDefaultMinimizerStrategy 0 --rMin -40 --rMax 40 >& /dev/null
combineTool.py -M Impacts -d vhh4b_Zll.root -m 1 -n t0 -o impacts_t0.json
plotImpacts.py -i  impacts_t0.json -o  impacts_t0
rm *paramFit*

combine -M FitDiagnostics vhh4b_Zll.txt --saveShapes -t -1 --expectSignal=1 --saveWithUncertainties -n test --plots

combineTool.py -M FitDiagnostics vhh4b_Zll.txt --saveShapes -t -1 --expectSignal=1 --saveWithUncertainties -n test --parallel 20 --plots

combine -M FitDiagnostics vhh4b_Zll.txt --saveShapes -t -1 --expectSignal=1 --saveWithUncertainties -n test --parallel 20 --plots


combineCards.py vhh4b_Wen_5_13TeV2016=SL/vhh4b_Wen_5_13TeV2016.txt vhh4b_Wen_5_13TeV2017=SL/vhh4b_Wen_5_13TeV2017.txt vhh4b_Wen_5_13TeV2018=SL/vhh4b_Wen_5_13TeV2018.txt vhh4b_Wen_6_13TeV2016=SL/vhh4b_Wen_6_13TeV2016.txt vhh4b_Wen_6_13TeV2017=SL/vhh4b_Wen_6_13TeV2017.txt vhh4b_Wen_6_13TeV2018=SL/vhh4b_Wen_6_13TeV2018.txt vhh4b_Wen_7_13TeV2016=SL/vhh4b_Wen_7_13TeV2016.txt vhh4b_Wen_7_13TeV2017=SL/vhh4b_Wen_7_13TeV2017.txt vhh4b_Wen_7_13TeV2018=SL/vhh4b_Wen_7_13TeV2018.txt vhh4b_Wen_8_13TeV2016=SL/vhh4b_Wen_8_13TeV2016.txt vhh4b_Wen_8_13TeV2017=SL/vhh4b_Wen_8_13TeV2017.txt vhh4b_Wen_8_13TeV2018=SL/vhh4b_Wen_8_13TeV2018.txt vhh4b_Wmn_9_13TeV2016=SL/vhh4b_Wen_9_13TeV2016.txt vhh4b_Wmn_9_13TeV2017=SL/vhh4b_Wmn_9_13TeV2017.txt vhh4b_Wmn_9_13TeV2018=SL/vhh4b_Wmn_9_13TeV2018.txt vhh4b_Wmn_10_13TeV2016=SL/vhh4b_Wmn_10_13TeV2016.txt vhh4b_Wmn_10_13TeV2017=SL/vhh4b_Wmn_10_13TeV2017.txt vhh4b_Wmn_10_13TeV2018=SL/vhh4b_Wmn_10_13TeV2018.txt vhh4b_Wmn_11_13TeV2016=SL/vhh4b_Wmn_11_13TeV2016.txt vhh4b_Wmn_11_13TeV2017=SL/vhh4b_Wmn_11_13TeV2017.txt vhh4b_Wmn_11_13TeV2018=SL/vhh4b_Wmn_11_13TeV2018.txt vhh4b_Wmn_12_13TeV2016=SL/vhh4b_Wmn_12_13TeV2016.txt vhh4b_Wmn_12_13TeV2017=SL/vhh4b_Wmn_12_13TeV2017.txt vhh4b_Wmn_12_13TeV2018=SL/vhh4b_Wmn_12_13TeV2018.txt > vhh4b_All.txt

combineCards.py  vhh4b_Znn_1_13TeV2016=MET/vhh4b_Znn_1_13TeV2016.txt vhh4b_Znn_1_13TeV2017=MET/vhh4b_Znn_1_13TeV2017.txt vhh4b_Znn_1_13TeV2018=MET/vhh4b_Znn_1_13TeV2018.txt vhh4b_Znn_2_13TeV2016=MET/vhh4b_Znn_2_13TeV2016.txt vhh4b_Znn_2_13TeV2017=MET/vhh4b_Znn_2_13TeV2017.txt vhh4b_Znn_2_13TeV2018=MET/vhh4b_Znn_2_13TeV2018.txt vhh4b_Znn_3_13TeV2016=MET/vhh4b_Znn_3_13TeV2016.txt vhh4b_Znn_3_13TeV2017=MET/vhh4b_Znn_3_13TeV2017.txt vhh4b_Znn_3_13TeV2018=MET/vhh4b_Znn_3_13TeV2018.txt vhh4b_Znn_4_13TeV2016=MET/vhh4b_Znn_4_13TeV2016.txt vhh4b_Znn_4_13TeV2017=MET/vhh4b_Znn_4_13TeV2017.txt vhh4b_Znn_4_13TeV2018=MET/vhh4b_Znn_4_13TeV2018.txt > vhh4b_All.txt

text2workspace.py vhh4b_All.txt
combineTool.py -M Impacts -d vhh4b_All.root -t -1 --expectSignal 0 --doInitialFit --allPars -m 1 -n t0 --cminDefaultMinimizerStrategy 0 --rMin -40 --rMax 40
combineTool.py -M Impacts -d vhh4b_All.root -o impacts_t0.json -t -1 --expectSignal 0 --doFits -m 1 -n t0 --parallel 20 --task-name t0 --cminDefaultMinimizerStrategy 0 --rMin -40 --rMax 40 >& /dev/null
combineTool.py -M Impacts -d vhh4b_All.root -m 1 -n t0 -o impacts_t0.json
plotImpacts.py -i  impacts_t0.json -o  impacts_t0
rm *paramFit*

export VHH_DL_Run2_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*/*.txt | sed 's/ /,/g')"
export VHH_DL_16_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*2016*/*.txt | sed 's/ /,/g')"
export VHH_DL_17_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*2017*/*.txt | sed 's/ /,/g')"
export VHH_DL_18_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*2018*/*.txt | sed 's/ /,/g')"

export VHH_DL_CARD_Run2_git="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/DL/*.txt | sed 's/ /,/g')"
export VHH_DL_CARD_16_git="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/DL/*16*.txt | sed 's/ /,/g')"
export VHH_DL_CARD_17_git="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/DL/*17*.txt | sed 's/ /,/g')"
export VHH_DL_CARD_18_git="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/DL/*18*.txt | sed 's/ /,/g')"

# $VHH_DL_CARD_16_git:$VHH_DL_CARD_17_git:$VHH_DL_CARD_18_git:$VHH_DL_CARD_Run2_git
# $VHH_DL_16_CARD:$VHH_DL_17_CARD:$VHH_DL_18_CARD:$VHH_DL_Run2_CARD

export TEST_C2V="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/C2V/*.txt | sed 's/ /,/g')"
export TEST_Kl="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/Kl/*.txt | sed 's/ /,/g')"

export DL_Run2_Fake16="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_fake16/*.txt | sed 's/ /,/g')"
export DL_18="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_fake16/*2018*.txt | sed 's/ /,/g')"
export DL_17="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_fake16/*2017*.txt | sed 's/ /,/g')"
export DL_Fake16="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_fake16/*2016*.txt | sed 's/ /,/g')"

export DL_nobug="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/card_0413/*/*.txt | sed 's/ /,/g')"
export DL_16_nobug="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/card_0413/DL_2016/*.txt | sed 's/ /,/g')"
export DL_17_nobug="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/card_0413/DL_2017/*.txt | sed 's/ /,/g')"
export DL_18_nobug="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/card_0413/DL_2018/*.txt | sed 's/ /,/g')"

export DL_18_unrwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_unrwt_0421/*.txt | sed 's/ /,/g')"
export DL_18_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt_0421/*.txt | sed 's/ /,/g')"

export DL_18ScaleRunII_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt_0421/*.txt | sed 's/ /,/g')"
export MET="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/MET/*.txt | sed 's/ /,/g')"
export SL="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/SL/*.txt | sed 's/ /,/g')"

export DL_18_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt/*.txt | sed 's/ /,/g')"
export DL_17_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2017_rwt/*.txt | sed 's/ /,/g')"
export DL_17_unrwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2017_unrwt/*.txt | sed 's/ /,/g')"

export VHH_DL_Run2_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*/*.txt | sed 's/ /,/g')"
export VHH_DL_Run2_strong_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*/*strong*.txt | sed 's/ /,/g')"
export VHH_DL_Run2_sm_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*/*sm*.txt | sed 's/ /,/g')"
export VHH_DL_Run2_4b_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*/*4b*.txt | sed 's/ /,/g')"
export VHH_DL_Run2_3b_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*/*3b*.txt | sed 's/ /,/g')"

export VHH_DL_Run2_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/*/*.txt | sed 's/ /,/g')"
export VHH_DL_16_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/DL*2016*/*.txt | sed 's/ /,/g')"
export VHH_DL_16_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/2016/*.txt | sed 's/ /,/g')"
export VHH_DL_17_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/2017/*.txt | sed 's/ /,/g')"
export VHH_DL_18_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_0407/2018/*.txt | sed 's/ /,/g')"

export DL_18_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt/*.txt | sed 's/ /,/g')"
export DL_18_rwt_float="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt_float/*.txt | sed 's/ /,/g')"


export DL_18_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt/*.txt | sed 's/ /,/g')"
export DL_17_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2017_rwt/*.txt | sed 's/ /,/g')"
export DL_16_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2016_rwt/*.txt | sed 's/ /,/g')"
export DL_RunII_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_201*_rwt/*.txt | sed 's/ /,/g')"
export DL_18ScaleRunII_rwt="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt_0421/*.txt | sed 's/ /,/g')"

export DL_18_rwt_full_Syst="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/DL_2018_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_17_rwt_full_Syst="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/DL_2017_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_16_rwt_full_Syst="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/DL_2016_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_RunII_rwt_full_Syst="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/DL_RunII_full_syst/*.txt | sed 's/ /,/g')"

export DL="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/VHH/DL/*.txt | sed 's/ /,/g')"
export SL="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/VHH/SL/*.txt | sed 's/ /,/g')"
export MET="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/VHH/MET/*.txt | sed 's/ /,/g')"
export FH="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/VHH/FH/*.txt | sed 's/ /,/g')"
export VHH="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/upperlimit/CMSSW_10_2_13/src/MyWorkArea/VHH/*/*.txt | sed 's/ /,/g')"

export DL_18_rwt_full_Syst="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_17_rwt_full_Syst="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2017_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_16_rwt_full_Syst="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2016_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_RunII_rwt_full_Syst="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_RunII_full_syst/*.txt | sed 's/ /,/g')"

export DL="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/DL/*.txt | sed 's/ /,/g')"
export SL="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/SL/*.txt | sed 's/ /,/g')"
export MET="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/MET/*.txt | sed 's/ /,/g')"
export FH="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/FH/*.txt | sed 's/ /,/g')"
export VHH="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/*/*.txt | sed 's/ /,/g')"

export DL_18_rwt_full_Syst="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_18_rwt_hbb="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_hbb/*.txt | sed 's/ /,/g')"

export DL_18_rwt_full_Syst="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_9bins="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_9bins/*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_eemm_9bins="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm_9bins/*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_11bins="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_11bins/*.txt | sed 's/ /,/g')"


export DL_18_rwt_full_Syst="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst/*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_eemm="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*.txt | sed 's/ /,/g')"


export DL_18_rwt_full_Syst_eemm="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_ee="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*ee*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_mm="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*mm*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_3b="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*3b*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_4b="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*4b*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_SM="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*SM*.txt | sed 's/ /,/g')"
export DL_18_rwt_full_Syst_High="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/DL_2018_rwt_full_syst_eemm/*High*.txt | sed 's/ /,/g')"


export DL_16="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/2022_0606/DL_2016_0606/*.txt | sed 's/ /,/g')"
export DL_17="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/2022_0606/DL_2017_0606/*.txt | sed 's/ /,/g')"
export DL_18="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/2022_0606/DL_2018_0606/*.txt | sed 's/ /,/g')"

export DL_0606="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/2022_0606/DL_0608/*.txt | sed 's/ /,/g')"
export DL="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/DL/*.txt | sed 's/ /,/g')"

export DL_4b_SM_1="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0608_2022/*_8bins/*.txt | sed 's/ /,/g')"
export DL_4b_SM_2="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0608_2022/*_7bins/*.txt | sed 's/ /,/g')"
export DL_4b_SM_3="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0608_2022/*_12bins/*.txt | sed 's/ /,/g')"
# export DL_4b_SM_4="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0608_2022/*_old/*.txt | sed 's/ /,/g')"

export DL_4b_SM_4="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/DL/*SM_4b*.txt | sed 's/ /,/g')"

--PO verbose

combineCards.py card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_SR_Z.txt card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_SR_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_SR_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_SR_Z=card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_SR_Z.txt card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_CR_Z=card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_CR_Z.txt card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_CR_Z=card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_CR_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_CR_Z=card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_CR_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_CR_Z=card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_CR_Z.txt card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_SB_Z=card_hists_RunII_R_Zll_Klbdt_High_3b_ll_bin_SB_Z.txt card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_SB_Z=card_hists_RunII_R_Zll_Klbdt_High_4b_ll_bin_SB_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_SB_Z=card_hists_RunII_R_Zll_Klbdt_SM_3b_ll_bin_SB_Z.txt card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_SB_Z=card_hists_RunII_R_Zll_Klbdt_SM_4b_ll_bin_SB_Z.txt card_hists_RunII_R_Zll_Klbdt_3b_ll_bin_TT=card_hists_RunII_R_Zll_Klbdt_3b_ll_bin_TT.txt card_hists_RunII_R_Zll_Klbdt_4b_ll_bin_TT=card_hists_RunII_R_Zll_Klbdt_4b_ll_bin_TT.txt > vhh4b_Zll.txt

combineTool.py -M FitDiagnostics vhh4b_Zll.txt --saveShapes -t -1 --expectSignal=1 --saveWithUncertainties -n test --plots & 
 --absolute
text2workspace.py vhh4b_Zll.txt -m 125 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO 'map=.*/VHH_CV_1_C2V_1_kl_1_hbbhbb:r[1,-200,200]' --PO 'map=.*/VHH_CV_1_C2V_1_kl_2_hbbhbb:0' --PO 'map=.*/VHH_CV_1_C2V_1_kl_0_hbbhbb:0' --PO 'map=.*/VHH_CV_1_C2V_0_kl_1_hbbhbb:0' --PO 'map=.*/VHH_CV_1_C2V_2_kl_1_hbbhbb:0' --PO 'map=.*/VHH_CV_0p5_C2V_1_kl_1_hbbhbb:0' --PO 'map=.*/VHH_CV_1p5_C2V_1_kl_1_hbbhbb:0' --PO 'map=.*/VHH_CV_1_C2V_1_kl_20_hbbhbb:0'
combineTool.py -M Impacts -d vhh4b_Zll.root -t -1 --expectSignal=1 --doInitialFit --allPars -m 125 -n t0 --cminDefaultMinimizerStrategy 0 --rMin -400 --rMax 400 
combineTool.py -M Impacts -d vhh4b_Zll.root -o impacts_t0.json -t -1 --expectSignal=1 --doFits -m 125 -n t0 --parallel 20 --task-name t0 --cminDefaultMinimizerStrategy 0 --rMin -400 --rMax 400 >& /dev/null
combineTool.py -M Impacts -d vhh4b_Zll.root -m 125 -n t0 -o impacts_t0.json
plotImpacts.py -i  impacts_t0.json -o  impacts_t0
rm *paramFit*

export DL_Flat="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/new_v/VHH/DL/*.txt | sed 's/ /,/g')"
export DL="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*/*.txt | sed 's/ /,/g')"
export DL_SR="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*SR/*.txt | sed 's/ /,/g')"
export DL_CR="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*CR/*.txt | sed 's/ /,/g')"
export DL_add_TT="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*TT/*.txt /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*SR/*.txt | sed 's/ /,/g')"
export DL_add_SB="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*SB/*.txt /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*SR/*.txt | sed 's/ /,/g')"
export DL_add_TT_SB="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*TT/*.txt /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*SR/*.txt /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*SB/*.txt | sed 's/ /,/g')"
export DL_add_CR="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*CR/*.txt /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/0620_2022/DL*SR/*.txt | sed 's/ /,/g')"

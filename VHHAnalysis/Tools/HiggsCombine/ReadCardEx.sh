export VHH_RunII_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/*/*.txt | sed 's/ /,/g')"
export VHH_DL_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/DL/*.txt | sed 's/ /,/g')"
export VHH_SL_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/SL/*.txt | sed 's/ /,/g')"
export VHH_MET_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/MET/*.txt | sed 's/ /,/g')"
export VHH_FH_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/vhh_run2_combine/datacards_run2/bbbb_vhh/FH/*.txt | sed 's/ /,/g')"

find . -name "card*.txt" -type f -exec sh -c "echo '* autoMCStats 0' >> {}" \;

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
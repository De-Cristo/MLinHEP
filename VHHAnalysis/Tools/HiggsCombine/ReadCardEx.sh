export Zll_SvBbdt_flatten_UL_rwt_CARD="$(echo /afs/cern.ch/work/l/lichengz/private/VHH/sandbox/CMSSW_10_2_13/src/MyWorkArea/*b_rwt_Z.txt | sed 's/ /,/g' )"
export Zll_SvBbdt_flatten_UL_unrwt_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*b_Z.txt | sed 's/ /,/g' )"
export Zll_SvBbdt_flatten_UL_rwt_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*b_Z_rwt.txt | sed 's/ /,/g' )"
export Zll_SvBbdt_flatten_UL_unrwt_DJ_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*b_Z_DJ.txt | sed 's/ /,/g' )"


export Zll_SvBbdt_flatten_UL_unrwt_CARD_st="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*strong*b_Z.txt | sed 's/ /,/g' )"
export Zll_SvBbdt_flatten_UL_rwt_CARD_st="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*strong*b_Z_rwt.txt | sed 's/ /,/g' )"

export Zll_SvBbdt_flatten_UL_unrwt_CARD_sm="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*sm*b_Z.txt | sed 's/ /,/g' )"
export Zll_SvBbdt_flatten_UL_rwt_CARD_sm="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*sm*b_Z_rwt.txt | sed 's/ /,/g' )"

export Zll_SvBbdt_flatten_UL_unrwt_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*b_Z.txt | sed 's/ /,/g' )"
export Zll_SvBbdt_flatten_UL_rwt_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*b_Z_rwt.txt | sed 's/ /,/g' )"

export Zll_95bins_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*_95bins_*.txt | sed 's/ /,/g' )"
export Zee_Zmm_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*eemm95bins*.txt | sed 's/ /,/g' )"
export Zll_3b4b_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*b_bin_*.txt | sed 's/ /,/g' )"

export Zll_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*Zll*.txt | sed 's/ /,/g' )"

export Zll_2016_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*2016*.txt | sed 's/ /,/g' )"
export Zll_2016Pre_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*2016Pre*.txt | sed 's/ /,/g' )"
export Zll_2016Post_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*2016Post*.txt | sed 's/ /,/g' )"
export Zll_2017_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*2017*.txt | sed 's/ /,/g' )"
export Zll_2018_CARD="$(echo /data/pubfs/zhanglic/workspace/CMSSW_10_2_13/src/MyWorkArea/*2018*.txt | sed 's/ /,/g' )"

find . -name "card*.txt" -type f -exec sh -c "echo '* autoMCStats 0' >> {}" \;

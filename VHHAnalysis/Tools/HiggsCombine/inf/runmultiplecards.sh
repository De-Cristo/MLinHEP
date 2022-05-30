#!/bin/bash

datacard=$1
#echo ${datacard}

# $DL_18_wo_NLO:$DL_18_w_NLO:$DL_18_w_NLO_float
# upperlimit multi:
# law run PlotMultipleUpperLimits \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --pois r_vhh \
#     --scan-parameters C2V,-20,20,41 \
#     --show-parameters kl,CV \
#     --workers 64 \
#     --xsec fb \
#     --datacard-names DL_18_wo_NLO,DL_18_w_NLO,DL_18_w_NLO_float &
    
# wait
    
# law run PlotMultipleUpperLimits \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --pois r_vhh \
#     --scan-parameters kl,-40,40,81 \
#     --show-parameters C2V,CV \
#     --workers 64 \
#     --xsec fb \
#     --datacard-names DL_18_wo_NLO,DL_18_w_NLO,DL_18_w_NLO_float &

# law run PlotMultipleUpperLimits \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --pois r_vhh \
#     --scan-parameters CV,-20,20,81 \
#     --show-parameters C2V,Kl \
#     --workers 64 \
#     --xsec fb \
#     --datacard-names DL_17_now,DL_17_new
    
#upperlimit point:
law run PlotUpperLimitsAtPoint \
    --version dev \
    --hh-model hh_model.model_default_vhh \
    --multi-datacards $datacard \
    --workers 64 \
    --xsec fb \
    --pois r_vhh \
    --datacard-names DL_18_wo_NLO,DL_18_w_NLO,DL_18_w_NLO_float &
    
# law run PlotUpperLimitsAtPoint \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --workers 64 \
#     --xsec fb \
#     --pois C2V \
#     --datacard-names Zll_2017_UL,Zll_2018_UL,Zll_1718_UL &

# law run PlotUpperLimitsAtPoint \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --workers 64 \
#     --datacard-names DL_17,DL_17_lumi &
    
# law run PlotUpperLimitsAtPoint \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --workers 64 \
#     --xsec fb \
#     --pois CV \
#     --datacard-names Zll_2017_UL,Zll_2018_UL,Zll_1718_UL &
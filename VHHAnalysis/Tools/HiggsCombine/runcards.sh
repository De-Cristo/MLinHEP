#!/bin/bash

datacard=$1
#echo ${datacard}

law run PlotUpperLimits --version dev --hh-model hh_model.model_default_vhh --datacards $datacard --pois r_gghh --scan-parameters C2V,-12,12,23 --show-parameters kl,CV --workers 64 --y-log --xsec fb &

law run PlotUpperLimits --version dev --hh-model hh_model.model_default_vhh --datacards $datacard --pois r_vhh --scan-parameters kl,-22,22,45 --show-parameters C2V,CV --workers 64 --y-log --xsec fb &

law run PlotUpperLimits --version dev --hh-model hh_model.model_default_vhh --datacards $datacard --pois r_vhh --scan-parameters CV,-15,15,31 --show-parameters C2V,kl --workers 64 --y-log --xsec fb &

# law run PlotLikelihoodScan --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois kl,CV --scan-parameters kl,-10,10:CV,-10,10 --workers 4 &

# law run PlotLikelihoodScan --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois kl,C2V --scan-parameters kl,-10,10:C2V,-10,10 --workers 4 &

# law run PlotLikelihoodScan --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois C2V,CV --scan-parameters C2V,-10,10:CV,-10,10 --workers 4 &

# law run PlotMultipleUpperLimits --version dev --hh-model hh_model.model_default_vhh --multi-datacards $datacard --pois r_vhh --scan-parameters C2V,-15,15,61 --show-parameters kl,CV --workers 64 --xsec fb --datacard-names Zll_16_UL,Zll_2017_UL,Zll_2018_UL,Zll_RunII_UL

# law run PlotMultipleUpperLimits --version dev --hh-model hh_model.model_default_vhh --multi-datacards $datacard --pois r_vhh --scan-parameters kl,-30,30,81 --show-parameters C2V,CV --workers 64 --xsec fb --datacard-names Zll_16_UL,Zll_2017_UL,Zll_2018_UL,Zll_RunII_UL

law run PlotLikelihoodScan --version dev --hh-model hh_model.model_default_vhh --datacards $datacard --pois kl --scan-parameters kl,-20,20 --workers 64 --y-log &

law run PlotLikelihoodScan --version dev --hh-model hh_model.model_default_vhh --datacards $datacard --pois C2V --scan-parameters C2V,-10,10 --workers 64 --y-log &

law run PlotLikelihoodScan --version dev --hh-model hh_model.model_default_vhh --datacards $datacard --pois CV --scan-parameters CV,-10,10 --workers 64 --y-log &
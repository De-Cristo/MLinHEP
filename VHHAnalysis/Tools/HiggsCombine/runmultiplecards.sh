#!/bin/bash

datacard=$1
#echo ${datacard}

# law run PlotMultipleUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters C2V,-50,50,101 --show-parameters kl,CV --workers 4 --y-log --xsec fb --datacard-names Z_nn,Z_ll

# law run PlotMultipleUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters kl,-50,50,101 --show-parameters C2V,CV --workers 4 --y-log --xsec fb --datacard-names Z_nn,Z_ll

# law run PlotMultipleUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters CV,-50,50,101 --show-parameters C2V,kl --workers 4 --y-log --xsec fb --datacard-names Z_nn,Z_ll


law run PlotMultipleUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters C2V,-30,30,61 --show-parameters kl,CV --workers 8 --xsec fb --datacard-names Zll_unrwt_UL
#-19.8,18.9

law run PlotMultipleUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters kl,-30,30,61 --show-parameters C2V,CV --workers 8 --xsec fb --datacard-names Zll_unrwt_UL

law run PlotMultipleUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters CV,-20,20,41 --show-parameters C2V,kl --workers 8 --y-log --xsec fb --datacard-names Zll_unrwt_UL



# law run PlotMultipleSignificanceScans --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters C2V,-10,10,21 --show-parameters kl,CV --workers 4 --y-log --datacard-names SL,SL_new

# law run PlotMultipleSignificanceScans --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters kl,-10,10,21 --show-parameters C2V,CV --workers 4 --y-log --datacard-names SL,SL_new

# law run PlotMultipleSignificanceScans --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters CV,-10,10,21 --show-parameters C2V,kl --workers 4 --y-log --datacard-names SL,SL_new

# law run PlotMultipleLikelihoodScans --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois kl --scan-parameters kl,-10,10,21 --workers 4 --datacard-names SL,SL_new --y-log --y-min 1e-24 &

# law run PlotMultipleLikelihoodScans --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois CV --scan-parameters CV,-10,10,21 --workers 4 --datacard-names SL,SL_new --y-log --y-min 1e-24 &

# law run PlotMultipleLikelihoodScans --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois C2V --scan-parameters C2V,-10,10,21 --workers 4 --datacard-names SL,SL_new --y-log --y-min 1e-24 &

# law run PlotMultipleLikelihoodScans --version dev --hh-model HHModelPinvVHH.model_default --multi-datacards $datacard --pois r_vhh --scan-parameters r_vhh,-30,30,61 --workers 4 --datacard-names SL,SL_new --y-log --y-min 1e-24 &


#!/bin/bash

datacard=$1
#echo ${datacard}

law run PlotUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois r_vhh --scan-parameters C2V,-50,50,61 --show-parameters kl,CV --workers 4 --y-log --xsec fb

law run PlotUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois r_vhh --scan-parameters kl,-50,50,61 --show-parameters C2V,CV --workers 4 --y-log --xsec fb

law run PlotUpperLimits --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois r_vhh --scan-parameters CV,-50,50,61 --show-parameters C2V,kl --workers 4 --y-log --xsec fb

# law run PlotLikelihoodScan --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois kl,CV --scan-parameters kl,-10,10:CV,-10,10 --workers 4 &

# law run PlotLikelihoodScan --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois kl,C2V --scan-parameters kl,-10,10:C2V,-10,10 --workers 4 &

# law run PlotLikelihoodScan --version dev --hh-model HHModelPinvVHH.model_default --datacards $datacard --pois C2V,CV --scan-parameters C2V,-10,10:CV,-10,10 --workers 4 &

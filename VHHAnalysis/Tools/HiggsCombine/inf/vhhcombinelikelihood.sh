datacard=$1

#likelihood scan:
law run PlotLikelihoodScan \
    --version dev \
    --hh-model hh_model.model_default_vhh \
    --datacards $Zll_CARD \
    --pois kl \
    --scan-parameters kl,-25,25 \
     --workers 64 \
     --y-log &

law run PlotLikelihoodScan \
    --version dev \
    --hh-model hh_model.model_default_vhh \
    --datacards $Zll_CARD \
    --pois C2V \
    --scan-parameters C2V,-15,15 \
     --workers 64 \
     --y-log &
     
law run PlotLikelihoodScan \
    --version dev \
    --hh-model hh_model.model_default_vhh \
    --datacards $Zll_CARD \
    --pois CV \
    --scan-parameters CV,-15,15 \
     --workers 64 \
     --y-log &
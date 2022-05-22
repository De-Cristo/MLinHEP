datacard=$1

law run PlotMultipleLikelihoodScans \
    --version dev \
    --hh-model hh_model.model_default_vhh \
    --multi-datacards $datacard \
    --pois kl \
    --workers 64 \
    --y-log \
    --datacard-names DL_18_unrwt,DL_18_rwt \
    --scan-parameters kl,-50,50,101 &
    
    
law run PlotMultipleLikelihoodScans \
    --version dev \
    --hh-model hh_model.model_default_vhh \
    --multi-datacards $datacard \
    --pois C2V \
    --workers 64 \
    --y-log \
    --datacard-names DL_18_unrwt,DL_18_rwt \
    --scan-parameters C2V,-50,50,101 &
    
# law run PlotMultipleLikelihoodScans \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --pois CV \
#     --workers 64 \
#     --y-log \
#     --datacard-names DL,SL,MET,FH,Combine \
#     --scan-parameters CV,-20,20,41 &
    
# law run PlotMultipleLikelihoodScans \
#     --version dev \
#     --hh-model hh_model.model_default_vhh \
#     --multi-datacards $datacard \
#     --pois C2V \
#     --workers 64 \
#     --y-log \
#     --datacard-names DL,SL,MET,FH,Combine \
#     --scan-parameters C2V,-15,15,31 &
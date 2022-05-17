#!/bin/bash

nohup python slim_analysis_samples.py -m 16 -p 5 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2018 -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v3/2018 >> 2018_slim.log 2>&1 &

nohup python slim_analysis_samples.py -m 16 -p 5 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2017 -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v3/2017 >> 2017_slim.log 2>&1 &

nohup python slim_analysis_samples.py -m 16 -p 5 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2016Pre -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v3/2016Pre >> 2016Pre_slim.log 2>&1 &

nohup python slim_analysis_samples.py -m 16 -p 5 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2016Post -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v3/2016Post >> 2016Post_slim.log 2>&1 &

# python slim_analysis_samples.py -m 16 -p 5 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/TEST_2018_TMVAv2_hadd_0418 -o ./TEST_2018_TMVAv2_hadd_0418_Ntuple_Norm
#!/bin/bash

nohup python slim_analysis_samples.py -m 32 -p 16 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2018 -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v2/2018 >> 2018_slim.log 2>&1 &

nohup python slim_analysis_samples.py -m 32 -p 16 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2017 -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v2/2017 >> 2017_slim.log 2>&1 &

nohup python slim_analysis_samples.py -m 1 -p 16 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2016Pre -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v2/2016Pre >> 2016Pre_slim.log 2>&1 &

nohup python slim_analysis_samples.py -m 1 -p 16 -d /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2016Post -o /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple_v2/2016Post >> 2016Post_slim.log 2>&1 &
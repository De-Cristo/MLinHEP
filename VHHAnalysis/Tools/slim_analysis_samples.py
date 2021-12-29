import ROOT as R
import os
import math
R.gROOT.SetBatch(True)
from multiprocessing import Pool
import subprocess
import argparse
from analysis_branch import *
    
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--NtupleDir",     dest="ndir", default='/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/TEST_1113UL',   help="Ntuple direction" )
parser.add_argument("-m", "--MultThread",    dest="MT",   type=int, default=8,   help="How many threads will be used (default = 8)" )
args = parser.parse_args()

R.EnableImplicitMT(args.MT)
path = args.ndir

file_dict     = {}
rdf_dict      = {}

string_list_for_TT     = []
string_list_for_ttbb   = []
string_list_for_DY     = []
string_list_for_Other  = []
string_list_for_ZHH    = []
string_list_for_Data   = []

file_list = os.listdir(path)

for _file in file_list:
    if _file in file_list_for_TT:
        string_list_for_TT.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_for_ttbb:
        string_list_for_ttbb.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_DY:
        string_list_for_DY.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_Other:
        string_list_for_Other.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_Data:
        string_list_for_Data.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_ZHH:
        string_list_for_ZHH.append('{0}/{1}/*.root'.format(path,_file))
        rdf_dict[_file] = R.RDataFrame('Events','{0}/{1}/*.root'.format(path,_file))
    else:
        print("WARNING:::File : "+_file+" is not in any case. Will be DROPPED.")
#END

Vars = analysis_branches
    
newpath = 'Pre_SlimmedSample/{0}_sample_forTrain'.format(args.bdt)
os.system('mkdir -p {0}'.format(newpath))
sample_list = ['TT', 'ttbb', 'DY', 'Other', 'Data']
sample_list+=file_list_ZHH
    
rdf_dict['TT']     = R.RDataFrame('Events', string_list_for_TT, Vars)
rdf_dict['ttbb']   = R.RDataFrame('Events', string_list_for_ttbb, Vars)
rdf_dict['DY']     = R.RDataFrame('Events', string_list_for_DY, Vars)
rdf_dict['Other']  = R.RDataFrame('Events', string_list_for_Other, Vars)
rdf_dict['Data']   = R.RDataFrame('Events', string_list_for_Data, Vars)
for _zhh_sig in string_list_for_ZHH:
    rdf_dict[_zhh_sig.split('/')[-2]] = R.RDataFrame('Events', _zhh_sig, Vars)
    
arg_list = []
for _sample in sample_list:
    for _rhh_name, _rhh in rHH_region_dict.items():
        for _zmass_name, _zmass in Zmass_region_dict.items():
            for _btag_name, _btag in btag_multiplicity_dict.items():
                loop.append([_sample, args.lcha, _rhh_name, _btag_name, _zmass_name, lepton_channel, _rhh, _btag, _zmass])
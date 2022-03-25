import ROOT as R
import os
import math
R.gROOT.SetBatch(True)
from multiprocessing import Pool
import subprocess
import argparse
from analysis_branch import *

#     .Define("No3_btag_score",\
#             "float _bts = 0;\
#             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
#             sort(bts,bts+4);\
#             return _bts = bts[1];")\
#     .Define("No4_btag_score",\
#             "float _bts = 0;\
#             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
#             sort(bts,bts+4);\
#             return _bts = bts[0];")\

def slimmer(_arg_list):
    print('Starting {0} {1} {2} {3}...\n'.format(_arg_list[0],_arg_list[1],_arg_list[2],_arg_list[3]))
    rdf_dict[_arg_list[0]].Filter(_arg_list[4]).Filter(_arg_list[5]).Filter(_arg_list[6])\
    .Define("No3_btag_score",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return bts[_idx_sorted[2]];'
           )\
    .Define("No3_btag_pt",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             float bpt[4] = {VHH_H1_BJet1_pT, VHH_H1_BJet2_pT, VHH_H2_BJet1_pT, VHH_H2_BJet2_pT};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return bpt[_idx_sorted[2]];'
            )\
    .Define("No3_btag_eta",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             float beta[4] = {VHH_H1_BJet1_eta, VHH_H1_BJet2_eta, VHH_H2_BJet1_eta, VHH_H2_BJet2_eta};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return beta[_idx_sorted[3]];'
           )\
    .Define("No3_btag_phi",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             float bphi[4] = {VHH_H1_BJet1_phi, VHH_H1_BJet2_phi, VHH_H2_BJet1_phi, VHH_H2_BJet2_phi};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return bphi[_idx_sorted[2]];'
           )\
    .Define("No4_btag_score",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return bts[_idx_sorted[3]];'
           )\
    .Define("No4_btag_pt",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             float bpt[4] = {VHH_H1_BJet1_pT, VHH_H1_BJet2_pT, VHH_H2_BJet1_pT, VHH_H2_BJet2_pT};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return bpt[_idx_sorted[3]];'
           )\
    .Define("No4_btag_eta",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             float beta[4] = {VHH_H1_BJet1_eta, VHH_H1_BJet2_eta, VHH_H2_BJet1_eta, VHH_H2_BJet2_eta};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return beta[_idx_sorted[3]];'
           )\
    .Define("No4_btag_phi",\
            'std::map<float, int> _jpt_idx;\
             std::vector<int> _idx_sorted;\
             float bts[4] = {VHH_H1_BJet1_btag, VHH_H1_BJet2_btag, VHH_H2_BJet1_btag, VHH_H2_BJet2_btag};\
             float bphi[4] = {VHH_H1_BJet1_phi, VHH_H1_BJet2_phi, VHH_H2_BJet1_phi, VHH_H2_BJet2_phi};\
             for (int i = 0; i < 4; ++i){ _jpt_idx[bts[i]] = i;}\
             for (auto _kc : _jpt_idx){_idx_sorted.push_back(_kc.second);}\
             std::reverse(_idx_sorted.begin(), _idx_sorted.end());\
             return bphi[_idx_sorted[3]];'
           )\
    .Snapshot('Events','{0}/{1}_{2}_{3}_{4}.root'.format(newpath,_arg_list[0],_arg_list[1],_arg_list[2],_arg_list[3]),Vars)
    print('Finishing {0} {1} {2} {3}...\n'.format(_arg_list[0],_arg_list[1],_arg_list[2],_arg_list[3]))

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--NtupleDir",     dest="ndir", default='/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022/2018',   help="Ntuple direction" )
parser.add_argument("-m", "--MultThread",    dest="MT",   type=int, default=16,   help="How many threads will be used (default = 16)" )
parser.add_argument("-p", "--MultProc",      dest="MP",   type=int, default=8,    help="How many sub processes will be started (default = 8)" )
parser.add_argument("-o", "--OutDir",        dest="odir", default='/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/2022_Ntuple/2018',   help="Output Ntuple direction" )
args = parser.parse_args()

path = args.ndir

file_dict     = {}
rdf_dict      = {}

string_list_for_TT     = []
string_list_for_TTBB   = []
string_list_for_DY     = []
string_list_for_Other  = []
string_list_for_ZHH    = []
string_list_for_Data   = []

file_list = os.listdir(path)
file_list_ZHH_update = []

for _file in file_list:
    if _file in file_list_for_TT:
        string_list_for_TT.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_for_TTBB:
        string_list_for_TTBB.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_DY:
        string_list_for_DY.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_Other:
        string_list_for_Other.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_Data:
        string_list_for_Data.append('{0}/{1}/*.root'.format(path,_file))
    elif _file in file_list_ZHH:
        file_list_ZHH_update.append(_file)
        string_list_for_ZHH.append('{0}/{1}/*.root'.format(path,_file))
        rdf_dict[_file] = R.RDataFrame('Events','{0}/{1}/*.root'.format(path,_file))
    else:
        print("WARNING:::File : "+_file+" is not in any case. Will be DROPPED.")
#END

Vars = analysis_branches
    
newpath = args.odir
os.system('rm -rfv {0}'.format(newpath))
os.system('mkdir -p {0}'.format(newpath))
sample_list = ['TT', 'TTBB', 'DY', 'Other', 'Data']
sample_list+=file_list_ZHH_update

R.EnableImplicitMT(args.MT)
rdf_dict['TT']     = R.RDataFrame('Events', string_list_for_TT)
rdf_dict['TTBB']   = R.RDataFrame('Events', string_list_for_TTBB)
rdf_dict['DY']     = R.RDataFrame('Events', string_list_for_DY)
rdf_dict['Other']  = R.RDataFrame('Events', string_list_for_Other)
rdf_dict['Data']   = R.RDataFrame('Events', string_list_for_Data)

for _zhh_sig in string_list_for_ZHH:
    rdf_dict[_zhh_sig.split('/')[-2]] = R.RDataFrame('Events', _zhh_sig)
    
arg_list = []
for _sample in sample_list:
    for _rhh_name, _rhh in rHH_region_dict.items():
        for _btag_name, _btag in btag_multiplicity_dict.items():
            for _lepchan_name, _lepchan in lepton_channel_dict.items():
                arg_list.append([_sample, _lepchan_name, _rhh_name, _btag_name, _lepchan, _rhh, _btag])
# print(arg_list)
Vars.update({"No3_btag_score","No3_btag_pt","No3_btag_eta","No3_btag_phi",\
             "No4_btag_score","No4_btag_pt","No4_btag_eta","No4_btag_phi",\
            })

#TODO: angle information from two leptons

# print(Vars)

with Pool(args.MP) as p:
    p.map(slimmer, arg_list)
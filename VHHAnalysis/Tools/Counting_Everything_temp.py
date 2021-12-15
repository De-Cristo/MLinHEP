import ROOT as R
import os
import math
R.gROOT.SetBatch(True)
from multiprocessing import Pool
import subprocess
import argparse

R.EnableImplicitMT()

def counter(_loop):
    print('{0}_{1}_{2}_{3}_{4} : '.format(_loop[0], _loop[1], _loop[2], _loop[3], _loop[4]) + ' Start Checking... \n')
    print('Events number: {0}_{1}_{2}_{3}_{4} : '.format(_loop[0], _loop[1], _loop[2], _loop[3], _loop[4]) + str(rdf_dict[_loop[0]].Filter(_loop[5]).Filter(_loop[6]).Filter(_loop[7]).Filter(_loop[8]).Filter('weight > 0 && weight<4').Sum('weight').GetValue())+'\n')
                
def subprocessWrapper(c):
    subprocess.call(c, shell=True)
    
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--NtupleDir",     dest="ndir", default='/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/TEST_1127_UL_DeepJet/',   help="Ntuple direction (default = /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/TEST_1127_UL_DeepJet/)" )
parser.add_argument("-l", "--Lepchan",       dest="lcha", default='Zll',   help="Which leptonic channel (default = Zll)" )
args = parser.parse_args()

path = args.ndir

if args.lcha == 'Zll':
    lepton_channel = "(isZee || isZmm)"
elif args.lcha == 'Znn':
    lepton_channel = "isZnn"
else:
    print('We only support for Zll and Znn channel temporarily')
    exit(0)

file_dict = {}
rdf_dict = {}
histo_dict = {}
canvas_dict = {}
legend_dict = {}

rHH_region_dict = {
        'rHH_SR' : "VHH_rHH<25",
#         'rHH_CR' : "VHH_rHH>25 && VHH_rHH<50",
#         'rHH_SB' : "VHH_rHH>50",
}

Zmass_region_dict = {
        'TT_CR'  : "V_mass<75 || V_mass>105",
        'Z_mass'  : "V_mass>75 && V_mass<105",
#     'no_mass' : "weight>0"
}

btag_multiplicity_dict = {
        'two_btag' : "VHH_nBJets == 2",
        'three_btag' : "VHH_nBJets == 3",
        'four_btag' : "VHH_nBJets == 4",
}

IsttB_TT = "IsttB == 0"
IsttB_TTB = "IsttB > 0"

file_list_for_TT = ['TT_AllHadronic','TT_DiLep_NoPSWeights','TT_SingleLep']
file_list_for_ttbb = ['ttbb_AllHadronic','ttbb_DiLep','ttbb_SingleLep']
file_list_DY = ['DYToLL_M10-50_Inc_madgraph','DYToLL_M-50_Inc_madgraph','DYToLL_M-50_HT70to100_madgraph','DYToLL_M-50_HT100to200_madgraph','DYToLL_M-50_HT200to400_madgraph','DYToLL_M-50_HT400to600_madgraph',\
                'DYToLL_M-50_HT600to800_madgraph','DYToLL_M-50_HT800to1200_madgraph','DYToLL_M-50_HT1200to2500_madgraph','DYToLL_M-50_HT2500toInf_madgraph']
file_list_ZHH = ['ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0','ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0','ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0']
file_list_Other = ['ST_s-c_4f_lep','ST_t-channel_eleDecays','ST_t-channel_muDecays','ST_t-channel_tauDecays','ST_tW_antitop_5f_noFullHad','ST_tW_top_5f_noFullHad',\
                   'ttHTobb_M125','TTWLNuJets','TTWQQJets','TTZLLNuNuJets','TTZQQJets']
file_list_Data = ['Run2018_DoubleMu_ReMiniAOD','Run2018_EG_ReMiniAOD']

string_list_for_TT = []
string_list_for_ttbb = []
string_list_for_DY = []
string_list_for_Other = []
string_list_for_ZHH = []
string_list_for_Data = []

for _file in file_list_for_TT:
    string_list_for_TT.append('{0}/{1}/*.root'.format(path,_file))
print(string_list_for_TT)

for _file in file_list_for_ttbb:
    string_list_for_ttbb.append('{0}/{1}/*.root'.format(path,_file))
print(string_list_for_ttbb)

for _file in file_list_DY:
    string_list_for_DY.append('{0}/{1}/*.root'.format(path,_file))
print(string_list_for_DY)

for _file in file_list_Other:
    string_list_for_Other.append('{0}/{1}/*.root'.format(path,_file))
print(string_list_for_Other)

for _file in file_list_Data:
    string_list_for_Data.append('{0}/{1}/*.root'.format(path,_file))
print(string_list_for_Data)

for _file in file_list_ZHH:
    string_list_for_ZHH.append('{0}/{1}/*.root'.format(path,_file))
    rdf_dict[_file] = R.RDataFrame('Events','{0}/{1}/*.root'.format(path,_file))
print(string_list_for_ZHH)

rdf_dict['TT'] = R.RDataFrame('Events',string_list_for_TT).Filter(IsttB_TT)
rdf_dict['ttbb'] = R.RDataFrame('Events',string_list_for_ttbb).Filter(IsttB_TTB)
rdf_dict['DY'] = R.RDataFrame('Events',string_list_for_DY)
rdf_dict['Other'] = R.RDataFrame('Events',string_list_for_Other)
rdf_dict['Data'] = R.RDataFrame('Events',string_list_for_Data)

sample_list = ['TT', 'ttbb', 'DY', 'Other', 'Data']
sample_list+=['ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0']

# sample_list+=file_list_ZHH

sample_list = ['TT', 'Data', 'ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0']
sample_list = ['TT']
loop = []

for _sample in sample_list:
    for _rhh_name, _rhh in rHH_region_dict.items():
        for _zmass_name, _zmass in Zmass_region_dict.items():
            for _btag_name, _btag in btag_multiplicity_dict.items():
                loop.append([_sample, args.lcha, _rhh_name, _btag_name, _zmass_name, lepton_channel, _rhh, _btag, _zmass])

print(loop)
                
with Pool(52) as p:
    p.map(counter, loop)

# p = multiprocessing.Pool(20)
# p.map(subprocessWrapper, sample_list)    
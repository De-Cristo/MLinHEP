import ROOT as R
import os
import math
R.gROOT.SetBatch(True)
from multiprocessing import Pool
import subprocess
import argparse

from training_branch import c2v_training_branches,svb_training_branches,rwt_training_branches,scaling_branches

R.EnableImplicitMT(16)

def counter(_sample):
    for _rhh_name, _rhh in rHH_region_dict.items():
        for _zmass_name, _zmass in Zmass_region_dict.items():
            for _btag_name, _btag in btag_multiplicity_dict.items():
                print('{0}_Z_{1}_{2}_{3} : '.format(_sample, _rhh_name, _btag_name, _zmass_name) + ' Start Checking...')
                if args.bdt == 'scale':
                    rdf_dict[_sample].Filter(lepton_channel).Filter(_rhh).Filter(_btag).Filter(_zmass).Filter("weight<4").Define("No3_btag_score", "float _bts = 0;\
                                                        if(VHH_H1_BJet2_btag>VHH_H2_BJet1_btag){_bts = VHH_H2_BJet1_btag;}\
                                                        else{if(VHH_H1_BJet2_btag>VHH_H2_BJet1_btag){_bts = VHH_H1_BJet2_btag;}else{_bts = VHH_H2_BJet1_btag;}}\
                                                        return _bts;").Snapshot("Tree_Events", "../scaleFactor/sample_forScale/{0}_Z_{1}_{2}_{3}.root".format(_sample, _rhh_name, _btag_name, _zmass_name),Vars)
                else:
                    rdf_dict[_sample].Filter(lepton_channel).Filter(_rhh).Filter(_btag).Filter(_zmass).Filter("weight<4").Snapshot("Tree_Events", newpath+"/{0}_Z_{1}_{2}_{3}.root".format(_sample, _rhh_name, _btag_name, _zmass_name),Vars)
                print('{0}_Z_{1}_{2}_{3} : '.format(_sample, _rhh_name, _btag_name, _zmass_name) + ' Done :)')
                
def subprocessWrapper(c):
    subprocess.call(c, shell=True)
    
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--BDTtype",       dest="bdt",  default='C2V',   help="samples for which BDT type (default = C2V)" )
parser.add_argument("-d", "--NtupleDir",     dest="ndir", default='/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/TEST_1113UL/',   help="Ntuple direction (default = /data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/TEST_1113UL/)" )
parser.add_argument("-l", "--Lepchan",       dest="lcha", default='Zll',   help="Which leptonic channel (default = Zll)" )
args = parser.parse_args()

path = args.ndir

if args.lcha == 'Zll':
    lepton_channel = "isZee || isZmm"
elif args.lcha == 'Znn':
    lepton_channel = "isZnn"
else:
    print('We only support for Zll and Znn channel temporarily')
    exit(0)

os.system('mkdir -p ./temp')

file_dict = {}
rdf_dict = {}
histo_dict = {}
canvas_dict = {}
legend_dict = {}

rHH_region_dict = {
        'rHH_SR' : "VHH_rHH<25",
        'rHH_CR' : "VHH_rHH>25 && VHH_rHH<50",
        'rHH_SB' : "VHH_rHH>50",
}

Zmass_region_dict = {
        'TT_CR'  : "V_mass<75 || V_mass>105",
        'Z_mass'  : "V_mass>75 && V_mass<105",
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
file_list_ZHH = ['ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0','ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0','ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0']
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

rdf_dict['TT'] = R.RDataFrame('Events',string_list_for_TT).Filter('weight<4')
rdf_dict['ttbb'] = R.RDataFrame('Events',string_list_for_ttbb).Filter('weight<4')
rdf_dict['DY'] = R.RDataFrame('Events',string_list_for_DY).Filter('weight<4')
rdf_dict['Other'] = R.RDataFrame('Events',string_list_for_Other).Filter('weight<4')
rdf_dict['Data'] = R.RDataFrame('Events',string_list_for_Data).Filter('weight<4')

if args.bdt == 'C2V':
    Vars = {'isZee','isZmm','isZnn','IsttB', 'VHH_nBJets',\
            'VHH_H1_pT', 'VHH_H2_e','VHH_H2_eta',\
            'VHH_H2_e','VHH_H2_eta',\
            'VHH_HH_m', 'VHH_HH_e', 'VHH_HH_eta',\
            'V_pt',\
            'VHH_V_H2_dPhi', 'VHH_V_HH_dPhi',\
            'VHH_HH_deta', 'VHH_HH_dR',\
            'weight'}
    os.system('mkdir -p ../C2V_BDT/c2v_sample_forTrain')
    newpath = '../C2V_BDT/c2v_sample_forTrain'
    sample_list=file_list_ZHH
    
elif args.bdt == 'SvB':
    Vars = {'isZee','isZmm','isZnn','IsttB', 'VHH_nBJets',\
            'VHH_H1_BJet1_pT','VHH_H2_BJet1_pT',\
            'VHH_H1_m', 'VHH_H1_pT', 'VHH_H1_e',\
            'VHH_HH_m', 'VHH_HH_e', 'VHH_HH_pT',\
            'V_pt', 'V_mass', 'VHH_Vreco4j_HT',\
            'VHH_V_H1_dPhi', 'VHH_V_HH_dPhi',\
            'VHH_HH_deta', 'VHH_HH_dR',\
            'weight'}
    os.system('mkdir -p ../SvB_BDT/svb_sample_forTrain')
    newpath = '../SvB_BDT/svb_sample_forTrain'
    sample_list = ['TT', 'ttbb', 'DY', 'Other', 'Data']
    sample_list+=file_list_ZHH

elif args.bdt == 'RwT':
    Vars = {'isZee','isZmm','isZnn','IsttB', 'VHH_nBJets',\
            'VHH_H1_BJet1_pT','VHH_H2_BJet1_pT',\
            'VHH_H1_m', 'VHH_H1_pT', 'VHH_H1_e',\
            'VHH_HH_m', 'VHH_HH_e', 'VHH_HH_pT',\
            'V_pt', 'V_mass', 'VHH_Vreco4j_HT',\
            'VHH_V_H1_dPhi', 'VHH_V_HH_dPhi',\
            'VHH_HH_deta', 'VHH_HH_dR',\
            'weight'}
    os.system('mkdir -p ../RwT_BDT/rwt_sample_forTrain')
    newpath = '../RwT_BDT/rwt_sample_forTrain'
    sample_list = ['TT', 'ttbb', 'DY', 'Other', 'Data']
    
elif args.bdt == 'scale':
    Vars = {'isZee','isZmm','isZnn','IsttB', 'VHH_nBJets',\
            'weight', 'No3_btag_score'}
    os.system('mkdir -p ../scaleFactor/sample_forScale')
    sample_list = ['TT', 'ttbb', 'DY', 'Other', 'Data']
    
else:
    print('Using the wrong BDT type... Please CHECK and try again.')
    exit(0)

print(sample_list)

with Pool(10) as p:
    p.map(counter, sample_list)

# p = multiprocessing.Pool(20)
# p.map(subprocessWrapper, sample_list)    
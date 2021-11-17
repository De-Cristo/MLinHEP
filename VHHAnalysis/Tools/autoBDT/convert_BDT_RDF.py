import ROOT as R
from multiprocessing.dummy import Pool as ThreadPool
import sys
import os
import math
import argparse
from BDT_util import *
from cfg_BDT_setting import training_branches
import fileinput


# R.gInterpreter.Declare('#include "assist_vhh.C"')

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--MultiProcess",       dest="multi",    default=0,    type=int,              help="enable multi-processing threads (defalt = 0)" )
parser.add_argument("-i", "--InputFile",          dest="inFile",   default="VHH_BDT_sample.txt",        help="input MC signal sample (defalt = sample.txt)" )
parser.add_argument("-t", "--EventsType",         dest="eveType",  default="isZee",                     help="Events Cats (defalt = isZee)" )
parser.add_argument("-v", "--verbose",            dest="verb",     default=0,              type=int,    help="different verbose level (defalt = 0)" )
parser.add_argument("-b", "--BatchMode",          dest="batch",    default=1,                           help="showing and save figures in pdf (defalt = 1)" )
args = parser.parse_args()

if args.multi != 0:
    R.EnableImplicitMT(args.multi)
    print('using ' + str(args.multi) + ' threads in MT Mode!')
else:
    print('not using MT Mode!')

GlobalInDir = '/eos/user/l/lichengz/VHH4bAnalysisNtuples/haddjobs2018'
GlobalOutDir='/eos/user/l/lichengz/VHH4bAnalysisNtuples/LocalBDT/'

if not os.path.exists(args.inFile):
#FIXME
    checkin = getabsroute(GlobalInDir)
else:
    print('reading '+args.inFile)
    
# exit(0)

Tree_Name = 'Events'

if args.eveType == 'isZee' or args.eveType == 'isZmm':
    vmasswindow = ' V_mass <= 120 && V_mass >= 70 '
if args.eveType == 'isZnn':
    vmasswindow = ' '

Samples_Lines = ReadSamples(args.inFile)
Samples_Number= len(Samples_Lines)
Sample_Type, Signal_Samples, Background_Samples = ClassifySamples(Samples_Lines)

print('Reading prev. files ...')
Rdf_Inp_Sig = R.RDataFrame(Tree_Name, Signal_Samples)
Rdf_Inp_Bkg = R.RDataFrame(Tree_Name, Background_Samples)

Branch_List = R.vector('string')()
for Branch_Name in training_branches:
    Branch_List.push_back(Branch_Name)
    print(Branch_Name+' is one of the variable.')
    
print('Saving training files ...')
Rdf_Inp_Sig.Filter(args.eveType+'==1').Filter('VHH_nBJets >= 3').Filter(vmasswindow).Snapshot('TreeS', GlobalOutDir+'VHH_BDT_Signal' +args.eveType+ '_111.root', Branch_List)
Rdf_Inp_Bkg.Filter(args.eveType+'==1').Filter('VHH_nBJets >= 3').Filter(vmasswindow).Snapshot('TreeB', GlobalOutDir+'VHH_BDT_Background' +args.eveType+ '.root', Branch_List)

print(Rdf_Inp_Sig.Filter(args.eveType+'==1').Filter('VHH_nBJets >= 3').Filter(vmasswindow).Sum('weight').GetValue())
print(Rdf_Inp_Bkg.Filter(args.eveType+'==1').Filter('VHH_nBJets >= 3').Filter(vmasswindow).Sum('weight').GetValue())

print('finish slimming files, now generate scripts.')

new_branch_content = '//dataloader insert point!!! \n'
_i = 0
for _branches in training_branches:
    if _branches != 'weight':
        new_branch_content += '\n    dataloader->AddVariable("{0}", "{0}", "units", {1} );'.format(_branches, "'F'")
        _i = _i + 1 
#end

os.system('cp -rv LocalBDT_TMVA_Training_Template.C LocalBDT_TMVA_Training.C')
replacementStrings_Branches = {
    '//dataloader insert point!!!' : new_branch_content,
}

change_file('LocalBDT_TMVA_Training.C', replacementStrings_Branches)

#FIXME generate application file

# os.system('rm ' + args.inFile) # FIXME
print('Everything has been done.')
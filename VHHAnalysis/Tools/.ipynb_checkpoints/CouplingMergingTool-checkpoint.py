#WHH_CV_1_0_C2V_0_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0001562 +- 7.128e-07 pb
#1.047
#LO Madgraph xsecs
#WHH_CV_0_5_C2V_1_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0002864 +- 9.158e-07 pb
#WHH_CV_1_0_C2V_0_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0001492 +- 6.739e-07 pb
#WHH_CV_1_0_C2V_1_0_C3_0_0_13TeV-madgraph.log:     Cross-section :   0.0002366 +- 1.025e-06 pb
#WHH_CV_1_0_C2V_1_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0004157 +- 1.319e-06 pb
#WHH_CV_1_0_C2V_1_0_C3_2_0_13TeV-madgraph.log:     Cross-section :   0.0006848 +- 1.987e-06 pb
#WHH_CV_1_0_C2V_2_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.001114 +- 3.251e-06 pb
#WHH_CV_1_5_C2V_1_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0008897 +- 3.418e-06 pb
#ZHH_CV_0_5_C2V_1_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0001652 +- 5.321e-07 pb
#ZHH_CV_1_0_C2V_0_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   9.027e-05 +- 3.358e-07 pb
#ZHH_CV_1_0_C2V_1_0_C3_0_0_13TeV-madgraph.log:     Cross-section :   0.0001539 +- 8.34e-07 pb
#ZHH_CV_1_0_C2V_1_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0002632 +- 1.022e-06 pb
#ZHH_CV_1_0_C2V_1_0_C3_2_0_13TeV-madgraph.log:     Cross-section :   0.0004233 +- 1.411e-06 pb
#ZHH_CV_1_0_C2V_2_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.0006739 +- 2.855e-06 pb
#ZHH_CV_1_5_C2V_1_0_C3_1_0_13TeV-madgraph.log:     Cross-section :   0.000573 +- 2.833e-06 pb

# name=ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0 xsec=0.0002278
# name=ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0 xsec=0.0001245
# name=ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0 xsec=0.000212
# name=ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0 xsec=0.000363
# name=ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0 xsec=0.000584
# name=ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0 xsec=0.000929
# name=ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0 xsec=0.000790

import numpy as np
import ROOT as R
import sys
import os
from util import convert_coupling_diagramweight, Save_Temp_Components
import argparse

# R.gInterpreter.Declare('#include "assist_vhh.C"')

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--multiprocess",       dest="multi",  default=0, type=int,   help="enable multi-processing (defalt = 0)" )
parser.add_argument("-v", "--verbose",            dest="verb",   default=0, type=int,   help="different verbose level (defalt = 0)" )
args = parser.parse_args()

# dict_rdf    = dict()

if args.multi != 0:
    R.EnableImplicitMT(args.multi)
    print('using ' + str(args.multi) + ' threads in MT Mode!')
else:
    print('Disable MT Mode!')
    
path = './Coupling_TEST'
path_remote = '/eos/user/l/lichengz/VHH4bAnalysisNtuples/TEST_2018_IHEPsite_20210414/haddjobs'

# file_list = {'{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0.root'.format(path),\
#              '{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0.root'.format(path),\
#              '{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0.root'.format(path),\
#              '{0}/sum_ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0.root'.format(path),\
#              '{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0.root'.format(path),\
#              '{0}/sum_ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0.root'.format(path)
#             }
    
# fin1 = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0.root'.format(path_remote),'READ')
# fin2 = R.TFile.Open('{0}/sum_ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0.root'.format(path_remote),'READ')
# fin3 = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0.root'.format(path_remote),'READ')
# fin4 = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0.root'.format(path_remote),'READ')
# fin5 = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0.root'.format(path_remote),'READ')
# fin6 = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0.root'.format(path_remote),'READ')

# dict_rdf['ZHH_111'] = R.RDataFrame('Events', '{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0.root'.format(path))
# dict_rdf['ZHH_121'] = R.RDataFrame('Events', '{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0.root'.format(path))
# dict_rdf['ZHH_112'] = R.RDataFrame('Events', '{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0.root'.format(path))
# dict_rdf['ZHH_101'] = R.RDataFrame('Events', '{0}/sum_ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0.root'.format(path))
# dict_rdf['ZHH_110'] = R.RDataFrame('Events', '{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0.root'.format(path))
# dict_rdf['ZHH_1p511'] = R.RDataFrame('Events', '{0}/sum_ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0.root'.format(path))

# df_basis = R.RDataFrame('Events', file_list)

listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1]])
CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.0002278,0.000790])

Coupling0 = convert_coupling_diagramweight(listOfCouplings0)
CouplingInv0=np.linalg.inv(Coupling0)

matrix_ele = np.matmul(CouplingInv0, CrossSec0)

listOfCouplings = np.array([[0,1,1],[-0.5,1,1],[-1,1,1],[-1.5,1,1],[-2,1,1],[-3,1,1]])
strlistOfCouplings = ['-15_0', '-8_0', '-3_0', '3_0', '8_0', '15_0']

NewCoupling = convert_coupling_diagramweight(listOfCouplings)
newXsec = np.matmul(NewCoupling,matrix_ele.reshape(6,1))
composition = np.matmul(NewCoupling, CouplingInv0)

if args.verb == 0:
    print('composition of basic files has been saved, now start merging! ... ')
else:
    print("--------------------------- print Coupling0:")
    print(listOfCouplings0)
    print("--------------------------- print CrossSec0:")
    print(CrossSec0)
    print("---------------------------- print new couplings:")
    print(listOfCouplings)
    print("---------------------------- print new Xsec:")
    print(newXsec)
    print("---------------------------- print composition of original samples:")
    print(composition)

exit()
    
def Merge_Components(infile_name1, infile_name2, infile_name3, infile_name4, infile_name5, infile_name6, composition_matrix, string_couplings):
    tin1 = infile_name1.Get("Events")
    tin2 = infile_name2.Get("Events")
    tin3 = infile_name3.Get("Events")
    tin4 = infile_name4.Get("Events")
    tin5 = infile_name5.Get("Events")
    tin6 = infile_name6.Get("Events")
    
    print('Got All Trees.')
    
    for i in range(0,6,1):
        print('Start generate ' + str(i) + ' mixed sample...')
        
        fin1_bak = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0_bak.root'.format(path),'RECREATE')
        Save_Temp_Components(tin1, fin1_bak, composition[i,0])
        fin1_bak.Close()
        fin2_bak = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0_bak.root'.format(path),'RECREATE')
        Save_Temp_Components(tin2, fin2_bak, composition[i,1])
        fin2_bak.Close()
        fin3_bak = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0_bak.root'.format(path),'RECREATE')
        Save_Temp_Components(tin3, fin3_bak, composition[i,2])
        fin3_bak.Close()
        fin4_bak = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0_bak.root'.format(path),'RECREATE')
        Save_Temp_Components(tin3, fin3_bak, composition[i,3])
        fin4_bak.Close()
        fin5_bak = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0_bak.root'.format(path),'RECREATE')
        Save_Temp_Components(tin4, fin4_bak, composition[i,4])
        fin5_bak.Close()
        fin6_bak = R.TFile.Open('{0}/sum_ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0_bak.root'.format(path),'RECREATE')
        Save_Temp_Components(tin6, fin6_bak, composition[i,5])
        fin6_bak.Close()
        
        print('start saving ' + str(i) + ' mixed sample...')
        
#         chain_out = R.TChain('Events')
#         chain_out.Add('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0_bak.root'.format(path))
#         chain_out.Add('{0}/sum_ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0_bak.root'.format(path))
#         chain_out.Add('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0_bak.root'.format(path))
#         chain_out.Add('{0}/sum_ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0_bak.root'.format(path))
#         chain_out.Add('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0_bak.root'.format(path))
#         chain_out.Add('{0}/sum_ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0_bak.root'.format(path))
#         chain_out.Merge('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_{1}.root'.format(path,string_couplings[i]))
        
        df_new = R.RDataFrame('Events',{'{0}/*_bak.root'.format(path)})
#         os.system('hadd {0}/sum_ZHHTo4B_CV_1_0_C2V_{1}_C3_1_0.root {2}/*_bak.root'.format(path,string_couplings[i],path))
        df_new.Snapshot('Events','{0}/sum_ZHHTo4B_CV_1_0_C2V_{1}_C3_1_0.root'.format(path,string_couplings[i]))
        
        print('The ' + str(i) + ' mixed sample: {0}/sum_ZHHTo4B_CV_1_0_C2V_{1}_C3_1_0.root has been Saved!  Deleting temp files...'.format(path,string_couplings[i]))
        
        del fin1_bak, fin2_bak, fin3_bak, fin4_bak, fin5_bak, fin6_bak
        del df_new
#         del chain_out
        
        os.remove('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0_bak.root'.format(path))
        os.remove('{0}/sum_ZHHTo4B_CV_1_0_C2V_2_0_C3_1_0_bak.root'.format(path))
        os.remove('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0_bak.root'.format(path))
        os.remove('{0}/sum_ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0_bak.root'.format(path))
        os.remove('{0}/sum_ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0_bak.root'.format(path))
        os.remove('{0}/sum_ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0_bak.root'.format(path))
    #end
    del tin1, tin2, tin3, tin4, tin5, tin6
#END

Merge_Components(fin1, fin2, fin3, fin4, fin5, fin6, composition, strlistOfCouplings)
print('All new mixed sample saved')
fin1.Close()
fin2.Close()
fin3.Close()
fin4.Close()
fin5.Close()
fin6.Close()
del fin1, fin2, fin3, fin4, fin5, fin6
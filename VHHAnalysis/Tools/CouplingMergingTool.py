import numpy as np
import ROOT as R
import sys
import os
import argparse
import matplotlib.pyplot as plt
from util import *
from analysis_branch import file_list_ZHH

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--multiprocess",       dest="multi",    default=0,     type=int,   help="enable multi-processing with n threads (default = 0)" )
parser.add_argument("-v", "--verbose",            dest="verb",     default=0,     type=int,   help="different verbose level (default = 0)" )
parser.add_argument("-n", "--nBasicSamples",      dest="nBV",      default=6,     type=int,   help="N basic samples (default = 6)" )
parser.add_argument("-c", "--CouplingType",       dest="CType",    default="c2v", type=str,   help="Coupling type (default = c2v) cv/kl/kt ..." )
parser.add_argument("-hh", "--HHModel",            dest="HHModel",  default="VHH", type=str,   help="Coupling type (default = VHH) GGF/VBF/VHH ..." )
parser.add_argument("-r", "--CouplingRange",      dest="cRange",   nargs='+',                 help="[lower limit] [higher limit] (default = -30 30)")
parser.add_argument("-d", "--ifDoCombine",        dest="doComb",   default=0,     type=int,   help="if do combination (default = 0)")
parser.add_argument("-w", "--NewCoupling",        dest="newCoup",  default=10,    type=int,   help="The new coupling we need to combine (default = 10)")
args = parser.parse_args()

if args.multi != 0:
    R.EnableImplicitMT(args.multi)
    print('using ' + str(args.multi) + ' threads in MT Mode!')
else:
    print('Disable MT Mode!')
    
if args.HHModel == 'VHH':
    if args.nBV == 6:
        listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1,2,1]])
        CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000929])
    elif args.nBV == 7:
        listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1,2,1],[1.5,1,1]])
        CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000929,0.000790])
    elif args.nBV == 8:
        listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1,2,1],[1.5,1,1],[1,1,20]])
        CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000929,0.000790,0.0165721])
    else:
        print('There should be 6~8 samples to form the basic vectors, enforce to 6')
        listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1,2,1]])
        CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000790])

elif args.HHModel == 'VBF':
    listOfCouplings0 = np.array([[1,1,1],[1,1,0],[1,1,2],[1,0,1],[1,2,1],[0.5,1,1],[1.5,1,1]])
    CrossSec0 = np.array([0.0017260,0.0046089,0.0014228,0.0270800,0.0142178,0.0108237,0.0660185])
    
elif args.HHModel == 'GGF':
    listOfCouplings0 = np.array([[0,1],[1,1],[2.45,1],[5,1]])
    CrossSec0 = np.array([0.069725,0.031047,0.013124,0.091172])
else:
    print(args.HHModel+" model not exist or haven't been developped, please further check.")
    exit(0)
    
lowLimit = int(args.cRange[0])
highLimit = int(args.cRange[1])
numEle = highLimit - lowLimit
longListOfXSec0 = []

if args.HHModel == 'VHH' or args.HHModel == 'VBF':
    Coupling0 = convert_coupling_diagramweight_VBF_VHH(listOfCouplings0)
    CouplingInv0=np.linalg.pinv(Coupling0)
    matrix_ele0 = np.matmul(CouplingInv0, CrossSec0)
    longListOfCoupling = np.zeros(shape=(numEle,3))
    if args.CType == 'c2v':
        for num in range(lowLimit,highLimit):
            longListOfCoupling[num-lowLimit] = [1,num,1]
    elif args.CType == 'kl':
        for num in range(lowLimit,highLimit):
            longListOfCoupling[num-lowLimit] = [1,1,num]
    elif args.CType == 'cv':
        for num in range(lowLimit,highLimit):
            longListOfCoupling[num-lowLimit] = [num,1,1]
    else:
        print(args.CType + 'is not in SM coupling list or under developing, enforce to c2v')
        for num in range(lowLimit,highLimit):
            longListOfCoupling[num-lowLimit] = [1,num,1]
    
    for element in longListOfCoupling:
        elementCoupling = convert_coupling_diagramweight_VBF_VHH(element.reshape(1,3))
        elementXsec = np.matmul(elementCoupling,matrix_ele0.reshape(6,1))
        longListOfXSec0.append(elementXsec[0,0])
    
elif args.HHModel == 'GGF':
    Coupling0 = convert_coupling_diagramweight_GGF(listOfCouplings0)
    CouplingInv0=np.linalg.pinv(Coupling0)
    matrix_ele0 = np.matmul(CouplingInv0, CrossSec0)
    longListOfCoupling = np.zeros(shape=(numEle,2))
    if args.CType == 'kl':
        for num in range(lowLimit,highLimit):
            longListOfCoupling[num-lowLimit] = [num,1]
    elif args.CType == 'kt':
#         for num in range(lowLimit,highLimit):
#             longListOfCoupling[num-lowLimit] = [1,num]
        print(args.CType + 'is under developing, enforce to kl')
        for num in range(lowLimit,highLimit):
            longListOfCoupling[num-lowLimit] = [num,1]
    else:
        print(args.CType + 'is not in SM coupling list or under developing, enforce to kl')
        for num in range(lowLimit,highLimit):
            longListOfCoupling[num-lowLimit] = [num,1]
            
    for element in longListOfCoupling:
        elementCoupling = convert_coupling_diagramweight_GGF(element.reshape(1,2))
        elementXsec = np.matmul(elementCoupling,matrix_ele0.reshape(3,1))
        longListOfXSec0.append(elementXsec[0,0])
else:
    print(args.HHModel+" model not exist or haven't been developped, please further check.")
    exit(0)

x = np.arange(lowLimit,highLimit)
plt.plot(x,longListOfXSec0,color='green',label='{0} bases'.format(args.nBV))
annotation = "Base [1,1,20]"
new_annotation = "{2} new point {0} = {1} \n xs = {3}".format(args.CType,args.newCoup,args.HHModel,str(longListOfXSec0[np.argwhere(x == int(args.newCoup))[0][0]]))

plt.xlabel(args.CType)
plt.ylabel("XSec")
plt.title("XSec variation with {0}".format(args.CType))
plt.grid()
plt.legend(loc='best',fontsize=12)
# plt.text(-20,0.035,'6 bases:[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1]\n7 bases: Add [0.5,1,1]\n8 bases: Add [1,1,20]\nAttention:The green and red line overlap',fontsize=12)
# plt.text(0,1,'other couplings are set to 1 (SM)')
# plt.scatter(x=20,y=0.0165721,s=40,c='y',marker='^')
# plt.annotate(annotation,(20,0.0165721))
plt.scatter(x=args.newCoup,y=longListOfXSec0[np.argwhere(x == int(args.newCoup))[0][0]],s=40,c='y',marker='^')
plt.annotate(new_annotation,(args.newCoup,longListOfXSec0[np.argwhere(x == int(args.newCoup))[0][0]]))
plt.savefig('./MyFig.jpg')
plt.show()
plt.close()

if args.HHModel == 'VHH' or args.HHModel == 'VBF': 
    if args.CType == 'c2v':
        listOfCouplings = np.array([[1,args.newCoup,1]])
    elif args.CType == 'kl':
        listOfCouplings = np.array([[1,1,args.newCoup]])
    elif args.CType == 'cv':
        listOfCouplings = np.array([[args.newCoup,1,1]])
    else:
        print(args.CType + 'is not in SM coupling list or under developing, enforce to c2v')
        listOfCouplings = np.array([[1,args.newCoup,1]])
    NewCoupling = convert_coupling_diagramweight_VBF_VHH(listOfCouplings)
    newXsec = np.matmul(NewCoupling,matrix_ele0.reshape(6,1))
    composition = np.matmul(NewCoupling, CouplingInv0)
elif args.HHModel == 'GGF':
    if args.CType == 'kl':
        listOfCouplings = np.array([[args.newCoup,1]])
    elif args.CType == 'kt':
        print(args.CType + 'is under developing, enforce to kl') #Cautious
        listOfCouplings = np.array([[args.newCoup,1]])
    else:
        print(args.CType + 'is not in SM coupling list or under developing, enforce to kl')
        listOfCouplings = np.array([[args.newCoup,1]])
    NewCoupling = convert_coupling_diagramweight_GGF(listOfCouplings)
    newXsec = np.matmul(NewCoupling,matrix_ele0.reshape(3,1))
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

if args.doComb == 0:
    exit(0)
else:
    print("Combination process starting...")

#TODO Add VBF & GGF channels
# args.path
# if VHH
slimmed_sample_path = 'Pre_SlimmedSample_temp'
slimmed_signal_path = 'Pre_SlimmedSignal'
os.system('mkdir -p Pre_SlimmedSignal')

if args.nBV == 6:
    file_list_ZHH = ['ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0','ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0',\
                     'ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0','ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0']
elif args.nBV == 7:
    file_list_ZHH = ['ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0','ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0',\
                     'ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0','ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0',\
                     'ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0']
elif args.nBV == 8:
    file_list_ZHH = ['ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0','ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_2_0',\
                     'ZHHTo4B_CV_1_0_C2V_0_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_0_0','ZHHTo4B_CV_1_5_C2V_1_0_C3_1_0',\
                     'ZHHTo4B_CV_0_5_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0']
else:
    print('There should be 6~8 samples to form the basic vectors, combine failed')
    exit(0)
    
rdf_dict = {}
for _sig_file in file_list_ZHH:
    haddcmd = 'hadd -f {0}/{1}.root {2}/{1}*.root'.format(slimmed_signal_path,_sig_file,slimmed_sample_path)
    os.system(haddcmd)
    rdf_dict[_sig_file] = R.RDataFrame('Events','{0}/{1}.root'.format(slimmed_signal_path,_sig_file))
#end

composition_string = []
for _comp in composition:
    composition_string.append(str(_comp))

indexx = 0
for _sig_file in file_list_ZHH:
    print('calculating new weight for '+_sig_file)
    rdf_dict[_sig_file].Define('new_weight_for_signal','weight*{0}'.format(composition[0,indexx])).Snapshot('Events','{0}/{1}_new_weight.root'.format(slimmed_signal_path,_sig_file))
    print(rdf_dict[_sig_file].Filter('VHH_nBJets==4').Sum('weight').GetValue())
    print('weight*{0}'.format(composition[0,indexx]))
    print(rdf_dict[_sig_file].Define('new_weight_for_signal','weight*{0}'.format(composition[0,indexx])).Sum('intWeight').GetValue())
    indexx+=1
#end

if args.CType == 'c2v':
    comb_filename = 'ZHHTo4B_CV_1_0_C2V_{0}_0_C3_1_0_new_sample_by_{1}'.format(str(args.newCoup),str(args.nBV))
elif args.CType == 'kl':
    comb_filename = 'ZHHTo4B_CV_1_0_C2V_1_0_C3_{0}_0_new_sample_by_{1}'.format(str(args.newCoup),str(args.nBV))
elif args.CType == 'cv':
    comb_filename = 'ZHHTo4B_CV_{0}_0_C2V_1_0_C3_1_0_new_sample_by_{1}'.format(str(args.newCoup),str(args.nBV))
else:
    print(args.CType + 'is not in SM coupling list or under developing, enforce to c2v')
    comb_filename = 'ZHHTo4B_CV_1_0_C2V_{0}_0_C3_1_0_new_sample_by_{1}'.format(str(args.newCoup),str(args.nBV))
    
haddcmd = 'hadd -f {0}/{1}.root {2}/*_new_weight.root'.format(slimmed_signal_path,comb_filename,slimmed_signal_path)
os.system(haddcmd)

rdf_dict['new'] = R.RDataFrame('Events', '{0}/{1}.root'.format(slimmed_signal_path,comb_filename))

rdf_dict['val'] = R.RDataFrame('Events', '{0}/ZHHTo4B_CV_1_0_C2V_1_0_C3_20_0_val.root'.format(slimmed_signal_path))

# rdf_dict.delete()
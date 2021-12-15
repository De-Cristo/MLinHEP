import numpy as np
import ROOT as R
import sys
import os
from util import convert_coupling_diagramweight, Save_Temp_Components
import argparse
import matplotlib.pyplot as plt


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
listOfCouplings1 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1],[0.5,1,1]])
listOfCouplings2 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1],[0.5,1,1],[1,1,20]])

CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.0002278,0.000790])
CrossSec1 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.0002278,0.000790,0.0002278])
CrossSec2 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.0002278,0.000790,0.0002278,0.0165721])#Maybe some bias

Coupling0 = convert_coupling_diagramweight(listOfCouplings0)
Coupling1 = convert_coupling_diagramweight(listOfCouplings1)
Coupling2 = convert_coupling_diagramweight(listOfCouplings2)

CouplingInv0=np.linalg.pinv(Coupling0)
CouplingInv1=np.linalg.pinv(Coupling1)
CouplingInv2=np.linalg.pinv(Coupling2)

matrix_ele0 = np.matmul(CouplingInv0, CrossSec0)
print(CouplingInv1)
print(CrossSec1)
matrix_ele1 = np.matmul(CouplingInv1, CrossSec1)
matrix_ele2 = np.matmul(CouplingInv2, CrossSec2)

#print(matrix_ele)
lowLimit = -30
highLimit = 31
numEle = highLimit - lowLimit
#Coupling list of c2v [-30,30]
longListOfCoupling = np.zeros(shape=(numEle,3))

longListOfXSec0 = []
longListOfXSec1 = []
longListOfXSec2 = []

for num in range(lowLimit,highLimit):
    longListOfCoupling[num-lowLimit] = [1,1,num]


for element in longListOfCoupling:
    elementCoupling = convert_coupling_diagramweight(element.reshape(1,3))
    elementXsec = np.matmul(elementCoupling,matrix_ele0.reshape(6,1))
    #print(elementXsec)
    longListOfXSec0.append(elementXsec[0,0])

for element in longListOfCoupling:
    elementCoupling = convert_coupling_diagramweight(element.reshape(1,3))
    elementXsec = np.matmul(elementCoupling,matrix_ele1.reshape(6,1))
    #print(elementXsec)
    longListOfXSec1.append(elementXsec[0,0])

for element in longListOfCoupling:
    elementCoupling = convert_coupling_diagramweight(element.reshape(1,3))
    elementXsec = np.matmul(elementCoupling,matrix_ele2.reshape(6,1))
    #print(elementXsec)
    longListOfXSec2.append(elementXsec[0,0])


#print(longListOfXSec)
x = np.arange(lowLimit,highLimit)
plt.plot(x,longListOfXSec0,color='green',label='6 bases')
plt.plot(x,longListOfXSec1,color='red',label='7 bases')
plt.plot(x,longListOfXSec2,color='blue',label='8 bases')

annotation = "Base [1,1,20]"

plt.xlabel("kl")
plt.ylabel("XSec")
plt.title("XSec variation with kl")
plt.grid()
plt.legend(loc='best',fontsize=12)
plt.text(-20,0.035,'6 bases:[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1]\n7 bases: Add [0.5,1,1]\n8 bases: Add [1,1,20]\nAttention:The green and red line overlap',fontsize=12)
plt.text(0,1,'cv=1,KL=1')
plt.scatter(x=20,y=0.0165721,s=40,c='y',marker='^')
plt.annotate(annotation,(20,0.0165721))
plt.show()

listOfCouplings = np.array([[1,1,20],[1,1,1],[-1,1,1],[-1.5,1,1],[-2,1,1]])
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
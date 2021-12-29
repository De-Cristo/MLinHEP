import numpy as np
import ROOT as R
import sys
import os
from util import convert_coupling_diagramweight, Save_Temp_Components
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--multiprocess",       dest="multi",  default=0, type=int,   help="enable multi-processing with n threads (default = 0)" )
parser.add_argument("-v", "--verbose",            dest="verb",   default=0, type=int,   help="different verbose level (default = 0)" )
parser.add_argument("-n", "--nBasicSamples",      dest="nBV",    default=6, type=int,   help="N basic samples (default = 6)" )
parser.add_argument("-c", "--CouplingType",       dest="CType",  default="c2v", type=str,   help="Coupling type (default = c2v) cv/kl/kt ..." )
parser.add_argument("-r", "--CouplingRange",      dest="cRange", nargs='+', help="[lower limit] [higher limit] (default = -30 30)")
parser.add_argument("-d", "--ifDoCombine",        dest="doComb", default=0, type=int,   help="if do combination (default = 0)")
parser.add_argument("-w", "--NewCoupling",        dest="newCoup",default=10,type=int,   help="The new coupling we need to combine (default = 10)")
parser.add_argument("-p", "--IOpaths",            dest="path",   default='.',type=str,   help="I/O path of the basic/merged samples (default = .)")
args = parser.parse_args()

if args.multi != 0:
    R.EnableImplicitMT(args.multi)
    print('using ' + str(args.multi) + ' threads in MT Mode!')
else:
    print('Disable MT Mode!')
    
if args.nBV == 6:
    listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1]])
    CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000790])
elif args.nBV == 7:
    listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1],[0.5,1,1]])
    CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000790,0.0002278])
elif args.nBV == 8:
    listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1],[0.5,1,1],[1,1,20]])
    CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000790,0.0002278,0.0165721])
else:
    print('There should be 6~8 samples to form the basic vectors, enforce to 6')
    listOfCouplings0 = np.array([[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1]])
    CrossSec0 = np.array([0.000363,0.0002278,0.000584,0.0001245,0.000212,0.000790])

Coupling0 = convert_coupling_diagramweight(listOfCouplings0)
CouplingInv0=np.linalg.pinv(Coupling0)
matrix_ele0 = np.matmul(CouplingInv0, CrossSec0)

print(CouplingInv0)
print(CrossSec0)

lowLimit = int(args.cRange[0])
highLimit = int(args.cRange[1])

numEle = highLimit - lowLimit
longListOfCoupling = np.zeros(shape=(numEle,3))

longListOfXSec0 = []

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
    elementCoupling = convert_coupling_diagramweight(element.reshape(1,3))
    elementXsec = np.matmul(elementCoupling,matrix_ele0.reshape(6,1))
    longListOfXSec0.append(elementXsec[0,0])

x = np.arange(lowLimit,highLimit)
plt.plot(x,longListOfXSec0,color='green',label='{0} bases'.format(args.nBV))
annotation = "Base [1,1,20]"
new_annotation = "new point {0} = {1}".format(args.CType,args.newCoup)

print("c2v = 10, xs = "+str(np.argwhere(x == int(args.newCoup))))

plt.xlabel(args.CType)
plt.ylabel("XSec")
plt.title("XSec variation with {0}".format(args.CType))
plt.grid()
plt.legend(loc='best',fontsize=12)
plt.text(-20,0.035,'6 bases:[1,1,1],[0.5,1,1],[1,1,2],[1,0,1],[1,1,0],[1.5,1,1]\n7 bases: Add [0.5,1,1]\n8 bases: Add [1,1,20]\nAttention:The green and red line overlap',fontsize=12)
plt.text(0,1,'other couplings are set to 1 (SM)')
# plt.scatter(x=20,y=0.0165721,s=40,c='y',marker='^')
# plt.annotate(annotation,(20,0.0165721))
plt.scatter(x=args.newCoup,y=longListOfXSec0[np.argwhere(x == int(args.newCoup))[0][0]],s=40,c='y',marker='^')
plt.annotate(new_annotation,(args.newCoup,longListOfXSec0[np.argwhere(x == int(args.newCoup))[0][0]]))
plt.savefig('./MyFig.jpg')
plt.show()
plt.close()

if args.CType == 'c2v':
    listOfCouplings = np.array([[1,args.newCoup,1]])
elif args.CType == 'kl':
    listOfCouplings = np.array([[1,1,args.newCoup]])
elif args.CType == 'cv':
    listOfCouplings = np.array([[args.newCoup,1,1]])
else:
    print(args.CType + 'is not in SM coupling list or under developing, enforce to c2v')
    listOfCouplings = np.array([[1,args.newCoup,1]])

NewCoupling = convert_coupling_diagramweight(listOfCouplings)
newXsec = np.matmul(NewCoupling,matrix_ele0.reshape(6,1))
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

#TODO
# args.path
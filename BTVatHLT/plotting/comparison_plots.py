import numpy as np
import matplotlib.pyplot as plt
import uproot as u
import awkward as ak

import os
import sys
import argparse

from util import *
from train_vars import *

from multiprocessing import Pool

from functools import reduce

parser = argparse.ArgumentParser()
parser.add_argument("--diffFile", dest='difffile', default=0, type=int, help="Set to 1 if comparing different file, OR 0")
parser.add_argument("--diffLabel", dest='difflabel', default=1, type=int, help="Set to 1 if comparing different label, OR 0")
parser.add_argument("-i1", "--File1", dest='file1', default='../datasample/output_0502.root', type=str, help="input root file 1")
parser.add_argument("-i2", "--File2", dest='file2', default='../datasample/output_0502.root', type=str, help="input root file 2")
parser.add_argument("-l1", "--Label1", dest='label1', default='B', type=str, help="The label 1; default: B;")
parser.add_argument("-l2", "--Label2", dest='label2', default='UDSG', type=str, help="The label 2; default: UDSG;")
parser.add_argument("-o", "--outDir", dest='outdir', default='./plots_comparison/', type=str, help="direction that output figure stored in")
parser.add_argument("-m", "--MultiThreads", dest='mt', default=1, type=int, help="The number of threads that been used")
args = parser.parse_args()

File1 = args.file1
File2 = args.file2
Label1= args.label1
Label2= args.label2
ourDir = args.outdir
MT     = args.mt

os.system('mkdir -p {}'.format(ourDir))

arg_list = []
information_list = time_information+csv_information+track_information

if args.difffile == 1 and args.difflabel == 1:
    process_tree1 = u.open(File1)["deepntuplizer"]["tree"]
    process_tree2 = u.open(File2)["deepntuplizer"]["tree"]
    label_sel1 = reduce(np.logical_or, [process_tree1[k].array() == 1 for k in label_n_masks[Label1]])
    label_sel2 = reduce(np.logical_or, [process_tree2[k].array() == 1 for k in label_n_masks[Label2]])
    
    # time information
    for _var in information_list:
        array1 = ak.flatten(process_tree1[_var].array()[label_sel1], axis=None)
        array2 = ak.flatten(process_tree2[_var].array()[label_sel2], axis=None)
        arguement = [array1, array2, _var, ourDir, Label1, Label2]
        arg_list.append(arguement)
    with Pool(MT) as p:
        p.map(plot_comparison_manager, arg_list)
        
elif args.difffile == 1 and args.difflabel == 0:
    process_tree1 = u.open(File1)["deepntuplizer"]["tree"]
    process_tree2 = u.open(File2)["deepntuplizer"]["tree"]
#     label_sel1 = reduce(np.logical_or, [process_tree1[k].array() == 1 for k in label_n_masks[Label1]])
    # time information
    for _var in information_list:
        array1 = ak.flatten(process_tree1[_var].array(), axis=None)
        array2 = ak.flatten(process_tree2[_var].array(), axis=None)
        arguement = [array1, array2, _var, ourDir, 'local', 'condor']
        arg_list.append(arguement)
    with Pool(MT) as p:
        p.map(plot_comparison_manager, arg_list)
    
elif args.difffile == 0 and args.difflabel == 1:
    process_tree1 = u.open(File1)["deepntuplizer"]["tree"]
    label_sel1 = reduce(np.logical_or, [process_tree1[k].array() == 1 for k in label_n_masks[Label1]])
    label_sel2 = reduce(np.logical_or, [process_tree1[k].array() == 1 for k in label_n_masks[Label2]])
    
    # time information
    for _var in information_list:
        array1 = ak.flatten(process_tree1[_var].array()[label_sel1], axis=None)
        array2 = ak.flatten(process_tree1[_var].array()[label_sel2], axis=None)
        arguement = [array1, array2, _var, ourDir, Label1, Label2]
        arg_list.append(arguement)
    with Pool(MT) as p:
        p.map(plot_comparison_manager, arg_list)
    
else:
    exit(0)
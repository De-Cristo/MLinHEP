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

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inFile", dest='infile', default='../datasample/output_0502.root', type=str, help="input root file")
parser.add_argument("-o", "--outDir", dest='outdir', default='./plots/', type=str, help="direction that output figure stored in")
parser.add_argument("-m", "--MultiThreads", dest='mt', default=1, type=int, help="The number of threads that been used")
args = parser.parse_args()

inFile = args.infile
ourDir = args.outdir
MT     = args.mt
os.system('mkdir -p {}'.format(ourDir))

process_tree = u.open(inFile)["deepntuplizer"]["tree"]

arg_list = []

information_list = time_information+csv_information+track_information

for _var in information_list:
    arguement = [process_tree[_var], _var, ourDir]
    arg_list.append(arguement)
    
with Pool(MT) as p:
    p.map(plot_manager, arg_list)
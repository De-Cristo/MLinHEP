import os
import sys

import numpy as np
import pandas as pd
import array as array

import ROOT as R

from multiprocessing import Pool
import subprocess
import argparse

from file_config import *

def data_split(full_list, batch=1, shuffle=False):
    n_total   = len(full_list)
    cats      = int(n_total/batch)
    n_cats = 1
    res_batch = batch%n_total
    sublist = []
    
    if cats == 0:
        return n_cats, full_list
    
    if shuffle:
        np.random.shuffle(full_list)
                
    for _c in range(1,cats+1):
        sublist.append(full_list[batch*(_c-1):batch*_c])
        
    n_cats = cats
    if res_batch!=0:
        sublist.append(full_list[batch*(cats):])
        n_cats+=1
        
    return n_cats, sublist

def ClassifySamples(_file_list):
    _sample_type = []
    _training_samples = []
    _testing_samples  = []
        
    for _file_name in _file_list:
        _type = -1
        for _flag in training_list:
            if _flag in _file_name:
                print(_file_name + ' will be used as training sample.')
                _training_samples.append(_file_name)
                _type = 0
                break
            else:
                continue
        #end
        for _flag in testing_list:
            if _flag in _file_name:
                print(_file_name + ' will be used as testing sample.')
                _testing_samples.append(_file_name)
                _type = 1
                break
            else:
                continue
        #end
        if _type==-1:
            print('WARNING:: ' + _file_name + ' is not concluded in the sample lists! It will not be used.')
        _sample_type.append(_type)
    #end
    return _sample_type, _training_samples, _testing_samples
#END
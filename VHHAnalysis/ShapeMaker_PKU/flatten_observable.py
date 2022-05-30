from rootpy.plotting import Hist
from rootpy.io import File
import numpy as np
from Dictionaries.VHH4b_channelDict_2018 import channelDict
from rootpy.tree import Tree, TreeChain
from glob import glob

from condor_config import indir as ntuple_path

#WH_signal = ["*WplusH125_powheg*.root","*WminusH125_powheg*.root"]
#ZH_signal = ["*ZH125_ZLL_powheg*.root","*ZH125_ZNuNu_powheg*.root","*ggZH125_ZLL_powheg*.root","*ggZH125_ZNuNu_powheg*.root"]

VHH_signal = ["/ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0*/*root"]
# VHH_signal = ["/WHHTo4B_CV_1_0_C2V_1_0_C3_20_0/*root"]

#selection = "V_pt>=150&&isWenu&&controlSample==0&&V_pt<=250&&boostedCategory==0"
#variable = "CMS_vhbb_DNN_Wen_13TeV"

#for a given channel in the channel dict, get the selection and plot variable and compute the flattened signal, nbins
def getFlatBinning(files,selection,variable,_nbins,xlow,xhigh):
    values = []
    for f in files:
        tree = File(f,"read").get("Events")
        array = tree.to_array([variable,"weight"],selection=selection)
        values.append(array)
    values = np.concatenate(values)
    #values = tree.to_array([variable,"weight"],selection=selection+"&&event%2==1")

    s_tot = values["weight"].sum()
    #make 5 bins the minimum and 15 bins the max
    if s_tot>15:
        bins = 15
    elif s_tot<1:
        bins = 1
    else:
        bins = int(s_tot)
    bins = _nbins
    if 'isZnn' in selection:  bins = 10
    print("Signal total: ",s_tot)
    values = np.sort(values)
    cumu = np.cumsum(values["weight"])
    targets = [n*s_tot/bins for n in range(1,bins)]
    #print(targets)
    workingPoints = []
    
    for target in targets:
        index = np.argmax(cumu>target)
        workingPoints.append(values[index][variable])
    

    #To test:
    #chain = TreeChain('Events',files)
    #hist = Hist(([-1]+workingPoints+[1]),name="hist")
    #chain.Draw(variable,selection="weight*("+selection+"&&event%2==1)",hist=hist)

    print(workingPoints) 
    return [float(xlow)]+workingPoints+[float(xhigh)]

binsDict = {}
for key in channelDict:
    if "doRebin" in channelDict[key].keys():
        if channelDict[key]["doRebin"]==1:
            print(key)
            print("it's flattening time")
            #if "Wen" in key or "Wmn" in key:
            #    samples = WH_signal
            #elif "Znn" in key or "Zee" in key or "Zmm" in key:
            #    samples = ZH_signal
            samples = VHH_signal
            sample_paths = [glob(ntuple_path+sample) for sample in samples]
            sample_paths1D = [path for sample_glob in sample_paths for path in sample_glob]
            binning = getFlatBinning(sample_paths1D,channelDict[key]["cutstring"],channelDict[key]["varNames"][0],channelDict[key]["nBins"],channelDict[key]["xlow"],channelDict[key]["xhigh"])
            binsDict[key] = binning

outputFile = open("Dictionaries/VHH4b_binsDict.py","w")
content = "binsDict = "
content += str(binsDict).replace('],','],\n')+'\n'
outputFile.write(content)
outputFile.close()

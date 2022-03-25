# ======================================================
# Shape Maker for Datacards, for VHbb 2016 Analysis
# Author: Spandan Mondal
# RWTH Aachen University, Germany
#
# This is the first step for the ShapeMaker module, to
# get the binnings in the SR that satisfy the maximum
# statistical uncertainty requirement.
# ======================================================

from ROOT import *
gROOT.SetBatch(True)
import argparse, os, sys, numpy, json
from math import sqrt, pow
import pdb

usingRDF = False
rootver = gROOT.GetVersion()
if '/' in rootver: rootver = rootver.split('/')[0]
if float(rootver) >= 6.14:
    TH1DModel = ROOT.RDF.TH1DModel
    ROOTDataFrame = ROOT.RDataFrame
    print "Detected ROOT %s. Successfully loaded RDataFrame."%rootver
    usingRDF = True
else:
    TH1DModel = ROOT.Experimental.TDF.TH1DModel
    ROOTDataFrame = ROOT.Experimental.TDataFrame
    print "***** WARNING *****: Detected ROOT %s. Loaded TDataFrame instead of RDataFrame. Multithreading will also be forced off. This is usually slower than RDataFrame. Please use ROOT 6.14 and above for better performance.\n"%rootver

parser = argparse.ArgumentParser("Get the necessary binnings for SRs such that first and last bins have at most 35% statistical uncertainty.")
parser.add_argument('-d', '--inputdir', type=str, default="/nfs/dust/cms/user/lmastrol/VHbbAnalysisNtuples/VHbbNtuple_March16_forApproval_fixZnnHF/haddjobs/", help="The directory where all the ntuples are stored.")
parser.add_argument('--vptcut', type=str, default="", help="The cut on V_pT, required for combination with boosted analysis.")
parser.add_argument('--multithread', action="store_true", default=False, help="Enable Multithreading for RDataFrame.")
args = parser.parse_args()
print args

from Dictionaries.VHbb_combinedFileDict import Zll_fileDict, Wln_fileDict, Znn_fileDict
fileDict = dict(Zll_fileDict.items() + Wln_fileDict.items() + Znn_fileDict.items())
from Dictionaries.VHbb_channelDict import channelDict
#from nano_samples_2016_FlavSplit_vhcc import the_samples_dict
from nano_samples_2017stxs import the_samples_dict
from nano_samples_znn2017stxs import the_samples_dict as the_samples_dict_znn

if args.multithread and usingRDF: ROOT.EnableImplicitMT(2)

rootList = sorted([i for i in os.listdir(args.inputdir) if i.endswith(".root")])

nBinsFine = 1000

MCDict = {}

for rootFile in rootList:
    sampMatch = [sampname for sampname in fileDict.keys() if sampname in rootFile]
    #print fileDict.keys()
    if len(sampMatch) == 0:
        print "\n***** WARNING *****: No sample matches with file: %s. Skipping.\n"%(rootFile)
    else:
        isamp = sorted(sampMatch,key=len)[-1]
        if isamp.startswith("Run"):
            print "File %s has been identified as data."%rootFile
        else:
            MCDict[rootFile] = isamp

chain = TChain("Events")
for MC in MCDict:
    chain.Add(os.path.join(args.inputdir,MC))

DF = ROOTDataFrame(chain)
#pdb.set_trace()
nMyCol = 0
columnDict = {}
def addcolumn(formula):
    global DF, nMyCol, columnDict
    collist = list(DF.GetColumnNames())
    if formula not in columnDict.keys() and formula not in collist:
        nMyCol+=1
        DF = DF.Define("MyCol%i"%nMyCol,formula)
        columnDict[formula] = "MyCol%i"%nMyCol
    if formula not in columnDict.keys() and formula in collist:
        columnDict[formula] = formula

varDict = {}
histDict = {}
#print "channeldict:"
#print channelDict
for channel in channelDict:
    if channelDict[channel]["doRebin"] == 1:
        channelName = channelDict[channel]["channelName"]
        presel = channelDict[channel]["cutstring"]
        print channelName, ": ", presel
        if args.vptcut == "":
            vptcutStr = ""
        else:
            if channelName == "Znn":
                vptcutStr = " && MET_Pt < %s"%(args.vptcut)
            else:
                vptcutStr = " && V_pt < %s"%(args.vptcut)
        presel = presel.replace("VPTCUT",vptcutStr)
        addCuts = " && ("        
        
        if channelName == "Znn":
            samples_dict = the_samples_dict_znn
        else:
            samples_dict = the_samples_dict
        for process in samples_dict:
            legend = samples_dict[process][2]
            sInd = samples_dict[process][0]
            #print "process",process
            print "legend", legend
            print "channel", channel
            #print "sInd", sInd
            #if channel.startswith("VH"):
            if channel.startswith("bdt_SR"):
                if not legend.startswith(("WH_hbb","ZH_hbb","ggZH_hbb")):
                #if legend not in ["WH_hbb","ZH_hbb","ggZH_hbb"]:
                    if type(sInd)==int:
                        addCuts += "sampleIndex==%i || "%sInd
                    elif type(sInd)==str:
                        addCuts += sInd + " || "
                    else:
                        raise Exception("Bad sampleIndex value")

            #elif channel.startswith("VZ"):
            #    if legend != "VVbb":
            #        addCuts += "sampleIndex==%i || "%sInd
            else:
                print "\n***** WARNING *****: I was not expecting selection %s to require rebinning.\n"%(channel)
                
        addCuts = addCuts.rstrip(" || ")
        cutstring = presel + addCuts + ")"
        varStr = channelDict[channel]["varName"]
        
        if channelDict[channel]["doEven"] == 1:
            weightStr = "2.0*weight"
            cutstring += " && (event%2==0)"            
        else:
            weightStr = "weight"
        
        addcolumn(varStr)
        addcolumn(weightStr)
    
        print cutstring
        histDict[channel] = DF.Filter(  cutstring  )        \
                            .Histo1D(   TH1DModel(channel,channel,nBinsFine,float(channelDict[channel]["xlow"]),float(channelDict[channel]["xhigh"])),
                                        columnDict[varStr],
                                        columnDict[weightStr]
                                    )
        print "Created pointer to histogram for channel %s with cutstring:\n%s\n"%(channel,cutstring)

print "Triggering event loop. This will take a while."
nEvents = DF.Count()
binsDict = {}

oroot = TFile.Open("bkgHistos.root","RECREATE")
oroot.cd()
for channel in histDict:
    hBkg = histDict[channel]
    hBkg.Write()
    
    nBins = int(channelDict[channel]["nBins"])
    binBoundaries = numpy.zeros(nBins+1,dtype=float)
    binBoundaries[0] = float(channelDict[channel]["xlow"])
    binBoundaries[nBins] = float(channelDict[channel]["xhigh"])
    
    foundLowBinEdge = False
    foundHighBinEdge = False
    
    B_err2_low = 0.
    B_err2_high = 0.
    for ibin in range(1,nBinsFine):
        if not foundLowBinEdge:
            B_low = hBkg.Integral(1,ibin)
            B_err2_low += pow(hBkg.GetBinError(ibin),2) 
            if (B_low > 0 and sqrt(B_err2_low)/B_low < 0.35):
                binBoundaries[1] = hBkg.GetBinLowEdge(ibin+1)
                foundLowBinEdge = True

        if not foundHighBinEdge:
            B_high = hBkg.Integral(nBinsFine-ibin+1, nBinsFine) 
            B_err2_high += pow(hBkg.GetBinError(nBinsFine-ibin+1),2)
#            S_high = hSig.Integral(nBinsFine-ibin+1, nBinsFine) 
            if (B_high > 0 and sqrt(B_err2_high)/B_high < 0.35):
                binBoundaries[nBins-1] = hBkg.GetBinLowEdge(nBinsFine-ibin+1)
                foundHighBinEdge = True

    # split the middle bins equidistantly
    for i in range(2,nBins-1):
        binBoundaries[i] = binBoundaries[1] + (i-1)*((binBoundaries[nBins-1] - binBoundaries[1])/(nBins-2)) 
    
    binsDict[channel] = list(binBoundaries)

oroot.Close()

print "\nProcessed %i events.\n"%(int(nEvents))
for i in binsDict:
    print i, ":", binsDict[i]

with open('Dictionaries/VHbb_binsDict.py','w') as data:
    data.write("binsDict = ")
    data.write(str(json.dumps(binsDict, indent=4, sort_keys=True)))

print "\nCreated VHbb_binsDict.py with the binning."

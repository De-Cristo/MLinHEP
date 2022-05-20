# ======================================================
# Shape Maker for Datacards, for VHcc 2016 Analysis
# Author: Spandan Mondal
# RWTH Aachen University, Germany
#
# This code aims to optimize file access by adopting
# a per-file processing approach. It implements
# ROOT RDataFrame to create histograms (instead of
# TTree::Draw) for all pocesses, channels and
# systematics, so that the program loops only once
# over the input chain, thereby reducing disk access.
# ======================================================
#
# Modified for VHH analysis 
# Author: Yihui Lai
# ======================================================


from datetime import datetime
launchtime = datetime.now()
lasttime = launchtime

import rootpy
from ROOT import *
gROOT.SetBatch(True)
import argparse, os, sys
from array import array
from Dictionaries.VHH4b_fileDict_2018_2TO4_SM import Zll_fileDict, Wln_fileDict, Znn_fileDict
from Dictionaries.VHH4b_channelDict_2018_2TO4 import channelDict
from Dictionaries.VHH4b_sampleDict import Zll_sampleDict, Wln_sampleDict, Znn_sampleDict
from Dictionaries.VHH4b_binsDict import binsDict
from Dictionaries.VHH4b_reweightDict import reweightDict,reweightValueDict,reweightErrorDict
from Dictionaries.VHH4b_binsDict_addShapes import binsDictAddVars
from condor_config import year,addHists,doJEROnly

fileDict = dict(Zll_fileDict.items() + Wln_fileDict.items() + Znn_fileDict.items())

usingRDF = False
rootver = gROOT.GetVersion()
if '/' in rootver: rootver = rootver.split('/')[0]
if float(rootver) >= 6.14:
    TH1DModel = ROOT.RDF.TH1DModel
    TH2DModel = ROOT.RDF.TH2DModel
    ROOTDataFrame = ROOT.RDataFrame
    print "Detected ROOT %s. Successfully loaded RDataFrame."%rootver
    usingRDF = True
else:
    TH1DModel = ROOT.Experimental.TDF.TH1DModel
    TH2DModel = ROOT.Experimental.TDF.TH2DModel
    ROOTDataFrame = ROOT.Experimental.TDataFrame
    print "***** WARNING *****: Detected ROOT %s. Loaded TDataFrame instead of RDataFrame. Multithreading will also be forced off. This is usually slower than RDataFrame. Please use ROOT 6.14 and above for better performance.\n"%rootver 

# Message logger
def elapsed(string,level=0):
    nowtime = datetime.now()
    global lasttime
    print ' '*(level*4)+"T = %.1f mins; dT = %.3f mins: "%(float((nowtime-launchtime).seconds)/60, float((nowtime-lasttime).seconds)/60) + string
    lasttime = nowtime

parser = argparse.ArgumentParser("Produce shape histograms for datacards.")
parser.add_argument('-samp', '--samplename', type=str, default="", help="The name of the sample, eg, 'WHHTo4B_CV_1_0_C2V_1_0_C3_1_0'.")
parser.add_argument('-i', '--inputfile', type=str, default="", help="The input root file (ntuple). eg, 'output_WHHTo4B_CV_1_0_C2V_2_0_C3_1_0_1.root'")
parser.add_argument('-n', '--nOuts', type=str, default="0", help="The max. number of output files to produce. Use 0 to process full input file.")
parser.add_argument('-io', '--iOut', type=str, default="", help="The index of the first output file that will be produced if iOut!=0. So this instance of the program will produce ith to (i+n-1)th outputs.")
parser.add_argument('-d', '--inputdir', type=str, default="/eos/home-y/yilai/VHH4bAnalysisNtuples/TEST_0830_BDT/", help="The directory where all the ntuples are stored.")
parser.add_argument('-o', '--suffix', type=str, default="", help="suffix at the end of outputs")

parser.add_argument('-ld', '--lockDir', type=str, default=".", help="The directory where lock files will be stored to avoid parallel access while reading the same input file")
parser.add_argument('--vptcut', type=str, default="", help="The cut on V_pT, required for combination with boosted analysis.")
parser.add_argument('--skipVZ', action="store_true", default=False, help="Skip VZ selections.")
parser.add_argument('--skipsysts', action="store_true", default=False, help="Skip systematics.")
parser.add_argument('--dochannel',  type=str, default="", help="Do only specified channel.")
parser.add_argument('--multithread', action="store_true", default=False, help="Enable Multithreading for RDataFrame.")
parser.add_argument('--addBoostRewUnc', action="store_true", default=False, help="Add Reweight Uncertainty to the Boosted topology.")
args = parser.parse_args()
print args
# prefer two ways to run shapemaker
# 1) locally run the whole sample, -samp WHHTo4B_CV_1_0_C2V_1_0_C3_1_0,ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0
# 2) condor, -samp WHHTo4B_CV_1_0_C2V_1_0_C3_1_0 -i WHHTo4B_CV_1_0_C2V_1_0_C3_1_0_1.root,WHHTo4B_CV_1_0_C2V_1_0_C3_1_0_2.root

if args.multithread and usingRDF: ROOT.EnableImplicitMT(64)

ifile = args.inputfile
ipath = args.inputdir
isamp = args.samplename

ilist = []
if ',' in isamp:
    ilist = isamp.split(',')
    isamp = ilist[0]
#ilist will be ['WHHTo4B_CV_1_0_C2V_1_0_C3_1_0','ZHHTo4B_CV_1_0_C2V_1_0_C3_1_0'...]

nOuts = int(args.nOuts)
if nOuts != 0:
    if args.iOut=="" or int(args.iOut) < 0:
        print "\n***** ERROR *****: Invalid input for iOut.\n"
        sys.exit(1)
    iOut = int(args.iOut)
    lockDir = args.lockDir

print('fileDict ',fileDict)
print('isamp ',isamp)

if isamp != "":
    sampMatch = [sampname for sampname in fileDict.keys() if sampname in isamp]
    if len(sampMatch) == 0:
        print "\n***** ERROR *****: No sample matches with the input file, %s.\n"%(isamp)
        sys.exit(1)
    else:
        print("going to process "+ipath+"/"+isamp+"/*"+isamp+"*.root")
    print('sampMatch', sampMatch)
else:
    print "\n***** ERROR *****: Please provide inputfile and/or samplename as input."


outSuffix = ''.join(isamp.rstrip('.root').lstrip('sum_').split('_')) + '_'+args.suffix

if ifile=='':
    if ilist==[]:
        elapsed("Using *%s* as input file(s) and %s as input sample name."%(isamp,isamp))
        chain = TChain("Events")
        chain.Add(ipath+"/"+isamp+"/*"+isamp+"*.root")
        mainDF = ROOTDataFrame(chain)
        print("tot Events :", int(mainDF.Count()))
    else:
        #merge all the sample
        elapsed("Using %s as input files and %s as input sample name."%(str(ilist),isamp))
        chain = TChain("Events")
        for rootfile in ilist:
            print(ipath+"/"+rootfile+"/*"+rootfile+"*.root")
            chain.Add(ipath+"/"+rootfile+"/*"+rootfile+"*.root")
        mainDF = ROOTDataFrame(chain)
    elapsed("Created pointer to input files containing %s in the filename."%isamp)
else:    
    ifilelist = []
    ifilelist = ifile.split(',')
    elapsed("Using *%s* as input file(s) and %s as input sample name."%(isamp,isamp))
    chain = TChain("Events")
    for rootfile in ifilelist:
        chain.Add(ipath+"/"+isamp+"/"+rootfile)
    mainDF = ROOTDataFrame(chain)
    print("tot Events :", int(mainDF.Count()))

processArrays = fileDict[isamp]
print("================================= processArrays",processArrays)
processNames = [i[0] for i in processArrays]
print("================================= processNames",processNames)
elapsed("I see this file contributes to the following processes: "+str(processNames))

channelList = []
if isamp in Zll_fileDict:
    channelList.extend([channel for channel in channelDict if channelDict[channel]["channelName"]=="Zll"])
if isamp in Wln_fileDict:
    channelList.extend([channel for channel in channelDict if channelDict[channel]["channelName"]=="Wln"])
if isamp in Znn_fileDict:
    channelList.extend([channel for channel in channelDict if channelDict[channel]["channelName"]=="Znn"])


if args.skipVZ: channelList = [i for i in channelList if not i.startswith('VZ')]
elapsed("I am going to run over %i channels: "%(len(channelList)) + str(channelList))
print "Therefore, I will produce %ix%i=%i outputs."%(len(processNames),len(channelList),len(processNames)*len(channelList))
if nOuts != 0: print "However, I see this instance of me has been asked to produce only %i of these outputs starting with index %i."%(nOuts,iOut)

collist = list(mainDF.GetColumnNames())
if len(collist) == 0:
    print "\n***** ERROR *****: Wrong input file. Failed to load any data."
    sys.exit(1)

outputHistoDict = {}

nMyCol = 0
columnDict = {}
def addcolumn(formula):
    global mainDF, nMyCol, columnDict
    collist = list(mainDF.GetColumnNames())
    if formula not in columnDict.keys() and formula not in collist:
        nMyCol+=1
        mainDF = mainDF.Define("MyCol%i"%nMyCol,formula)
        columnDict[formula] = "MyCol%i"%nMyCol
    if formula not in columnDict.keys() and formula in collist:
        columnDict[formula] = formula
nFile = -1

for iprocess, processArray in enumerate(processArrays):
    #run over process 
    processName = processArray[0]
    processIdx = processArray[1]
    processSF  = processArray[2]
    elapsed("(%i of %i) Beginning with %s process."%(iprocess+1,len(processArrays),processName))
    if type(processIdx)==int:
        processCut = "sampleIndex==%i"%processIdx
    elif type(processIdx)==str:
        processCut = processIdx
    else:
        raise Exception("Bad sampleIndex value")

    for ichannel, channel in enumerate(channelList):
    #run over channel
        nFile += 1
        if nOuts != 0:
            if nFile < iOut or nFile >= iOut+nOuts: continue
        if args.dochannel != "":
            if not ',' in args.dochannel:
                if channel != args.dochannel: continue
            else:
                channelsToDo = args.dochannel.split(',')
                if channel not in channelsToDo: continue
        
        elapsed("(%i of %i) Processing %s channel."%(ichannel+1,len(channelList),channel),1)
        subdict = channelDict[channel]
        doReweight = False
        if "doReweight" in channelDict[channel].keys() and ("TT" in processName):# or "ST" in processName) :
            if channelDict[channel]["doReweight"]==1:
                doReweight = True
        if doReweight:
            presel = subdict["failcutstring"]
        else:
            presel = subdict["cutstring"]
        doEven = bool(subdict["doEven"])
        xlow = float(subdict["xlow"])
        xhigh = float(subdict["xhigh"])
        nBins = int(subdict["nBins"])
        channelName = subdict["channelName"]
        drawFromNom = bool(subdict["drawFromNom"])
        doVV = bool(subdict["doVV"])
        doRebin = bool(subdict["doRebin"])
        varNames = subdict["varNames"]
        N_vars=len(varNames) if addHists else 1
        isJEROnly = "_JEROnly" if doJEROnly else ""
        if type(processIdx)==int:
            outfilename = "hists_%s_%s_%s_idx%i_file-%s%s.root"%(year,channel,processName,processIdx,outSuffix,isJEROnly)
        elif type(processIdx)==str:
            print processIdx 
            outfilename = "hists_%s_%s_%s_idx%s_file-%s%s.root"%(year,channel,processName,processIdx.split("==")[1].split("&&")[0],outSuffix,isJEROnly)
        outputHistoDict[outfilename] = []

        for var_ind in range(N_vars):
            #run over varible
            varName = varNames[var_ind]
            if args.vptcut == "":
                vptcutStr = ""
            else:
                vptcutStr = " && V_pt < %s"%(args.vptcut)
            presel = presel.replace("VPTCUT",vptcutStr)
            #print("presel: ",presel)
            def addHisto(filterStr, hName, hTitle, varToPlot,varName, weight="", info="", reweightvarToPlot=""):
                global outputHistoDict
                if not varName=="":
                    if varName=="V_pt":
                        if "low" in channel:binning = binsDictAddVars[varName+"_low"]
                        elif "med" in channel:binning = binsDictAddVars[varName+"_med"]
                        elif "high" in channel: binning = binsDictAddVars[varName+"_high"]
                    else:binning = binsDictAddVars[varName]
                    histoModel = TH1DModel(hName,hTitle,len(binning)-1,array('d',binning))
                    print("create a histoModel:",hName,hTitle,binning)
                else:
                    if doRebin:
                        binning = binsDict[channel]
                        if len(binning)-1 != nBins:
                            print "\n***** WARNING *****: The binning in the file and 'nBins' are not consistent for channel %s. I will proceed, but please double check.\n"%channel
                        if doReweight:
                            if 'TTB' in hName:
                                rewbinning = reweightDict[channel]['TTB']
                            elif 'TT' in hName:
                                rewbinning = reweightDict[channel]['TT']
                            elif 'ST' in hName:
                                rewbinning = reweightDict[channel]['ST']
                            else:
                                print('impossible, so far I only consider TT and TTB')
                                exit()
                            histoModel = TH2DModel(hName,hTitle,len(binning)-1,array('d',binning) , len(rewbinning)-1,array('d',rewbinning))
                        else:
                            histoModel = TH1DModel(hName,hTitle,len(binning)-1,array('d',binning))
                    else:
                        histoModel = TH1DModel(hName,hTitle,nBins,xlow,xhigh)
                if doReweight:
                    if weight=="":
                        outputHistoDict[outfilename].append([mainDF.Filter(filterStr)        \
                                                            .Histo2D(   histoModel,
                                                                        columnDict[varToPlot],
                                                                        columnDict[reweightvarToPlot]
                                                                    ),
                                                            info ]
                                                           )
                    else:
                        outputHistoDict[outfilename].append([mainDF.Filter(filterStr)        \
                                                            .Histo2D(   histoModel,
                                                                        columnDict[varToPlot],
                                                                        columnDict[reweightvarToPlot],
                                                                        columnDict[weight]
                                                                    ),
                                                            info ]
                                                           )
                else:
                    if weight=="":
                        outputHistoDict[outfilename].append([mainDF.Filter(filterStr)        \
                                                            .Histo1D(   histoModel,
                                                                        columnDict[varToPlot]
                                                                    ),
                                                            info ]
                                                           )
                    else:
                        outputHistoDict[outfilename].append([mainDF.Filter(filterStr)        \
                                                            .Histo1D(   histoModel,
                                                                        columnDict[varToPlot],
                                                                        columnDict[weight]
                                                                    ),
                                                            info ]
                                                           ) 
            if doEven and processName!="data_obs":
                weight_string = "2.0*weight*1.0*VHH_Zll_rwt_TO4b_weight*{}".format(str(processSF))
                cutstring = presel + " && (event%1==0)"
            else:
                weight_string = "weight*1.0*VHH_Zll_rwt_TO4b_weight*{}".format(str(processSF))
                # SF -- Yihui
                if 'SPweight' in subdict.keys() and (processArray[0]=='TT' or processArray[0]=='TTB'):
                    if subdict["SPweight"] !='':
                        print(subdict["SPweight"])
                        weight_string = subdict["SPweight"]
                cutstring = presel
            cutstring += "&& ("+processCut+")"
            #================================= Nominal =================================
            addcolumn(varName)
            print("addcolumn ", varName)
            if doReweight: 
                print("addcolumn for reweight ", subdict["rewvarNames"][0])
                addcolumn(subdict["rewvarNames"][0])
            varname_tmp = ""
            varname_tmp1 = ""
            if var_ind>0:
                varname_tmp="_"+varName
                varname_tmp1=varName
            if doJEROnly:
                print "Skipping nominal because I'm only processing JER Up/Down, doJEROnly==True"
            else:
                if processName == "data_obs":
                    addHisto(cutstring+" && Pass_nominal", "%s"%(processName), "nominal", varName,varname_tmp1)
                    #addHisto(cutstring+" && Pass_nominal", "BDT_%s%s_%s"%(channel,varname_tmp,processName), "nominal", varName,varname_tmp1)
                else:
                    addcolumn(weight_string)
                    if doReweight:
                        addHisto(cutstring+" && Pass_nominal", "%s"%(processName), "nominal", varName,varname_tmp1, weight_string,"",subdict["rewvarNames"][0])
                    else:
                        addHisto(cutstring+" && Pass_nominal", "%s"%(processName), "nominal", varName,varname_tmp1, weight_string)
                    #addHisto(cutstring+" && Pass_nominal", "BDT_%s%s_%s"%(channel,varname_tmp,processName), "nominal", varName,varname_tmp1, weight_string)
            #---------------------------------------------------------------------------
            if args.skipsysts: continue
            #================================= Start systs =================================    
            if channelName == "Zll":
                sampleDict = Zll_sampleDict
            elif channelName == "Wln":
                sampleDict = Wln_sampleDict
            elif channelName == "Znn":
                sampleDict = Znn_sampleDict
    
            if processName == "data_obs":
                elapsed("Created pointer to nominal histogram. Since this is data, there are no systematics to process.",1)
                continue
            systListofList = []
            for x in sampleDict:
                l = len(sampleDict[x])
                if l==4:
                    processList = sampleDict[x][3]
                else:
                    processList = sampleDict[x][4]
                if processName not in processList:
                    continue
                if l==4:
                    systList=[x,sampleDict[x][0],sampleDict[x][1],sampleDict[x][2]]
                else:
                    systList=[x,sampleDict[x][0],sampleDict[x][1],sampleDict[x][2],sampleDict[x][3]]
                systListofList.append(systList)
            systNameList = [i[0] for i in systListofList]
            print("============= systListofList",systListofList)
            elapsed("Created pointer to nominal histogram, next I will plot %i systematics. "%(len(systNameList)),1)
            for isyst, systList in enumerate(systListofList):
                print "\n"
                if "Zee" in channel or "Wen" in channel or "wenu" in channel:
                    systName = systList[0].replace("eff_m","eff_e")
                else:
                    systName = systList[0]
                elapsed("(%i of %i) Processing %s systematic."%(isyst+1,len(systListofList),systName),2)
    
                systWeight = systList[3]
                #systList[3] is the branch stores the syst variation 
                if '.root' in str(systWeight):
                    elapsed("***** ERROR *****: I have not been programmed to load weights from .root files for systematics. Exiting." )
                    # Weights in .root files are not used in VHcc 2016, so I didn't bother to code it... yet. *shrug*
                    sys.exit(1)
                if "Model" in systName:
                    elapsed("***** ERROR *****: I have not been programmed to handle alternative 'Models' in the systematics. Exiting." )
                    # None of the systematics in VHcc 2016 have "Model" in their names
                    sys.exit(1)
    
                bS = ""
                if len(systList) == 5:
                    bS = systList[4]
                varNameUp = varName
                varNameDown = varName
                pSUp = "Pass_nominal"
                pSDown = "Pass_nominal"
                cutstringUp = cutstring
                cutstringDown = cutstring
                weight_stringUp = weight_string
                weight_stringDown = weight_string            
                #FIXME when bS was called branchSuffix, the variable would get unset and I have no clue why
                if bS != "":
                    if not drawFromNom:
#                         if '[' in varName:
                            #bTagWeight_HFUp_pt1_eta0 et al break this convention
                            #btagweight_XUp_... or btagweight_XDown_...
#                             varNameUp = varName.replace('[',"_"+bS+"Up[")
#                             varNameDown = varName.replace('[',"_"+bS+"Down[")
                        if '_13TeV' in varName:
                            varNameUp = varName.replace('_13TeV',"_13TeV_"+bS+"Up")
                            varNameDown = varName.replace('_13TeV',"_13TeV_"+bS+"Down")
                        if '_v2' in varName:
                            varNameUp = varName.replace('_v2',"_v2_"+bS+"Up")
                            varNameDown = varName.replace('_v2',"_v2_"+bS+"Down")
                        if '_v3' in varName:
                            varNameUp = varName.replace('_v3',"_v3_"+bS+"Up")
                            varNameDown = varName.replace('_v3',"_v3_"+bS+"Down")
                        if '_v4' in varName:
                            varNameUp = varName.replace('_v4',"_v4_"+bS+"Up")
                            varNameDown = varName.replace('_v4',"_v4_"+bS+"Down")
#                         elif '[' not in varName and '_13TeV' not in varName:
#                             varNameUp = varName + "_%sUp"%bS
#                             varNameDown = varName + "_%sDown"%bS
                    pSUp = "Pass_%sUp"%bS
                    pSDown = "Pass_%sDown"%bS
    
                    if bS=='unclustEn':
                        for var in ["MET_Phi", "MET_Pt", "controlSample","_v2","_v3","_v4"]:
                            cutstringUp = cutstringUp.replace(var, var+"_%sUp"%bS)
                            cutstringDown = cutstringDown.replace(var, var+"_%sDown"%bS)
                    else:
                        for var in ["controlSample","_v2","_v3","_v4"]:
                            cutstringUp = cutstringUp.replace(var, var+"_%sUp"%bS)
                            cutstringDown = cutstringDown.replace(var, var+"_%sDown"%bS)
    
                    weight_stringUp = weight_string.replace("weight*1.0","weight_%sUp*1.0"%bS)
                    weight_stringDown = weight_string.replace("weight*1.0","weight_%sDown*1.0"%bS)
                else:
                # systWeight is not 1.0
                    # name of syst branches, for example bTagWeight_JES
                    if ',' not in str(systWeight):
                        # up and down branch are not separate
                        if systWeight == "weight_PU":
                            #weight_PU==0 term prevents divide-by-zero resulting in Nans
                            weight_stringUp = "%s*(1./(weight_PU+1*(weight_PU==0)))*(%sUp)"%(weight_stringUp,systWeight)
                            weight_stringDown = "%s*(1./(weight_PU+1*(weight_PU==0)))*(%sDown)"%(weight_stringDown,systWeight)
                        elif systWeight == "VJetsNLOvsLOWeight_p0" or systWeight == "VJetsNLOvsLOWeight_p1":
                            weight_stringUp = "%s*(1./VJetsNLOvsLOWeight)*(%sUp)"%(weight_stringUp,systWeight)
                            weight_stringDown = "%s*(1./VJetsNLOvsLOWeight)*(%sDown)"%(weight_stringDown,systWeight)
                        #check if weight is of form btagweight_ptX_etaY and correct name to btagweightUp_ptX_etaY
                        elif str(systWeight)[-8:-6] == "pt" and str(systWeight)[-4:-1] == "eta":
                            #e.g. systWeight: bTagWeight_JES_pt0_eta0+Up
                            #to bTagWeight_JESUp_pt0_eta0
                            #so if _ptX_etaY in systWeight, remove suffix, add Up, reappend
                            eta_pt_suffix = systWeight[-9:]
                            systWeight_root = systWeight[:-9]
    
                            weight_stringUp = "%s*(%sUp%s)"%(weight_stringUp, systWeight_root,eta_pt_suffix)
                            weight_stringDown = "%s*(%sDown%s)"%(weight_stringDown, systWeight_root,eta_pt_suffix)
    
                        else:
                            weight_stringUp = "%s*(%sUp)"%(weight_stringUp,systWeight)
                            weight_stringDown = "%s*(%sDown)"%(weight_stringDown,systWeight)
    
                    else:
                        # up and down branch may be separate
                        weight_stringUp = "%s*(%s)"%(weight_stringUp,systWeight.split(',')[1])
                        weight_stringDown = "%s*(%s)"%(weight_stringDown,systWeight.split(',')[0])
                # For ZHH NNLO
                if systWeight == 'ZHHNNLO':
                    if 'sampleIndex==-21' in processIdx :
                        addcolumn("LeadGenVBoson_pt")        
                        weight_stringUp=weight_string+'*( ( (%f+%f*LeadGenVBoson_pt+%f*LeadGenVBoson_pt*LeadGenVBoson_pt)/(%f+%f*LeadGenVBoson_pt+%f*LeadGenVBoson_pt*LeadGenVBoson_pt) )*(LeadGenVBoson_pt>=0&&LeadGenVBoson_pt<=500)  + 0.969835*(LeadGenVBoson_pt>500) )'%(1.13151,-0.000566154,7.02718e-07,0.780538,0.0023697,-3.6377e-06)
                        weight_stringDown=weight_string+'*( ( (%f+%f*LeadGenVBoson_pt+%f*LeadGenVBoson_pt*LeadGenVBoson_pt)/(%f+%f*LeadGenVBoson_pt+%f*LeadGenVBoson_pt*LeadGenVBoson_pt) )*(LeadGenVBoson_pt>=0&&LeadGenVBoson_pt<=500) + 1.03208*(LeadGenVBoson_pt>500) )'%(0.452161,0.00503546,-7.52023e-06,0.780538,0.0023697,-3.6377e-06)
                    else:
                        weight_stringUp=weight_stringUp
                        weight_stringDown=weight_stringDown
                # For DY RwT
                if systWeight == 'CMS_DY_RwT':
                    if '(sampleIndex/100)' in processIdx :
                        addcolumn("CMS_vhh_bdt_RwT_DY_2TO4_13TeV")        
                        weight_stringUp=weight_string+'*(exp({0}*CMS_vhh_bdt_RwT_DY_2TO4_13TeV)+{1})/(exp({2}*CMS_vhh_bdt_RwT_DY_2TO4_13TeV)+{1})'.format('1.3217','-0.1335','1.5217')
                        weight_stringDown=weight_string+'*(exp({0}*CMS_vhh_bdt_RwT_DY_2TO4_13TeV)+{1})/(exp({2}*CMS_vhh_bdt_RwT_DY_2TO4_13TeV)+{1})'.format('1.7217','-0.1335','1.5217')
                    else:
                        weight_stringUp=weight_stringUp
                        weight_stringDown=weight_stringDown
                # For TT RwT
                if systWeight == 'CMS_TT_RwT':
                    if 'IsttB==0' in processIdx :
                        addcolumn("CMS_vhh_bdt_RwT_TT_2TO4_13TeV")        
                        weight_stringUp=weight_string+'*(exp({0}*CMS_vhh_bdt_RwT_TT_2TO4_13TeV)+{1})/(exp({2}*CMS_vhh_bdt_RwT_TT_2TO4_13TeV)+{1})'.format('2.0191','0.0056','2.2191')
                        weight_stringDown=weight_string+'*(exp({0}*CMS_vhh_bdt_RwT_TT_2TO4_13TeV)+{1})/(exp({2}*CMS_vhh_bdt_RwT_TT_2TO4_13TeV)+{1})'.format('2.4191','0.0056','2.2191')
                    else:
                        weight_stringUp=weight_stringUp
                        weight_stringDown=weight_stringDown
                # For TTB RwT
                if systWeight == 'CMS_TTB_RwT':
                    if 'IsttB>0' in processIdx :
                        addcolumn("CMS_vhh_bdt_RwT_TTBB_2TO4_13TeV")        
                        weight_stringUp=weight_string+'*(exp({0}*CMS_vhh_bdt_RwT_TTBB_2TO4_13TeV)+{1})/(exp({2}*CMS_vhh_bdt_RwT_TTBB_2TO4_13TeV)+{1})'.format('2.1240','-0.0031','2.3240')
                        weight_stringDown=weight_string+'*(exp({0}*CMS_vhh_bdt_RwT_TTBB_2TO4_13TeV)+{1})/(exp({2}*CMS_vhh_bdt_RwT_TTBB_2TO4_13TeV)+{1})'.format('2.5240','-0.0031','2.3240')
                    else:
                        weight_stringUp=weight_stringUp
                        weight_stringDown=weight_stringDown
                print "branchSuffix " + (bS)
                print "varname " + (varName)
                print "varnameUp " + (varNameUp)
                print "varnameDown " + (varNameDown)
                print "weight_stringUp " + (weight_stringUp)
                print "weight_stringDown " + (weight_stringDown)
                print "systWeight " + (systWeight)
                addcolumn(varNameUp)
                addcolumn(varNameDown)
                addcolumn(weight_stringUp)
                addcolumn(weight_stringDown)
                if doReweight:
                    addHisto(cutstringUp+" && "+pSUp, "%s_%sUp"%(processName,systName), systName+"Up", varNameUp,varname_tmp1, weight_stringUp, systWeight,subdict["rewvarNames"][0])
                    addHisto(cutstringDown+" && "+pSDown, "%s_%sDown"%(processName,systName), systName+"Down", varNameDown,varname_tmp1, weight_stringDown, systWeight,subdict["rewvarNames"][0])
                else:
                    addHisto(cutstringUp+" && "+pSUp, "%s_%sUp"%(processName,systName), systName+"Up", varNameUp,varname_tmp1, weight_stringUp, systWeight)
                    addHisto(cutstringDown+" && "+pSDown, "%s_%sDown"%(processName,systName), systName+"Down", varNameDown,varname_tmp1, weight_stringDown, systWeight)
                #addHisto(cutstringUp+" && "+pSUp, "BDT_%s%s_%s_%sUp"%(channel,varname_tmp,processName,systName), systName+"Up", varNameUp,varname_tmp1, weight_stringUp, systWeight)
                #addHisto(cutstringDown+" && "+pSDown, "BDT_%s%s_%s_%sDown"%(channel,varname_tmp,processName,systName), systName+"Down", varNameDown,varname_tmp1, weight_stringDown, systWeight)
                elapsed("Created pointers to both Up and Down histograms for this systematic.",2)

print
elapsed("==== Now triggering the actual loop over all events. This will take a while. ====")

nEvents = int(mainDF.Count())   # The loop gets triggered while assigning nEvents.
elapsed("Done! I looped over %i events and produced all the histograms."%nEvents)

for outfilename in outputHistoDict:
    ofile = TFile.Open(outfilename,"RECREATE")
    ofile.cd()
    histcount = 0
    for histtuple in outputHistoDict[outfilename]:
        hist = histtuple[0]
        if hist.GetTitle() == "nominal": histNominal = hist
        if hist.Integral() < 0:
            hist.Scale(-0.00001)
        if histtuple[1]=="WJetNLOWeight" and hist.Integral() > 0:
            hist.Scale(histNominal.Integral()/hist.Integral())
            elapsed("Reweighted %s histogram."%(hist.GetName()),1)
        hist.Write()
        histcount += 1
    ofile.Close()
    elapsed("Written %i histograms to %s."%(histcount,outfilename))
elapsed("I produced a total of %i output .root files. And now my watch is ended."%(len(outputHistoDict.keys())))

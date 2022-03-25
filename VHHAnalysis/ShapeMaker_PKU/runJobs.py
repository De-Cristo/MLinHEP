import os, sys, time
from Dictionaries.VHH4b_fileDict import Zll_fileDict, Wln_fileDict, Znn_fileDict
fileDict = dict(Zll_fileDict.items() + Wln_fileDict.items() + Znn_fileDict.items())
from Dictionaries.VHH4b_channelDict import channelDict
from condor_config import *

if "VHH4b_binsDict.py" not in os.listdir("./Dictionaries"):
    print "ERROR: You must run getSRBinning first to get the binnings of SRs."
    sys.exit(1)

if "grouping.txt" in os.listdir("."):
    print "WARNING: Looks like one set of jobs was already submitted from this directory (grouping.txt exists). Submitting another set will overwrite this grouping info and you will not be able to resubmit condor jobs that may have failed in the previous set. It is recommended that you use a separate directory for submitting more jobs or keep a backup of grouping.txt. Proceed only if you are sure all jobs from the last run are complete."
    proceed = raw_input("Proceed? (y/n) ")
    if proceed.lower() != "y": sys.exit()
    
if vptcut=="": vptcutstring = "Inclusive"
else: vptcutstring = vptcut
print "\nUsing the following configuration:\nInput directory: %s\nVpT Cut: %s\n# channels per job: %d\nCompatibility mode for SL6: %s"%(indir,vptcutstring,nChannelsPerJob,str(isSL6))
proceed = raw_input("(These can be changed in condor_config.py.)\n\nProceed? (y/n) ")
if proceed.lower() != "y": sys.exit()

os.system("mkdir -p "+condorDir)

if vptcut=="": runscrText = runscrText.replace("VPTCUT","")
else: runscrText = runscrText.replace("VPTCUT","--vptcut %s"%vptcut)

with open("condor_runscript.sh",'w') as runscr:
    runscr.write(runscrText)
os.system("chmod +x condor_runscript.sh")

if skipString == "": skipString = "sOmErAnDoMiMpOsSiBlEsTrInG"

samplelist = [i for i in os.listdir(indir) if i not in skipList and skipString not in i]
rootlist={}
for samp in samplelist:
    rootlist[samp]=[i for i in os.listdir(indir+'/'+samp) if i not in skipList and skipString not in i]
    #print('samp: ', samp, rootlist[samp])

filegroups = {}
bunchstr = ""
counter=0
for i in sorted(rootlist):
    filegroups[i]=[]
    flen=0
    bunchstr = ""
    counter=0
    fullist=os.listdir(indir+'/'+i)
    for j in fullist:
        flen += 1
        if len(fullist)==1:
           bunchstr+=j
           filegroups[i].append(bunchstr)
           continue
        if flen>=len(fullist):
           bunchstr+=","+j
           filegroups[i].append(bunchstr)
        elif counter >= sizeperbunch:
           filegroups[i].append(bunchstr)
           bunchstr = j
           counter=os.path.getsize(indir+"/"+i+'/'+j)
        else:
           if flen==1:
               bunchstr+=j
           else:
               bunchstr+=","+j
           counter+=os.path.getsize(indir+"/"+i+'/'+j)


with open("grouping.txt",'w') as group:
    for line in filegroups:
        group.write(line+'\n')

jobCount = 0
with open("submit.sub",'w') as subf:
    subf.write(subText)
    for i in filegroups:
        for igroup in filegroups[i]:
            ifile = igroup.split(',')[0]
            sampMatch = [sampname for sampname in fileDict.keys() if sampname in ifile]
            if len(sampMatch) == 0:
                print "\n***** WARNING *****: No sample matches with the input file, %s.\n"%(ifile)
                continue
            else:
                isamp = sorted(sampMatch,key=len)[-1]
            print "isamp: ", isamp    
            nProc = len(fileDict[isamp])
            channelList = []
            if isamp in Zll_fileDict:
                channelList.extend([channel for channel in channelDict if channelDict[channel]["channelName"]=="Zll"])
            if isamp in Wln_fileDict:
                channelList.extend([channel for channel in channelDict if channelDict[channel]["channelName"]=="Wln"])
            if isamp in Znn_fileDict:
                channelList.extend([channel for channel in channelDict if channelDict[channel]["channelName"]=="Znn"])
            nChan = len(channelList)    
            nSections = nProc*nChan
            start = 0
            while start < nSections:
                logText = logFileText.replace("CONDORDIR",condorDir).replace("ROOTFILE",ifile.rstrip(".root")).replace("CHANSTART",str(start))
                subf.write(logText)
                subf.write("arguments = %s %s %s %s %s %s\nqueue\n"%(i, igroup,nChannelsPerJob,start,indir,jobCount))
                start += nChannelsPerJob
                jobCount += 1
    #        if jobCount >= 100: break
print "Produced %i jobs."%jobCount
os.system("condor_submit submit.sub")

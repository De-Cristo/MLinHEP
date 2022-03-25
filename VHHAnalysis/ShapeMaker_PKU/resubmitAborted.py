import os,sys
import linecache
import datetime
from condor_config import *

listdir = os.listdir(".")

if "submit.sub" not in listdir:
    print "Missing submit.sub file. Have condor jobs been submitted yet? Exiting."
    sys.exit(1)

if "resubmitAbortedNew.sub" in listdir:
    print "Previous set of resubmitted aborted jobs detected. Renaming .sub files."
    cmd = "mv -v submit.sub submit_%s.sub" % datetime.datetime.fromtimestamp(os.stat("submit.sub").st_mtime).strftime('%Y%m%d%H%M%S')
    os.system(cmd)
    cmd = "mv -v resubmitAbortedNew.sub submit.sub"
    os.system(cmd)

os.system("grep -Ril aborted %s/*.log &> abortedJobs.log"%condorDir)
subf = open("resubmitAbortedNew.sub",'w')
subf.write(subText)
os.system("mkdir -p %s/oldlog"%condorDir)

af = open("abortedJobs.log",'r')
start = 0
for line in af:    
    line = line.strip()
    os.system("mv %s %s/oldlog"%(line,condorDir))
    line = line.lstrip(condorDir+"/log_").rstrip(".log")
    ifile = line.split('_')[-1]
    NLine = 15 + 6*int(ifile)
    print NLine, ifile
    lineS = linecache.getline("submit.sub", NLine)
    logText = logFileText.replace("CONDORDIR",condorDir)
    subf.write(logText)
    subf.write(lineS)
    subf.write("queue\n")
af.close()
subf.close()
print "Created resubmitAbortedNew.sub"
os.system("condor_submit resubmitAbortedNew.sub")

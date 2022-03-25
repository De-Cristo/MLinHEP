import os,sys
import matplotlib.pyplot as plt

if len(sys.argv)>1:
    condorDir = sys.argv[1]
else:
    condorDir = "condor"

outList = []
for cdir in condorDir.split(','):
    outList += [cdir+"/"+i for i in os.listdir(cdir) if i.endswith(".out") and "Run2016" not in i]
    
nJobs = len(outList)
timelist = []
sizelist = []
neventlist = []
for outFile in sorted(outList):
    f = open(outFile,"r")
    lines = f.readlines()
    argLine = lines[1].strip()
    lastLine = lines[-1].strip()
    eventline = [i for i in lines if "Done! I looped over " in i][0]
    f.close()
    
    idir = argLine.split("inputdir='")[1].split("'")[0]
    ifiles = argLine.split("inputfile='")[1].split("'")[0]
    size = 0
    for fl in ifiles.split(','):
        size += os.path.getsize(idir+"/"+fl)
    nevents = eventline.split("Done! I looped over ")[1].split()[0]
            
    sizelist.append(float(size)/1024**3)    
    time = lastLine.split(" mins;")[0].lstrip("T = ")
    timelist.append(float(time))
    neventlist.append(int(nevents))
    
    if int(nevents) > 900000: print outFile, nevents, time
    
plottext = "%d jobs\n14 channels per job\nMC samples only"%nJobs

plt.hist(timelist,bins=30)
plt.xlabel("Run time (mins)")
plt.ylabel("# Jobs")
plt.title(r"VHcc ShapeMaker on DESY Condor")
plt.text(120, 210, plottext)
plt.savefig("timeHist.png")
plt.cla()
plt.plot(sizelist,timelist,'.')
plt.xlabel("Input file size (GiB)")
plt.ylabel("Run time (mins)")
plt.title(r"VHcc ShapeMaker on DESY Condor")
plt.text(0.5, 150, plottext)
plt.savefig("timevssize.png")
print("Produced timeHist.png and timevssize.png.")
plt.cla()
plt.plot(neventlist,timelist,'.')
plt.xlabel("# events processed")
plt.ylabel("Run time (mins)")
plt.title(r"VHcc ShapeMaker on DESY Condor")
plt.text(40000, 150, plottext)
plt.savefig("timevsnevents.png")
print("Produced timeHist.png, timevssize.png and timevsnevents.png.")
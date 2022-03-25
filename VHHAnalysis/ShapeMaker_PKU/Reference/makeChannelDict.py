import glob, json, sys
#infilelist = glob.glob("runCards_*.sh")
infilelist = sys.argv[1:]

channelDict = {}
for ifile in sorted(infilelist):
    with open(ifile,'r') as f:
        for line in f:
            if not line.startswith('python'): continue
            selname = line.split('-c ')[1].split()[0]
            cutstring = line.split('-p ')[1].split(line.split('-p ')[1][0])[1]
            if 'SR' in ifile: selname = ifile.split("_")[2] + "_" + selname
            xlow = line.split('--xlow ')[1].split()[0]
            xhigh = line.split('--xhigh ')[1].split()[0]
            nBins = line.split('-n ')[1].split()[0]
            varName = line.split('-v ')[1].split(line.split('-v ')[1][0])[1]
            even = "--even" in line
            drawFromNom = " --drawFromNom " in line
            doVV = " --doVV " in line
            doRebin = " -r 1" in line
            #doRebin = "SR" in selname #force SR rebin
            channelName = line.split('--channel ')[1].split()[0].strip("'").strip('"')
            
            channelDict[selname] = {  "cutstring" : cutstring,
                                        "varName"   : varName,
                                        "xlow"      : xlow,
                                        "xhigh"     : xhigh,
                                        "nBins"     : nBins,
                                        "channelName": channelName,
                                        "doEven"    : int(even),
                                        "drawFromNom": int(drawFromNom),
                                        "doVV"      : int(doVV),
                                        "doRebin"   : int(doRebin)
                                     }
                                         
with open('Dictionaries/VHbb_channelDict.py','w') as data:
    data.write("channelDict = ")
    data.write(str(json.dumps(channelDict, indent=4, sort_keys=True)))
    data.write("\n\n")

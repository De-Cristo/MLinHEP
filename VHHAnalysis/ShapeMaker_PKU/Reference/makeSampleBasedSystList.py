import json

def convert(inpname, selname, fileio='a'):
    sampleDict = {}
    with open(inpname,'r') as inp:
        for line in inp:
            if line.strip().startswith('#'): continue
            l = line.split()
            for samp in l[3].split(','):
                if not samp in sampleDict:
                    sampleDict[samp] = []
                sampleDict[samp].append([col for i,col in enumerate(l) if i!=3])

    # for filename in sorted(sampleDict.keys()):
    #     print filename,":"
    #     for array in sampleDict[filename]:
    #         print '\t', array
    #
    # print json.dumps(fileDict, indent=4)
    with open('Dictionaries/VHbb_sampleDict.py',fileio) as data:
        data.write(selname+"_sampleDict = ")
        data.write(str(json.dumps(sampleDict, indent=4, sort_keys=True)))
        data.write("\n\n")
    return sampleDict

Zll_sampleDict = convert("systematics_Zllshapes2017STXS.txt","Zll","w")
Wln_sampleDict = convert("systematics_Wlnshapes2017STXS.txt","Wln","a")
Znn_sampleDict = convert("systematics_Znnshapes2017STXS.txt","Znn","a")

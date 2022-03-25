import sys
#from nano_samples_2017stxs import the_samples_dict as indict
indict = __import__(sys.argv[1]).the_samples_dict
#from sys.argv[1] import the_samples_dict as indict
import json

fileDict = {}
for longname in indict:
    array = indict[longname]
    index = array[0]
    scale = array[1]
    name = array[2]
    filenamelist = array[3]
    for filename in filenamelist:
        if not filename in fileDict:
            fileDict[filename] = []
        fileDict[filename].append([ name, index, scale, longname ])

# for filename in sorted(fileDict.keys()):
#     print filename,":"
#     for array in fileDict[filename]:
#         print '\t', array

# print json.dumps(fileDict, indent=4)
#if __name__=="__main__":
with open('Dictionaries/VHbb_fileDict.py','w') as data:
    data.write("fileDict = ")
    data.write(str(json.dumps(fileDict, indent=4, sort_keys=True)))

##Crosscheck
#from VHbb_fileDict import fileDict as newdict
#print "Checks passed:", fileDict == newdict

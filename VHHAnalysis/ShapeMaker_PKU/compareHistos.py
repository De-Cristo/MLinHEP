import os,sys
from ROOT import *

path1 = "/afs/cern.ch/user/l/lmastrol/public/after_PreApproval/VHcc_forUnblinding_v1"
path1 = "/nfs/dust/cms/user/andreypz/hcc/VZ_shapes_2019_04_17_VPT_incl"
#path1 = "/afs/desy.de/user/s/spmondal/private/vhcc/CMSSW_10_2_0_pre6/src/AnalysisTools/StatTools/ShapeMaker/190424/haddlevel2"
path2 = "/afs/desy.de/user/s/spmondal/private/vhcc/CMSSW_10_2_0_pre6/src/AnalysisTools/StatTools/ShapeMaker/190425_novptcut/haddlevel1"

rlist1 = sorted([i for i in os.listdir(path1) if i.endswith('.root')])
rlist2 = sorted([i for i in os.listdir(path2) if i.endswith('.root')])

#if set(rlist1) != set(rlist2):
#    print "List of files not matched."
#    sys.exit(1)

samelist = []
difflist = []    
for r1 in rlist1:
    print "Processing",r1
    f1 = TFile.Open(path1+'/'+r1,'READ')
    f2 = TFile.Open(path2+'/'+r1.replace('_SR_','_VZ_SR_').replace('_ISYS',''),'READ')
    
    hlist1 = sorted([i.GetName() for i in list(f1.GetListOfKeys())])
    hlist2 = sorted([i.GetName() for i in list(f2.GetListOfKeys())])
    
#    for i in range(len(hlist1)):
#        print hlist1[i], hlist2[i]
    
    for h in hlist1:
        if h.endswith('Up') or h.endswith('Down'): continue
        h2 = h.replace('BDT_SR','BDT_VZ_SR')
        if "Wmunu" in h2 or "Zmm" in h2: h2 = h2.replace('eff_e','eff_m')
        #if 'data_obs' in h: continue
        if h2 not in hlist2:
            print h,"not in second file."
            continue
#        if 'VVother' in h: continue
        histo1 = f1.Get(h)
        histo2 = f2.Get(h2)
        E1 = histo1.GetEntries()
        E2 = histo2.GetEntries()
        I1 = histo1.Integral()
        I2 = histo2.Integral()
        if I1 == 0: comp = I1 == I2
        else: comp = (I1 - I2)/I1 < 0.005
        if E1 == 0: comp2 = E1==E2
        else: comp2 = (E1-E2)/E1 < 0.005
        if comp2 and  comp: 
           # print h, E1, E2, histo1.Integral(), histo2.Integral()
            samelist.append([h,E1,E2,I1,I2])
        else:
            difflist.append([h,E1,E2,I1,I2])
def diff(elem):
    return abs(elem[3]-elem[4])/elem[3]
print "Same: %d, Diff %d"%(len(samelist),len(difflist))
for i in sorted(difflist,key=diff): 
    if 'VVother' in i[0]: continue
    print i

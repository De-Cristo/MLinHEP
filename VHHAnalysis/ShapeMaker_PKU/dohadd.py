import os, sys, argparse
import multiprocessing as mp
parser = argparse.ArgumentParser("hadd shape files")
parser.add_argument('-y', '--year', type=str, default="", help="2016, 2017 or 2018")
args = parser.parse_args()
print args
if "2016" not in args.year and "2017" not in args.year and "2018" not in args.year:
    print "\n****** ERROR *****: Year %s is not supported\n"%(args.year)
    sys.exit(1)
year = args.year
histfiles = [i for i in os.listdir('.') if i.startswith("hists_"+year) and i.endswith(".root")]

iy=3
if year=="2016":iy=0
elif year=="2017":iy=1
elif year=="2018":iy=2

MET = ["Run2016BToGMETReMiniAOD","Run2017METMiniAOD","Run2018MET"]
Mu = ["Run2016BToGMuReMiniAOD","Run2017MuReMiniAOD","Run2018Mu"]
Ele = ["Run2016BToGEleReMiniAOD","Run2017EleReMiniAOD","Run2018Ele"]
DoubleEle = ["Run2016BToGDoubleEleReMiniAOD","Run2017DoubleEleReMiniAOD","Run2018DoubleEle"]
DoubleMu = ["Run2016BToGDoubleMuReMiniAOD","Run2017DoubleMuReMiniAOD","Run2018DoubleMu"]

os.system("mkdir -p haddlevel1")
done = []
hadds = []
for fl in histfiles:
    outname = '_'.join(fl.rstrip('.root').split('_')[:-2])
    #hack escape characters where needed
    safe_outname = []
    for char in outname:
        if char == "=" or char == "&" or char == ")" or char == "(":
            safe_outname.append("\\" + char)
        else:
            safe_outname.append(char)
    outname = "".join(safe_outname)

    positions = [pos for pos, char in enumerate(outname) if char == "="]

    if outname in done: continue
    if 'data_obs' in fl:
        if '_Znn_' in fl: 
            suff = MET[iy]
            cmd = 'hadd haddlevel1/%s.root %s_*%s*.root %s_*%s*.root %s_*%s*.root'%(outname,outname,MET[iy],outname,Ele[iy],outname,Mu[iy])
        else:
            if '_Zee_' in fl: suff = DoubleEle[iy]
            elif '_Zmm_' in fl: suff = DoubleMu[iy]
            elif '_Wenu_' in fl: suff = Ele[iy]
            elif '_Wmunu_' in fl: suff = Mu[iy]
            else:
                print "%s: Matching dataset not found."%(fl)
                sys.exit(1)
            cmd = "hadd haddlevel1/%s.root %s_*%s*.root"%(outname,outname,suff)
    else:
        cmd = "hadd haddlevel1/%s.root %s_*.root"%(outname,outname)
    hadds.append(cmd)
    done.append(outname)

if __name__ == '__main__':
    nProc = mp.cpu_count()
    pool = mp.Pool(processes=nProc)
    pool.imap_unordered(os.system, hadds)
    pool.close()
    pool.join()

os.system("mkdir -p haddlevel3")
os.system("hadd haddlevel3/vhh_Zee-"+year+".root haddlevel1/*"+year+"*_Zee_*.root")
os.system("hadd haddlevel3/vhh_Zmm-"+year+".root haddlevel1/*"+year+"*_Zmm_*.root")
os.system("hadd haddlevel3/vhh_Wenu-"+year+".root haddlevel1/*"+year+"*_Wenu_*.root")
os.system("hadd haddlevel3/vhh_Wmunu-"+year+".root haddlevel1/*"+year+"*_Wmunu_*.root")
os.system("hadd haddlevel3/vhh_Znn-"+year+".root haddlevel1/*"+year+"*_Znn_*.root")

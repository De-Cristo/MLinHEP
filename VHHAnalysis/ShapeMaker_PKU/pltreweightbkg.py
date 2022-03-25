import ROOT as R

def plot_BDTreweight(VHHfiles, procs):
    legname=['Pass','Fail','weight']
    for ifile in VHHfiles:
        hsample = {}
        fin = R.TFile.Open('{0}'.format(ifile),'READ')
        #Get all plots
        MAX_ = 0
        MaxX_ = 0
        MinX_ = 0
        NX_ = 0
        Min_ = 0
        print('procs contains ',procs)
        for iprocs in procs:
            fin.cd()
            htmp = fin.Get(iprocs).Clone()
            NX_=htmp.GetNbinsX()
            htmp.Scale(1.0/htmp.Integral())
            MinX_=htmp.GetBinCenter(1) - htmp.GetBinWidth(1)/2.0
            MaxX_=htmp.GetBinCenter(NX_) + htmp.GetBinWidth(NX_)/2.0
            MAX_ = htmp.GetMaximum() if htmp.GetMaximum() > MAX_ else MAX_
            Min_ = htmp.GetMinimum() if htmp.GetMinimum() < Min_ else Min_
            hsample[iprocs] = R.TH1F(iprocs,iprocs,NX_,1,1+NX_)
            for i in range(1,NX_+1):
                hsample[iprocs].SetBinContent(i,htmp.GetBinContent(i))
                hsample[iprocs].SetBinError(i,htmp.GetBinError(i))
        if MinX_<=0: MinX_=0.001
        print(NX_,MinX_,MaxX_)
        c=R.TCanvas()
        #c.SetLogy()
        c.SetFillColor(0)
        c.SetBorderMode(0)
        c.SetBorderSize(2)
        c.SetFrameBorderMode(0)
        histframe = R.TH1D("histframe","",NX_,1,1+NX_)
        histframe.GetXaxis().SetTitle("transformed BDT variable")
        histframe.GetXaxis().SetTitleSize(0.05)
        histframe.GetXaxis().SetTitleOffset(0.8)
        histframe.GetXaxis().SetTitleFont(42)
        histframe.GetYaxis().SetTitle("")
        histframe.GetYaxis().SetLabelFont(42)
        histframe.GetYaxis().SetLabelSize(0.05)
        histframe.GetYaxis().SetTitleSize(0.05)
        histframe.GetYaxis().SetTitleFont(42)
        histframe.GetYaxis().SetRangeUser(Min_*0.7,MAX_*1.3)
        histframe.Draw("AXISSAME")
        R.gStyle.SetOptStat(0)
        #c.SetLogy()
        leg = R.TLegend(0.3,0.6,0.45,0.8)
        leg.SetBorderSize(0)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        i=0
        for iprocs in procs:
            print(iprocs)
            hsample[iprocs].SetLineColor(i+2)
            hsample[iprocs].SetLineWidth(2)
            hsample[iprocs].SetMarkerColor(i+2)
            hsample[iprocs].Draw("same e")
            entry=leg.AddEntry(iprocs,legname[i] ,"lp")
            entry.SetFillStyle(1001)
            entry.SetMarkerStyle(8)
            entry.SetMarkerSize(1.5)
            entry.SetLineStyle(1)
            entry.SetLineWidth(3)
            entry.SetTextFont(42)
            entry.SetTextSize(0.06)
            i+=1
        hsample['histsweight'].Fit("pol1")
        f1 = hsample['histsweight'].GetFunction("pol1")
        f1.SetLineColor(R.kBlue)
        f1.Draw("same")
        #f1_up= R.TF1("f1_up","[0] + [1]*x",0,100);
        #f1_dn= R.TF1("f1_dn","[0] + [1]*x",0,100);
        #f1_up.SetParameters(f1.GetParameter(0)+f1.GetParError(0),f1.GetParameter(1)+f1.GetParError(1))
        #f1_dn.SetParameters(f1.GetParameter(0)-f1.GetParError(0),f1.GetParameter(1)-f1.GetParError(1))
        #f1_up.SetLineColor(R.kOrange)
        #f1_dn.SetLineColor(R.kOrange)
        #f1_up.SetLineStyle(9)
        #f1_dn.SetLineStyle(9)
        #f1_up.Draw("same")
        #f1_dn.Draw("same")
        f2_up= R.TF1("f2_up","[0] + [1]*(x-1)",0,100);
        f2_dn= R.TF1("f2_dn","[0] + [1]*(x+1)",0,100);
        f2_up.SetParameters(f1.GetParameter(0),f1.GetParameter(1))
        f2_dn.SetParameters(f1.GetParameter(0),f1.GetParameter(1))
        f2_up.SetLineColor(R.kOrange)
        f2_dn.SetLineColor(R.kOrange)
        f2_up.SetLineStyle(9)
        f2_dn.SetLineStyle(9)
        f2_up.Draw("same")
        f2_dn.Draw("same")
        leg.Draw()
        tex = R.TLatex(0.14,0.95,"CMS")
        tex.SetNDC()
        tex.SetTextAlign(13)
        tex.SetTextSize(0.048)
        tex.SetLineWidth(2)
        tex.Draw()
        tex1 = R.TLatex(0.22,0.95,"Simulation Work in Progress")
        tex1.SetNDC()
        tex1.SetTextAlign(13)
        tex1.SetTextFont(52)
        tex1.SetTextSize(0.03648)
        tex1.SetLineWidth(2)
        tex1.Draw()
        #c.SaveAs("test.png")
        input("exit...")

from Dictionaries.VHH4b_reweightDict import reweightDict,reweightValueDict,reweightErrorDict
from Dictionaries.VHH4b_channelDict import channelDict
reweightError1Dict={}
reweightError2Dict={}
procs = ['TT','TTB']
for key in channelDict:
    if "doReweight" in channelDict[key].keys():
        if channelDict[key]["doReweight"]==1:
            reweightError1Dict[key]={}
            reweightError2Dict[key]={}
            NX_ = 0
            for iprocs in procs:
                reweightError1Dict[key][iprocs]={}
                reweightError2Dict[key][iprocs]={}
                c=R.TCanvas()
                #c.SetLogy()
                c.SetFillColor(0)
                c.SetBorderMode(0)
                c.SetBorderSize(2)
                c.SetFrameBorderMode(0)
                R.gStyle.SetOptStat(0)
                print(key,iprocs,reweightValueDict[key][iprocs])
                NX_=len(reweightValueDict[key][iprocs])
                hsample = R.TH1F(iprocs,"",NX_,1,1+NX_)
                for i in range(1,1+NX_):
                    hsample.SetBinContent(i,reweightValueDict[key][iprocs][i-1])
                    hsample.SetBinError(i,reweightErrorDict[key][iprocs][i-1])      
                hsample.SetLineColor(R.kBlue)
                hsample.Draw("e")
                hsample.GetXaxis().SetTitle("transformed BDT variable")
                hsample.GetXaxis().SetTitleSize(0.05)
                hsample.GetXaxis().SetTitleOffset(0.8)
                hsample.GetXaxis().SetTitleFont(42)
                hsample.GetYaxis().SetTitle("")
                hsample.GetYaxis().SetLabelFont(42)
                hsample.GetYaxis().SetLabelSize(0.05)
                hsample.GetYaxis().SetTitleSize(0.05)
                hsample.GetYaxis().SetTitleFont(42)
                hsample.Fit("pol1")
                f1 = hsample.GetFunction("pol1")
                f1.SetLineColor(R.kBlue)
                f1.Draw("same")
                f1_up= R.TF1("f1_up","[0] + [1]*x",0,100);
                f1_dn= R.TF1("f1_dn","[0] + [1]*x",0,100);
                f1_up.SetParameters(f1.GetParameter(0)+f1.GetParError(0),f1.GetParameter(1)+f1.GetParError(1))
                f1_dn.SetParameters(f1.GetParameter(0)-f1.GetParError(0),f1.GetParameter(1)-f1.GetParError(1))
                reweightError1Dict[key][iprocs]['Up']=[]
                reweightError2Dict[key][iprocs]['Up']=[]
                reweightError1Dict[key][iprocs]['Down']=[]
                reweightError2Dict[key][iprocs]['Down']=[]
                for i in range(1,1+NX_):
                    reweightValueDict[key][iprocs][i-1] = (f1.Eval(hsample.GetBinCenter(i)))
                    #reweightErrorDict[key][iprocs][i-1] = ( abs(f1_up.Eval(hsample.GetBinCenter(i))-f1.Eval(hsample.GetBinCenter(i))) + abs(f1_dn.Eval(hsample.GetBinCenter(i))-f1.Eval(hsample.GetBinCenter(i))) )/2.0
                    reweightError1Dict[key][iprocs]['Up'].append(  f1_up.Eval(hsample.GetBinCenter(i))) if f1_up.Eval(hsample.GetBinCenter(i))>=0 else reweightError1Dict[key][iprocs]['Up'].append(0)
                    reweightError1Dict[key][iprocs]['Down'].append( f1_dn.Eval(hsample.GetBinCenter(i))) if f1_dn.Eval(hsample.GetBinCenter(i))>=0 else reweightError1Dict[key][iprocs]['Down'].append(0)
                print(' para =====> ', reweightValueDict[key][iprocs])
                print('err para ====> ', reweightErrorDict[key][iprocs])
                f1_up.SetLineColor(R.kOrange)
                f1_dn.SetLineColor(R.kOrange)
                f1_up.SetLineStyle(9)
                f1_dn.SetLineStyle(9)
                f1_up.Draw("same")
                f1_dn.Draw("same")
                f2_up= R.TF1("f2_up","[0] + [1]*(x-5)",0,100);
                f2_dn= R.TF1("f2_dn","[0] + [1]*(x+5)",0,100);
                f2_up.SetParameters(f1.GetParameter(0),f1.GetParameter(1))
                f2_dn.SetParameters(f1.GetParameter(0),f1.GetParameter(1))
                for i in range(1,1+NX_):
                    reweightError2Dict[key][iprocs]['Up'].append(  f2_up.Eval(hsample.GetBinCenter(i))) if f2_up.Eval(hsample.GetBinCenter(i))>=0 else reweightError2Dict[key][iprocs]['Up'].append(0)
                    reweightError2Dict[key][iprocs]['Down'].append( f2_dn.Eval(hsample.GetBinCenter(i))) if f2_dn.Eval(hsample.GetBinCenter(i))>=0 else reweightError2Dict[key][iprocs]['Down'].append(0)
                f2_up.SetLineColor(R.kRed)
                f2_dn.SetLineColor(R.kRed)
                f2_up.SetLineStyle(9)
                f2_dn.SetLineStyle(9)
                f2_up.Draw("same")
                f2_dn.Draw("same")
                tex = R.TLatex(0.14,0.95,"CMS")
                tex.SetNDC()
                tex.SetTextAlign(13)
                tex.SetTextSize(0.048)
                tex.SetLineWidth(2)
                tex.Draw()
                tex1 = R.TLatex(0.22,0.95,"Simulation Work in Progress")
                tex1.SetNDC()
                tex1.SetTextAlign(13)
                tex1.SetTextFont(52)
                tex1.SetTextSize(0.03648)
                tex1.SetLineWidth(2)
                tex1.Draw()
                c.SaveAs('gr_rwpra_'+key+iprocs+".png")
                c.SaveAs('gr_rwpra_'+key+iprocs+".C")
                #input()
     
#plot_BDTreweight(['wenuBBDT_v_svb_HMP_TT_weight.root'], ['histspass','histsfail','histsweight'])
#exit()

outputFile = open("Dictionaries/VHH4b_reweightDict_para_shift5.py","w")
content = "reweightDict = "
content += str(reweightDict).replace('],','],\n')+'\n'
content += "reweightValueDict = "
content += str(reweightValueDict).replace('],','],\n')+'\n'
content += "reweightError1Dict = "
content += str(reweightError1Dict).replace('],','],\n')+'\n'
content += "reweightError2Dict = "
content += str(reweightError2Dict).replace('],','],\n')+'\n'
outputFile.write(content)
outputFile.close()


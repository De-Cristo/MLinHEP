import ROOT as R
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool
import sys
import array
# import warnings
import matplotlib.pyplot as plt
from ctypes import *

dict_th1    = dict()
dict_canv   = dict()
dict_leg    = dict()

rdf_dict = {}
np_rdf_dict = {}
pd_rdf_dict = {}
variables = {}

canvas_list = ['VHH_HH_m', 'VHH_HH_pT', 'VHH_HH_eta', 'VHH_HH_phi', 'VHH_HH_e',\
               'VHH_H1_m', 'VHH_H1_pT', 'VHH_H1_eta', 'VHH_H1_phi', 'VHH_H1_e',\
               'VHH_H2_m', 'VHH_H2_pT', 'VHH_H2_eta', 'VHH_H2_phi', 'VHH_H2_e',\
               'VHH_HH_dR','VHH_HH_deta','VHH_HH_dphi','VHH_rHH', 'VHH_nBJets']

sample_compare_list = ['VHH_HH_m', 'VHH_HH_pT', 'VHH_HH_eta', 'VHH_HH_phi', 'VHH_HH_e',\
                       'VHH_H1_m', 'VHH_H1_pT', 'VHH_H1_eta', 'VHH_H1_phi', 'VHH_H1_e',\
                       'VHH_H2_m', 'VHH_H2_pT', 'VHH_H2_eta', 'VHH_H2_phi', 'VHH_H2_e',\
                       'VHH_HH_dR','VHH_HH_deta','VHH_HH_dphi','VHH_rHH', 'VHH_nBJets']

def th1_gev     ( name, title, xmin, xmax ):
    dict_th1[name] = R.TH1F( name, title, int((xmax-xmin)/10), xmin, xmax )
#end

def th1         ( name, title, nbin, xmin, xmax ):
    dict_th1[name] = R.TH1F( name, title, nbin, xmin, xmax )
#end

def canv        ( name, Lep_Num , lep_cha ):
    dict_canv[name] = R.TCanvas()
    dict_canv[name] . SetLogy()
    
    dict_th1[name+str(2)].SetLineColor(R.kViolet)
    dict_th1[name+str(3)].SetLineColor(R.kBlue)
    dict_th1[name+str(4)].SetLineColor(R.kRed)
    dict_th1[name + lep_cha].SetLineColor(R.kGreen)

    dict_th1[name+str(2)].SetLineWidth(2)
    dict_th1[name+str(3)].SetLineWidth(2)
    dict_th1[name+str(4)].SetLineWidth(2)
    dict_th1[name + lep_cha].SetLineWidth(2)
    
    dict_th1[name+str(2)].Sumw2()
    dict_th1[name+str(3)].Sumw2()
    dict_th1[name+str(4)].Sumw2()
    
    dict_th1[name+str(2)].DrawNormalized()
    dict_th1[name+str(3)].DrawNormalized('same')
    dict_th1[name + lep_cha].DrawNormalized('same')
    dict_th1[name+str(4)].DrawNormalized('same')
    
    dict_leg[name] = R.TLegend(0.75,0.85,0.95,0.95)
    dict_leg[name].AddEntry(dict_th1[name+'2'],'Bjets tagged 2')
    dict_leg[name].AddEntry(dict_th1[name+'3'],'Bjets tagged 3')
    dict_leg[name].AddEntry(dict_th1[name+'4'],'Bjets tagged 4')
    dict_leg[name].AddEntry(dict_th1[name + lep_cha], lep_cha + ' MC Signal')

    dict_leg[name].Draw('same')
    
    dict_canv[name].SaveAs(name+ Lep_Num +'.pdf')
#end

def canv_sample_compare        ( name, lep_cha_1 , lep_cha_2 ):
    dict_canv[name] = R.TCanvas()
    dict_canv[name] . SetLogy()

    dict_th1[name + lep_cha_1].SetLineColor(R.kBlue)
    dict_th1[name + lep_cha_2].SetLineColor(R.kRed)

    dict_th1[name + lep_cha_1].SetLineWidth(2)
    dict_th1[name + lep_cha_2].SetLineWidth(2)

    dict_th1[name + lep_cha_1].DrawNormalized()
    dict_th1[name + lep_cha_2].DrawNormalized('same')
    
    dict_leg[name] = R.TLegend(0.75,0.85,0.95,0.95)
    dict_leg[name].AddEntry(dict_th1[name + lep_cha_1], lep_cha_1 + ' MC Signal')
    dict_leg[name].AddEntry(dict_th1[name + lep_cha_2], lep_cha_2 + ' MC Signal')
    dict_leg[name].Draw('same')
    
    dict_canv[name].SaveAs(name + lep_cha_1 + 'VS' + lep_cha_2 +'.pdf')
#end

def convert_coupling_diagramweight_VBF_VHH(coupling_nx3):
    nrow=len(coupling_nx3[:,0])
    cv = coupling_nx3[:,0].reshape(nrow,1)
    c2v = coupling_nx3[:,1].reshape(nrow,1)
    kl = coupling_nx3[:,2].reshape(nrow,1)
    weights = np.matrix(np.zeros(nrow*6).reshape((nrow,6)),dtype=np.float64)
    weights[:,0] = np.power(np.multiply(cv,kl),2)
    weights[:,1] = np.power(cv,4)
    weights[:,2] = np.power(c2v,2)
    weights[:,3] = np.multiply(np.power(cv,3),kl)
    weights[:,4] = np.multiply(np.multiply(cv,c2v),kl)
    weights[:,5] = np.multiply(np.power(cv,2),c2v)
    return weights

def convert_coupling_diagramweight_GGF(coupling_nx2):
    nrow=len(coupling_nx2[:,0])
    kt = coupling_nx2[:,0].reshape(nrow,1)
    kl = coupling_nx2[:,1].reshape(nrow,1)
    weights = np.matrix(np.zeros(nrow*3).reshape((nrow,3)),dtype=np.float64)
    weights[:,0] = np.power(kt,4)
    weights[:,1] = np.power(np.multiply(kt,kl),2)
    weights[:,2] = np.multiply(np.power(kt,3),kl)
    return weights

def Save_Temp_Components(tree_in, bak_file, weight):
    print("weighting the trees..." + str(weight))
    tree_in.SetBranchStatus('*', 1);
    tout1 = tree_in.CloneTree()
    tout1.SetWeight(weight)
    tout1.Write()
    del tout1
#END

def NormHisto(histo_name, norm):
    scale = 1/histo_name.Integral()
    histo_name.Scale(scale)

def DF_HISTO1D(_rdf, _jet_filter, _other_filters, _name, _describe, _nbins, _xmin, _xmax, _branch_name, _Xtitle, _Batch):
    
    _histo_name = _rdf.Filter(_jet_filter+' && '+_other_filters).Histo1D((_name, _describe, _nbins, _xmin, _xmax), _branch_name)
    
    _histo_with2bjets = _rdf.Filter('VHH_nBJets == 2 && '+ _other_filters).Histo1D((_name+'2b', _describe+'2b', _nbins, _xmin, _xmax), _branch_name)
    
    _histo_weight = R.TH1D(_name+'_weight', _describe+'_weight', _nbins, _xmin, _xmax)
    
    inclusiveBinningP = np.array([0, 200, 350, 1000],dtype = float) #FIXME
    _nbins = len(inclusiveBinningP)
    
    _histo_name = _histo_name.Rebin(_nbins,_name,inclusiveBinningP)
    _histo_with2bjets = _histo_with2bjets.Rebin(_nbins, _name, inclusiveBinningP)
    _histo_weight = _histo_weight.Rebin(_nbins, _name+'_weight', inclusiveBinningP)

    NormHisto(_histo_name,1)
    NormHisto(_histo_with2bjets,1)
    
    for i in range(0, _nbins):
        if _histo_name.GetBinContent(i)!= 0:
            _histo_weight.SetBinContent(i,_histo_with2bjets.GetBinContent(i)/float(_histo_name.GetBinContent(i)))
        else:
            _histo_weight.SetBinContent(i,0)
    if _Batch :
        _canvas_histo_name = R.TCanvas()
    #     R.gstyle.SetLogy()
    #     R.gStyle.SetOptStat(0000)

        upper_pad = R.TPad("upper_pad", "", 0, 0.35, 1, 1)
        lower_pad = R.TPad("lower_pad", "", 0, 0, 1, 0.35)
        for p in [upper_pad, lower_pad]:
            p.SetLeftMargin(0.14)
            p.SetRightMargin(0.05)
            p.SetTickx(False)
            p.SetTicky(False)
        upper_pad.SetBottomMargin(0)
        lower_pad.SetTopMargin(0)
        lower_pad.SetBottomMargin(0.3)

        upper_pad.Draw()
        lower_pad.Draw()
        upper_pad.cd()
    #     dict_th1[_histo_name].SetStats(0)
    #     dict_th1[_histo_name+'_2b'].SetStats(0)

        _histo_with2bjets.GetXaxis().SetTitle(_Xtitle)
        _histo_with2bjets.GetYaxis().SetTitle('Yields')

        _histo_name.SetMarkerStyle(20)
        _histo_name.SetMarkerSize(1)

        _histo_with2bjets.SetFillColor(R.kBlue-5)
        _histo_with2bjets.SetLineColor(R.kBlue-5)

        _histo_with2bjets.Draw()
        _histo_name.Draw('SAME')
        lower_pad.cd()
        _histo_weight.SetStats(0)
        _histo_weight.Draw()

    #     dict_legend[_histo_name] = R.TLegend(0.7,0.8,0.9,0.9)
    #     dict_legend[_histo_name].AddEntry(dict_th1[_histo_name])
    #     dict_legend[_histo_name].AddEntry(dict_th1[_histo_name+'_2b'], "bkg")
    #     dict_legend[_histo_name].Draw('SAME')

        _canvas_histo_name.SaveAs(str(_histo_name)+'.pdf')
    else:
        print('No Figures can be saved in batch mode.')
    
    return _histo_weight
#END

class variable:
    def __init__(self, name, title, binning=None):
        if binning is not None and (not isinstance(binning, list) or len(binning)!=3):
            raise Exception("Error in declaration of variable {0}. Binning must be a list like [nbins, min, max]".format(name))
        self.title = title
        self.binning = binning
        variables[name] = self #add yourself to dictionary

    def get_nbins(self):
        if self.binning is not None:
            return self.binning[0]
        else: return 50

    def get_xmin(self):
        if self.binning is not None:
            return self.binning[1]
        else: return 0

    def get_xmax(self):
        if self.binning is not None:
            return self.binning[2]
        else: return 0
        
def plot_vars_as_ROOT_ML(sig_key,bkg_key,var_key,var_items,plot_path):
    #RDataFrame
    model_sig = R.RDF.TH1DModel(var_key+sig_key, var_items.title, var_items.get_nbins(), var_items.get_xmin(), var_items.get_xmax())
    model_bkg = R.RDF.TH1DModel(var_key+bkg_key, var_items.title, var_items.get_nbins(), var_items.get_xmin(), var_items.get_xmax())
    c_temp = R.TCanvas() #auto canvas 
    #TODO : weight
    _histo_sig = rdf_dict[sig_key].Histo1D(model_sig, var_key, 'weight')
    _histo_bkg = rdf_dict[bkg_key].Histo1D(model_bkg, var_key, 'new_weight_for_signal')
    
    _histo_sig.SetFillColorAlpha(900, 0.5)
    _histo_bkg.SetFillColorAlpha(860, 0.5)
    _histo_sig.SetLineColorAlpha(616, 0.7)
    _histo_bkg.SetLineColorAlpha(840, 0.7)
    
    NormHisto(_histo_sig,1)
    NormHisto(_histo_bkg,1)
    
    print('Plotting {0}.pdf & {0}.png'.format(var_key))
    
    _binheight = 0
    for _bin in range(var_items.get_nbins()):
        _binheight = max(_binheight,_histo_sig.GetBinContent(_bin),_histo_bkg.GetBinContent(_bin))

    _histo_zoom = R.TH2F(var_key, var_items.title, var_items.get_nbins(), var_items.get_xmin(), var_items.get_xmax(),10,0.,_binheight*1.1)
    _histo_zoom.SetStats(R.kFALSE)
    _histo_zoom.Draw()
    _histo_sig.Draw('histoSAME')
    _histo_bkg.Draw('histoSAME')
    
    _legend = R.TLegend(0.15,0.7,0.35,0.85)
    _legend.AddEntry(var_key+sig_key,sig_key,'f')
    _legend.AddEntry(var_key+bkg_key,bkg_key,'f')
    _legend.SetLineColor(0)
    _legend.SetFillColorAlpha(0,0.5)
    _legend.Draw('SAME')
    
    c_temp.SaveAs('{0}/{1}.pdf'.format(plot_path,var_key))
    c_temp.SaveAs('{0}/{1}.png'.format(plot_path,var_key))
    
    del c_temp
    del model_sig, model_bkg
    
def correlations(data, extra_str, **kwds):
    """Calculate pairwise correlation between features.
    
    Extra arguments are passed on to DataFrame.corr()
    """
    # simply call df.corr() to get a table of
    # correlation values if you do not need
    # the fancy plotting
    corrmat = data.corr(**kwds)

    fig, ax1 = plt.subplots(ncols=1, figsize=(6,5))
    
    opts = {'cmap': plt.get_cmap("RdBu"),
            'vmin': -1, 'vmax': +1}
    heatmap1 = ax1.pcolor(corrmat, **opts)
    plt.colorbar(heatmap1, ax=ax1)

    ax1.set_title("Correlations_"+extra_str)

    labels = corrmat.columns.values
    for ax in (ax1,):
        # shift location of ticks to center of the bins
        ax.set_xticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_yticks(np.arange(len(labels))+0.5, minor=False)
        ax.set_xticklabels(labels, minor=False, ha='right', rotation=70)
        ax.set_yticklabels(labels, minor=False)
        
    plt.tight_layout()
    save_plot_batch(extra_str+'corr.png')
    
def save_plot_batch( plot_str ):
    plt.savefig(plot_str)
    plt.show()
    plt.close()
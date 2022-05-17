#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import ROOT as R
import glob
import numpy as np
import os
import sys
import argparse

def AddCommonSystematics(cb,year):

    signal = cb.cp().signals().process_set()
    backgrounds  = cb.cp().backgrounds().process_set()
    # Theory uncertainties: signal
    cb.cp().process(signal).AddSyst(cb, 'BR_hbb', 'lnN', ch.SystMap()((0.9747, 1.0248)))
    cb.cp().process(signal).AddSyst(cb, 'pdf_Higgs_VHH', 'lnN', ch.SystMap()(1.028))
    cb.cp().process(signal).AddSyst(cb, 'QCDscale_VHH', 'lnN', ch.SystMap()((0.973, 1.034)) )

    TT_prefit=1.0
    TTB_prefit=1.0
    cb.cp().channel(['Wen']).process(["TT"]).AddSyst(cb, "CMS_TT_norm"+str(year), "rateParam", ch.SystMap()(TT_prefit));
    cb.cp().channel(['Wen']).process(["TTB"]).AddSyst(cb, "CMS_TTB_norm"+str(year), "rateParam", ch.SystMap()(TTB_prefit));
    cb.cp().channel(['Wmn']).process(["TT"]).AddSyst(cb, "CMS_TT_norm"+str(year), "rateParam", ch.SystMap()(TT_prefit));
    cb.cp().channel(['Wmn']).process(["TTB"]).AddSyst(cb, "CMS_TTB_norm"+str(year), "rateParam", ch.SystMap()(TTB_prefit));
    cb.cp().channel(['Znn']).process(["TT"]).AddSyst(cb, "CMS_TT_norm"+str(year), "rateParam", ch.SystMap()(TT_prefit));
    cb.cp().channel(['Znn']).process(["TTB"]).AddSyst(cb, "CMS_TTB_norm"+str(year), "rateParam", ch.SystMap()(TTB_prefit));

    ##Experimental uncertainties
    ##https://gitlab.cern.ch/hh/naming-conventions
    uncorrLumi={}
    uncorrLumi["2016"]=1.010
    uncorrLumi["2017"]=1.020
    uncorrLumi["2018"]=1.015
    cb.cp().AddSyst(cb,'lumi_13TeV_'+year,'lnN', ch.SystMap()(uncorrLumi[year]))
    if year=="2016":
        cb.cp().AddSyst(cb,'lumi_13TeV_correlated','lnN', ch.SystMap()(1.006))
    elif year=="2017":
        cb.cp().AddSyst(cb,'lumi_13TeV_correlated','lnN', ch.SystMap()(1.009))
        cb.cp().AddSyst(cb,'lumi_13TeV_1718','lnN', ch.SystMap()(1.006))
    elif year=="2018":
        cb.cp().AddSyst(cb,'lumi_13TeV_correlated','lnN', ch.SystMap()(1.020))
        cb.cp().AddSyst(cb,'lumi_13TeV_1718','lnN', ch.SystMap()(1.002))



def AddSystematics(cb, year = "2018"):
  print('add shape sys')
  #backgrounds  = cb.cp().backgrounds().process_set()
  #signal = cb.cp().signals().process_set()
  cb.cp().AddSyst(cb,'CMS_pileup_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_HF_2016_2017_2018','shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_LF_2016_2017_2018','shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_cferr1_2016_2017_2018','shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_cferr2_2016_2017_2018','shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_hfstats1_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_hfstats2_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_lfstats1_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_lfstats2_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_btag_jes_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,'CMS_PNet_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().channel(['Zee','Wen']).AddSyst(cb,'CMS_eff_e_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().channel(['Zmm','Wmn']).AddSyst(cb,'CMS_eff_m_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().channel(['Znn']).AddSyst(cb,'CMS_eff_MET_'+year,'shape',ch.SystMap()(1.0))
  cb.cp().channel(['Wen','Wmn','Znn']).process(['TT','TTB']).AddSyst(cb,'CMS_BRewError1_'+year, 'shape', ch.SystMap('bin_id')([3,4,7,8,11,12],1.0))
  cb.cp().channel(['Wen','Wmn','Znn']).process(['TT','TTB']).AddSyst(cb,'CMS_BRewError2_'+year, 'shape', ch.SystMap('bin_id')([3,4,7,8,11,12],1.0))

  # JEC reduced scheme 
  cb.cp().AddSyst(cb,"CMS_res_j_"+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_Abs",'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_Abs_"+year,'shape',ch.SystMap()(1.0))  
  cb.cp().AddSyst(cb,"CMS_scale_j_BBEC1",'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_BBEC1_"+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_EC2",'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_EC2_"+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_FlavQCD",'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_HF",'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_HF_"+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_RelBal",'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_scale_j_RelSample_"+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_MSD_JMS_"+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_MSD_JMR_"+year,'shape',ch.SystMap()(1.0))
  cb.cp().AddSyst(cb,"CMS_unclusteredEnergy_"+year,'shape',ch.SystMap()(1.0))



def drop_zero_procs(chob,proc):
  null_yield = not (proc.rate() > 0.)
  if(null_yield):
    chob.FilterSysts(lambda sys: matching_proc(proc,sys)) 
  return null_yield


def drop_zero_systs(syst):
  null_yield = (not (syst.value_u() > 0. and syst.value_d()>0.) ) and syst.type() in 'shape'
  if(null_yield):
    print 'Dropping systematic ',syst.name(),' for region ', syst.bin(), ' ,process ', syst.process(), '. up norm is ', syst.value_u() , ' and down norm is ', syst.value_d()
  return null_yield


def matching_proc(p,s):
  return ((p.bin()==s.bin()) and (p.process()==s.process()) and (p.signal()==s.signal()) 
         and (p.analysis()==s.analysis()) and  (p.era()==s.era()) 
         and (p.channel()==s.channel()) and (p.bin_id()==s.bin_id()) and (p.mass()==s.mass()))

def remove_norm_effect(syst):
  syst.set_value_u(1.0)
  syst.set_value_d(1.0)

def symm(syst,nominal):
  print 'Symmetrising systematic ', syst.name(), ' in region ', syst.bin(), ' for process ', syst.process()
  hist_u = syst.ShapeUAsTH1F()
  hist_u.Scale(nominal.Integral()*syst.value_u())
  hist_d = nominal.Clone()
  hist_d.Scale(2)
  hist_d.Add(hist_u,-1)
  syst.set_shapes(hist_u,hist_d,nominal)
  
  
def symmetrise_syst(chob,proc,sys_name):
  nom_hist = proc.ShapeAsTH1F()
  nom_hist.Scale(proc.rate())
  chob.ForEachSyst(lambda s: symm(s,nom_hist) if (s.name()==sys_name and matching_proc(proc,s)) else None)

def increase_bin_errors(proc):
  print 'increasing bin errors for process ', proc.process(), ' in region ', proc.bin()
  new_hist = proc.ShapeAsTH1F();
  new_hist.Scale(proc.rate())
  for i in range(1,new_hist.GetNbinsX()+1):
    new_hist.SetBinError(i,np.sqrt(2)*new_hist.GetBinError(i))
  proc.set_shape(new_hist,False)

  

parser = argparse.ArgumentParser()
parser.add_argument(
 '--channel', default='all', help="""Which channels to run? Supported options: 'all', 'Znn', 'Zee', 'Zmm', 'Zll', 'Wen', 'Wmn','Wln'""")
parser.add_argument(
 '--output_folder', default='vhh4b', help="""Subdirectory of ./output/ where the cards are written out to""")
parser.add_argument(
 '--year', default='2018', help="""Year to produce datacards for (2017 or 2016)""")
parser.add_argument(
 '--extra_folder', default='', help="""Additional folder where cards are""")
 #'--extra_folder', default='2017_VHbb_July17_VVfixed', help="""Additional folder where cards are""")

args = parser.parse_args()

cb = ch.CombineHarvester()
#cb.SetFlag("check-negative-bins-on-import",0)
shapes = os.environ['CMSSW_BASE'] + '/src/test_220412_2018lumi_DL_trans/'

mass = ['125']

chns = []
if args.channel=="all":
  chns = ['Wen','Wmn','Znn','Zee','Zmm']

if 'Zll' in args.channel or 'Zmm' in args.channel:
  chns.append('Zmm')
if 'Zll' in args.channel  or 'Zee' in args.channel:
  chns.append('Zee')
if 'Wln' in args.channel or 'Wmn' in args.channel:
  chns.append('Wmn')
if 'Wln' in args.channel or 'Wen' in args.channel:
  chns.append('Wen')
if 'Znn' in args.channel:
  chns.append('Znn')

year = args.year
if year is not "2016" and not "2017" and not "2018":
  print "Year ", year, " not supported! Choose from: '2016', '2017', '2018'"
  sys.exit()


bkg_procs = {
    'Wen' : ['TT','TTB','s_Top','ttH','TTV'],
    'Wmn' : ['TT','TTB','s_Top','ttH','TTV'],
    'Znn' : ['TT','TTB','s_Top','ttH','TTV'],
    'Zee' : ['TT','TTB','s_Top','ttH','TTV','DY'],
    'Zmm' : ['TT','TTB','s_Top','ttH','TTV','DY'],
}

sig_procs = {
        'Wen' : ['VHH_CV_1_C2V_1_kl_1_hbbhbb','VHH_CV_0p5_C2V_1_kl_1_hbbhbb','VHH_CV_1p5_C2V_1_kl_1_hbbhbb','VHH_CV_1_C2V_0_kl_1_hbbhbb','VHH_CV_1_C2V_2_kl_1_hbbhbb','VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_2_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb',],
        'Wmn' : ['VHH_CV_1_C2V_1_kl_1_hbbhbb','VHH_CV_0p5_C2V_1_kl_1_hbbhbb','VHH_CV_1p5_C2V_1_kl_1_hbbhbb','VHH_CV_1_C2V_0_kl_1_hbbhbb','VHH_CV_1_C2V_2_kl_1_hbbhbb','VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_2_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb',],
        'Zee' : ['VHH_CV_1_C2V_1_kl_1_hbbhbb','VHH_CV_0p5_C2V_1_kl_1_hbbhbb','VHH_CV_1p5_C2V_1_kl_1_hbbhbb','VHH_CV_1_C2V_0_kl_1_hbbhbb','VHH_CV_1_C2V_2_kl_1_hbbhbb','VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_2_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb',],
        'Zmm' : ['VHH_CV_1_C2V_1_kl_1_hbbhbb','VHH_CV_0p5_C2V_1_kl_1_hbbhbb','VHH_CV_1p5_C2V_1_kl_1_hbbhbb','VHH_CV_1_C2V_0_kl_1_hbbhbb','VHH_CV_1_C2V_2_kl_1_hbbhbb','VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_2_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb',],
        'Znn' : ['VHH_CV_1_C2V_1_kl_1_hbbhbb','VHH_CV_0p5_C2V_1_kl_1_hbbhbb','VHH_CV_1p5_C2V_1_kl_1_hbbhbb','VHH_CV_1_C2V_0_kl_1_hbbhbb','VHH_CV_1_C2V_2_kl_1_hbbhbb','VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_2_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb',],
        'Zee' : ['VHH_CV_1_C2V_1_kl_1_hbbhbb','VHH_CV_0p5_C2V_1_kl_1_hbbhbb','VHH_CV_1p5_C2V_1_kl_1_hbbhbb','VHH_CV_1_C2V_0_kl_1_hbbhbb','VHH_CV_1_C2V_2_kl_1_hbbhbb','VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_2_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb',],
        'Zmm' : ['VHH_CV_1_C2V_1_kl_1_hbbhbb','VHH_CV_0p5_C2V_1_kl_1_hbbhbb','VHH_CV_1p5_C2V_1_kl_1_hbbhbb','VHH_CV_1_C2V_0_kl_1_hbbhbb','VHH_CV_1_C2V_2_kl_1_hbbhbb','VHH_CV_1_C2V_1_kl_0_hbbhbb','VHH_CV_1_C2V_1_kl_2_hbbhbb','VHH_CV_1_C2V_1_kl_20_hbbhbb',],
}

cats = {
  'Znn' : [
    (1, 'Znn_High_R'), (2, 'Znn_Low_R'), # (13, 'Znn_High3b_R'), (14, 'Znn_Low3b_R'),(15, 'Znn_High4b_R'), (16, 'Znn_Low4b_R'),
    (3, 'Znn_HMP_B'),
    (4, 'Znn_LP_B'),
  ],
  'Wen' : [
    (5, 'Wen_High_R'), (6, 'Wen_Low_R'), # (17, 'Wen_High3b_R'), (18, 'Wen_Low3b_R'),(19, 'Wen_High4b_R'), (20, 'Wen_Low4b_R'),
    (7, 'Wen_HMP_B'),
    (8, 'Wen_LP_B'),
  ],
  'Wmn' : [
    (9, 'Wmn_High_R'), (10, 'Wmn_Low_R'), # (21, 'Wmn_High3b_R'), (22, 'Wmn_Low3b_R'),(23, 'Wmn_High4b_R'), (24, 'Wmn_Low4b_R'),
    (11, 'Wmn_HMP_B'),
    (12, 'Wmn_LP_B'),
  ],
  'Zee' : [
    (25, 'Zee_High3b_R'), (26, 'Zee_Low3b_R'),(27, 'Zee_High4b_R'), (28, 'Zee_Low4b_R'),
  ],
  'Zmm' : [
    (29, 'Zmm_High3b_R'), (30, 'Zmm_Low3b_R'),(31, 'Zmm_High4b_R'), (32, 'Zmm_Low4b_R'),
  ]
}

for chn in chns:
  cb.AddObservations( ['*'], ['vhh4b'], ['13TeV'], [chn], cats[chn])
  cb.AddProcesses( ['*'], ['vhh4b'], ['13TeV'], [chn], bkg_procs[chn], cats[chn], False)
  cb.AddProcesses( ['*'], ['vhh4b'], ['13TeV'], [chn], sig_procs[chn], cats[chn], True)


#cb.FilterProcs(lambda x: x.bin_id()==7 and x.channel()=='Znn' and x.process()=='Zj1b')
#cb.FilterProcs(lambda x: x.bin_id()==1 and x.channel()=='Znn' and x.process()=='QCD')

AddCommonSystematics(cb,year)
#AddSystematics(cb,year)

cb.AddDatacardLineAtEnd("* autoMCStats 0")

for chn in chns:
  for icat in cats[chn]:
      file = shapes + "/sum_hists_"+year+"_"+icat[1]+".root"
      cb.cp().channel([chn]).bin_id([icat[0]]).backgrounds().ExtractShapes(
      file, '$PROCESS', '$PROCESS_$SYSTEMATIC')
      cb.cp().channel([chn]).bin_id([icat[0]]).signals().ExtractShapes(
      file, '$PROCESS', '$PROCESS_$SYSTEMATIC')


ch.SetStandardBinNames(cb)
writer=ch.CardWriter("output/" + args.output_folder + year + "/$TAG/$BIN"+year+".txt",
                      "output/" + args.output_folder + year +"/$TAG/vhbb_input_$BIN"+year+".root")
writer.SetWildcardMasses([])
writer.SetVerbosity(0);
#Combined:
writer.WriteCards("cmb_all",cb);

exit()

#Per channel:
for chn in chns:
  writer.WriteCards(chn,cb.cp().channel([chn]))

if 'Znn' in chns:
      writer.WriteCards("Znn",cb.cp().channel(['Znn']))
      writer.WriteCards("Znn",cb.cp().bin_id([2,3,4,6,7,8,10,11,12,14,15,16,18,19,20]).channel(['Wmn','Wen']))
      writer.WriteCards("Znn_CRonly",cb.cp().bin_id([2,3,4,6,7,8,10,11,12,14,15,16,18,19,20]).channel(['Znn','Wmn','Wen']))

if 'Wen' in chns and 'Wmn' in chns:
  writer.WriteCards("Wln",cb.cp().channel(['Wen','Wmn']))
  writer.WriteCards("Wln_CRonly",cb.cp().bin_id([2,3,4,6,7,8,10,11,12,14,15,16,18,19,20]).channel(['Wen','Wmn']))

if 'Zee' in chns and 'Zmm' in chns:
  writer.WriteCards("Zll",cb.cp().channel(['Zee','Zmm']))
  writer.WriteCards("Zll_CRonly",cb.cp().bin_id([2,3,4,6,7,8,10,11,12,14,15,16,18,19,20]).channel(['Zee','Zmm']))










import os
year="2018"
LUMI='59.7 fb^{-1} (13 TeV)'
#year="2017"
#LUMI='41.5 fb^{-1} (13 TeV)'
#year="2016"
#LUMI='36.3 fb^{-1} (13 TeV)'
CHN_DICT_SR = {
    "Wen": [ ["vhh4b_Wen_5_13TeV"+year,"1-lepton (e)","Resolved High #kappa_{#lambda}",1,15],
             ["vhh4b_Wen_6_13TeV"+year,"1-lepton (e)","Resolved Low #kappa_{#lambda}",1,15],
             ["vhh4b_Wen_8_13TeV"+year,"1-lepton (e)","Boosted LP",1,15],],
    "Wmn": [ ["vhh4b_Wmn_9_13TeV"+year,"1-lepton (#mu)","Resolved High #kappa_{#lambda}",1,15],
             ["vhh4b_Wmn_10_13TeV"+year,"1-lepton (#mu)","Resolved Low #kappa_{#lambda}",1,15],
             ["vhh4b_Wmn_12_13TeV"+year,"1-lepton (#mu)","Boosted LP",1,15],],
    "Znn": [ ["vhh4b_Znn_1_13TeV"+year,"0-lepton","Resolved High #kappa_{#lambda}",1,15], 
             ["vhh4b_Znn_2_13TeV"+year,"0-lepton","Resolved Low #kappa_{#lambda}",1,15],
             ["vhh4b_Znn_4_13TeV"+year,"0-lepton","Boosted LP",1,15],] 
}

DIRECF = "output/test_220413_2018lumi_controlSamplecut_mask2018/cmb_all//shapes_All.root"

for MODE in ['postfit']:
    for CHN in ['Wen','Wmn','Znn']:
        for i in range(0,len(CHN_DICT_SR[CHN])):
              LABEL = "%s" % CHN_DICT_SR[CHN][i][1]
              REGION = "%s" % CHN_DICT_SR[CHN][i][2]
              OUTNAME = "%s" % CHN_DICT_SR[CHN][i][0]
              XLOW = CHN_DICT_SR[CHN][i][3]
              XHIGH = CHN_DICT_SR[CHN][i][4]
              extra= "Work in progress"
              os.system(('python postFitPlot.py' \
                  ' --file="%(DIRECF)s" --ratio --extra_pad=0.53  --extralabel "%(extra)s" --file_dir=%(OUTNAME)s ' \
                  ' --ratio_range 0.6,1.4 --empty_bin_error --channel=%(CHN)s  --x_title="BDT output" --lumi="%(LUMI)s"' \
                  ' --outname %(OUTNAME)s --mode %(MODE)s --x_axis_min %(XLOW)f --x_axis_max %(XHIGH)f --custom_x_range --log_y --custom_y_range --y_axis_min "1E-2" '\
                  ' --channel_label "%(LABEL)s" --region "%(REGION)s"' % vars()))



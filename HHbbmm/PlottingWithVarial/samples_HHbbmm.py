# The name of the TTree in the ntuple.
treename = 'Events'

stacking_order = [
    'HHbbmm(C3m05_0)*0.01',
    'DY',
]

sample_colors = {
    'HHbbmm(C3m05_0)*0.01'  :       632,
    'DY'                    :       396,
}

input_pattern = ['/data/pubfs/zhanglic/workspace/VHH4bAnalysisNtuples/TEST_1113UL/*/*%s*.root', '/data/pubfs/zhanglic/workspace/HHbbmm/*%s*/reco.root']

def get_samples(channel, signal_overlay=True, **kwargs):
    
    sf_lumi = 1.
    sf_zjb = kwargs.get('sf_zjb', 1.)
    
    ##########################################
    
    samples = {
        'DY': ["weight>-99", sf_zjb*sf_lumi, 'DY', ['DY_Zpt100to200','DY_Zpt200toinf'],1],
#         'DY': ["weight>-99", sf_zjb*sf_lumi, 'DY', ['DYToLL_M10-50_Inc_madgraph'],0],
        }
    if signal_overlay:
        samples.update({
            'HHbbmmC3m05_0':  ["weight>-99", 1.*sf_lumi*0.01, 'HHbbmm(C3m05_0)*0.01',   ['HHbbmmC3m05_0'],1],
        })
        
    if channel == 'ggF':
        samples.update({
            'Data': ["weight>-99", sf_zjb*sf_lumi, 'Data', ['DY_Zpt100to200','DY_Zpt200toinf'],1],
        })
    
    return samples
#!/usr/bin/env python

import glob


histos = {
    'dr_higg_top' : ('#DeltaR(H, t)',                          50, 0, 5      ),
    'h_pt'        : (';Higgs candidate p_{T};events / 40 GeV', 25, 0, 1000   ),
    'tlep_pt'     : (';lept. top p_{T};events / 20 GeV',       50, 0, 1000   ),
    'h_mass'      : (';Higgs candidate mass;events / 10 GeV',  25, 50, 300   ),
}
samples = [
    'TTbar',
    #'SingleT',
    #'QCD',
    #'DYJets',
    'WJets',
    'Run2015D',
    'TpB_TH_700',
    #'TpB_TH_1700',
]
all_files = glob.glob('./uhh2*.root')
filenames = dict(
    (sample, list(f for f in all_files if sample in f))
    for sample in samples
)
treename = 'AnalysisTree'
weight = {  # weight can also be a string, if common to all samples: 'weight'
    'TTbar': 'weight',
    'SingleT': 'weight',
    'QCD': 'weight',
    'DYJets': 'weight',
    'WJets': 'weight',
    'Run2015D': 'weight',
    'TpB_TH_700': 'weight',
    'TpB_TH_1700': 'weight',
}

colors = {
    'TTbar': 632 - 7,
    'WJets': 901,
    'ZJets': 856,
    'DYJets': 856,
    'DYJetsToLL': 856,
    'SingleT': 433,
    'QCD': 851,
    'TpB_TH_700': 634,
    'TpB_TH_1700': 418,
}
stacking_order=[
    'TTbar',
    'WJets',
    'SingleT',
    'QCD',
    'DYJets'
]

if __name__ == '__main__':
    from varial_ext.hquery import main
    main(
        # required parameters
        filenames=filenames,
        treename=treename,
        backend='local',  # one of jug, local

        # additional parameters
        weight=weight,
        signal_samples=['TpB_TH_700'],
        data_samples=['Run2015D'],
        stack=True,
        histos=histos,
        dump_python_conf=False,  # write histos and sections in python code
        colors=colors,
        stacking_order=stacking_order,
    )

from samples_HHbbmm import *
import varial

####################
# General Settings #
####################

#varial.settings.max_num_processes = 8
varial.settings.rootfile_postfixes += ['.pdf', '.png']
varial.settings.stacking_order = stacking_order
# try to find output on disk and don't run a step if present
enable_reuse_step = True

#################
# Plot Settings #
#################

name = 'test_plot_HHbbmm_ggF'

weight = 'weight'

plot_vars = {
    'weight'           :           ('weight',             ';weight;',           100,     -1,      1),
}

# from Muon
plot_vars.update({
    'mu0_pt'           :           ('mu0_pt',             ';p_{T}_Mu1 [GeV];',  25,     0,      600),
    'm_2mu'           :            ('m_2mu',              ';Mass_H(mm) [GeV];', 25,     50,     200),
})

#######################################
# Samples, Selections, and Categories #
#######################################

the_samples_dict = get_samples(
    channel='ggF',
    
    signal_overlay=True,
    
    sf_zjb = 1.0,
)

Hmm_win = "(m_2mu > 100 && m_2mu < 150)"

regions = {
    "ALL"                  : '{0}'.format("0 == 0"),
    "Hmm_win"              : '{0}'.format(Hmm_win),
    "out_Hmm_win"          : '!{0}'.format(Hmm_win),
}

selections = [
    'weight>-99','weight>-199',
]

the_category_dict = {
    'HHbbmm': [regions, selections, plot_vars],
}

# Blinding the Signal Region
def additional_input_hook(wrps):

    @varial.history.track_history

    def blind_in_HmmWin(w):
        if w.legend == 'Data' and w.in_file_path.startswith('Hmm_win'):
            if 'pt' or 'mu' in w.name:
                print('BLINDING Data in %s' % w.in_file_path)
                for i in xrange(w.histo.GetNbinsX() + 1):
                    w.histo.SetBinContent(i, 0.)
                    w.histo.SetBinError(i, 0.)
        return w
    
    wrps = (blind_in_HmmWin(w) for w in wrps)
    return wrps
"""
This module contains project wide settings.

Everything can be set from the outside. Checkout the source code for further
reference.
"""
import ROOT
ROOT.TH1.AddDirectory(False)


################################################################### general ###
import time
import os


recieved_sigint = False
only_reload_results = False
diskio_check_readability = False
varial_working_dir = './'
db_name = '.varial.db'
default_data_lumi = 1.
sys_var_token_up   = '__plus'
sys_var_token_down = '__minus'
# TODO default_colors_light (for backgrounds)
# TODO default_colors_strong (for signals)
default_colors = [632, 814, 596, 870, 800, 840, 902, 797, 891, 401, 434, 838,
                  872, 420, 403, 893, 881, 804, 599, 615, 831, 403, 593, 810]
wrp_sorting_keys = ['in_file_path', 'is_signal', 'is_data', 'sample']


def logfilename():
    """Generate a logfile name with timestamp."""
    return time.strftime(
        os.path.join(varial_working_dir,
                     '.varial_logs/varial_%Y%m%dT%H%M%S.log'),
        time.localtime()
    )


################################################################ processing ###
import multiprocessing
max_num_processes = multiprocessing.cpu_count()
use_parallel_chains = True
not_ask_execute = False
suppress_eventloop_exec = False
try_reuse_results = True
default_enable_sample = True
fwlite_force_reuse = False
fwlite_profiling = False
fileservice_filename = 'fileservice'
max_open_root_files = 998


def can_go_parallel():
    return use_parallel_chains and max_num_processes > 1


########################################################### style constants ###
canvas_size_x = 550
canvas_size_y = 400

box_text_size = 0.04
defaults_Legend = {
    'x_pos': 0.81,  # left edge
    'y_pos': 0.5,   # upper edge
    'label_width': 0.2,
    'label_height': 0.05,
    'opt': 'f',
    'opt_data': 'p',
    'reverse': True
    # 'text_size': 0.03,
    # 'text_font': 42,
}

defaults_BottomPlot = {
    'y_title': '',
    'draw_opt': 'E0X0',
    'draw_opt_multi_line': 'E0X1',
    'y_min': -.8,
    'y_max': .8,
    'force_y_range': False,
    'poisson_errs': False,
}

rootfile_postfixes = ['.root', '.png']
no_toggles = False  # for webcreator
colors = {}  # legend entries => fill colors
pretty_names = {}
stacking_order = []
canvas_post_build_funcs = []
stack_line_color = [1]

stat_error_color = 921
stat_error_fill = 3013
sys_error_color = 923
sys_error_fill = 3002
tot_error_color = 922
tot_error_fill = 3013


################################################################ root style ###
from array import array
from ROOT import gROOT, gStyle, TColor, TStyle, TGaxis


def apply_axis_style(obj, y_bounds):
    y_min, y_max = y_bounds
    obj.GetXaxis().SetNoExponent()
    obj.GetXaxis().SetLabelSize(0.052)
    obj.SetMinimum(y_min)
    obj.SetMaximum(y_max * 1.1 + 1e-23)
    # (the tiny addition makes sure that y_max > y_min)


def apply_error_hist_style(h, col, fill):
    if isinstance(col, tuple):
        col, opac = col
        h.SetFillColorAlpha(col, opac)
    elif isinstance(col, int):
        h.SetFillColor(col)
    h.SetMarkerColor(1)
    h.SetMarkerSize(0)
    h.SetFillStyle(fill)
    h.SetLineColor(1)


def apply_split_pad_styles(cnv_wrp):
    main, scnd = cnv_wrp.main_pad, cnv_wrp.second_pad

    main.SetTopMargin(0.135)
    main.SetBottomMargin(0.25)
    #main.SetRightMargin(0.04)
    #main.SetLeftMargin(0.16)

    scnd.SetTopMargin(0.)
    scnd.SetBottomMargin(0.375)
    #scnd.SetRightMargin(0.04)
    #scnd.SetLeftMargin(0.16)
    scnd.SetRightMargin(main.GetRightMargin())
    scnd.SetLeftMargin(main.GetLeftMargin())
    scnd.SetGridy()

    first_obj = cnv_wrp.first_obj
    first_obj.GetYaxis().CenterTitle(1)
    first_obj.GetYaxis().SetTitleSize(0.055)
    first_obj.GetYaxis().SetTitleOffset(1.3)
    first_obj.GetYaxis().SetLabelSize(0.055)
    first_obj.GetXaxis().SetNdivisions(505)


def stat_error_style(histo):
    histo.SetTitle('Stat. uncert. MC')
    apply_error_hist_style(histo, stat_error_color, stat_error_fill)


def sys_error_style(histo):
    histo.SetTitle('Sys. uncert. MC')
    apply_error_hist_style(histo, sys_error_color, sys_error_fill)


def tot_error_style(histo):
    histo.SetTitle('Tot. uncert. MC')
    apply_error_hist_style(histo, tot_error_color, tot_error_fill)


def set_bottom_plot_general_style(obj):
    obj.GetYaxis().CenterTitle(1)
    obj.GetYaxis().SetTitleSize(0.15) #0.11
    obj.GetYaxis().SetTitleOffset(0.44) #0.55
    obj.GetYaxis().SetLabelSize(0.16)
    obj.GetYaxis().SetNdivisions(205)
    obj.GetXaxis().SetNoExponent()
    obj.GetXaxis().SetTitleSize(0.16)
    obj.GetXaxis().SetLabelSize(0.17)
    obj.GetXaxis().SetTitleOffset(1)
    obj.GetXaxis().SetLabelOffset(0.006)
    obj.GetXaxis().SetNdivisions(505)
    obj.GetXaxis().SetTickLength(obj.GetXaxis().GetTickLength() * 3.)
    obj.SetTitle('')


def set_bottom_plot_ratio_style(obj):
    obj.SetLineColor(1)
    obj.SetLineStyle(1)
    obj.SetLineWidth(1)
    obj.SetMarkerStyle(20)
    obj.SetMarkerSize(.7)


def set_bottom_plot_pull_style(obj):
    obj.SetFillColor(807)


class StyleClass(TStyle):
    #"""
    #Sets all ROOT style variables.
    #Places self as new ROOT style.
    #"""
    def __init__(self):
        super(StyleClass, self).__init__('CmsRootStyle', 'CmsRootStyle')

        ################################ custom root style commands ###
        self.SetFrameBorderMode(0)
        self.SetCanvasBorderMode(0)
        self.SetPadBorderMode(0)
        self.SetPadBorderMode(0)

        #self.SetFrameColor(0)
        self.SetPadColor(0)
        self.SetCanvasColor(0)
        self.SetStatColor(0)
        self.SetFillColor(0)
        self.SetNdivisions(505, 'XY')

        self.SetTextFont(42) #132
        self.SetTextSize(0.09)
        self.SetLabelFont(42, 'xyz')
        self.SetTitleFont(42, 'xyz')
        self.SetLabelSize(0.045, 'xyz') #0.035
        self.SetTitleSize(0.045, 'xyz')
        self.SetTitleOffset(1.3, 'xy')

        self.SetTitleX(0.16)
        self.SetTitleY(0.93)
        self.SetTitleColor(1)
        self.SetTitleTextColor(1)
        self.SetTitleFillColor(0)
        self.SetTitleBorderSize(1)
        self.SetTitleFontSize(0.04)
        self.SetPadTopMargin(0.05)
        self.SetPadBottomMargin(0.13)
        #self.SetPadLeftMargin(0.14)
        #self.SetPadRightMargin(0.02)

        self.SetPaperSize(20, 26)
        self.SetPadRightMargin(0.3)
        self.SetPadLeftMargin(0.16)
        #self.SetCanvasDefH(800)
        #self.SetCanvasDefW(800)
        #self.SetPadGridX(1)
        #self.SetPadGridY(1)
        self.SetPadTickX(1)
        self.SetPadTickY(1)

        # use bold lines and markers
        self.SetMarkerStyle(8)
        self.SetMarkerSize(1.2)
        self.SetHistLineWidth(1)
        self.SetLineWidth(1)
        self.SetEndErrorSize(0)

        self.SetOptTitle(1)
        self.SetOptStat(0)

        # don't know what these are for. Need to ask the kuess'l-o-mat.
        self.colors = [1, 2, 3, 4, 6, 7, 8, 9, 11]
        self.markers = [20, 21, 22, 23, 24, 25, 26, 27, 28]
        self.styles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ############################ end custom root style commands ###

        self.cd()
        self.set_palette()
        gROOT.SetStyle('CmsRootStyle')
        gROOT.ForceStyle()
        TGaxis.SetMaxDigits(3)

    @staticmethod
    def set_palette(name='', ncontours=999):
        if name == 'gray' or name == 'grayscale':
            stops = [0.00, 0.34, 0.61, 0.84, 1.00]
            red   = [1.00, 0.84, 0.61, 0.34, 0.00]
            green = [1.00, 0.84, 0.61, 0.34, 0.00]
            blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
        else:
            # default palette, looks cool
            stops = [0.00, 0.34, 0.61, 0.84, 1.00]
            red   = [0.00, 0.00, 0.87, 1.00, 0.51]
            green = [0.00, 0.81, 1.00, 0.20, 0.00]
            blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

        s = array('d', stops)
        r = array('d', red)
        g = array('d', green)
        b = array('d', blue)

        npoints = len(s)
        TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
        gStyle.SetNumberContours(ncontours)

root_style = StyleClass()

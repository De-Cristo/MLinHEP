from ROOT import TH1I, gROOT, kRed, kBlue
import unittest
import tempfile
import shutil
import os

from varial.extensions.cmsrun import Sample
from varial.wrappers import HistoWrapper
from varial.history import History
from varial import analysis
from varial import settings
from varial import diskio


class TestHistoToolsBase(unittest.TestCase):
    def setUp(self):
        super(TestHistoToolsBase, self).setUp()

        test_fs = "fileservice/"
        if not os.path.exists(test_fs):
            test_fs = "varial/test/" + test_fs

        settings.DIR_FILESERVICE = test_fs
        if (not os.path.exists(test_fs + "tt.root")) \
        or (not os.path.exists(test_fs + "ttgamma.root")) \
        or (not os.path.exists(test_fs + "zjets.root")):
            self.fail("Fileservice testfiles not present!")

        # create samples
        analysis.all_samples["tt"] = Sample(
            name = "tt",
            is_data = True,
            lumi = 3.,
            legend = "pseudo data",
            input_files = ["none"],
        )
        analysis.all_samples["ttgamma"] = Sample(
            name = "ttgamma",
            lumi = 4.,
            legend = "tt gamma",
            input_files = ["none"],
        )
        analysis.all_samples["zjets"] = Sample(
            name = "zjets",
            lumi = 0.1,
            legend = "z jets",
            input_files = ["none"],
        )
        analysis.colors = {
            "tt gamma": kRed,
            "z jets": kBlue
        }
        settings.stacking_order = [
            "tt gamma",
            "z jets"
        ]
        analysis.active_samples = analysis.all_samples.keys()

        # create a test wrapper
        h1 = TH1I("h1", "H1", 2, .5, 4.5)
        h1.Fill(1)
        h1.Fill(3,2)
        hist = History("test_op") # create some fake history
        hist.add_args([History("fake_input_A"), History("fake_input_B")])
        hist.add_kws({"john": "cleese"})
        self.test_wrp = HistoWrapper(
            h1,
            name="Nam3",
            title="T1tl3",
            history=hist
        )

        self.test_dir = tempfile.mkdtemp()
        analysis.cwd = self.test_dir

    def tearDown(self):
        super(TestHistoToolsBase, self).tearDown()

        del self.test_wrp

        diskio.close_open_root_files()
        gROOT.Reset()

        if os.path.exists(self.test_dir):
            os.system('rm -r %s' % self.test_dir)

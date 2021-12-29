#!/usr/bin/env python

import os
import ROOT
ROOT.gROOT.SetBatch()

from test_histotoolsbase import TestHistoToolsBase
from varial.wrappers import HistoWrapper
import varial.rendering as rnd
import varial.diskio as diskio

class TestRendering(TestHistoToolsBase):
    def test_canvasBuilder_make(self):
        wrp1 = self.test_wrp
        wrp2 = HistoWrapper(wrp1.histo, history="Fake history")
        wrp2.histo.Scale(1.5)
        wrp = rnd.build_canvas((wrp1, wrp2), rnd.build_funcs, [])

        # check for stack and data to be in canvas primitives
        prim = wrp.canvas.GetListOfPrimitives()
        self.assertTrue(wrp1.histo in prim)
        self.assertTrue(wrp2.histo in prim)
        self.test_wrp = wrp

    def test_canvas_info_file(self):
        fname = self.test_dir + '/cnv_save.info'
        self.test_canvasBuilder_make()
        diskio.write(self.test_wrp, fname)

        # file should have a couple of lines
        with open(fname) as fhandle:
            self.assertGreater(len(list(fhandle)), 10)


import unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestRendering)
if __name__ == '__main__':
    unittest.main()

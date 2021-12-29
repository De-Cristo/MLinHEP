#!/usr/bin/env python

import unittest
from varial.operations import stack, NoLumiMatchError
from varial.wrappers import HistoWrapper
from varial.history import History
from ROOT import TH1I, THStack


class TestOps(unittest.TestCase):
    def setUp(self):
        super(TestOps, self).setUp()
        h1 = TH1I("h1", "", 2, .5, 4.5)
        h1.Fill(1, 4)
        self.wrp1 = HistoWrapper(h1, lumi=2., history=History("wrp1"))
        h2 = TH1I("h2", "", 2, .5, 4.5)
        h2.Fill(1, 3)
        h2.Fill(3, 6)
        self.wrp2 = HistoWrapper(h2, lumi=3., history=History("wrp2"))

    def tearDown(self):
        super(TestOps, self).tearDown()
        del self.wrp1
        del self.wrp2

    def test_stack(self):
        self.assertRaises(NoLumiMatchError, stack, [self.wrp1, self.wrp2])
        self.wrp2.lumi = 2.
        res = stack([self.wrp1, self.wrp2])
        self.assertEqual(res.histo.Integral(), 13.0)
        self.assertEqual(res.lumi, 2.0)
        self.assertTrue(isinstance(res.stack, THStack))
        self.assertEqual(res.stack.GetHists()[0], self.wrp1.histo)
        self.assertEqual(res.stack.GetHists()[1], self.wrp2.histo)

    def test_history(self):
        self.wrp2.lumi = 2.
        res = stack([self.wrp1, self.wrp2])
        history = "stack(\n    [\n        wrp1(),\n        wrp2(),\n    ],\n)"
        self.assertEqual(str(res.history), history)
        self.wrp1.history = History("one")
        res = stack([self.wrp1, self.wrp2])
        self.assertEqual(res.history.args[0][0], self.wrp1.history)
        self.assertEqual(res.history.args[0][1], self.wrp2.history)


suite = unittest.TestLoader().loadTestsFromTestCase(TestOps)
if __name__ == '__main__':
    unittest.main()

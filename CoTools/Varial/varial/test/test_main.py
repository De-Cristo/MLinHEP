#!/usr/bin/env python

import unittest
import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')
ROOT.TH1.AddDirectory(False)

from test_diskio import suite as dio_suite
from test_sparseio import suite as sio_suite
from test_dbio import suite as dbi_suite
from test_pklio import suite as pki_suite
from test_generators import suite as gen_suite
from test_ops import suite as ops_suite
from test_rendering import suite as rnd_suite
from test_tools import suite as tls_suite

import doctest
import varial.generators as gen
import varial.history as hst
import varial.operations as ops
import varial.rendering as rnd
import varial.wrappers as wrp
import varial.util as uti

suite = unittest.TestSuite((
    doctest.DocTestSuite(wrp),
    doctest.DocTestSuite(hst),
    doctest.DocTestSuite(ops),
    doctest.DocTestSuite(rnd),
    doctest.DocTestSuite(gen),
    doctest.DocTestSuite(uti),
    ops_suite,
    dio_suite,
    sio_suite,
    dbi_suite,
    pki_suite,
    gen_suite,
    rnd_suite,
    tls_suite,
))

import sys
if __name__ == '__main__':
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    if res.failures:
        sys.exit(-1)

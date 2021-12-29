#!/usr/bin/env python

import os
from test_histotoolsbase import TestHistoToolsBase
from varial import dbio
from varial import analysis


class TestDbio(TestHistoToolsBase):
    def setUp(self):
        super(TestDbio, self).setUp()
        dbio._init(self.test_dir + '/test.db')

    def tearDown(self):
        dbio._close()
        super(TestDbio, self).tearDown()
        
    def test_write(self):
        dbio.write(self.test_wrp)

        # check existance
        c = dbio._db_conn.cursor()
        c.execute('SELECT * FROM analysis')
        self.assertTrue(bool(c.fetchone()))

        c.execute('SELECT data FROM analysis')
        self.assertTrue(bool(c.fetchone()))

        c.execute('SELECT data FROM analysis WHERE path=?',
                  (analysis.cwd + self.test_wrp.name,))
        self.assertTrue(bool(c.fetchone()))

    def test_read(self):
        self.test_wrp.history = str(self.test_wrp.history)
        dbio.write(self.test_wrp)
        loaded = dbio.read(self.test_wrp.name)

        # check names
        self.assertEqual(
            self.test_wrp.all_writeable_info(),
            loaded.all_writeable_info()
        )

        # check histograms (same integral, different instance)
        self.assertEqual(self.test_wrp.histo.Integral(),loaded.histo.Integral())
        self.assertNotEqual(str(self.test_wrp.histo), str(loaded.histo))

        # check error
        self.assertRaises(RuntimeError, dbio.read, "non_existent")


import unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestDbio)
if __name__ == '__main__':
    unittest.main()

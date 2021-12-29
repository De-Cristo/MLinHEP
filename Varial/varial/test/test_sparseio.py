#!/usr/bin/env python

import os
from test_histotoolsbase import TestHistoToolsBase
from varial import diskio
from varial import sparseio
from varial import wrappers
from varial import settings

class TestSparseio(TestHistoToolsBase):

    def setUp(self):
        super(TestSparseio, self).setUp()
        if not os.path.exists('test_data'):
            os.mkdir('test_data')
        aliases = diskio.generate_aliases(settings.DIR_FILESERVICE+'tt.root')
        self.test_wrps = list(diskio.load_histogram(a) for a in aliases)
        self.name_func = lambda w: w.in_file_path.replace('/', '_')


    def test_bulk_write(self):
        sparseio.bulk_write(
            self.test_wrps, self.name_func, self.test_dir, ('.png', '.pdf'))

        # files should exist
        self.assertTrue(os.path.exists(self.test_dir+'/'+sparseio._infofile))
        self.assertTrue(os.path.exists(self.test_dir+'/'+sparseio._rootfile))
        for w in self.test_wrps:
            tok = self.name_func(w)
            self.assertTrue(os.path.exists(self.test_dir+'/%s.png' % tok))
            self.assertTrue(os.path.exists(self.test_dir+'/%s.pdf' % tok))

    def test_bulk_read_info_dict(self):
        sparseio.bulk_write(
            self.test_wrps, self.name_func, self.test_dir, ('.png', '.pdf'))
        read_in = sparseio.bulk_read_info_dict(self.test_dir)

        # verify filenames
        for name, wrp in read_in.iteritems():
            self.assertEqual(name, self.name_func(wrp))

        # assert input info == output info
        dict_out = dict((self.name_func(w),
                         wrappers.Wrapper(  # need to harmonize 'klass' item
                             **w.all_writeable_info()
                         ).pretty_writeable_lines())
                        for w in self.test_wrps)
        dict_inp = dict((self.name_func(w), w.pretty_writeable_lines())
                        for w in read_in.itervalues())
        self.assertDictEqual(dict_out, dict_inp)


import unittest
suite = unittest.TestLoader().loadTestsFromTestCase(TestSparseio)
if __name__ == '__main__':
    unittest.main()

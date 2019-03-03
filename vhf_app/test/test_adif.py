#!/usr/bin/env python3

import unittest
import os.path

from vhf.adif import Adif

# adif file examples dir (relative to this test file)
EXAMPLES_DIR = 'examples'

class TestAdif(unittest.TestCase):

    def _get_adif(self, example):
        return os.path.join(os.path.dirname(__file__), EXAMPLES_DIR, example)


    def test_adif(self):
        a = Adif()
        self.assertIsInstance(a, Adif, 'new object is an instance of Adif')
    
    def test_adif_from_file(self):
       
        adif_file = self._get_adif('PA OM1AKU.adi')
        self.assertTrue(os.path.isfile(adif_file), "Check if %s exists." % adif_file)
        adif_log = Adif(from_file=adif_file)
        self.assertIsInstance(adif_log, Adif, 'Create ADIF log from file')
        self.assertEqual(len(adif_log.qsos), 31, 'Correct number of processed QSOs')


if __name__ == '__main__':
    unittest.main()
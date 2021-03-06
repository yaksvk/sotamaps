#!/usr/bin/env python3

import unittest
import os.path

from vhf.adif import Adif

# adif file examples dir (relative to this test file)
EXAMPLES_DIR = 'examples'

class TestAdif(unittest.TestCase):

    def _get_adif(self, example):
        return os.path.join(os.path.dirname(__file__), EXAMPLES_DIR, example)
    
    def setUp(self):
        self.adif1 = self._get_adif('PA OM1AKU.adi')
        self.adif2 = self._get_adif('20190317_OM1WS.adif')

    def test_adif(self):
        a = Adif()
        self.assertIsInstance(a, Adif, 'new object is an instance of Adif')
    
    def test_adif_from_file(self):
        self.assertTrue(os.path.isfile(self.adif1), "Check if %s exists." % self.adif1)
        adif_log = Adif(from_file=self.adif1)
        self.assertIsInstance(adif_log, Adif, 'Create ADIF log from file')
        self.assertEqual(len(adif_log.qsos), 31, 'Correct number of processed QSOs')

    def test_adif_header(self):
        # we should be able to extract a header out of the adif if available
        adif1 = Adif(from_file=self.adif1)
        adif2 = Adif(from_file=self.adif2)

        self.assertIsInstance(adif1.header, dict)
        self.assertIsInstance(adif2.header, dict)
        self.assertEqual('PROGRAMID' in adif1.header, True)
        self.assertEqual(adif1.header.get('PROGRAMID'), 'MacLoggerDX')

    def test_adif_comments(self):
        adif = Adif(from_file=self._get_adif('20190317_OM1WS.adif'))
        self.assertEqual(adif.comments.get('PWWLO'), 'JN88OJ')

    def test_adif_guess(self):
        with open(self.adif1) as f:
            data = f.read()
            self.assertTrue(Adif.can_process(data))


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3

import unittest
import os.path

from vhf.activity import Qso, Log

# adif file examples dir (relative to this test file)
EXAMPLES_DIR = 'examples'

class TestActivity(unittest.TestCase):

    def _get_adif(self, example):
        return os.path.join(os.path.dirname(__file__), EXAMPLES_DIR, example)

    def test_basic_log(self):
        self.assertIsInstance(Log(), Log)

    def test_adif_log(self):
        self.assertIsInstance(Log(adif_file=self._get_adif('PA OM1AKU.adi')), Log)
        
    def test_points_and_scores_1(self):
        log = Log(adif_file=self._get_adif('PA OM1AKU.adi'))
        self.assertEqual(len(log.qsos), 31, 'Number of qsos')

        scores = log.compute_scores()
        self.assertIsInstance(scores, dict)
        self.assertEqual(scores['multiplier_count'], 8, 'Number of multipliers')
        self.assertEqual(scores['original_qso_count'], 31, 'Number of original QSOs')
        self.assertEqual(scores['score'], 88, 'Score')
        self.assertEqual(scores['score_multiplied'], 704, 'Score multiplied')


if __name__ == '__main__':
    unittest.main()
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

    def test_distances(self):
        # test parsing a log without contest exchanges and with 4letter gridsquares
        log = Log(adif_file=self._get_adif('wsjtx_log.adi'))
        self.assertEqual(log.qsos[10].gridsquare, 'KO33')
        self.assertEqual(log.qsos[10].latlng, (53.5, 27.0))

    def test_my_gridsquare_guessing(self):
        cases = (        
            { 'log': 'PA OM1AKU.adi', 'grid': 'JN88PE' },
            { 'log': 'wsjtx_log.adi', 'grid': 'JN88QF' },
            { 'log': 'test2019.adif', 'grid': 'KN08OR' },
            { 'log': 'european vhf simple.ADI', 'grid': 'NONE'},
        )
        for case in cases:
            with self.subTest(case):
                log = Log(adif_file=self._get_adif(case['log']))
                self.assertEqual(str(log.gridsquare).upper(), case['grid'])

    def test_rx_tx(self):
        # pick first qso and test RX, TX
        cases = (        
            { 'log': 'PA OM1AKU.adi', 'use_grid': 'JN88pe', 'stx': 1, 'srx': 17 },
            { 'log': 'european vhf simple.ADI', 'use_grid': 'JN88nc', 'stx': 1, 'srx': 14 },
            { 'log': 'test2019.adif', 'use_grid': 'KN08OR', 'stx': 1, 'srx': 17 },
        )
        for case in cases:
            with self.subTest(case):
                log = Log(adif_file=self._get_adif(case['log']), gridsquare=case['use_grid'])
                first_qso = log.qsos[0]
                self.assertEqual(
                    (int(first_qso.stx), int(first_qso.srx)),
                    (case['stx'], case['srx'])
                )
    
    def test_gridsquare_guess(self):
        # test gridsquare guessing from various logs srx/srx_string/etc.
        pass


if __name__ == '__main__':
    unittest.main()

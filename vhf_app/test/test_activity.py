#!/usr/bin/env python3

import unittest
import os.path

from vhf.activity import Qso, Log

# adif file examples dir (relative to this test file)
EXAMPLES_DIR = 'examples'

class TestActivity(unittest.TestCase):
    maxDiff = None

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
        # test gridsquare guessing from log comments
        log = Log(adif_file=self._get_adif('20190317_OM1WS.adif'))
        self.assertEqual(log.gridsquare, 'JN88OJ')

    def test_export_dictionary(self):
        # test if QSO can be exported as a dictionary (we use this later for saving)
        log = Log(adif_file=self._get_adif('20190317_OM1WS.adif'))
        self.assertEqual(log.export_dictionary(),
            {'comments': {'PCALL': 'OM1WS', 'PSECT': 'Single', 'PWWLO': 'JN88OJ'},
            'gridsquare': 'JN88OJ',
            'qsos': [{'adif_ver': '1.00',
            'band': '2M',
            'call': 'S57O',
            'distance': 229,
            'gridsquare': 'JN86DK',
            'latlng': (46.4375, 16.291666666666664),
            'mode': 'SSB',
            'no_rcvd': '006',
            'no_sent': '001',
            'operator': 'OM1WS',
            'points': 4,
            'prop_mode': 'TR',
            'qrb': '228',
            'qso_date': '20190317',
            'qtf': '198',
            'rst_rcvd': '59',
            'rst_sent': '59',
            'srx': '006',
            'stx': '001',
            'time_on': '0805',
            'top_distance': True},
            {'band': '2M',
            'call': 'SP6KEP',
            'distance': 239,
            'gridsquare': 'JO90CK',
            'latlng': (50.4375, 18.208333333333336),
            'mode': 'SSB',
            'no_rcvd': '026',
            'no_sent': '002',
            'operator': 'OM1WS',
            'points': 4,
            'prop_mode': 'TR',
            'qrb': '238',
            'qso_date': '20190317',
            'qtf': '17',
            'rst_rcvd': '59',
            'rst_sent': '59',
            'srx': '026',
            'stx': '002',
            'time_on': '0810',
            'top_distance': True}]})

    def test_init_from_dictionary(self):
        # test log initialization from the dictionary
        log1 = Log(adif_file=self._get_adif('20190317_OM1WS.adif'))
        log_dict = log1.export_dictionary()
        log2 = Log(dictionary=log_dict)

        cases = (
            (len(log1.qsos), len(log2.qsos), 'number of QSOs match'),
            (log1.gridsquare, log2.gridsquare, 'gridsquare match'),
            (log1.scores['score'], log2.scores['score'], 'score match')
        )

        for case in cases:
            with self.subTest(case):
                self.assertEqual(case[0], case[1], case[2]);

if __name__ == '__main__':
    unittest.main()

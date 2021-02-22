#!/usr/bin/env python3

import unittest

from vhf.gridsquare import is_gridsquare, small_square_distance, gridsquare2latlng, extract_gridsquare, \
    dist_haversine, dist_ham, gridsquare2latlngedges, _norm_gridsquare

class TestGridsquare(unittest.TestCase):

    def test_norm_gridsquare(self):
        self.assertEqual(_norm_gridsquare('AAbbCC'), (0,0,1,1,2,2))
        self.assertEqual(_norm_gridsquare('JN88nc'), (9,13,8,8,13,2))

    def test_is_gridsquare(self):
        self.assertTrue(is_gridsquare('JN88nc'))
        self.assertFalse(is_gridsquare('xxx'))
        self.assertFalse(is_gridsquare(''))
        self.assertFalse(is_gridsquare(None))
        self.assertFalse(is_gridsquare('xJN88ncx'))
        self.assertTrue(is_gridsquare('KN13'))

    def test_extract_gridsquare(self):
        self.assertEqual(extract_gridsquare('xJN88ncx'), 'JN88nc')
        self.assertEqual(extract_gridsquare('x188ncx'), None)

    def test_small_square_distance(self):
        cases = (
            ('JN88nc','JN88nc', 0),
            ('JN88nc','JN88aa', 0),
            ('JO42bm','JO51fl', 1),
            ('JN88uu','JO60LJ', 2)
        )
        for case in cases:
            with self.subTest(case):
                self.assertEqual(small_square_distance(case[0], case[1]), case[2])

    def test_gridsquare2latlng(self):
        self.assertEqual(gridsquare2latlng('JN88nc'),(48.10416666666667, 17.125))

    def test_dist_ham_polymorphism(self):
        # test that the function can work with latlng tuples as good as with gridsquares
        dist1 = dist_ham((48.354167, 19.708333), (48.104167, 17.125))
        dist2 = dist_ham('JN98ui','JN88nc')
        self.assertEqual(dist1, dist2)

    def test_distance_subregional(self):
        cases = (
            ('JN87WV', 'JN97QO', 117),
            ('JN87WV', 'JN64DJ', 580),
            ('JN87WV', 'JN66WB', 366),
            ('JN87WV', 'JN98AH', 48),
            ('JN87WV', 'JO82CK', 519),
            ('JN87WV', 'JN45CD', 800),
            ('JN98UI', 'JN97WM', 94),
            ('JN98UI', 'JO91QF', 321),
            ('JN98UI', 'JN98PP', 45),
            ('JN98UI', 'JN98WD', 27),
            ('JN88NG', 'JN95GO', 316),
            ('JN88NG', 'JN96LX', 199),
            ('JN88NG', 'KN13OT', 683),
            ('JN88NG', 'JO61WN', 434)
        )
        for vals in cases:
            with self.subTest(vals):
                self.assertEqual(dist_ham(vals[0],vals[1]),vals[2])

    def test_gridsquare_edges(self):
        self.assertEqual(gridsquare2latlngedges('JN88nc'),((48.083333333333336, 17.083333333333332), (48.125, 17.166666666666664)))
        self.assertEqual(gridsquare2latlngedges('JN88'), ((48.0, 16.0), (49.0, 18.0)))

if __name__ == '__main__':
    unittest.main()

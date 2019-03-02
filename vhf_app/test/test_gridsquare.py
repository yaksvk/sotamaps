#!/usr/bin/env python3

import unittest

from vhf.gridsquare import is_gridsquare, small_square_distance, gridsquare2latlng, extract_gridsquare

class TestGridsquare(unittest.TestCase):

    def test_is_gridsquare(self):
        self.assertTrue(is_gridsquare('JN88nc'))
        self.assertFalse(is_gridsquare('xxx'))
        self.assertFalse(is_gridsquare('xJN88ncx'))

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

    def test_distance_k7fry(self):
        cases = (        
            ('JN88le','JN98iv',151.166), 
            ('JN88le','JN98ai',82.386),
            ('JN88le','JO80il',255.751),
            ('JN88le','JN88qw',88.953),
            ('JN88le','JN84gv',367.811)
        )

        #for vals in cases:
        #    with self.subTest(vals):
        #        self.assertEqual(small_square_distance(vals[0], vals[1]), vals[2])
            


if __name__ == '__main__':
    unittest.main()

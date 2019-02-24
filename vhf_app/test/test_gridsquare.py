#!/usr/bin/env python3

import unittest

from vhf.gridsquare import is_gridsquare, small_square_distance, gridsquare2latlng

class TestGridsquare(unittest.TestCase):

    def test_is_gridsquare(self):
        self.assertTrue(is_gridsquare('JN88nc'))
        self.assertFalse(is_gridsquare('xxx'))

    def test_small_square_distance(self):
        self.assertEqual(small_square_distance('JN88nc','JN88aa'), 0)
        self.assertEqual(small_square_distance('JO42bm','JO51fl'), 1)
        self.assertEqual(small_square_distance('JN88uu','JO60LJ'), 2)

    def test_gridsquare2latlng(self):
        self.assertEqual(gridsquare2latlng('JN88nc'),(48.10416666666667, 17.125))


if __name__ == '__main__':
    unittest.main()

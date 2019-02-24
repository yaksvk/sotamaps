#!/usr/bin/env python3

import unittest

from vhf.adif import Adif

class TestAdif(unittest.TestCase):

    def test_adif(self):
        a = Adif()
        self.assertIsInstance(a, Adif, 'new object is an instance of Adif')


if __name__ == '__main__':
    unittest.main()

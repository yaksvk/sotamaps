#!/usr/bin/env python3

import unittest

from vhf.gridsquare import is_gridsquare

class TestGridsquare(unittest.TestCase):

    def test_is_gridsquare(self):
        self.assertTrue(is_gridsquare('JN88nc'))


if __name__ == '__main__':
    unittest.main()

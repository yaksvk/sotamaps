#!/usr/bin/env python3

import unittest

from vhf.activity import Qso, Log

class TestActivity(unittest.TestCase):
    def test_basic_log(self):
        a = Log()
        self.assertIsInstance(a, Log)
    def test_adif_log(self):
        pass



if __name__ == '__main__':
    unittest.main()

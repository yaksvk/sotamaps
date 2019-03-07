#!/usr/bin/env python3

import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index(self):
        res_index = self.app.get('/')
        self.assertEqual(res_index.status_code, 404)

    def test_vhf_index_redirect(self):
        res_index = self.app.get('/vhf')
        self.assertEqual(res_index.status_code, 301)

if __name__ == '__main__':
    unittest.main()

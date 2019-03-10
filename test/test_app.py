#!/usr/bin/env python3

import unittest
import re
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index(self):
        res_index = self.app.get('/')
        self.assertEqual(res_index.status_code, 404)

    def test_vhf_index(self):
        res_index = self.app.get('/vhf', follow_redirects=True)
        self.assertEqual(res_index.status_code, 200)
        self.assertTrue(str(res_index.data).index('<div id="upload_form"') > 0)

    def test_vhf_log_upload(self):
        data = {}

        with open('vhf_app/test/examples/PA OM1AKU.adi', 'rb') as f:

            data = {
                'file': (f, f.name),
                'gridsquare': 'JN88pe'
            }

            res_upload = self.app.post(
                '/vhf/',
                content_type='multipart/form-data',
                data=data,
                follow_redirects=True
            )
            self.assertEqual(res_upload.status_code, 200, 'Upload OK.')
            text = res_upload.get_data(as_text=True)
            self.assertIsInstance(text, str, 'Extract HTML as string from reply.')

            # extract table data
            table = re.search('<table id="results">(.*?)</table>', text, flags=re.MULTILINE | re.DOTALL).group(1)

            # extract and compare scores
            score_values = re.findall('<td>(?:<strong>)?(.*?)(?:</strong>)?</td>', table)
            self.assertEqual(len(score_values), 5, 'Scores table length.')
            self.assertEqual('JN88pe', score_values[0], 'Gridsquare.')
            self.assertEqual('31', score_values[1], 'Number of QSOs parsed.') 
            self.assertEqual('8', score_values[2], 'Number of Multipliers')
            self.assertEqual('88', score_values[3], 'QSO points')

if __name__ == '__main__':
    unittest.main()

import io
import os
import json
import unittest
import app_server

class AuthServerTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        "set up test fixtures"
        print('### Setting up auth server ###')
        app = app_server.app
        app.config['TESTING'] = True
        self.app = app.test_client()

    @classmethod
    def tearDownClass(self):
        "tear down test fixtures"
        print('### Tearing down the auth server ###')

    def test_01_get_ping(self):
        """ Test that the auth server is running and reachable"""

        r = self.app.get('/api/v1/ping')
        self.assertEqual(r.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()

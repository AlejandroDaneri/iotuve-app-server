import unittest
import app_server
from http import HTTPStatus
from mongoengine import connect, disconnect
from src.conf import APP_NAME


class StatusTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = app_server.app
        app.config['TESTING'] = True
        cls.app = app.test_client()
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_home_should_return_ok(self):
        r = self.app.get('/api/v1/')
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertTrue('Welcome' in r.get_data(as_text=True))

    def test_ping_should_return_ok(self):
        r = self.app.get('/api/v1/ping')
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual('Pong!', r.get_data(as_text=True))

    def test_stats_should_return_stats_list(self):
        r = self.app.get('/api/v1/stats')
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(HTTPStatus.OK, r.json[0]['status'])

    def test_status_should_return_ok(self):
        r = self.app.get('/api/v1/status')
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(APP_NAME, r.json['message'])


if __name__ == '__main__':
    unittest.main()

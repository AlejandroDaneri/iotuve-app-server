import unittest
import app_server
from http import HTTPStatus
from mongoengine import connect, disconnect
from src.conf import APP_NAME
from tests.test_utils import utils


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

    def tearDown(self):
        utils.delete_all()

    def test_home_should_return_ok(self):
        res = self.app.get('/api/v1/')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertTrue('Welcome' in res.get_data(as_text=True))

    def test_ping_should_return_ok(self):
        res = self.app.get('/api/v1/ping')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual('Pong!', res.get_data(as_text=True))

    def test_stats_should_return_stats_list(self):
        for _ in range(0, 4):
            self.app.get('/api/v1/ping')
        res = self.app.get('/api/v1/stats')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(4, len(res.json['data']))
        for data in res.json['data']:
            self.assertEqual('GET', data["method"])
            self.assertEqual('/api/v1/ping?', data["full_path"])
            self.assertEqual(200, data["status"])

    def test_stats_query_should_return_stats_list(self):
        for _ in range(0, 4):
            self.app.get('/api/v1/ping')
            self.app.get('/api/v1')

        res = self.app.get('/api/v1/stats', query_string={"method": "GET"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(8, len(res.json['data']))

        res = self.app.get('/api/v1/stats', query_string={"method": "POST"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(0, len(res.json['data']))

        res = self.app.get('/api/v1/stats', query_string={"path": "/api/v1"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(4, len(res.json['data']))

        res = self.app.get('/api/v1/stats', query_string={"path": "/api/v1/ping"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(4, len(res.json['data']))

    def test_status_should_return_ok(self):
        res = self.app.get('/api/v1/status')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(APP_NAME, res.json['message'])


if __name__ == '__main__':
    unittest.main()

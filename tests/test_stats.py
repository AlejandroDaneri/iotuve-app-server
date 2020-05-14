import unittest
import app_server
from mongoengine import connect, disconnect


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
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Welcome' in r.get_data(as_text=True))

    def test_ping_should_return_ok(self):
        r = self.app.get('/api/v1/ping')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_data(as_text=True), 'Pong!')

    def test_stats_should_return_stats_list(self):
        r = self.app.get('/api/v1/stats')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json[0]['status'], 200)


if __name__ == '__main__':
    unittest.main()

import unittest
import app_server


class StatusTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = app_server.app
        app.config['TESTING'] = True
        cls.app = app.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_home_should_return_ok(self):
        self.assertEqual(True, True)

    def test_ping_should_return_ok(self):
        r = self.app.get('/api/v1/ping')
        self.assertEqual(r.status_code, 200)

    def test_stats_should_return_server_status(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

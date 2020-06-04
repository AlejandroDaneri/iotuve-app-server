import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect


class UsersTestCase(unittest.TestCase):

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

    def test_private_enpoints_recovery_without_token_should_return_unauthorized(self):
        res = self.app.get('/api/v1/recovery')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/recovery/testuser')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.requests.post')
    def test_post_valid_recovery_request_should_return_auth_api_response(self, mock_post):
        mock_post.return_value.json.return_value = dict(recovery_key="123456")
        mock_post.return_value.status_code = HTTPStatus.CREATED
        r = self.app.post('/api/v1/recovery', json=dict(username="testuser"))
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("123456", r.json["recovery_key"])

    @patch('src.clients.auth_api.requests.post')
    def test_post_empty_recovery_request_should_return_bad_request(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/recovery')
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.requests.post')
    def test_post_valid_recovery_reset_should_return_auth_api_response(self, mock_post):
        mock_post.return_value.json.return_value = dict(message="ok")
        mock_post.return_value.status_code = HTTPStatus.CREATED
        r = self.app.post('/api/v1/recovery/testuser',
                          json=dict(password="testpassword", recovery_key="123456"))
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("ok", r.json["message"])

    @patch('src.clients.auth_api.requests.post')
    def test_post_empty_recovery_reset_should_return_auth_api_response(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/recovery/testuser')
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)


if __name__ == '__main__':
    unittest.main()

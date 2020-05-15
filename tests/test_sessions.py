import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect


class SessionsTestCase(unittest.TestCase):

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

    def test_private_enpoints_session_without_token_should_return_unauthorized(self):
        res = self.app.get('/api/v1/sessions')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.delete('/api/v1/sessions')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_session_should_return_auth_api_response(self, mock_get):
        mock_get.return_value.json.return_value = dict(session_token="123456", username="testuser")
        mock_get.return_value.status_code = HTTPStatus.OK
        r = self.app.get(
            '/api/v1/sessions',
            headers={'X-Auth-Token': '123456'}
        )
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("123456", r.json["session_token"])
        self.assertEqual("testuser", r.json["username"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.delete')
    def test_delete_session_should_return_auth_api_response(self, mock_delete, mock_session):
        mock_delete.return_value.json.return_value = dict(message="deleted")
        mock_delete.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(session_token="123456", username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.delete(
            '/api/v1/sessions',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("deleted", r.json["message"])

    @patch('src.clients.auth_api.requests.post')
    def test_post_valid_session_should_return_auth_api_response(self, mock_post):
        mock_post.return_value.json.return_value = dict(session_token="123456")
        mock_post.return_value.status_code = HTTPStatus.CREATED
        r = self.app.post('/api/v1/sessions', json=dict(
            username="testuser",
            password="password"
        ))
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("123456", r.json["session_token"])

    @patch('src.clients.auth_api.requests.post')
    def test_post_without_username_should_return_bad_request(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/sessions', json=dict(
            password="password"
        ))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.requests.post')
    def test_post_without_password_should_return_bad_request(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/sessions', json=dict(
            username="testuser"
        ))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)


if __name__ == '__main__':
    unittest.main()

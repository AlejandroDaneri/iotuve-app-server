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

    def test_private_enpoints_users_without_token_should_return_unauthorized(self):
        res = self.app.get('/api/v1/users')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/users/testuser')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.put('/api/v1/users/testuser')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.patch('/api/v1/users/testuser')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.delete('/api/v1/users/testuser')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.requests.post')
    def test_post_valid_user_should_return_auth_api_response(self, mock_post):
        mock_post.return_value.json.return_value = dict(username="testuser")
        mock_post.return_value.status_code = HTTPStatus.CREATED
        r = self.app.post('/api/v1/users', json=dict(
            username="testuser",
            password="password",
            first_name="test",
            last_name="test",
            contact=dict(
                phone="1545642323",
                email="test@mail.com")
        ))
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("testuser", r.json["username"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.patch')
    def test_patch_valid_format_should_return_auth_api_response(self, mock_patch, mock_session):
        mock_patch.return_value.json.return_value = dict(message="ok")
        mock_patch.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.patch(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'},
            json=dict(op="replace", path="password", value="newpassword"))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("ok", r.json["message"])

    @patch('src.clients.auth_api.requests.post')
    def deprecated_test_post_user_without_username_should_return_bad_request(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/users', json=dict(
            password="password",
            first_name="test",
            last_name="test",
            contact=dict(
                phone="1545642323",
                email="test@mail.com")
        ))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.requests.post')
    def deprecated_test_post_user_without_password_should_return_bad_request(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/users', json=dict(
            username="testuser",
            first_name="test",
            last_name="test",
            contact=dict(
                phone="1545642323",
                email="test@mail.com")
        ))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.requests.post')
    def deprecated_test_post_user_without_email_should_return_bad_request(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/users', json=dict(
            username="testuser",
            password="password",
            first_name="test",
            last_name="test",
            contact=dict(
                phone="1545642323")
        ))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.requests.post')
    def deprecated_test_post_user_with_invalid_email_should_return_bad_request(self, mock_post):
        mock_post.side_effect = Exception("should not call auth api post")
        r = self.app.post('/api/v1/users', json=dict(
            username="testuser",
            password="password",
            first_name="test",
            last_name="test",
            contact=dict(
                phone="1545642323",
                email="noemail")
        ))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.patch')
    def deprecated_test_patch_invalid_format_should_return_bad_request(self, mock_patch, mock_session):
        mock_patch.side_effect = Exception("should not call auth api patch")
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.patch(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'},
            json=dict(password="password"))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.patch')
    def deprecated_test_patch_invalid_op_should_return_bad_request(self, mock_patch, mock_session):
        mock_patch.side_effect = Exception("should not call auth api patch")
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.patch(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'},
            json=dict(op="invalid", path="password", value="newpassword"))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)


if __name__ == '__main__':
    unittest.main()

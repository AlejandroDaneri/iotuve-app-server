import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect


class AdminusersTestCase(unittest.TestCase):

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
        res = self.app.get('/api/v1/adminusers')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/users/adminusers')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.put('/api/v1/users/adminusers')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.patch('/api/v1/users/adminusers')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.delete('/api/v1/users/adminusers')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.get')
    def test_get_adminusers_should_return_auth_api_response(self, mock_delete, mock_session):
        mock_delete.return_value.json.return_value = dict(message="ok")
        mock_delete.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get(
            '/api/v1/adminusers',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("ok", r.json["message"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.get')
    def test_get_adminuser_should_return_auth_api_response(self, mock_delete, mock_session):
        mock_delete.return_value.json.return_value = dict(message="ok")
        mock_delete.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get(
            '/api/v1/adminusers/testuser',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("ok", r.json["message"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.put')
    def test_put_adminuser_should_return_auth_api_response(self, mock_patch, mock_session):
        mock_patch.return_value.json.return_value = dict(message="ok")
        mock_patch.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.put(
            '/api/v1/adminusers/testuser',
            headers={'X-Auth-Token': '123456'},
            json=dict(first_name="test"))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("ok", r.json["message"])

    @patch('src.clients.auth_api.requests.post')
    def test_post_adminuser_should_return_auth_api_response(self, mock_post):
        mock_post.return_value.json.return_value = dict(username="testuser")
        mock_post.return_value.status_code = HTTPStatus.CREATED
        r = self.app.post('/api/v1/adminusers', json=dict(
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
    def test_patch_adminuser_should_return_auth_api_response(self, mock_patch, mock_session):
        mock_patch.return_value.json.return_value = dict(message="ok")
        mock_patch.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.patch(
            '/api/v1/adminusers/testuser',
            headers={'X-Auth-Token': '123456'},
            json={})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("ok", r.json["message"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.auth_api.requests.delete')
    def test_delete_user_should_return_auth_api_response(self, mock_delete, mock_session):
        mock_delete.return_value.json.return_value = dict(message="ok")
        mock_delete.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.delete(
            '/api/v1/adminusers/testuser',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("ok", r.json["message"])


if __name__ == '__main__':
    unittest.main()

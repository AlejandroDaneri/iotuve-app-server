import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect
from tests.test_utils import utils
from src.services.fcm import FCMService, FCMError


class FCMTestCase(unittest.TestCase):

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

    def test_private_enpoints_fcm_without_token_should_return_unauthorized(self):
        res = self.app.post('/api/v1/fcm')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_fcm_token_without_token_should_return_badrequest(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        res = self.app.post('/api/v1/fcm', headers={'X-Auth-Token': '123456'}, json={})
        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_fcm_token_already_exists_token_should_return_alreadyreported(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        utils.save_new_fcm_token("testuser", "token")

        res = self.app.post('/api/v1/fcm', headers={'X-Auth-Token': '123456'}, json={"token": "token"})
        self.assertEqual(HTTPStatus.ALREADY_REPORTED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_fcm_token_should_return_created(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        res = self.app.post('/api/v1/fcm', headers={'X-Auth-Token': '123456'}, json={"token": "token"})
        self.assertEqual(HTTPStatus.CREATED, res.status_code)


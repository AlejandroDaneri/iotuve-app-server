import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect
from tests.test_utils import utils


class FriendRequestsTestCase(unittest.TestCase):

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

    def test_private_enpoints_friendships_without_token_should_return_unauthorized(self):
        res = self.app.post('/api/v1/friendships')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/friendships')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/friendships/1234')
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, res.status_code)
        res = self.app.put('/api/v1/friendships/1234')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.delete('/api/v1/friendships/1234')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_friendship_should_return_created(self, mock_session, mock_user):
        post_json = {
            "to_user": "otheruser",
            "message": "Mensaje de prueba"
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(username="otheruser")
        mock_user.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("Mensaje de prueba", r.json["message"])
        self.assertEqual("otheruser", r.json["to_user"])
        self.assertEqual("testuser", r.json["from_user"])

    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_friendship_empty_message_should_return_created(self, mock_session, mock_user):
        post_json = {
            "to_user": "otheruser",
            "message": ""
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(username="otheruser")
        mock_user.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("", r.json["message"])
        self.assertEqual("otheruser", r.json["to_user"])
        self.assertEqual("testuser", r.json["from_user"])

    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_invalid_friendship_should_return_bad_request(self, mock_session, mock_user):
        post_json = {
            "to_user": "otheruser",
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(username="otheruser")
        mock_user.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertTrue("message" in r.json["message"])

    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_same_friendship_should_return_bad_request(self, mock_session, mock_user):
        post_json = {
            "to_user": "otheruser",
            "message": ""
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(username="otheruser")
        mock_user.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.CREATED, r.status_code)

        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

        post_json["to_user"] = "testuser"
        mock_session.return_value.json.return_value = dict(username="otheruser")
        mock_user.return_value.json.return_value = dict(username="testuser")
        mock_user.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_self_friendship_should_return_bad_request(self, mock_session, mock_user):
        post_json = {
            "to_user": "testuser",
            "message": ""
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(username="testuser")
        mock_user.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_friendship_with_no_existing_to_user_should_return_bad_request(self, mock_session, mock_user):
        post_json = {
            "to_user": "noexists",
            "message": ""
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(message="error")
        mock_user.return_value.status_code = HTTPStatus.NOT_FOUND
        r = self.app.post('/api/v1/friendships',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_pending_friendship_should_return_ok(self, mock_session):
        friendship = utils.save_new_friendship("testuser", "otheruser")
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.delete('/api/v1/friendships/{}'.format(friendship.id),
                            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertIsNone(utils.get_friendship(friendship.id))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_friendship_with_other_user_should_return_forbidden(self, mock_session):
        friendship = utils.save_new_friendship("testuser1", "testuser2")
        mock_session.return_value.json.return_value = dict(username="othertestuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.delete('/api/v1/friendships/{}'.format(friendship.id),
                            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.FORBIDDEN, r.status_code)
        self.assertIsNotNone(utils.get_friendship(friendship.id))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_pending_to_approved_should_return_ok(self, mock_session):
        friendship = utils.save_new_friendship(to_user="testuser", status="pending")
        put_json = {"status": "approved"}
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.put('/api/v1/friendships/{}'.format(friendship.id),
                         headers={'X-Auth-Token': '123456'},
                         json=put_json)
        self.assertEqual(HTTPStatus.OK, r.status_code)
        friendship = utils.get_friendship(friendship.id)
        self.assertEqual(friendship.status, "approved")

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_approved_to_approved_should_return_ok(self, mock_session):
        friendship = utils.save_new_friendship(to_user="testuser", status="approved")
        put_json = {"status": "approved"}
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.put('/api/v1/friendships/{}'.format(friendship.id),
                         headers={'X-Auth-Token': '123456'},
                         json=put_json)
        self.assertEqual(HTTPStatus.OK, r.status_code)
        friendship = utils.get_friendship(friendship.id)
        self.assertEqual(friendship.status, "approved")

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_invalid_status_should_return_bad_request(self, mock_session):
        friendship = utils.save_new_friendship(to_user="testuser", status="approved")
        put_json = {"status": "INVALID"}
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.put('/api/v1/friendships/{}'.format(friendship.id),
                         headers={'X-Auth-Token': '123456'},
                         json=put_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_friendships_paginated(self, mock_session):
        from_user = "testuser"
        for _ in range(0, 10):
            utils.save_new_friendship(from_user, status="pending")
            utils.save_new_friendship(from_user, status="approved")

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/friendships',
                         headers={'X-Auth-Token': '123456'},
                         query_string=dict(from_user=from_user, status="pending", offset=0, limit=20))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(10, len(r.json["data"]))

        r = self.app.get('/api/v1/friendships',
                         headers={'X-Auth-Token': '123456'},
                         query_string=dict(from_user=from_user, status="approved", offset=0, limit=20))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(10, len(r.json["data"]))
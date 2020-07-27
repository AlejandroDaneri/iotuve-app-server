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

    @patch('src.clients.fcm_api.FCMAPIClient.send_message')
    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_friendship_and_fcm_message(self, mock_session, mock_user, mock_fcm):
        post_json = {
            "to_user": "otheruser",
            "message": "Mensaje de prueba"
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(username="otheruser")
        mock_user.return_value.status_code = HTTPStatus.OK
        mock_fcm.return_value.json.return_value = {
            "multicast_id": 3752629586375318742, "success": 1, "failure": 0, "canonical_ids": 0,
            "results": [{"message_id": "0:1595701209097390%50ceb1d450ceb1d4"}]}
        mock_fcm.return_value.status_code = HTTPStatus.OK

        utils.save_new_fcm_token("otheruser", "token")

        r = self.app.post('/api/v1/friendships', headers={'X-Auth-Token': '123456'}, json=post_json)
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("Mensaje de prueba", r.json["message"])
        self.assertEqual("otheruser", r.json["to_user"])
        self.assertEqual("testuser", r.json["from_user"])

    @patch('src.clients.fcm_api.FCMAPIClient.send_message')
    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_friendship_with_admin_user_should_return_forbidden(self, mock_session, mock_user, mock_fcm):
        post_json = {
            "to_user": "otheruser",
            "message": "Mensaje de prueba"
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.side_effect = Exception("should not call user api")
        mock_fcm.side_effect = Exception("should not call fcm api")
        resp = self.app.post('/api/v1/friendships',
                             headers={'X-Auth-Token': '123456', 'X-Admin': 'true'}, json=post_json)
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)

    @patch('src.clients.fcm_api.FCMAPIClient.send_message')
    @patch('src.clients.auth_api.AuthAPIClient.get_user')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_friendship_and_send_fcm_message_error_should_return_created(self, mock_session, mock_user, mock_fcm):
        post_json = {
            "to_user": "otheruser",
            "message": "Mensaje de prueba"
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_user.return_value.json.return_value = dict(username="otheruser")
        mock_user.return_value.status_code = HTTPStatus.OK
        mock_fcm.return_value.json.return_value = {
            "multicast_id": 3752629586375318742, "success": 1, "failure": 0, "canonical_ids": 0,
            "results": [{"message_id": "0:1595701209097390%50ceb1d450ceb1d4"}]}
        mock_fcm.return_value.status_code = HTTPStatus.BAD_REQUEST
        mock_fcm.return_value.text = "Error en los datos"

        utils.save_new_fcm_token("otheruser", "token")

        r = self.app.post('/api/v1/friendships', headers={'X-Auth-Token': '123456'}, json=post_json)
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
    def test_delete_friendship_when_not_exists_should_return_notfound(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser1")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.delete('/api/v1/friendships/{}'.format(utils.get_object_id()),
                            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.NOT_FOUND, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_friendship_invalid_id_should_return_badrequest(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser1")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.delete('/api/v1/friendships/{}'.format(1234),
                            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.fcm_api.FCMAPIClient.send_message')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_pending_to_approved_should_return_ok(self, mock_session, mock_fcm):
        mock_session.return_value.json.return_value = dict(username="to_user")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_fcm.return_value.json.return_value = {
            "multicast_id": 3752629586375318742, "success": 1, "failure": 0, "canonical_ids": 0,
            "results": [{"message_id": "0:1595701209097390%50ceb1d450ceb1d4"}]}
        mock_fcm.return_value.status_code = HTTPStatus.OK

        friendship = utils.save_new_friendship(from_user="from_user", to_user="to_user", status="pending")
        utils.save_new_fcm_token("from_user", "token")

        r = self.app.put('/api/v1/friendships/{}'.format(friendship.id), headers={'X-Auth-Token': '123456'},
                         json={"status": "approved"})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        friendship = utils.get_friendship(friendship.id)
        self.assertEqual(friendship.status, "approved")

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_status_with_other_user_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="othertestuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        friendship = utils.save_new_friendship("testuser1", "testuser2")
        r = self.app.put('/api/v1/friendships/{}'.format(friendship.id), headers={'X-Auth-Token': '123456'},
                         json={"status": "approved"})
        self.assertEqual(HTTPStatus.FORBIDDEN, r.status_code)
        self.assertEqual(friendship.status, "pending")

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_when_not_exists_should_return_notfound(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="to_user")
        mock_session.return_value.status_code = HTTPStatus.OK

        r = self.app.put('/api/v1/friendships/{}'.format(utils.get_object_id()), headers={'X-Auth-Token': '123456'},
                         json={"status": "approved"})
        self.assertEqual(HTTPStatus.NOT_FOUND, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_invalid_data_should_return_badrequest(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="to_user")
        mock_session.return_value.status_code = HTTPStatus.OK
        friendship = utils.save_new_friendship("from_user", "to_user")
        r = self.app.put('/api/v1/friendships/{}'.format(friendship.id), headers={'X-Auth-Token': '123456'},
                         json={"status": "some"})
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_friendship_invalid_id_should_return_badrequest(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="to_user")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.put('/api/v1/friendships/{}'.format("1234"), headers={'X-Auth-Token': '123456'},
                         json={"status": "approved"})
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

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

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_friendship_paginated_wrong_limit_or_offset_should_return_bad_request(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        resp = self.app.get('/api/v1/friendships', headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=5))
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)
        self.assertEqual("{'limit': ['Must be one of: 10, 20, 30, 40, 50.']}", resp.json["message"])

        resp = self.app.get('/api/v1/friendships', headers={'X-Auth-Token': '123456'}, query_string=dict(offset=-2, limit=10))
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)
        self.assertEqual("{'offset': ['Must be greater than or equal to 0.']}", resp.json["message"])


    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_user_friends(self, mock_session):
        username = "testuser"
        for _ in range(0, 10):
            utils.save_new_friendship(from_user=username, status="pending")
            utils.save_new_friendship(from_user=username, status="approved")
            utils.save_new_friendship(to_user=username, status="approved")
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/users/{}/friends'.format(username),
                         headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        friends = r.json["friends"]
        self.assertEqual(20, len(friends))
        friend = friends[0]
        self.assertIsNotNone(friend.get("friendship_id", None))
        self.assertIsNotNone(friend.get("username", None))

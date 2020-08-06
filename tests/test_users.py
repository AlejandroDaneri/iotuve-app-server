import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect
from tests.test_utils import utils


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

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.media_api.MediaAPIClient.get_picture')
    @patch('src.clients.auth_api.requests.get')
    def test_get_users_should_return_auth_api_response_status(self, mock_get, mock_media, mock_session):
        mock_get.return_value.json.return_value = [dict(username="testuser")]
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_media.return_value.json.return_value = dict(user_id="testuser", name="picture", url="http...")
        mock_media.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get(
            '/api/v1/users',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("testuser", r.json[0]['username'])
        self.assertEqual("testuser", r.json[0]["avatar"]["user_id"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.media_api.MediaAPIClient.get_picture')
    @patch('src.clients.auth_api.requests.get')
    def test_get_user_should_return_auth_api_response(self, mock_get, mock_media, mock_session):
        mock_get.return_value.json.return_value = dict(username="testuser")
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_media.return_value.json.return_value = dict(user_id="testuser", name="picture", url="http...")
        mock_media.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("testuser", r.json["username"])
        self.assertEqual("testuser", r.json["avatar"]["user_id"])

    @patch('src.clients.auth_api.requests.post')
    def test_post_user_should_return_auth_api_response(self, mock_post):
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
    @patch('src.clients.media_api.MediaAPIClient.get_picture')
    @patch('src.clients.auth_api.requests.patch')
    def test_patch_user_should_return_auth_api_response(self, mock_patch, mock_media, mock_session):
        mock_patch.return_value.json.return_value = dict(username="testuser")
        mock_patch.return_value.status_code = HTTPStatus.OK
        mock_media.side_effect = Exception("should not call media api")
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.patch(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'},
            json=dict(op="replace", path="password", value="newpassword"))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("testuser", r.json["username"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.media_api.MediaAPIClient.get_picture')
    @patch('src.clients.auth_api.requests.put')
    def test_put_user_should_return_auth_api_response(self, mock_put, mock_media, mock_session):
        mock_put.return_value.json.return_value = dict(username="testuser")
        mock_put.return_value.status_code = HTTPStatus.OK
        mock_media.return_value.json.return_value = dict(user_id="testuser", name="picture", url="http...")
        mock_media.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.put(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'},
            json=dict(first_name="test"))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("testuser", r.json["username"])
        self.assertEqual("testuser", r.json["avatar"]["user_id"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.media_api.MediaAPIClient.delete_picture')
    @patch('src.clients.auth_api.requests.delete')
    def test_delete_user_should_return_auth_api_response(self, mock_delete, mock_media, mock_session):
        mock_media.return_value.json.return_value = dict(message="ok")
        mock_media.return_value.status_code = HTTPStatus.OK
        mock_delete.return_value.json.return_value = dict(message="ok")
        mock_delete.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.delete(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("ok", r.json["message"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.media_api.MediaAPIClient.get_picture')
    @patch('src.clients.auth_api.requests.get')
    def test_get_user_should_return_auth_api_statistics(self, mock_get, mock_media, mock_session):
        mock_get.return_value.json.return_value = dict(username="testuser")
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_media.return_value.json.return_value = dict(user_id="testuser", name="picture", url="http...")
        mock_media.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("testuser", r.json["username"])
        self.assertEqual("testuser", r.json["avatar"]["user_id"])
        self.assertEqual(dict(likes=0, dislikes=0, views=0, uploaded=0, friends=0), r.json["statistics"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    @patch('src.clients.media_api.MediaAPIClient.get_picture')
    @patch('src.clients.auth_api.requests.get')
    def test_get_user_should_return_auth_api_statistics_with_data(self, mock_get, mock_media, mock_session):
        mock_get.return_value.json.return_value = dict(username="testuser")
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_media.return_value.json.return_value = dict(user_id="testuser", name="picture", url="http...")
        mock_media.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        video1 = utils.save_new_video()
        video2 = utils.save_new_video()
        video3 = utils.save_new_video()
        video4 = utils.save_new_video()

        utils.save_new_friendship(from_user="testuser", to_user="otheruser1", status="approved")
        utils.save_new_friendship(from_user="otheruser2", to_user="testuser", status="approved")
        utils.save_new_friendship(from_user="testuser", to_user="otheruser3", status="approved")

        utils.save_new_video_like(video=video1.id, user="otheruser1")
        utils.save_new_video_like(video=video2.id, user="otheruser1")
        utils.save_new_video_like(video=video3.id, user="otheruser1")

        utils.save_new_video_dislike(video=video3.id, user="otheruser1")
        utils.save_new_video_dislike(video=video4.id, user="otheruser1")

        utils.save_new_video_view(video=video2.id, user="otheruser1")

        r = self.app.get(
            '/api/v1/users/testuser',
            headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual("testuser", r.json["username"])
        self.assertEqual("testuser", r.json["avatar"]["user_id"])
        self.assertEqual(dict(likes=3, dislikes=2, views=1, uploaded=4, friends=3), r.json["statistics"])



if __name__ == '__main__':
    unittest.main()

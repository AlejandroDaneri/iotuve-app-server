import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect
from tests.test_utils import utils


class LikesTestCase(unittest.TestCase):

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

    def test_private_enpoints_likes_without_token_should_return_unauthorized(self):
        res = self.app.get('/api/v1/videos/1234/likes')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/videos/1234/likes/me')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.post('/api/v1/videos/1234/likes/me')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.delete('/api/v1/videos/1234/likes/me')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_video_like_should_return_ok(self, mock_session):
        video = utils.save_new_video()
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        resp = self.app.post('/api/v1/videos/%s/likes/me' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("Like saved", resp.json["message"])
        self.assertEqual(1, video.reload().count_likes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_duplicated_video_like_should_return_bad_request(self, mock_session):
        like = utils.save_new_video_like(user="testuser")
        self.assertEqual(1, like.video.fetch().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        resp = self.app.post('/api/v1/videos/%s/likes/me' % like.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)
        self.assertEqual("Already liked", resp.json["message"])
        self.assertEqual(1, like.video.fetch().reload().count_likes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_new_valid_video_like_should_return_ok(self, mock_session):
        like = utils.save_new_video_like(user="testuser")
        self.assertEqual(1, like.video.fetch().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        resp = self.app.delete('/api/v1/videos/%s/likes/me' % like.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual("Like deleted", resp.json["message"])
        self.assertEqual(0, like.video.fetch().reload().count_likes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_video_like_should_return_ok(self, mock_session):
        like = utils.save_new_video_like(user="testuser")
        self.assertEqual(1, like.video.fetch().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        resp = self.app.get('/api/v1/videos/%s/likes/me' % like.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual("testuser", resp.json["user"])
        self.assertEqual(str(like.video.id), resp.json["video"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_video_likes_paginated(self, mock_session):
        video = utils.save_new_video()
        for _ in range(0, 25):
            utils.save_new_video_like(user="testuser", video=video.id)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        resp = self.app.get('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(10, len(resp.json["data"]))

        resp = self.app.get('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=50))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(25, len(resp.json["data"]))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_and_delete_video_like_should_increment_decrement_count_likes(self, mock_session):
        video = utils.save_new_video()

        mock_session.return_value.json.return_value = dict(username="testuser1")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.post('/api/v1/videos/%s/likes/me' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(1, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser2")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.post('/api/v1/videos/%s/likes/me' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(2, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser3")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.post('/api/v1/videos/%s/likes/me' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(3, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser2")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.delete('/api/v1/videos/%s/likes/me' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(2, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser3")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.delete('/api/v1/videos/%s/likes/me' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(1, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser1")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.delete('/api/v1/videos/%s/likes/me' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(0, video.reload().count_likes)

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

    def test_private_enpoints_reactions_without_token_should_return_unauthorized(self):
        for reaction in ('likes', 'dislikes', 'views'):
            res = self.app.get('/api/v1/videos/1234/%s' % reaction)
            self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
            res = self.app.post('/api/v1/videos/1234/%s' % reaction)
            self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
            res = self.app.delete('/api/v1/videos/1234/%s' % reaction)
            self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_video_reaction_should_return_ok(self, mock_session, mock_media):
        video = utils.save_new_video()
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        url = "https://storage.googleapis.com/chotuve-grupo8.appspot.com/uploads/videos/.."
        mock_media.return_value.json.return_value = dict(name="testmedia", video_id="123456",
                                                         date_created='2020-05-30T02:36:53.074000',
                                                         url=url, thumb=url, size=3215421, type="video/mp4")
        mock_media.return_value.status_code = HTTPStatus.OK

        resp = self.app.get('/api/v1/videos/%s' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(False, resp.json["user_like"])
        self.assertEqual(False, resp.json["user_dislike"])
        self.assertEqual(False, resp.json["user_view"])

        resp = self.app.post('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("Like saved", resp.json["message"])
        self.assertEqual(1, video.reload().count_likes)

        resp = self.app.post('/api/v1/videos/%s/dislikes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("Dislike saved", resp.json["message"])
        self.assertEqual(1, video.reload().count_dislikes)

        resp = self.app.post('/api/v1/videos/%s/views' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("View saved", resp.json["message"])

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_video_reaction_should_return_ok(self, mock_session, mock_media):
        video = utils.save_new_video()
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        url = "https://storage.googleapis.com/chotuve-grupo8.appspot.com/uploads/videos/.."
        mock_media.return_value.json.return_value = dict(name="testmedia", video_id="123456",
                                                         date_created='2020-05-30T02:36:53.074000',
                                                         url=url, thumb=url, size=3215421, type="video/mp4")
        mock_media.return_value.status_code = HTTPStatus.OK

        resp = self.app.get('/api/v1/videos/%s' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(False, resp.json["user_like"])
        self.assertEqual(False, resp.json["user_dislike"])
        self.assertEqual(False, resp.json["user_view"])

        resp = self.app.post('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("Like saved", resp.json["message"])
        self.assertEqual(1, video.reload().count_likes)

        resp = self.app.post('/api/v1/videos/%s/dislikes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("Dislike saved", resp.json["message"])
        self.assertEqual(1, video.reload().count_dislikes)

        resp = self.app.post('/api/v1/videos/%s/views' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("View saved", resp.json["message"])
        self.assertEqual(1, video.reload().count_views)

        resp = self.app.get('/api/v1/videos/%s' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(True, resp.json["user_like"])
        self.assertEqual(True, resp.json["user_dislike"])
        self.assertEqual(True, resp.json["user_view"])
        self.assertEqual(1, video.reload().count_views)

        resp = self.app.get('/api/v1/videos/%s' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(True, resp.json["user_like"])
        self.assertEqual(True, resp.json["user_dislike"])
        self.assertEqual(True, resp.json["user_view"])

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_video_reaction_with_admin_user_should_return_forbidden(self, mock_session, mock_media):
        video = utils.save_new_video()
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        url = "https://storage.googleapis.com/chotuve-grupo8.appspot.com/uploads/videos/.."
        mock_media.return_value.json.return_value = dict(name="testmedia", video_id="123456",
                                                         date_created='2020-05-30T02:36:53.074000',
                                                         url=url, thumb=url, size=3215421, type="video/mp4")
        mock_media.return_value.status_code = HTTPStatus.OK

        resp = self.app.post('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456', 'X-Admin': 'true'})
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)
        self.assertEqual("Admin users can't react to videos", resp.json["message"])

        resp = self.app.post('/api/v1/videos/%s/dislikes' % video.id, headers={'X-Auth-Token': '123456', 'X-Admin': 'true'})
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)
        self.assertEqual("Admin users can't react to videos", resp.json["message"])

        resp = self.app.post('/api/v1/videos/%s/views' % video.id, headers={'X-Auth-Token': '123456', 'X-Admin': 'true'})
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)
        self.assertEqual("Admin users can't react to videos", resp.json["message"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_duplicated_video_like_should_return_bad_request(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        like = utils.save_new_video_like(user="testuser")
        self.assertEqual(1, like.video.fetch().count_likes)
        resp = self.app.post('/api/v1/videos/%s/likes' % like.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)
        self.assertEqual("Like already exists", resp.json["message"])
        self.assertEqual(1, like.video.fetch().reload().count_likes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_duplicated_video_dislike_should_return_bad_request(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        dislike = utils.save_new_video_dislike(user="testuser")
        self.assertEqual(1, dislike.video.fetch().count_dislikes)
        resp = self.app.post('/api/v1/videos/%s/dislikes' % dislike.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)
        self.assertEqual("Dislike already exists", resp.json["message"])
        self.assertEqual(1, dislike.video.fetch().reload().count_dislikes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_duplicated_video_view_should_return_created(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        view = utils.save_new_video_view(user="testuser")
        self.assertEqual(1, view.video.fetch().count_views)
        resp = self.app.post('/api/v1/videos/%s/views' % view.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual("View saved", resp.json["message"])
        self.assertEqual(2, view.video.fetch().reload().count_views)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_new_valid_video_reaction_like_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        like = utils.save_new_video_like(user="testuser")
        self.assertEqual(1, like.video.fetch().count_likes)
        resp = self.app.delete('/api/v1/videos/%s/likes' % like.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual("Like deleted", resp.json["message"])
        self.assertEqual(0, like.video.fetch().reload().count_likes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_new_valid_video_reaction_like_with_admin_user_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        like = utils.save_new_video_like(user="testuser")
        self.assertEqual(1, like.video.fetch().count_likes)
        resp = self.app.delete('/api/v1/videos/%s/likes' % like.video.id,
                               headers={'X-Auth-Token': '123456', 'X-Admin': 'true'})
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_new_valid_video_reaction_dislike_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        dislike = utils.save_new_video_dislike(user="testuser")
        self.assertEqual(1, dislike.video.fetch().count_dislikes)
        resp = self.app.delete('/api/v1/videos/%s/dislikes' % dislike.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual("Dislike deleted", resp.json["message"])
        self.assertEqual(0, dislike.video.fetch().reload().count_dislikes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_new_valid_video_reaction_dislike_with_admin_user_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        dislike = utils.save_new_video_dislike(user="testuser")
        self.assertEqual(1, dislike.video.fetch().count_dislikes)
        resp = self.app.delete('/api/v1/videos/%s/dislikes' % dislike.video.id,
                               headers={'X-Auth-Token': '123456', 'X-Admin': 'true'})
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_video_view_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        view = utils.save_new_video_view(user="testuser")
        self.assertEqual(1, view.video.fetch().count_views)
        resp = self.app.delete('/api/v1/videos/%s/views' % view.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)
        self.assertEqual("Cant remove a view", resp.json["message"])
        self.assertEqual(1, view.video.fetch().reload().count_views)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_video_reactions_paginated(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        video = utils.save_new_video()
        for _ in range(0, 25):
            utils.save_new_video_like(user="testuser", video=video.id)
            utils.save_new_video_dislike(user="testuser", video=video.id)
            utils.save_new_video_view(user="testuser", video=video.id)

        resp = self.app.get('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(10, len(resp.json["data"]))
        resp = self.app.get('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=50))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(25, len(resp.json["data"]))

        resp = self.app.get('/api/v1/videos/%s/dislikes' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(10, len(resp.json["data"]))
        resp = self.app.get('/api/v1/videos/%s/dislikes' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=50))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(25, len(resp.json["data"]))

        resp = self.app.get('/api/v1/videos/%s/views' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(10, len(resp.json["data"]))
        resp = self.app.get('/api/v1/videos/%s/views' % video.id, headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=50))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(25, len(resp.json["data"]))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_and_delete_video_like_should_increment_decrement_count_likes(self, mock_session):
        video = utils.save_new_video()

        mock_session.return_value.json.return_value = dict(username="testuser1")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.post('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(1, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser2")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.post('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(2, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser3")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.post('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(3, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser2")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.delete('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(2, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser3")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.delete('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(1, video.reload().count_likes)

        mock_session.return_value.json.return_value = dict(username="testuser1")
        mock_session.return_value.status_code = HTTPStatus.OK
        self.app.delete('/api/v1/videos/%s/likes' % video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(0, video.reload().count_likes)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_video_like_when_not_exists_should_return_not_found(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        resp = self.app.delete('/api/v1/videos/%s/likes' % utils.get_object_id(), headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.NOT_FOUND, resp.status_code)
        self.assertEqual("Video not found", resp.json["message"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_video_like_when_video_not_exists_should_return_not_found(self, mock_session):
        like = utils.save_new_video_like(user="testuser")
        self.assertEqual(1, like.video.fetch().count_likes)

        like.video.fetch().delete()

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        resp = self.app.delete('/api/v1/videos/%s/likes' % like.video.id, headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.NOT_FOUND, resp.status_code)
        self.assertEqual("Video not found", resp.json["message"])

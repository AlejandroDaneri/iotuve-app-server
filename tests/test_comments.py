import unittest
import app_server
from bson import ObjectId
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect
from tests.test_utils import utils


class CommentsTestCase(unittest.TestCase):

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

    def test_private_enpoints_comments_without_token_should_return_unauthorized(self):
        res = self.app.post('/api/v1/comments')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/comments')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/comments/1234')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.delete('/api/v1/comments/1234')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_comment_should_return_created(self, mock_session):
        parent = utils.save_new_comment()
        post_json = {
            "content": "Comentario de prueba",
            "video": str(parent.video.id)
        }
        mock_session.return_value.json.return_value = dict(username="testusercomment")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/comments',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("Comentario de prueba", r.json["content"])
        self.assertEqual(str(parent.video.id), r.json["video"])
        self.assertEqual(None, r.json["parent"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_comment_with_parent_should_return_created(self, mock_session):
        parent = utils.save_new_comment()
        post_json = {
            "content": "Comentario de prueba",
            "video": str(parent.video.id),
            "parent": str(parent.id)
        }
        mock_session.return_value.json.return_value = dict(username="testusercomment")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/comments',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.CREATED, r.status_code)
        self.assertEqual("Comentario de prueba", r.json["content"])
        self.assertEqual(str(parent.video.id), r.json["video"])
        self.assertEqual(str(parent.id), r.json["parent"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_invalid_comment_should_return_bad_request(self, mock_session):
        post_json = {
            "content": "",
            "video": str(utils.save_new_video().id)
        }
        mock_session.return_value.json.return_value = dict(username="testusercomment")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/comments',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_comment_no_existing_video_should_return_not_found(self, mock_session):
        post_json = {
            "content": "Comentario de prueba",
            "video": str(ObjectId())
        }
        mock_session.return_value.json.return_value = dict(username="testusercomment")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/comments',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.NOT_FOUND, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_comment_with_parent_in_another_video_should_return_not_found(self, mock_session):
        parent = utils.save_new_comment()
        post_json = {
            "content": "Comentario de prueba",
            "video": str(utils.save_new_video().id),
            "parent": str(parent.id)
        }
        mock_session.return_value.json.return_value = dict(username="testusercomment")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/comments',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.NOT_FOUND, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_comment_with_no_existing_parent_should_return_not_found(self, mock_session):
        video = utils.save_new_video()
        post_json = {
            "content": "Comentario de prueba",
            "video": str(video.id),
            "parent": str(ObjectId())
        }
        mock_session.return_value.json.return_value = dict(username="testusercomment")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/comments',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.NOT_FOUND, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_comment_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        comment = utils.save_new_comment()
        self.assertIsNotNone(utils.get_comment(comment.id))
        res_del = self.app.delete('/api/v1/comments/{}'.format(comment.id),
                                  headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, res_del.status_code)
        self.assertEqual("Comment deleted", res_del.json["message"])
        self.assertIsNone(utils.get_comment(comment.id))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_comment_not_owner_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="otheruser")
        mock_session.return_value.status_code = HTTPStatus.OK
        comment = utils.save_new_comment()
        self.assertIsNotNone(utils.get_comment(comment.id))
        res_del = self.app.delete('/api/v1/comments/{}'.format(comment.id),
                                  headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.FORBIDDEN, res_del.status_code)
        self.assertIsNotNone(utils.get_comment(comment.id))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_comment_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        comment = utils.save_new_comment()
        res_get = self.app.get('/api/v1/comments/{}'.format(comment.id),
                               headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, res_get.status_code)
        self.assertEqual(str(comment.id), res_get.json["id"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_comments_no_filter(self, mock_session):
        utils.delete_all()
        video = utils.save_new_video()
        utils.save_new_comment(video.id)
        utils.save_new_comment(video.id)
        utils.save_new_comment(video.id)
        video = utils.save_new_video()
        utils.save_new_comment(video.id)
        utils.save_new_comment(video.id)
        utils.save_new_comment(video.id)
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/comments',
                         headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(6, len(r.json["data"]))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_comments_filter_video(self, mock_session):
        video = utils.save_new_video()
        utils.save_new_comment(video.id)
        utils.save_new_comment(video.id)
        utils.save_new_comment(video.id)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/comments',
                         headers={'X-Auth-Token': '123456'},
                         query_string=dict(video=video.id))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(3, len(r.json["data"]))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_comments_filter_parent(self, mock_session):
        video = utils.save_new_video()
        parent = utils.save_new_comment(video.id)
        utils.save_new_comment(video.id, parent.id)
        utils.save_new_comment(video.id, parent.id)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/comments',
                         headers={'X-Auth-Token': '123456'},
                         query_string=dict(parent=parent.id))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(2, len(r.json["data"]))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_comments_paginated(self, mock_session):
        video = utils.save_new_video()
        for _ in range(1, 25):
            utils.save_new_comment(video.id)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/comments',
                         headers={'X-Auth-Token': '123456'},
                         query_string=dict(video=video.id, offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(10, len(r.json["data"]))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_comments_paginated_error(self, mock_session):
        video = utils.save_new_video()
        for _ in range(1, 25):
            utils.save_new_comment(video.id)

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/comments',
                         headers={'X-Auth-Token': '123456'},
                         query_string=dict(video=video.id, offset=0, limit=1))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

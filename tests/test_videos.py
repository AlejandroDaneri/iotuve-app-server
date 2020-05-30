import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect
from tests.test_utils import utils


class VideosTestCase(unittest.TestCase):

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

    def test_private_enpoints_videos_without_token_should_return_unauthorized(self):
        res = self.app.get('/api/v1/videos')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.get('/api/v1/videos/1234')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.put('/api/v1/videos/1234')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)
        res = self.app.delete('/api/v1/videos/1234')
        self.assertEqual(HTTPStatus.UNAUTHORIZED, res.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_video_should_return_ok(self, mock_session):
        post_json = {
            "title": "Un titulo",
            "description": "Una descripcion",
            "visibility": "public",
            "media": {
                "url": "https://una.url.io/mediafield"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/videos',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.CREATED, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_invalid_video_should_return_bad_request(self, mock_session):
        post_json = {
            "visibility": "public",
            "media": {
                "url": "INVALID"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.post('/api/v1/videos',
                          headers={'X-Auth-Token': '123456'},
                          json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_valid_video_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        put_json = {
            "title": "Otro titulo",
            "description": "Una descripcion",
            "visibility": "public",
            "media": {
                "url": "https://una.url.io/mediafield"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        res_put = self.app.put('/api/v1/videos/{}'.format(video.id),
                               headers={'X-Auth-Token': '123456'},
                               json=put_json)
        self.assertEqual(HTTPStatus.OK, res_put.status_code)
        self.assertEqual(str(video.id), res_put.json["id"])
        self.assertEqual(video.media["url"], res_put.json["media"]["url"])
        self.assertEqual("Otro titulo", res_put.json["title"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_invalid_video_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        put_json = {
            "media": {
                "url": "https://una.url.io/mediafield"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        res_put = self.app.put('/api/v1/videos/{}'.format(video.id),
                               headers={'X-Auth-Token': '123456'},
                               json=put_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, res_put.status_code)
        self.assertTrue("visibility" in res_put.json["message"])


    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_video_with_other_user_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="othertestuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        put_json = {
            "title": "Otro titulo",
            "description": "Una descripcion",
            "visibility": "public",
            "media": {
                "url": "https://una.url.io/mediafield"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        res_put = self.app.put('/api/v1/videos/{}'.format(video.id),
                               headers={'X-Auth-Token': '123456'},
                               json=put_json)
        self.assertEqual(HTTPStatus.FORBIDDEN, res_put.status_code)

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_video_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        res_get = self.app.get('/api/v1/videos/{}'.format(video.id),
                               headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, res_get.status_code)
        self.assertEqual(str(video.id), res_get.json["id"])

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_video_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        self.assertIsNotNone(utils.get_video(video.id))
        res_del = self.app.delete('/api/v1/videos/{}'.format(video.id),
                                  headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, res_del.status_code)
        self.assertEqual("Video deleted", res_del.json["message"])
        self.assertIsNone(utils.get_video(video.id))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_video_not_owner_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="otheruser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        self.assertIsNotNone(utils.get_video(video.id))
        res_del = self.app.delete('/api/v1/videos/{}'.format(video.id),
                                  headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.FORBIDDEN, res_del.status_code)
        self.assertIsNotNone(utils.get_video(video.id))

    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_videos_paginated(self, mock_session):
        for _ in range(1, 25):
            utils.save_new_video()

        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        r = self.app.get('/api/v1/videos',
                         headers={'X-Auth-Token': '123456'},
                         query_string=dict(offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertEqual(10, len(r.json["data"]))

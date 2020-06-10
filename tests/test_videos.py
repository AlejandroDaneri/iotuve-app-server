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

    @patch('src.clients.media_api.MediaAPIClient.post_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_valid_video_should_return_ok(self, mock_session, mock_media):
        post_json = {
            'title': 'Un titulo',
            'description': 'Una descripcion',
            'visibility': 'public',
            'media': {
                'name': 'mediafile',
                'date_created': '2020-05-30T02:36:53.074000',
                'size': 3215421,
                'type': 'video/mp4'
            },
            'location': {
                'latitude': 1212121.232323,
                'longitude': 1212121.232323
            }
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        url = "https://storage.googleapis.com/chotuve-grupo8.appspot.com/uploads/videos/.."
        mock_media.return_value.json.return_value = dict(name="mediafile", video_id="1234", date_created="2020-05-01",
                                                         url=url, thumb=url, size=3215421, type="video/mp4")
        mock_media.return_value.status_code = HTTPStatus.CREATED

        resp = self.app.post('/api/v1/videos', headers={'X-Auth-Token': '123456'}, json=post_json)
        self.assertEqual(HTTPStatus.CREATED, resp.status_code)
        self.assertEqual(url, resp.json["media"]["url"])

    @patch('src.clients.media_api.MediaAPIClient.post_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_media_server_error_on_post_video_should_return_server_error(self, mock_session, mock_media):
        post_json = {
            "title": "Un titulo",
            "description": "Una descripcion",
            "visibility": "public",
            "media": {
                "name": "mediafile",
                "date_created": "2020-05-30T02:36:53.074000",
                "size": 3215421,
                "type": "video/mp4"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        mock_media.return_value.json.return_value = dict(code=-1, message="ups!")
        mock_media.return_value.status_code = HTTPStatus.BAD_REQUEST

        resp = self.app.post('/api/v1/videos', headers={'X-Auth-Token': '123456'}, json=post_json)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, resp.status_code)

    @patch('src.clients.media_api.MediaAPIClient.post_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_post_new_invalid_video_should_return_bad_request(self, mock_session, mock_media):
        mock_media.side_effect = Exception("should not call media api")
        post_json = {
            'title': 'Un titulo',
            'description': 'Una descripcion',
            'visibility': 'public',
            'media': {
                'name': 'mediafile',
                'date_created': '2020-05-30T02:36:53.074000',
                'size': 3215421,
                'type': 'video/mp4'
            },
            'location': {
                'longitude': 1212121.232323
            }
        }
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        resp = self.app.post('/api/v1/videos', headers={'X-Auth-Token': '123456'}, json=post_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_valid_video_should_return_ok(self, mock_session, mock_media):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        put_json = {
            'title': 'Otro titulo',
            'description': 'Otra descripcion',
            'visibility': 'public',
            'media': {
                'name': 'mediafile',
                'date_created': '2020-05-30T02:36:53.074000',
                'size': 3215421,
                'type': 'video/mp4'
            },
            'location': {
                'latitude': 1212121.232323,
                'longitude': 1212121.232323
            }
        }

        url = "https://storage.googleapis.com/chotuve-grupo8.appspot.com/uploads/videos/.."
        mock_media.return_value.json.return_value = dict(name="mediafile", video_id=str(video.id),
                                                         date_created='2020-05-30T02:36:53.074000',
                                                         url=url, thumb=url, size=3215421, type="video/mp4")
        mock_media.return_value.status_code = HTTPStatus.OK

        resp = self.app.put('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'}, json=put_json)
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(str(video.id), resp.json["id"])
        self.assertEqual('mediafile', resp.json["media"]["name"])
        self.assertEqual('Otro titulo', resp.json["title"])

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_media_server_error_on_put_video_should_return_server_error(self, mock_session, mock_media):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        put_json = {
            'title': 'Un titulo',
            'description': 'Una descripcion',
            'visibility': 'public',
            'media': {
                'name': 'mediafile',
                'date_created': '2020-05-30T02:36:53.074000',
                'size': 3215421,
                'type': 'video/mp4'
            },
            'location': {
                'latitude': 1212121.232323,
                'longitude': 1212121.232323
            }
        }

        mock_media.return_value.json.return_value = dict(code=-1, message="ups!")
        mock_media.return_value.status_code = HTTPStatus.BAD_REQUEST

        resp = self.app.put('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'}, json=put_json)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, resp.status_code)

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_invalid_video_should_return_ok(self, mock_session, mock_media):
        mock_media.side_effect = Exception("should not call media api")
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        put_json = {
            "media": {
                "name": "mediafile"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        resp = self.app.put('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'}, json=put_json)
        self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status_code)
        self.assertTrue("visibility" in resp.json["message"])

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_put_video_with_other_user_should_return_forbidden(self, mock_session, mock_media):
        mock_media.side_effect = Exception("should not call media api")
        mock_session.return_value.json.return_value = dict(username="othertestuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        put_json = {
            "title": "Otro titulo",
            "description": "Una descripcion",
            "visibility": "public",
            "media": {
                "name": "mediafile"
            },
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        resp = self.app.put('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'}, json=put_json)
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_video_should_return_ok(self, mock_session, mock_media):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        video = utils.save_new_video()

        url = "https://storage.googleapis.com/chotuve-grupo8.appspot.com/uploads/videos/.."
        mock_media.return_value.json.return_value = dict(name="testmedia", video_id=str(video.id),
                                                         date_created=video.date_created, url=url, thumb=url,
                                                         size=3215421, type="video/mp4")
        mock_media.return_value.status_code = HTTPStatus.OK

        resp = self.app.get('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(str(video.id), resp.json["id"])
        self.assertEqual(url, resp.json["media"]["url"])

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_media_server_error_on_get_video_should_return_server_error(self, mock_session, mock_media):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK

        video = utils.save_new_video()

        mock_media.return_value.json.return_value = dict(code=-1, message="ups!")
        mock_media.return_value.status_code = HTTPStatus.BAD_REQUEST

        resp = self.app.get('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, resp.status_code)

    @patch('src.clients.media_api.MediaAPIClient.delete_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_video_should_return_ok(self, mock_session, mock_media):
        mock_media.return_value.status_code = HTTPStatus.OK
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        self.assertIsNotNone(utils.get_video(video.id))
        resp = self.app.delete('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual("Video deleted", resp.json["message"])
        self.assertIsNone(utils.get_video(video.id))

    @patch('src.clients.media_api.MediaAPIClient.delete_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_media_server_error_on_delete_video_should_return_server_error(self, mock_session, mock_media):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        self.assertIsNotNone(utils.get_video(video.id))

        mock_media.return_value.json.return_value = dict(code=-1, message="ups!")
        mock_media.return_value.status_code = HTTPStatus.BAD_REQUEST

        resp = self.app.delete('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, resp.status_code)

    @patch('src.clients.media_api.MediaAPIClient.delete_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_delete_video_not_owner_should_return_forbidden(self, mock_session, mock_media):
        mock_media.side_effect = Exception("should not call media api")
        mock_session.return_value.json.return_value = dict(username="otheruser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = utils.save_new_video()
        self.assertIsNotNone(utils.get_video(video.id))
        resp = self.app.delete('/api/v1/videos/{}'.format(video.id), headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.FORBIDDEN, resp.status_code)
        self.assertIsNotNone(utils.get_video(video.id))

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_get_videos_paginated(self, mock_session, mock_media):
        for _ in range(0, 25):
            utils.save_new_video()
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        url = "https://storage.googleapis.com/chotuve-grupo8.appspot.com/uploads/videos/.."
        mock_media.return_value.json.return_value = dict(name="testmedia", video_id="123456",
                                                         date_created='2020-05-30T02:36:53.074000',
                                                         url=url, thumb=url, size=3215421, type="video/mp4")
        mock_media.return_value.status_code = HTTPStatus.OK
        resp = self.app.get('/api/v1/videos', headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(10, len(resp.json["data"]))

        resp = self.app.get('/api/v1/videos', headers={'X-Auth-Token': '123456'},
                            query_string=dict(offset=0, limit=50, user='testuser'))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(25, len(resp.json["data"]))

        resp = self.app.get('/api/v1/videos', headers={'X-Auth-Token': '123456'},
                            query_string=dict(offset=0, limit=50, user='otheruser'))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(0, len(resp.json["data"]))

    @patch('src.clients.media_api.MediaAPIClient.get_video')
    @patch('src.clients.auth_api.AuthAPIClient.get_session')
    def test_media_server_error_on_get_videos_should_not_return_server_error(self, mock_session, mock_media):
        for _ in range(1, 25):
            utils.save_new_video()
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        mock_media.return_value.json.return_value = dict(code=-1, message="ups!")
        mock_media.return_value.status_code = HTTPStatus.BAD_REQUEST
        resp = self.app.get('/api/v1/videos', headers={'X-Auth-Token': '123456'}, query_string=dict(offset=0, limit=10))
        self.assertEqual(HTTPStatus.OK, resp.status_code)
        self.assertEqual(0, len(resp.json["data"]))

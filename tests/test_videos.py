import datetime
import unittest
import app_server
from unittest.mock import patch
from http import HTTPStatus
from mongoengine import connect, disconnect
from src.schemas.video import VideoSchema


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

    @classmethod
    def save_new_video(cls):
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
        schema = VideoSchema()
        new_video = schema.load(post_json)
        now = datetime.datetime.utcnow()
        new_video.user = "testuser"
        new_video.date_created = now
        new_video.date_updated = now
        new_video.save()
        return new_video

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
    def test_put_valid_video_should_return_ok(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="testuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = self.save_new_video()
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
    def test_put_video_with_other_user_should_return_forbidden(self, mock_session):
        mock_session.return_value.json.return_value = dict(username="othertestuser")
        mock_session.return_value.status_code = HTTPStatus.OK
        video = self.save_new_video()
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
        video = self.save_new_video()
        res_put = self.app.get('/api/v1/videos/{}'.format(video.id),
                               headers={'X-Auth-Token': '123456'})
        self.assertEqual(HTTPStatus.OK, res_put.status_code)
        self.assertEqual(str(video.id), res_put.json["id"])



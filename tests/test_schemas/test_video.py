import unittest
from marshmallow.exceptions import ValidationError
from src.schemas.video import VideoSchema, MediaSchema


class SchemaVideoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_load_valid_video_should_return_ok(self):
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
        new_post = VideoSchema()
        new_post.load(post_json)

    def test_load_post_without_optional_fields_should_return_ok(self):
        post_json = {
            'visibility': 'public'
        }
        schema = VideoSchema()
        loaded = schema.load(post_json)
        dumped = schema.dump(loaded)
        self.assertEqual(dumped['title'], None)
        self.assertEqual(dumped['description'], None)
        self.assertEqual(dumped['user'], None)
        self.assertEqual(dumped['visibility'], "public")
        self.assertEqual(dumped['statistics'], {'dislikes': {'count': 0, 'users': []},
                                                'likes': {'count': 0, 'users': []},
                                                'views': {'count': 0, 'users': []}})

    def test_load_valid_media_should_return_ok(self):
        post_json = {
            'name': 'mediafile',
            'date_created': '2020-05-30T02:36:53.074000',
            'size': 3215421,
            'type': 'video/mp4'
        }
        schema = MediaSchema()
        loaded = schema.load(post_json)
        dumped = schema.dump(loaded)
        self.assertEqual(dumped["name"], "mediafile")

    def test_load_invalid_media_should_return_error(self):
        post_json = {}
        new_post = MediaSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)



import unittest
from marshmallow.exceptions import ValidationError
from src.schemas.video import VideoSchema


class SchemaVideoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_load_valid_video_should_return_ok(self):
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
        new_post = VideoSchema()
        new_post.load(post_json)

    def test_load_post_without_optional_fields_should_return_ok(self):
        post_json = {
            "visibility": "public",
            "media": {
                "url": "https://una.url.io/mediafield"
            }
        }
        schema = VideoSchema()
        loaded = schema.load(post_json)
        dumped = schema.dump(loaded)
        self.assertEqual(dumped['title'], None)
        self.assertEqual(dumped['description'], None)
        self.assertEqual(dumped['comments'], None)
        self.assertEqual(dumped['user'], None)
        self.assertEqual(dumped['visibility'], "public")
        self.assertEqual(dumped['media']['url'], "https://una.url.io/mediafield")

    def test_load_post_without_media_should_return_error(self):
        post_json = {
            "title": "Un titulo",
            "description": "Una descripcion",
            "visibility": "public",
            "location": {
                "latitude": 1212121.232323,
                "longitude": 1212121.232323
            }
        }
        new_post = VideoSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)



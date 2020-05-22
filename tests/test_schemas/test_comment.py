import unittest
from bson import ObjectId
from marshmallow.exceptions import ValidationError
from src.schemas.comment import CommentSchema, CommentPaginatedSchema


class SchemaCommentTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_load_valid_comment_should_return_ok(self):
        post_json = {
            "content": "Hola este es un comentario de prueba",
            "video": str(ObjectId())
        }
        new_post = CommentSchema()
        new_post.load(post_json)

    def test_load_comment_without_content_should_return_error(self):
        post_json = {
            "video": str(ObjectId())
        }
        new_post = CommentSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)
        post_json = {
            "content": "",
            "video": str(ObjectId())
        }
        new_post = CommentSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)

    def test_load_comment_without_video_should_return_error(self):
        post_json = {
            "content": "Hola este es un comentario de prueba"
        }
        new_post = CommentSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)

        post_json = {
            "content": "Hola este es un comentario de prueba",
            "video": ""
        }
        new_post = CommentSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)

    def test_load_valid_paginated_empty_comment_should_return_ok(self):
        post_json = {}
        new_post = CommentPaginatedSchema()
        result = new_post.load(post_json)
        self.assertEqual(result, {"filters": {}, "limit": 10, "offset": 0})

    def test_load_valid_paginated_comment_should_return_ok(self):
        comment_id = str(ObjectId())
        post_json = {"id": comment_id, "limit": 50, "offset": 0}
        new_post = CommentPaginatedSchema()
        result = new_post.load(post_json)
        self.assertEqual(result, {"filters": {"id": comment_id}, "limit": 50, "offset": 0})

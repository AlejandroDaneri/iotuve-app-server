import unittest
from bson import ObjectId
from marshmallow.exceptions import ValidationError
from src.schemas.stat import StatSchema, StatPaginatedSchema, INCLUDE


class SchemaStatTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_stat_ok(self):
        data_json = {'path': '/api/v1/ping', 'full_path': '/api/v1/ping?',
                     'headers': {'Host': 'localhost', 'User-Agent': 'werkzeug/1.0.1'},
                     'host': 'localhost', 'id': '5ed1f0f5ed63c612079b8a77', 'method': 'GET', 'remote_ip': '127.0.0.1',
                     'request_id': '67910060-3a28-46a3-9957-f037f6661e28', 'status': 200, 'time': 0.000438690185546875,
                     'timestamp': '2020-05-30T02:36:53.074000', 'version': 'v1'}
        new_post = StatSchema()
        new_post.load(data_json)

    def test_stat_error(self):
        post_json = {
            "video": str(ObjectId())
        }
        new_post = StatSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)

    def test_stat_error2(self):
        post_json = {
            "content": "Hola este es un comentario de prueba"
        }
        new_post = StatSchema()
        self.assertRaises(ValidationError, new_post.load, post_json)

    def test_stat_paginated(self):
        post_json = {}
        new_post = StatPaginatedSchema(unknown=INCLUDE)
        result = new_post.load(post_json)
        self.assertEqual(result, {"filters": {}, "limit": 10, "offset": 0})

    def test_load_valid_paginated_comment_should_return_ok(self):
        stat_id = str(ObjectId())
        post_json = {"id": stat_id, "limit": 50, "offset": 0}
        new_post = StatPaginatedSchema()
        result = new_post.load(post_json)
        self.assertEqual(result, {"filters": {"id": stat_id}, "limit": 50, "offset": 0})

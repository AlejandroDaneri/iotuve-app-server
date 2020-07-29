import datetime
import unittest
import app_server
from mongoengine import connect, disconnect
from src.misc.importance import ImportanceCalculator
from tests.test_utils import utils


class ImportanceTestCase(unittest.TestCase):

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

    def test_rules(self):
        video = {
            'user_posts': 100,
            'user_reactions': 500,
            'user_friends': 10,
            'days': 3,
            'likes': 10,
            'dislikes': 1,
            'views': 100,
            'comments': 10,
            'importance': 0
        }

        importance_calculator = ImportanceCalculator(video)
        importance_calculator.calculate_importance()

        self.assertTrue(video['importance'] > 0)

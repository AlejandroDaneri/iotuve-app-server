import datetime
import unittest
import app_server
from http import HTTPStatus
from mongoengine import connect, disconnect
from src.conf import APP_NAME
from tests.test_utils import utils
from src.services.stats import StatisticsService


class StatusTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = app_server.app
        app.config['TESTING'] = True
        cls.app = app.test_client()
        disconnect()
        client = connect('mongoenginetest', host='mongomock://localhost')
        cls.db = client['mongoenginetest']

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def tearDown(self):
        utils.delete_all()

    def test_home_should_return_ok(self):
        res = self.app.get('/api/v1/')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertTrue('Welcome' in res.get_data(as_text=True))

    def test_ping_should_return_ok(self):
        res = self.app.get('/api/v1/ping')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual('Pong!', res.get_data(as_text=True))

    def test_stats_should_return_stats_list(self):
        for _ in range(0, 4):
            self.app.get('/api/v1/ping')
        res = self.app.get('/api/v1/stats')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(4, len(res.json['data']))
        for data in res.json['data']:
            self.assertEqual('GET', data["method"])
            self.assertEqual('/api/v1/ping?', data["full_path"])
            self.assertEqual(200, data["status"])

    def test_stats_query_should_return_stats_list(self):
        for _ in range(0, 4):
            self.app.get('/api/v1/ping')
            self.app.get('/api/v1')

        res = self.app.get('/api/v1/stats', query_string={"method": "GET"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(8, len(res.json['data']))

        res = self.app.get('/api/v1/stats', query_string={"method": "POST"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(0, len(res.json['data']))

        res = self.app.get('/api/v1/stats', query_string={"path": "/api/v1"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(4, len(res.json['data']))

        res = self.app.get('/api/v1/stats', query_string={"path": "/api/v1/ping"})
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(4, len(res.json['data']))

    def test_status_should_return_ok(self):
        res = self.app.get('/api/v1/status')
        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(APP_NAME, res.json['message'])

    def test_statistics_requests(self):
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:36:53.074000', status=200, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:36:53.074000', status=200, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:36:53.074000', status=200, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:37:53.074000', status=200, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:37:53.074000', status=200, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:37:53.074000', status=200, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:37:53.074000', status=200, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:37:53.074000', status=400, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:37:53.074000', status=400, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:38:53.074000', status=400, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:38:53.074000', status=400, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:38:53.074000', status=500, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:38:53.074000', status=500, time=0.1)
        utils.save_new_stat(path='/api/v1/ping', timestamp='2020-05-30T02:38:53.074000', status=500, time=0.1)

        # count
        count = StatisticsService.count_requests(datetime.datetime(year=2020, month=5, day=28),
                                                 datetime.datetime(year=2020, month=6, day=1))
        self.assertEqual(count, 14)

        # rpm
        result = list(StatisticsService.rpm(datetime.datetime(year=2020, month=5, day=28),
                                            datetime.datetime(year=2020, month=6, day=1)))
        self.assertEqual(result[0]["count"], 3)
        self.assertEqual(result[1]["count"], 6)
        self.assertEqual(result[2]["count"], 5)

        # by status
        result = StatisticsService.count_requests_grouped_by_status(datetime.datetime(year=2020, month=5, day=28),
                                                                    datetime.datetime(year=2020, month=6, day=1))
        self.assertEqual(result['200'], 7)
        self.assertEqual(result['400'], 4)
        self.assertEqual(result['500'], 3)

        # by path
        result = StatisticsService.count_requests_grouped_by_path(datetime.datetime(year=2020, month=5, day=28),
                                                                  datetime.datetime(year=2020, month=6, day=1))
        self.assertEqual(result['/api/v1/ping'], 14)

    def tests_statistics_counter(self):
        # TODO: Mejorar tests
        video = utils.save_new_video(date_created=datetime.datetime(year=2020, month=5, day=29))
        comm = utils.save_new_comment(video=video.id, date_created=datetime.datetime(year=2020, month=5, day=29))
        utils.save_new_comment(video=video.id, parent=comm.id,
                               date_created=datetime.datetime(year=2020, month=6, day=2))

        videos = StatisticsService.count_videos(datetime.datetime(year=2020, month=5, day=28),
                                                datetime.datetime(year=2020, month=6, day=1))
        self.assertEqual(videos, 1)

        comments = StatisticsService.count_comments(datetime.datetime(year=2020, month=5, day=28),
                                                    datetime.datetime(year=2020, month=6, day=1))
        self.assertEqual(comments, 1)

        friendships = StatisticsService.count_friendships(datetime.datetime(year=2020, month=5, day=28),
                                                          datetime.datetime(year=2020, month=6, day=1))
        self.assertEqual(friendships, 0)


if __name__ == '__main__':
    unittest.main()

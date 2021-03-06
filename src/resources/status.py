from http import HTTPStatus
from flask import current_app as app
from flask import make_response, request
from flask_restful import Resource
from src.conf import APP_NAME
from src.models.stat import Stat
from src.schemas.stat import StatSchema, StatPaginatedSchema
from src.services.stats import StatisticsService


class Home(Resource):
    def get(self):
        home_response_get = "Welcome to %s!" % APP_NAME
        return make_response(home_response_get, HTTPStatus.OK)


class Ping(Resource):
    def get(self):
        return make_response('Pong!', HTTPStatus.OK)


#class Stats(Resource):
#    def get(self):
#        schema = StatPaginatedSchema()
#        paginated = schema.load(request.args)
#        stats = Stat.objects(**paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
#        return make_response(dict(data=StatSchema().dump(stats, many=True)), HTTPStatus.OK)


class StatsNew(Resource):
    def get(self):
        response = {
            "top_dislikes": StatisticsService.top_dislikes(),
            "most_viewed": StatisticsService.top_most_viewed_videos(),
            "approved_friends": StatisticsService.count_approved_friendships(),
            "pending_friends": StatisticsService.count_pending_friendships(),
            "top_likes": StatisticsService.top_likes(),

            "top_writer_users": StatisticsService.top_writer_users(),
            "visibility": StatisticsService.count_visibility(),
            # "min_max_comm": StatisticsService.min_max_avg_comments(),
            "top_active_users": StatisticsService.top_active_users(),
            "top_liker": StatisticsService.top_liker(),
            "top_disliker": StatisticsService.top_disliker()
        }
        return make_response(response, HTTPStatus.OK)


class Status(Resource):
    def get(self):
        result = {
            "code": 0,
            "message": APP_NAME,
            "data:": {
                "server_status": "online",
                "database_status": "online"
            }
        }
        return make_response(result, HTTPStatus.OK)

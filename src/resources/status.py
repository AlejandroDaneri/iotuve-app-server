from http import HTTPStatus
from flask import current_app as app
from flask import make_response, request
from flask_restful import Resource
from src.conf import APP_NAME
from src.models.stat import Stat
from src.schemas.stat import StatSchema, StatPaginatedSchema


class Home(Resource):
    def get(self):
        home_response_get = "Welcome to %s!" % APP_NAME
        return make_response(home_response_get, HTTPStatus.OK)


class Ping(Resource):
    def get(self):
        return make_response('Pong!', HTTPStatus.OK)


class Stats(Resource):
    def get(self):
        schema = StatPaginatedSchema()
        paginated = schema.load(request.args)
        stats = Stat.objects(**paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
        return make_response(dict(data=StatSchema().dump(stats, many=True)), HTTPStatus.OK)


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

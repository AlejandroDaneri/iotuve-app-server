from http import HTTPStatus
from flask import current_app as app
from flask import make_response, jsonify
from flask_restful import Resource
from src.conf import APP_NAME
from src.models.stat import Stat


class Home(Resource):
    def get(self):
        home_response_get = "Welcome to %s!" % APP_NAME
        app.logger.debug('Displaying home with server information.')
        return make_response(home_response_get, HTTPStatus.OK)


class Ping(Resource):
    def get(self):
        app.logger.debug('Ping requested.')
        return make_response('Pong!', HTTPStatus.OK)


class Stats(Resource):
    def get(self):
        app.logger.debug(app.json_encoder.__name__)
        stats = Stat
        objectss = stats.objects()
        oball = objectss.all()
        result = [stat.to_json() for stat in oball]
        return result, HTTPStatus.OK


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

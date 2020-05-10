from http import HTTPStatus
from flask_restful import Resource
from flask import current_app as app
from src import mongo


class Home(Resource):
    def get(self):
        home_response_get = "Welcome to %s!" % app.name
        app.logger.debug('Displaying home with server information.')
        return home_response_get, HTTPStatus.OK


class TestDB(Resource):
    def get(self):
        app.logger.debug('Database info requested.')
        test_db_response_get = {
            "db_server_info": str(mongo.cx.server_info())
        }
        app.logger.debug(test_db_response_get)
        return test_db_response_get, HTTPStatus.OK


class Ping(Resource):
    def get(self):
        app.logger.debug('Ping requested.')
        return "Pong!", HTTPStatus.OK


class Stats(Resource):
    def get(self):
        stats = mongo.db.server_stats.find()
        result = [dict(
            timestamp=st["timestamp"],
            status=st["status"],
            time=st["time"],
            full_path=st["full_path"],
            request_id=st["request_id"]
        ) for st in stats]
        return result, HTTPStatus.OK

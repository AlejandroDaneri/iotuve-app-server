from http import HTTPStatus
from flask_restful import Resource
from flask import current_app as app
from .. import api_name


class Home(Resource):
    def get(self):
        home_response_get = "Welcome to %s!" % api_name
        app.logger.debug('Displaying home with server information.')
        return home_response_get, HTTPStatus.OK


class TestDB(Resource):
    def get(self):
        app.logger.debug('Database info requested.')
        test_db_response_get = {
            "db_server_info": str(app.cl.server_info())
        }
        app.logger.debug(test_db_response_get)
        return test_db_response_get, HTTPStatus.OK


class Ping(Resource):
    def get(self):
        app.logger.debug('Ping requested.')
        return "Pong!", HTTPStatus.OK

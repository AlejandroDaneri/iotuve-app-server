from flask_restful import Resource
from flask import request
from src.misc.authorization import check_token
from src.clients.auth_api import AuthAPIClient


class Recovery(Resource):

    @check_token
    def get(self, username):
        response = AuthAPIClient.get_recovery(username)
        return response.json(), response.status_code

    def post(self, username):
        response = AuthAPIClient.post_recovery_reset(username, request.get_json(force=True))
        return response.json(), response.status_code


class RecoveryList(Resource):

    @check_token
    def get(self):
        response = AuthAPIClient.get_recoveries()
        return response.json(), response.status_code

    def post(self):
        response = AuthAPIClient.post_recovery_request(request.get_json(force=True))
        return response.json(), response.status_code

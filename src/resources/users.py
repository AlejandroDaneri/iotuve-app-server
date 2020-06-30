from flask_restful import Resource
from flask import request
from src.misc.authorization import check_token
from src.clients.auth_api import AuthAPIClient


class Users(Resource):

    @check_token
    def get(self, username):
        response = AuthAPIClient.get_user(username)
        return response.json(), response.status_code

    @check_token
    def put(self, username):
        response = AuthAPIClient.put_user(username, request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def patch(self, username):
        response = AuthAPIClient.patch_user(username, request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def delete(self, username):
        response = AuthAPIClient.delete_user(username)
        return response.json(), response.status_code


class UsersList(Resource):

    def post(self):
        response = AuthAPIClient.post_user(request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def get(self):
        response = AuthAPIClient.get_users(request.data)
        return response.json(), response.status_code


class UsersSessions(Resource):

    @check_token
    def get(self, username):
        response = AuthAPIClient.get_user_sessions(username)
        return response.json(), response.status_code

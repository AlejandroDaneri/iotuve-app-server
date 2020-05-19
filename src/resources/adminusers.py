from flask_restful import Resource
from flask import request
from src.misc.authorization import check_token
from src.clients.auth_api import AuthAPIClient


class AdminUsers(Resource):

    @check_token
    def get(self, username):
        response = AuthAPIClient.get_adminuser(username)
        return response.json(), response.status_code

    @check_token
    def put(self, username):
        response = AuthAPIClient.put_adminuser(username, request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def patch(self, username):
        response = AuthAPIClient.patch_adminuser(username, request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def delete(self, username):
        response = AuthAPIClient.delete_adminuser(username)
        return response.json(), response.status_code


class AdminUsersList(Resource):

    def post(self):
        response = AuthAPIClient.post_adminuser(request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def get(self):
        response = AuthAPIClient.get_adminusers(request.data)
        return response.json(), response.status_code

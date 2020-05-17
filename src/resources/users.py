from http import HTTPStatus
from marshmallow import ValidationError
from flask_restful import Resource
from flask import request
from src.misc.authorization import check_token
from src.misc.responses import response_error
from src.clients.auth_api import AuthAPIClient
from src.schemas.user import UserSchema
from src.schemas.patch import PatchSchema


class Users(Resource):

    @check_token
    def get(self, username):
        response = AuthAPIClient.get_user(username)
        return response.json(), response.status_code

    @check_token
    def put(self, username):
        schema = UserSchema(exclude=('password',))
        try:
            user = schema.load(request.get_json(force=True))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        response = AuthAPIClient.put_user(username, schema.dump(user))
        return response.json(), response.status_code

    @check_token
    def patch(self, username):
        schema_patch = PatchSchema()  # many=True
        try:
            patch_data = schema_patch.load(request.get_json(force=True))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        response = AuthAPIClient.patch_user(username, schema_patch.dump(patch_data))
        return response.json(), response.status_code

    @check_token
    def delete(self, username):
        response = AuthAPIClient.delete_user(username)
        return response.json(), response.status_code


class UsersList(Resource):

    def post(self):
        schema = UserSchema()
        try:
            user = schema.load(request.get_json(force=True))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        response = AuthAPIClient.post_user(schema.dump(user))
        return response.json(), response.status_code

    @check_token
    def get(self):
        response = AuthAPIClient.get_users(request.data)
        return response.json(), response.status_code


class Recovery(Resource):

    @check_token
    def get(self, username):
        response = AuthAPIClient.get_recovery(username)
        return response.json(), response.status_code

    def post(self, username):
        response = AuthAPIClient.post_recovery_reset(username, request.data)
        return response.json(), response.status_code


class RecoveryList(Resource):

    @check_token
    def get(self):
        response = AuthAPIClient.get_recoveries()
        return response.json(), response.status_code

    def post(self):
        response = AuthAPIClient.post_recovery_request(request.data)
        return response.json(), response.status_code

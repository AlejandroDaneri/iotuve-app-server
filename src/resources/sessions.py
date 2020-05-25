from http import HTTPStatus
from marshmallow import ValidationError
from flask_restful import Resource
from flask import request, g
from src.misc.authorization import check_token
from src.misc.responses import response_error
from src.clients.auth_api import AuthAPIClient
from src.schemas.user import UserSchema


class Sessions(Resource):

    def post(self):
        response = AuthAPIClient.post_session(request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def get(self):
        response = AuthAPIClient.get_session(g.session_token)
        return response.json(), response.status_code

    @check_token
    def delete(self):
        response = AuthAPIClient.delete_session(g.session_token)
        return response.json(), response.status_code


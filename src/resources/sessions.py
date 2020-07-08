from http import HTTPStatus
from flask import request, g
from flask_restful import Resource
from src.misc.authorization import check_token
from src.misc.responses import response_error
from src.clients.auth_api import AuthAPIClient


class Sessions(Resource):

    @check_token
    def get(self, session):
        if not (g.session_token == session or g.session_admin):
            return response_error(HTTPStatus.FORBIDDEN, "Not session owner or admin")
        response = AuthAPIClient.get_session(session)
        return response.json(), response.status_code

    @check_token
    def delete(self, session):
        if not (g.session_token == session or g.session_admin):
            return response_error(HTTPStatus.FORBIDDEN, "Not session owner or admin")
        response = AuthAPIClient.delete_session(session)
        return response.json(), response.status_code


class SessionsOwner(Resource):

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

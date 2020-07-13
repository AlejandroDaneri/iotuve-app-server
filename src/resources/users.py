from http import HTTPStatus
from flask import request, current_app as app
from flask_restful import Resource
from marshmallow import ValidationError as MarshmallowValidationError
from src.clients.auth_api import AuthAPIClient
from src.clients.media_api import MediaAPIClient
from src.misc.authorization import check_token
from src.misc.responses import response_error
from src.schemas.avatar import AvatarSchema


def marshal_user(username, data):
    resp_media = MediaAPIClient.get_picture(username)
    if resp_media.status_code == HTTPStatus.OK:
        data['avatar'] = resp_media.json()
    else:
        app.logger.error("[avatar:%s] Error getting avatar from media-server: %s" %
                         (username, resp_media.text))
    data['statistics'] = dict(likes=0, dislikes=0, views=0, uploaded=0, friends=0)


class Users(Resource):

    @check_token
    def get(self, username):
        resp_auth = AuthAPIClient.get_user(username)
        data = resp_auth.json()
        if resp_auth.status_code == HTTPStatus.OK:
            marshal_user(username, data)
        else:
            app.logger.error("[username:%s] Get user - Error from auth-server: %s" %
                             (username, resp_auth.text))
        return data, resp_auth.status_code

    @check_token
    def put(self, username):
        resp_auth = AuthAPIClient.put_user(username, request.get_json(force=True))
        data = resp_auth.json()
        if resp_auth.status_code == HTTPStatus.OK:
            marshal_user(username, data)
        else:
            app.logger.error("[username:%s] Put user - Error from auth-server: %s" %
                             (username, resp_auth.text))
        return data, resp_auth.status_code

    @check_token
    def patch(self, username):
        resp_auth = AuthAPIClient.patch_user(username, request.get_json(force=True))
        data = resp_auth.json()
        if resp_auth.status_code == HTTPStatus.OK:
            marshal_user(username, data)
        else:
            app.logger.error("[username:%s] Patch user - Error from auth-server: %s" %
                             (username, resp_auth.text))
        return data, resp_auth.status_code

    @check_token
    def delete(self, username):
        resp_auth = AuthAPIClient.delete_user(username)
        if resp_auth.status_code == HTTPStatus.OK:
            resp_media = MediaAPIClient.delete_picture(username)
            if resp_media.status_code not in (HTTPStatus.OK, HTTPStatus.NOT_FOUND):
                app.logger.error("[avatar:%s] Error deleting avatar from media-server: %s" %
                                 (username, resp_media.text))
        else:
            app.logger.error("[username:%s] Delete user - Error from auth-server: %s" %
                             (username, resp_auth.text))
        return resp_auth.json(), resp_auth.status_code


class UsersList(Resource):

    def post(self):
        response = AuthAPIClient.post_user(request.get_json(force=True))
        return response.json(), response.status_code

    @check_token
    def get(self):
        response = AuthAPIClient.get_users(request.data)
        users = response.json()
        for user in users:
            marshal_user(user['username'], user)
        return users, response.status_code


class UsersSessions(Resource):

    @check_token
    def get(self, username):
        response = AuthAPIClient.get_user_sessions(username)
        return response.json(), response.status_code


class UsersAvatars(Resource):

    @check_token
    def post(self, username):
        if AuthAPIClient.get_user(username).status_code != HTTPStatus.OK:
            return response_error(HTTPStatus.BAD_REQUEST, "Error getting user")

        schema_avatar = AvatarSchema()
        try:
            request_json = request.get_json(force=True)
            avatar = schema_avatar.load(request_json)
            avatar["user_id"] = username
        except MarshmallowValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err.normalized_messages()))

        response = MediaAPIClient.get_picture(username)
        if response.status_code == HTTPStatus.OK:
            response = MediaAPIClient.patch_picture(username, schema_avatar.dump(avatar))
            return response.json(), response.status_code
        elif response.status_code == HTTPStatus.NOT_FOUND:
            response = MediaAPIClient.post_picture(schema_avatar.dump(avatar))
            return response.json(), response.status_code

        app.logger.error("[avatar:%s] Post avatar - Error from media-server: %s" % (username, response.text))
        return response_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Unexpected error from media-server",
                              data=dict(status=response.status_code, data=response.json()))

    @check_token
    def delete(self, username):
        response = MediaAPIClient.delete_picture(username)
        return response.json(), response.status_code

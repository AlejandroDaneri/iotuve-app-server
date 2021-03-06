import datetime
from http import HTTPStatus
from flask import g, request
from flask_restful import Resource
from flask_mongoengine import ValidationError as MongoValidationError
from src.misc.authorization import check_token
from src.misc.responses import response_error, response_ok
from src.models.fcm_token import FCMToken


class FCMTokens(Resource):

    @check_token
    def post(self):
        token = request.get_json(force=True).get('token', None)
        if not token:
            return response_error(HTTPStatus.BAD_REQUEST, "Must provide FCM token")

        user_tokens = FCMToken.objects(user=g.session_username)
        if user_tokens:
            if token in user_tokens.first().tokens:
                return response_ok(HTTPStatus.ALREADY_REPORTED, "FCM token already exists")
            user_tokens.update_one(push__tokens=token)
        else:
            FCMToken(user=g.session_username, tokens=[token]).save()

        return response_ok(HTTPStatus.CREATED, "FCM token saved")

    @check_token
    def delete(self):
        token = request.get_json(force=True).get('token', None)
        if not token:
            return response_error(HTTPStatus.BAD_REQUEST, "Must provide FCM token")

        try:
            user_tokens = FCMToken.objects(user=g.session_username, tokens__in=[token])
        except MongoValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err))

        if not user_tokens:
            return response_error(HTTPStatus.NOT_FOUND, "FCM token not found")

        user_tokens.update_one(pull__tokens=token)

        return response_ok(HTTPStatus.OK, "FCM token deleted")

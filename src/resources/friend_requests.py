from http import HTTPStatus
from marshmallow import ValidationError
from flask_restful import Resource
from flask import request
from flask import current_app as app
from src import mongo
from src.misc.authorization import check_token
from src.misc.responses import response_error
from src.schemas.friend_request import FriendRequestSchema


class FriendRequestsList(Resource):

    @check_token
    def post(self):
        app.logger.debug("PRUEBA POST FRIEND REQUEST")
        schema = FriendRequestSchema()
        try:
            friend_request = schema.load(request.get_json(force=True))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        app.logger.debug(friend_request)
        return friend_request, HTTPStatus.CREATED

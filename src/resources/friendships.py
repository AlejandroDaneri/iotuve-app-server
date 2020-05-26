import datetime
from http import HTTPStatus
from marshmallow import ValidationError
from flask_restful import Resource
from flask import make_response, request, g, current_app as app
from mongoengine.queryset.visitor import Q
from src.misc.authorization import check_token
from src.misc.responses import response_error, response_ok
from src.schemas.friendship import FriendshipSchema, FriendshipPaginatedSchema
from src.models.friendship import Friendship
from src.clients.auth_api import AuthAPIClient


class Friendships(Resource):

    @check_token
    def put(self, friendship_id):
        friendship = Friendship.objects(id=friendship_id).first_or_404()

        if friendship.to_user != g.session_username:
            return response_error(HTTPStatus.FORBIDDEN, "Cant modify this friend request")

        schema = FriendshipSchema(only=("status",))
        try:
            status = schema.load(request.get_json(force=True)).status
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()), code=-1)

        if friendship.status == "pending" and friendship.status != status:
            now = datetime.datetime.utcnow()
            friendship.date_updated = now
            friendship.status = status
            friendship.save()

        return make_response(FriendshipSchema().dump(friendship), HTTPStatus.OK)

    @check_token
    def delete(self, friendship_id):
        friendship = Friendship.objects(id=friendship_id).first_or_404()
        if g.session_username not in (friendship.from_user, friendship.to_user):
            return response_error(HTTPStatus.FORBIDDEN, "Cant delete this friend request")
        friendship.delete()
        return response_ok(HTTPStatus.OK, "Friend request deleted")


class FriendshipsList(Resource):

    @check_token
    def get(self):
        schema = FriendshipPaginatedSchema()
        paginated = schema.load(request.args)
        friendships = Friendship.objects(**paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
        return make_response(dict(data=schema.dump(friendships, many=True)), HTTPStatus.OK)

    @check_token
    def post(self):
        schema = FriendshipSchema()
        try:
            friendship = schema.load(request.get_json(force=True))
        except ValidationError as e:
            app.logger.debug(str(e.normalized_messages()))
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()), code=-1)

        friendship.from_user = g.session_username

        if friendship.to_user == g.session_username:
            return response_error(HTTPStatus.BAD_REQUEST, "Cant request yourself")

        if AuthAPIClient.get_user(friendship.to_user).status_code != HTTPStatus.OK:
            return response_error(HTTPStatus.BAD_REQUEST, "Error getting to_user", code=-2)

        if Friendship.objects(
             ((Q(from_user=friendship.from_user) & Q(to_user=friendship.to_user)) |
              (Q(from_user=friendship.to_user) & Q(to_user=friendship.from_user)))).count():
            return response_error(HTTPStatus.BAD_REQUEST, "Friend request already exist", code=-4)

        now = datetime.datetime.utcnow()
        friendship.status = "pending"
        friendship.date_created = now
        friendship.date_updated = now
        friendship.save()
        return make_response(schema.dump(friendship), HTTPStatus.CREATED)

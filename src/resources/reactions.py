import datetime
from http import HTTPStatus
from flask import g, request, make_response
from flask_restful import Resource
from flask_mongoengine import ValidationError as MongoValidationError
from src.misc.authorization import check_token
from src.misc.responses import response_error, response_ok
from src.models.reaction import Like, Dislike, View
from src.models.video import Video
from src.schemas.reaction import ReactionSchema, ReactionPaginatedSchema


class Reactions(Resource):

    def add_video_reaction(self, video):
        raise NotImplementedError()

    def remove_video_reaction(self, video):
        raise NotImplementedError()

    def post(self, video_id):
        raise NotImplementedError()

    def delete(self, video_id):
        raise NotImplementedError()

    @check_token
    def get(self, video_id):
        schema = ReactionPaginatedSchema()
        paginated = schema.load(request.args)
        reactions = self.reaction.objects(video=video_id, **paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
        return make_response(dict(data=ReactionSchema().dump(reactions, many=True)), HTTPStatus.OK)


class LikeReactions(Reactions):

    def add_video_reaction(self, video):
        raise NotImplementedError()

    def remove_video_reaction(self, video):
        raise NotImplementedError()

    @check_token
    def post(self, video_id):
        try:
            video = Video.objects(id=video_id).first()
        except MongoValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err))
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")
        if self.reaction.objects(video=video_id, user=g.session_username).first():
            return response_error(HTTPStatus.BAD_REQUEST, self.message_reaction_already_exist)
        self.reaction(video=video_id, user=g.session_username, date_created=datetime.datetime.utcnow()).save()
        self.add_video_reaction(video)
        video.save()
        return response_ok(HTTPStatus.CREATED, self.message_reaction_saved)

    @check_token
    def delete(self, video_id):
        try:
            video = Video.objects(id=video_id).first()
        except MongoValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err))
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")
        reaction = self.reaction.objects(video=video_id, user=g.session_username).first()
        if reaction is None:
            return response_error(HTTPStatus.NOT_FOUND, self.message_reaction_not_found)
        reaction.delete()
        self.remove_video_reaction(video)
        video.save()
        return response_ok(HTTPStatus.OK, self.message_reaction_deleted)


class Likes(LikeReactions):

    reaction = Like
    message_reaction_already_exist = "Like already exists"
    message_reaction_saved = "Like saved"
    message_reaction_deleted = "Like deleted"
    message_reaction_not_found = "Like not found"

    def add_video_reaction(self, video):
        video.count_likes += 1

    def remove_video_reaction(self, video):
        video.count_likes -= 1


class Dislikes(LikeReactions):

    reaction = Dislike
    message_reaction_already_exist = "Dislike already exists"
    message_reaction_saved = "Dislike saved"
    message_reaction_deleted = "Dislike deleted"
    message_reaction_not_found = "Dislike not found"

    def add_video_reaction(self, video):
        video.count_dislikes += 1

    def remove_video_reaction(self, video):
        video.count_dislikes -= 1


class Views(Reactions):

    reaction = View
    message_reaction_saved = "View saved"
    message_reaction_not_found = "View not found"

    def add_video_reaction(self, video):
        video.count_views += 1

    def remove_video_reaction(self, video):
        video.count_views -= 1

    @check_token
    def post(self, video_id):
        try:
            video = Video.objects(id=video_id).first()
        except MongoValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err))
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")
        if self.reaction.objects(video=video_id, user=g.session_username).first() is None:
            self.reaction(video=video_id, user=g.session_username, date_created=datetime.datetime.utcnow()).save()
        self.add_video_reaction(video)
        video.save()
        return response_ok(HTTPStatus.CREATED, self.message_reaction_saved)

    @check_token
    def delete(self, video_id):
        return response_error(HTTPStatus.FORBIDDEN, "Cant remove a view")

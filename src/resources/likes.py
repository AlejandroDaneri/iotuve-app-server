import datetime
from http import HTTPStatus
from flask import g, request, make_response
from flask_restful import Resource
from src.misc.authorization import check_token
from src.misc.responses import response_error, response_ok
from src.models.like import Like
from src.models.video import Video
from src.schemas.like import LikeSchema, LikePaginatedSchema


class Likes(Resource):
    @check_token
    def get(self, video_id):
        like = Like.objects(video=video_id, user=g.session_username).first()
        if like is None:
            return response_error(HTTPStatus.NOT_FOUND, "Like not found")
        return make_response(LikeSchema().dump(like), HTTPStatus.OK)

    @check_token
    def post(self, video_id):
        if Like.objects(video=video_id, user=g.session_username).first():
            return response_error(HTTPStatus.BAD_REQUEST, "Already liked")
        video = Video.objects(id=video_id).first()
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")
        Like(video=video_id, user=g.session_username, date_created=datetime.datetime.utcnow()).save()
        video.count_likes += 1
        video.save()
        return response_ok(HTTPStatus.CREATED, "Like saved")

    @check_token
    def delete(self, video_id):
        like = Like.objects(video=video_id, user=g.session_username).first()
        if like is None:
            return response_error(HTTPStatus.NOT_FOUND, "Like not found")
        video = Video.objects(id=video_id).first()
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")
        like.delete()
        video.count_likes -= 1
        video.save()
        return response_ok(HTTPStatus.OK, "Like deleted")


class LikesList(Resource):
    @check_token
    def get(self, video_id):
        schema = LikePaginatedSchema()
        paginated = schema.load(request.args)
        likes = Like.objects(video=video_id, **paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
        return make_response(dict(data=LikeSchema().dump(likes, many=True)), HTTPStatus.OK)

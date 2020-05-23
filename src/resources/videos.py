import datetime
from http import HTTPStatus
from flask import make_response, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from src.misc.authorization import check_token
from src.misc.responses import response_error, response_ok
from src.models.video import Video
from src.schemas.video import VideoSchema, VideoPaginatedSchema


class Videos(Resource):
    @check_token
    def get(self, video_id):
        schema = VideoSchema()
        video = Video.objects(id=video_id).first_or_404()
        return make_response(schema.dump(video), HTTPStatus.OK)

    @check_token
    def put(self, video_id):
        schema = VideoSchema()
        video = Video.objects(id=video_id).first_or_404()
        if video.user != g.session_username:
            return response_error(HTTPStatus.FORBIDDEN, str("Forbidden"))
        try:
            new_video = schema.load(request.get_json(force=True))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        video.title = new_video.title
        video.description = new_video.description
        video.location = new_video.location
        video.visibility = new_video.visibility
        video.date_updated = datetime.datetime.utcnow()
        video.save()
        return make_response(schema.dump(video), HTTPStatus.OK)

    @check_token
    def delete(self, video_id):
        video = Video.objects(id=video_id).first_or_404()
        if video.user != g.session_username:
            return response_error(HTTPStatus.FORBIDDEN, str("Forbidden"))
        video.delete()
        return response_ok(HTTPStatus.OK, "Video deleted")


class VideosList(Resource):
    @check_token
    def get(self):
        schema = VideoPaginatedSchema()
        paginated = schema.load(request.args)
        video = Video.objects(**paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
        return make_response(dict(data=schema.dump(video, many=True)), HTTPStatus.OK)

    @check_token
    def post(self):
        schema = VideoSchema()
        try:
            video = schema.load(request.get_json(force=True))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        now = datetime.datetime.utcnow()
        video.user = g.session_username
        video.date_created = now
        video.date_updated = now
        video.save()
        return make_response(schema.dump(video), HTTPStatus.CREATED)

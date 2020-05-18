import datetime
from http import HTTPStatus
from flask import make_response, request, g
from flask_restful import Resource
from marshmallow import ValidationError
from src.misc.authorization import check_token
from src.misc.responses import response_error
from src.models.video import Video
from src.schemas.video import VideoSchema


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


class VideosList(Resource):
    @check_token
    def get(self):
        schema = VideoSchema()
        video = Video.objects()
        return make_response(schema.dump(video, many=True), HTTPStatus.OK)

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

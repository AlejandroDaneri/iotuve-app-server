import datetime
from http import HTTPStatus
from flask import make_response, request, g, current_app as app
from flask_restful import Resource
from marshmallow import ValidationError
from src.clients.media_api import MediaAPIClient
from src.misc.authorization import check_token
from src.misc.responses import response_error, response_ok
from src.models.comment import Comment
from src.models.video import Video
from src.schemas.video import VideoSchema, VideoPaginatedSchema, MediaSchema


class Videos(Resource):
    @check_token
    def get(self, video_id):
        schema = VideoSchema()
        video = Video.objects(id=video_id).first_or_404()
        resp_media = MediaAPIClient.get_video(video.id)
        if resp_media.status_code != HTTPStatus.OK:
            app.logger.error("[video_id:%s] Error getting media from media-server: %s" %
                             (video.id, resp_media.text))
            return response_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Error getting media")
        result = schema.dump(video)
        result["media"] = resp_media.json()
        return make_response(result, HTTPStatus.OK)

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
        resp_media = MediaAPIClient.get_video(video.id)
        if resp_media.status_code != HTTPStatus.OK:
            app.logger.error("[video_id:%s] Error getting media from media-server: %s" %
                             (video.id, resp_media.text))
            return response_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Error getting media")
        result = schema.dump(video)
        result["media"] = resp_media.json()
        return make_response(result, HTTPStatus.OK)

    @check_token
    def delete(self, video_id):
        video = Video.objects(id=video_id).first_or_404()
        if video.user != g.session_username:
            return response_error(HTTPStatus.FORBIDDEN, str("Forbidden"))
        resp_media = MediaAPIClient.delete_video(video.id)
        if resp_media.status_code != HTTPStatus.OK:
            app.logger.error("[video_id:%s] Error deleting media from media-server: %s" %
                             (video.id, resp_media.text))
            return response_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Error getting media")
        video.delete()
        Comment.objects(video=video_id).delete()
        return response_ok(HTTPStatus.OK, "Video deleted")


class VideosList(Resource):
    @check_token
    def get(self):
        schema = VideoPaginatedSchema()
        paginated = schema.load(request.args)
        videos = Video.objects(**paginated["filters"]).skip(paginated["offset"]).limit(paginated["limit"])
        results = []
        for video in videos:
            resp_media = MediaAPIClient.get_video(video.id)
            if resp_media.status_code != HTTPStatus.OK:
                app.logger.error("[video_id:%s] Error getting media from media-server: %s" %
                                 (video.id, resp_media.text))
                continue
            result = schema.dump(video)
            result["media"] = resp_media.json()
            results.append(result)
        return make_response(dict(data=results), HTTPStatus.OK)

    @check_token
    def post(self):
        schema_video = VideoSchema()
        schema_media = MediaSchema()
        try:
            request_json = request.get_json(force=True)
            video = schema_video.load(request_json)
            media = schema_media.load(request_json.get("media", {}))
        except ValidationError as e:
            return response_error(HTTPStatus.BAD_REQUEST, str(e.normalized_messages()))
        now = datetime.datetime.utcnow()
        video.user = g.session_username
        video.date_created = now
        video.date_updated = now
        new_video = video.save()
        media["video_id"] = new_video.id
        media["user_id"] = new_video.user
        resp_media = MediaAPIClient.post_video(schema_media.dump(media))
        if resp_media.status_code != HTTPStatus.CREATED:
            app.logger.error("[video_name:%s] Error saving new video on media-server: %s" %
                             (media["name"], resp_media.text))
            video.delete()
            return response_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Error saving media")
        result = schema_video.dump(new_video)
        result["media"] = resp_media.json()
        return make_response(result, HTTPStatus.CREATED)

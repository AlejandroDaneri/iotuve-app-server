import datetime
from http import HTTPStatus
from flask import make_response, request, g, current_app as app
from flask_restful import Resource
from flask_mongoengine import ValidationError as MongoValidationError
from marshmallow import ValidationError as MarshmallowValidationError
from src.clients.media_api import MediaAPIClient
from src.misc.authorization import check_token
from src.misc.responses import response_error, response_ok
from src.models.comment import Comment
from src.models.friendship import Friendship
from src.models.reaction import Like, Dislike, View
from src.models.video import Video
from src.schemas.video import VideoSchema, VideoPaginatedSchema, MediaSchema


class Videos(Resource):
    @check_token
    def get(self, video_id):
        try:
            video = Video.objects(id=video_id).first()
        except MongoValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err))
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")

        if not g.session_admin and video.user != g.session_username and video.visibility == "private"\
                and Friendship.friendship_exist(video.user, g.session_username, "approved") == 0:
            return response_error(HTTPStatus.FORBIDDEN, "This video is private")

        resp_media = MediaAPIClient.get_video(video.id)
        if resp_media.status_code != HTTPStatus.OK:
            app.logger.error("[video_id:%s] Error getting media from media-server: %s" %
                             (video.id, resp_media.text))
            return response_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Error getting media")
        schema = VideoSchema()
        result = schema.dump(video)
        result["media"] = resp_media.json()
        result["user_like"] = Like.objects(video=video, user=g.session_username).first() is not None
        result["user_dislike"] = Dislike.objects(video=video, user=g.session_username).first() is not None
        result["user_view"] = View.objects(video=video, user=g.session_username).first() is not None
        return make_response(result, HTTPStatus.OK)

    @check_token
    def put(self, video_id):
        if g.session_admin:
            return response_error(HTTPStatus.FORBIDDEN, "Admin users can't update videos")
        try:
            video = Video.objects(id=video_id).first()
        except MongoValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err))
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")
        if video.user != g.session_username:
            return response_error(HTTPStatus.FORBIDDEN, str("Forbidden"))
        schema = VideoSchema()
        try:
            new_video = schema.load(request.get_json(force=True))
        except MarshmallowValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err.normalized_messages()))
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
        result["user_like"] = Like.objects(video=video, user=g.session_username).first() is not None
        result["user_dislike"] = Dislike.objects(video=video, user=g.session_username).first() is not None
        result["user_view"] = View.objects(video=video, user=g.session_username).first() is not None
        return make_response(result, HTTPStatus.OK)

    @check_token
    def delete(self, video_id):
        try:
            video = Video.objects(id=video_id).first()
        except MongoValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err))
        if video is None:
            return response_error(HTTPStatus.NOT_FOUND, "Video not found")
        if video.user != g.session_username and not g.session_admin:
            return response_error(HTTPStatus.FORBIDDEN, "Forbidden")
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
        try:
            paginated = VideoPaginatedSchema().load(request.args)
        except MarshmallowValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err.normalized_messages()))

        filters = paginated["filters"]
        offset = paginated["offset"]
        limit = paginated["limit"]
        user = filters.get("user", None)

        if not g.session_admin and user != g.session_username:
            video_id = filters.get("id", None)
            visibility = filters.get("visibility", None)
            friends = Friendship.get_user_friends_list(g.session_username)
            videos = Video.get_videos_wall(
                wall_user=g.session_username, friends_wall_user=friends, video_id=video_id,
                user=user, visibility=visibility, offset=offset, limit=limit)
        else:
            videos = Video.get_videos(filters=filters, offset=offset, limit=limit)

        results = []
        for video in videos:
            resp_media = MediaAPIClient.get_video(video.id)
            if resp_media.status_code != HTTPStatus.OK:
                app.logger.error("[video_id:%s] Error getting media from media-server: %s" %
                                 (video.id, resp_media.text))
                continue
            result = VideoSchema().dump(video)
            result["media"] = resp_media.json()
            result["user_like"] = Like.objects(video=video, user=g.session_username).first() is not None
            result["user_dislike"] = Dislike.objects(video=video, user=g.session_username).first() is not None
            result["user_view"] = View.objects(video=video, user=g.session_username).first() is not None
            results.append(result)
        return make_response(dict(data=results), HTTPStatus.OK)

    @check_token
    def post(self):
        if g.session_admin:
            return response_error(HTTPStatus.FORBIDDEN, "Admin users can't post videos")
        schema_video = VideoSchema()
        schema_media = MediaSchema()
        try:
            request_json = request.get_json(force=True)
            video = schema_video.load(request_json)
            media = schema_media.load(request_json.get("media", {}))
        except MarshmallowValidationError as err:
            return response_error(HTTPStatus.BAD_REQUEST, str(err.normalized_messages()))
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

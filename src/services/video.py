from http import HTTPStatus
from flask import g, current_app as app
from src.clients.auth_api import AuthAPIClient
from src.clients.media_api import MediaAPIClient
from src.models.reaction import Like, Dislike, View
from src.services.user import UserService


class MediaServerError(Exception):
    """
    """
    pass


class AuthServerError(Exception):
    """
    """
    pass


class VideoService:

    @staticmethod
    def __marshal_media(video_id):
        resp_media = MediaAPIClient.get_video(video_id)
        if resp_media.status_code != HTTPStatus.OK:
            app.logger.error("[video_id:%s] Error getting media from media-server: %s" %
                             (video_id, resp_media.text))
            raise MediaServerError("Error getting video media data")
        return resp_media.json()

    @staticmethod
    def __marshal_user(username):
        resp_auth = AuthAPIClient.get_user(username)
        data = resp_auth.json()
        if resp_auth.status_code != HTTPStatus.OK:
            app.logger.error("[username:%s] Get user - Error from auth-server: %s" %
                             (username, resp_auth.text))
            raise AuthServerError("Error getting video user data")
        return UserService.marshal_user(username, data)

    @staticmethod
    def marshal_video(video_id, data):
        data["media"] = VideoService.__marshal_media(video_id)
        data["user_like"] = Like.objects(video=video_id, user=g.session_username).first() is not None
        data["user_dislike"] = Dislike.objects(video=video_id, user=g.session_username).first() is not None
        data["user_view"] = View.objects(video=video_id, user=g.session_username).first() is not None
        data["user"] = VideoService.__marshal_user(data["user"])
        return data

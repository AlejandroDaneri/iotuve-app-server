from http import HTTPStatus
from flask import g, current_app as app
from src.clients.media_api import MediaAPIClient
from src.models.reaction import Like, Dislike, View


class MediaServerError(Exception):
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
    def marshal_video(video_id, data):
        data["media"] = VideoService.__marshal_media(video_id)
        data["user_like"] = Like.objects(video=video_id, user=g.session_username).first() is not None
        data["user_dislike"] = Dislike.objects(video=video_id, user=g.session_username).first() is not None
        data["user_view"] = View.objects(video=video_id, user=g.session_username).first() is not None
        return data

from http import HTTPStatus
from flask import current_app as app
from src.clients.auth_api import AuthAPIClient
from src.clients.media_api import MediaAPIClient
from src.models.friendship import Friendship
from src.models.video import Video


class AuthServerError(Exception):
    """
    """
    pass


class UserService:

    @staticmethod
    def __marshal_avatar(username):
        resp_media = MediaAPIClient.get_picture(username)
        if resp_media.status_code == HTTPStatus.OK:
            return resp_media.json()
        if resp_media.status_code != HTTPStatus.NOT_FOUND:
            app.logger.error("[avatar:%s] Error getting avatar from media-server: %s" % (username, resp_media.text))
        return None

    @staticmethod
    def __marshal_statistics(username):
        result = dict(likes=0, dislikes=0, views=0, uploaded=0, friends=0)
        for video in Video.objects(user=username):
            result['likes'] += video.count_likes
            result['dislikes'] += video.count_dislikes
            result['views'] += video.count_views
            result['uploaded'] += 1
        result['friends'] = Friendship.count_user_friends(username)
        return result

    @staticmethod
    def marshal_user(username, data):
        data['avatar'] = UserService.__marshal_avatar(username) or data['avatar']
        data['statistics'] = UserService.__marshal_statistics(username)
        return data

    @staticmethod
    def get_marshalled_user(username):
        resp_auth = AuthAPIClient.get_user(username)
        data = resp_auth.json()
        if resp_auth.status_code != HTTPStatus.OK:
            app.logger.error("[username:%s] Get user - Error from auth-server: %s" %
                             (username, resp_auth.text))
            raise AuthServerError("Error getting video user data")
        return UserService.marshal_user(username, data)

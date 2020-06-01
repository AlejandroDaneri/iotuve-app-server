import requests
from flask import g
import src.conf as conf


class MediaAPIClient:

    @staticmethod
    def __headers():
        headers = {'X-Client-ID': conf.API_MEDIA_CLIENT_ID,
                   'X-Request-ID': g.request_id}
        if g.session_token:
            headers['X-Auth-Token'] = g.session_token

        return headers

    @staticmethod
    def get_video(video_id):
        return requests.get("%s%s%s" % (conf.API_MEDIA_CLIENT_URL, "videos/", video_id),
                            headers=MediaAPIClient.__headers())

    @staticmethod
    def post_video(data):
        return requests.post("%s%s" % (conf.API_MEDIA_CLIENT_URL, "videos"),
                             json=data, headers=MediaAPIClient.__headers())

    @staticmethod
    def delete_video(video_id):
        return requests.delete("%s%s%s" % (conf.API_MEDIA_CLIENT_URL, "videos/", video_id),
                               headers=MediaAPIClient.__headers())

    @staticmethod
    def get_picture(picture_id):
        return requests.get("%s%s%s" % (conf.API_MEDIA_CLIENT_URL, "pictures", picture_id),
                            headers=MediaAPIClient.__headers())

    @staticmethod
    def post_picture(data):
        return requests.post("%s%s" % (conf.API_MEDIA_CLIENT_URL, "pictures"),
                             json=data, headers=MediaAPIClient.__headers())

    @staticmethod
    def delete_picture(picture_id):
        return requests.delete("%s%s%s" % (conf.API_MEDIA_CLIENT_URL, "pictures/", picture_id),
                               headers=MediaAPIClient.__headers())

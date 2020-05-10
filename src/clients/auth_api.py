import requests
from flask import g
from flask import current_app as app
import src.conf as conf


class AuthAPIClient:

    @staticmethod
    def __headers():
        headers = {'X-Client-ID': conf.API_AUTH_CLIENT_ID,
                   'X-Request-ID': g.request_id}
        if g.session_token:
            headers['X-Auth-Token'] = g.session_token

        return headers

    @staticmethod
    def get_ping():
        return requests.get("%s%s" % (conf.API_AUTH_CLIENT_URL, "ping"),
                            headers=AuthAPIClient.__headers())

    @staticmethod
    def get_status():
        return requests.get("%s%s" % (conf.API_AUTH_CLIENT_URL, "status"),
                            headers=AuthAPIClient.__headers())

    @staticmethod
    def get_stats():
        return requests.get("%s%s" % (conf.API_AUTH_CLIENT_URL, "stats"),
                            headers=AuthAPIClient.__headers())

    @staticmethod
    def get_session(session_token):
        return requests.get("%s%s%s" % (conf.API_AUTH_CLIENT_URL, "sessions/", session_token),
                            headers=AuthAPIClient.__headers())

    @staticmethod
    def delete_session(session_token):
        return requests.delete("%s%s%s" % (conf.API_AUTH_CLIENT_URL, "sessions/", session_token),
                               headers=AuthAPIClient.__headers())

    @staticmethod
    def post_session(data):
        return requests.post("%s%s" % (conf.API_AUTH_CLIENT_URL, "sessions"),
                             json=data, headers=AuthAPIClient.__headers())

    @staticmethod
    def get_user(username):
        return requests.get("%s%s%s" % (conf.API_AUTH_CLIENT_URL, "users/", username),
                            headers=AuthAPIClient.__headers())

    @staticmethod
    def put_user(username, data):
        return requests.put("%s%s%s" % (conf.API_AUTH_CLIENT_URL, "users/", username),
                            json=data, headers=AuthAPIClient.__headers())

    @staticmethod
    def patch_user(username, data):
        return requests.patch("%s%s%s" % (conf.API_AUTH_CLIENT_URL, "users/", username),
                              json=data, headers=AuthAPIClient.__headers())

    @staticmethod
    def get_recovery(username):
        return requests.get("%s%s%s" % (conf.API_AUTH_CLIENT_URL, "recovery/", username),
                            headers=AuthAPIClient.__headers())

    @staticmethod
    def get_users(filters):
        return requests.get("%s%s" % (conf.API_AUTH_CLIENT_URL, "users"),
                            params=filters, headers=AuthAPIClient.__headers())

    @staticmethod
    def post_user(data):
        app.logger.debug("Inside post_user data: %s" % data)
        return requests.post("%s%s" % (conf.API_AUTH_CLIENT_URL, "users"),
                             json=data, headers=AuthAPIClient.__headers())

import requests
from http import HTTPStatus
from functools import wraps
from flask import g
from flask import request
from src.clients.auth_api import AuthAPIClient
from src.misc.responses import response_error


# Check if token is valid
def check_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session_token = request.headers.get('X-Auth-Token')
        if not session_token:
            return response_error(HTTPStatus.UNAUTHORIZED, 'Token required')
        response = AuthAPIClient.get_session(session_token)
        if response.status_code != requests.codes.ok:
            return response_error(HTTPStatus.UNAUTHORIZED, 'Authentication error. %s' % response.text)
        g.session_token = session_token
        g.session_username = response.json()['username']
        return f(*args, **kwargs)
    return wrapper

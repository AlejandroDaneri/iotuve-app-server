from http import HTTPStatus
from flask import current_app as app
from src.models.fcm_token import FCMToken
from src.clients.fcm_api import FCMAPIClient


class FCMError(Exception):
    """
    FCMError
    https://firebase.google.com/docs/reference/fcm/rest/v1/ErrorCode
    """
    pass


class AuthenticationError(FCMError):
    """
    API key not found
    """
    pass


class FCMNotRegisteredError(FCMError):
    """
    push token is not registered
    """
    pass


class FCMServerError(FCMError):
    """
    Internal server error or timeout error on Firebase Cloud Messaging server
    """
    pass


class InvalidDataError(FCMError):
    """
    Invalid input
    """
    pass


class FCMService:

    @staticmethod
    def get_user_fcm_tokens(user):
        user_tokens = FCMToken.objects(user=user).first()
        return user_tokens.tokens if user_tokens else None

    @staticmethod
    def validate_response(response, silent):
        def validate():
            if response.status_code == HTTPStatus.OK:
                if 'content-length' in response.headers and int(response.headers['content-length']) <= 0:
                    raise FCMServerError("FCM server connection error, the response is empty")
                else:
                    parsed_response = response.json()
                    success = parsed_response.get('success', 0)
                    failure = parsed_response.get('failure', 0)
                    if success == 0 or failure != 0:
                        raise FCMServerError("FCM Response success %s and failure %s" % (success, failure))
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                raise AuthenticationError("There was an error authenticating the sender account")
            elif response.status_code == HTTPStatus.BAD_REQUEST:
                raise InvalidDataError(response.text)
            elif response.status_code == HTTPStatus.NOT_FOUND:
                raise FCMNotRegisteredError("Token not registered")
            else:
                raise FCMServerError("FCM server is temporarily unavailable")

        try:
            validate()
        except FCMError as err:
            app.logger.error(str(err))
            if not silent:
                raise FCMError(err)

    @staticmethod
    def send_friendship_requested(from_user, to_user, silent):
        user_tokens = FCMService.get_user_fcm_tokens(to_user)
        if user_tokens:
            response = FCMAPIClient.post_friendship_requested(user_tokens, from_user)
            FCMService.validate_response(response, silent)

    @staticmethod
    def send_friendship_approved(from_user, to_user, silent):
        user_tokens = FCMService.get_user_fcm_tokens(from_user)
        if user_tokens:
            response = FCMAPIClient.post_friendship_approved(user_tokens, to_user)
            FCMService.validate_response(response, silent)

    @staticmethod
    def send_new_video_comment(from_user, to_user, video, silent):
        user_tokens = FCMService.get_user_fcm_tokens(to_user)
        if user_tokens:
            response = FCMAPIClient.post_new_video_comment(user_tokens, from_user, video)
            FCMService.validate_response(response, silent)

    @staticmethod
    def send_new_video_like(from_user, to_user, video, silent):
        user_tokens = FCMService.get_user_fcm_tokens(to_user)
        if user_tokens:
            response = FCMAPIClient.post_new_video_like(user_tokens, from_user, video)
            FCMService.validate_response(response, silent)

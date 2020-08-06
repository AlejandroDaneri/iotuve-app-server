from enum import Enum
import requests
import src.conf as conf


class FCMTopics(str, Enum):

    def __new__(cls, value, title, body):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.title = title
        obj.body = body
        return obj

    # Friendship
    FRIENDSHIP_REQUESTED = 'FRIENDSHIP_REQUESTED', 'Nueva solicitud de amistad', 'Tienes una solicitud de amistad de %s'
    FRIENDSHIP_APPROVED = 'FRIENDSHIP_APPROVED', 'Tienes un amigo', '%s acaba de aceptar tu solicitud'

    # Comments
    NEW_COMMENT = 'NEW_COMMENT', 'Nuevo comentario', '%s ha comentado en tu video %s'

    # Likes
    NEW_LIKE = 'NEW_LIKE', 'Me gusta', 'A %s le gusta tu video %s'


class FCMAPIClient:

    @staticmethod
    def __headers():
        return {'Authorization': "key=%s" % conf.API_FIREBASE_KEY,
                'Content-Type': 'application/json'}

    @staticmethod
    def send_message(tokens, title, body, data):

        data["channelId"] = "CHANNEL_GENERAL"
        fcm_payload = {
            "notification": {"color": "#0000ff", "title": title, "body": body, "android_channel_id": "CHANNEL_GENERAL"},
            "priority": "high",
            "data": data}

        if len(tokens) > 1:
            fcm_payload['registration_ids'] = tokens
        else:
            fcm_payload['to'] = tokens[0]

        res = requests.post(conf.API_FIREBASE_CLIENT_URL, json=fcm_payload, headers=FCMAPIClient.__headers())
        return res

    @staticmethod
    def post_friendship_requested(tokens, requester):
        topic = FCMTopics.FRIENDSHIP_REQUESTED
        title = topic.title
        body = topic.body % requester
        data = {"code": topic}
        return FCMAPIClient.send_message(tokens, title, body, data)

    @staticmethod
    def post_friendship_approved(tokens, requested):
        topic = FCMTopics.FRIENDSHIP_APPROVED
        title = topic.title
        body = topic.body % requested
        data = {"code": topic}
        return FCMAPIClient.send_message(tokens, title, body, data)

    @staticmethod
    def post_new_video_comment(tokens, user, video):
        topic = FCMTopics.NEW_COMMENT
        title = topic.title
        body = topic.body % (user, video)
        data = {"code": topic}
        return FCMAPIClient.send_message(tokens, title, body, data)

    @staticmethod
    def post_new_video_like(tokens, user, video):
        topic = FCMTopics.NEW_LIKE
        title = topic.title
        body = topic.body % (user, video)
        data = {"code": topic}
        return FCMAPIClient.send_message(tokens, title, body, data)

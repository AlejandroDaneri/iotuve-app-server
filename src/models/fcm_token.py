from src.conf.database import db


class FCMToken(db.Document):
    meta = {'collection': 'fcm_token'}
    user = db.StringField(required=True)
    tokens = db.ListField(db.StringField())

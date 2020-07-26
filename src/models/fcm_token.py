from src.conf.database import db


class FCMToken(db.Document):
    user = db.StringField(required=True)
    tokens = db.ListField(db.StringField())

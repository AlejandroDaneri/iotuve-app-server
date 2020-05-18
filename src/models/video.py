import datetime
from src.conf.database import db


class Video(db.Document):
    title = db.StringField(required=False, default=None)
    description = db.StringField(required=False, default=None)
    visibility = db.StringField(required=True)
    media = db.DictField(required=True)
    statics = db.DictField(
        required=False,
        default=dict(
            likes=dict(count=0, users=[]),
            dislikes=dict(count=0, users=[]),
            views=dict(count=0, users=[])))
    location = db.DictField(required=False, default=None)
    comments = db.ListField(required=False, default=None)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)
    date_updated = db.ComplexDateTimeField(required=True)

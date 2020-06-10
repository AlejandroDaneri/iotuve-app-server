from src.conf.database import db


class Video(db.Document):
    title = db.StringField(required=False, default=None)
    description = db.StringField(required=False, default=None)
    visibility = db.StringField(required=True)
    location = db.DictField(required=False, default=None)
    count_likes = db.IntField(required=True, default=0)
    count_dislikes = db.IntField(required=True, default=0)
    count_views = db.IntField(required=True, default=0)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)
    date_updated = db.ComplexDateTimeField(required=True)

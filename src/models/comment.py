from src.conf.database import db


class Comment(db.Document):
    content = db.StringField(required=True)
    video = db.StringField(required=True)
    parent = db.StringField(required=False)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)
    date_updated = db.ComplexDateTimeField(required=True)

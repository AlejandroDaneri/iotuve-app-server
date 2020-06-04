from src.conf.database import db
from src.models.video import Video


class Comment(db.Document):
    content = db.StringField(required=True)
    video = db.LazyReferenceField(Video)
    parent = db.LazyReferenceField('self', required=False)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)
    date_updated = db.ComplexDateTimeField(required=True)

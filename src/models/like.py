from src.conf.database import db
from src.models.video import Video


class Like(db.Document):
    video = db.LazyReferenceField(Video)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)

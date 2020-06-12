from src.conf.database import db
from src.models.video import Video


class Reaction:
    video = db.LazyReferenceField(Video)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)


class Like(Reaction, db.Document):
    pass


class Dislike(Reaction, db.Document):
    pass


class View(Reaction, db.Document):
    pass

from src.conf.database import db
from src.models.video import Video


class Reaction:
    video = db.LazyReferenceField(Video)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)


class Like(Reaction, db.Document):
    video = db.LazyReferenceField(Video)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)

    @staticmethod
    def count_by_user(user):
        return Like.objects(user=user).count()


class Dislike(Reaction, db.Document):
    video = db.LazyReferenceField(Video)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)

    @staticmethod
    def count_by_user(user):
        return Dislike.objects(user=user).count()


class View(Reaction, db.Document):
    video = db.LazyReferenceField(Video)
    user = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)

    @staticmethod
    def count_by_user(user):
        return View.objects(user=user).count()

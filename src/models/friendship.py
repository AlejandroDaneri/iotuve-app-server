from src.conf.database import db


class Friendship(db.Document):
    from_user = db.StringField(required=True)
    to_user = db.StringField(required=True)
    message = db.StringField(required=False)
    status = db.StringField(required=True)
    date_created = db.ComplexDateTimeField(required=True)
    date_updated = db.ComplexDateTimeField(required=True)


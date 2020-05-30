from src.conf.database import db


class Stat(db.Document):
    timestamp = db.DateTimeField(required=True)
    version = db.StringField(required=True)
    status = db.IntField(required=True)
    time = db.FloatField(required=True)
    request_id = db.StringField(required=True)
    remote_ip = db.StringField(required=True)
    method = db.StringField(required=True)
    host = db.StringField(required=True)
    path = db.StringField(required=True)
    full_path = db.StringField(required=True)
    headers = db.DictField(required=False)

from src.conf.database import db


class Stat(db.Document):
    version = db.StringField(required=True)
    status = db.IntField(required=True)
    time = db.FloatField(required=True)
    full_path = db.StringField(required=True)
    request_id = db.StringField(required=True)
    timestamp = db.DateTimeField(required=True)

    def to_json(self):
        stat = dict(
            id=str(self.id),
            version=self.version,
            status=int(self.status),
            time=str(self.time),
            full_path=self.full_path,
            request_id=self.request_id,
            timestamp=str(self.timestamp)
        )
        return stat

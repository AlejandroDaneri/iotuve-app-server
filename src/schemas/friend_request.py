from marshmallow import Schema, fields, validate, EXCLUDE
import datetime


class FriendRequestSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    _id = fields.Int(dump_only=True)
    user_from = fields.Str(required=True, attribute="from")
    user_to = fields.Str(required=True, attribute="to")
    message = fields.Str(required=True, validate=validate.Length(min=0, max=150))
    status = fields.Str(required=False, validate=validate.OneOf(["pending", "approved", "declined"]), default="pending")
    date_created = fields.DateTime(required=False, default=datetime.datetime.now(), dump_only=True)
    date_updated = fields.DateTime(required=False, default=datetime.datetime.now(), dump_only=True)

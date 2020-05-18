from marshmallow import Schema, fields, validate, EXCLUDE
from src.schemas.user import UserSchema


class CommentSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    comment = fields.Str(required=True, validate=validate.Length(min=1))
    user = fields.Nested(UserSchema)
    #children = fields.List(CommentSchema, allow_none=True, default=None)

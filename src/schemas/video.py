from marshmallow import Schema, fields, validate, EXCLUDE, post_load
from src.schemas.comment import CommentSchema
from src.schemas.location import LocationSchema
from src.models.video import Video


class StaticSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    count = fields.Int(required=True)
    users = fields.List(fields.Str, required=True)


class StaticsSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    views = fields.Nested(StaticSchema, required=True)
    likes = fields.Nested(StaticSchema, required=True)
    dislikes = fields.Nested(StaticSchema, required=True)


class MediaSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True, dump_only=True)
    url = fields.URL(required=True)


class VideoSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True, dump_only=True)
    title = fields.Str(required=False, validate=validate.Length(max=100), default=None)
    description = fields.Str(required=False, validate=validate.Length(max=300), default=None)
    visibility = fields.Str(required=True, validate=validate.OneOf(["public", "private"]))
    media = fields.Nested(MediaSchema, required=True)
    statics = fields.Nested(StaticsSchema, allow_none=True, dump_only=True, default=None)
    location = fields.Nested(LocationSchema, allow_none=True, default=None)
    comments = fields.List(fields.Nested(CommentSchema), allow_none=True, dump_only=True, default=None)
    user = fields.Str(required=True, dump_only=True)
    date_created = fields.DateTime(required=True, dump_only=True)
    date_updated = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return Video(**data)

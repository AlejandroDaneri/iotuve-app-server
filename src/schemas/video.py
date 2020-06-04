from marshmallow import Schema, fields, validate, EXCLUDE, post_load
from src.schemas.location import LocationSchema
from src.schemas.pagination import PaginationSchema
from src.models.video import Video
from src.misc.validators import ObjectIdValidator


class MediaSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    video_id = fields.Str(required=True, dump_only=True)
    user_id = fields.Str(required=True, dump_only=True)
    name = fields.String(required=True)
    size = fields.Float(required=True)
    type = fields.Str(requirede=True)
    date_created = fields.DateTime(required=True)


class StaticSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    count = fields.Int(required=True)
    users = fields.List(fields.Str, required=True)


class StatisticsSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    views = fields.Nested(StaticSchema, required=True)
    likes = fields.Nested(StaticSchema, required=True)
    dislikes = fields.Nested(StaticSchema, required=True)


class VideoSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True, dump_only=True)
    title = fields.Str(required=False, validate=validate.Length(max=100), default=None)
    description = fields.Str(required=False, validate=validate.Length(max=300), default=None)
    visibility = fields.Str(required=True, validate=validate.OneOf(["public", "private"]))
    statistics = fields.Nested(StatisticsSchema, dump_only=True, default=None)
    location = fields.Nested(LocationSchema, allow_none=True, default=None)
    user = fields.Str(required=True, dump_only=True)
    date_created = fields.DateTime(required=True, dump_only=True)
    date_updated = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_video(self, data, **kwargs):
        return Video(**data)


class VideoPaginatedSchema(PaginationSchema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=False, validate=ObjectIdValidator(error="Is not a valid Video Id"))
    visibility = fields.Str(required=False, validate=validate.OneOf(["public", "private"]))
    user = fields.Str(required=False)

    @post_load
    def make_paginated(self, data, **kwargs):
        limit = data.pop("limit")
        offset = data.pop("offset")
        return dict(filters=data, limit=limit, offset=offset)

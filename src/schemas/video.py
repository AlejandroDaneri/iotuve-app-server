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


class VideoSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True, dump_only=True)
    title = fields.Str(required=False, validate=validate.Length(max=100), default=None)
    description = fields.Str(required=False, validate=validate.Length(max=300), default=None)
    visibility = fields.Str(required=True, validate=validate.OneOf(["public", "private"]))
    location = fields.Nested(LocationSchema, allow_none=True, default=None)
    count_likes = fields.Int(dump_only=True, default=0)
    count_dislikes = fields.Int(dump_only=True, default=0)
    count_views = fields.Int(dump_only=True, default=0)
    user = fields.Str(required=True, dump_only=True)
    date_created = fields.DateTime(required=True, dump_only=True)
    date_updated = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_video(self, data, **kwargs):
        return Video(**data)


class VideoPaginatedSchema(PaginationSchema):
    id = fields.Str(required=False, validate=ObjectIdValidator(error="Is not a valid Video Id"))
    visibility = fields.Str(required=False, validate=validate.OneOf(["public", "private"]))
    user = fields.Str(required=False)

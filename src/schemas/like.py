from marshmallow import Schema, fields, EXCLUDE, post_load
from src.schemas.pagination import PaginationSchema
from src.models.like import Like
from src.misc.validators import ObjectIdValidator, ObjectIdField


class LikeSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    video = ObjectIdField(required=True)
    user = fields.Str(required=True)
    date_created = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_like(self, data, **kwargs):
        return Like(**data)


class LikePaginatedSchema(PaginationSchema):

    class Meta:
        unknown = EXCLUDE

    video = fields.Str(required=False, validate=ObjectIdValidator(error="Is not a valid Video Id"))
    user = fields.Str(required=False)

    @post_load
    def make_paginated(self, data, **kwargs):
        limit = data.pop("limit")
        offset = data.pop("offset")
        return dict(filters=data, limit=limit, offset=offset)

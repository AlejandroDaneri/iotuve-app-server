from marshmallow import Schema, fields, validate, EXCLUDE, post_load
from src.models.comment import Comment
from src.schemas.pagination import PaginationSchema
from src.misc.validators import ObjectIdValidator



class CommentSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    content = fields.Str(required=True, validate=validate.Length(min=1, max=2200))
    video = fields.Str(required=True, validate=validate.Length(min=1))
    parent = fields.Str(required=False)
    user = fields.Str(required=True, dump_only=True)
    date_created = fields.DateTime(required=True, dump_only=True)
    date_updated = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_comment(self, data, **kwargs):
        return Comment(**data)


class CommentPaginatedSchema(PaginationSchema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=False, validate=ObjectIdValidator(error="Is not a valid Comment Id"))
    video = fields.Str(required=False, validate=ObjectIdValidator(error="Is not a valid Video Id"))
    parent = fields.Str(required=False, validate=ObjectIdValidator(error="Is not a valid Comment Id"))

    @post_load
    def make_paginated(self, data, **kwargs):
        limit = data.pop("limit")
        offset = data.pop("offset")
        return dict(filters=data, limit=limit, offset=offset)

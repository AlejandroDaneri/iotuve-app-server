from marshmallow import Schema, fields, EXCLUDE, INCLUDE, post_load
from src.models.stat import Stat
from src.schemas.pagination import PaginationSchema


class StatSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True, dump_only=True)
    timestamp = fields.DateTime(required=True)
    version = fields.Str(required=True)
    status = fields.Int(required=True)
    time = fields.Float(required=True)
    request_id = fields.Str(required=True)
    remote_ip = fields.Str(required=True)
    method = fields.Str(required=True)
    host = fields.Str(required=True)
    path = fields.Str(required=True)
    full_path = fields.Str(required=True)
    headers = fields.Dict(required=True)

    @post_load
    def make_stat(self, data, **kwargs):
        return Stat(**data)


class StatPaginatedSchema(PaginationSchema):

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_paginated(self, data, **kwargs):
        limit = data.pop("limit")
        offset = data.pop("offset")
        return dict(filters=data, limit=limit, offset=offset)

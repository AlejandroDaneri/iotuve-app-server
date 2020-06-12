from marshmallow import Schema, fields, validate, post_load, EXCLUDE


class PaginationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    limit = fields.Int(
        required=False,
        validate=(validate.Range(min=1, max_inclusive=50),
                  validate.OneOf([10, 20, 30, 40, 50])), default=10, missing=10)
    offset = fields.Int(required=False, validate=validate.Range(min=0), default=0, missing=0)

    @post_load
    def make_paginated(self, data, **kwargs):
        limit = data.pop("limit")
        offset = data.pop("offset")
        return dict(filters=data, limit=limit, offset=offset)

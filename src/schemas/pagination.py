from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    limit = fields.Int(required=True, validate=validate.Range(min=1, max_inclusive=50), default=10)
    offset = fields.Str(required=True, validate=validate.Range(min=0), default=0)

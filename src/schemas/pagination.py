from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    limit = fields.Int(
        required=False,
        validate=(validate.Range(min=1, max_inclusive=50),
                  validate.OneOf([10, 20, 30, 40, 50])), default=10, missing=10)
    offset = fields.Int(required=False, validate=validate.Range(min=0), default=0, missing=0)

from marshmallow import Schema, fields, EXCLUDE
from src.schemas.pagination import PaginationSchema


class ReactionSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    user = fields.Str(required=True)
    date_created = fields.DateTime(required=True, dump_only=True)


class ReactionPaginatedSchema(PaginationSchema):
    user = fields.Str(required=False)


from marshmallow import Schema, fields, validate, EXCLUDE, post_load
from src.models.friendship import Friendship
from src.schemas.pagination import PaginationSchema


class FriendshipSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True, dump_only=True)
    from_user = fields.Str(required=True, dump_only=True)
    to_user = fields.Str(required=True)
    message = fields.Str(required=True, validate=validate.Length(min=0, max=150))
    status = fields.Str(required=False, validate=validate.OneOf(["pending", "approved"]), default="pending")
    date_created = fields.DateTime(required=True, dump_only=True)
    date_updated = fields.DateTime(required=True, dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return Friendship(**data)


class FriendshipPaginatedSchema(PaginationSchema):
    from_user = fields.Str(required=False)
    to_user = fields.Str(required=False)
    status = fields.Str(required=False)

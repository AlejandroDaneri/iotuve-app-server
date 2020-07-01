from marshmallow import Schema, fields, EXCLUDE


class AvatarSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    user_id = fields.Str(required=True, dump_only=True)
    name = fields.String(required=True)

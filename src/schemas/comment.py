from marshmallow import Schema, fields, validate, EXCLUDE


class CommentSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    comment = fields.Str(required=True, validate=validate.Length(min=1, max=2200))
    user = fields.Str(required=True, dump_only=True)
    date_created = fields.DateTime(required=True, dump_only=True)
    date_updated = fields.DateTime(required=True, dump_only=True)


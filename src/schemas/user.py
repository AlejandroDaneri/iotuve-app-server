from marshmallow import Schema, fields, validate, EXCLUDE


class ContactSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True, validate=validate.Email())
    phone = fields.Str(required=True, validate=validate.Length(min=8))


class AvatarSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    url = fields.Url(required=True)


class UserSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    contact = fields.Nested(ContactSchema)
    avatar = fields.Nested(AvatarSchema)

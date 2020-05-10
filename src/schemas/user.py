from marshmallow import Schema, fields, post_load, validate, EXCLUDE
# from src.dtos.user import User, Contact, Avatar


class ContactSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True, validate=validate.Email())
    phone = fields.Str(required=True, validate=validate.Length(min=8))

    #@post_load
    #def make_contact(self, data, **kwargs):
    #    return Contact(**data)


class AvatarSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    url = fields.Url(required=True)

    #@post_load
    #def make_avatar(self, data, **kwargs):
    #    return Avatar(**data)


class UserSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    contact = fields.Nested(ContactSchema)
    avatar = fields.Nested(AvatarSchema)

    #@post_load
    #def make_user(self, data, **kwargs):
    #    return User(**data)


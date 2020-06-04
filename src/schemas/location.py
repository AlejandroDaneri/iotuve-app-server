from marshmallow import Schema, fields, validate, EXCLUDE


class LocationSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    longitude = fields.Number(required=True)
    latitude = fields.Number(required=True)

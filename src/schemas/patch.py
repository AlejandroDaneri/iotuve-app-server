# from marshmallow import Schema, fields, validate
#
#
# class PatchSchema(Schema):
#     op = fields.Str(required=True, validate=validate.OneOf(["add", "remove", "replace", "move", "copy"]))
#     path = fields.Str(required=True)
#     value = fields.Str(required=True)
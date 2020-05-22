import typing
from bson import ObjectId
from marshmallow.validate import Validator, ValidationError


class ObjectIdValidator(Validator):
    """Validate an id.

    :param error: Error message to raise in case of a validation error. Can be
        interpolated with `{input}`.
    """

    default_message = "Not a valid id."

    def __init__(self, *, error: str = None):
        self.error = error or self.default_message  # type: str

    def _format_error(self, value) -> typing.Any:
        return self.error.format(input=value)

    def __call__(self, value) -> typing.Any:
        message = self._format_error(value)

        if not value:
            raise ValidationError(message)

        if not ObjectId.is_valid(value):
            raise ValidationError(message)

        return value

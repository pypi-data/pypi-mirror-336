"""Module contains schema entity."""
from __future__ import annotations
from typing import Any
from typing import Dict

from oapi3.exceptions import BodyValidationError
from oapi3.exceptions import SchemaValidationError
from oapi3.jsonschema_validator import Validator
from oapi3.jsonschema_validator import ValidationError

from .base import Entity


class SchemaEntity(Entity[Dict[str, Any]]):
    """Schema entity represents Schema Object.

    https://spec.openapis.org/oas/v3.1.0#schema-object
    """

    __slots__ = ["validator"]

    def __init__(self, obj: dict[str, Any]):
        super().__init__(obj)
        self.validator = Validator(dict(obj))

    def validate(self, value: Any) -> None:
        """Validate value by schema."""
        try:
            self.validator.validate(value)
        except ValidationError as exc:
            raise BodyValidationError(
                str(SchemaValidationError(exc.absolute_path, exc.message)),
            ) from exc

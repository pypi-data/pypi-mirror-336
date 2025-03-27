"""Module contains patched jsonschema validator.

>>> form oapi3.jsonschema_validator import Validator
>>> validator = Validator(schema)
>>> validator.valiate(instance)
"""
# ruff: noqa: ANN202
# ruff: noqa: ANN001
from __future__ import annotations
from typing import Any

import datetime

import jsonschema
from jsonschema._utils import load_schema
from jsonschema import _validators
from jsonschema import validators
from jsonschema import FormatChecker
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError


__all__ = (
    "DraftOpenapi3",
    "ValidationError",
    "Validator",
)


format_checker = FormatChecker()


@format_checker.checks("date-time")
def validate_datetime(value):
    """Validate date-time format."""
    try:
        datetime.datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


draft_openapi3_meta_schema = load_schema("draft4")
# Disable Draft4 schema validator
draft_openapi3_meta_schema["$schema"] = "DraftOpenai3"
# Add disctiminator schema
draft_openapi3_meta_schema["properties"]["discriminator"] = {
    "type": "object",
    "properties": {
        "propertyName": {"type": "string"},
        "mapping": {"type": "object"},
    },
    "required": ["propertyName", "mapping"],
}


def discriminator_validator(validator, one_of, instance, schema):
    """Descriminator json schema validator."""
    discriminator = schema.get("discriminator")
    property_name = discriminator["propertyName"]
    mapping = discriminator["mapping"]
    errs = list(validator.descend(
        instance,
        {
            "type": "object",
            "properties": {
                property_name: {
                    "type": "string",
                    "enum": list(mapping),
                },
            },
            "required": [property_name],
        },
    ))
    if errs:
        yield errs[0]
        return

    descr_value = instance[property_name]
    descr_schema = mapping[descr_value]

    try:
        index = one_of.index(descr_schema)
    except ValueError:
        yield SchemaError("descriminator error")
        return
    yield from validator.descend(instance, descr_schema, schema_path=index)


def one_of_draft_openapi3(validator, one_of, instance, schema):
    """OneOf json schema validator. Add openapi3 discriminator support."""
    if "discriminator" in schema:
        yield from discriminator_validator(validator, one_of, instance, schema)
    else:
        yield from _validators.oneOf(validator, one_of, instance, schema)


def ref_openapi3(validator, ref, instance, schema):
    """$ref json schema validator. Skip recursive refs."""
    if not isinstance(instance, dict):
        return None
    items = instance.get("items", {})
    if not isinstance(items, dict):
        return None
    properties = items.get("properties", {}).values()
    if instance in properties:
        return None
    return _validators.ref(validator, ref, instance, schema)


DraftOpenapi3 = validators.create(
    meta_schema=draft_openapi3_meta_schema,
    validators={
        **validators.Draft4Validator.VALIDATORS,
        "$ref": ref_openapi3,
        "oneOf": one_of_draft_openapi3,
    },
    version="draft_openapi3",
    format_checker=format_checker,
)


def drop_cyclic_refs(value: Any, stack: list):
    """Drop cyclic refs in value."""
    if value in stack:
        return type(value)()
    if isinstance(value, dict):
        return {
            k: drop_cyclic_refs(v, [*stack, value]) for k, v in value.items()
        }
    if isinstance(value, list):
        return [drop_cyclic_refs(v, [*stack, value]) for v in value]
    return value


class Validator:
    """Josnschema validator wrapper."""

    def __init__(self, schema: dict[str, Any]):
        DraftOpenapi3.check_schema(drop_cyclic_refs(schema, []))
        self._validator = DraftOpenapi3(schema, format_checker=format_checker)

    def validate(self, instance: Any) -> None:
        """Validate json by json schema."""
        error = jsonschema.exceptions.best_match(
            self._validator.iter_errors(instance),
        )
        if error is not None:
            raise error

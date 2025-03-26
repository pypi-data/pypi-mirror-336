"""Module contain classes for serialize, deserialize and validate params."""
from __future__ import annotations

from typing import Any
try:
    from typing import TypedDict
    from typing import NotRequired
except ImportError:
    from typing_extensions import TypedDict
    from typing_extensions import NotRequired
import json
import abc

from oapi3.exceptions import ParameterTypeError
from oapi3.exceptions import SchemaValidationError
from oapi3.jsonschema_validator import Validator
from oapi3.jsonschema_validator import ValidationError

from .base import Entity


IMPLIMENTED_IN_VALUES: list[str] = ["path", "query"]


"""Parameter Object typed dict."""
ParameterObject = TypedDict(
    "ParameterObject",
    {
        "name": str,
        "content": "NotRequired[dict[str, Any]]",
        "style": "NotRequired[str]",
        "in": str,
        "explode": "NotRequired[bool]",
        "required": "NotRequired[bool]",
        "schema": "NotRequired[dict]",
    },
)


class ParameterEntity(Entity[ParameterObject]):
    """Parameter Entity represents Parameter Object.

    https://spec.openapis.org/oas/v3.1.0#parameter-object
    """

    __slots__ = [
        "required",
        "schema",
    ]
    required: bool
    schema: dict

    def __init__(self, parameter_obj: ParameterObject):
        super().__init__(parameter_obj)
        self.required = parameter_obj.get("required", False)
        self.schema = self._schema()

    @abc.abstractmethod
    def serialize(self, value: Any) -> str:
        """Serialize value."""

    @abc.abstractmethod
    def deserialize(self, value: str) -> Any:
        """Deserialize value."""

    @abc.abstractmethod
    def _schema(self) -> dict:
        """Get or create schema."""


class JsonParameterEntity(ParameterEntity):
    """Parameter entity for params with conent type "application/json"."""

    def serialize(self, value: Any) -> str:
        """Serialize value."""
        return json.dumps(value)

    def deserialize(self, value: str) -> Any:
        """Deserialize value."""
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError as exc:
            raise ParameterTypeError(
                self.obj["name"],
                value,
                "application/json",
            ) from exc

    def _schema(self) -> dict:
        content_type_obj = self.obj["content"]["application/json"]
        return content_type_obj.get("schema", {})


class PrimitiveParameterEntity(ParameterEntity):
    """Parameter entity for simple parameters."""

    def serialize(self, value: Any) -> str:
        """Serialize value."""
        return str(value)

    def deserialize(self, value: str) -> Any:
        """Deserialize value."""
        return value

    def _schema(self) -> dict:
        return self.obj.get("schema", {})


class StringParameterEntity(PrimitiveParameterEntity):
    """Parameter entity for simple string parameters."""


class IntegerParameterEntity(PrimitiveParameterEntity):
    """Parameter entity for simple integer parameters."""

    def deserialize(self, value: str) -> Any:
        """Deserialize value."""
        try:
            return int(value)
        except ValueError:
            # Not raise exception. It will be raised in schema validation.
            return value


class BooleanParameterEntity(PrimitiveParameterEntity):
    """Parameter entity for simple boolean parameters."""

    def serialize(self, value: Any) -> str:
        """Serialize value."""
        if value:
            return "1"
        return ""

    def deserialize(self, value: str) -> Any:
        """Deserialize value."""
        return bool(value)


class ArrayParameterEntity(PrimitiveParameterEntity):
    """Base parameter entity class for array parameters."""

    __slots__ = [
        "inner_schema",
    ]
    inner_schema: ParameterEntity

    def __init__(self, parameter_obj: ParameterObject):
        super().__init__(parameter_obj)
        inner_schema_obj = self.schema.get("items", {})
        inner_type = inner_schema_obj.get("type")
        self.inner_schema = PRIMITIVE_SCHEMAS[inner_type](
            {
                "name": '{{self.obj["name"]}}[]',
                "in": self.obj["in"],
                "schema": inner_schema_obj,
            },
        )


class DelemitedArrayParameterEntity(ArrayParameterEntity):
    """Base parameter entity for delimitted array parameter."""

    @property
    @abc.abstractmethod
    def delimiter(self) -> str:
        """Array delimiter."""

    def serialize(self, value: Any) -> str:
        """Serialize value."""
        return self.delimiter.join(
            [self.inner_schema.serialize(item) for item in value],
        )

    def deserialize(self, value: str) -> Any:
        """Deserialize value."""
        if not value:
            return []
        return [
            self.inner_schema.deserialize(item)
            for item in value.split(self.delimiter)
        ]


class FormNEArrayParameterEntity(DelemitedArrayParameterEntity):
    """Parameter entity for form not explode array parameters."""

    delimiter: str = ","


class PipedelimitedNEArrayParameterEntity(DelemitedArrayParameterEntity):
    """Parameter entity for pipedelimited not explode array parameters."""

    delimiter: str = "|"


class SpacedelimitedNEArrayParameterEntity(DelemitedArrayParameterEntity):
    """Parameter entity for pipedelimited not explode array parameters."""

    delimiter: str = " "


CONTENT_PARAM_TYPES = {
    "application/json": JsonParameterEntity,
}

PRIMITIVE_SCHEMAS = {
    None: PrimitiveParameterEntity,
    "string": StringParameterEntity,
    "integer": IntegerParameterEntity,
    "long": IntegerParameterEntity,
    "double": IntegerParameterEntity,
    "boolean": BooleanParameterEntity,
}

ARRAY_SCHEMAS: dict[tuple[str, bool], type[DelemitedArrayParameterEntity]] = {
    ("form", False): FormNEArrayParameterEntity,
    ("pipedelimited", False): PipedelimitedNEArrayParameterEntity,
    ("spacedelimited", False): SpacedelimitedNEArrayParameterEntity,
}

IMPLEMENTED_PARAM_TYPES: dict[tuple[str, str, bool], list[str | None]] = {
    ("path", "simple", False): list(PRIMITIVE_SCHEMAS),
    ("query", "form", True): list(PRIMITIVE_SCHEMAS),
    ("query", "form", False): [*PRIMITIVE_SCHEMAS, "array"],
    ("query", "pipedelimited", False): ["array"],
    ("query", "spacedelimited", False): ["array"],
}


def create_parameter_entity(parameter_obj: ParameterObject) -> ParameterEntity:
    """Create param schema by param_obj."""
    if "content" in parameter_obj:
        return _create_parameter_entity_by_content(parameter_obj)
    return _create_parameter_entity_by_schema(parameter_obj)


def _create_parameter_entity_by_content(
    parameter_obj: ParameterObject,
) -> ParameterEntity:
    content_type = next(iter(parameter_obj["content"]), None)
    if content_type:
        schema_cls = CONTENT_PARAM_TYPES.get(content_type)
        if schema_cls:
            return schema_cls(parameter_obj)
    msg = f"Unknown param content_type {content_type}"
    raise NotImplementedError(msg)


def _create_parameter_entity_by_schema(
    parameter_obj: ParameterObject,
) -> ParameterEntity:
    schema = parameter_obj.get("schema", {})
    parameter_type = schema.get("type")
    # https://spec.openapis.org/oas/latest.html#parameter-object
    if "style" in parameter_obj:
        style = parameter_obj["style"]
    elif parameter_obj["in"] == "path":
        style = "simple"
    elif parameter_obj["in"] == "query":
        style = "form"
    if "explode" in parameter_obj:
        explode = parameter_obj["explode"]
    elif style == "form":
        explode = True
    else:
        explode = False

    implemented_types = IMPLEMENTED_PARAM_TYPES.get(
        (parameter_obj["in"], style, explode),
        [],
    )
    if parameter_type in implemented_types:
        if parameter_type in PRIMITIVE_SCHEMAS:
            return PRIMITIVE_SCHEMAS[parameter_type](parameter_obj)
        if parameter_type == "array":
            inner_type = parameter_obj["schema"].get("itmes", {}).get("type")
            if inner_type not in PRIMITIVE_SCHEMAS:
                msg = (
                    f'Param name={parameter_obj["name"]}: '
                    f'inner type {inner_type} not implemented'
                )
                raise NotImplementedError(msg)
            return ARRAY_SCHEMAS[(style, explode)](parameter_obj)
    msg = (
        f'Param name={parameter_obj["name"]} in={parameter_obj["in"]} '
        f'style={style} explode={explode} type={parameter_type}'
    )
    raise NotImplementedError(msg)


class ParametersEntity(Entity):
    """Parameters Entity represents parameters list in
    PathObject or OperationObject.

    https://spec.openapis.org/oas/v3.1.0#path-item-object
    https://spec.openapis.org/oas/v3.1.0#operation-object
    """

    __slots__ = ["parameters", "schema", "validators"]
    parameters: dict[str, dict[str, ParameterEntity]]
    schema: dict[str, dict]

    def __init__(self, parameter_objs: list[ParameterObject]):
        super().__init__(parameter_objs)
        self.parameters = {in_: {} for in_ in IMPLIMENTED_IN_VALUES}
        for obj in parameter_objs:
            if obj["in"] not in IMPLIMENTED_IN_VALUES:
                continue
            self.parameters[obj["in"]][obj["name"]] = create_parameter_entity(
                obj,
            )
        self.schema = {in_: self._schema(in_) for in_ in IMPLIMENTED_IN_VALUES}
        self.validators = {k: Validator(v) for k, v in self.schema.items()}

    def deserialize(self, in_: str, values: dict[str, str]) -> dict[str, Any]:
        """Deserialize parameters."""
        if in_ not in IMPLIMENTED_IN_VALUES:
            raise NotImplementedError(in_)
        return {
            **values,
            **{
                k: self.parameters[in_][k].deserialize(v)
                for k, v in values.items()
                if k in self.parameters[in_]
            },
        }

    def serialize(self, in_: str, values: dict[str, Any]) -> dict[str, str]:
        """Serialize parameters."""
        if in_ not in IMPLIMENTED_IN_VALUES:
            raise NotImplementedError(in_)
        return {
            **values,
            **{
                k: self.parameters[in_][k].serialize(v)
                for k, v in values.items()
                if k in self.parameters[in_]
            },
        }

    def validate(self, in_: str, values: dict[str, Any]) -> None:
        """Validate parameters dict by parameter_objs dict."""
        if in_ not in IMPLIMENTED_IN_VALUES:
            raise NotImplementedError(in_)
        try:
            self.validators[in_].validate(values)
        except ValidationError as exc:
            raise SchemaValidationError(
                exc.absolute_path,
                exc.message,
            ) from exc

    def _schema(self, in_: str) -> dict:
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                k: v.schema for k, v in self.parameters[in_].items()
            },
        }
        required = [k for k, v in self.parameters[in_].items() if v.required]
        if required:
            schema["required"] = required
        return schema

"""Module contain PathEntity and PathEntity classes."""
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import cast
try:
    from typing import TypedDict
    from typing import NotRequired
except ImportError:
    from typing_extensions import TypedDict
    from typing_extensions import NotRequired
import re

from oapi3.exceptions import PathNotFoundError
from oapi3.exceptions import OperationNotAllowedError

from .base import Entity
from .operations import OperationEntity
from .operations import OperationObject
from .operations import METHODS

if TYPE_CHECKING:
    from .parameters import ParameterObject


class PathObject(TypedDict):
    """Path object typed dict."""

    parameters: NotRequired[list[ParameterObject]]

    get: OperationObject
    put: OperationObject
    post: OperationObject
    delete: OperationObject
    options: OperationObject
    head: OperationObject
    patch: OperationObject
    trace: OperationObject


class PathEntity(Entity[PathObject]):
    """Path Entity represents Path Object.

    https://spec.openapis.org/oas/v3.1.0#path-item-object
    """

    __slots__ = [
        "operations",
        "parameters",
        "parts",
        "path_param_names",
        "pattern",
        "regex",
    ]
    parts: list[str]
    pattern: str
    path_param_names: list[str]
    regex: re.Pattern
    operations: dict[str, OperationEntity]

    def __init__(self, pattern: str, path_obj: PathObject):
        super().__init__(path_obj)
        self.pattern = pattern
        self.parts = pattern.split("/")[1:]
        self.path_param_names = re.findall(r"\{([0-9a-zA-Z_]+)\}", pattern)
        self.regex = re.compile(
            re.sub(
                r"\{[0-9a-zA-Z_]+\}",
                r"([0-9a-zA-Z_\-\.]+)",
                pattern,
            ) + "$",
        )
        parameters_obj = path_obj.get("parameters", [])
        self.operations = {
            method: OperationEntity(
                method,
                cast("OperationObject", obj),
                parameters_obj,
            ) for method, obj in path_obj.items() if method in METHODS
        }

    def match(self, path: str) -> bool:
        """Match path."""
        return bool(self.regex.match(path))

    def parse_path_parameters(self, path: str) -> dict:
        """Get path parameters from path."""
        result = self.regex.match(path)
        if not result:
            return {}
        return dict(zip(self.path_param_names, result.groups()))

    def match_operation(self, operation: str) -> OperationEntity:
        """Match http operation(method)."""
        operation_entity = self.operations.get(operation)
        if not operation_entity:
            raise OperationNotAllowedError(operation, list(self.operations))
        return operation_entity


class PathsEntity(Entity):
    """Paths Entity represents Paths Object.

    https://spec.openapis.org/oas/v3.1.0#paths-object
    """

    __slots__ = [
        "paths",
    ]
    paths: list[PathEntity]

    def __init__(self, paths_obj: dict):
        super().__init__(paths_obj)
        self.paths = [PathEntity(k, v) for k, v in paths_obj.items()]
        self.paths.sort(key=lambda x: x.parts)

    def match_path(self, path: str) -> PathEntity:
        """Match path."""
        for path_entity in self.paths:
            if path_entity.match(path):
                return path_entity
        raise PathNotFoundError(path)

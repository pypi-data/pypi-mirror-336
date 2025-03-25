"""Module conatins Schema class."""
from __future__ import annotations
from typing import Any
from typing import Iterator

from .entities import PathsEntity
from .entities import OperationEntity
from .exceptions import SchemaValidationError
from .exceptions import ParameterTypeError
from .exceptions import PathParamValidationError
from .exceptions import QueryParamValidationError


class Schema(dict):
    """Schema for validating reauests and responses."""

    paths_entity: PathsEntity
    operations: dict[str, tuple[str, str, OperationEntity]]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.paths_entity = PathsEntity(self["paths"])
        self.operations = {
            entity.operation_id: (path, method, entity)
            for path, method, entity in self._iter_operations()
        }

    def validate_request(
        self,
        path: str,
        operation: str,
        query: dict[str, Any],
        media_type: str,
        body: Any,
    ) -> dict[str, Any]:
        """Validate request."""
        path_entity = self.paths_entity.match_path(path)
        path_params = path_entity.parse_path_parameters(path)

        operation_entity = path_entity.match_operation(operation)
        parameters_entity = operation_entity.parameters
        # Validate path params
        try:
            path_params = parameters_entity.deserialize("path", path_params)
            parameters_entity.validate("path", path_params)
        except (SchemaValidationError, ParameterTypeError) as exc:
            raise PathParamValidationError(str(exc)) from exc
        # Validate query params
        try:
            query_params = parameters_entity.deserialize("query", query)
            parameters_entity.validate("query", query_params)
        except (SchemaValidationError, ParameterTypeError) as exc:
            raise QueryParamValidationError(str(exc)) from exc
        # Validate body
        if operation_entity.request_body:
            content = operation_entity.request_body.content
            media_type_entity = content.match_media_type(media_type)
            media_type_entity.validate_body(body)
            body_dict = media_type_entity.get_body_value(body)
        else:
            body_dict = {}
        return {
            "path": path,
            "operation": operation,
            "operation_id": operation_entity.operation_id,
            "query": query_params,
            "query_params_dict": query_params,
            "media_type": media_type,
            "body": body,
            "body_dict": body_dict,
            "path_params": path_params,
            "path_params_dict": path_params,
            "query_params": query_params,
        }

    def validate_response(
        self,
        path: str,
        operation: str,
        status_code: int,
        media_type: str,
        body: Any,
    ) -> dict[str, Any]:
        """Validate http response."""
        path_entity = self.paths_entity.match_path(path)
        operation_entity = path_entity.match_operation(operation)

        response = operation_entity.responses.match_status_code(status_code)
        if response.content:
            media_type_entity = response.content.match_media_type(media_type)
            media_type_entity.validate_body(body)

        return {
            "path": path,
            "operation": operation,
            "media_type": media_type,
            "body": body,
        }

    def _iter_operations(self) -> Iterator[tuple[str, str, OperationEntity]]:
        """Iter operations flat list."""
        for path_entity in self.paths_entity.paths:
            for method, operation_entity in path_entity.operations.items():
                yield path_entity.pattern, method, operation_entity

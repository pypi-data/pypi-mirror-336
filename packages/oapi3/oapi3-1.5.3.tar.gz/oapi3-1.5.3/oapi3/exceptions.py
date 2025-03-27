"""Module contains exceptions."""
from __future__ import annotations

from typing import Any
from typing import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class OApiError(Exception):
    """Base oapi lib exception."""


class ApiRequestError(OApiError):
    """Api request error."""

    url: str
    error_text: str
    http_code: int | None
    error_body: Any | None

    def __init__(
        self,
        url: str,
        error_text: str,
        http_code: int | None = None,
        error_body: Any | None = None,
    ):
        super().__init__()
        self.url = url
        self.error_text = error_text
        self.http_code = http_code
        self.error_body = error_body

    def __str__(self) -> str:
        """String representation of error."""
        return (
            f"Request error <url={self.url}>: "
            "{self.http_code} {self.error_text}"
        )



class ValidationError(Exception):
    """Base schema validation error."""


class PathNotFoundError(ValidationError):
    """Path not found error."""

    path: str

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def __str__(self):
        """String representation of error."""
        return f"Path={self.path}, error: Path not found"


class PathParamValidationError(ValidationError):
    """Path parameter validation not found error."""

    message: str

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self):
        """String representation of error."""
        return f"'Path parameter validation error: {self.message}"


class OperationNotAllowedError(ValidationError):
    """Operation not allowed error."""

    operation: str
    allowed_operations: list[str]

    def __init__(self, operation: str, allowed_operations: list[str]):
        super().__init__()
        self.operation = operation
        self.allowed_operations = allowed_operations

    def __str__(self):
        """String representation of error."""
        allowed_operations_str = ", ".join(self.allowed_operations)
        return (
            f"Operation {self.operation} not allowed, "
            f"allowed_operations {allowed_operations_str}"
        )


class OperationError(ValidationError):
    """Operation error."""

    path: str
    pattern: str
    operation: str
    query: str
    error_message: str

    def __init__(
        self,
        path: str,
        pattern: str,
        operation: str,
        query: str,
        error_message: str,
    ):
        super().__init__()
        self.path = path
        self.pattern = pattern
        self.operation = operation
        self.query = query
        self.error_message = error_message

    def __str__(self):
        """String representation of error."""
        return (
            f"Path={self.path}, pattern={self.pattern}, "
            f"operation={self.operation}, query={self.query}: "
            f"{self.error_message}"
        )


class QueryParamValidationError(ValidationError):
    """Query parameter validation error."""

    message: str

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self):
        """String representation of error."""
        return f"Query parameter validation error: {self.message}"


class ParameterError(ValidationError):
    """Parameter base error."""


class ParameterTypeError(ParameterError):
    """Parameter type error."""

    name: str
    value: Any
    required_type: str
    max_param_len: int = 20

    def __init__(self, name: str, value: Any, required_type: str):
        super().__init__()
        self.name = name
        self.value = value
        self.required_type = required_type

    def __str__(self):
        """String representation of error."""
        value = str(self.value)
        if len(value) > self.max_param_len:
            value = f"{value[:self.max_param_len]}..."
        return f"Param {self.name}={value} must be {self.required_type} type"


class BodyValidationError(ValidationError):
    """Body validation error."""

    message: str

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self):
        """String representation of error."""
        return f"Body content error: {self.message}"


class MediaTypeNotAllowedError(BodyValidationError):
    """Media type not allowed error."""

    content_type: str
    allowed_content_types: list[str]

    def __init__(self, content_type: str, allowed_content_types: list[str]):
        self.content_type = content_type
        self.allowed_content_types = allowed_content_types
        allowed_content_types_str = ", ".join(allowed_content_types)
        message = (
            f"Media type {content_type} is not allowed, "
            f"allowed content types {allowed_content_types_str}"
        )
        super().__init__(message)


class JsonDecodeError(BodyValidationError):
    """Json decode erroe."""

    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"JSON decode error: {message}")


class SchemaValidationError(ValidationError):
    """Schema validation error."""

    path_parts: Sequence[str | int]
    message: str

    def __init__(self, path_parts: Sequence[str | int], message: str):
        super().__init__()
        self.path_parts = path_parts
        self.message = message

    def __str__(self):
        """String representation of error."""
        path = ".".join([str(p) for p in self.path_parts])
        return f"Schema validation error path='{path}': {self.message}"


class ResponseError(ValidationError):
    """Response error."""


class ResponseCodeNotAllowedError(ResponseError):
    """Response code not allowed error."""

    response_code: str
    allowed_codes: list[str]

    def __init__(self, response_code: str, allowed_codes: list[str]):
        super().__init__()
        self.response_code = response_code
        self.allowed_codes = allowed_codes

    def __str__(self):
        """String representation of error."""
        allowed_codes_str = ", ".join(self.allowed_codes)
        return (
            f"Response code {self.response_code} is not allowed, "
            f"allowed codes {allowed_codes_str}"
        )


class RefNotFoundError(OApiError):
    """Ref not found error."""

    file_path: Path
    ref: str

    def __init__(self, file_path: Path, ref: str):
        super().__init__()
        self.file_path = file_path
        self.ref = ref

    def __str__(self):
        """String representation of error."""
        return f"Ref not found file={self.file_path}, ref={self.ref}"

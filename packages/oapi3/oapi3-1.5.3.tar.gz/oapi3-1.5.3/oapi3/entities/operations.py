"""Module contains operation entity class."""
from __future__ import annotations

from typing import Dict
try:
    from typing import TypedDict
    from typing import NotRequired
except ImportError:
    from typing_extensions import TypedDict
    from typing_extensions import NotRequired

from .base import Entity
from .parameters import ParametersEntity
from .parameters import ParameterObject
from .media_types import ContentEntity
from .media_types import ContentObject


METHODS = {
    "get",
    "put",
    "post",
    "delete",
    "options",
    "head",
    "patch",
    "trace",
}


class RequestBodyObject(TypedDict):
    """Request body object typed dict."""

    required: NotRequired[bool]
    content: ContentObject


class RequestBodyEntity(Entity[RequestBodyObject]):
    """Request Body entity represents Request Body Object.

    https://spec.openapis.org/oas/v3.1.0#request-body-object
    """

    __slots__ = [
        "content",
        "media_types",
        "required",
    ]
    required: bool
    content: ContentEntity

    def __init__(self, request_body_obj: RequestBodyObject):
        super().__init__(request_body_obj)
        self.required = request_body_obj.get("required", False)
        self.content = ContentEntity(request_body_obj["content"])


class ResponseObject(TypedDict):
    """Request body object typed dict."""

    content: NotRequired[ContentObject]


class ResponseEntity(Entity[ResponseObject]):
    """Response entity represents Responses Object.

    https://spec.openapis.org/oas/v3.1.0#response-object
    """

    __slots__ = ["content"]
    content: ContentEntity | None

    def __init__(self, response_obj: ResponseObject):
        super().__init__(response_obj)
        content_obj = response_obj.get("content")
        if content_obj:
            self.content = ContentEntity(content_obj)
        else:
            self.content = None


ResponsesObject = Dict[str, ResponseObject]


class ResponsesEntity(Entity[ResponsesObject]):
    """Response entity represents Responses Object.

    https://spec.openapis.org/oas/v3.1.0#responses-object
    """

    __slots__ = [
        "default",
        "responses",
    ]

    default: ResponseEntity
    responses: dict[str, ResponseEntity]

    def __init__(self, responses_obj: ResponsesObject):
        super().__init__(responses_obj)
        default_obj = responses_obj.get("default") or {}
        self.default = ResponseEntity(default_obj)
        self.responses = {
            k: ResponseEntity(v)
            for k, v in responses_obj.items() if k != "default"
        }

    def match_status_code(self, status_code: int) -> ResponseEntity:
        """Match http response status code."""
        return self.responses.get(str(status_code), self.default)


class OperationObject(TypedDict):
    """OperationObject typed dict."""

    operationId: str
    parameters: NotRequired[list[ParameterObject]]
    requestBody: NotRequired[RequestBodyObject]
    responses: NotRequired[ResponsesObject]


class OperationEntity(Entity[OperationObject]):
    """Operation entity represents Operation Object.

    https://spec.openapis.org/oas/v3.1.0#operation-object
    """

    __slots__ = [
        "operation",
        "operation_id",
        "parameters",
        "request_body",
        "responses",
    ]
    operation: str
    operation_id: str
    parameters: ParametersEntity
    request_body: RequestBodyEntity | None
    responses: ResponsesEntity

    def __init__(
        self,
        operation: str,
        operation_obj: OperationObject,
        path_parameter_objs: list[ParameterObject],
    ):
        super().__init__(operation_obj)
        self.operation = operation
        self.operation_id = operation_obj["operationId"]

        operation_parameter_objs = operation_obj.get("parameters", [])
        parameter_objs = path_parameter_objs + operation_parameter_objs
        # parameters objs unique by "in" and "name" properties
        # replace path parameters by operation parameters
        unic_parameter_objs = {
            (p["in"], p["name"]): p for p in parameter_objs
        }
        self.parameters = ParametersEntity(list(unic_parameter_objs.values()))

        request_body_obj = operation_obj.get("requestBody")
        if request_body_obj is None:
            self.request_body = None
        else:
            self.request_body = RequestBodyEntity(request_body_obj)
        self.responses = ResponsesEntity(operation_obj.get("responses", {}))

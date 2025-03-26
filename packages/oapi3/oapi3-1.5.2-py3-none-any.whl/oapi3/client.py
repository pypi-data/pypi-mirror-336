"""Module contains openapi3 client."""
# ruff: noqa: S310
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Optional
from typing import Tuple
import json
import logging

import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode

from .exceptions import BodyValidationError
from .exceptions import ApiRequestError

if TYPE_CHECKING:
    from .schema import Schema
    from .entities import OperationEntity

logger = logging.getLogger(__name__)

DEFAULT_CLIENT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


SendRequestCallback = Callable[
    [
        str,
        str,
        str,
        Optional[dict],
        Optional[str],
        Optional[dict],
        Optional[dict],
    ],
    Tuple[int, str, bytes],
]


def send_request(
    operation_id: str,
    url: str,
    method: str,
    query: dict | None,
    media_type: str | None = None,
    body: dict | None = None,
    headers: dict | None = None,
) -> tuple[int, str, bytes]:
    """Send request func."""
    if headers is None:
        headers = {}
    request_headers = DEFAULT_CLIENT_HEADERS.copy()
    request_headers.update(**headers)
    if query:
        url = f"{url}?{urlencode(query)}"
    _body = json.dumps(body).encode("utf-8") if body else None

    if not url.startswith(("http:", "https:")):
        msg = "URL must start with 'http:' or 'https:'"
        raise ValueError(msg)

    request = urllib.request.Request(
        url,
        data=_body,
        headers=request_headers,
        method=method.upper(),
    )
    if media_type:
        request.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(request) as resp:
            return resp.code, resp.headers.get_content_type(), resp.read()
    except HTTPError as exc:
        logger.exception("HTTPError for url: %s", url)
        logger.exception(exc)  # noqa: TRY401
        http_code = getattr(exc, "code", 422)
        raise ApiRequestError(url, exc.reason, http_code, exc.read()) from exc
    except URLError as exc:
        logger.exception("URLError for url: %s", url)
        logger.exception(exc)  # noqa: TRY401
        http_code = getattr(exc, "code", 503)
        raise ApiRequestError(url, str(exc.reason), http_code) from exc


class Operation:
    """Client operation class."""

    pattern: str
    method: str
    operation_id: str
    enitity: OperationEntity

    def __init__(
        self,
        client: Client,
        pattern: str,
        method: str,
        entity: OperationEntity,
    ):
        self.client = client
        self.pattern = pattern
        self.method = method
        self.operation_id = entity.operation_id
        self.entity = entity

    def __call__(
        self,
        params: dict | None = None,
        media_type: str | None =None,
        body: dict | None = None,
        headers: dict | None = None,
    ):
        """Call operation."""
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        parameters_entity = self.entity.parameters
        path_params = {
            k: v for k, v in params.items()
            if k in parameters_entity.parameters["path"]
        }
        query_params = {
            k: v for k, v in params.items()
            if k in parameters_entity.parameters["query"]
        }
        unknown = set(params) - set(path_params) - set(query_params)
        if unknown:
            msg = f"Unknown params: {unknown}"
            raise ValueError(msg)

        parameters_entity.validate("path", path_params)
        parameters_entity.validate("query", query_params)
        query_params = parameters_entity.serialize("query", query_params)

        path = str(self.pattern)
        for k, v in path_params.items():
            path = path.replace(f"{{{k}}}", str(v))
        url = self.client.url + path

        if media_type is None:
            media_type = "application/json"

        self.client.schema.validate_request(
            path,
            self.method,
            query_params,
            media_type,
            body,
        )
        resp_code, resp_content_type, resp_content = self.client.send_request(
            self.operation_id,
            url,
            self.method,
            query_params,
            media_type,
            body,
            headers,
        )
        if resp_content_type in (
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ):
            raise NotImplementedError
        if resp_content_type == "application/json":
            try:
                resp_body = json.loads(resp_content.decode())
            except (json.decoder.JSONDecodeError, ValueError) as exc:
                logger.exception(str(body)[:5000])
                raise BodyValidationError(str(exc)) from exc
        else:
            resp_body = None
        return self.client.schema.validate_response(
            path,
            self.method,
            resp_code,
            resp_content_type,
            resp_body,
        )


class Client:
    """Openapi client class."""

    schema: Schema
    url: str
    operation_cls: type[Operation] = Operation
    operations: dict[str, Operation]
    send_request: SendRequestCallback

    def __init__(
        self,
        url: str,
        schema: Schema,
        send_request: SendRequestCallback = send_request,
    ):
        self.schema = schema
        self.url = url.rstrip("/")
        self.send_request = send_request
        operations = schema.operations.items()
        self.operations = {
            operation_id: self._create_operation(pattern, method, entity)
            for operation_id, (pattern, method, entity) in operations
        }

    def _create_operation(
        self,
        pattern: str,
        method: str,
        entity: OperationEntity,
    ) -> Operation:
        return self.operation_cls(self, pattern, method, entity)

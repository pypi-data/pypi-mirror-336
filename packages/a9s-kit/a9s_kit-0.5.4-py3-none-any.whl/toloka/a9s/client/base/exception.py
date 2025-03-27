import json
from functools import wraps
from io import StringIO
from json import JSONDecodeError
from typing import Any, Awaitable, Callable, TypeVar, cast

from httpx import HTTPStatusError
from pydantic import ConfigDict, TypeAdapter, ValidationError
from pydantic.dataclasses import dataclass

F = TypeVar('F', bound=Callable[..., Awaitable[Any]])


@dataclass(config=ConfigDict(extra='allow'))
class AnnotationStudioError(Exception):
    type: str
    title: str
    status: int
    detail: str
    instance: str
    request_id: str
    timestamp: str

    def __str__(self) -> str:
        # TypeAdapter does not preserve extra fields
        # https://github.com/pydantic/pydantic/issues/9645
        return json.dumps(self.__dict__, indent=2)

    def with_request(
        self,
        url: str,
        method: str,
        body: str | None,
    ) -> 'AnnotationStudioErrorWithRequest':
        if body:
            try:
                body = json.dumps(json.loads(body), indent=2)
            except JSONDecodeError:
                body = '<Failed to parse JSON body>'

        return AnnotationStudioErrorWithRequest(
            type=self.type,
            title=self.title,
            status=self.status,
            detail=self.detail,
            instance=self.instance,
            request_id=self.request_id,
            timestamp=self.timestamp,
            url=url,
            method=method,
            request_body=body,
        )


@dataclass(config=ConfigDict(extra='allow'))
class AnnotationStudioErrorWithRequest(AnnotationStudioError):
    url: str
    method: str
    request_body: str | None

    def __str__(self) -> str:
        msg = StringIO()
        msg.write('Request:\n')
        msg.write(f'{self.method} {self.url}\n')
        if isinstance(self.request_body, str):
            msg.write(self.request_body + '\n')
        msg.write('Response:\n')
        msg.write(super().__str__())
        return msg.getvalue()


A9S_ERROR_TYPE_ADAPTER = TypeAdapter(AnnotationStudioError)


class UnexpectedAnnotationStudioError(Exception):
    pass


def wrap_async_http_status_exception(f: F) -> F:
    @wraps(f)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await f(*args, **kwargs)
        except HTTPStatusError as e:
            try:
                response_exception = A9S_ERROR_TYPE_ADAPTER.validate_json(e.response.text)
                raise response_exception.with_request(
                    url=str(e.request.url),
                    method=str(e.request.method),
                    body=e.request.content.decode(),
                )
            except ValidationError:
                try:
                    response_text = json.dumps(e.response.json(), indent=2)
                except JSONDecodeError:
                    response_text = e.response.text
                raise UnexpectedAnnotationStudioError(response_text)

    return cast(F, wrapper)

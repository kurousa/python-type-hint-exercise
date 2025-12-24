"""
http_client.py

責務: HTTPクライアントの抽象化と実装を提供する
"""

from __future__ import annotations

from typing import Protocol

import requests as requests_lib

from .models import FetchErrorType, Headers
from .decorators import measure_time

type JsonObject = dict[str, object]


class HttpResponse(Protocol):
    @property
    def status_code(self) -> int: ...
    def json(self) -> object: ...


class HttpClient(Protocol):
    def post(self, url: str, json: JsonObject, headers: Headers | None = None) -> HttpResponse: ...


# Requestsのラッパークラス
class RequestsHttpResponse:
    """requestsからのHttpResponse"""

    def __init__(self, response: requests_lib.Response):
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    def json(self) -> object:
        return self._response.json()


class RequestsHttpClient:
    """requestsを用いたHttpクライアント"""

    def __init__(self) -> None:
        self._session = requests_lib.Session()

    @measure_time
    def post(self, url: str, json: JsonObject, headers: Headers | None = None) -> HttpResponse:
        response = self._session.post(url, json=json, headers=headers)
        return RequestsHttpResponse(response)


def to_error_type(status_code: int) -> FetchErrorType:
    match status_code:
        case 404:
            return FetchErrorType.NOT_FOUND_ERROR
        case num if 400 <= num < 500:
            return FetchErrorType.CLIENT_ERROR
        case _:
            return FetchErrorType.SERVER_ERROR

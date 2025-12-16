"""
http_client.py

責務: HTTPクライアントの抽象化と実装を提供する
"""

from typing import Protocol

import requests as requests_lib

from models import Headers

type JsonObject = dict[str, object]


class HttpResponse(Protocol):
    @property
    def status_code(self) -> int: ...
    def json(self) -> object: ...


class HttpClient(Protocol):
    def post(
        self, url: str, json: JsonObject, headers: Headers | None = None
    ) -> HttpResponse: ...


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

    def post(
        self, url: str, json: JsonObject, headers: Headers | None = None
    ) -> HttpResponse:
        response = requests_lib.post(url, json=json, headers=headers)
        return RequestsHttpResponse(response)

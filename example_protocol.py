from typing import Protocol
import requests

from example_abc import JsonObject


class HttpResponse(Protocol):
    @property
    def status_code(self) -> int: ...
    def json(self) -> object: ...


class HttpClient(Protocol):
    def post(self, url: str, json: JsonObject) -> HttpResponse: ...


def fetch_address(client: HttpClient) -> None:
    response = client.post("https://example.com", {})
    print(response.status_code)


# requests.SessionはHttpClientを継承していないが、postメソッドを持つため問題ない
session = requests.session()
fetch_address(session)


# 利用側が必要とする定義だけに絞ったインターフェース定義が可能
class PostOnlyClient(Protocol):
    def post(self, url: str, json: JsonObject) -> HttpResponse: ...


def fetch_address(client: PostOnlyClient) -> None:
    # post()だけ利用したい
    ...


class GetOnlyClient(Protocol):
    def get(self, url: str) -> HttpResponse: ...


def fetch_health(client: GetOnlyClient) -> None:
    # get()だけ利用したい
    ...


session = requests.session()
fetch_address(session)
fetch_health(session)

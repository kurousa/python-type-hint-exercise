from http_client import HttpResponse, JsonObject
from main import (
    fetch_and_format_address,
)
from models import Headers, ZipCode


class MockResponse:
    def __init__(self, status_code: int, data: object):
        self._status_code = status_code
        self._data = data

    @property
    def status_code(self) -> int:
        return self._status_code

    def json(self) -> object:
        return self._data


class MockHttpClient:
    def __init__(self, response: MockResponse):
        self._response = response

    def post(self, url: str, json: JsonObject, headers: Headers | None = None) -> HttpResponse:
        return self._response


def test_fetch_address_success() -> None:
    # 👉 好きなレスポンスを返すモックを用意
    mock_response = MockResponse(
        200,
        {
            "zipcode": "1000001",
            "prefecture": "東京都",
            "prefecture_kana": "トウキョウト",
            "city": "千代田区",
            "city_kana": "チヨダク",
            "town": "千代田",
            "town_kana": "チヨダ",
        },
    )
    mock_client = MockHttpClient(mock_response)

    # 👉 ネットワーク通信なしでテストできる！
    result = fetch_and_format_address(ZipCode("1000001"), include_kana=True, http_client=mock_client)
    assert isinstance(result, dict)
    assert result["full_address"] == "東京都千代田区千代田"
    assert result["full_address_kana"] == "トウキョウトチヨダクチヨダ"

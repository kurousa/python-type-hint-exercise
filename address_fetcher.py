from abc import ABC, abstractmethod
import requests as requests_lib
import json

from typing import NewType, NotRequired, TypedDict, cast

class AddressInfo(TypedDict):
    prefecture: str
    city: str
    town: str
    prefecture_kana: str
    city_kana: str
    town_kana: str

class FormattedAddress(TypedDict):
    zipcode: str
    full_address: str
    prefecture: str
    city: str
    town: str
    # include_kanaがFalseの場合は、full_address_kanaは不要なためNotRequiredとする
    full_address_kana: NotRequired[str]

# 実態はstrだが、型チェッカーに対してZipCodeという別の型であることを明示する
ZipCode = NewType("ZipCode", str)
# 型エイリアス
type Headers = dict[str, str]
type JsonObject = dict[str, object]

class HttpResponse(ABC):
    @property
    @abstractmethod
    def status_code(self) -> int: ...

    @abstractmethod
    def json(self) -> object: ...

class HttpClient(ABC):
    @abstractmethod
    def post(self, url: str, json: JsonObject, headers: Headers | None = None) -> HttpResponse: ...

# ABCを継承した、Requestsのラッパークラス
class RequestsHttpResponse(HttpResponse):
    """requestsからのHttpResponse"""
    def __init__(self, response: requests_lib.Response):
        self._response = response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    def json(self) -> object:
        return self._response.json()

class RequestsHttpClient(HttpClient):
    """requestsを用いたHttpクライアント"""
    def post(self, url: str, json: JsonObject, headers: Headers | None = None) -> HttpResponse:
        response = requests_lib.post(url, json=json, headers=headers)
        return RequestsHttpResponse(response)

def _build_full_address(address_data: AddressInfo) -> str:
    """
    住所データからフル住所文字列を生成する。
    """
    return address_data["prefecture"] + address_data["city"] + address_data["town"]

def fetch_and_format_address(
    zipcode: ZipCode,
    include_kana: bool,
    http_client: HttpClient,
    headers: Headers | None = None,
) -> str | None:
    """郵便番号から住所を取得し、整形して返す"""

    # APIエンドポイントのURLを定義（架空の API）
    api_url = "https://api.zipcode-jp.example/v1/address"

    try:
        # 郵便番号検索APIにリクエスト
        response: HttpResponse = http_client.post(api_url, json={"zipcode": zipcode})
        if response.status_code != 200:
            print(f"Error: Failed to fetch address. Status: {response.status_code}")
            return None

        # APIの戻り値に、定義した型ヒントを適用
        # HttpResponseとしてはobjectを返すため、AddressInfoへとキャストを実施
        address_data: AddressInfo = cast(AddressInfo, response.json())

        # フル住所を生成
        full_address = _build_full_address(address_data)

        # 結果を組み立て
        result: FormattedAddress = {
            "zipcode": zipcode,
            "full_address": full_address,
            "prefecture": address_data["prefecture"],
            "city": address_data["city"],
            "town": address_data["town"],
        }

        # カナを含める場合は、取得結果に対して各カナ情報を連結し、 full_address_kana にする
        if include_kana:
            result["full_address_kana"] = (
                address_data["prefecture_kana"]
                + address_data["city_kana"]
                + address_data["town_kana"]
            )

        # 結果を JSON 形式で返す
        return json.dumps(result, indent=2, ensure_ascii=False)

    except requests_lib.exceptions.RequestException as e:
        # APIリクエスト時の例外を処理
        print(f"An error occurred during API request: {e}")
        return None
    except (KeyError, IndexError) as e:
        # 外部APIからのレスポンスが予期しない形式の場合のエラーは事前チェック不可である前提であるためRuntime Errorとする
        raise RuntimeError(f"予期しないレスポンス: {e}") from e

# 実行例
# ここでは便宜上、本スクリプト内で上記関数を呼び出していますが、
# 本来は別のファイルに呼び出し処理があることを想定してください。
if __name__ == "__main__":
    zipcode: ZipCode = ZipCode("1000001")
    http_client = RequestsHttpClient()
    result = fetch_and_format_address(zipcode, http_client=http_client, include_kana=True)
    if result is not None:
        print(result)

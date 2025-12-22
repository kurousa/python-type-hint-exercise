"""
main.py

責務: アプリケーションの主要ビジネスロジックを組み合わせ、実行を行う
"""

import json
from typing import Annotated, Any, Final, Mapping, assert_never, cast

import requests
import typer


from http_client import HttpClient, HttpResponse, RequestsHttpClient, to_error_type
from models import (
    AddressFormatter,
    AddressInfo,
    ApiError,
    ApiResponse,
    FetchError,
    FetchErrorType,
    FormattedAddress,
    Headers,
    ZipCode,
    is_error_response,
)

BASE_URL: Final[str] = "https://api.zipcode-jp.example"
HTTP_OK: Final[int] = 200


def parse_response(payload: Mapping[str, Any]) -> ApiResponse:
    if "error_code" in payload:
        return ApiError.unmarshall_payload(payload)
    return AddressInfo.unmarshall_payload(payload)


def handle_fetch_error(error: FetchError) -> None:
    """エラーの種類に応じてメッセージを表示する"""
    match error.type:
        case FetchErrorType.NETWORK_ERROR:
            print(f"ネットワークエラー: {error.message}")
        case FetchErrorType.NOT_FOUND_ERROR:
            print(f"郵便番号が見つかりません: {error.message}")
        case FetchErrorType.CLIENT_ERROR:
            print(f"リクエストエラー: {error.message}")
        case FetchErrorType.SERVER_ERROR:
            print(f"サーバーエラー: {error.message}")
        case FetchErrorType.API_ERROR:
            print(f"APIエラー: {error.message}")
        case _:
            assert_never(error.type)


def fetch_and_format_address(
    zipcode: ZipCode,
    include_kana: bool,
    http_client: HttpClient,
    headers: Headers | None = None,
) -> FormattedAddress | FetchError:
    """郵便番号から住所を取得し、整形して返す"""

    # APIエンドポイントのURLを定義（架空の API）
    api_url = f"{BASE_URL}{AddressInfo.API_PATH}"

    try:
        # 郵便番号検索APIにリクエスト
        response: HttpResponse = http_client.post(api_url, json={"zipcode": zipcode}, headers=headers)
        if response.status_code != HTTP_OK:
            error_type = to_error_type(response.status_code)
            return FetchError(error_type, f"HTTP {response.status_code}")

        payload: dict[str, Any] = cast(dict[str, Any], response.json())
        api_response = parse_response(payload)

        if is_error_response(api_response):
            return FetchError(FetchErrorType.API_ERROR, api_response.message)

        address_info = api_response
        # フル住所を生成
        return AddressFormatter.from_address(address_info).with_kana(include_kana).build()

    except requests.exceptions.RequestException as e:
        return FetchError(type=FetchErrorType.NETWORK_ERROR, message=str(e))
    except (KeyError, IndexError, TypeError, requests.exceptions.JSONDecodeError) as e:
        return FetchError(type=FetchErrorType.SERVER_ERROR, message=f"予期しないレスポンス形式です: {e}")


def main(
    param: Annotated[str, typer.Argument(help="検索対象の郵便番号")],
    include_kana: Annotated[bool, typer.Option(help="カナ表記を含める")] = True,
) -> None:
    """APIで郵便番号を検索して、情報を出力します

    --include_kana をつけることで、カナ表記で出力します
    """
    http_client = RequestsHttpClient()
    zipcode: ZipCode = ZipCode(param)
    result = fetch_and_format_address(zipcode, http_client=http_client, include_kana=include_kana)
    if isinstance(result, FetchError):
        handle_fetch_error(result)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    typer.run(main)

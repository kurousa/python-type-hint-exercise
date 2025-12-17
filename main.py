"""
main.py

責務: アプリケーションの主要ビジネスロジックを組み合わせ、実行を行う
"""

import json
from typing import Any, cast

import requests as requests_lib

from http_client import HttpClient, HttpResponse, RequestsHttpClient
from models import AddressInfo, FormattedAddress, Headers, ZipCode


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
        response_dict: dict[str, Any] = cast(dict[str, Any], response.json())
        address_info: AddressInfo = AddressInfo(**response_dict)
        # フル住所を生成
        full_address = address_info.full_address()

        # 結果を組み立て
        result: FormattedAddress = {
            "zipcode": zipcode,
            "full_address": full_address,
            "prefecture": address_info.prefecture,
            "city": address_info.city,
            "town": address_info.town,
        }

        # カナを含める場合は、取得結果に対して各カナ情報を連結し、 full_address_kana にする
        if include_kana:
            result = {**result, "full_address_kana": address_info.full_address_kana()}

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
    result = fetch_and_format_address(
        zipcode, http_client=http_client, include_kana=True
    )
    if result is not None:
        print(result)

import requests
import json

from typing import TypedDict

class AddressInfo(TypedDict):
    prefecture: str
    city: str
    town: str
    prefecture_kana: str
    city_kana: str
    town_kana: str

def _build_full_address(address_data: AddressInfo) -> str:
    """
    住所データからフル住所文字列を生成する。
    """
    return address_data["prefecture"] + address_data["city"] + address_data["town"]

def fetch_and_format_address(zipcode: str, include_kana: bool) -> str | None:
    """郵便番号から住所を取得し、整形して返す"""

    # APIエンドポイントのURLを定義（架空の API）
    api_url = "https://api.zipcode-jp.example/v1/address"

    try:
        # 郵便番号検索APIにリクエスト
        response = requests.post(api_url, json={"zipcode": zipcode})
        if response.status_code != 200:
            print(f"Error: Failed to fetch address. Status: {response.status_code}")
            return None

        # APIの戻り値に、定義した型ヒントを適用
        address_data: AddressInfo = response.json()  # 結果を JSON 形式にする

        # フル住所を生成
        full_address = _build_full_address(address_data)

        # 結果を組み立て
        result = {
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

    except requests.exceptions.RequestException as e:
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
    result = fetch_and_format_address("1000001", include_kana=True)
    if result is not None:
        print(result)
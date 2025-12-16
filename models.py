"""
models.py

責務: アプリケーションで共通して使うデータ構造を定義する
ドメイン固有の ZipCode や API レスポンスの構造に加えて、複数のモジュールで使う Headers もここに配置
"""

from typing import NewType, NotRequired, TypedDict

ZipCode = NewType("ZipCode", str)
type Headers = dict[str, str]


class AddressInfo(TypedDict):
    prefecture: str
    city: str
    town: str
    prefecture_kana: str
    city_kana: str
    town_kana: str

    # FIXME: データとロジックが分離してしまっている
    # main.pyの_build_full_addressメソッドをクラスのメソッドとして定義すべき


class FormattedAddress(TypedDict):
    zipcode: str
    full_address: str
    prefecture: str
    city: str
    town: str
    # include_kanaがFalseの場合は、full_address_kanaは不要なためNotRequiredとする
    full_address_kana: NotRequired[str]

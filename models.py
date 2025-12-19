"""
models.py

責務: アプリケーションで共通して使うデータ構造を定義する
ドメイン固有の ZipCode や API レスポンスの構造に加えて、複数のモジュールで使う Headers もここに配置
"""

from dataclasses import dataclass
from typing import Any, ClassVar, Mapping, NewType, NotRequired, TypedDict

ZipCode = NewType("ZipCode", str)
type Headers = dict[str, str]


@dataclass(frozen=True, slots=True)
class AddressInfo:
    API_PATH: ClassVar[str] = "/v1/address"
    zipcode: str
    prefecture: str
    prefecture_kana: str
    city: str
    city_kana: str
    town: str
    town_kana: str

    @classmethod
    def unmarsahl_payload(cls, payload: Mapping[str, Any]) -> "AddressInfo":
        """APIレスポンスからAddressInfoオブジェクトを生成する"""
        return cls(
            zipcode=str(payload.get("zipcode")),
            prefecture=str(payload.get("prefecture")),
            prefecture_kana=str(payload.get("prefecture_kana")),
            city=str(payload.get("city")),
            city_kana=str(payload.get("city_kana")),
            town=str(payload.get("town")),
            town_kana=str(payload.get("town_kana")),
        )

    def full_address(self) -> str:
        """郵便番号、都道府県、市区町村、町名を結合した住所を返す"""
        return self.prefecture + self.city + self.town

    def full_address_kana(self) -> str:
        """郵便番号、都道府県、市区町村、町名を結合した住所(カナ表記)を返す"""
        return self.prefecture_kana + self.city_kana + self.town_kana


class FormattedAddress(TypedDict):
    zipcode: str
    full_address: str
    prefecture: str
    city: str
    town: str
    # include_kanaがFalseの場合は、full_address_kanaは不要なためNotRequiredとする
    full_address_kana: NotRequired[str]

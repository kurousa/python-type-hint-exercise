"""
models.py

責務: アプリケーションで共通して使うデータ構造を定義する
ドメイン固有の ZipCode や API レスポンスの構造に加えて、複数のモジュールで使う Headers もここに配置
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, auto
from typing import Any, ClassVar, Mapping, NewType, NotRequired, TypedDict, Self
from typing_extensions import ReadOnly, TypeIs

ZipCode = NewType("ZipCode", str)
type Headers = dict[str, str]


@dataclass(frozen=True, slots=True)
class AddressInfo:
    zipcode: str
    prefecture: str
    prefecture_kana: str
    city: str
    city_kana: str
    town: str
    town_kana: str

    API_PATH: ClassVar[str] = "/v1/address"

    @classmethod
    def unmarshall_payload(cls, payload: Mapping[str, Any]) -> AddressInfo:
        """APIレスポンスからAddressInfoオブジェクトを生成する"""
        return cls(
            zipcode=str(payload["zipcode"]),
            prefecture=str(payload["prefecture"]),
            prefecture_kana=str(payload["prefecture_kana"]),
            city=str(payload["city"]),
            city_kana=str(payload["city_kana"]),
            town=str(payload["town"]),
            town_kana=str(payload["town_kana"]),
        )

    def full_address(self) -> str:
        """郵便番号、都道府県、市区町村、町名を結合した住所を返す"""
        return self.prefecture + self.city + self.town

    def full_address_kana(self) -> str:
        """郵便番号、都道府県、市区町村、町名を結合した住所(カナ表記)を返す"""
        return self.prefecture_kana + self.city_kana + self.town_kana


class FormattedAddress(TypedDict):
    zipcode: ReadOnly[str]
    full_address: ReadOnly[str]
    prefecture: ReadOnly[str]
    city: ReadOnly[str]
    town: ReadOnly[str]
    # include_kanaがFalseの場合は、full_address_kanaは不要なためNotRequiredとする
    full_address_kana: NotRequired[str]


@dataclass(frozen=True, slots=True)
class AddressFormatter:
    """データ整形ロジック"""

    _address: AddressInfo
    _include_kana: bool = False

    @classmethod
    def from_address(cls, address: AddressInfo) -> Self:
        """AddressInfoからAddressFormatterインスタンスを生成"""
        return cls(_address=address)

    def with_kana(self, include_kana: bool) -> Self:
        """カナ表記を含めるかどうかを設定する"""
        return replace(self, _include_kana=include_kana)

    def build(self) -> FormattedAddress:
        """整形ロジックの組み立て"""
        formatted_address: FormattedAddress = {
            "zipcode": self._address.zipcode,
            "full_address": self._address.full_address(),
            "prefecture": self._address.prefecture,
            "city": self._address.city,
            "town": self._address.town,
        }

        if self._include_kana:
            formatted_address["full_address_kana"] = self._address.full_address_kana()

        return formatted_address


@dataclass(frozen=True, slots=True)
class ApiError:
    error_code: int
    message: str

    @classmethod
    def unmarshall_payload(cls, payload: Mapping[str, Any]) -> ApiError:
        return cls(
            error_code=int(payload["error_code"]),
            message=str(payload["message"]),
        )


type ApiResponse = AddressInfo | ApiError


def is_error_response(response: ApiResponse) -> TypeIs[ApiError]:
    """responseがApiErrorかどうかを判定"""
    return isinstance(response, ApiError)


class FetchErrorType(Enum):
    """リクエストエラータイプ列挙型"""

    NETWORK_ERROR = auto()
    NOT_FOUND_ERROR = auto()
    CLIENT_ERROR = auto()
    SERVER_ERROR = auto()
    API_ERROR = auto()


@dataclass(frozen=True, slots=True)
class FetchError:
    type: FetchErrorType
    message: str

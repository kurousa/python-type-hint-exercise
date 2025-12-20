from typing import TypedDict


class AddressInfo(TypedDict):
    prefecture: str
    city: str
    town: str


# TypedDictの使用例
def print_address_info(address_info: AddressInfo) -> None:
    print(f" prefectura: {address_info['prefecture']}")
    print(f" city: {address_info['city']}")
    print(f" town: {address_info['town']}")


address_info: AddressInfo = {
    "prefecture": "東京都",
    "city": "千代田区",
    "town": "永田町1-7-1",
}
print_address_info(address_info)

print(address_info["unknown_key"])  # mypeでエラーを検出する

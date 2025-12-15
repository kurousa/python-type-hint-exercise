from typing import NewType

# ZipCodeという新しい型を定義。実行時にはただのstrだが、
# 型チェック時にはstrとは区別される。
ZipCode = NewType("ZipCode", str)


def get_address(zipcode: ZipCode) -> str:
    # ...
    return "東京都千代田区千代田"


# 正しい使い方
zipcode: ZipCode = ZipCode("1000001")
get_address(zipcode)

# 間違った使い方
zipcode_str: str = "1000001"
get_address(zipcode_str)  # これは型エラー！
# --> 'ZipCode' 型を期待する引数に 'str' 型を渡すことはできない

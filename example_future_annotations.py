# from models import AddressInfo


# def create_address() -> AddressInfo:
#     return AddressInfo()

# print(create_address.__annotations__)
# {'return': <class '__main__.Address'>}  # クラスオブジェクトとして評価される

# from __future__ import annotations

# def create_address() -> AddressInfo:
#     return AddressInfo()

# print(create_address.__annotations__)
# {'return': 'Address'}  # 文字列のまま保持される

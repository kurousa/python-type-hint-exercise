from collections.abc import Iterable, Sequence

from models import AddressInfo


def format_addresses(addresses: Sequence[AddressInfo]) -> list[str]:
    """複数の Address をフォーマットして返す"""
    return [addr.full_address() for addr in addresses]


def count_by_prefecture(addresses: Iterable[AddressInfo]) -> dict[str, int]:
    """都道府県ごとの住所数をカウントする"""
    counts: dict[str, int] = {}
    for addr in addresses:
        counts[addr.prefecture] = counts.get(addr.prefecture, 0) + 1
    return counts

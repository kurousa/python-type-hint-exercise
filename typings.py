from __future__ import annotations

from collections.abc import Mapping, Sequence


def first[T](items: Sequence[T]) -> T | None:
    """シーケンス最初の要素を返却。空の場合はNoneを返す.

    Examples:
        >>> items = [0, 1, 2, 3]
        >>> first(items)
        0

        >>> items = []
        >>> first(items) is None
        True
    """
    return items[0] if items else None


def get_or[K, V](d: Mapping[K, V], key: K, default: V) -> V:
    """マッピングから値を取得する。キーがなければデフォルト値を返す

    Examples:
        >>> d = {"timeout": 30, "retries": 3}
        >>> get_or(d, "timeout", 10)
        30
        >>> get_or(d, "retries", 1)
        3
        >>> get_or(d, "unknown", "this is unknown key")
        "this is unknown key"
    """
    return d.get(key, default)

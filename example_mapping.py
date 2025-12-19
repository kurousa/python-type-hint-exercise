from collections.abc import Mapping
from typing import (
    Any,
    Collection,
    Dict,
    Iterable,
    List,
    MutableMapping,
    MutableSequence,
    Sequence,
)


def illegal_mapping_func(payload: Mapping[str, Any]) -> None:
    _ = payload["zipcode"]  # 読み取りは OK
    # payload["zipcode"] = "0000000"  # ← mypy がエラーにしてくれる


def mutable_mapping_func(payload: MutableMapping[str, Any]) -> None:
    _ = payload["zipcode"]  # 読み取りOK
    payload["zipcode"] = "0000000"  # 書き込みOK


def sequence_func(payload: Sequence[List[Any]]) -> None:
    for item in payload:
        print(item)
    # payload[0] = "0"  # mypy がエラーにしてくれる


def mutable_sequence_func(payload: MutableSequence[str]) -> None:
    for item in payload:
        print(item)
    payload[0] = "0"  # OK


def iterable_func(payload: Iterable[Any]) -> None:
    for item in payload:
        print(item)


def collection_func(payload: Collection[List[Any] | Dict[str, Any]]) -> None:
    for item in payload:
        print(item)

    len(payload)

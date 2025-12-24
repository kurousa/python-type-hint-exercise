from __future__ import annotations

from dataclasses import dataclass
from typing import final
from typing_extensions import TypeIs


@final
@dataclass(frozen=True, slots=True)
class Ok[T]:
    """成功を表すコンテナ

    T: 成功時の値の型
    """

    value: T


@final
@dataclass(frozen=True, slots=True)
class Err[E]:
    """失敗を表すコンテナ

    E: エラー時の型
    """

    error: E


# Ok, ErrをUnionとして束ねたResult型エイリアス
type Result[T, E] = Ok[T] | Err[E]


def is_ok[T, E](result: Result[T, E]) -> TypeIs[Ok[T]]:
    """成功かどうかを判定し、型を絞り込む"""
    return isinstance(result, Ok)


def is_err[T, E](result: Result[T, E]) -> TypeIs[Err[E]]:
    """失敗かどうかを判定し、型を絞り込む"""
    return isinstance(result, Err)

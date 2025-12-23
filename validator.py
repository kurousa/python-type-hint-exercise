# validator.py
from __future__ import annotations

import inspect
from dataclasses import dataclass
from functools import wraps
from typing import Annotated, Callable, get_args, get_origin, get_type_hints

from result import Err, Ok, Result, is_err


@dataclass(frozen=True, slots=True)
class EmptyStringError:
    """空文字列エラー"""

    message: str = "空文字列は許可されていません"


@dataclass(frozen=True, slots=True)
class ValidationError:
    """バリデーション失敗時のエラー"""

    field: str
    message: str


def non_empty(value: str) -> Result[str, EmptyStringError]:
    """空文字列を許可しない"""
    if not value or value.isspace():
        return Err(EmptyStringError())
    return Ok(value)


def validate_args[**P, R](
    func: Callable[P, Result[R, ValidationError]],
) -> Callable[P, Result[R, ValidationError]]:
    """Annotated のメタデータに callable があれば適用し、Result で返す"""
    hints = get_type_hints(func, include_extras=True)
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, ValidationError]:
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            hint = hints.get(name)
            if hint is not None and get_origin(hint) is Annotated:
                type_args = get_args(hint)
                for meta in type_args[1:]:
                    # Annotatedで第2引数以降に埋め込まれた関数うがあればその処理を適用する
                    if callable(meta):
                        result = meta(value)
                        if is_err(result):
                            return Err(ValidationError(field=name, message=result.error.message))
                        value = result.value
            bound.arguments[name] = value

        return func(*bound.args, **bound.kwargs)

    return wrapper

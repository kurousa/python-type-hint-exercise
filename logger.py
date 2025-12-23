# logger.py
from __future__ import annotations

import logging
from typing import Annotated, Literal

from result import Result, Ok
from validator import ValidationError, non_empty, validate_args

# Literal でログレベルを型安全に
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Annotated でバリデーション関数を付与
LoggerName = Annotated[str, non_empty]


@validate_args
def setup_logger(
    name: LoggerName,
    level: LogLevel = "INFO",
) -> Result[logging.Logger, ValidationError]:
    """指定された名前とレベルでロガーを設定する"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return Ok(logger)

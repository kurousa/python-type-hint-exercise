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
) -> Result[logging.Logger, ValidationError]:
    """指定された名前でロガーを取得する"""
    logger = logging.getLogger(name)
    return Ok(logger)

# address_search/__init__.py
"""郵便番号から住所を検索するライブラリ"""

from .models import (
    ZipCode,
    Headers,
    AddressInfo,
    FormattedAddress,
    AddressFormatter,
    FetchError,
    FetchErrorType,
)
from .http_client import (
    HttpClient,
    RequestsHttpClient,
    to_error_type,
)
from .result import Result, Ok, Err, is_ok, is_err
from .validator import ValidationError, validate_args
from .logger import setup_logger, LogLevel, LoggerName

__all__ = [
    # 型
    "ZipCode",
    "Headers",
    "AddressInfo",
    "FormattedAddress",
    "AddressFormatter",
    # HTTP
    "HttpClient",
    "RequestsHttpClient",
    "FetchError",
    "FetchErrorType",
    "to_error_type",
    # Result
    "Result",
    "Ok",
    "Err",
    "is_ok",
    "is_err",
    # Validator
    "ValidationError",
    "validate_args",
    # Logger
    "setup_logger",
    "LogLevel",
    "LoggerName",
]

"""Stacked DataTable - 엑셀 데이터의 컴마 구분 컬럼을 Stack/Explode하는 도구."""

from .core import (
    detect_comma_columns,
    parse_clipboard_data,
    stack_dataframe,
    unstack_dataframe,
)

__all__ = [
    "detect_comma_columns",
    "parse_clipboard_data",
    "stack_dataframe",
    "unstack_dataframe",
]
__version__ = "0.1.0"

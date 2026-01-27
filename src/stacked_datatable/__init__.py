"""Stacked DataTable - 엑셀 데이터의 컴마 구분 컬럼을 Stack/Explode하는 도구."""

from .core import stack_dataframe, parse_clipboard_data, detect_comma_columns

__all__ = ["stack_dataframe", "parse_clipboard_data", "detect_comma_columns"]
__version__ = "0.1.0"

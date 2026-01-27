"""핵심 Stack/Explode 기능을 제공하는 모듈."""

from __future__ import annotations

import re


def parse_clipboard_data(text: str) -> tuple[list[str], list[list[str]]]:
    """클립보드에서 복사한 탭 구분 텍스트를 파싱합니다.

    Args:
        text: 엑셀에서 복사한 탭 구분 텍스트.

    Returns:
        (헤더 리스트, 데이터 행 리스트) 튜플.

    Raises:
        ValueError: 데이터가 비어있거나 유효하지 않은 경우.
    """
    lines = text.strip().split("\n")
    if not lines:
        raise ValueError("입력 데이터가 비어있습니다.")

    headers = lines[0].split("\t")

    rows: list[list[str]] = []
    for line in lines[1:]:
        if line.strip():
            row = line.split("\t")
            while len(row) < len(headers):
                row.append("")
            rows.append(row)

    return headers, rows


def detect_comma_columns(
    headers: list[str],
    rows: list[list[str]],
) -> list[int]:
    """컴마로 구분된 숫자가 포함된 컬럼의 인덱스를 감지합니다.

    Args:
        headers: 헤더 리스트.
        rows: 데이터 행 리스트.

    Returns:
        컴마 구분 숫자가 포함된 컬럼의 인덱스 리스트.
    """
    comma_columns: list[int] = []
    pattern = re.compile(r"^\s*\d+\s*(,\s*\d+\s*)+$")

    for col_idx in range(len(headers)):
        has_comma_values = False
        for row in rows:
            if col_idx < len(row):
                value = row[col_idx].strip()
                if pattern.match(value):
                    has_comma_values = True
                    break
        if has_comma_values:
            comma_columns.append(col_idx)

    return comma_columns


def _split_comma_values(value: str) -> list[str]:
    if "," in value:
        return [v.strip() for v in value.split(",") if v.strip()]
    return [value.strip()] if value.strip() else [""]


def stack_dataframe(
    headers: list[str],
    rows: list[list[str]],
    target_columns: list[int] | None = None,
) -> tuple[list[str], list[list[str]]]:
    """컴마로 구분된 컬럼을 기준으로 행을 확장(Stack/Explode)합니다.

    Args:
        headers: 헤더 리스트.
        rows: 데이터 행 리스트.
        target_columns: Stack할 컬럼 인덱스 리스트. None이면 자동 감지.

    Returns:
        (헤더 리스트, 확장된 데이터 행 리스트) 튜플.
    """
    if target_columns is None:
        target_columns = detect_comma_columns(headers, rows)

    if not target_columns:
        return headers, rows

    stacked_rows: list[list[str]] = []

    for row in rows:
        split_values: dict[int, list[str]] = {}
        max_splits = 1

        for col_idx in target_columns:
            if col_idx < len(row):
                values = _split_comma_values(row[col_idx])
                split_values[col_idx] = values
                max_splits = max(max_splits, len(values))

        for i in range(max_splits):
            new_row: list[str] = []
            for col_idx, cell in enumerate(row):
                if col_idx in split_values:
                    values = split_values[col_idx]
                    if i < len(values):
                        new_row.append(values[i])
                    else:
                        new_row.append("")
                else:
                    new_row.append(cell)
            stacked_rows.append(new_row)

    return headers, stacked_rows


def format_as_tsv(headers: list[str], rows: list[list[str]]) -> str:
    """헤더와 행을 탭 구분 텍스트로 포맷합니다.

    Args:
        headers: 헤더 리스트.
        rows: 데이터 행 리스트.

    Returns:
        탭 구분 텍스트 (엑셀에 붙여넣기 가능).
    """
    lines = ["\t".join(headers)]
    for row in rows:
        lines.append("\t".join(row))
    return "\n".join(lines)


def add_zero_padded_column(
    headers: list[str],
    rows: list[list[str]],
    source_column: int,
    new_column_name: str,
) -> tuple[list[str], list[list[str]]]:
    """숫자 컬럼에 대해 2자리 zero-padding된 새 컬럼을 추가합니다.

    Args:
        headers: 헤더 리스트.
        rows: 데이터 행 리스트.
        source_column: 원본 숫자 컬럼의 인덱스.
        new_column_name: 새 컬럼의 이름.

    Returns:
        (새 헤더 리스트, 새 컬럼이 추가된 행 리스트) 튜플.
    """
    new_headers = headers + [new_column_name]
    new_rows: list[list[str]] = []

    for row in rows:
        value = row[source_column] if source_column < len(row) else ""
        try:
            num = int(value)
            padded = f"{num:02d}"
        except ValueError:
            padded = value
        new_rows.append(row + [padded])

    return new_headers, new_rows

"""엑셀 데이터를 붙여넣으면 컴마 구분 컬럼을 Stack하는 CLI 도구."""

import csv
import sys
from datetime import datetime
from pathlib import Path

from src.stacked_datatable.core import (
    add_zero_padded_column,
    parse_clipboard_data,
    stack_dataframe,
)


def main() -> None:
    print("엑셀에서 복사한 데이터를 붙여넣으세요 (입력 완료 후 Ctrl+D 또는 빈 줄 2번):")
    print("-" * 50)

    lines: list[str] = []
    empty_count = 0

    try:
        for line in sys.stdin:
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line.rstrip("\n\r"))
    except EOFError:
        pass

    if not lines:
        print("입력 데이터가 없습니다.")
        sys.exit(1)

    input_text = "\n".join(lines)

    try:
        headers, rows = parse_clipboard_data(input_text)
        print(f"\n원본: {len(rows)}행, {len(headers)}열")

        stacked_headers, stacked_rows = stack_dataframe(headers, rows)

        wafer_col_idx = (
            stacked_headers.index("Wafer") if "Wafer" in stacked_headers else 1
        )
        stacked_headers, stacked_rows = add_zero_padded_column(
            stacked_headers, stacked_rows, wafer_col_idx, "Wafer_Padded"
        )

        print(f"Stack 후: {len(stacked_rows)}행, {len(stacked_headers)}열")

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"stacked_{timestamp}.csv"

        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(stacked_headers)
            writer.writerows(stacked_rows)

        print(f"\n결과 저장됨: {output_file}")

    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

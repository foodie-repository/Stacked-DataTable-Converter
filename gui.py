import csv
import sys
from datetime import datetime
from pathlib import Path

import webview

if getattr(sys, "frozen", False):
    base_path: str = getattr(sys, "_MEIPASS", "")
    sys.path.insert(0, base_path)

from src.stacked_datatable.core import (
    add_zero_padded_column,
    parse_clipboard_data,
    stack_dataframe,
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Stacked DataTable</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 20px;
            background: #f5f5f5;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 24px; }
        .container { flex: 1; display: flex; flex-direction: column; gap: 15px; }
        .section { flex: 1; display: flex; flex-direction: column; }
        label { font-weight: 600; color: #555; margin-bottom: 5px; }
        textarea {
            flex: 1;
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-family: "SF Mono", Consolas, monospace;
            font-size: 13px;
            resize: none;
            background: white;
        }
        textarea:focus { outline: none; border-color: #007AFF; }
        textarea:disabled { background: #fafafa; }
        .buttons { display: flex; gap: 10px; justify-content: center; padding: 10px 0; }
        button {
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .primary { background: #007AFF; color: white; }
        .primary:hover { background: #0056b3; }
        .secondary { background: #e9e9e9; color: #333; }
        .secondary:hover { background: #d5d5d5; }
        .status {
            text-align: center;
            padding: 8px;
            color: #666;
            font-size: 13px;
        }
        .status.success { color: #28a745; }
        .status.error { color: #dc3545; }
    </style>
</head>
<body>
    <h1>Stacked DataTable</h1>
    <div class="container">
        <div class="section">
            <label>엑셀에서 복사한 데이터를 붙여넣으세요:</label>
            <textarea id="input" placeholder="여기에 붙여넣기 (Ctrl+V / Cmd+V)"></textarea>
        </div>
        <div class="buttons">
            <button class="primary" onclick="convert()">변환 (Stack)</button>
            <button class="secondary" onclick="saveCSV()">CSV로 저장</button>
            <button class="secondary" onclick="clearAll()">지우기</button>
        </div>
        <div class="section">
            <label>결과:</label>
            <textarea id="output" disabled placeholder="변환 결과가 여기에 표시됩니다"></textarea>
        </div>
        <div id="status" class="status">준비</div>
    </div>
    <script>
        async function convert() {
            const input = document.getElementById('input').value;
            if (!input.trim()) {
                setStatus('데이터를 입력해주세요.', 'error');
                return;
            }
            try {
                const result = await pywebview.api.convert(input);
                if (result.error) {
                    setStatus(result.error, 'error');
                } else {
                    document.getElementById('output').value = result.data;
                    setStatus(result.message, 'success');
                }
            } catch (e) {
                setStatus('변환 중 오류: ' + e, 'error');
            }
        }
        async function saveCSV() {
            const output = document.getElementById('output').value;
            if (!output.trim()) {
                setStatus('먼저 데이터를 변환해주세요.', 'error');
                return;
            }
            try {
                const result = await pywebview.api.save_csv();
                if (result.error) {
                    setStatus(result.error, 'error');
                } else {
                    setStatus(result.message, 'success');
                }
            } catch (e) {
                setStatus('저장 중 오류: ' + e, 'error');
            }
        }
        function clearAll() {
            document.getElementById('input').value = '';
            document.getElementById('output').value = '';
            setStatus('준비', '');
        }
        function setStatus(msg, type) {
            const el = document.getElementById('status');
            el.textContent = msg;
            el.className = 'status' + (type ? ' ' + type : '');
        }
    </script>
</body>
</html>
"""


class Api:
    def __init__(self) -> None:
        self.stacked_headers: list[str] = []
        self.stacked_rows: list[list[str]] = []
        self.window: webview.Window | None = None

    def convert(self, input_data: str) -> dict:
        try:
            headers, rows = parse_clipboard_data(input_data)
            self.stacked_headers, self.stacked_rows = stack_dataframe(headers, rows)

            wafer_col_idx = (
                self.stacked_headers.index("Wafer")
                if "Wafer" in self.stacked_headers
                else 1
            )
            self.stacked_headers, self.stacked_rows = add_zero_padded_column(
                self.stacked_headers, self.stacked_rows, wafer_col_idx, "Wafer_Padded"
            )

            result_lines = ["\t".join(self.stacked_headers)]
            for row in self.stacked_rows:
                result_lines.append("\t".join(row))

            return {
                "data": "\n".join(result_lines),
                "message": f"변환 완료: {len(rows)}행 → {len(self.stacked_rows)}행",
            }
        except ValueError as e:
            return {"error": str(e)}

    def save_csv(self) -> dict:
        if not self.stacked_rows:
            return {"error": "먼저 데이터를 변환해주세요."}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"stacked_{timestamp}.csv"

        file_path = self.window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename=default_filename,
            file_types=("CSV Files (*.csv)",),
        )

        if not file_path:
            return {"error": "저장이 취소되었습니다."}

        try:
            save_path = file_path if isinstance(file_path, str) else file_path[0]
            if not save_path.endswith(".csv"):
                save_path += ".csv"

            with open(save_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(self.stacked_headers)
                writer.writerows(self.stacked_rows)

            return {"message": f"저장 완료: {save_path}"}
        except Exception as e:
            return {"error": f"저장 오류: {e}"}


def main() -> None:
    api = Api()
    window = webview.create_window(
        "Stacked DataTable",
        html=HTML,
        js_api=api,
        width=800,
        height=700,
        min_size=(600, 500),
    )
    api.window = window
    webview.start()


if __name__ == "__main__":
    main()

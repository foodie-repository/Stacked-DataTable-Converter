# Stacked DataTable

엑셀에서 복사한 데이터의 컴마 구분 컬럼을 Stack(Explode)하는 도구입니다.

## 기능

- 엑셀 데이터 붙여넣기 (탭 구분)
- 컴마로 구분된 숫자 컬럼 자동 감지
- 각 값을 별도 행으로 확장 (Stack/Explode)
- Zero-padding 컬럼 자동 추가 (01, 02, ... 09, 10, 11, ...)
- CSV 파일로 저장

## 예시

**입력:**
```
Lot       Wafer
TAG1111   1,2,3,10,11,12
TAG1112   5,6
```

**출력:**
```
Lot       Wafer   Wafer_Padded
TAG1111   1       01
TAG1111   2       02
TAG1111   3       03
TAG1111   10      10
TAG1111   11      11
TAG1111   12      12
TAG1112   5       05
TAG1112   6       06
```

## 설치 및 실행

### GUI 앱 (권장)

**Mac:**
- `dist/StackedDataTable.app` 실행

**Windows:**
- `dist/StackedDataTable/StackedDataTable.exe` 실행

### CLI

```bash
uv run python main.py
```

## 빌드 방법

### Mac

```bash
uv sync
uv run python build_mac.py
```

결과: `dist/StackedDataTable.app`

### Windows

```powershell
# uv 설치 (최초 1회)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 빌드
uv sync
uv run python build_windows.py
```

결과: `dist/StackedDataTable/StackedDataTable.exe`

## 배포

- **Mac**: `dist/StackedDataTable.app` 폴더를 압축해서 전달
- **Windows**: `dist/StackedDataTable/` 폴더 전체를 압축해서 전달

받는 사람은 Python 설치 없이 실행파일만 실행하면 됩니다.

## 프로젝트 구조

```
Stacked-DataTable/
├── src/stacked_datatable/
│   ├── __init__.py
│   └── core.py          # 핵심 로직 (파싱, Stack, 포맷)
├── gui.py               # GUI 앱 (pywebview)
├── main.py              # CLI 앱
├── build_mac.py         # Mac 빌드 스크립트
├── build_windows.py     # Windows 빌드 스크립트
├── pyproject.toml
└── README.md
```

## 의존성

- Python 3.11+
- flask
- pywebview
- pyinstaller (빌드용)

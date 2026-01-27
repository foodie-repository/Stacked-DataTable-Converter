# AGENTS.md

이 파일은 AI 코딩 에이전트(Claude, Cursor 등)가 이 저장소에서 작업할 때 참고하는 가이드입니다.

---

## 프로젝트 개요

- **프로젝트명**: Stacked-DataTable
- **언어**: Python 3.11
- **패키지 매니저**: uv (https://docs.astral.sh/uv/)
- **프로젝트 타입**: 라이브러리/애플리케이션

---

## 빌드/실행 명령어

### 환경 설정

```bash
# 가상환경 생성 및 의존성 설치 (최초 1회)
uv sync

# 프로젝트 실행
uv run python main.py

# Python REPL 실행
uv run python
```

### 의존성 관리

```bash
# 의존성 추가
uv add <패키지명>

# 개발 의존성 추가
uv add --dev <패키지명>

# 의존성 제거
uv remove <패키지명>

# 잠금 파일 업데이트
uv lock

# 의존성 동기화
uv sync
```

### 린트/포맷

```bash
# Ruff 린터 실행 (권장)
uv run ruff check .

# Ruff 자동 수정
uv run ruff check --fix .

# Ruff 포맷터 실행
uv run ruff format .

# 포맷 검사만 (수정 없이)
uv run ruff format --check .

# 타입 검사 (mypy 사용 시)
uv run mypy .
```

### 테스트

```bash
# 전체 테스트 실행 (pytest 사용 시)
uv run pytest

# 특정 파일 테스트
uv run pytest tests/test_example.py

# 특정 테스트 함수 실행
uv run pytest tests/test_example.py::test_function_name

# 특정 키워드로 테스트 필터링
uv run pytest -k "keyword"

# 상세 출력과 함께 테스트
uv run pytest -v

# 첫 번째 실패에서 중단
uv run pytest -x

# 커버리지 포함 테스트
uv run pytest --cov=src --cov-report=term-missing
```

---

## 코드 스타일 가이드라인

### 기본 원칙

- **PEP 8** 준수
- **PEP 257** Docstring 규약 준수
- 최대 줄 길이: **88자** (Black/Ruff 기본값)
- 들여쓰기: **스페이스 4칸** (탭 사용 금지)

### 네이밍 규칙

| 유형 | 규칙 | 예시 |
|------|------|------|
| 모듈 | snake_case | `data_processor.py` |
| 클래스 | PascalCase | `DataTable`, `StackedColumn` |
| 함수/메서드 | snake_case | `process_data()`, `get_value()` |
| 변수 | snake_case | `row_count`, `column_names` |
| 상수 | UPPER_SNAKE_CASE | `MAX_ROWS`, `DEFAULT_TIMEOUT` |
| Private | 언더스코어 접두사 | `_internal_method()`, `_cache` |

### 임포트 순서

```python
# 1. 표준 라이브러리
import os
import sys
from typing import Any, Optional

# 2. 서드파티 라이브러리
import pandas as pd
import numpy as np

# 3. 로컬 모듈
from .core import DataTable
from .utils import helpers
```

- 각 그룹 사이에 빈 줄 1개
- 알파벳 순서로 정렬
- `from` 임포트는 각 그룹의 마지막에

### 타입 힌트

```python
# 함수 시그니처에 타입 힌트 필수
def process_data(
    data: list[dict[str, Any]],
    columns: list[str] | None = None,
    *,
    strict: bool = False,
) -> pd.DataFrame:
    """데이터를 처리하여 DataFrame으로 반환합니다."""
    ...

# 복잡한 타입은 TypeAlias 사용
type RowData = dict[str, Any]
type ColumnSpec = list[str] | tuple[str, ...]

# Optional 대신 X | None 사용 (Python 3.10+)
def get_value(key: str) -> str | None:
    ...
```

### Docstring 형식 (Google 스타일)

```python
def calculate_statistics(
    data: list[float],
    exclude_outliers: bool = False,
) -> dict[str, float]:
    """데이터의 통계 정보를 계산합니다.

    Args:
        data: 분석할 숫자 데이터 리스트.
        exclude_outliers: True이면 이상치를 제외하고 계산.

    Returns:
        평균, 중앙값, 표준편차를 포함하는 딕셔너리.

    Raises:
        ValueError: data가 비어있는 경우.

    Example:
        >>> calculate_statistics([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3.0, 'std': 1.41}
    """
    ...
```

### 에러 처리

```python
# 구체적인 예외 타입 사용
try:
    result = risky_operation()
except FileNotFoundError:
    logger.error("파일을 찾을 수 없습니다")
    raise
except ValueError as e:
    logger.warning(f"잘못된 값: {e}")
    return default_value

# 커스텀 예외는 프로젝트 예외 클래스 상속
class DataTableError(Exception):
    """DataTable 관련 기본 예외."""
    pass

class ValidationError(DataTableError):
    """데이터 검증 실패 예외."""
    pass
```

### 클래스 구조

```python
class DataTable:
    """데이터 테이블을 관리하는 클래스.

    Attributes:
        name: 테이블 이름.
        columns: 컬럼 목록.
    """

    # 클래스 변수
    DEFAULT_PAGE_SIZE: int = 100

    def __init__(self, name: str, columns: list[str]) -> None:
        """DataTable을 초기화합니다."""
        self.name = name
        self.columns = columns
        self._cache: dict[str, Any] = {}

    # 프로퍼티
    @property
    def column_count(self) -> int:
        """컬럼 수를 반환합니다."""
        return len(self.columns)

    # Public 메서드
    def add_row(self, data: dict[str, Any]) -> None:
        """행을 추가합니다."""
        ...

    # Private 메서드
    def _validate_data(self, data: dict[str, Any]) -> bool:
        """데이터를 검증합니다."""
        ...
```

---

## 프로젝트 구조 (권장)

```
stacked-datatable/
├── src/
│   └── stacked_datatable/
│       ├── __init__.py
│       ├── core.py          # 핵심 클래스
│       ├── utils.py         # 유틸리티 함수
│       └── exceptions.py    # 커스텀 예외
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures
│   ├── test_core.py
│   └── test_utils.py
├── main.py
├── pyproject.toml
├── README.md
├── CLAUDE.md
└── AGENTS.md
```

---

## 주의사항

### 금지 사항
- `type: ignore` 주석 남용 금지
- 빈 `except:` 블록 금지
- 하드코딩된 경로 사용 금지
- 전역 변수 남용 금지

### 권장 사항
- 함수는 단일 책임 원칙 준수 (20줄 이하 권장)
- 매직 넘버 대신 상수 사용
- f-string 사용 (% 포맷팅, .format() 지양)
- Context manager 적극 활용 (`with` 문)
- 주석과 문서는 한국어 사용 가능

---

## 커밋 메시지 형식

```
<type>: <subject>

[optional body]

[optional footer]
```

**타입**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 포맷팅 (코드 변경 없음)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 변경

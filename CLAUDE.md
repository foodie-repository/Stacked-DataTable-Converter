# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

Stacked-DataTable은 Python 3.11 기반 프로젝트입니다. `uv` 패키지 매니저를 사용합니다.

## 개발 명령어

```bash
# 가상환경 생성 및 의존성 설치
uv sync

# 프로젝트 실행
uv run python main.py

# 의존성 추가
uv add <패키지명>

# 개발 의존성 추가
uv add --dev <패키지명>
```

## 코드 스타일

- PEP 8 준수
- 함수명: snake_case
- 클래스명: PascalCase
- 주석 및 문서: 한국어 가능

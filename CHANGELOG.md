# Changelog

All notable changes to DeepFileX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### 🔄 Planned
- 고급 검색 필터 (정규식, 날짜 범위)
- 대시보드 차트 (파일 분포 시각화)
- 영어 버전 (다국어 지원)
- AI 파일 분류 및 추천

---

## [1.3.0] - 2026-02-07

### 🎨 Changed
- **대규모 프로젝트 구조 개편**
  - 모든 소스 코드를 `src/` 폴더로 이동
  - 스크립트를 `scripts/` 폴더로 통합
  - 문서를 `docs/` 폴더로 정리
  - 릴리즈 파일을 `releases/` 폴더로 체계화
  - 광고 리소스를 `assets/` 폴더로 이동
  - 빌드 설정을 `build/` 폴더로 분리

### ✨ Added
- `.gitignore` 파일 추가 (Python, IDE, 프로젝트별 규칙)
- 개발 가이드 및 기여 가이드 (README.md)
- CHANGELOG.md (이 파일)

### 🗑️ Removed
- `__pycache__/` 폴더 삭제 (268KB 절약)
- 빈 폴더 삭제 (`backup_before_cleanup/`, `indexes/`)
- 구버전 파일 아카이브 (`scripts/legacy/`)

### 🔷 Rebranding (2025-08-28)
- **FileMRI → DeepFileX** 완전한 리브랜딩
- QuantumLayer 회사명 적용
- 의료 테마 → 프로페셔널 테크 테마 전환
- 모든 파일, 코드, 문서에서 브랜딩 일관성 확보

### 💰 Monetization
- **쿠팡파트너스 통합**
  - WebView2 기반 광고 시스템 구축
  - 로컬 웹서버 (Bottle) 통합
  - 광고 통계 추적 시스템
  - Adsterra 백업 시스템

### 🔄 Update System
- **자동 업데이트 시스템 개선**
  - 업데이트 팝업 UI/UX 개선 (텍스트 영역 3배 확대)
  - 카운트다운 타이머 제거 (사용자 압박 완화)
  - GitHub API 연동
  - 테스트 모드 지원

### 🐛 Bug Fixes
- UTF-8/Emoji 완벽 지원
- Unicode 인코딩 오류 수정
- 로깅 시스템 안정성 향상

---

## [1.2.0] - 2025-08-27

### ✨ Added
- **Everything-style 인스톨러** 완성
- Adsterra SmartLinks 시스템 구축
- 수익 추적 시스템 구현

### 🎨 Changed
- 프로젝트 구조 정리 및 최적화
- 빌드 시스템 최적화

### 🐛 Bug Fixes
- 성능 개선
- 불필요한 파일 정리

---

## [1.0.0] - 2025-08-26

### 🎉 Initial Release

#### ✨ Features
- **30+ 파일 형식 지원**
  - 문서: TXT, PDF, DOCX, XLSX, PPTX, HWP
  - 코드: PY, JS, JAVA, C, CPP, CS, HTML, CSS
  - 이미지: JPG, PNG, GIF, BMP, TIFF, WEBP, SVG
  - 압축: ZIP, RAR, 7Z, TAR, GZ

- **SQLite 기반 인덱싱**
  - 영구 인덱스 저장
  - 고속 검색 (밀리초 단위)
  - 인덱스 저장/불러오기

- **멀티스레딩 스캔**
  - 병렬 처리로 10,000+ 파일/분
  - 실시간 진행률 표시
  - 메모리 최적화

- **모던 UI**
  - Light/Dark 모드
  - 직관적인 사용자 인터페이스
  - PyQt6 기반 GUI

#### 📦 Deliverables
- FileMRI.exe (실행 파일)
- FileMRI_v1.0.0_Setup.exe (인스톨러)
- 소스 코드 및 문서

---

## Release Links

- **v1.3.0**: [DeepFileX v1.3.0](https://github.com/quantumlayer/deepfilex/releases/tag/v1.3.0)
- **v1.0.0**: [FileMRI v1.0.0](https://github.com/quantumlayer/deepfilex/releases/tag/v1.0.0)

---

## Versioning Guide

DeepFileX follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: 호환되지 않는 API 변경
- **MINOR** version: 하위 호환성 있는 기능 추가
- **PATCH** version: 하위 호환성 있는 버그 수정

---

**DeepFileX by QuantumLayer** - Advanced File Analysis System 🔷

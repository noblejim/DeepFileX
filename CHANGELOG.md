# Changelog

All notable changes to DeepFileX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### 🔄 Planned
- 고급 검색 필터 (정규식, 날짜 범위)
- 대시보드 차트 (파일 분포 시각화)
- 다국어 지원 (영어, 일본어)
- AI 기반 파일 분류 및 추천

---

## [1.4.1] - 2026-02-09

### 🔧 Fixed
- **검색 크래시 수정**: 검색 중 프로그램 종료 문제 해결
- **예외 처리 강화**: `perform_search()` 및 `display_search_results()` 함수에 포괄적 예외 처리 추가
- **개별 결과 보호**: 한 개 결과 오류가 전체 검색 실패로 이어지지 않도록 개선
- **에러 로깅**: 상세한 traceback 로그 기록 (`exc_info=True`)
- **사용자 피드백**: 오류 발생 시 명확한 메시지 및 상태바 업데이트

### 📝 Technical Details
- **File**: `src/filemri.py:2876-2983`
- **Issue**: PyQt6 signal handlers lacked exception handling
- **Solution**: Comprehensive try-except blocks with logging
- **Impact**: Prevents application crashes during search operations

---

## [1.4.0] - 2026-02-08

### ⬆️ Upgraded
- **PyQt6**: 6.9.1 → 6.10.2
- **PyQt6-WebEngine**: 6.7.0 → 6.10.0
- **PyQt6-Qt6**: 6.9.1 → 6.10.2
- **PyQt6-WebEngine-Qt6**: 6.7.3 → 6.10.2

### 🔧 Fixed
- **DLL 로드 문제**: PyQt6 버전 불일치로 인한 DLL 로드 실패 해결
- **UI 안정성**: 웹 컴포넌트 안정성 개선
- **예외 처리**: 다양한 UI 이벤트 핸들러에 예외 처리 추가

### 🎨 Improved
- **성능 최적화**: 메모리 사용량 및 응답 속도 개선
- **UI 반응성**: 사용자 인터페이스 반응 속도 향상

---

## [1.3.0] - 2026-02-07

### 🎨 Changed
- **프로젝트 구조 재편**
  - 소스 코드를 `src/` 폴더로 이동
  - 스크립트를 `scripts/` 폴더로 통합
  - 문서를 `docs/` 폴더로 정리
  - 릴리즈 파일을 `releases/` 폴더로 체계화
  - 빌드 설정을 `build/` 폴더로 분리

### ✨ Added
- **자동 업데이트 시스템**: GitHub API 연동 자동 업데이트 체커
- **`.gitignore`**: Python, IDE, 프로젝트별 규칙 추가
- **개발 가이드**: README.md에 기여 가이드 추가
- **CHANGELOG.md**: 버전별 변경사항 문서화

### 🐛 Fixed
- **Unicode/Emoji 지원**: UTF-8 인코딩 완벽 지원
- **로깅 안정성**: 로깅 시스템 에러 처리 개선

### 🗑️ Removed
- **`__pycache__/`**: 캐시 폴더 삭제 (268KB 절약)
- **빈 폴더**: 사용하지 않는 디렉토리 정리
- **레거시 파일**: 구버전 파일 아카이브

### 🔷 Rebranding
- **프로젝트명 변경**: 전체 리브랜딩 완료
- **회사명 적용**: QuantumLayer 브랜딩
- **테마 전환**: 프로페셔널 테크 테마로 변경
- **일관성 확보**: 모든 파일, 코드, 문서 일관성 유지

---

## [1.2.0] - 2025-08-27

### ✨ Added
- **인스톨러 시스템**: Everything-style 인스톨러 완성
- **설치 옵션**: 사용자 정의 설치 경로 지원

### 🎨 Changed
- **프로젝트 구조**: 파일 구조 최적화
- **빌드 시스템**: PyInstaller 설정 개선

### 🐛 Fixed
- **성능 개선**: 스캔 및 검색 속도 최적화
- **파일 정리**: 불필요한 파일 제거

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
- DeepFileX.exe (실행 파일)
- 소스 코드 및 문서

---

## Release Links

- **v1.4.1**: [DeepFileX v1.4.1](https://github.com/noblejim/DeepFileX/releases/tag/v1.4.1)
- **v1.4.0**: [DeepFileX v1.4.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.4.0)
- **v1.3.0**: [DeepFileX v1.3.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.3.0)
- **v1.2.0**: [DeepFileX v1.2.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.2.0)
- **v1.0.0**: [DeepFileX v1.0.0](https://github.com/noblejim/DeepFileX/releases/tag/v1.0.0)

---

## Versioning Guide

DeepFileX follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: 호환되지 않는 API 변경
- **MINOR** version: 하위 호환성 있는 기능 추가
- **PATCH** version: 하위 호환성 있는 버그 수정

---

**DeepFileX by QuantumLayer** - Advanced File Analysis System 🔷

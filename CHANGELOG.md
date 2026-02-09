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

## [1.4.1] - 2026-02-09

### 🔧 Bug Fixes

#### 검색 크래시 문제 해결 (Critical Fix)
- **검색 중 프로그램 종료 문제 수정**: `perform_search()` 함수에 예외 처리 추가
- **검색 결과 표시 안정성 강화**: `display_search_results()` 함수에 포괄적 예외 처리 구현
- **개별 결과 아이템 보호**: 한 개 결과 오류가 전체 검색 실패로 이어지지 않도록 개선
- **SmartLinks 컨텍스트 업데이트 보호**: 광고 시스템 오류가 검색에 영향 없도록 분리
- **에러 로깅 강화**: 검색 오류 발생 시 전체 traceback 로그 기록 (`exc_info=True`)
- **사용자 피드백 개선**: 오류 발생 시 명확한 메시지 표시 및 상태바 업데이트

### 📝 Technical Details
- **File**: `src/filemri.py:2876-2983`
- **Issue**: PyQt6 signal handlers (timer callback) lacked exception handling
- **Solution**: Comprehensive try-except blocks with logging and user feedback
- **Impact**: Prevents application crashes during search operations

---

## [1.4.0] - 2026-02-08

### 🎉 Major Features

#### GitHub Pages 기반 광고 시스템
- **실제 광고 이미지 표시**: Adsterra 배너 광고가 프로그램 내부에서 직접 표시
- **광고 자동 회전**: Adsterra가 제공하는 광고 자동 변경 시스템
- **외부 브라우저 연동**: 광고 클릭 시 기본 브라우저에서 광고 페이지 자동 열림
- **광고 배너 유지**: 클릭 후에도 프로그램 내 배너가 계속 표시되도록 자동 리로드
- **최적화된 광고 높이**: 240px 높이로 광고 이미지 완전 표시

### ⬆️ Upgraded
- **PyQt6**: 6.9.1 → 6.10.2
- **PyQt6-WebEngine**: 6.7.0 → 6.10.0
- **PyQt6-Qt6**: 6.9.1 → 6.10.2
- **PyQt6-WebEngine-Qt6**: 6.7.3 → 6.10.2

### ✨ Added
- `github_pages_ad_widget.py`: GitHub Pages 광고 위젯 (QWebEngineView 기반)
- `AdWebEnginePage`: 커스텀 웹 엔진 페이지 클래스 (외부 링크 처리)
- `acceptNavigationRequest()`: 네비게이션 요청 인터셉터
- `createWindow()`: JavaScript 팝업 처리 핸들러
- 광고 클릭 후 자동 리로드 기능 (QTimer 100ms)
- 상세한 네비게이션 디버깅 로그

### 🔧 Fixed
- **QWebEngineView DLL 로드 실패**: PyQt6 버전 불일치 문제 해결
- **광고 배너 사라짐**: 클릭 후 배너가 사라지던 버그 수정
- **외부 링크 네비게이션**: JavaScript window.open 및 링크 클릭 처리 개선
- **광고 이미지 잘림**: 컨테이너 높이를 90px → 140px → 190px → 240px로 단계적 증가

### 🎨 Changed
- 광고 시스템 우선순위:
  1. GitHubPagesAdWidget (최우선)
  2. RotatingImageBanner (Fallback 1)
  3. SmartLinksAdWidget (Fallback 2)
- `test_mode`: True → False (실제 GitHub API 사용)
- GitHub 저장소 URL: `quantumlayer/deepfilex` → `noblejim/DeepFileX`
- 광고 컨테이너 크기: 970×90 → 970×240

### 🚀 Deployment
- v1.4.0 빌드 스크립트 작성 (`build_v1.4.0.bat`)
- PyInstaller 스펙 파일 생성 (`DeepFileX_v1.4.0.spec`)
- 실행 파일 크기: ~222MB
- GitHub Release 생성 및 게시

### 📝 Documentation
- `RELEASE_NOTES_v1.4.0.md`: 상세 릴리즈 노트
- `docs/ads/README.md`: 광고 시스템 설정 가이드
- `docs/ads/index.html`: GitHub Pages 광고 페이지 템플릿

### 🧪 Testing
- 광고 시스템 정상 작동 확인
- 광고 클릭 → 브라우저 열림 확인
- 광고 배너 유지 확인
- 자동 업데이트 시스템 검증

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

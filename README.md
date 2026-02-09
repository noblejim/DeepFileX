# 🔷 DeepFileX

**DeepFileX** - 차세대 파일 검색 및 분석 솔루션

> **Latest**: v1.4.1 (2026-02-09) - 안정성 개선 및 버그 수정

[![Latest Release](https://img.shields.io/github/v/release/noblejim/DeepFileX)](https://github.com/noblejim/DeepFileX/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)

## 🎯 프로젝트 개요

DeepFileX는 고급 알고리즘으로 파일 시스템을 분석하는 혁신적인 파일 관리 도구입니다. 빠르고 정확한 파일 검색과 인덱싱을 제공합니다.

## 🚀 빠른 시작

### 다운로드 및 실행

1. **[최신 릴리스 다운로드](https://github.com/noblejim/DeepFileX/releases)**
2. **DeepFileX.exe 실행**

개발자 모드는 [개발 가이드](#-개발-가이드)를 참조하세요.

## ⭐ 핵심 기능

### 🔬 고급 파일 분석
- **30+ 파일 형식 지원**: 문서, 코드, 이미지, 압축 파일
- **실시간 검색**: 파일명 및 내용 검색
- **영구 인덱싱**: SQLite 기반 데이터베이스

### ⚡ 초고속 성능
- **멀티스레딩**: 병렬 처리로 빠른 스캔
- **10,000+ 파일/분**: 대용량 디렉토리 처리
- **메모리 최적화**: 효율적인 리소스 사용

### 🎨 현대적 UI
- **Light/Dark 모드**: 눈에 편안한 테마
- **직관적 인터페이스**: 쉬운 사용법
- **실시간 진행률**: 작업 상태 표시

## 📁 지원 파일 형식

| 카테고리 | 확장자 |
|---------|--------|
| **📄 문서** | `.txt`, `.md`, `.log`, `.csv`, `.json`, `.xml`, `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.hwp` |
| **💻 코드** | `.py`, `.js`, `.java`, `.c`, `.cpp`, `.cs`, `.html`, `.css`, `.php`, `.go`, `.rs` |
| **🖼️ 이미지** | `.jpg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`, `.ico` |
| **📦 압축** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2` |

## 💾 시스템 요구사항

- **OS**: Windows 10+ (64bit)
- **RAM**: 4GB+ 권장
- **저장공간**: 100MB+
- **Python**: 3.8+ (개발자 모드만 해당)

## 📊 성능 지표

- 스캔 속도: **10,000+ 파일/분**
- 검색 속도: **밀리초 단위 응답**
- 메모리 사용: **100MB 내외**

## 🔧 사용 방법

### 1️⃣ 파일 스캔
1. "Scan Folders" 버튼으로 폴더 선택
2. "Start Scan" 버튼으로 스캔 시작
3. 실시간 진행률 확인

### 2️⃣ 파일 검색
1. 검색창에 키워드 입력
2. Enter 키 또는 "Search" 버튼 클릭
3. 결과에서 파일 선택하여 미리보기

### 3️⃣ 인덱스 관리
- **Save Index**: 현재 인덱스 저장
- **Load Index**: 저장된 인덱스 불러오기
- **Clear Records**: 인덱스 초기화

## 📈 최근 업데이트

### v1.4.1 (2026-02-09)
- 🔧 검색 중 크래시 문제 수정
- 🛡️ 예외 처리 강화
- 📝 상세 에러 로깅 추가

### v1.4.0 (2026-02-08)
- ⬆️ PyQt6 6.10.2 업그레이드
- 🐛 UI 안정성 개선
- 🎨 성능 최적화

### v1.3.0 (2026-02-07)
- 🎨 프로젝트 구조 재편
- ✨ 자동 업데이트 시스템
- 🐛 Unicode/Emoji 지원 개선

📖 전체 변경사항은 [CHANGELOG.md](CHANGELOG.md)를 참조하세요.

## 🛠️ 개발 가이드

### 개발 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/noblejim/DeepFileX.git
cd DeepFileX

# 2. 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate  # Windows

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 실행
python src\filemri.py
```

### 빌드 방법

```bash
# PyInstaller로 실행 파일 생성
pyinstaller build\specs\DeepFileX_v1.4.1.spec --clean
```

빌드 결과물: `build/temp/dist/DeepFileX.exe`

### 프로젝트 구조

```
DeepFileX/
├── src/                   # 소스 코드
│   ├── filemri.py         # 메인 애플리케이션
│   ├── update_checker.py  # 자동 업데이트
│   └── version_config.py  # 버전 관리
├── tests/                 # 테스트 파일
├── build/                 # 빌드 관련
│   ├── specs/             # PyInstaller 설정
│   └── scripts/           # 빌드 스크립트
├── docs/                  # 문서
│   ├── releases/          # 릴리즈 노트
│   └── development/       # 개발 문서
├── README.md              # 프로젝트 소개
├── CHANGELOG.md           # 변경 이력
├── LICENSE.txt            # MIT 라이선스
└── requirements.txt       # 의존성
```

## 🤝 기여하기

기여를 환영합니다! 다음 절차를 따라주세요:

1. **Fork** 후 저장소 클론
2. **브랜치 생성**: `git checkout -b feature/AmazingFeature`
3. **변경사항 커밋**: `git commit -m "✨ feat: Add AmazingFeature"`
4. **푸시**: `git push origin feature/AmazingFeature`
5. **Pull Request 생성**

### 기여 가이드라인

- ✅ PEP 8 코딩 스타일 준수
- ✅ 변경사항 충분히 테스트
- ✅ 새 기능은 문서 업데이트
- ✅ Python 3.8+ 호환성 유지
- ✅ PR에 관련 이슈 번호 명시

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE.txt](LICENSE.txt)를 참고하세요.

## 📞 지원 및 문의

- **GitHub**: https://github.com/noblejim/DeepFileX
- **Releases**: https://github.com/noblejim/DeepFileX/releases
- **Issues**: https://github.com/noblejim/DeepFileX/issues
- **Discussions**: https://github.com/noblejim/DeepFileX/discussions

---

**DeepFileX v1.4.1** by **QuantumLayer** - Advanced File Analysis System 🔷

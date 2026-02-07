# 🔷 DeepFileX v1.3.0

**DeepFileX** - 차세대 파일 검색 및 분석 솔루션

## 🎯 프로젝트 개요

DeepFileX는 딥러닝 기술로 파일 시스템을 분석하는 혁신적인 파일 관리 도구입니다. 첨단 알고리즘으로 파일들을 정밀하게 스캔하고 분석합니다.

## 🚀 빠른 시작

### 🔥 즉시 실행 (권장)
```cmd
# 배포 버전 실행 (Python 설치 불요)
DeepFileX.exe
```

### 🛠️ 개발자 모드
```cmd
# Python으로 직접 실행
scripts\run_deepfilex.bat
```

### 📦 수동 설치
```cmd
pip install -r requirements.txt
python src\filemri.py
```

## ⭐ 핵심 기능

### 🔬 고급 스캔 기능
- **파일 분석**: 30+ 파일 형식 지원
- **실시간 검색**: 파일명 + 내용 검색
- **모던 UI**: 직관적인 사용자 인터페이스

### ⚡ 초고속 성능
- **멀티스레딩 스캔**: 병렬 처리로 극속 스캔
- **SQLite 데이터베이스**: 영구 인덱스 저장
- **메모리 최적화**: 대용량 파일도 부드럽게

### 🎨 현대적 테마
- **Light/Dark 모드**: 사용자 친화적 디자인
- **DeepFileX 색상 스키마**: 딥 블루 기반
- **세련된 패널**: 모던 스타일 UI

## 📁 지원 파일 형식 (30+)

### 📄 문서
- **텍스트**: `.txt`, `.md`, `.log`, `.csv`, `.json`, `.xml`
- **오피스**: `.pdf`, `.docx`, `.pptx`, `.xlsx`
- **한글**: `.hwp`, `.hwpx`

### 💻 코드
- **프로그래밍**: `.py`, `.js`, `.java`, `.c`, `.cpp`, `.cs`
- **웹**: `.html`, `.css`, `.php`, `.rb`
- **최신 언어**: `.go`, `.rs`

### 🖼️ 이미지
- **일반**: `.jpg`, `.png`, `.gif`, `.bmp`
- **고급**: `.tiff`, `.webp`, `.svg`, `.ico`

### 📦 압축
- **표준**: `.zip`, `.rar`, `.7z`
- **리눅스**: `.tar`, `.gz`, `.bz2`

## 💾 시스템 요구사항

- **OS**: Windows 10+ (64bit)
- **RAM**: 4GB+ 권장
- **저장공간**: 100MB+
- **Python**: 3.8+ (개발자 모드)

## 📊 성능 지표

- **스캔 속도**: 10,000+ 파일/분
- **검색 속도**: 밀리초 단위 응답
- **메모리 사용량**: 100MB 내외
- **실행파일 크기**: 50.6MB

## 🏗️ 프로젝트 구조

```
DeepFileX/
├── 📂 src/                   # 소스 코드
│   ├── filemri.py           # 메인 애플리케이션 (3,345 라인)
│   ├── filemri_smartlinks.py # 광고 수익화 시스템
│   ├── update_checker.py    # 자동 업데이트 체커
│   ├── webview2_ad_widget.py # WebView2 광고 위젯
│   ├── version_config.py    # 버전 관리
│   └── version_info.py      # 버전 정보
│
├── 📂 scripts/              # 실행 스크립트
│   ├── DeepFileX.bat        # 메인 런처
│   ├── run_deepfilex.bat    # 개발자 모드 실행
│   ├── quick_deploy.bat     # GitHub 배포 스크립트
│   └── system_check.bat     # 시스템 호환성 체크
│
├── 📂 releases/             # 릴리즈 파일
│   ├── v1.0.0/              # v1.0.0 릴리즈
│   └── v1.3.0/              # 최신 릴리즈 (159MB)
│       ├── DeepFileX_v1.3.0.exe         # 실행 파일 (79MB)
│       └── DeepFileX_v1.3.0_Setup.exe   # 인스톨러 (80MB)
│
├── 📂 docs/                 # 문서
│   ├── system_requirements.md
│   ├── TEST_REPORT.md
│   ├── reports/             # 개발 리포트
│   └── archive/             # 과거 문서
│
├── 📂 assets/               # 리소스
│   └── ads/                 # 광고 배너
│
├── 📂 build/                # 빌드 설정
│   ├── FileMRI_Phase11_Fixed.spec  # PyInstaller 설정
│   └── FileMRI_Installer.iss       # Inno Setup 스크립트
│
├── 📂 website/              # 웹사이트
│   ├── index.html           # DeepFileX 웹사이트
│   └── legacy.html          # 구 FileMRI 웹사이트
│
├── 📄 README.md             # 프로젝트 소개 (이 파일)
├── 📄 LICENSE.txt           # MIT 라이선스
└── 📄 requirements.txt      # Python 의존성
```

## 🔧 사용 방법

### 1️⃣ 파일 스캔 (File Scan)
1. "Scan Folders" 버튼으로 폴더 선택
2. "Start Scan" 버튼으로 스캔 시작
3. 실시간 진행률 확인

### 2️⃣ 파일 검색 (File Search)
1. 검색창에 키워드 입력
2. Enter 키 또는 "Search" 버튼 클릭
3. 결과에서 파일 선택하여 미리보기

### 3️⃣ 인덱스 관리 (Index Management)
- **Save Index**: 현재 인덱스 저장
- **Load Index**: 저장된 인덱스 불러오기
- **Clear Records**: 인덱스 초기화

## 🎨 UI 테마

### 🌞 Light 모드
- **기본색**: #2c5aa0 (딥 블루)
- **버튼**: 검정 글자 (#000000)
- **배경**: 흰색 기반

### 🌙 Dark 모드
- **기본색**: #2c5aa0 (딥 블루)
- **버튼**: 흰색 글자 (#ffffff)
- **배경**: 어두운 테마

## 📈 개발 히스토리

### v1.3.0 (2025-08-28)
- ✅ FileMRI → DeepFileX 리브랜딩
- ✅ QuantumLayer 회사명 적용
- ✅ 자동 업데이트 시스템 추가
- ✅ SmartLinks 수익화 시스템 통합
- ✅ Unicode/Emoji 완벽 지원
- ✅ 성능 최적화 및 안정성 향상

### v1.2.0 (2025-08-27)
- ✅ 인스톨러 시스템 구축
- ✅ 프로젝트 구조 최적화

### v1.0.0 (2025-08-26)
- ✅ 초기 릴리즈
- ✅ 30+ 파일 형식 지원
- ✅ SQLite 기반 인덱싱

## 🛠️ 개발 가이드

### 개발 환경 설정

1. **저장소 클론**
   ```bash
   git clone https://github.com/quantumlayer/deepfilex.git
   cd deepfilex
   ```

2. **가상환경 생성 (권장)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **개발 모드로 실행**
   ```bash
   python src\filemri.py
   # 또는
   scripts\run_deepfilex.bat
   ```

### 프로젝트 구조 이해

- **src/**: 모든 Python 소스 코드
  - `filemri.py`: 메인 GUI 애플리케이션
  - `filemri_smartlinks.py`: 광고 수익화 시스템
  - `update_checker.py`: 자동 업데이트 기능

- **scripts/**: 실행 및 배포 스크립트
  - `run_deepfilex.bat`: 개발용 실행 스크립트
  - `quick_deploy.bat`: GitHub 릴리즈 배포

- **docs/**: 모든 문서 및 리포트
  - `reports/`: 개발 진행 리포트
  - `archive/`: 과거 문서 보관

- **releases/**: 버전별 릴리즈 파일
  - `v1.3.0/`: 최신 릴리즈 (실행 파일 + 인스톨러)

### 빌드 방법

1. **PyInstaller로 실행 파일 생성**
   ```bash
   pyinstaller build\FileMRI_Phase11_Fixed.spec
   ```

2. **Inno Setup으로 인스톨러 생성**
   ```bash
   # Inno Setup Compiler 실행
   iscc build\FileMRI_Installer.iss
   ```

### 코딩 규칙

- **Python 스타일**: PEP 8 준수
- **인코딩**: UTF-8 사용 (이모지 지원)
- **커밋 메시지**:
  - 형식: `🔷 타입: 간단한 설명`
  - 예: `✨ feat: Add dark mode toggle button`
- **브랜치 전략**:
  - `master`: 안정 버전
  - `feature/*`: 새 기능 개발
  - `bugfix/*`: 버그 수정

## 🤝 기여하기

### 기여 프로세스

1. **이슈 확인 또는 생성**
   - 기존 이슈 검색
   - 새로운 기능이나 버그는 이슈 생성

2. **Fork & Clone**
   ```bash
   # GitHub에서 Fork 후
   git clone https://github.com/YOUR_USERNAME/deepfilex.git
   ```

3. **브랜치 생성**
   ```bash
   git checkout -b feature/AmazingFeature
   # 또는
   git checkout -b bugfix/FixSomething
   ```

4. **코드 작성 및 테스트**
   - 코드 작성
   - 로컬에서 충분히 테스트
   - 커밋 메시지 작성 규칙 준수

5. **커밋 및 푸시**
   ```bash
   git add .
   git commit -m "✨ feat: Add some AmazingFeature"
   git push origin feature/AmazingFeature
   ```

6. **Pull Request 생성**
   - GitHub에서 PR 생성
   - 변경사항 설명 작성
   - 리뷰 대기

### 기여 가이드라인

- ✅ 코드 품질: PEP 8 준수
- ✅ 테스트: 변경사항 테스트 완료
- ✅ 문서화: 새 기능은 문서 업데이트
- ✅ 호환성: Python 3.8+ 호환성 유지
- ✅ 이슈 링크: PR에 관련 이슈 번호 명시

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE.txt` 파일을 참고하세요.

## 📞 지원 및 문의

- **GitHub**: https://github.com/quantumlayer/deepfilex
- **Email**: contact@quantumlayer.com
- **이슈 리포트**: GitHub Issues 활용
- **기능 제안**: Discussion 탭 활용

## 🏆 특별 감사

- **UI/UX 디자인**: 현대적 인터페이스 참조
- **성능 최적화**: 커뮤니티 기여자들의 도움
- **QuantumLayer 팀**: 지속적인 개발과 지원

---

**DeepFileX v1.3.0** by **QuantumLayer** - Advanced File Analysis System 🔷💻

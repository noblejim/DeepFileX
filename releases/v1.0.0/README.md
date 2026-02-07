# 🏥 FileMRI v1.0

**FileMRI (File Medical Resonance Imaging)** - 파일을 의료용 MRI처럼 스캔하고 진단하는 초고속 파일 검색 도구

## 🎯 프로젝트 개요

FileMRI는 파일 시스템을 의료진단 관점에서 접근하는 혁신적인 파일 관리 도구입니다. 의료용 MRI가 인체를 스캔하듯, FileMRI는 컴퓨터의 파일들을 정밀하게 스캔하고 분석합니다.

## 🚀 빠른 시작

### 🔥 즉시 실행 (권장)
```cmd
# 배포 버전 실행 (Python 설치 불요)
FileMRI_Optimized.exe
```

### 🛠️ 개발자 모드
```cmd
# Python으로 직접 실행
run_filemri.bat
```

### 📦 수동 설치
```cmd
pip install -r requirements.txt
python filemri.py
```

## ⭐ 핵심 기능

### 🔬 MRI 스캔 기능
- **파일 진단 스캔**: 30+ 파일 형식 지원
- **실시간 진단**: 파일명 + 내용 검색
- **의료차트 스타일 UI**: 직관적인 진단 인터페이스

### ⚡ 초고속 성능
- **멀티스레딩 스캔**: 병렬 처리로 극속 스캔
- **SQLite 데이터베이스**: 영구 인덱스 저장
- **메모리 최적화**: 대용량 파일도 부드럽게

### 🎨 의료진단 테마
- **Light/Dark 모드**: 의료기기 스타일
- **MRI 색상 스키마**: 의료용 파란색 기반
- **진단 패널**: 병원 차트 스타일 UI

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
C:\FileMRI\
├── 📄 filemri.py              # 메인 애플리케이션 (2,394줄)
├── 🚀 run_filemri.bat        # 실행 스크립트
├── 🎯 FileMRI_Optimized.exe  # 배포용 실행파일 (50.6MB)
├── 📋 requirements.txt       # 의존성 라이브러리
├── 📜 LICENSE.txt           # MIT 라이선스
└── 📁 indexes/              # 인덱스 저장소
```

## 🔧 사용 방법

### 1️⃣ 파일 스캔 (File Scan)
1. "Scan Folders" 버튼으로 폴더 선택
2. "Start Diagnosis" 버튼으로 스캔 시작
3. 실시간 진행률 확인

### 2️⃣ 파일 진단 (File Diagnosis)
1. 검색창에 키워드 입력
2. Enter 키 또는 "Diagnose" 버튼 클릭
3. 결과에서 파일 선택하여 미리보기

### 3️⃣ 인덱스 관리 (Index Management)
- **Save Index**: 현재 인덱스 저장
- **Load Index**: 저장된 인덱스 불러오기
- **Clear Records**: 인덱스 초기화

## 🎨 UI 테마

### 🌞 Light 모드
- **기본색**: #2c5aa0 (의료용 파란색)
- **버튼**: 검정 글자 (#000000)
- **배경**: 흰색 기반

### 🌙 Dark 모드
- **기본색**: #2c5aa0 (의료용 파란색)
- **버튼**: 흰색 글자 (#ffffff)
- **배경**: 어두운 테마

## 📈 개발 히스토리

### v1.0.0 (2025-08-26)
- ✅ InsightSearch → FileMRI 완전 리브랜딩
- ✅ 의료진단 UI 테마 적용
- ✅ 50.6MB 최적화 빌드 완성
- ✅ Phase 4 완료 및 배포 준비

### 이전 버전 (InsightSearch 시절)
- 초고속 검색 엔진 구현
- 30+ 파일 형식 지원
- SQLite 기반 인덱싱

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE.txt` 파일을 참고하세요.

## 📞 지원 및 문의

- **이슈 리포트**: GitHub Issues 활용
- **기능 제안**: Discussion 탭 활용
- **기술 문의**: 개발자 연락처 참조

## 🏆 특별 감사

- **의료진단 컨셉**: 의료계 전문가들의 피드백
- **UI/UX 디자인**: 현대적 의료기기 인터페이스 참조
- **성능 최적화**: 커뮤니티 기여자들의 도움

---

**FileMRI v1.0** - 파일을 진단하다, 더 나은 파일 관리의 시작 🏥💻
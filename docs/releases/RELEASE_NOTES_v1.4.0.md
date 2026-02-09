# DeepFileX v1.4.0 Release Notes

**Release Date**: 2026-02-08
**Build**: 140
**Status**: Stable Release

---

## 🎉 주요 신규 기능

### GitHub Pages 기반 광고 시스템
- ✅ **실제 광고 이미지 표시**: Adsterra 배너 광고가 프로그램 내에서 직접 표시됩니다
- ✅ **광고 자동 회전**: 광고가 자동으로 변경되어 다양한 광고를 볼 수 있습니다
- ✅ **외부 브라우저 연동**: 광고 클릭 시 기본 브라우저에서 자동으로 광고 페이지가 열립니다
- ✅ **광고 배너 유지**: 광고 클릭 후에도 프로그램 내 배너가 계속 표시됩니다
- ✅ **최적화된 광고 높이**: 240px 높이로 광고 이미지가 완전히 표시됩니다

### 기술적 개선사항
- ✅ **PyQt6 6.10.2 업그레이드**: 최신 버전으로 업그레이드하여 안정성 향상
- ✅ **QWebEngineView 지원**: 웹 엔진을 통한 풍부한 광고 콘텐츠 표시
- ✅ **GitHub Pages 호스팅**: 광고 코드를 GitHub Pages에서 관리하여 업데이트 용이

---

## 🔧 버그 수정 및 개선

### 광고 시스템 안정화
- 🔧 **QWebEngineView DLL 로드 문제 해결**: PyQt6 버전 불일치로 인한 DLL 로드 오류 수정
- 🔧 **광고 배너 사라짐 문제 수정**: 광고 클릭 후 배너가 사라지던 문제 해결
- 🔧 **외부 링크 네비게이션 개선**: JavaScript 팝업 및 링크 클릭 처리 개선
- 🔧 **광고 이미지 잘림 해결**: 광고 컨테이너 높이 최적화로 전체 이미지 표시

---

## 📊 시스템 요구사항

### 필수 요구사항
- **운영체제**: Windows 10/11 (64bit)
- **메모리**: 최소 512MB RAM (권장 2GB)
- **디스크 공간**: 100MB 이상
- **인터넷 연결**: 광고 및 업데이트 확인용

### Python 환경 (소스 실행 시)
- **Python**: 3.8.0 이상 (권장 3.13.0)
- **PyQt6**: 6.10.2 이상
- **PyQt6-WebEngine**: 6.10.0 이상

---

## 📥 다운로드

### 실행 파일 (.exe)
- **DeepFileX_v1.4.0.exe** (권장)
  - 설치 불필요, 바로 실행
  - 모든 필수 라이브러리 포함
  - 크기: ~80MB

### 소스 코드
- **Source code (zip)**
- **Source code (tar.gz)**

---

## 🚀 설치 및 실행

### 실행 파일 사용 (권장)
1. `DeepFileX_v1.4.0.exe` 다운로드
2. 더블클릭하여 실행
3. Windows Defender 경고가 나올 수 있습니다 (정상)
   - "추가 정보" → "실행" 클릭

### 소스 코드 실행
1. 저장소 클론:
   ```bash
   git clone https://github.com/noblejim/DeepFileX.git
   cd DeepFileX
   ```

2. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

3. 실행:
   ```bash
   python src/deepfilex.py
   ```

---

## 🔄 자동 업데이트

이 버전부터 자동 업데이트 시스템이 실제 GitHub API를 사용합니다:
- 프로그램 시작 시 자동으로 업데이트 확인
- 새 버전 발견 시 알림 표시
- 7일마다 자동 확인

---

## 📋 변경사항 전체 목록

### 추가된 기능
1. GitHub Pages 기반 Adsterra 배너 광고 시스템
2. 실제 광고 이미지 표시 및 자동 회전
3. 광고 클릭 시 외부 브라우저 자동 열기
4. 광고 높이 최적화 (240px)
5. PyQt6 6.10.2 업그레이드
6. 광고 클릭 후 배너 유지 기능

### 수정된 버그
1. QWebEngineView DLL 로드 문제
2. 광고 배너 사라짐 문제
3. 외부 링크 네비게이션 처리
4. 광고 이미지 잘림 문제

### 기술적 변경
1. `github_pages_ad_widget.py` 추가
2. `version_config.py` v1.4.0 업데이트
3. GitHub 저장소 URL 업데이트 (noblejim/DeepFileX)
4. 테스트 모드 비활성화 (실제 GitHub API 사용)

---

## 🐛 알려진 이슈

현재 알려진 주요 이슈는 없습니다.

문제 발견 시 GitHub Issues에 제보해주세요:
https://github.com/noblejim/DeepFileX/issues

---

## 💬 피드백 및 지원

- **GitHub Issues**: https://github.com/noblejim/DeepFileX/issues
- **GitHub Discussions**: https://github.com/noblejim/DeepFileX/discussions
- **GitHub Repository**: https://github.com/noblejim/DeepFileX

---

## 📜 라이선스

MIT License
© 2025-2026 QuantumLayer. All rights reserved.

---

## 🙏 감사의 말

DeepFileX를 사용해주셔서 감사합니다!

이 버전은 광고 시스템의 대대적인 개선으로 더 나은 사용자 경험과 안정적인 수익 창출을 목표로 합니다.

**Powered by Adsterra** 🚀

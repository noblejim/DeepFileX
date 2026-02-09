# DeepFileX v1.4.1 Release Notes

**Release Date**: 2026-02-09
**Build**: 141
**Status**: Stable Release (Bug Fix)

---

## 🔧 주요 버그 수정

### 검색 중 프로그램 크래시 문제 해결 (Critical Fix)

v1.4.0에서 발견된 치명적인 버그를 수정했습니다:

- ✅ **검색 중 프로그램 종료 문제 수정**: 검색창에 텍스트 입력 시 발생하던 크래시 완전 해결
- ✅ **포괄적 예외 처리 추가**: `perform_search()` 및 `display_search_results()` 함수에 완벽한 예외 처리 구현
- ✅ **개별 결과 보호**: 검색 결과 중 하나에 오류가 있어도 전체 검색이 실패하지 않도록 개선
- ✅ **에러 로깅 강화**: 문제 발생 시 상세한 traceback 로그 기록으로 디버깅 용이
- ✅ **사용자 피드백 개선**: 오류 발생 시 명확한 메시지와 상태 표시

---

## 🐛 수정된 버그

### 1. 검색 중 프로그램 종료 문제
**증상**: 인덱스 로드 후 검색창에 텍스트를 입력하면 프로그램이 갑자기 종료됨

**원인**:
- PyQt6 signal handler (timer callback)에 예외 처리가 없었음
- 검색 중 발생하는 예외가 로그되지 않고 프로그램 종료를 야기

**해결**:
```python
# perform_search() 함수에 try-except 추가
try:
    # 검색 로직
    ...
except Exception as e:
    logger.error(f"Search failed: {e}", exc_info=True)
    self.status_bar.showMessage(f"Search error: {str(e)}")
```

### 2. 검색 결과 표시 오류
**증상**: 특정 검색 결과에 문제가 있으면 전체 검색 실패

**해결**:
```python
# 개별 결과 아이템 처리에 try-except 추가
for result in results:
    try:
        # 결과 표시 로직
        ...
    except Exception as item_error:
        logger.warning(f"Error displaying result item: {item_error}")
        continue  # 다음 결과로 계속 진행
```

---

## 📊 기술적 세부사항

### 변경된 파일
- **src/deepfilex.py** (lines 2876-2983)
  - `perform_search()`: 전체 함수 try-except 래핑
  - `display_search_results()`: 포괄적 예외 처리 추가
  - SmartLinks 컨텍스트 업데이트 보호

### 개선된 에러 처리
- ✅ 전체 함수 수준 예외 처리
- ✅ 개별 아이템 수준 예외 처리
- ✅ 상세 로그 기록 (`exc_info=True`)
- ✅ 사용자 친화적 에러 메시지
- ✅ 프로그램 안정성 유지

---

## 📥 다운로드

### 실행 파일 (.exe)
- **DeepFileX_v1.4.1.exe** (권장)
  - 설치 불필요, 바로 실행
  - 모든 필수 라이브러리 포함
  - 크기: ~80MB

### 소스 코드
- **Source code (zip)**
- **Source code (tar.gz)**

---

## 🚀 설치 및 실행

### 실행 파일 사용 (권장)
1. `DeepFileX_v1.4.1.exe` 다운로드
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

## 🔄 v1.4.0에서 업그레이드

v1.4.0 사용자는 반드시 v1.4.1로 업그레이드하시기 바랍니다:

**업그레이드 이유**:
- 🔴 v1.4.0: 검색 중 크래시 발생 (치명적 버그)
- 🟢 v1.4.1: 크래시 완전 해결 + 안정성 강화

**업그레이드 방법**:
1. 기존 v1.4.0 종료
2. v1.4.1 다운로드 및 실행
3. 기존 인덱스 파일 그대로 사용 가능

---

## 📋 v1.4.0 대비 변경사항

### 버그 수정만 포함 (Patch Release)
- ✅ 검색 크래시 문제 해결
- ✅ 예외 처리 강화
- ✅ 에러 로깅 개선

### 기능 변경 없음
- ✅ 모든 v1.4.0 기능 그대로 유지
- ✅ GitHub Pages 광고 시스템 정상 작동
- ✅ 인덱스 호환성 100%

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

## 🔄 자동 업데이트

이 버전부터 자동 업데이트 시스템이 실제 GitHub API를 사용합니다:
- 프로그램 시작 시 자동으로 업데이트 확인
- 새 버전 발견 시 알림 표시
- 7일마다 자동 확인

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

v1.4.0 사용자 여러분의 버그 제보 덕분에 빠르게 문제를 해결할 수 있었습니다.

이번 패치는 안정성에 초점을 맞춘 중요한 업데이트입니다. 모든 v1.4.0 사용자는 v1.4.1로 업그레이드하시기 바랍니다.

**Powered by Adsterra** 🚀

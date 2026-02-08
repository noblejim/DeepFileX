# GitHub Pages 광고 시스템 가이드

**DeepFileX v1.4.0+**

이 문서는 DeepFileX의 GitHub Pages 기반 Adsterra 광고 시스템에 대한 완전한 가이드입니다.

---

## 📋 목차

1. [시스템 개요](#시스템-개요)
2. [아키텍처](#아키텍처)
3. [설정 방법](#설정-방법)
4. [광고 코드 관리](#광고-코드-관리)
5. [문제 해결](#문제-해결)
6. [고급 설정](#고급-설정)

---

## 시스템 개요

### 개념

GitHub Pages를 사용하여 광고 HTML을 호스팅하고, DeepFileX 프로그램이 QWebEngineView를 통해 해당 페이지를 로드하여 광고를 표시합니다.

### 장점

✅ **프로그램 재컴파일 불필요**: HTML만 수정하면 광고 변경 가능
✅ **무료 호스팅**: GitHub Pages는 무료
✅ **HTTPS 자동 제공**: 보안 연결 기본 제공
✅ **버전 관리**: Git으로 광고 변경 이력 추적
✅ **실제 광고 이미지**: Adsterra가 제공하는 실제 광고 표시

### 단점

⚠️ **인터넷 연결 필수**: 오프라인에서는 광고 미표시
⚠️ **GitHub Pages 의존**: GitHub 장애 시 광고 미표시
⚠️ **로딩 시간**: 네트워크 속도에 따라 로딩 지연 가능

---

## 아키텍처

### 전체 구조

```
┌─────────────────────────────────────────┐
│  DeepFileX (filemri.py)                │
│  ┌───────────────────────────────────┐ │
│  │ GitHubPagesAdWidget               │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │ QWebEngineView              │ │ │
│  │  │  ┌───────────────────────┐  │ │ │
│  │  │  │ AdWebEnginePage       │  │ │ │
│  │  │  │  - acceptNavigation   │  │ │ │
│  │  │  │  - createWindow       │  │ │ │
│  │  │  └───────────────────────┘  │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
              ↓ HTTPS Request
┌─────────────────────────────────────────┐
│  GitHub Pages                           │
│  https://noblejim.github.io/            │
│         DeepFileX/ads/                  │
│  ┌───────────────────────────────────┐ │
│  │ index.html                        │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │ Adsterra JavaScript         │ │ │
│  │  │ <script src="...invoke.js"> │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
              ↓ Ad Request
┌─────────────────────────────────────────┐
│  Adsterra Ad Server                     │
│  - 광고 이미지 제공                      │
│  - 자동 회전 처리                        │
│  - 클릭 추적                            │
└─────────────────────────────────────────┘
```

### 데이터 흐름

1. **프로그램 시작**
   ```
   filemri.py
     → GitHubPagesAdWidget.__init__()
     → QWebEngineView 생성
     → setUrl("https://noblejim.github.io/DeepFileX/ads/")
   ```

2. **광고 페이지 로드**
   ```
   GitHub Pages → index.html
     → Adsterra JavaScript 실행
     → 광고 서버에서 광고 가져오기
     → DOM에 광고 이미지 삽입
   ```

3. **광고 클릭**
   ```
   사용자 클릭
     → JavaScript 이벤트
     → acceptNavigationRequest() 호출
     → QDesktopServices.openUrl() → 브라우저 열기
     → QTimer(100ms) → 광고 페이지 리로드
   ```

### 클래스 다이어그램

```python
QFrame
  ↑
  └── GitHubPagesAdWidget
        - ad_page_url: str
        - web_view: QWebEngineView
        + __init__(parent, location)
        + init_ui()
        + track_impression()

QWebEnginePage
  ↑
  └── AdWebEnginePage
        - ad_page_url: str
        + acceptNavigationRequest(url, nav_type, is_main_frame) -> bool
        + createWindow(window_type) -> QWebEnginePage
```

---

## 설정 방법

### 초기 설정

#### 1. GitHub Pages 활성화

1. GitHub 저장소 접속: https://github.com/noblejim/DeepFileX
2. **Settings** → **Pages**
3. **Source** 설정:
   - Deploy from a branch
   - Branch: `master`
   - Folder: `/docs`
4. **Save** 클릭

5~10분 후 활성화 확인:
```
https://noblejim.github.io/DeepFileX/ads/
```

#### 2. Adsterra 광고 단위 생성

1. https://publishers.adsterra.com/ 로그인
2. **Create Ad Unit** → **Banner Ad**
3. 설정:
   - Size: 970×90 (Leaderboard)
   - Zone Name: `DeepFileX_Banner`
4. **Get Code** 클릭

#### 3. 광고 코드 삽입

`docs/ads/index.html` 파일 편집:

```html
<div id="adsterra-banner">
    <!-- Adsterra 코드를 여기에 붙여넣기 -->
    <script async="async" data-cfasync="false"
      src="https://pl28674757.effectivegatecpm.com/YOUR_ID/invoke.js">
    </script>
    <div id="container-YOUR_ID"></div>
</div>
```

#### 4. GitHub에 푸시

```bash
cd C:\QuantumLayer\DeepFileX
git add docs/ads/index.html
git commit -m "Add Adsterra banner code"
git push
```

5~10분 후 광고 활성화됨.

---

## 광고 코드 관리

### 광고 변경

광고 코드를 변경하려면:

1. `docs/ads/index.html` 편집
2. 새 Adsterra 코드 붙여넣기
3. Git 커밋 및 푸시
4. 5~10분 대기
5. **프로그램 재시작 필요 없음!**

### 광고 크기 조정

현재 지원 크기: 970×240

크기 변경 시:

**HTML (docs/ads/index.html)**:
```css
.ad-container {
    height: 250px;  /* 전체 컨테이너 높이 */
}

.ad-wrapper {
    height: 240px;  /* 광고 영역 높이 */
}
```

**Python (src/github_pages_ad_widget.py)**:
```python
self.setFixedHeight(260)  # 위젯 높이
self.web_view.setFixedSize(970, 240)  # WebView 크기
```

### 여러 광고 단위

여러 광고를 번갈아 표시하려면:

1. Adsterra에서 여러 광고 단위 생성
2. `index.html`에 JavaScript로 랜덤/순환 표시:

```html
<script>
const ads = [
    'YOUR_AD_ID_1',
    'YOUR_AD_ID_2',
    'YOUR_AD_ID_3'
];
const randomAd = ads[Math.floor(Math.random() * ads.length)];
// 해당 광고 코드 로드
</script>
```

---

## 문제 해결

### 광고가 표시되지 않음

#### 1. GitHub Pages 확인

브라우저에서 직접 접속:
```
https://noblejim.github.io/DeepFileX/ads/
```

- **404 에러**: GitHub Pages 미활성화 → Settings에서 활성화
- **빈 페이지**: Adsterra 코드 누락 → index.html 확인
- **로딩 중**: 정상 (Adsterra 서버에서 광고 가져오는 중)

#### 2. 프로그램 로그 확인

로그 위치:
```
C:\Users\[사용자]\AppData\Roaming\DeepFileX\deepfilex.log
```

정상 로그:
```
✅ GitHub Pages ad banner system loaded (Adsterra hosted)
GitHub Pages ad widget loaded: https://noblejim.github.io/DeepFileX/ads/
Navigation request: https://noblejim.github.io/DeepFileX/ads/, type: NavigationTypeTyped
```

에러 로그:
```
⚠️ GitHub Pages banner not available: DLL load failed
```
→ PyQt6-WebEngine 재설치 필요

#### 3. QWebEngineView DLL 문제

증상:
```
DLL load failed while importing QtWebEngineWidgets
```

해결:
```bash
pip install --upgrade PyQt6==6.10.2 PyQt6-WebEngine==6.10.0
```

#### 4. 인터넷 연결 확인

광고는 인터넷 연결 필수:
```python
# 테스트
import requests
response = requests.get('https://noblejim.github.io/DeepFileX/ads/')
print(response.status_code)  # 200이어야 정상
```

### 광고 클릭이 작동하지 않음

#### 증상
- 광고 클릭 시 아무 반응 없음

#### 원인 및 해결

1. **acceptNavigationRequest 미호출**

   로그 확인:
   ```
   Navigation request: [URL], type: [TYPE]
   ```

   없으면 → `AdWebEnginePage` 미적용

   확인:
   ```python
   custom_page = AdWebEnginePage(self.web_view)
   self.web_view.setPage(custom_page)
   ```

2. **JavaScript 차단**

   설정 확인:
   ```python
   settings.setAttribute(
       QWebEngineSettings.WebAttribute.JavascriptEnabled,
       True
   )
   ```

### 광고 클릭 후 배너 사라짐

#### 증상
- 광고 클릭 후 배너 영역이 비어버림

#### 해결
`acceptNavigationRequest()`에 리로드 로직 확인:

```python
from PyQt6.QtCore import QTimer
QTimer.singleShot(100, lambda: self.setUrl(QUrl(self.ad_page_url)))
```

---

## 고급 설정

### 광고 통계 추적

DeepFileX는 자동으로 광고 통계를 추적합니다:

**위치**:
```
C:\Users\[사용자]\AppData\Roaming\DeepFileX\ads\stats.json
```

**내용**:
```json
{
  "impressions": 100,
  "clicks": 5,
  "last_impression": "2026-02-08T20:00:00",
  "last_click": "2026-02-08T19:55:00",
  "source": "github_pages"
}
```

**CTR 계산**:
```python
ctr = (clicks / impressions) * 100
# 예: (5 / 100) * 100 = 5%
```

### 커스텀 광고 페이지

기본 광고 페이지 대신 다른 URL 사용:

```python
# github_pages_ad_widget.py
self.ad_page_url = "https://your-custom-domain.com/ads/"
```

### 다크 모드 지원

광고 배경을 다크 모드에 맞추려면:

```css
/* docs/ads/index.html */
body {
    background-color: #1e1e1e;  /* 다크 배경 */
}

.ad-wrapper {
    background: #2d2d2d;
    border: 1px solid #444;
}
```

### A/B 테스팅

여러 광고 레이아웃 테스트:

```html
<script>
// 50% 확률로 레이아웃 A 또는 B
const layout = Math.random() < 0.5 ? 'A' : 'B';

if (layout === 'A') {
    // 레이아웃 A 광고 코드
} else {
    // 레이아웃 B 광고 코드
}

// 서버에 레이아웃 기록
fetch('/track?layout=' + layout);
</script>
```

### 광고 프리로딩

광고 로딩 속도 개선:

```html
<!-- 광고 스크립트 프리로드 -->
<link rel="preconnect" href="https://pl28674757.effectivegatecpm.com">
<link rel="dns-prefetch" href="https://pl28674757.effectivegatecpm.com">
```

### 광고 비활성화 (프리미엄 사용자)

```python
# QSettings 사용
settings = QSettings('DeepFileX', 'SmartLinks')
settings.setValue('ads_enabled', False)

# 또는 프리미엄 플래그
settings.setValue('is_premium', True)
```

---

## 베스트 프랙티스

### 1. 광고 로딩 최적화

- ✅ Async 스크립트 사용
- ✅ DNS 프리페칭
- ✅ 이미지 최적화

### 2. 사용자 경험

- ✅ 광고 크기 적절하게 유지
- ✅ 자동 소리 재생 금지
- ✅ 팝업 차단

### 3. 보안

- ✅ HTTPS 사용
- ✅ CSP (Content Security Policy) 설정
- ✅ 신뢰할 수 있는 광고 네트워크만 사용

### 4. 성능

- ✅ 광고 로딩으로 인한 앱 시작 지연 최소화
- ✅ 메모리 사용량 모니터링
- ✅ 광고 캐싱 고려

---

## 참고 자료

### 공식 문서
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [QWebEngineView Documentation](https://doc.qt.io/qt-6/qwebengineview.html)
- [Adsterra Publisher Guide](https://adsterra.com/publishers/)

### 관련 파일
- `src/github_pages_ad_widget.py`
- `docs/ads/index.html`
- `docs/ads/README.md`
- `src/version_config.py`

### 유용한 링크
- Adsterra Dashboard: https://publishers.adsterra.com/
- GitHub Pages: https://noblejim.github.io/DeepFileX/ads/
- GitHub Repository: https://github.com/noblejim/DeepFileX

---

**문서 버전**: 1.0
**마지막 업데이트**: 2026-02-09
**작성자**: QuantumLayer

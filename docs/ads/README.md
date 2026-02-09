# DeepFileX Adsterra Banner 설정 가이드

## 📋 개요

DeepFileX는 GitHub Pages를 통해 Adsterra 배너 광고를 표시합니다.

- **GitHub Pages URL**: https://noblejim.github.io/DeepFileX/ads/
- **광고 크기**: 970×90 (Banner Ad)
- **광고 제공**: Adsterra

## 🚀 설정 방법

### 1단계: GitHub Pages 활성화

1. GitHub 저장소로 이동: https://github.com/noblejim/DeepFileX
2. **Settings** → **Pages** 클릭
3. **Source** 설정:
   - **Deploy from a branch** 선택
   - **Branch**: `master` 선택
   - **Folder**: `/docs` 선택
   - **Save** 클릭

4. 몇 분 후 페이지가 활성화됩니다:
   - URL: `https://noblejim.github.io/DeepFileX/ads/`

### 2단계: Adsterra Banner Ad 코드 받기

1. **Adsterra Dashboard** 로그인: https://publishers.adsterra.com/
2. **Create Ad Unit** 클릭
3. **Banner Ad** 선택
4. 설정:
   - **Size**: 970×90 (Leaderboard)
   - **Zone Name**: DeepFileX_Banner
5. **Get Code** 클릭하여 JavaScript 코드 복사

예시 코드:
```html
<script type="text/javascript">
    atOptions = {
        'key' : 'YOUR_BANNER_KEY_HERE',
        'format' : 'iframe',
        'height' : 90,
        'width' : 970,
        'params' : {}
    };
</script>
<script type="text/javascript" src="//www.topcreativeformat.com/YOUR_CODE_ID/invoke.js"></script>
```

### 3단계: index.html에 코드 삽입

1. `docs/ads/index.html` 파일 열기
2. **73~91번 줄** 사이의 주석 부분을 삭제
3. Adsterra 코드 붙여넣기:

```html
<div id="adsterra-banner">
    <!-- 여기에 Adsterra 코드 붙여넣기 -->
    <script type="text/javascript">
        atOptions = {
            'key' : 'YOUR_BANNER_KEY_HERE',
            'format' : 'iframe',
            'height' : 90,
            'width' : 970,
            'params' : {}
        };
    </script>
    <script type="text/javascript" src="//www.topcreativeformat.com/YOUR_CODE_ID/invoke.js"></script>
</div>
```

4. 파일 저장 후 GitHub에 푸시:
```bash
git add docs/ads/index.html
git commit -m "Add Adsterra banner code"
git push
```

### 4단계: DeepFileX 실행

DeepFileX를 실행하면 자동으로 GitHub Pages의 광고를 로드합니다.

**광고 시스템 우선순위:**
1. ✅ **GitHub Pages Banner** (가장 우선) - 실제 Adsterra 광고 표시
2. 🔄 **Rotating Image Banner** (Fallback 1) - 플레이스홀더 이미지
3. 🔗 **SmartLinks** (Fallback 2) - 그라데이션 배너

## 📊 광고 통계 확인

광고 노출/클릭 통계는 다음 위치에 저장됩니다:
```
C:\Users\[사용자명]\AppData\Roaming\DeepFileX\ads\stats.json
```

통계 내용:
```json
{
  "impressions": 100,
  "clicks": 5,
  "last_impression": "2026-02-08T20:00:00",
  "last_click": "2026-02-08T19:55:00",
  "source": "github_pages"
}
```

## 🔧 문제 해결

### 광고가 표시되지 않는 경우:

1. **GitHub Pages 활성화 확인**:
   - https://noblejim.github.io/DeepFileX/ads/ 접속하여 페이지가 보이는지 확인

2. **Adsterra 코드 확인**:
   - `docs/ads/index.html` 파일에 올바른 코드가 있는지 확인
   - 브라우저 개발자 도구(F12)로 JavaScript 오류 확인

3. **프로그램 로그 확인**:
   ```
   C:\Users\[사용자명]\AppData\Roaming\DeepFileX\deepfilex.log
   ```
   - "GitHub Pages ad banner system loaded" 메시지 확인

4. **QWebEngineView 문제**:
   - PyQt6-WebEngine이 설치되어 있는지 확인:
   ```bash
   pip install PyQt6-WebEngine
   ```

### Fallback 순서:

만약 GitHub Pages 배너가 로드되지 않으면, 자동으로 다음 순서로 시도합니다:

1. **GitHub Pages Banner** (index.html) ❌ 실패
   ↓
2. **Rotating Image Banner** (rotating_image_banner.py) ❌ 실패
   ↓
3. **SmartLinks Gradient Banner** (filemri_smartlinks.py) ✅ 항상 작동

## 📝 파일 구조

```
DeepFileX/
├── docs/
│   └── ads/
│       ├── index.html         ← Adsterra 배너 코드 여기에 추가
│       └── README.md          ← 이 문서
└── src/
    ├── github_pages_ad_widget.py    ← GitHub Pages 로더
    ├── rotating_image_banner.py     ← Fallback 1
    └── filemri_smartlinks.py        ← Fallback 2
```

## ✅ 완료 체크리스트

- [ ] GitHub Pages 활성화 (Settings → Pages)
- [ ] Adsterra Dashboard에서 Banner Ad 생성
- [ ] `docs/ads/index.html`에 Adsterra 코드 추가
- [ ] GitHub에 푸시 (`git push`)
- [ ] DeepFileX 실행하여 광고 확인
- [ ] 광고 클릭이 Adsterra로 추적되는지 확인

## 🔗 참고 링크

- **Adsterra Dashboard**: https://publishers.adsterra.com/
- **GitHub Repository**: https://github.com/noblejim/DeepFileX
- **GitHub Pages URL**: https://noblejim.github.io/DeepFileX/ads/
- **Adsterra Banner Sizes**: https://adsterra.com/ad-formats/banner/

## 💡 팁

1. **광고 업데이트**: `docs/ads/index.html` 파일만 수정하면 프로그램 재컴파일 없이 광고 변경 가능
2. **테스트**: 브라우저에서 `https://noblejim.github.io/DeepFileX/ads/` 직접 접속하여 광고 확인
3. **수익 추적**: Adsterra Dashboard에서 실시간 수익 확인 가능

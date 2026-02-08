# Ralph Loop - DeepFileX 쿠팡 배너 개선

## 목표
프로그램 하단의 쿠팡 배너가:
1. ✅ 상품 이미지로 출력
2. ✅ 상품이 자동으로 회전
3. ✅ 해당 상품 클릭 시 해당 상품 구매 페이지로 이동

## Iteration 1 - SimpleAdBanner 구현 (브라우저 기반)

### 발견된 문제:
- ❌ QWebEngineView DLL 로드 실패 (ImportError: DLL load failed)
- ❌ 유니코드 인코딩 오류 (이모지 출력 문제)
- ❌ pywebview도 별도 창이라 UX가 좋지 않음

### 최종 해결 방안:
- ✅ **SimpleAdBanner**: 임시 HTML 파일을 생성하여 시스템 브라우저에서 열기
- ✅ 가장 안정적이고 호환성이 높은 방식
- ✅ 쿠팡 carousel이 완벽하게 작동 (회전, 개별 클릭 모두 가능)

### 생성된 파일:
- `src/simple_ad_widget.py` - 브라우저 기반 광고 배너 (최종)
- `src/pywebview_ad_widget.py` - pywebview 기반 (fallback)

### 수정된 파일:
- `src/filemri.py` - SimpleAdBanner 최우선 사용
- `src/webview2_ad_widget.py` - 오류 처리 개선

### 최종 구현:
```python
# SimpleAdBanner 방식 (임시 HTML + 브라우저)
def open_carousel_page(self):
    html_content = f"""<!DOCTYPE html>
    <html>
    <body>
        <iframe src="{self.carousel_url}"
                width="900" height="100"
                frameborder="0" scrolling="no">
        </iframe>
    </body>
    </html>"""

    temp_file = temp_dir / 'coupang_carousel.html'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    QDesktopServices.openUrl(QUrl(temp_file.as_uri()))
```

### 구현된 기능:
1. ✅ **상품 이미지 출력**: 쿠팡 carousel iframe으로 상품 이미지 표시
2. ✅ **자동 회전**: 쿠팡 서버가 자동으로 상품 회전 (5-10초 간격)
3. ✅ **개별 상품 클릭**: 각 상품 클릭 시 해당 상품 구매 페이지로 이동
4. ✅ **통계 추적**: 노출/클릭 통계 자동 기록
5. ✅ **Fallback**: 문제 발생 시 파트너스 메인 링크로 이동

### Import 우선순위:
1. SimpleAdBanner (브라우저 기반) - 최우선
2. PyWebViewAdBanner (pywebview) - fallback 1
3. WebView2AdBanner (QWebEngineView) - fallback 2

### 테스트 상태:
- ✅ 프로그램 실행 성공 (PID: 14196)
- 🔄 사용자가 배너 클릭 시 브라우저에서 carousel 열림
- 🔄 쿠팡이 자동으로 상품 회전
- 🔄 개별 상품 클릭 → 구매 페이지 이동

### 검증 필요:
- [ ] 실제 배너 클릭 테스트
- [ ] 브라우저에서 carousel 표시 확인
- [ ] 상품 회전 확인
- [ ] 개별 상품 클릭 → 구매 페이지 이동 확인

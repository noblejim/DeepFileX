#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX SmartLinks Web Banner
Adsterra 광고를 QWebEngineView로 표시하는 모듈

Created: 2026-02-06
Author: QuantumLayer
License: MIT
Version: 2.0.0
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, pyqtSignal, QSettings
from datetime import datetime
import json
from pathlib import Path


class AdWebPage(QWebEnginePage):
    """광고 전용 웹 페이지 (새 창 열기 방지)"""

    link_clicked = pyqtSignal(str)

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        """링크 클릭 시 새 창 대신 시그널 발송"""
        if nav_type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            self.link_clicked.emit(url.toString())
            return False  # 현재 페이지에서는 이동하지 않음
        return True


class SmartLinksWebBanner(QFrame):
    """
    Adsterra SmartLinks를 QWebEngineView로 표시하는 웹 배너 위젯
    """

    ad_clicked = pyqtSignal(str)  # 광고 클릭 시그널

    def __init__(self, parent=None, location="bottom_banner"):
        super().__init__(parent)
        self.location = location
        self.settings = QSettings('DeepFileX', 'SmartLinks')

        # Adsterra SmartLinks 설정
        self.config = {
            'smartlink_id': '27417447',
            'base_url': 'https://www.profitableratecpm.com/nndiuxsyi',
            'key': '7f25d09e5bc7b1e1c3cb37e467e6821d'
        }

        # 광고가 비활성화되어 있으면 숨기기
        if not self.is_ads_enabled() or self.is_premium_user():
            self.hide()
            return

        self.init_ui()
        self.track_impression()

    def is_ads_enabled(self):
        """광고 활성화 여부"""
        return self.settings.value('ads_enabled', True, type=bool)

    def is_premium_user(self):
        """프리미엄 사용자 여부"""
        return self.settings.value('is_premium', False, type=bool)

    def init_ui(self):
        """UI 초기화"""
        self.setFixedHeight(120)
        self.setStyleSheet("""
            SmartLinksWebBanner {
                background-color: transparent;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # QWebEngineView 생성
        self.web_view = QWebEngineView()
        self.web_view.setFixedHeight(100)

        # 커스텀 페이지 설정 (새 창 열기 방지)
        self.web_page = AdWebPage(self.web_view)
        self.web_page.link_clicked.connect(self.on_link_clicked)
        self.web_view.setPage(self.web_page)

        # 웹 엔진 설정
        web_settings = self.web_view.settings()
        web_settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        web_settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        web_settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)

        layout.addWidget(self.web_view)

        # HTML 배너 로드
        self.load_banner_html()

    def load_banner_html(self):
        """HTML 배너 생성 및 로드"""

        # SmartLinks URL 생성
        smartlink_url = self.generate_smartlink_url()

        # HTML 배너 코드
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }}

        .banner-container {{
            width: 100%;
            height: 100px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            border-radius: 12px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .banner-container:hover {{
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }}

        .banner-content {{
            position: relative;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: 20px;
            text-align: center;
        }}

        .banner-text {{
            color: white;
        }}

        .banner-text h2 {{
            font-size: 20px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 8px;
        }}

        .banner-text p {{
            font-size: 13px;
            opacity: 0.95;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}

        .ad-label {{
            position: absolute;
            bottom: 8px;
            right: 10px;
            background-color: rgba(0,0,0,0.3);
            color: rgba(255,255,255,0.8);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 10px;
            z-index: 3;
        }}

        /* 반짝이는 애니메이션 효과 */
        @keyframes shimmer {{
            0% {{ background-position: -1000px 0; }}
            100% {{ background-position: 1000px 0; }}
        }}

        .banner-container::before {{
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            animation: shimmer 3s infinite;
        }}
    </style>
</head>
<body>
    <div class="banner-container" onclick="openAd()">
        <div class="banner-content">
            <div class="banner-text">
                <h2>🚀 Discover Premium Tools & Software</h2>
                <p>Click to explore professional recommendations curated for you</p>
            </div>
        </div>
        <div class="ad-label">Ad</div>
    </div>

    <script>
        function openAd() {{
            // 클릭 추적
            console.log('Ad clicked - Opening SmartLink');

            // SmartLinks URL로 이동
            window.location.href = '{smartlink_url}';
        }}
    </script>
</body>
</html>
"""

        # HTML 로드
        self.web_view.setHtml(html_content, QUrl("about:blank"))

    def generate_smartlink_url(self):
        """SmartLink URL 생성"""
        from datetime import datetime

        params = {
            'key': self.config['key'],
            'source': 'deepfilex_app',
            'context': 'web_banner',
            'location': self.location,
            'smartlink_id': self.config['smartlink_id'],
            'timestamp': int(datetime.now().timestamp()),
            'version': '2.0.0'
        }

        param_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        full_url = f"{self.config['base_url']}?{param_string}"

        return full_url

    def on_link_clicked(self, url):
        """링크 클릭 시 처리"""
        import webbrowser

        # 클릭 추적
        self.track_click()

        # 외부 브라우저로 열기
        webbrowser.open(url)

        # 시그널 발송
        self.ad_clicked.emit(url)

        print(f"💰 광고 클릭: {url[:80]}...")

    def track_impression(self):
        """노출 추적"""
        stats_file = Path.home() / 'AppData' / 'Roaming' / 'DeepFileX' / 'ads' / 'stats.json'
        stats_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            else:
                stats = {'impressions': 0, 'clicks': 0}

            stats['impressions'] += 1
            stats['last_impression'] = datetime.now().isoformat()

            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2)

        except Exception as e:
            print(f"노출 추적 오류: {e}")

    def track_click(self):
        """클릭 추적"""
        stats_file = Path.home() / 'AppData' / 'Roaming' / 'DeepFileX' / 'ads' / 'stats.json'

        try:
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            else:
                stats = {'impressions': 0, 'clicks': 0}

            stats['clicks'] += 1
            stats['last_click'] = datetime.now().isoformat()

            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2)

            # 클릭율 계산
            if stats['impressions'] > 0:
                ctr = (stats['clicks'] / stats['impressions']) * 100
                print(f"📊 광고 통계: {stats['clicks']}클릭 / {stats['impressions']}노출 = {ctr:.1f}% CTR")

        except Exception as e:
            print(f"클릭 추적 오류: {e}")


# 테스트 코드
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("DeepFileX SmartLinks Web Banner Test")
    window.setGeometry(100, 100, 800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # Web 배너 추가
    web_banner = SmartLinksWebBanner(location="test_banner")

    def on_ad_clicked(url):
        print(f"✅ 광고 클릭 이벤트: {url[:50]}...")

    web_banner.ad_clicked.connect(on_ad_clicked)

    layout.addStretch()
    layout.addWidget(web_banner)

    window.show()

    print("🎯 SmartLinks Web Banner 테스트 시작")
    print("📊 배너 클릭 시 브라우저가 열리고 통계가 기록됩니다")

    sys.exit(app.exec())

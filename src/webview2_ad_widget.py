#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX WebView2 광고 배너 위젯
PyQt6 + WebView2를 사용한 실시간 광고 시스템

Created: 2026-02-06
Author: QuantumLayer
License: MIT
Version: 3.0.0
"""

import os
import sys
import threading
import webbrowser
from pathlib import Path
from bottle import Bottle, static_file, ServerAdapter
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QWidget)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QTimer, QUrl, QByteArray
from PyQt6.QtGui import QFont, QCursor, QDesktopServices, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

# QWebEngineView import (iframe 표시용)
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError as e:
    WEBENGINE_AVAILABLE = False
    # logger는 아직 정의 안 됨, 나중에 로그로 출력

import logging

logger = logging.getLogger(__name__)


class QuietWSGIRefServer(ServerAdapter):
    """조용한 WSGI 서버 (로그 최소화)"""
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler

        class QuietHandler(WSGIRequestHandler):
            def log_message(self, format, *args):
                pass  # 로그 출력 안 함

        self.srv = make_server(self.host, self.port, handler, handler_class=QuietHandler)
        self.srv.serve_forever()


class LocalAdServer:
    """로컬 광고 서버 (HTML 파일 서빙)"""

    def __init__(self, port=8765):
        self.port = port
        self.app = Bottle()
        self.server_thread = None
        self.is_running = False

        # 라우트 설정
        @self.app.route('/')
        @self.app.route('/ad')
        def serve_ad():
            # 프로젝트 루트 디렉토리 찾기
            project_root = Path(__file__).parent.parent

            # 쿠팡파트너스 JavaScript 배너 (우선)
            coupang_file = project_root / 'assets' / 'ads' / 'coupang_iframe.html'
            if coupang_file.exists():
                return static_file('coupang_iframe.html', root=coupang_file.parent)

            return "<h1>Ad file not found</h1>"

    def start(self):
        """서버 시작 (백그라운드 스레드)"""
        if not self.is_running:
            self.server_thread = threading.Thread(
                target=lambda: self.app.run(
                    host='127.0.0.1',
                    port=self.port,
                    quiet=True,
                    server=QuietWSGIRefServer
                ),
                daemon=True
            )
            self.server_thread.start()
            self.is_running = True
            logger.info(f"✅ 로컬 광고 서버 시작: http://127.0.0.1:{self.port}")

    def stop(self):
        """서버 중지"""
        self.is_running = False
        logger.info("로컬 광고 서버 중지")

    def get_url(self):
        """광고 URL 반환"""
        return f"http://127.0.0.1:{self.port}/ad"


# 전역 서버 인스턴스
_ad_server = None


def get_ad_server():
    """전역 광고 서버 가져오기 (싱글톤)"""
    global _ad_server
    if _ad_server is None:
        _ad_server = LocalAdServer()
        _ad_server.start()
    return _ad_server


class WebView2AdBanner(QFrame):
    """
    WebView2 기반 광고 배너 위젯
    로컬 웹서버를 통해 Adsterra 광고 표시
    """

    ad_clicked = pyqtSignal(str)  # 광고 클릭 시그널

    def __init__(self, parent=None, location="bottom_banner"):
        super().__init__(parent)
        self.location = location
        self.settings = QSettings('DeepFileX', 'SmartLinks')
        self.ad_server = get_ad_server()

        # 쿠팡 파트너스 iframe 정보
        self.iframe_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        iframe {
            border: none;
        }
    </style>
</head>
<body>
    <iframe src="https://ads-partners.coupang.com/widgets.html?id=963651&template=carousel&trackingCode=AF1662515&subId=&width=900&height=100&tsource="
            width="900"
            height="100"
            frameborder="0"
            scrolling="no"
            referrerpolicy="unsafe-url"
            browsingtopics>
    </iframe>
</body>
</html>
        '''

        # 광고 비활성화 확인
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
        """UI 초기화 - 쿠팡 광고 보기 버튼"""
        self.setFixedHeight(70)
        self.setStyleSheet("""
            WebView2AdBanner {
                background-color: transparent;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        if WEBENGINE_AVAILABLE:
            # QWebEngineView로 iframe 표시
            self.web_view = QWebEngineView()
            self.web_view.setFixedHeight(105)
            self.web_view.setHtml(self.iframe_html)
            self.web_view.setStyleSheet("background: transparent;")
            layout.addWidget(self.web_view)
            logger.info("✅ QWebEngineView로 쿠팡 iframe 배너 로드")
        else:
            # Fallback: 광고 보기 버튼
            ad_button = QPushButton("🛒 쿠팡 특가 광고 보기")
            ad_button.setFixedHeight(55)
            ad_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            ad_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 #667eea, stop: 1 #764ba2);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 #5568d3, stop: 1 #6a3f8f);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 #4556c2, stop: 1 #5a357e);
                }
            """)

            # 부제목
            subtitle = QLabel("💝 광고 클릭으로 DeepFileX 무료 서비스를 지원해주세요!")
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 11px;
                    background: transparent;
                    padding: 2px;
                }
            """)

            ad_button.clicked.connect(self.open_ad_page)

            layout.addWidget(ad_button)
            layout.addWidget(subtitle)

            logger.info("✅ 쿠팡 광고 버튼 표시 (Fallback 모드)")

    def open_ad_page(self):
        """광고 페이지 열기 - 로컬 서버를 통해 JavaScript 배너 서빙"""
        try:
            # 로컬 서버 URL (JavaScript 실행 가능)
            ad_url = f"http://localhost:{self.ad_server.port}/ad"

            # 시스템 브라우저로 열기
            success = QDesktopServices.openUrl(QUrl(ad_url))

            if success:
                # 클릭 추적
                self.track_click()
                logger.info(f"💰 쿠팡 파트너스 광고 페이지 열기 (localhost): {ad_url}")
            else:
                logger.warning(f"광고 페이지 열기 실패: {ad_url}")

        except Exception as e:
            logger.error(f"광고 페이지 열기 오류: {e}")

    def track_impression(self):
        """노출 추적"""
        try:
            stats_file = Path.home() / 'AppData' / 'Roaming' / 'DeepFileX' / 'ads' / 'stats.json'
            stats_file.parent.mkdir(parents=True, exist_ok=True)

            import json
            from datetime import datetime

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
            logger.error(f"노출 추적 오류: {e}")

    def track_click(self):
        """클릭 추적"""
        try:
            stats_file = Path.home() / 'AppData' / 'Roaming' / 'DeepFileX' / 'ads' / 'stats.json'

            import json
            from datetime import datetime

            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
            else:
                stats = {'impressions': 0, 'clicks': 0}

            stats['clicks'] += 1
            stats['last_click'] = datetime.now().isoformat()

            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2)

            # CTR 계산
            if stats['impressions'] > 0:
                ctr = (stats['clicks'] / stats['impressions']) * 100
                logger.info(f"📊 광고 통계: {stats['clicks']}클릭 / {stats['impressions']}노출 = {ctr:.1f}% CTR")

        except Exception as e:
            logger.error(f"클릭 추적 오류: {e}")


# 테스트 코드
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys

    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("DeepFileX WebView2 Ad Banner Test")
    window.setGeometry(100, 100, 800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # WebView2 배너 추가
    ad_banner = WebView2AdBanner(location="test_banner")

    def on_ad_clicked(url):
        print(f"✅ 광고 클릭됨: {url}")

    ad_banner.ad_clicked.connect(on_ad_clicked)

    layout.addStretch()
    layout.addWidget(ad_banner)

    window.show()

    print("🎯 WebView2 광고 배너 테스트 시작")
    print("📊 배너를 클릭하면 브라우저가 열리고 Adsterra 광고가 표시됩니다")

    sys.exit(app.exec())

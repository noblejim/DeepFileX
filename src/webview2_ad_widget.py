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
import tempfile
from pathlib import Path
from bottle import Bottle, static_file, ServerAdapter
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QWidget)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QTimer, QUrl, QByteArray
from PyQt6.QtGui import QFont, QCursor, QDesktopServices, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from playwright.sync_api import sync_playwright

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

        # 쿠팡 파트너스 정보 (carousel 위젯 900x100)
        self.partner_link = "https://link.coupang.com/a/dHXhN0"
        self.carousel_url = "https://ads-partners.coupang.com/widgets.html?id=963651&template=carousel&trackingCode=AF1662515&subId=&width=900&height=100&tsource="
        self.screenshot_path = None

        # 광고 비활성화 확인
        if not self.is_ads_enabled() or self.is_premium_user():
            self.hide()
            return

        self.init_ui()
        self.load_carousel_screenshot()
        self.track_impression()

    def is_ads_enabled(self):
        """광고 활성화 여부"""
        return self.settings.value('ads_enabled', True, type=bool)

    def is_premium_user(self):
        """프리미엄 사용자 여부"""
        return self.settings.value('is_premium', False, type=bool)

    def init_ui(self):
        """UI 초기화 - 쿠팡 배너 이미지 표시 (900x100)"""
        # 배너 크기: 900x100 + 여백
        self.setFixedHeight(110)
        self.setStyleSheet("""
            WebView2AdBanner {
                background-color: #f5f5f5;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 배너 이미지 레이블 (900x100 크기에 맞춤)
        self.banner_label = QLabel("🛒 쿠팡 배너 로딩 중...")
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #ddd;
                color: #666;
            }
        """)
        # 배너 크기 고정: 900x100
        self.banner_label.setFixedSize(900, 100)
        self.banner_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # 클릭 이벤트
        self.banner_label.mousePressEvent = lambda e: self.open_ad()

        layout.addWidget(self.banner_label)

        logger.info("✅ 쿠팡 carousel 상품이미지 표시 (900x100)")

    def load_carousel_screenshot(self):
        """Playwright로 carousel 스크린샷 캡처"""
        def capture_in_thread():
            try:
                logger.info(f"📸 Carousel 스크린샷 캡처 시작: {self.carousel_url}")

                with sync_playwright() as p:
                    # Chromium 브라우저 시작 (headless)
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page(viewport={'width': 900, 'height': 100})

                    # Carousel URL 로드
                    page.goto(self.carousel_url, wait_until='networkidle', timeout=10000)

                    # 광고가 로드될 시간 대기
                    page.wait_for_timeout(2000)

                    # 스크린샷 저장
                    temp_dir = Path(tempfile.gettempdir()) / 'deepfilex_ads'
                    temp_dir.mkdir(exist_ok=True)
                    screenshot_file = temp_dir / 'coupang_carousel.png'

                    page.screenshot(path=str(screenshot_file))
                    browser.close()

                    self.screenshot_path = str(screenshot_file)

                    # UI 스레드에서 이미지 로드
                    QTimer.singleShot(0, self.display_screenshot)

                    logger.info(f"✅ Carousel 스크린샷 저장: {screenshot_file}")

            except Exception as e:
                logger.error(f"❌ Carousel 스크린샷 캡처 실패: {e}")
                QTimer.singleShot(0, lambda: self.banner_label.setText("❌ 광고 로드 실패"))

        # 백그라운드 스레드에서 스크린샷 캡처
        thread = threading.Thread(target=capture_in_thread, daemon=True)
        thread.start()

    def display_screenshot(self):
        """캡처한 스크린샷 표시"""
        try:
            if self.screenshot_path and Path(self.screenshot_path).exists():
                pixmap = QPixmap(self.screenshot_path)

                if not pixmap.isNull():
                    # 900x100 크기에 맞게 스케일
                    scaled_pixmap = pixmap.scaled(
                        900, 100,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.banner_label.setPixmap(scaled_pixmap)
                    self.banner_label.setText("")
                    logger.info("✅ Carousel 상품이미지 표시 완료 (900x100)")
                else:
                    logger.error("스크린샷 로드 실패")
                    self.banner_label.setText("❌ 광고 이미지 오류")
            else:
                logger.error(f"스크린샷 파일 없음: {self.screenshot_path}")
                self.banner_label.setText("❌ 광고 파일 없음")

        except Exception as e:
            logger.error(f"스크린샷 표시 오류: {e}")
            self.banner_label.setText("❌ 광고 오류")

    def open_ad(self):
        """배너 클릭 - 쿠팡 파트너스 링크로 이동"""
        QTimer.singleShot(100, self._do_open_ad)

    def _do_open_ad(self):
        """실제 광고 열기 (지연 실행)"""
        try:
            success = QDesktopServices.openUrl(QUrl(self.partner_link))

            if success:
                self.track_click()
                logger.info(f"💰 쿠팡 파트너스 클릭: {self.partner_link}")
            else:
                logger.warning(f"파트너스 링크 열기 실패: {self.partner_link}")

        except Exception as e:
            logger.error(f"광고 열기 오류: {e}")

    def open_ad_page(self):
        """광고 페이지 열기 - 쿠팡 위젯 URL 직접 열기"""
        try:
            # 쿠팡 위젯 URL 직접 열기
            widget_url = "https://ads-partners.coupang.com/widgets.html?id=963651&template=carousel&trackingCode=AF1662515&subId=&width=900&height=100&tsource="

            # 시스템 브라우저로 열기
            success = QDesktopServices.openUrl(QUrl(widget_url))

            if success:
                # 클릭 추적
                self.track_click()
                logger.info(f"💰 쿠팡 위젯 직접 열기: {widget_url}")
            else:
                logger.warning(f"위젯 URL 열기 실패: {widget_url}")

        except Exception as e:
            logger.error(f"광고 열기 오류: {e}")

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

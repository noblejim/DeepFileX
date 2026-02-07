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
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QTimer, QUrl
from PyQt6.QtGui import QFont, QCursor, QDesktopServices
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
            # 쿠팡파트너스 배너 우선 사용
            coupang_file = Path(__file__).parent / 'coupang_partners_banner.html'
            if coupang_file.exists():
                return static_file('coupang_partners_banner.html', root=coupang_file.parent)

            # 백업: Adsterra 배너
            adsterra_file = Path(__file__).parent / 'adsterra_banner.html'
            if adsterra_file.exists():
                return static_file('adsterra_banner.html', root=adsterra_file.parent)

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
        """UI 초기화"""
        self.setFixedHeight(110)
        self.setStyleSheet("""
            WebView2AdBanner {
                background-color: #f5f5f5;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 광고 영역
        ad_area = QFrame()
        ad_area.setFixedHeight(95)
        ad_area.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #FA2828, stop: 0.5 #FF6B2C, stop: 1 #FFD93D);
                border-radius: 10px;
                border: none;
            }
            QFrame:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #E81515, stop: 0.5 #FF5219, stop: 1 #FFC700);
            }
        """)
        ad_area.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # 광고 영역 레이아웃
        ad_layout = QVBoxLayout(ad_area)
        ad_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 메인 텍스트
        title_label = QLabel("🛒 쿠팡에서 IT 제품 특가!")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 서브 텍스트
        subtitle_label = QLabel("지금 바로 확인하고 최저가로 구매하세요")
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 파트너스 활동 라벨
        ad_label = QLabel("파트너스")
        ad_label.setFont(QFont("Arial", 8))
        ad_label.setStyleSheet("""
            color: rgba(255,255,255,0.8);
            background-color: rgba(0,0,0,0.3);
            padding: 2px 6px;
            border-radius: 3px;
        """)
        ad_label.setFixedSize(50, 16)
        ad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ad_layout.addWidget(title_label)
        ad_layout.addWidget(subtitle_label)

        # Ad 라벨을 우측 하단에 배치
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(ad_label)
        ad_layout.addLayout(bottom_layout)

        layout.addWidget(ad_area)

        # 클릭 이벤트
        ad_area.mousePressEvent = lambda e: self.open_ad()

    def open_ad(self):
        """광고 열기 - 로컬 서버의 HTML 페이지"""
        ad_url = self.ad_server.get_url()

        try:
            # 기본 브라우저로 열기
            webbrowser.open(ad_url)

            # 클릭 추적
            self.track_click()

            # 시그널 발송
            self.ad_clicked.emit(ad_url)

            logger.info(f"💰 광고 클릭: {ad_url}")

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

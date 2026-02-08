#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX pywebview 광고 배너 위젯
pywebview를 사용한 쿠팡 파트너스 배너 (QWebEngineView 대체)

Created: 2026-02-08
Author: QuantumLayer
License: MIT
Version: 1.0.0
"""

import os
import sys
import threading
import webview
from pathlib import Path
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QTimer
from PyQt6.QtGui import QCursor, QDesktopServices
from PyQt6.QtCore import QUrl
import logging

logger = logging.getLogger(__name__)


class PyWebViewAdBanner(QFrame):
    """
    pywebview 기반 광고 배너 위젯
    쿠팡 파트너스 carousel iframe 표시
    """

    ad_clicked = pyqtSignal(str)

    def __init__(self, parent=None, location="bottom_banner"):
        super().__init__(parent)
        self.location = location
        self.settings = QSettings('DeepFileX', 'SmartLinks')

        # 쿠팡 파트너스 정보
        self.partner_link = "https://link.coupang.com/a/dHXhN0"
        self.carousel_url = "https://ads-partners.coupang.com/widgets.html?id=963651&template=carousel&trackingCode=AF1662515&subId=&width=900&height=100&tsource="

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
        """UI 초기화 - 쿠팡 carousel iframe 표시"""
        self.setFixedHeight(110)
        self.setStyleSheet("""
            PyWebViewAdBanner {
                background-color: #f5f5f5;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # pywebview를 별도 창으로 열기 버튼
        self.banner_label = QLabel("Coupang Partners Carousel\n(Click to view products)")
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #FA2828, stop: 0.5 #FF6B2C, stop: 1 #FFD93D);
                border-radius: 6px;
                border: 1px solid #ddd;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        self.banner_label.setFixedSize(900, 100)
        self.banner_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.banner_label.mousePressEvent = lambda e: self.open_carousel_window()

        layout.addWidget(self.banner_label)
        logger.info("PyWebView banner initialized (click to open carousel)")

    def open_carousel_window(self):
        """pywebview로 쿠팡 carousel 창 열기"""
        try:
            def start_webview():
                # 쿠팡 iframe HTML 생성
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{
                            margin: 0;
                            padding: 10px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                            background: #f5f5f5;
                        }}
                    </style>
                </head>
                <body>
                    <iframe src="{self.carousel_url}"
                            width="900"
                            height="100"
                            frameborder="0"
                            scrolling="no"
                            referrerpolicy="unsafe-url"
                            allow="autoplay">
                    </iframe>
                </body>
                </html>
                """

                # pywebview 창 생성
                webview.create_window(
                    'Coupang Partners - DeepFileX',
                    html=html_content,
                    width=920,
                    height=150,
                    resizable=False
                )
                webview.start()

            # 별도 스레드에서 webview 시작
            thread = threading.Thread(target=start_webview, daemon=True)
            thread.start()

            self.track_click()
            logger.info("Coupang carousel window opened via pywebview")

        except Exception as e:
            logger.error(f"Error opening carousel window: {e}")
            # Fallback: 외부 브라우저로 열기
            self.open_in_browser()

    def open_in_browser(self):
        """Fallback: 외부 브라우저에서 열기"""
        try:
            success = QDesktopServices.openUrl(QUrl(self.partner_link))
            if success:
                self.track_click()
                logger.info("Opened partner link in external browser (fallback)")
        except Exception as e:
            logger.error(f"Error opening in browser: {e}")

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
            logger.error(f"Error tracking impression: {e}")

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
                logger.info(f"Ad stats: {stats['clicks']} clicks / {stats['impressions']} impressions = {ctr:.1f}% CTR")

        except Exception as e:
            logger.error(f"Error tracking click: {e}")


# 테스트 코드
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("DeepFileX PyWebView Ad Banner Test")
    window.setGeometry(100, 100, 800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    ad_banner = PyWebViewAdBanner(location="test_banner")

    layout.addStretch()
    layout.addWidget(ad_banner)

    window.show()

    print("PyWebView Ad Banner Test Started")
    print("Click the banner to open Coupang carousel in separate window")

    sys.exit(app.exec())

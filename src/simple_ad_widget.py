#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX 간단한 광고 배너 위젯
시스템 브라우저를 사용한 쿠팡 파트너스 배너

Created: 2026-02-08
Author: QuantumLayer
License: MIT
Version: 1.0.0
"""

import os
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QUrl
from PyQt6.QtGui import QCursor, QDesktopServices
import logging

logger = logging.getLogger(__name__)


class SimpleAdBanner(QFrame):
    """
    간단한 광고 배너 위젯
    클릭 시 시스템 브라우저에서 쿠팡 carousel 표시
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
        """UI 초기화"""
        self.setFixedHeight(110)
        self.setStyleSheet("""
            SimpleAdBanner {
                background-color: #f5f5f5;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 쿠팡 배너 레이블
        self.banner_label = QLabel("Coupang Partners\n[Click to view rotating product carousel]")
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #FA2828, stop: 0.5 #FF6B2C, stop: 1 #FFD93D);
                border-radius: 6px;
                border: 1px solid #ddd;
                color: white;
                font-size: 18px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
        """)
        self.banner_label.setFixedSize(900, 100)
        self.banner_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.banner_label.mousePressEvent = lambda e: self.open_carousel_page()

        layout.addWidget(self.banner_label)
        logger.info("Coupang ad banner initialized (click to open)")

    def open_carousel_page(self):
        """임시 HTML 파일 생성 후 브라우저에서 열기"""
        try:
            # 임시 HTML 파일 생성
            html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coupang Partners - DeepFileX</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 960px;
            width: 100%;
        }}
        h1 {{
            color: #FA2828;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .carousel-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 120px;
            background: #f8f9fa;
            border-radius: 8px;
            padding: 10px;
        }}
        .info {{
            margin-top: 20px;
            padding: 15px;
            background: #fff8e1;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
            font-size: 13px;
            color: #666;
        }}
        .info strong {{
            color: #333;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Coupang Partners Carousel</h1>
        <p class="subtitle">Powered by DeepFileX</p>

        <div class="carousel-wrapper">
            <iframe src="{self.carousel_url}"
                    width="900"
                    height="100"
                    frameborder="0"
                    scrolling="no"
                    referrerpolicy="unsafe-url"
                    browsingtopics
                    allow="autoplay"
                    style="border: none;">
            </iframe>
        </div>

        <div class="info">
            <strong>About this carousel:</strong><br>
            - Products rotate automatically every few seconds<br>
            - Click on any product to view details and purchase<br>
            - All purchases support DeepFileX development
        </div>

        <div class="footer">
            This is a Coupang Partners affiliate advertisement.<br>
            A commission may be earned from qualifying purchases.
        </div>
    </div>

    <script>
        console.log('Coupang Partners carousel loaded via DeepFileX');

        // 창 크기 자동 조정 (선택사항)
        window.addEventListener('load', function() {{
            console.log('Page fully loaded');
        }});
    </script>
</body>
</html>"""

            # 임시 파일 저장
            temp_dir = Path(tempfile.gettempdir()) / 'deepfilex_ads'
            temp_dir.mkdir(exist_ok=True)
            temp_file = temp_dir / 'coupang_carousel.html'

            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # 브라우저에서 열기
            file_url = temp_file.as_uri()
            success = QDesktopServices.openUrl(QUrl(file_url))

            if success:
                self.track_click()
                logger.info(f"Coupang carousel opened in browser: {temp_file}")
            else:
                logger.warning(f"Failed to open carousel: {temp_file}")

        except Exception as e:
            logger.error(f"Error opening carousel: {e}")
            # Fallback: 파트너스 링크로 이동
            self.open_partner_link()

    def open_partner_link(self):
        """Fallback: 파트너스 메인 링크로 이동"""
        try:
            success = QDesktopServices.openUrl(QUrl(self.partner_link))
            if success:
                self.track_click()
                logger.info("Opened Coupang partner link (fallback)")
        except Exception as e:
            logger.error(f"Error opening partner link: {e}")

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
    window.setWindowTitle("DeepFileX Simple Ad Banner Test")
    window.setGeometry(100, 100, 800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    ad_banner = SimpleAdBanner(location="test_banner")

    layout.addStretch()
    layout.addWidget(ad_banner)

    window.show()

    print("Simple Ad Banner Test Started")
    print("Click the banner to open Coupang carousel in your browser")

    sys.exit(app.exec())

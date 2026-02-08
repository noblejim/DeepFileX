#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX CEF 광고 배너 위젯
CEFPython을 사용한 인앱 쿠팡 carousel 표시

Created: 2026-02-08
Author: QuantumLayer
License: MIT
Version: 2.0.0
"""

import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QTimer, QSize
import logging

logger = logging.getLogger(__name__)

# CEFPython import
try:
    from cefpython3 import cefpython as cef
    CEF_AVAILABLE = True
except ImportError as e:
    CEF_AVAILABLE = False
    logger.error(f"CEFPython not available: {e}")


class CEFAdBanner(QFrame):
    """
    CEFPython 기반 광고 배너 위젯
    프로그램 내부에 쿠팡 carousel 직접 표시
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

        if not CEF_AVAILABLE:
            logger.error("CEFPython not available - cannot create ad banner")
            self.hide()
            return

        self.browser = None
        self.init_ui()
        self.track_impression()

    def is_ads_enabled(self):
        """광고 활성화 여부"""
        return self.settings.value('ads_enabled', True, type=bool)

    def is_premium_user(self):
        """프리미엄 사용자 여부"""
        return self.settings.value('is_premium', False, type=bool)

    def init_ui(self):
        """UI 초기화 - CEF 브라우저 위젯 생성"""
        self.setFixedHeight(110)
        self.setStyleSheet("""
            CEFAdBanner {
                background-color: #f5f5f5;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # CEF 초기화
        sys.excepthook = cef.ExceptHook  # 예외 처리
        settings = {
            "debug": False,
            "log_severity": cef.LOGSEVERITY_INFO,
            "log_file": "",
        }
        cef.Initialize(settings)

        # HTML 콘텐츠 생성 (쿠팡 iframe 포함)
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
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
</html>"""

        # CEF 브라우저 생성
        window_info = cef.WindowInfo()
        window_info.SetAsChild(int(self.winId()), [0, 0, 900, 100])

        self.browser = cef.CreateBrowserSync(window_info, url="data:text/html;base64," +
                                             __import__('base64').b64encode(html_content.encode()).decode())

        logger.info("CEF browser created - Coupang carousel embedded")

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

    def closeEvent(self, event):
        """위젯 종료 시 CEF 정리"""
        if self.browser:
            self.browser.CloseBrowser(True)
        event.accept()


def shutdown_cef():
    """CEF 종료"""
    cef.Shutdown()


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
    window.setWindowTitle("CEF Ad Banner Test - DeepFileX")
    window.setGeometry(100, 100, 1000, 700)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # CEF Ad Banner 추가
    ad_banner = CEFAdBanner(location="test_banner")

    layout.addStretch()
    layout.addWidget(ad_banner)

    window.show()

    print("="*60)
    print("CEF Ad Banner Test Started")
    print("="*60)
    print("\nCoupang carousel should be visible at the bottom")
    print("Products should auto-rotate every 5-10 seconds")
    print("Click on products to visit purchase page")
    print("="*60 + "\n")

    app.aboutToQuit.connect(shutdown_cef)
    sys.exit(app.exec())

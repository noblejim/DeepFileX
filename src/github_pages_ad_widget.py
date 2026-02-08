#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX GitHub Pages 광고 배너 위젯
GitHub Pages에서 호스팅되는 Adsterra 배너 표시

Created: 2026-02-08
Author: QuantumLayer
License: MIT
Version: 1.0.0
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
import logging

logger = logging.getLogger(__name__)


class GitHubPagesAdWidget(QFrame):
    """
    GitHub Pages 광고 배너 위젯
    https://noblejim.github.io/DeepFileX/ads/ 에서 Adsterra 배너 로드
    """

    ad_clicked = pyqtSignal(str)

    def __init__(self, parent=None, location="bottom_banner"):
        super().__init__(parent)
        self.location = location
        self.settings = QSettings('DeepFileX', 'SmartLinks')

        # GitHub Pages URL
        self.ad_page_url = "https://noblejim.github.io/DeepFileX/ads/"

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
        """UI 초기화 - QWebEngineView로 GitHub Pages 로드"""
        self.setFixedHeight(160)
        self.setStyleSheet("""
            GitHubPagesAdWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        try:
            # QWebEngineView 생성
            self.web_view = QWebEngineView()
            self.web_view.setFixedSize(970, 140)

            # 설정
            page = self.web_view.page()
            settings = page.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

            # URL 로드
            self.web_view.setUrl(QUrl(self.ad_page_url))

            layout.addWidget(self.web_view, alignment=Qt.AlignmentFlag.AlignCenter)

            logger.info(f"GitHub Pages ad widget loaded: {self.ad_page_url}")

        except Exception as e:
            logger.error(f"Error creating web view: {e}")
            # Fallback to text label
            from PyQt6.QtWidgets import QLabel
            fallback_label = QLabel(f'<a href="{self.ad_page_url}">View Ads</a>')
            fallback_label.setOpenExternalLinks(True)
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)

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
            stats['source'] = 'github_pages'

            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2)

        except Exception as e:
            logger.error(f"Error tracking impression: {e}")


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
    window.setWindowTitle("GitHub Pages Ad Widget Test - DeepFileX")
    window.setGeometry(100, 100, 1000, 700)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # GitHub Pages Ad Widget 추가
    ad_banner = GitHubPagesAdWidget(location="test_banner")

    layout.addStretch()
    layout.addWidget(ad_banner)

    window.show()

    print("="*60)
    print("GitHub Pages Ad Widget Test Started")
    print("="*60)
    print(f"\nLoading ads from: https://noblejim.github.io/DeepFileX/ads/")
    print("Make sure GitHub Pages is enabled in repository settings")
    print("="*60 + "\n")

    sys.exit(app.exec())

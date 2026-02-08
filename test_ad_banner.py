#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SimpleAdBanner 테스트 스크립트
배너 클릭 시 쿠팡 carousel 페이지가 브라우저에서 열리는지 확인
"""

import sys
import logging
from pathlib import Path

# src 디렉토리를 sys.path에 추가
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
from simple_ad_widget import SimpleAdBanner

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SimpleAdBanner Test - DeepFileX")
        self.setGeometry(100, 100, 1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 제목
        title = QLabel("SimpleAdBanner Test")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # 설명
        description = QLabel(
            "Click the Coupang banner below to test:\n"
            "1. Browser opens with carousel page\n"
            "2. Products auto-rotate every 5-10 seconds\n"
            "3. Click individual products to view purchase page"
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("font-size: 14px; color: #666; margin: 10px;")
        layout.addWidget(description)

        layout.addStretch()

        # SimpleAdBanner 추가
        self.ad_banner = SimpleAdBanner(location="test_banner")

        # 시그널 연결
        self.ad_banner.ad_clicked.connect(self.on_ad_clicked)

        layout.addWidget(self.ad_banner)

        # 통계 레이블
        self.stats_label = QLabel("No clicks yet")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 12px; color: #999; margin: 10px;")
        layout.addWidget(self.stats_label)

        # 수동 테스트 버튼
        test_btn = QPushButton("Manual Test: Open Carousel")
        test_btn.clicked.connect(self.ad_banner.open_carousel_page)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(test_btn)

        print("\n" + "="*60)
        print("SimpleAdBanner Test Started")
        print("="*60)
        print("\nTest Steps:")
        print("1. Click the orange 'Coupang Partners' banner")
        print("2. Browser should open with carousel page")
        print("3. Wait 5-10 seconds to see products auto-rotate")
        print("4. Click individual products to test navigation")
        print("\nAlternatively, click the green button for manual test")
        print("="*60 + "\n")

    def on_ad_clicked(self, url):
        print(f"\n✅ Ad clicked! URL: {url}")
        self.stats_label.setText(f"✅ Ad clicked! Browser should be opening...")

        # 통계 읽기
        try:
            import json
            stats_file = Path.home() / 'AppData' / 'Roaming' / 'DeepFileX' / 'ads' / 'stats.json'
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                clicks = stats.get('clicks', 0)
                impressions = stats.get('impressions', 0)
                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                self.stats_label.setText(
                    f"✅ {clicks} clicks / {impressions} impressions = {ctr:.1f}% CTR"
                )
        except Exception as e:
            print(f"Error reading stats: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

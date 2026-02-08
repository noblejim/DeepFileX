#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX 회전 이미지 배너 위젯
쿠팡 상품 이미지를 자동으로 회전시키는 배너

Created: 2026-02-08
Author: QuantumLayer
License: MIT
Version: 1.0.0
"""

import sys
import requests
from io import BytesIO
from pathlib import Path
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QTimer, QUrl
from PyQt6.QtGui import QPixmap, QCursor, QDesktopServices
import logging

logger = logging.getLogger(__name__)


class RotatingImageBanner(QFrame):
    """
    회전 이미지 배너 위젯
    쿠팡 상품 이미지를 자동으로 회전하며 표시
    """

    ad_clicked = pyqtSignal(str)

    def __init__(self, parent=None, location="bottom_banner"):
        super().__init__(parent)
        self.location = location
        self.settings = QSettings('DeepFileX', 'SmartLinks')

        # 쿠팡 파트너스 트래킹 코드
        self.tracking_code = "AF1662515"
        self.partner_base = "https://link.coupang.com/a/dHXhN0"

        # 상품 데이터 (이미지 URL, 상품명, 구매 링크)
        self.products = [
            {
                "name": "삼성 갤럭시북4",
                "image_url": "https://image.coupangcdn.com/image/retail/images/2024/03/06/16/0/d5c5e5f0-3b61-4e3a-8b0a-7c8e8e8e8e8e.jpg",
                "product_url": "https://www.coupang.com/vp/products/7851234567?itemId=21234567&vendorItemId=88234567&src=1139000&spec=10799999&addtag=400&ctag=7851234567&lptag=AF1662515&itime=20260208&pageType=PRODUCT&pageValue=7851234567&wPcid=17391234567890&wRef=&wTime=20260208&redirect=landing&traceid=V0-153-12345678-12345678&mcid=5678901234567890&placementid=&clickBeacon=&campaignid=&contentcategory=&imgsize=&tsource=&pageid=&deviceid=&token=&contenttype=&subid=&impressionid=&campaigntag=&requestid=&contentkeyword=&subparam=&isAddedCart="
            },
            {
                "name": "LG 그램 노트북",
                "image_url": "https://image.coupangcdn.com/image/retail/images/2024/02/15/10/5/a1b2c3d4-5e6f-7g8h-9i0j-k1l2m3n4o5p6.jpg",
                "product_url": "https://www.coupang.com/vp/products/7654321098?itemId=20987654&vendorItemId=87654321&src=1139000&spec=10799999&addtag=400&ctag=7654321098&lptag=AF1662515"
            },
            {
                "name": "애플 에어팟 프로",
                "image_url": "https://image.coupangcdn.com/image/retail/images/2024/01/20/14/2/b2c3d4e5-6f7g-8h9i-0j1k-l2m3n4o5p6q7.jpg",
                "product_url": "https://www.coupang.com/vp/products/6543210987?itemId=19876543&vendorItemId=86543210&src=1139000&spec=10799999&addtag=400&ctag=6543210987&lptag=AF1662515"
            },
            {
                "name": "로지텍 MX Master",
                "image_url": "https://image.coupangcdn.com/image/retail/images/2024/03/10/9/7/c3d4e5f6-7g8h-9i0j-1k2l-m3n4o5p6q7r8.jpg",
                "product_url": "https://www.coupang.com/vp/products/5432109876?itemId=18765432&vendorItemId=85432109&src=1139000&spec=10799999&addtag=400&ctag=5432109876&lptag=AF1662515"
            },
        ]

        self.current_index = 0
        self.image_cache = {}

        # 광고 비활성화 확인
        if not self.is_ads_enabled() or self.is_premium_user():
            self.hide()
            return

        self.init_ui()
        self.load_images()
        self.start_rotation()
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
            RotatingImageBanner {
                background-color: #ffffff;
                border: 2px solid #FA2828;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 이미지 레이블
        self.image_label = QLabel("Loading products...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(900, 100)
        self.image_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.image_label.mousePressEvent = lambda e: self.on_banner_clicked()
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border-radius: 6px;
                color: #666;
                font-size: 14px;
            }
        """)

        layout.addWidget(self.image_label)
        logger.info("Rotating image banner initialized")

    def load_images(self):
        """상품 이미지 로드"""
        # 실제 쿠팡 이미지 대신 플레이스홀더 사용
        # 실제 구현에서는 requests로 이미지 다운로드

        try:
            # 임시: 첫 번째 상품 표시
            self.show_product(0)
        except Exception as e:
            logger.error(f"Error loading images: {e}")
            self.image_label.setText("Failed to load products")

    def show_product(self, index):
        """특정 상품 표시"""
        if index >= len(self.products):
            index = 0

        product = self.products[index]

        # 이미지가 캐시에 있으면 사용
        if index in self.image_cache:
            pixmap = self.image_cache[index]
        else:
            # 실제로는 product['image_url']에서 다운로드
            # 여기서는 플레이스홀더 생성
            pixmap = self.create_placeholder(product['name'])
            self.image_cache[index] = pixmap

        # 이미지 표시
        scaled_pixmap = pixmap.scaled(
            900, 100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.current_index = index

    def create_placeholder(self, product_name):
        """플레이스홀더 이미지 생성 (실제로는 다운로드한 이미지 사용)"""
        from PyQt6.QtGui import QImage, QPainter, QFont, QColor

        # 900x100 이미지 생성
        image = QImage(900, 100, QImage.Format.Format_RGB32)
        image.fill(QColor(255, 255, 255))

        painter = QPainter(image)

        # 배경 그라데이션
        from PyQt6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 900, 0)
        gradient.setColorAt(0, QColor(250, 40, 40))
        gradient.setColorAt(0.5, QColor(255, 107, 44))
        gradient.setColorAt(1, QColor(255, 217, 61))
        painter.fillRect(0, 0, 900, 100, gradient)

        # 텍스트
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 20, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(0, 0, 900, 100, Qt.AlignmentFlag.AlignCenter,
                        f"🛒 {product_name}")

        painter.end()

        return QPixmap.fromImage(image)

    def start_rotation(self):
        """자동 회전 시작"""
        self.rotation_timer = QTimer()
        self.rotation_timer.timeout.connect(self.rotate_to_next)
        self.rotation_timer.start(7000)  # 7초마다 회전
        logger.info("Product rotation started (7 seconds interval)")

    def rotate_to_next(self):
        """다음 상품으로 회전"""
        next_index = (self.current_index + 1) % len(self.products)
        self.show_product(next_index)
        logger.info(f"Rotated to product {next_index}: {self.products[next_index]['name']}")

    def on_banner_clicked(self):
        """배너 클릭 처리"""
        product = self.products[self.current_index]
        product_url = product['product_url']

        try:
            success = QDesktopServices.openUrl(QUrl(product_url))

            if success:
                self.track_click()
                self.ad_clicked.emit(product_url)
                logger.info(f"Product clicked: {product['name']}")
            else:
                logger.warning(f"Failed to open URL: {product_url}")

        except Exception as e:
            logger.error(f"Error opening product URL: {e}")

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
    window.setWindowTitle("Rotating Image Banner Test - DeepFileX")
    window.setGeometry(100, 100, 1000, 700)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # Rotating Image Banner 추가
    ad_banner = RotatingImageBanner(location="test_banner")

    layout.addStretch()
    layout.addWidget(ad_banner)

    window.show()

    print("="*60)
    print("Rotating Image Banner Test Started")
    print("="*60)
    print("\nProduct images rotate every 7 seconds")
    print("Click on banner to visit product page")
    print("="*60 + "\n")

    sys.exit(app.exec())

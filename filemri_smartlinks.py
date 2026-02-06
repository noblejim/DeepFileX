#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX SmartLinks 통합 시스템
Adsterra SmartLinks를 DeepFileX 메인 앱에 통합하는 모듈

Created: 2025-08-28
Author: QuantumLayer
License: MIT
Version: 1.0.0
"""

import os
import json
import webbrowser
from datetime import datetime, date
from pathlib import Path
from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QDialog, QDialogButtonBox, QCheckBox,
                            QProgressBar, QMessageBox, QGroupBox, QTextEdit)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSettings, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon


class DeepFileXSmartLinksManager:
    """DeepFileX SmartLinks 관리자"""

    def __init__(self):
        # Adsterra SmartLinks 설정 (실제 활성화된 정보)
        self.config = {
            'smartlink_id': '27417447',
            'status': 'Active',
            'publisher': 'quantumlayer',
            'api_token': '2ba30d53a9017b5390b38736dda7156e',
            'base_url': 'https://www.profitableratecpm.com/nndiuxsyi',
            'key': '7f25d09e5bc7b1e1c3cb37e467e6821d'
        }
        
        # 통계 데이터
        self.session_stats = {
            'impressions': 0,
            'clicks': 0,
            'session_start': datetime.now(),
            'last_interaction': None,
            'contexts': []
        }
        
        # 설정 및 로그 초기화
        self.settings = QSettings('DeepFileX', 'SmartLinks')
        self.setup_data_storage()
    
    def setup_data_storage(self):
        """데이터 저장소 설정"""
        # 경로: 기본 %APPDATA%\DeepFileX\ads\, 환경변수 FILEMRI_ADS_DIR로 덮어쓰기 가능
        ads_override = os.environ.get('FILEMRI_ADS_DIR')
        if ads_override:
            self.appdata_path = Path(ads_override)
        else:
            self.appdata_path = Path(os.environ.get('APPDATA', '')) / 'DeepFileX' / 'ads'
        self.appdata_path.mkdir(parents=True, exist_ok=True)
        
        # 로그 파일들
        today = date.today().strftime('%Y%m%d')
        self.daily_stats_file = self.appdata_path / 'daily_stats.json'
        self.smartlinks_log_file = self.appdata_path / f'smartlinks_{today}.log'
        
        # 기존 통계 로드
        self.load_daily_stats()
    
    def load_daily_stats(self):
        """일일 통계 로드"""
        try:
            if self.daily_stats_file.exists():
                with open(self.daily_stats_file, 'r', encoding='utf-8') as f:
                    self.daily_stats = json.load(f)
            else:
                self.daily_stats = {}
        except Exception as e:
            print(f"일일 통계 로드 실패: {e}")
            self.daily_stats = {}
    
    def save_daily_stats(self):
        """일일 통계 저장"""
        try:
            with open(self.daily_stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.daily_stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"일일 통계 저장 실패: {e}")
    
    def log_event(self, event_type, context="", details=""):
        """이벤트 로깅"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'type': event_type,
            'context': context,
            'details': details,
            'session_id': id(self)
        }
        
        # 파일에 로그 기록
        try:
            with open(self.smartlinks_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"로그 기록 실패: {e}")
        
        return log_entry
    
    def generate_smartlink_url(self, context="filemri", location="bottom_banner"):
        """SmartLink URL 생성"""
        # 기본 파라미터
        params = {
            'key': self.config['key'],
            'source': 'filemri_app',
            'context': context,
            'location': location,
            'smartlink_id': self.config['smartlink_id'],
            'timestamp': int(datetime.now().timestamp()),
            'version': '1.2.0'
        }
        
        # URL 조합
        param_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        full_url = f"{self.config['base_url']}?{param_string}"
        
        # 이벤트 로깅
        self.log_event('URL_GENERATED', context, f"Location: {location}")
        
        return full_url
    
    def track_impression(self, location="bottom_banner"):
        """광고 노출 추적"""
        self.session_stats['impressions'] += 1
        self.session_stats['last_interaction'] = datetime.now()
        
        # 일일 통계 업데이트
        today = date.today().strftime('%Y-%m-%d')
        if today not in self.daily_stats:
            self.daily_stats[today] = {'impressions': 0, 'clicks': 0, 'sessions': []}
        
        self.daily_stats[today]['impressions'] += 1
        if id(self) not in self.daily_stats[today]['sessions']:
            self.daily_stats[today]['sessions'].append(id(self))
        
        self.save_daily_stats()
        self.log_event('IMPRESSION', location)
        
        return self.session_stats['impressions']
    
    def track_click(self, context="unknown", location="bottom_banner"):
        """클릭 추적 및 URL 열기"""
        self.session_stats['clicks'] += 1
        self.session_stats['last_interaction'] = datetime.now()
        self.session_stats['contexts'].append(context)
        
        # 일일 통계 업데이트
        today = date.today().strftime('%Y-%m-%d')
        if today not in self.daily_stats:
            self.daily_stats[today] = {'impressions': 0, 'clicks': 0, 'sessions': []}
        
        self.daily_stats[today]['clicks'] += 1
        self.save_daily_stats()
        
        # URL 생성 및 브라우저 열기
        url = self.generate_smartlink_url(context, location)
        
        try:
            webbrowser.open(url)
            success = True
            self.log_event('CLICK_SUCCESS', context, f"URL: {url[:100]}...")
        except Exception as e:
            success = False
            self.log_event('CLICK_FAILED', context, f"Error: {e}")
        
        return success, url
    
    def get_click_rate(self):
        """클릭율 계산"""
        if self.session_stats['impressions'] == 0:
            return 0.0
        return (self.session_stats['clicks'] / self.session_stats['impressions']) * 100
    
    def get_estimated_revenue(self):
        """예상 수익 계산 (평균 CPC $0.15 기준)"""
        average_cpc = 0.15
        return self.session_stats['clicks'] * average_cpc
    
    def is_ads_enabled(self):
        """광고 활성화 여부 확인"""
        return self.settings.value('ads_enabled', True, type=bool)
    
    def is_premium_user(self):
        """프리미엄 사용자 여부 확인"""
        return self.settings.value('is_premium', False, type=bool)


class SmartLinksAdWidget(QFrame):
    """SmartLinks 광고 위젯"""
    
    # 시그널 정의
    ad_clicked = pyqtSignal(str, str)  # (context, url)
    ad_shown = pyqtSignal(str)         # (location)
    premium_requested = pyqtSignal()   # 프리미엄 업그레이드 요청
    
    def __init__(self, parent=None, location="bottom_banner"):
        super().__init__(parent)
        self.location = location
        self.manager = DeepFileXSmartLinksManager()
        self.context = "file_management"
        
        # 광고가 비활성화되어 있으면 숨기기
        if not self.manager.is_ads_enabled() or self.manager.is_premium_user():
            self.hide()
            return
        
        self.init_ui()
        self.setup_timer()
        
        # 노출 추적
        self.manager.track_impression(self.location)
        self.ad_shown.emit(self.location)
    
    def init_ui(self):
        """UI 초기화"""
        self.setFixedHeight(100)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 광고 배너 스타일 (이미지 형식)
        self.setStyleSheet("""
            SmartLinksAdWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #667eea, stop: 0.5 #764ba2, stop: 1 #f093fb);
                border: 1px solid #cccccc;
                border-radius: 12px;
                margin: 8px;
            }
            SmartLinksAdWidget:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #5a6fd8, stop: 0.5 #6a4190, stop: 1 #de7fe9);
                border: 1px solid #999999;
                transform: scale(1.02);
            }
            QLabel {
                color: white;
                background-color: transparent;
                font-weight: bold;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 광고 콘텐츠 영역
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 메인 광고 텍스트
        main_text = QLabel("Discover Premium Tools & Solutions")
        main_text.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        main_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_text.setStyleSheet("color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);")
        
        # 서브 텍스트  
        sub_text = QLabel("Click to explore professional software recommendations")
        sub_text.setFont(QFont("Arial", 11))
        sub_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_text.setStyleSheet("color: rgba(255,255,255,0.9); margin-top: 5px;")
        
        content_layout.addWidget(main_text)
        content_layout.addWidget(sub_text)
        
        # 작은 광고 표시 (우측 하단)
        ad_label = QLabel("Ad")
        ad_label.setFont(QFont("Arial", 8))
        ad_label.setStyleSheet("""
            color: rgba(255,255,255,0.7);
            background-color: rgba(0,0,0,0.3);
            padding: 2px 6px;
            border-radius: 3px;
        """)
        ad_label.setFixedSize(25, 16)
        ad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 메인 레이아웃
        layout.addLayout(content_layout, 1)
        layout.addWidget(ad_label, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        
        # 🆕 배너 전체에 클릭 이벤트 연결
        self.mousePressEvent = self.on_banner_clicked
    
    def on_banner_clicked(self, event):
        """🆕 배너 전체 클릭 처리"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_ad_clicked()
    
    def setup_timer(self):
        """타이머 설정 (광고 갱신용)"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_ad_content)
        self.refresh_timer.start(300000)  # 5분마다 갱신
    
    def on_ad_clicked(self):
        """💰 광고 클릭 처리 (배너 전체 클릭)"""
        try:
            success, url = self.manager.track_click(self.context, self.location)
            
            if success:
                # 통계 표시 (개발 중에만)
                stats = self.manager.session_stats
                estimated_revenue = self.manager.get_estimated_revenue()
                click_rate = self.manager.get_click_rate()
                
                print(f"💰 광고 클릭 성공!")
                print(f"📊 세션 통계: {stats['clicks']}클릭 / {stats['impressions']}노출")
                print(f"📈 클릭율: {click_rate:.1f}%")
                print(f"💵 예상 수익: ${estimated_revenue:.3f}")
            
            # 시그널 발송
            self.ad_clicked.emit(self.context, url)
            
        except Exception as e:
            print(f"광고 클릭 처리 오류: {e}")
    
    def show_ad_settings(self):
        """광고 설정 다이얼로그"""
        dialog = AdSettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 설정 변경 사항 적용
            if not self.manager.is_ads_enabled():
                self.hide()
    
    def show_premium_dialog(self):
        """프리미엄 업그레이드 다이얼로그"""
        dialog = PremiumUpgradeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.premium_requested.emit()
            self.hide()  # 프리미엄으로 업그레이드하면 광고 숨기기
    
    def refresh_ad_content(self):
        """광고 내용 갱신"""
        # 다양한 광고 메시지 로테이션
        main_messages = [
            "Discover Premium Tools & Solutions",
            "Professional Software Recommendations", 
            "Essential Tools for Productivity",
            "Recommended by IT Professionals"
        ]
        
        sub_messages = [
            "Click to explore professional software recommendations",
            "Find the right tools for your workflow",
            "Enhance your productivity with expert picks",
            "Discover software solutions that work"
        ]
        
        import random
        main_text = random.choice(main_messages)
        sub_text = random.choice(sub_messages)
        
        # UI 업데이트
        try:
            labels = self.findChildren(QLabel)
            for label in labels:
                if label.font().pointSize() == 16:  # 메인 텍스트
                    if label.text() != main_text:
                        label.setText(main_text)
                elif label.font().pointSize() == 11:  # 서브 텍스트
                    if label.text() != sub_text:
                        label.setText(sub_text)
        except Exception as e:
            print(f"광고 메시지 업데이트 오류: {e}")
    
    def update_ad_message(self, main_text, sub_text=None):
        """광고 메시지 업데이트"""
        try:
            labels = self.findChildren(QLabel)
            for label in labels:
                if label.font().pointSize() == 16:  # 메인 텍스트
                    label.setText(main_text)
                elif label.font().pointSize() == 11 and sub_text:  # 서브 텍스트
                    label.setText(sub_text)
        except Exception as e:
            print(f"광고 메시지 업데이트 오류: {e}")
    
    def set_context(self, new_context):
        """컨텍스트 설정 (DeepFileX 상태에 따라)"""
        self.context = new_context
        
        # 컨텍스트별 메시지 최적화
        context_messages = {
            "file_scan_complete": ("Scan Complete! Next Steps", "Discover optimization tools for better performance"),
            "large_files_found": ("Large Files Detected", "Find tools to manage and optimize storage space"),
            "system_health_good": ("System Running Well", "Maintain peak performance with recommended tools"),
            "search_results_empty": ("Enhance Your Search", "Discover advanced search and file management tools")
        }
        
        if new_context in context_messages:
            main_text, sub_text = context_messages[new_context]
            self.update_ad_message(main_text, sub_text)


class AdSettingsDialog(QDialog):
    """광고 설정 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎯 SmartLinks 광고 설정")
        self.setFixedSize(400, 300)
        self.settings = QSettings('DeepFileX', 'SmartLinks')
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 설명
        info_group = QGroupBox("📊 SmartLinks 수익화 정보")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
🎯 SmartLinks는 DeepFileX를 무료로 유지하기 위한 수익화 시스템입니다.
💰 광고 클릭을 통해 개발비용을 충당하고 지속적인 업데이트를 제공합니다.
🏥 의료 테마에 맞는 전문 도구들을 추천하여 사용자에게도 도움이 됩니다.
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #2c3e50; padding: 10px;")
        
        info_layout.addWidget(info_text)
        layout.addWidget(info_group)
        
        # 설정 옵션
        settings_group = QGroupBox("⚙️ 광고 설정")
        settings_layout = QVBoxLayout(settings_group)
        
        self.ads_enabled_cb = QCheckBox("📢 SmartLinks 광고 활성화")
        self.ads_enabled_cb.setChecked(self.settings.value('ads_enabled', True, type=bool))
        
        self.privacy_mode_cb = QCheckBox("🔒 개인정보 보호 모드 (추적 최소화)")
        self.privacy_mode_cb.setChecked(self.settings.value('privacy_mode', False, type=bool))
        
        settings_layout.addWidget(self.ads_enabled_cb)
        settings_layout.addWidget(self.privacy_mode_cb)
        layout.addWidget(settings_group)
        
        # 통계
        stats_group = QGroupBox("📈 현재 세션 통계")
        stats_layout = QVBoxLayout(stats_group)
        
        manager = DeepFileXSmartLinksManager()
        stats_text = f"""
노출 수: {manager.session_stats['impressions']}회
클릭 수: {manager.session_stats['clicks']}회
클릭율: {manager.get_click_rate():.1f}%
예상 수익: ${manager.get_estimated_revenue():.3f}
        """
        
        stats_label = QLabel(stats_text)
        stats_label.setFont(QFont("Consolas", 10))
        stats_layout.addWidget(stats_label)
        layout.addWidget(stats_group)
        
        # 버튼
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def accept(self):
        """설정 저장"""
        self.settings.setValue('ads_enabled', self.ads_enabled_cb.isChecked())
        self.settings.setValue('privacy_mode', self.privacy_mode_cb.isChecked())
        super().accept()


class PremiumUpgradeDialog(QDialog):
    """프리미엄 업그레이드 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👑 DeepFileX 프리미엄")
        self.setFixedSize(450, 400)
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 헤더
        header_label = QLabel("👑 DeepFileX 프리미엄으로 업그레이드")
        header_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("color: #f39c12; margin: 10px;")
        layout.addWidget(header_label)
        
        # 프리미엄 혜택
        benefits_group = QGroupBox("✨ 프리미엄 혜택")
        benefits_layout = QVBoxLayout(benefits_group)
        
        benefits = [
            "🚫 모든 광고 제거",
            "⚡ 더 빠른 스캔 속도",
            "🔍 고급 검색 필터",
            "💾 무제한 인덱스 저장",
            "🏥 의료진 전용 기능",
            "📊 상세 진단 리포트",
            "🔒 프라이버시 강화",
            "🆘 우선 기술 지원"
        ]
        
        for benefit in benefits:
            benefit_label = QLabel(benefit)
            benefit_label.setStyleSheet("padding: 3px; color: #27ae60;")
            benefits_layout.addWidget(benefit_label)
        
        layout.addWidget(benefits_group)
        
        # 가격 정보
        price_group = QGroupBox("💰 요금제")
        price_layout = QVBoxLayout(price_group)
        
        price_label = QLabel("월 $9.99 / 연 $99.99 (2개월 무료)")
        price_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        price_label.setStyleSheet("color: #e74c3c; margin: 10px;")
        
        trial_label = QLabel("🎁 7일 무료 체험 가능")
        trial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trial_label.setStyleSheet("color: #27ae60; font-style: italic;")
        
        price_layout.addWidget(price_label)
        price_layout.addWidget(trial_label)
        layout.addWidget(price_group)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        trial_btn = QPushButton("🎁 무료 체험 시작")
        trial_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        upgrade_btn = QPushButton("👑 지금 업그레이드")
        upgrade_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        
        cancel_btn = QPushButton("나중에")
        cancel_btn.clicked.connect(self.reject)
        
        trial_btn.clicked.connect(self.start_trial)
        upgrade_btn.clicked.connect(self.start_upgrade)
        
        button_layout.addWidget(trial_btn)
        button_layout.addWidget(upgrade_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
    
    def start_trial(self):
        """무료 체험 시작"""
        QMessageBox.information(self, "🎁 무료 체험", 
                               "7일 무료 체험이 시작되었습니다!\n"
                               "프리미엄 기능을 자유롭게 사용해보세요.")
        
        settings = QSettings('DeepFileX', 'SmartLinks')
        settings.setValue('is_premium', True)
        settings.setValue('trial_end_date', 
                         datetime.now().isoformat())
        
        self.accept()
    
    def start_upgrade(self):
        """프리미엄 업그레이드"""
        QMessageBox.information(self, "👑 프리미엄 업그레이드", 
                               "프리미엄 결제 페이지로 이동합니다.\n"
                               "결제 완료 후 자동으로 활성화됩니다.")
        
        # 결제 페이지 열기 (향후 구현)
        webbrowser.open("https://filemri.com/premium")
        
        self.accept()


# 사용 예시 및 테스트 코드
def test_smartlinks_widget():
    """SmartLinks 위젯 테스트"""
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    
    # 테스트 윈도우
    window = QMainWindow()
    window.setWindowTitle("DeepFileX SmartLinks 테스트")
    window.setGeometry(100, 100, 800, 600)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    
    # SmartLinks 위젯 추가
    smartlinks_widget = SmartLinksAdWidget(location="test_bottom")
    
    # 시그널 연결
    def on_ad_clicked(context, url):
        print(f"광고 클릭됨: {context} -> {url[:50]}...")
    
    def on_ad_shown(location):
        print(f"광고 표시됨: {location}")
    
    smartlinks_widget.ad_clicked.connect(on_ad_clicked)
    smartlinks_widget.ad_shown.connect(on_ad_shown)
    
    layout.addStretch()  # 상단 여백
    layout.addWidget(smartlinks_widget)  # 하단에 광고 배치
    
    window.show()
    
    print("🎯 SmartLinks 위젯 테스트 시작")
    print("📊 광고 클릭 시 브라우저가 열리고 통계가 기록됩니다")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_smartlinks_widget()

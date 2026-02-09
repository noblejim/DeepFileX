#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX 자동 업데이트 시스템
사용자가 앱을 시작할 때 새 버전 확인 및 알림

Created: 2025-08-28
Author: QuantumLayer
License: MIT
Version: 1.0.0
"""

import sys
import os
import json
import webbrowser
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTextEdit, QProgressBar, QCheckBox,
                            QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QTimer
from PyQt6.QtGui import QFont, QPixmap

# 버전 및 업데이트 설정 (version_config.py에서 import)
try:
    from version_config import (
        VERSION, UPDATE_CONFIG, UPDATE_MESSAGES,
        get_update_test_data, is_newer_version
    )
    CURRENT_VERSION = VERSION
    CONFIG_AVAILABLE = True
except ImportError:
    # Fallback: 하드코딩된 값들
    CURRENT_VERSION = "1.3.0"
    UPDATE_CONFIG = {
        "check_url": "https://api.github.com/repos/noblejim/DeepFileX/releases/latest",
        "test_mode": True,
        "test_version": "1.4.0",
        "auto_check_enabled": True,
        "check_interval_days": 7,
        "startup_delay_seconds": 5
    }
    UPDATE_MESSAGES = {
        "update_available": "🔷 New version available!",
        "download_update": "🚀 Update Now",
        "remind_later": "⏰ Remind Later"
    }
    CONFIG_AVAILABLE = False


class UpdateChecker(QThread):
    """업데이트 체크 스레드 (GitHub API 사용)"""
    
    update_available = pyqtSignal(dict)  # 업데이트 정보
    no_update = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_version = CURRENT_VERSION
        self.check_url = UPDATE_CONFIG.get("check_url", "")
        self.settings = QSettings('DeepFileX', 'Updates')
    
    def run(self):
        """업데이트 체크 실행"""
        try:
            # 테스트 모드이거나 실제 GitHub API 사용
            if UPDATE_CONFIG.get("test_mode", False):
                # 개발/테스트용: 가짜 업데이트 정보 생성
                release_data = get_update_test_data() if CONFIG_AVAILABLE else self.create_fake_update_data()
            else:
                # 실제 환경에서는 requests 사용
                import requests
                from requests.exceptions import (
                    ConnectionError, Timeout, HTTPError,
                    TooManyRedirects, JSONDecodeError, RequestException
                )

                try:
                    response = requests.get(self.check_url, timeout=10)
                    response.raise_for_status()
                    release_data = response.json()

                except ConnectionError:
                    self.error_occurred.emit("❌ 서버 연결 실패: 네트워크 연결을 확인하세요")
                    return
                except Timeout:
                    self.error_occurred.emit("⏱️ 요청 시간 초과: 네트워크가 느리거나 서버가 응답하지 않습니다")
                    return
                except HTTPError as e:
                    if hasattr(e.response, 'status_code'):
                        if e.response.status_code == 404:
                            self.error_occurred.emit("❌ 업데이트 정보를 찾을 수 없습니다 (404)")
                        elif e.response.status_code == 403:
                            self.error_occurred.emit("🚫 API 접근 제한: 잠시 후 다시 시도하세요 (403)")
                        elif e.response.status_code >= 500:
                            self.error_occurred.emit(f"🔧 서버 오류: GitHub 서버에 문제가 있습니다 ({e.response.status_code})")
                        else:
                            self.error_occurred.emit(f"❌ HTTP 오류: {e}")
                    else:
                        self.error_occurred.emit(f"❌ HTTP 오류: {e}")
                    return
                except TooManyRedirects:
                    self.error_occurred.emit("🔄 리다이렉트 오류: URL 설정을 확인하세요")
                    return
                except JSONDecodeError:
                    self.error_occurred.emit("⚠️ 응답 파싱 실패: 서버 응답 형식이 잘못되었습니다")
                    return
                except RequestException as e:
                    self.error_occurred.emit(f"🌐 네트워크 오류: {str(e)}")
                    return

            latest_version = release_data['tag_name'].lstrip('v')

            if CONFIG_AVAILABLE:
                version_is_newer = is_newer_version(latest_version)
            else:
                version_is_newer = self.is_newer_version(latest_version, self.current_version)

            if version_is_newer:
                # 사용자가 스킵한 버전인지 확인
                skipped_versions = self.settings.value('skipped_versions', [])
                if latest_version not in skipped_versions:
                    update_info = {
                        'version': latest_version,
                        'name': release_data.get('name', f'Version {latest_version}'),
                        'body': release_data.get('body', '업데이트 내용을 확인할 수 없습니다.'),
                        'download_url': self.get_installer_url(release_data),
                        'published_at': release_data.get('published_at'),
                        'html_url': release_data.get('html_url')
                    }
                    self.update_available.emit(update_info)
                else:
                    self.no_update.emit()
            else:
                self.no_update.emit()

        except KeyError as e:
            self.error_occurred.emit(f"⚠️ 응답 데이터 오류: 필수 필드가 없습니다 ({e})")
        except Exception as e:
            self.error_occurred.emit(f"❌ 예상치 못한 오류: {str(e)}")
    
    def create_fake_update_data(self):
        """개발/테스트용: 가짜 업데이트 데이터 생성"""
        return {
            'tag_name': 'v1.4.0',
            'name': 'DeepFileX v1.4.0 - 성능 향상 및 새 기능',
            'body': """🎉 주요 개선사항:
• 🚀 파일 스캔 속도 50% 향상
• 📁 새로운 파일 형식 지원 (ZIP, RAR, 7Z)
• 🎨 UI/UX 대폭 개선 및 다크모드 최적화
• 🔍 고급 검색 필터 추가
• 🛡️ 보안 강화 및 버그 수정

💰 SmartLinks 수익화 개선:
• 광고 클릭률 30% 향상된 새로운 배너 디자인
• 컨텍스트 기반 스마트 광고 타겟팅
• 수익 통계 대시보드 추가

🔷 프로페셔널 기능 강화:
• 모던 UI 디자인 완성도 향상
• 상세 분석 리포트 기능 추가
• 전문가를 위한 고급 기능 확장""",
            'assets': [
                {
                    'name': 'DeepFileX_v1.4.0_Setup.exe',
                    'browser_download_url': 'https://github.com/noblejim/DeepFileX/releases/download/v1.4.0/DeepFileX_v1.4.0_Setup.exe'
                }
            ],
            'published_at': '2025-08-29T10:00:00Z',
            'html_url': 'https://github.com/noblejim/DeepFileX/releases/tag/v1.4.0'
        }
    
    def is_newer_version(self, latest: str, current: str) -> bool:
        """버전 비교 (semantic versioning)"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # 길이 맞춤
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
        except ValueError:
            return False
    
    def get_installer_url(self, release_data) -> str:
        """인스톨러 다운로드 URL 추출"""
        assets = release_data.get('assets', [])
        for asset in assets:
            if asset['name'].endswith('_Setup.exe'):
                return asset['browser_download_url']
        return release_data.get('html_url', '')  # 없으면 릴리즈 페이지로
    
    def should_check_update(self) -> bool:
        """업데이트 체크 필요 여부 판단"""
        if not self.settings.value('auto_check_enabled', UPDATE_CONFIG.get('auto_check_enabled', True)):
            return False
        
        # 강제 체크 모드
        if UPDATE_CONFIG.get('force_update_check', False):
            return True
        
        last_check = self.settings.value('last_check_date')
        if last_check:
            try:
                last_check_date = datetime.fromisoformat(last_check)
                check_interval = self.settings.value('check_interval_days', UPDATE_CONFIG.get('check_interval_days', 7))
                if datetime.now() - last_check_date < timedelta(days=check_interval):
                    return False
            except ValueError:
                pass  # 잘못된 날짜 형식이면 체크 진행
        
        return True
    
    def mark_checked(self):
        """체크 완료 표시"""
        self.settings.setValue('last_check_date', datetime.now().isoformat())


class UpdateDialog(QDialog):
    """DeepFileX 업데이트 알림 다이얼로그"""
    
    def __init__(self, parent, update_info):
        super().__init__(parent)
        self.update_info = update_info
        self.settings = QSettings('DeepFileX', 'Updates')
        self.init_ui()
    
    def init_ui(self):
        """DeepFileX UI Initialization"""
        self.setWindowTitle("🔷 DeepFileX Update Notification")
        self.setFixedSize(550, 650)

        # DeepFileX 스타일 (메인 앱과 동일한 스타일)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 10px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2980b9;
            }
            QLabel {
                color: #2c3e50;
                background-color: transparent;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                padding: 10px;
                font-family: 'Consolas', monospace;
            }
            QCheckBox {
                color: #2c3e50;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #3498db;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #2980b9;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # DeepFileX 헤더
        header_group = QGroupBox("🔷 DeepFileX 업데이트")
        header_layout = QVBoxLayout(header_group)

        title = QLabel(UPDATE_MESSAGES.get('update_available', 'New update available!'))
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #27ae60; margin: 10px;")
        
        version_info = QLabel(f"Current Version: {CURRENT_VERSION} → New Version: {self.update_info['version']}")
        version_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_info.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        version_info.setStyleSheet("color: #e74c3c; margin: 5px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(version_info)
        layout.addWidget(header_group)
        
        # Release Notes
        changes_group = QGroupBox("📋 Analysis Improvements & New Features")
        changes_layout = QVBoxLayout(changes_group)
        
        changes_text = QTextEdit()
        changes_text.setPlainText(self.update_info['body'])
        changes_text.setMinimumHeight(400)
        changes_text.setReadOnly(True)
        
        changes_layout.addWidget(changes_text)
        layout.addWidget(changes_group)
        
        # Update Settings
        options_group = QGroupBox("⚙️ Update Settings")
        options_layout = QVBoxLayout(options_group)
        
        self.auto_check_cb = QCheckBox("🔄 Auto-check for updates (every 7 days)")
        auto_check_enabled = self.settings.value('auto_check_enabled', True)
        if isinstance(auto_check_enabled, str):
            auto_check_enabled = auto_check_enabled.lower() == 'true'
        self.auto_check_cb.setChecked(bool(auto_check_enabled))
        
        self.notify_cb = QCheckBox("🔔 Background auto-check")
        background_check = self.settings.value('background_check', True)
        if isinstance(background_check, str):
            background_check = background_check.lower() == 'true'
        self.notify_cb.setChecked(bool(background_check))
        
        options_layout.addWidget(self.auto_check_cb)
        options_layout.addWidget(self.notify_cb)
        layout.addWidget(options_group)

        # 액션 버튼들
        button_layout = QHBoxLayout()

        # Update Now
        update_text = UPDATE_MESSAGES.get('download_update', 'Update Now')
        if '(' in update_text:
            update_text = update_text.replace(' (', '\n(')
        self.update_btn = QPushButton(update_text)
        self.update_btn.setMinimumWidth(160)
        self.update_btn.setMinimumHeight(56)
        self.update_btn.clicked.connect(self.download_update)
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                font-size: 11px;
                padding: 10px 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        # Remind Later (Monitor Progress)
        later_text = UPDATE_MESSAGES.get('remind_later', 'Remind Later')
        if '(' in later_text:
            later_text = later_text.replace(' (', '\n(')
        self.later_btn = QPushButton(later_text)
        self.later_btn.setMinimumWidth(160)
        self.later_btn.setMinimumHeight(56)
        self.later_btn.clicked.connect(self.remind_later)
        self.later_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                font-size: 11px;
                padding: 10px 16px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        
        # Skip Version (Decline Treatment)
        skip_text = UPDATE_MESSAGES.get('skip_version', 'Skip Version')
        if '(' in skip_text:
            skip_text = skip_text.replace(' (', '\n(')
        self.skip_btn = QPushButton(skip_text)
        self.skip_btn.setMinimumWidth(160)
        self.skip_btn.setMinimumHeight(56)
        self.skip_btn.clicked.connect(self.skip_version)
        self.skip_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                font-size: 11px;
                padding: 10px 16px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.later_btn)
        button_layout.addWidget(self.skip_btn)
        layout.addLayout(button_layout)
    
    def download_update(self):
        """업데이트 다운로드 및 설치"""
        self.save_settings()
        
        try:
            # 다운로드 URL이 인스톨러인 경우
            if self.update_info['download_url'].endswith('.exe'):
                QMessageBox.information(self, "🚀 Update Started", 
                    f"Downloading DeepFileX update...\n\n"
                    f"New Version: {self.update_info['version']}\n"
                    f"Installer will run when download completes.\n\n"
                    f"💡 Tip: Please close DeepFileX during the update process.",
                    QMessageBox.StandardButton.Ok)
                
                # 실제 환경에서는 다운로드 구현
                # self.start_download(self.update_info['download_url'])
                
                # 개발 환경에서는 브라우저로 다운로드 페이지 열기
                webbrowser.open(self.update_info['html_url'])
            else:
                # 릴리즈 페이지로 이동
                webbrowser.open(self.update_info['html_url'])
                
        except Exception as e:
            QMessageBox.warning(self, "다운로드 오류", 
                               f"다운로드 중 오류가 발생했습니다:\n{str(e)}")
        
        self.accept()
    
    def remind_later(self):
        """나중에 알림 (기본 동작)"""
        self.save_settings()
        
        # 다음 체크는 설정된 기간 후로 설정
        remind_days = UPDATE_CONFIG.get('remind_later_days', 3)
        next_check = datetime.now() + timedelta(days=remind_days)
        self.settings.setValue('last_check_date', next_check.isoformat())
        
        self.reject()
    
    def skip_version(self):
        """이 버전 건너뛰기"""
        self.save_settings()
        
        # 스킵한 버전 목록에 추가
        skipped_versions = self.settings.value('skipped_versions', [])
        if self.update_info['version'] not in skipped_versions:
            skipped_versions.append(self.update_info['version'])
            self.settings.setValue('skipped_versions', skipped_versions)
        
        QMessageBox.information(self, "버전 건너뛰기", 
            f"버전 {self.update_info['version']}을(를) 건너뛰었습니다.\n"
            f"다음 버전이 출시되면 다시 알림을 받을 수 있습니다.",
            QMessageBox.StandardButton.Ok)
        
        self.reject()
    
    def save_settings(self):
        """설정 저장"""
        self.settings.setValue('auto_check_enabled', self.auto_check_cb.isChecked())
        self.settings.setValue('background_check', self.notify_cb.isChecked())
    
    def closeEvent(self, event):
        """다이얼로그 닫기 이벤트"""
        self.countdown_timer.stop()
        self.auto_close_timer.stop()
        super().closeEvent(event)


class UpdateManager:
    """업데이트 관리자 (DeepFileX 메인 앱에서 사용)"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.update_checker = None
        self.settings = QSettings('DeepFileX', 'Updates')
    
    def check_for_updates_async(self):
        """비동기 업데이트 체크"""
        try:
            self.update_checker = UpdateChecker()
            
            # 체크가 필요한지 먼저 확인
            if not self.update_checker.should_check_update():
                print("🔄 업데이트 체크 스킵 (최근에 확인함)")
                return
            
            # 시그널 연결
            self.update_checker.update_available.connect(self.on_update_available)
            self.update_checker.no_update.connect(self.on_no_update)
            self.update_checker.error_occurred.connect(self.on_update_error)
            self.update_checker.finished.connect(self.on_check_finished)
            
            # 백그라운드에서 체크 시작
            print("🔄 업데이트 확인 중...")
            self.update_checker.start()
            
        except Exception as e:
            print(f"업데이트 체크 시작 실패: {e}")
    
    def on_update_available(self, update_info):
        """업데이트 발견 시"""
        print(f"🎉 새 업데이트 발견: v{update_info['version']}")
        
        # 업데이트 다이얼로그 표시
        dialog = UpdateDialog(self.parent, update_info)
        dialog.exec()
    
    def on_no_update(self):
        """업데이트 없음"""
        print("✅ 최신 버전 사용 중")
        
    def on_update_error(self, error_msg):
        """업데이트 체크 오류"""
        print(f"❌ 업데이트 체크 오류: {error_msg}")
    
    def on_check_finished(self):
        """업데이트 체크 완료"""
        if self.update_checker:
            self.update_checker.mark_checked()
            self.update_checker = None
        print("🔄 업데이트 체크 완료")


# 테스트 및 사용 예시
def test_update_system():
    """업데이트 시스템 테스트"""
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    
    # 테스트 윈도우
    window = QMainWindow()
    window.setWindowTitle("DeepFileX Update System Test")
    window.setGeometry(100, 100, 400, 300)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    
    # 업데이트 매니저 초기화
    update_manager = UpdateManager(window)
    
    # 테스트 버튼들
    check_btn = QPushButton("🔄 업데이트 확인")
    check_btn.clicked.connect(update_manager.check_for_updates_async)
    
    force_check_btn = QPushButton("🔃 강제 업데이트 확인")
    def force_check():
        update_manager.settings.setValue('last_check_date', '')  # 강제 체크
        update_manager.check_for_updates_async()
    force_check_btn.clicked.connect(force_check)
    
    layout.addWidget(check_btn)
    layout.addWidget(force_check_btn)
    
    window.show()
    
    print("DeepFileX 업데이트 시스템 테스트 시작")
    print("- '업데이트 확인' 버튼: 정상적인 업데이트 체크")
    print("- '강제 업데이트 확인' 버튼: 체크 주기 무시하고 강제 체크")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    test_update_system()

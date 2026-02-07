#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX 버전 정보 및 업데이트 설정
메인 애플리케이션과 업데이트 시스템에서 공통으로 사용하는 버전 정보

Created: 2025-08-28
Author: QuantumLayer
License: MIT
"""

from datetime import datetime

# 🎯 현재 버전 정보
VERSION = "1.3.0"
VERSION_CODE = 130  # 숫자 버전 (비교용)
BUILD_DATE = "2025-08-28"
BUILD_TIME = "17:30:00"
BUILD_TIMESTAMP = datetime(2025, 8, 28, 17, 30, 0)

# 📋 버전 히스토리
VERSION_HISTORY = {
    "1.3.0": {
        "date": "2025-08-28",
        "features": [
            "SmartLinks 수익화 시스템 완전 통합",
            "세련된 사진 형식 광고 배너",
            "컨텍스트별 스마트 광고 시스템",
            "자동 업데이트 시스템 추가",
            "실제 수익 달성 ($0.001+)",
            "사용자 경험 최적화"
        ],
        "fixes": [
            "광고 클릭 영역 확대 (배너 전체)",
            "메모리 사용량 최적화",
            "UI 안정성 향상"
        ]
    },
    "1.2.0": {
        "date": "2025-08-27", 
        "features": [
            "Everything-style 인스톨러 완성",
            "Adsterra SmartLinks 시스템 구축",
            "프로젝트 구조 정리 및 최적화",
            "수익 추적 시스템 구현"
        ],
        "fixes": [
            "빌드 시스템 최적화",
            "불필요한 파일 정리",
            "성능 개선"
        ]
    }
}

# 🔄 업데이트 시스템 설정
UPDATE_CONFIG = {
    # GitHub 릴리즈 정보
    "check_url": "https://api.github.com/repos/quantumlayer/deepfilex/releases/latest",
    "download_base_url": "https://github.com/quantumlayer/deepfilex/releases/download/",
    "releases_page_url": "https://github.com/quantumlayer/deepfilex/releases",
    
    # 업데이트 확인 설정
    "auto_check_enabled": True,
    "check_interval_days": 7,  # 기본 7일마다 확인
    "background_check": True,
    "startup_delay_seconds": 5,  # 앱 시작 후 5초 뒤에 체크
    
    # 알림 설정
    "auto_close_seconds": 30,  # 30초 후 자동으로 "나중에"로 설정
    "remind_later_days": 3,    # "나중에" 선택 시 3일 후 다시 알림
    
    # 개발/테스트 모드
    "test_mode": True,  # 개발용: 테스트 데이터 사용 (GitHub API 호출 방지)
    "test_version": "1.4.0",
    "force_update_check": False  # True면 체크 주기 무시
}

# 🔷 DeepFileX Update Messages
UPDATE_MESSAGES = {
    "update_available": "🔷 New version available!",
    "download_update": "🚀 Update Now",
    "remind_later": "⏰ Remind Later",
    "skip_version": "🚫 Skip Version",
    "checking": "🔄 Checking for updates...",
    "up_to_date": "✅ You're using the latest version",
    "check_failed": "❌ Update check failed",
    "download_complete": "📥 Update downloaded successfully",
    "install_ready": "🔷 Update ready - restart required"
}

# 🎯 SmartLinks 수익화 정보 (관련 버전 정보)
MONETIZATION_CONFIG = {
    "smartlinks_integrated_version": "1.3.0",
    "first_revenue_date": "2025-08-28",
    "first_revenue_amount": 0.001,
    "adsterra_smartlink_id": "27417447",
    "revenue_tracking_enabled": True
}

# 🚀 성능 및 시스템 정보
SYSTEM_REQUIREMENTS = {
    "min_python_version": "3.8.0",
    "recommended_python_version": "3.11.0",
    "required_packages": [
        "PyQt6>=6.4.0",
        "PyQt6-WebEngine>=6.4.0", 
        "sqlite3",  # Built-in
        "requests>=2.28.0",
        "chardet>=5.0.0",
    ],
    "optional_packages": [
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0", 
        "python-docx>=0.8.11",
        "openpyxl>=3.1.0",
        "python-pptx>=0.6.21"
    ],
    "min_ram_mb": 512,
    "recommended_ram_mb": 2048,
    "min_disk_space_mb": 100,
    "supported_os": ["Windows 10", "Windows 11"],
    "supported_architectures": ["x86_64"]
}

# 📊 릴리즈 통계
RELEASE_STATS = {
    "total_releases": 3,
    "stable_releases": 2, 
    "beta_releases": 1,
    "download_count": 0,  # GitHub에서 집계
    "active_users_estimate": 500,
    "first_release_date": "2025-08-26",
    "latest_release_date": BUILD_DATE
}

# 🛠️ 개발자 정보
DEVELOPER_INFO = {
    "company": "QuantumLayer",
    "team": "DeepFileX Team",
    "lead_developer": "QuantumLayer",
    "contact_email": "contact@quantumlayer.com",
    "github_repo": "https://github.com/quantumlayer/deepfilex",
    "license": "MIT License",
    "copyright": f"© 2025-2026 QuantumLayer. All rights reserved."
}

def get_version_info():
    """현재 버전의 전체 정보를 반환"""
    return {
        "version": VERSION,
        "version_code": VERSION_CODE,
        "build_date": BUILD_DATE,
        "build_time": BUILD_TIME,
        "build_timestamp": BUILD_TIMESTAMP.isoformat(),
        "is_beta": "beta" in VERSION.lower(),
        "is_stable": "beta" not in VERSION.lower(),
        "update_config": UPDATE_CONFIG,
        "system_requirements": SYSTEM_REQUIREMENTS,
        "developer_info": DEVELOPER_INFO
    }

def get_version_string():
    """버전 문자열을 반환 (UI 표시용)"""
    beta_suffix = "-beta" if "beta" not in VERSION else ""
    return f"DeepFileX v{VERSION}{beta_suffix}"

def get_build_info():
    """빌드 정보를 반환"""
    return f"Built on {BUILD_DATE} at {BUILD_TIME}"

def is_newer_version(other_version: str) -> bool:
    """다른 버전이 현재 버전보다 새로운지 확인"""
    try:
        # 버전 문자열을 숫자 리스트로 변환
        current_parts = [int(x) for x in VERSION.split('.')]
        other_parts = [int(x) for x in other_version.split('.')]
        
        # 길이 맞춤
        max_len = max(len(current_parts), len(other_parts))
        current_parts.extend([0] * (max_len - len(current_parts)))
        other_parts.extend([0] * (max_len - len(other_parts)))
        
        return other_parts > current_parts
    except (ValueError, AttributeError):
        return False

def get_changelog(version: str = None):
    """특정 버전의 변경사항을 반환"""
    if version is None:
        version = VERSION
    
    changelog = VERSION_HISTORY.get(version, {})
    if not changelog:
        return "변경사항 정보가 없습니다."
    
    features = changelog.get('features', [])
    fixes = changelog.get('fixes', [])
    
    changelog_text = f"DeepFileX v{version} ({changelog.get('date', 'Unknown')})\n\n"
    
    if features:
        changelog_text += "🎉 새로운 기능:\n"
        for feature in features:
            changelog_text += f"• {feature}\n"
        changelog_text += "\n"
    
    if fixes:
        changelog_text += "🔧 개선사항 및 버그 수정:\n"
        for fix in fixes:
            changelog_text += f"• {fix}\n"
    
    return changelog_text

def get_update_test_data():
    """업데이트 테스트용 가짜 데이터 생성"""
    if not UPDATE_CONFIG.get("test_mode", False):
        return None
    
    test_version = UPDATE_CONFIG.get("test_version", "1.4.0")
    
    return {
        'tag_name': f'v{test_version}',
        'name': f'DeepFileX v{test_version} - 대형 업데이트',
        'body': f"""🎉 주요 개선사항:
• 🚀 파일 스캔 속도 50% 향상
• 📁 새로운 파일 형식 지원 (ZIP, RAR, 7Z)
• 🎨 UI/UX 대폭 개선 및 다크모드 최적화
• 🔍 고급 검색 필터 추가
• 🛡️ 보안 강화 및 버그 수정

💰 SmartLinks 수익화 개선:
• 광고 클릭률 30% 향상된 새로운 배너 디자인
• 컨텍스트 기반 스마트 광고 타겟팅
• 수익 통계 대시보드 추가

🔷 UI/UX 개선:
• 모던한 인터페이스 디자인 적용
• 사용자 경험 최적화
• 다크 모드 완성도 향상

🔄 업데이트 시스템:
• 자동 업데이트 확인 및 알림
• 사용자 친화적 업데이트 다이얼로그
• 백그라운드 업데이트 체크

📊 성능 최적화:
• 메모리 사용량 20% 감소
• 인덱싱 속도 향상
• 안정성 개선""",
        'assets': [
            {
                'name': f'DeepFileX_v{test_version}_Setup.exe',
                'browser_download_url': f'https://github.com/quantumlayer/deepfilex/releases/download/v{test_version}/DeepFileX_v{test_version}_Setup.exe'
            }
        ],
        'published_at': '2025-08-29T10:00:00Z',
        'html_url': f'https://github.com/quantumlayer/deepfilex/releases/tag/v{test_version}'
    }

# 🧪 테스트 및 디버깅용 함수
def print_version_info():
    """버전 정보를 콘솔에 출력 (디버깅용)"""
    print(f"=== {get_version_string()} ===")
    print(get_build_info())
    print(f"Version Code: {VERSION_CODE}")
    print(f"Update Check: {'Enabled' if UPDATE_CONFIG['auto_check_enabled'] else 'Disabled'}")
    print(f"Test Mode: {'ON' if UPDATE_CONFIG['test_mode'] else 'OFF'}")
    print(f"SmartLinks Integrated: {MONETIZATION_CONFIG['smartlinks_integrated_version']}")
    print(f"First Revenue: ${MONETIZATION_CONFIG['first_revenue_amount']}")

if __name__ == "__main__":
    # 테스트 실행
    print_version_info()
    print("\n" + "="*50)
    print(get_changelog())
    
    # 버전 비교 테스트
    test_versions = ["1.2.0", "1.3.0", "1.3.1", "1.4.0", "2.0.0"]
    print(f"\n현재 버전: {VERSION}")
    for test_ver in test_versions:
        is_newer = is_newer_version(test_ver)
        print(f"{test_ver}: {'🆕 새 버전' if is_newer else '🔄 동일/이전 버전'}")

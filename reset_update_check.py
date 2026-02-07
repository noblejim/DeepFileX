#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepFileX 업데이트 체크 설정 초기화
팝업창 테스트를 위한 QSettings 초기화 스크립트
"""

from PyQt6.QtCore import QSettings
import sys
import io

# UTF-8 출력 설정
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# DeepFileX 업데이트 설정 초기화
settings = QSettings('DeepFileX', 'Updates')
settings.clear()
print("DeepFileX update settings cleared")
print("Update popup will now show on next program launch")

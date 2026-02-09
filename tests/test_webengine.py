#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QWebEngine DLL 문제 진단 스크립트
"""

import sys
import os

# UTF-8 encoding 설정
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print()

# PyQt6 경로 확인
try:
    import PyQt6
    print("[OK] PyQt6 imported successfully")
    print("PyQt6 path:", PyQt6.__file__)
except Exception as e:
    print("[FAIL] PyQt6 import failed:", e)
    sys.exit(1)

# Qt6 바이너리 경로 추가
from pathlib import Path
qt_bin_path = Path(PyQt6.__file__).parent / 'Qt6' / 'bin'
if qt_bin_path.exists():
    print(f"[OK] Qt6 bin path exists: {qt_bin_path}")
    os.environ['PATH'] = str(qt_bin_path) + os.pathsep + os.environ.get('PATH', '')
    print("[OK] Added Qt6 bin to PATH")
else:
    print(f"[FAIL] Qt6 bin path not found: {qt_bin_path}")

print()

# QtWebEngineWidgets import 시도
try:
    print("Attempting to import QtWebEngineWidgets...")
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    print("[OK] QWebEngineView imported successfully!")
    print("QWebEngineView class:", QWebEngineView)
except ImportError as e:
    print("[FAIL] ImportError:", e)
    print("\n상세 에러 정보:")
    import traceback
    traceback.print_exc()
except OSError as e:
    print("[FAIL] OSError (DLL load failed):", e)
    print("\n상세 에러 정보:")
    import traceback
    traceback.print_exc()
except Exception as e:
    print("[FAIL] Unexpected error:", type(e).__name__, e)
    print("\n상세 에러 정보:")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("진단 완료")

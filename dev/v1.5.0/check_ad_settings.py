#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""광고 배너 설정 확인 스크립트"""

from PyQt6.QtCore import QSettings

print("=" * 60)
print("DeepFileX Ad Settings Check")
print("=" * 60)

settings = QSettings('DeepFileX', 'SmartLinks')

# 광고 설정 확인
ads_enabled = settings.value('ads_enabled', True, type=bool)
is_premium = settings.value('is_premium', False, type=bool)

print(f"\nAds Enabled: {ads_enabled}")
print(f"Is Premium: {is_premium}")
print()

if not ads_enabled:
    print("⚠️ WARNING: Ads are disabled!")
    print("Solution: Run the following to enable ads:")
    print('  settings.setValue("ads_enabled", True)')

if is_premium:
    print("⚠️ WARNING: Premium mode is enabled!")
    print("Solution: Run the following to disable premium:")
    print('  settings.setValue("is_premium", False)')

if ads_enabled and not is_premium:
    print("✅ Ads should be visible!")
else:
    print("\n🔧 Fix needed - Run this script to fix:")
    print()
    print("from PyQt6.QtCore import QSettings")
    print("settings = QSettings('DeepFileX', 'SmartLinks')")
    print("settings.setValue('ads_enabled', True)")
    print("settings.setValue('is_premium', False)")

print("=" * 60)

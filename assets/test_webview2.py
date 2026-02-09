#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebView2 간단 테스트
"""

import webview
import sys

# 간단한 HTML 테스트
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .content {
            text-align: center;
            color: white;
        }
        h1 { font-size: 32px; margin-bottom: 20px; }
        p { font-size: 18px; }
    </style>
</head>
<body>
    <div class="content">
        <h1>✅ WebView2 작동 성공!</h1>
        <p>DeepFileX 광고 배너 테스트</p>
        <p>이 창이 보인다면 WebView2가 정상 작동합니다</p>
    </div>
</body>
</html>
"""

def test_webview():
    """WebView2 테스트"""
    print("WebView2 테스트 시작...")
    print("창이 열리면 성공입니다!")

    # WebView 창 생성
    window = webview.create_window(
        'WebView2 Test',
        html=html_content,
        width=600,
        height=400
    )

    webview.start()
    print("WebView2 테스트 완료!")

if __name__ == "__main__":
    test_webview()

# -*- coding: utf-8 -*-
"""
인덱스 파일명 생성 모듈 (v1.5.0)

목표 형식: YYMMDD_HHMM_폴더명.pkl
예시: 260209_1759_내문서.pkl
"""

import os
from datetime import datetime


def generate_index_filename_v15(folder_paths):
    """
    v1.5.0 새로운 파일명 규칙
    
    형식: YYMMDD_HHMM_폴더명.pkl
    
    Args:
        folder_paths: 스캔한 폴더 경로 리스트
        
    Returns:
        str: 생성된 파일명 (예: "260209_1759_내문서.pkl")
    """
    # 타임스탬프 생성
    timestamp = datetime.now().strftime('%y%m%d_%H%M')
    
    # 폴더명 추출
    folder_name = extract_primary_folder_name(folder_paths)
    
    # 파일명 조합
    if folder_name:
        filename = f"{timestamp}_{folder_name}.pkl"
    else:
        filename = f"{timestamp}.pkl"
    
    return filename


def extract_primary_folder_name(folder_paths):
    """첫 번째 폴더의 이름을 추출하고 안전하게 처리"""
    if not folder_paths:
        return ""
    
    # 첫 번째 폴더 경로 사용
    primary_path = folder_paths[0]
    folder_name = os.path.basename(os.path.normpath(primary_path))
    
    # 안전한 파일명으로 변환
    safe_name = make_filename_safe_v15(folder_name)
    return safe_name



def make_filename_safe_v15(name):
    """파일명을 안전하게 처리 (한글 완전 지원)"""
    if not name:
        return ""
    
    # Windows 파일명 금지 문자 제거
    invalid_chars = '<>:"/\\|?*'
    safe_name = name
    
    for char in invalid_chars:
        safe_name = safe_name.replace(char, "")
    
    # 공백을 언더스코어로 변환
    safe_name = safe_name.replace(" ", "_")
    safe_name = safe_name.replace(".", "_")
    
    # 연속된 언더스코어 제거
    while "__" in safe_name:
        safe_name = safe_name.replace("__", "_")
    
    # 앞뒤 언더스코어 제거
    safe_name = safe_name.strip("_")
    
    # 길이 제한 (20자)
    if len(safe_name) > 20:
        safe_name = safe_name[:20]
    
    return safe_name



# 테스트 코드
if __name__ == "__main__":
    print("=" * 60)
    print("Index Filename Generator Test (v1.5.0)")
    print("=" * 60)
    print()
    
    # 테스트 케이스
    test_cases = [
        ([r"C:\Users\User\Documents"], "영문 폴더"),
        ([r"C:\Users\User\내 문서"], "한글 폴더 (공백 포함)"),
        ([r"C:\Users\User\Downloads"], "다운로드"),
        ([r"D:\Projects\DeepFileX"], "프로젝트"),
        ([r"C:\사용자\문서\프로젝트"], "한글 경로"),
        ([r"C:\Users\User\My Documents"], "공백 포함 폴더"),
        ([r"C:\Users\User\test<>:file"], "특수문자 폴더"),
        ([r"C:\Users\User\VeryLongFolderNameThatExceedsLimit"], "긴 폴더명"),
    ]
    
    print("Test Results:")
    print("-" * 60)
    for paths, desc in test_cases:
        filename = generate_index_filename_v15(paths)
        print(f"{desc:25} -> {filename}")
    
    print()
    print("=" * 60)
    
    # 현재 시간 표시
    now = datetime.now()
    print(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Timestamp: {now.strftime('%y%m%d_%H%M')}")
    print()
    
    # 비교: 기존 방식 vs 새 방식
    print("Comparison:")
    print("-" * 60)
    old_format = f"deepfilex_index_Documents_{now.strftime('%Y%m%d_%H%M%S')}.pkl"
    new_format = generate_index_filename_v15([r"C:\Users\User\Documents"])
    
    print(f"Old: {old_format}")
    print(f"     Length: {len(old_format)} chars")
    print()
    print(f"New: {new_format}")
    print(f"     Length: {len(new_format)} chars")
    reduction = len(old_format) - len(new_format)
    percent = (reduction / len(old_format) * 100)
    print(f"     Saved: {reduction} chars ({percent:.1f}%)")
    print()
    print("Test Complete!")

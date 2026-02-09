# -*- coding: utf-8 -*-
"""
인덱스 업데이트 모듈 (v1.5.0)

기능:
- 기존 인덱스 로드
- 변경 사항 감지 (추가/삭제/수정)
- 증분 업데이트
"""

import os
import pickle
from datetime import datetime
from pathlib import Path


class IndexUpdater:
    """인덱스 업데이트 관리 클래스"""
    
    def __init__(self, index_file):
        """
        Args:
            index_file: 업데이트할 인덱스 파일 경로
        """
        self.index_file = index_file
        self.old_index = None
        self.changes = {
            'added': [],
            'removed': [],
            'modified': [],
            'unchanged': []
        }
    
    
    def load_existing_index(self):
        """기존 인덱스 로드"""
        try:
            with open(self.index_file, 'rb') as f:
                self.old_index = pickle.load(f)
            print(f"Loaded index: {len(self.old_index.get('index_data', {}))} files")
            return True
        except Exception as e:
            print(f"Failed to load index: {e}")
            return False
    
    def scan_current_files(self, folder_paths):
        """현재 파일 시스템 스캔"""
        current_files = {}
        
        for folder in folder_paths:
            for root, dirs, files in os.walk(folder):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    
                    try:
                        # 파일 정보 수집
                        stat_info = os.stat(filepath)
                        current_files[filepath] = {
                            'size': stat_info.st_size,
                            'mtime': stat_info.st_mtime,
                            'path': filepath
                        }
                    except Exception as e:
                        print(f"Error scanning {filepath}: {e}")
        
        return current_files
    
    def detect_changes(self, current_files):
        """변경 사항 감지 (추가/삭제/수정)"""
        if not self.old_index:
            print("No old index loaded")
            return False
        
        old_files = set(self.old_index.get('index_data', {}).keys())
        new_files = set(current_files.keys())
        
        # 추가된 파일
        self.changes['added'] = list(new_files - old_files)
        
        # 삭제된 파일
        self.changes['removed'] = list(old_files - new_files)
        
        # 수정 여부 확인 (공통 파일)
        common_files = old_files & new_files
        
        for filepath in common_files:
            old_info = self.old_index['index_data'][filepath]
            new_info = current_files[filepath]
            
            # 크기 또는 수정 시간 변경 확인
            if (old_info.get('size') != new_info['size'] or 
                old_info.get('mtime') != new_info['mtime']):
                self.changes['modified'].append(filepath)
            else:
                self.changes['unchanged'].append(filepath)
        
        return True
    
    def update_index(self, current_files):
        """인덱스 업데이트"""
        # 기존 인덱스 데이터 복사
        updated_index = self.old_index.copy()
        
        # 삭제된 파일 제거
        for filepath in self.changes['removed']:
            if filepath in updated_index['index_data']:
                del updated_index['index_data'][filepath]
        
        # 추가된 파일 추가
        for filepath in self.changes['added']:
            updated_index['index_data'][filepath] = current_files[filepath]
        
        # 수정된 파일 업데이트
        for filepath in self.changes['modified']:
            updated_index['index_data'][filepath] = current_files[filepath]
        
        # 통계 업데이트
        updated_index['stats'] = {
            'total_files': len(updated_index['index_data']),
            'last_updated': datetime.now().isoformat()
        }
        
        return updated_index
    
    def save_index(self, updated_index):
        """업데이트된 인덱스 저장 (동일한 파일명)"""
        try:
            with open(self.index_file, 'wb') as f:
                pickle.dump(updated_index, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"Index updated and saved to {self.index_file}")
            return True
        except Exception as e:
            print(f"Failed to save index: {e}")
            return False
    
    def print_changes_summary(self):
        """변경 사항 요약 출력"""
        print("\n" + "=" * 60)
        print("Index Update Summary")
        print("=" * 60)
        print(f"Added:     {len(self.changes['added'])} files")
        print(f"Removed:   {len(self.changes['removed'])} files")
        print(f"Modified:  {len(self.changes['modified'])} files")
        print(f"Unchanged: {len(self.changes['unchanged'])} files")
        print("=" * 60)
        
        # 상세 출력 (처음 5개만)
        if self.changes['added']:
            print("\nAdded files (first 5):")
            for f in self.changes['added'][:5]:
                print(f"  + {f}")
        
        if self.changes['removed']:
            print("\nRemoved files (first 5):")
            for f in self.changes['removed'][:5]:
                print(f"  - {f}")
        
        if self.changes['modified']:
            print("\nModified files (first 5):")
            for f in self.changes['modified'][:5]:
                print(f"  * {f}")


def update_index_file(index_file, folder_paths):
    """인덱스 파일 업데이트 (메인 함수)"""
    updater = IndexUpdater(index_file)
    
    # 1. 기존 인덱스 로드
    print(f"Loading index: {index_file}")
    if not updater.load_existing_index():
        return False
    
    # 2. 현재 파일 스캔
    print("\nScanning current files...")
    current_files = updater.scan_current_files(folder_paths)
    print(f"Found {len(current_files)} files")
    
    # 3. 변경 사항 감지
    print("\nDetecting changes...")
    updater.detect_changes(current_files)
    updater.print_changes_summary()
    
    # 4. 인덱스 업데이트
    print("\nUpdating index...")
    updated_index = updater.update_index(current_files)
    
    # 5. 저장
    if updater.save_index(updated_index):
        print("\nUpdate complete!")
        return True
    else:
        print("\nUpdate failed!")
        return False


# 테스트 코드
if __name__ == "__main__":
    print("Index Updater Test (v1.5.0)")
    print("=" * 60)
    print()
    print("This module provides index update functionality.")
    print("Usage:")
    print("  from index_updater import update_index_file")
    print("  update_index_file('260209_1842_Documents.pkl', [r'C:\\Users\\Documents'])")
    print()

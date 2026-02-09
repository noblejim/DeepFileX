# -*- coding: utf-8 -*-
"""
인덱스 비교 모듈 (v1.5.0)

기능:
- 두 인덱스의 차이점 확인
- 추가/삭제/수정 파일 감지
- 통계 변화 분석
- 비교 리포트 생성
"""

import os
import pickle
from datetime import datetime
from pathlib import Path


class IndexComparator:
    """인덱스 비교 관리 클래스"""
    
    def __init__(self, index1_file, index2_file):
        """
        Args:
            index1_file: 첫 번째 인덱스 파일 (기준)
            index2_file: 두 번째 인덱스 파일 (비교 대상)
        """
        self.index1_file = index1_file
        self.index2_file = index2_file
        self.index1 = None
        self.index2 = None
        self.comparison = {
            'added': [],      # index2에만 있는 파일
            'removed': [],    # index1에만 있는 파일
            'modified': [],   # 둘 다 있지만 변경된 파일
            'unchanged': []   # 둘 다 있고 동일한 파일
        }
    
    def load_indexes(self):
        """두 인덱스 파일 로드"""
        try:
            # Index 1 로드
            with open(self.index1_file, 'rb') as f:
                self.index1 = pickle.load(f)
            print(f"Loaded index 1: {os.path.basename(self.index1_file)}")
            print(f"  Files: {len(self.index1.get('index_data', {}))}")
            
            # Index 2 로드
            with open(self.index2_file, 'rb') as f:
                self.index2 = pickle.load(f)
            print(f"Loaded index 2: {os.path.basename(self.index2_file)}")
            print(f"  Files: {len(self.index2.get('index_data', {}))}")
            
            return True
            
        except Exception as e:
            print(f"Failed to load indexes: {e}")
            return False
    
    def compare(self):
        """두 인덱스 비교"""
        if not self.index1 or not self.index2:
            print("Indexes not loaded")
            return False
        
        # 파일 경로 set으로 변환
        files1 = set(self.index1.get('index_data', {}).keys())
        files2 = set(self.index2.get('index_data', {}).keys())
        
        # 차집합으로 추가/삭제 감지
        self.comparison['added'] = list(files2 - files1)
        self.comparison['removed'] = list(files1 - files2)
        
        # 교집합으로 공통 파일 확인
        common_files = files1 & files2
        
        # 공통 파일 중 수정 여부 확인
        for filepath in common_files:
            info1 = self.index1['index_data'][filepath]
            info2 = self.index2['index_data'][filepath]
            
            # 크기 또는 수정 시간 비교
            if (info1.get('size') != info2.get('size') or
                info1.get('mtime') != info2.get('mtime')):
                self.comparison['modified'].append({
                    'path': filepath,
                    'old_size': info1.get('size'),
                    'new_size': info2.get('size'),
                    'old_mtime': info1.get('mtime'),
                    'new_mtime': info2.get('mtime')
                })
            else:
                self.comparison['unchanged'].append(filepath)
        
        return True
    
    def get_stats_comparison(self):
        """통계 비교"""
        stats1 = self.index1.get('stats', {})
        stats2 = self.index2.get('stats', {})
        
        return {
            'index1': {
                'files': stats1.get('total_files', len(self.index1.get('index_data', {}))),
                'size': stats1.get('total_size', 0)
            },
            'index2': {
                'files': stats2.get('total_files', len(self.index2.get('index_data', {}))),
                'size': stats2.get('total_size', 0)
            },
            'changes': {
                'added': len(self.comparison['added']),
                'removed': len(self.comparison['removed']),
                'modified': len(self.comparison['modified']),
                'unchanged': len(self.comparison['unchanged'])
            }
        }
    
    def print_comparison_summary(self):
        """비교 결과 요약 출력"""
        stats = self.get_stats_comparison()
        
        print("\n" + "=" * 60)
        print("Index Comparison Summary")
        print("=" * 60)
        print(f"\nIndex 1: {os.path.basename(self.index1_file)}")
        print(f"  Files: {stats['index1']['files']}")
        print(f"  Size:  {stats['index1']['size']:,} bytes")
        
        print(f"\nIndex 2: {os.path.basename(self.index2_file)}")
        print(f"  Files: {stats['index2']['files']}")
        print(f"  Size:  {stats['index2']['size']:,} bytes")
        
        print("\nChanges:")
        print(f"  + Added:    {stats['changes']['added']} files")
        print(f"  - Removed:  {stats['changes']['removed']} files")
        print(f"  * Modified: {stats['changes']['modified']} files")
        print(f"  = Unchanged: {stats['changes']['unchanged']} files")
        print("=" * 60)
        
        # 상세 출력 (처음 5개만)
        if self.comparison['added']:
            print("\nAdded files (first 5):")
            for f in self.comparison['added'][:5]:
                print(f"  + {f}")
        
        if self.comparison['removed']:
            print("\nRemoved files (first 5):")
            for f in self.comparison['removed'][:5]:
                print(f"  - {f}")
        
        if self.comparison['modified']:
            print("\nModified files (first 5):")
            for item in self.comparison['modified'][:5]:
                filepath = item['path']
                size_diff = item['new_size'] - item['old_size']
                print(f"  * {filepath}")
                print(f"    Size: {item['old_size']:,} -> {item['new_size']:,} ({size_diff:+,} bytes)")
    
    def generate_report(self, output_file=None):
        """비교 리포트 생성 (텍스트 파일)"""
        if not output_file:
            timestamp = datetime.now().strftime('%y%m%d_%H%M')
            output_file = f"comparison_report_{timestamp}.txt"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("Index Comparison Report\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"\nIndex 1: {self.index1_file}\n")
                f.write(f"Index 2: {self.index2_file}\n")
                f.write("\n")
                
                stats = self.get_stats_comparison()
                f.write("Statistics:\n")
                f.write(f"  Index 1: {stats['index1']['files']} files, {stats['index1']['size']:,} bytes\n")
                f.write(f"  Index 2: {stats['index2']['files']} files, {stats['index2']['size']:,} bytes\n")
                
                f.write("\nChanges:\n")
                f.write(f"  Added:    {len(self.comparison['added'])}\n")
                f.write(f"  Removed:  {len(self.comparison['removed'])}\n")
                f.write(f"  Modified: {len(self.comparison['modified'])}\n")
                f.write(f"  Unchanged: {len(self.comparison['unchanged'])}\n")
                f.write("\n")
                
                # 상세 목록
                if self.comparison['added']:
                    f.write("\nAdded Files:\n")
                    for filepath in self.comparison['added']:
                        f.write(f"  + {filepath}\n")
                
                if self.comparison['removed']:
                    f.write("\nRemoved Files:\n")
                    for filepath in self.comparison['removed']:
                        f.write(f"  - {filepath}\n")
                
                if self.comparison['modified']:
                    f.write("\nModified Files:\n")
                    for item in self.comparison['modified']:
                        f.write(f"  * {item['path']}\n")
                        f.write(f"    Size: {item['old_size']:,} -> {item['new_size']:,}\n")
            
            print(f"\nReport saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"Failed to generate report: {e}")
            return False


def compare_index_files(index1_file, index2_file, generate_report=False, output_file=None):
    """인덱스 파일 비교 (메인 함수)"""
    comparator = IndexComparator(index1_file, index2_file)

    # 1. 인덱스 로드
    print("Loading indexes...")
    if not comparator.load_indexes():
        return False

    # 2. 비교
    print("\nComparing indexes...")
    if not comparator.compare():
        return False

    # 3. 요약 출력
    comparator.print_comparison_summary()

    # 4. 리포트 생성 (선택사항)
    if generate_report:
        print("\nGenerating report...")
        comparator.generate_report(output_file)

    print("\nComparison complete!")
    return True


# 테스트 코드
if __name__ == "__main__":
    print("=" * 60)
    print("Index Comparator Test (v1.5.0)")
    print("=" * 60)
    print()
    print("This module provides index comparison functionality.")
    print()
    print("Usage:")
    print("  from index_comparator import compare_index_files")
    print()
    print("  # Compare two indexes")
    print("  compare_index_files(")
    print("      '260209_1842_Documents.pkl',")
    print("      '260209_1845_Documents.pkl'")
    print("  )")
    print()
    print("  # With report generation")
    print("  compare_index_files(")
    print("      '260209_1842_Documents.pkl',")
    print("      '260209_1845_Documents.pkl',")
    print("      generate_report=True")
    print("  )")
    print()

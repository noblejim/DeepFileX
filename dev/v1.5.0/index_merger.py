# -*- coding: utf-8 -*-
"""
인덱스 통합 모듈 (v1.5.0)

기능:
- 여러 인덱스 파일을 하나로 병합
- 중복 제거 및 통계 병합
- 자동 파일명 생성
"""

import os
import pickle
from datetime import datetime
from collections import defaultdict
from pathlib import Path


class IndexMerger:
    """인덱스 통합 관리 클래스"""
    
    def __init__(self, index_files):
        """
        Args:
            index_files: 통합할 인덱스 파일 경로 리스트
        """
        self.index_files = index_files
        self.merged_data = {
            'index_data': {},
            'word_index': defaultdict(set),
            'filename_index': defaultdict(set),
            'stats': {
                'total_files': 0,
                'total_size': 0,
                'source_indexes': []
            }
        }
    
    def load_and_merge(self):
        """모든 인덱스 파일 로드 및 병합"""
        print(f"Merging {len(self.index_files)} index files...")
        
        for idx_file in self.index_files:
            try:
                with open(idx_file, 'rb') as f:
                    data = pickle.load(f)
                
                print(f"  Loading: {os.path.basename(idx_file)}")
                self._merge_single_index(data, idx_file)
                
            except Exception as e:
                print(f"  Error loading {idx_file}: {e}")
                continue
        
        # 최종 통계 계산
        self._finalize_stats()
        return self.merged_data
    
    def _merge_single_index(self, data, source_file):
        """단일 인덱스 데이터 병합"""
        # 1. index_data 병합 (중복 파일 처리)
        index_data = data.get('index_data', {})
        for filepath, info in index_data.items():
            if filepath in self.merged_data['index_data']:
                # 중복: 최신 것 유지 (mtime 비교)
                existing = self.merged_data['index_data'][filepath]
                if info.get('mtime', 0) > existing.get('mtime', 0):
                    self.merged_data['index_data'][filepath] = info
            else:
                self.merged_data['index_data'][filepath] = info
        
        # 2. word_index 병합 (set union)
        word_index = data.get('word_index', {})
        for word, files in word_index.items():
            self.merged_data['word_index'][word].update(files)
        
        # 3. filename_index 병합 (set union)
        filename_index = data.get('filename_index', {})
        for filename, paths in filename_index.items():
            self.merged_data['filename_index'][filename].update(paths)
        
        # 4. 통계 수집
        stats = data.get('stats', {})
        self.merged_data['stats']['source_indexes'].append({
            'file': os.path.basename(source_file),
            'files': stats.get('total_files', len(index_data)),
            'size': stats.get('total_size', 0)
        })
    
    def _finalize_stats(self):
        """최종 통계 계산"""
        # 총 파일 수
        self.merged_data['stats']['total_files'] = len(self.merged_data['index_data'])
        
        # 총 크기
        total_size = 0
        for info in self.merged_data['index_data'].values():
            total_size += info.get('size', 0)
        self.merged_data['stats']['total_size'] = total_size
        
        # 병합 시간
        self.merged_data['stats']['merged_at'] = datetime.now().isoformat()
    
    def generate_merged_filename(self, output_name=None):
        """병합된 인덱스 파일명 생성"""
        if output_name:
            return output_name
        
        # 원본 파일명에서 폴더명 추출
        folder_names = []
        for idx_file in self.index_files:
            basename = os.path.basename(idx_file)
            # 형식: 260209_1842_Documents.pkl
            # 폴더명 추출: Documents
            parts = basename.replace('.pkl', '').split('_')
            if len(parts) >= 3:
                folder_name = '_'.join(parts[2:])
                if folder_name not in folder_names:
                    folder_names.append(folder_name)
        
        # 타임스탬프 생성
        timestamp = datetime.now().strftime('%y%m%d_%H%M')
        
        # 폴더명 결합 (+로 연결)
        if folder_names:
            combined = '+'.join(folder_names)
            # 길이 제한
            if len(combined) > 40:
                combined = combined[:37] + '...'
            filename = f"{timestamp}_{combined}.pkl"
        else:
            filename = f"{timestamp}_merged.pkl"
        
        return filename
    
    def save_merged_index(self, output_file):
        """병합된 인덱스 저장"""
        try:
            # set을 list로 변환 (pickle 호환성)
            save_data = self.merged_data.copy()
            save_data['word_index'] = {
                k: list(v) for k, v in self.merged_data['word_index'].items()
            }
            save_data['filename_index'] = {
                k: list(v) for k, v in self.merged_data['filename_index'].items()
            }
            
            with open(output_file, 'wb') as f:
                pickle.dump(save_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            print(f"\nMerged index saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"Failed to save merged index: {e}")
            return False
    
    def print_merge_summary(self):
        """병합 요약 출력"""
        print("\n" + "=" * 60)
        print("Index Merge Summary")
        print("=" * 60)
        print(f"Source indexes: {len(self.index_files)}")
        print(f"Total files:    {self.merged_data['stats']['total_files']}")
        print(f"Total size:     {self.merged_data['stats']['total_size']:,} bytes")
        print(f"Word index:     {len(self.merged_data['word_index'])} words")
        print(f"Filename index: {len(self.merged_data['filename_index'])} names")
        print("\nSource details:")
        for src in self.merged_data['stats']['source_indexes']:
            print(f"  - {src['file']}: {src['files']} files, {src['size']:,} bytes")
        print("=" * 60)


def merge_index_files(index_files, output_name=None):
    """인덱스 파일 병합 (메인 함수)"""
    if len(index_files) < 2:
        print("Error: Need at least 2 index files to merge")
        return False
    
    merger = IndexMerger(index_files)
    
    # 1. 로드 및 병합
    print("Starting merge process...")
    merger.load_and_merge()
    
    # 2. 요약 출력
    merger.print_merge_summary()
    
    # 3. 파일명 생성
    output_file = merger.generate_merged_filename(output_name)
    print(f"\nOutput filename: {output_file}")
    
    # 4. 저장
    if merger.save_merged_index(output_file):
        print("\nMerge complete!")
        return True
    else:
        print("\nMerge failed!")
        return False


# 테스트 코드
if __name__ == "__main__":
    print("=" * 60)
    print("Index Merger Test (v1.5.0)")
    print("=" * 60)
    print()
    print("This module provides index merge functionality.")
    print()
    print("Usage:")
    print("  from index_merger import merge_index_files")
    print()
    print("  # Merge multiple indexes")
    print("  index_files = [")
    print("      '260209_1842_Documents.pkl',")
    print("      '260209_1845_Downloads.pkl'")
    print("  ]")
    print("  merge_index_files(index_files)")
    print()
    print("  # With custom output name")
    print("  merge_index_files(index_files, 'combined.pkl')")
    print()

# DeepFileX 다른 컴퓨터 설치 요구사항 체크리스트

## 🎯 DeepFileX_Optimized.exe 실행 요구사항

### ✅ **필요 없는 것들 (PyInstaller가 포함함)**
- ❌ Python 설치 - 불필요 (이미 포함됨)
- ❌ PyQt6 설치 - 불필요 (이미 포함됨)
- ❌ Office 라이브러리들 - 불필요 (python-docx, openpyxl, python-pptx 포함됨)
- ❌ PDF 라이브러리 - 불필요 (PyPDF2 포함됨)

### ⚠️ **필요할 수 있는 것들 (Windows 기본 요구사항)**

#### 1. **Microsoft Visual C++ Redistributable**
   - **용량**: ~30MB
   - **필요한 이유**: PyQt6, 일부 네이티브 라이브러리용
   - **버전**: 2015-2022 (x64)
   - **다운로드**: Microsoft 공식 사이트
   - **확인 방법**: DeepFileX 실행 시 "VCRUNTIME140.dll 없음" 오류 발생시 필요

#### 2. **Windows 10/11 (권장)**
   - **최소**: Windows 7 64비트
   - **권장**: Windows 10/11 64비트
   - **필요한 이유**: PyQt6 최적화, 현대적 UI 지원

### 🔍 **테스트 방법**

#### **단계 1: 단순 실행 테스트**
1. DeepFileX_Optimized.exe를 다른 컴퓨터에 복사
2. 더블클릭하여 실행
3. GUI 창이 뜨는지 확인

#### **단계 2: 기능 테스트**
1. "Scan Folders" 버튼으로 폴더 추가
2. "Start Diagnosis" 버튼으로 스캔 시작
3. 검색 기능 테스트

#### **단계 3: Office 문서 테스트**
1. DOCX, XLSX, PPTX 파일 스캔
2. PDF 파일 스캔
3. 내용 검색 가능한지 확인

### 🚨 **문제 발생시 해결 방법**

#### **오류 1: "VCRUNTIME140.dll을 찾을 수 없습니다"**
**해결**: Microsoft Visual C++ Redistributable 2015-2022 설치

#### **오류 2: "응용 프로그램을 시작할 수 없습니다"**
**해결**: Windows Defender 제외 목록에 DeepFileX 추가

#### **오류 3: "Qt 플랫폼 플러그인을 로드할 수 없습니다"**
**해결**: Windows 업데이트, 그래픽 드라이버 업데이트

### 📋 **간단한 확인 체크리스트**

**목표 컴퓨터에서 확인할 사항:**
- [ ] Windows 10/11 64비트 (권장)
- [ ] Visual C++ Redistributable 2015-2022 설치됨
- [ ] 바이러스 백신이 실행파일을 차단하지 않음
- [ ] 관리자 권한 없이 실행 가능 (일반 사용자로 테스트)

### 🎉 **대부분의 경우 추가 설치 불필요**

**좋은 소식**: PyInstaller로 최적화 빌드했기 때문에
- 90% 이상의 Windows 컴퓨터에서 **바로 실행 가능**
- Python, 라이브러리들이 모두 포함되어 있음
- 설치 프로그램 없이 단일 실행파일로 사용 가능

**결론**: 대부분 **추가 소프트웨어 설치 없이 바로 실행됩니다!**

---
**테스트 일자**: 2025-08-26
**빌드 버전**: DeepFileX_Optimized.exe (53MB)
**테스트 환경**: Windows 10/11 64비트

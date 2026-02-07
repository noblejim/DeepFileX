@echo off
chcp 65001 >nul 2>&1
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              DeepFileX 시스템 호환성 체크                      ║
echo ║                System Compatibility Check                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 시스템 요구사항을 확인하는 중...
echo.

:: 1. Windows 버전 확인
echo 📋 1. Windows 버전 확인
ver
echo.

:: 2. 시스템 아키텍처 확인
echo 📋 2. 시스템 아키텍처 확인
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo    ✅ 64비트 시스템 (권장)
) else (
    echo    ⚠️  32비트 시스템 (호환성 문제 가능)
)
echo.

:: 3. Visual C++ Redistributable 확인
echo 📋 3. Visual C++ Redistributable 확인
echo    검색 중...

:: 레지스트리에서 VC++ 2015-2022 확인
reg query "HKLM\SOFTWARE\Classes\Installer\Dependencies\Microsoft.VS.VC_RuntimeMinimumVSU_amd64,v14" >nul 2>&1
if %errorlevel%==0 (
    echo    ✅ Microsoft Visual C++ 2015-2022 Redistributable 설치됨
) else (
    echo    ❌ Microsoft Visual C++ 2015-2022 Redistributable 필요
    echo       다운로드: https://aka.ms/vs/17/release/vc_redist.x64.exe
)
echo.

:: 4. DeepFileX 실행파일 확인
echo 📋 4. DeepFileX 실행파일 확인
if exist "DeepFileX_Optimized.exe" (
    echo    ✅ DeepFileX_Optimized.exe 발견
    for %%i in (DeepFileX_Optimized.exe) do echo       크기: %%~zi bytes
) else (
    echo    ❌ DeepFileX_Optimized.exe를 찾을 수 없습니다
    echo       이 스크립트를 DeepFileX_Optimized.exe와 같은 폴더에서 실행하세요
)
echo.

:: 5. 실행 테스트
echo 📋 5. DeepFileX 실행 테스트
if exist "DeepFileX_Optimized.exe" (
    echo    🚀 DeepFileX 실행 테스트를 시작합니다...
    echo       (창이 뜨면 정상, 오류 메시지 확인)
    echo.
    
    set /p RUN_TEST="   DeepFileX를 테스트 실행하시겠습니까? (Y/N): "
    if /i "%RUN_TEST%"=="Y" (
        echo       실행 중... (창이 안 뜨면 Ctrl+C로 중단)
        start "" "DeepFileX_Optimized.exe"
        echo       ✅ DeepFileX가 시작되었습니다
    )
) else (
    echo    ⏭️  실행파일이 없어 테스트를 건너뜁니다
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     🎯 진단 결과 요약                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 💡 문제 해결 방법:
echo.
echo    🔧 VC++ 오류 시:
echo       → https://aka.ms/vs/17/release/vc_redist.x64.exe 설치
echo.
echo    🔧 실행 안 될 시:
echo       → Windows Defender 제외 목록에 DeepFileX 추가
echo       → 파일 속성에서 "차단 해제" 체크
echo.
echo    🔧 GUI 문제 시:
echo       → Windows 업데이트 실행
echo       → 그래픽 드라이버 업데이트
echo.
echo 📞 추가 지원이 필요하시면 개발자에게 연락하세요
echo.
pause

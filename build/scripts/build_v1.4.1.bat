@echo off
REM DeepFileX v1.4.1 Build Script
REM Search Crash Bug Fix Release
REM Date: 2026-02-09

echo ============================================================
echo DeepFileX v1.4.1 Build Script
echo ============================================================
echo.

REM Change to project root directory (2 levels up from build/scripts/)
cd /d "%~dp0..\.."

echo [1/5] Cleaning previous builds...
if exist "build\temp\dist" rmdir /s /q "build\temp\dist"
if exist "build\temp\build_artifacts" rmdir /s /q "build\temp\build_artifacts"
echo Done.
echo.

echo [2/5] Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo Done.
echo.

echo [3/5] Installing/Updating dependencies...
pip install --upgrade pyinstaller
pip install --upgrade PyQt6 PyQt6-WebEngine
echo Done.
echo.

echo [4/5] Building executable with PyInstaller...
pyinstaller build\specs\DeepFileX_v1.4.1.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo Done.
echo.

echo [5/5] Organizing release files...
REM Move build artifacts to temp folder
if not exist "build\temp\dist" mkdir "build\temp\dist"
if exist "dist" move /Y "dist" "build\temp\dist_temp" && move /Y "build\temp\dist_temp\*" "build\temp\dist" && rmdir "build\temp\dist_temp"
if exist "build\DeepFileX_v1.4.1" mkdir "build\temp\build_artifacts" && move /Y "build\DeepFileX_v1.4.1" "build\temp\build_artifacts\"

REM Copy to releases folder
if not exist "releases\v1.4.1" mkdir "releases\v1.4.1"
copy "build\temp\dist\DeepFileX.exe" "releases\v1.4.1\DeepFileX_v1.4.1.exe"
echo Done.
echo.

echo ============================================================
echo Build Complete!
echo ============================================================
echo.
echo Output: releases\v1.4.1\DeepFileX_v1.4.1.exe
echo.
echo Next steps:
echo 1. Test the executable
echo 2. Create GitHub release
echo 3. Upload DeepFileX_v1.4.1.exe
echo.

pause

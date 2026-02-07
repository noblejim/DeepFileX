@echo off
chcp 65001 >nul
echo ========================================
echo DeepFileX - Starting Application
echo ========================================

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo Checking required packages...
python -c "import PyQt6; print('PyQt6: OK')"
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo Starting DeepFileX - Advanced File Analysis System...
cd /d "%~dp0.."
python src\filemri.py

echo.
echo Application closed.
pause

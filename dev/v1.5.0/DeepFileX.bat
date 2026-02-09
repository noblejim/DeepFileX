@echo off
chcp 65001 >nul

REM Get the directory where this script is located
set "APP_DIR=%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Running setup...
    call "%APP_DIR%setup_python.bat"
    if %errorlevel% neq 0 (
        echo Setup failed. Please install Python manually.
        pause
        exit /b 1
    )
)

REM Change to app directory and run DeepFileX
cd /d "%APP_DIR%.."
python src\deepfilex.py

REM If there's an error, show it and pause
if %errorlevel% neq 0 (
    echo.
    echo DeepFileX exited with error code: %errorlevel%
    echo Check the error messages above.
    pause
)

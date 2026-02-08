@echo off
echo ============================================================
echo    Animal Classification AI - Starting Application
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [INFO] Checking dependencies...
pip show gradio >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo [INFO] Starting application...
echo [INFO] Visit: http://127.0.0.1:7860
echo [INFO] Press Ctrl+C to stop
echo ============================================================
echo.

python app.py
pause

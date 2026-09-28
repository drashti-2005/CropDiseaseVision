@echo off
REM CropDiseaseVision - Full Stack Startup (Windows)
REM Starts both backend (Flask) and frontend (HTTP Server)

cls
echo ============================================
echo CropDiseaseVision - Multilingual System
echo ============================================
echo.

set "PROJECT_DIR=%~dp0"
set "BACKEND_DIR=%PROJECT_DIR%backend"
set "FRONTEND_DIR=%PROJECT_DIR%frontend"

REM Check directories
if not exist "%BACKEND_DIR%" (
    echo ERROR: Backend directory not found!
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo ERROR: Frontend directory not found!
    pause
    exit /b 1
)

echo Starting Backend Server...
echo   Location: %BACKEND_DIR%
echo   Command: python app.py
echo.

REM Start backend
cd /d "%BACKEND_DIR%"
start "CropDiseaseVision - Backend" cmd /k python app.py

REM Wait for backend to start
timeout /t 3 /nobreak

echo.
echo Starting Frontend Server...
echo   Location: %FRONTEND_DIR%
echo   Command: python -m http.server 8000
echo.

REM Start frontend
cd /d "%FRONTEND_DIR%"
start "CropDiseaseVision - Frontend" cmd /k python -m http.server 8000

echo.
echo ============================================
echo SYSTEM RUNNING
echo ============================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Open in browser: http://localhost:8000
echo.
echo Press Ctrl+C in each terminal to stop
echo.

REM Open browser
timeout /t 2 /nobreak
start http://localhost:8000

pause

@echo off
REM CropDiseaseVision v2.0 - Quick Start Script for Windows

echo.
echo ============================================
echo  CropDiseaseVision v2.0 - Quick Start
echo ============================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    pip install -r backend/requirements.txt
    echo Dependencies installed!
)

echo.
echo ============================================
echo  Starting CropDiseaseVision Services
echo ============================================
echo.

REM Start backend in a new window
echo Starting Backend Server...
start "Backend - CropDiseaseVision" cmd /k "cd backend && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak

REM Start frontend in another new window
echo Starting Frontend Server...
start "Frontend - CropDiseaseVision" cmd /k "cd frontend && python -m http.server 8000"

echo.
echo ============================================
echo  Services Started!
echo ============================================
echo.
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:8000
echo.
echo Opening browser...
timeout /t 2 /nobreak
start http://localhost:8000

echo.
echo Press any key to continue...
pause

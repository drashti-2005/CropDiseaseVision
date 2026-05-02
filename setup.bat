@echo off
REM Setup script for CropDiseaseVision Multilingual System (Windows)
REM Batch file for Windows Command Prompt

setlocal enabledelayedexpansion

echo.
echo ====================================
echo CropDiseaseVision Multilingual Setup
echo ====================================
echo.

REM Check Python
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Backend Setup
echo [INFO] Setting up Backend...
cd backend

REM Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Install requirements
echo Installing dependencies (this may take a few minutes)...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1
python -m pip install -r requirements_multilingual.txt >nul 2>&1
echo [OK] Dependencies installed

REM Create .env from example
if not exist ".env" (
    echo Creating .env file from template...
    copy .\..\env.example .env >nul 2>&1
    echo [WARNING] Please edit backend\.env with your configuration
)

echo.
echo [OK] Backend setup complete!
echo.

REM Frontend Setup
echo [INFO] Setting up Frontend...
cd ..\frontend
echo [OK] Frontend ready (using vanilla JavaScript)
echo.

REM Summary
echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo [NEXT STEPS]
echo.
echo 1. Configure Backend (.env file)
echo    Edit: backend\.env
echo    Add API keys if needed
echo.
echo 2. Start Backend Server (in Command Prompt)
echo    cd backend
echo    .venv\Scripts\activate.bat
echo    python app.py
echo    Server will run on http://localhost:5000
echo.
echo 3. Start Frontend Server (in new Command Prompt)
echo    cd frontend
echo    python -m http.server 8000
echo    Frontend will run on http://localhost:8000
echo.
echo 4. Open Browser
echo    Navigate to http://localhost:8000
echo    Select language and start using!
echo.
echo [SUPPORTED BROWSERS]
echo   ✓ Chrome (Recommended for voice features)
echo   ✓ Edge
echo   ✓ Safari
echo   ✓ Opera
echo.
echo [SUPPORTED LANGUAGES]
echo   ✓ English
echo   ✓ Gujarati
echo   ✓ Hindi
echo   ✓ Marathi
echo   ✓ Tamil
echo   ✓ Telugu
echo.
echo [DOCUMENTATION]
echo   - See MULTILINGUAL_GUIDE.md for detailed setup
echo   - See README_MULTILINGUAL.md for features
echo   - See .env.example for configuration options
echo.
echo Happy Farming!
echo.
pause

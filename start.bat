@echo off
color 0A
echo ==========================================
echo    Plant Disease Detection System Startup  
echo ==========================================
echo.
echo Starting the AI Backend Server...
start "AI Backend Server" cmd /k "python -m uvicorn backend.app:app --port 8080"

echo Waiting for the server to load the AI model into memory (this takes a few seconds)...
timeout /t 5 /nobreak >nul

echo Opening the User Interface in your default browser...
start frontend\index.html

echo.
echo Done! You can now analyze leaf images in the browser.
echo (Keep the black command prompt window open while using the app)
echo.
pause

@echo off
echo ========================================
echo  Face Recognition Attendance System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Starting application...
echo.

REM Run the application
python face_recognition_ui.py

REM If there's an error, pause to see the message
if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error message above
    pause
)

@echo off
echo Starting Discord Music Bot with Hidden Defense System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Check if config file exists
if not exist "config.env" (
    echo.
    echo ERROR: config.env file not found!
    echo Please copy config.env.example to config.env and fill in your credentials.
    pause
    exit /b 1
)

REM Start the bot
echo.
echo Starting bot...
echo Press Ctrl+C to stop the bot
echo.
python main.py

pause

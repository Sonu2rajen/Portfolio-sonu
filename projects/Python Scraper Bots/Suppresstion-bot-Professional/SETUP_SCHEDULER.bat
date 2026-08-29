@echo off
:: ============================================================
::  SUPPRESSION MONITOR - WINDOWS TASK SCHEDULER SETUP
::  Run this ONCE to register the daily 7 AM task
:: ============================================================

echo.
echo  ===============================================
echo   SUPPRESSION MONITOR - SCHEDULER SETUP
echo  ===============================================
echo.

:: Set paths
set TASK_NAME=SuppressionMonitor_Clicktech
set PYTHON_PATH=python
set SCRIPT_PATH=D:\admin\Desktop\Suppresstion-click\main.py
set SCHEDULE_TIME=07:00

:: Check if Python is available
%PYTHON_PATH% --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found in PATH.
    echo  Please install Python 3.8+ from https://python.org
    echo  Make sure to check "Add Python to PATH" during install
    pause
    exit /b 1
)

echo  [1/3] Installing required Python packages...
pip install requests beautifulsoup4 openpyxl pandas lxml -q
if errorlevel 1 (
    echo  [ERROR] Failed to install packages. Check internet connection.
    pause
    exit /b 1
)
echo  Packages installed successfully!
echo.

echo  [2/3] Registering Windows Scheduled Task...
echo  Task Name : %TASK_NAME%
echo  Script    : %SCRIPT_PATH%
echo  Schedule  : Daily at %SCHEDULE_TIME%
echo.

:: Delete existing task if it exists
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: Create the task - runs daily at 7:00 AM
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "%PYTHON_PATH% \"%SCRIPT_PATH%\"" ^
  /sc daily ^
  /st %SCHEDULE_TIME% ^
  /ru "%USERNAME%" ^
  /rl highest ^
  /f

if errorlevel 1 (
    echo  [ERROR] Failed to create scheduled task.
    echo  Try running this script as Administrator.
    pause
    exit /b 1
)

echo.
echo  [3/3] Creating folder structure...
mkdir "D:\admin\Desktop\Suppresstion-click\input" 2>nul
mkdir "D:\admin\Desktop\Suppresstion-click\output" 2>nul
mkdir "D:\admin\Desktop\Suppresstion-click\master" 2>nul
mkdir "D:\admin\Desktop\Suppresstion-click\logs" 2>nul
echo  Folders created!

echo.
echo  ===============================================
echo   SETUP COMPLETE!
echo  ===============================================
echo.
echo  NEXT STEPS:
echo  -----------
echo  1. Place Clck-asins.xlsx in:
echo     D:\admin\Desktop\Suppresstion-click\input\
echo.
echo  2. Place Sounce_Master_Monthly_Report.xlsx in:
echo     D:\admin\Desktop\Suppresstion-click\input\
echo.
echo  3. Place Suppression_Sheet__1_.xlsx in:
echo     D:\admin\Desktop\Suppresstion-click\master\
echo.
echo  4. The tool will run automatically at 7:00 AM daily
echo.
echo  5. To test right now, double-click: RUN_NOW.bat
echo  ===============================================
echo.
pause

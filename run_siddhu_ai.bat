@echo off
title SIDDHU AI // JARVIS HUD LAUNCHER
cd /d "%~dp0\siddhu_ai"
echo ======================================================================
echo    INITIALIZING SIDDHU AI // TACTICAL HUD (JARVIS PROTOCOL MK-VII)
echo ======================================================================
echo.
python app.py
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred while running SIDDHU AI.
    pause
)

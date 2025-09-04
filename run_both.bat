@echo off
title JakLike - Launching Both Services
echo.
echo ========================================
echo    JakLike - Bot + Mini App Launcher
echo ========================================
echo.

echo Starting Telegram Bot...
start "JakLike Bot" cmd /k "python main.py"

echo Starting Mini App...
start "JakLike Mini App" cmd /k "python user_app.py"

echo.
echo ========================================
echo Both services are starting...
echo.
echo Bot: Check the "JakLike Bot" window
echo Mini App: Check the "JakLike Mini App" window
echo.
echo Mini App will be available at: http://localhost:5000
echo ========================================
echo.
pause





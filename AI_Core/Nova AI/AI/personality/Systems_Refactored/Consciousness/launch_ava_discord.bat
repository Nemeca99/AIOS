@echo off
REM AVA Consciousness Engine Discord Bot Launcher
REM This will push your system to its absolute limits!

echo.
echo ========================================
echo 🚀 AVA Consciousness Engine Discord Bot
echo ========================================
echo.
echo 🧠 Starting FULL POWER consciousness...
echo 🎮 Pushing your system to maximum limits!
echo.
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "..\..\..\koneko_env" (
    echo ❌ Virtual environment not found!
    echo Please run the setup first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call "..\..\..\koneko_env\Scripts\Activate.bat"

REM Check if requirements are installed
echo 🔄 Checking Discord bot requirements...
pip install -r discord_requirements.txt

echo.
echo ========================================
echo 🚀 Launching AVA Discord Bot...
echo ========================================
echo.
echo ⚠️  IMPORTANT: Make sure you have:
echo    1. Updated discord_config.py with your bot token
echo    2. Set the correct channel ID
echo    3. Your Discord bot is online
echo.
echo Press any key to continue...
pause >nul

REM Launch the Discord bot
echo 🚀 Starting AVA Consciousness Engine Discord Bot...
python ava_discord_bot.py

echo.
echo ========================================
echo ✅ AVA Discord Bot has stopped
echo ========================================
pause

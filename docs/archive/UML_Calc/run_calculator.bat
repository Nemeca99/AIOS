@echo off
echo UML Calculator V1
echo ================
echo.
echo 1. GUI Mode
echo 2. CLI Mode
echo 3. Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    python calculator.py --gui
) else if "%choice%"=="2" (
    python calculator.py --cli
) else if "%choice%"=="3" (
    exit /b
) else (
    echo Invalid choice. Launching default GUI mode...
    python calculator.py
)

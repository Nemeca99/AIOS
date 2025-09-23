@echo off
echo 🧮 UML Calculator Launcher
echo ========================
echo.
echo Choose interface:
echo 1. GUI (Desktop app)
echo 2. Web (Browser interface) 
echo 3. CLI (Command line)
echo 4. Help
echo.
set /p choice="Enter choice (1-4): "

cd /d "d:\UML Calculator"

if "%choice%"=="1" (
    echo Starting GUI...
    python UML_Core\uml_calculator.py
) else if "%choice%"=="2" (
    echo Starting Web interface...
    python UML_Core\uml_calculator.py --web
) else if "%choice%"=="3" (
    echo Starting CLI...
    python UML_Core\uml_calculator.py --cli
) else if "%choice%"=="4" (
    python UML_Core\uml_calculator.py --help
) else (
    echo Invalid choice. Starting GUI...
    python UML_Core\uml_calculator.py
)

pause

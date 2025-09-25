@echo off
echo ============================================================
echo         T.R.E.E.S. UNIFIED CALCULATOR INTERFACE
echo           Transformative Recursive Emergent
echo           Embedding Systems Framework
echo ============================================================
echo.
echo Select which calculator interface to launch:
echo.
echo 1. UML Calculator - Mathematical UML operations and RIS meta-operators
echo 2. Codex Web Calculator - Symbolic algebra with web interface
echo 3. Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Launching UML Calculator...
    cd /d "D:\UML Calculator\UML_Core"
    python feature_demo.py
) else if "%choice%"=="2" (
    echo.
    echo Launching Codex Web Calculator...
    start "" "http://localhost:5000"
    cd /d "E:\Algebra\Calculator"
    python codex_web_calculator.py
) else if "%choice%"=="3" (
    echo.
    echo Exiting. Goodbye!
    exit /b
) else (
    echo.
    echo Invalid choice. Please try again.
    call %0
)

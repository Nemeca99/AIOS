@echo off
echo UML Symbolic Engine Launcher
echo ==========================
echo.
echo 1. Run UML Symbolic Engine Demo
echo 2. Start UML Symbolic Engine REPL
echo 3. Exit
echo.

:menu
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    python Documents\Code_Archives\symbolic_engine_demo.py
    pause
    goto menu
)
if "%choice%"=="2" (
    python -c "from UML_Core.symbolic_engine import SymbolicEngine; SymbolicEngine().run_interactive_repl()"
    goto menu
)
if "%choice%"=="3" (
    exit /b
)

echo Invalid choice, please try again.
goto menu

@echo off
REM UML Calculator Launcher
REM This batch file launches the UML Calculator

echo Starting UML Calculator...
python "%~dp0UML_Core\uml_calculator.py"

if %errorlevel% neq 0 (
    echo Calculator exited with error code %errorlevel%
    pause
)

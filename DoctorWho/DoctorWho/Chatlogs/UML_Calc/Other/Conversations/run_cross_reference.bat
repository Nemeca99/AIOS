@echo off
cd /d "%~dp0"
echo Running Cross-Reference Analysis...
echo This will find connections between different categories of insights
echo.
python cross_reference_analyzer.py
echo.
echo Cross-reference analysis complete!
pause

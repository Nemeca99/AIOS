@echo off
cd /d "%~dp0"
echo Running Timeline Correlation Analysis...
echo This will analyze how your ideas evolved over time and show correlations
echo.
python timeline_analyzer.py
echo.
echo Timeline analysis complete!
pause

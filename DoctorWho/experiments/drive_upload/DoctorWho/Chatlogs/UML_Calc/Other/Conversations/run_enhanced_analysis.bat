@echo off
cd /d "%~dp0"
echo Running Enhanced Conversation Analysis...
echo This will generate enhanced extracts with additional search terms, cross-references, and timeline analysis
echo.
python enhanced_analyzer.py
echo.
echo Enhanced analysis complete!
pause

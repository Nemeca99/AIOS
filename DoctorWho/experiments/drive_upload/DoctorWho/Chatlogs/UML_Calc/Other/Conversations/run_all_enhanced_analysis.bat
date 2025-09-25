@echo off
cd /d "%~dp0"
echo ================================================================
echo             ENHANCED CONVERSATION ANALYSIS SUITE
echo ================================================================
echo.
echo This will run all enhanced analysis tools in sequence:
echo 1. Enhanced Analyzer (additional search terms + new categories)
echo 2. Cross-Reference Analysis (find connections between categories)  
echo 3. Timeline Correlation (show idea evolution over time)
echo.
echo Starting enhanced analysis...
echo.

echo ----------------------------------------------------------------
echo 1. Running Enhanced Analyzer...
echo ----------------------------------------------------------------
python enhanced_analyzer.py
if errorlevel 1 (
    echo Warning: Enhanced analyzer encountered an issue but continuing...
)
echo.

echo ----------------------------------------------------------------
echo 2. Running Cross-Reference Analysis...
echo ----------------------------------------------------------------
python cross_reference_analyzer.py
if errorlevel 1 (
    echo Warning: Cross-reference analyzer encountered an issue but continuing...
)
echo.

echo ----------------------------------------------------------------
echo 3. Running Timeline Correlation Analysis...
echo ----------------------------------------------------------------
python timeline_analyzer.py
if errorlevel 1 (
    echo Warning: Timeline analyzer encountered an issue but continuing...
)
echo.

echo ================================================================
echo                    ANALYSIS COMPLETE!
echo ================================================================
echo.
echo Generated files:
echo - Enhanced extracts: enhanced_*_extracts.md
echo - Cross-references: cross_reference_report.md
echo - Timeline analysis: timeline_correlation_report.md
echo.
echo Check the generated files for comprehensive insights!
echo.
pause

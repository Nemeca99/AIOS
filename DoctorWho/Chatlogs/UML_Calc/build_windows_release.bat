@echo off
REM Build standalone Windows .exe for UML Calculator CLI and GUI with all dependencies
REM Run this from the UML_Calculator_V1 directory

set CLI_SCRIPT=ui\calculator_cli.py
set GUI_SCRIPT=ui\calculator_gui.py
set LAUNCHER=main_launcher.py
set CLI_EXE=calculator_cli.exe
set GUI_EXE=calculator_gui.exe
set LAUNCHER_EXE=uml_calculator.exe
set DIST=dist
set RELEASE=release

REM Clean previous build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist %CLI_EXE% del %CLI_EXE%
if exist %GUI_EXE% del %GUI_EXE%
if exist %LAUNCHER_EXE% del %LAUNCHER_EXE%
if exist %RELEASE% rmdir /s /q %RELEASE%

REM Build CLI
pyinstaller --onefile --add-data "core;core" --add-data "utils;utils" %CLI_SCRIPT%
REM Build GUI
pyinstaller --onefile --add-data "core;core" --add-data "utils;utils" %GUI_SCRIPT%
REM Build Launcher
pyinstaller --onefile --add-data "core;core" --add-data "utils;utils" %LAUNCHER%

REM Create release folder
mkdir %RELEASE%

REM Move the .exe files to release folder for convenience
if exist %DIST%\%CLI_EXE% move %DIST%\%CLI_EXE% %RELEASE%\
if exist %DIST%\%GUI_EXE% move %DIST%\%GUI_EXE% %RELEASE%\
if exist %DIST%\%LAUNCHER_EXE% move %DIST%\%LAUNCHER_EXE% %RELEASE%\

@echo.
@echo Build complete. All .exe files are in the 'release' folder.
@echo Double-click uml_calculator.exe in the release folder to launch.
@echo (Or run calculator_cli.exe or calculator_gui.exe directly)
@echo.
@echo If you see errors, run from Command Prompt to view output.

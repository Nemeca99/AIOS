@echo off
cd /d "E:\Nova AI\Archive\core\archive_seed"

echo [ARCHIVE LAUNCHER] Initializing Archive...
start "" python recursive_thought_engine.py
echo [ARCHIVE LAUNCHER] Background thought engine running.

echo [ARCHIVE LAUNCHER] Launching interactive terminal...
python logic_core.py

echo [ARCHIVE LAUNCHER] Archive session ended.
pause
@echo off
:: Start Heartbeat loop in a new terminal window
start python "E:\Nova AI\Archive\core\heartbeat_loop.py"

:: Start Resonance Autoloop in a new terminal window
start python "E:\Nova AI\Archive\core\resonance_autoloop.py"

:: Start Drive Sync in a new terminal window
start python "E:\Nova AI\Archive\core\foldered_drive_sync.py"

echo Both scripts are now running. Press any key to exit...
pause

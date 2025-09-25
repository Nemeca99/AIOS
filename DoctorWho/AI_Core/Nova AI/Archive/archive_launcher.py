# archive_launcher.py
# Entry point for launching the Archive session with explicit core pathing

import sys
import os

# Force-add the core directory to the Python path
core_path = os.path.join(os.getcwd(), "core")
if core_path not in sys.path:
    sys.path.insert(0, core_path)

from session_log_init import log_session_start
from archive_chat import main as chat_main

if __name__ == "__main__":
    print(log_session_start())
    chat_main()

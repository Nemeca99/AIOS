#!/usr/bin/env python3
"""
AIOS Chat - Clean entry point for Luna chat without main.py imports
"""

import sys
import subprocess
import os

def main():
    if len(sys.argv) < 4 or sys.argv[1] != "--luna" or sys.argv[2] != "--chat":
        print("Usage: python aios_chat.py --luna --chat <message>")
        sys.exit(1)
    
    message = sys.argv[3]
    
    try:
        # Call the clean luna chat script directly
        result = subprocess.run([sys.executable, "luna_chat.py", message], 
                              capture_output=True, text=True, cwd=os.getcwd())
        print(result.stdout.strip())
        if result.stderr:
            print(f"Error: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

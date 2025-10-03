#!/usr/bin/env python3
"""
Quick Luna chat - direct subprocess call without any imports
"""

import sys
import subprocess
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_chat.py <message>")
        sys.exit(1)
    
    message = sys.argv[1]
    
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

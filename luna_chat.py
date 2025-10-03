#!/usr/bin/env python3
"""
Clean Luna chat interface - completely bypasses main.py initialization
"""

import sys
import os
from io import StringIO

# Redirect stdout and stderr to suppress all output
old_stdout = sys.stdout
old_stderr = sys.stderr

# Also suppress the unicode output initialization
class SuppressOutput:
    def write(self, data):
        pass
    def flush(self):
        pass
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

sys.stdout = SuppressOutput()
sys.stderr = SuppressOutput()

# Set silent mode before any imports
os.environ["AIOS_SILENT_MODE"] = "true"

try:
    # Now import the system directly
    from main import AIOSClean
    
    def main():
        if len(sys.argv) < 2:
            # Restore output for usage message
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            print("Usage: python luna_chat.py <message>")
            sys.exit(1)
        
        message = " ".join(sys.argv[1:])
        
        # Initialize system (will be silent due to environment variable)
        aios = AIOSClean()
        
        # Get Luna system
        luna_system = aios._get_system('luna')
        
        # Get Luna's response
        response = luna_system.generate_response(message)
        
        # Restore output only for Luna's response
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        # Print only Luna's response
        print(response)
    
    if __name__ == "__main__":
        main()
        
except Exception as e:
    # Restore output in case of error
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    print(f"Error: {e}")

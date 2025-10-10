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

# Suppress unicode output initialization to prevent startup messages
class SuppressOutput:
    """Output suppressor for clean startup"""
    def write(self, data):
        # Intentionally suppress - used during initialization only
        return
    def flush(self):
        # Intentionally suppress - used during initialization only
        return
    def __getattr__(self, name):
        # Return no-op lambda for any other method calls
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

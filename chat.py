#!/usr/bin/env python3
"""
Clean chat interface for Luna - bypasses all system initialization logging
"""

import sys
import os
from io import StringIO

# Temporarily disable output suppression to debug
# old_stdout = sys.stdout
# old_stderr = sys.stderr
# sys.stdout = StringIO()
# sys.stderr = StringIO()

# Also suppress the unicode output initialization
# class SuppressOutput:
#     def write(self, data):
#         pass
#     def flush(self):
#         pass
#     def __getattr__(self, name):
#         return lambda *args, **kwargs: None

# sys.stdout = SuppressOutput()
# sys.stderr = SuppressOutput()

# Set silent mode before any imports
# os.environ["AIOS_SILENT_MODE"] = "true"

try:
    # Now import the system
    from main import AIOSClean
    
    def main():
        if len(sys.argv) < 2:
            # Restore output for usage message
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            print("Usage: python chat.py <message>")
            sys.exit(1)
        
        message = " ".join(sys.argv[1:])
        
        # Initialize system (will be silent due to environment variable)
        aios = AIOSClean()
        
        # Get Luna system
        luna_system = aios._get_system('luna')
        
        # Get Luna's response
        response = luna_system.generate_response(message, "general", None, [])
        
        # Print only Luna's response
        print(response)
    
    if __name__ == "__main__":
        main()
        
except Exception as e:
    print(f"Error: {e}")

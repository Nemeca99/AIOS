"""
UML Calculator Launcher
A simple entry point script to launch the enhanced UML Calculator
"""

import sys
import os
import subprocess

def main():
    """Main entry point for the UML Calculator"""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # The calculator script path
    calculator_path = os.path.join(script_dir, "enhanced_calculator.py")
    
    # Check if the calculator script exists
    if not os.path.exists(calculator_path):
        print(f"Error: Could not find the calculator script at {calculator_path}")
        return 1
    
    # Process command line arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else ["gui"]
    
    # Execute the calculator with the provided arguments
    cmd = [sys.executable, calculator_path] + args
    try:
        subprocess.run(cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error running calculator: {e}")
        return e.returncode
    
if __name__ == "__main__":
    sys.exit(main())

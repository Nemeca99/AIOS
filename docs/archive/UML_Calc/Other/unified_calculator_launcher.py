"""
TREES Unified Calculator Interface

This script provides a unified interface to launch either:
1. The UML Calculator for advanced mathematical operations
2. The Codex Web Calculator for symbolic algebra

Author: @Nemeca99
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_header():
    print("=" * 60)
    print("        T.R.E.E.S. UNIFIED CALCULATOR INTERFACE")
    print("          Transformative Recursive Emergent")
    print("          Embedding Systems Framework")
    print("=" * 60)
    print("\nSelect which calculator interface to launch:\n")

def main():
    print_header()
    
    # Define paths to different calculator components
    uml_calc_path = Path("d:/UML Calculator/UML_Core/feature_demo.py")
    codex_web_calc_path = Path("e:/Algebra/Calculator/codex_web_calculator.py")
    
    options = [
        ("1", "UML Calculator - Mathematical UML operations and RIS meta-operators"),
        ("2", "Codex Web Calculator - Symbolic algebra with web interface"),
        ("3", "Exit")
    ]
    
    for option, description in options:
        print(f"{option}. {description}")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        print("\nLaunching UML Calculator...")        try:
            os.chdir(uml_calc_path.parent)
            subprocess.run([sys.executable, str(uml_calc_path)], check=True)
        except (FileNotFoundError, PermissionError, subprocess.SubprocessError) as e:
            print(f"Error launching UML Calculator: {e}")
        except Exception as e:
            print(f"Unexpected error launching UML Calculator: {e}")
    
    elif choice == "2":
        print("\nLaunching Codex Web Calculator...")
        try:
            os.chdir(codex_web_calc_path.parent)
            # Start the web server in a subprocess
            process = subprocess.Popen([sys.executable, str(codex_web_calc_path)])
            print("Web calculator server starting...")
            # Give the server a moment to start
            import time
            time.sleep(2)
            # Open the web browser
            webbrowser.open("http://localhost:5000")
            print("\nPress Ctrl+C when finished to stop the server.")
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping web calculator server...")
            process.terminate()
        except Exception as e:
            print(f"Error launching Codex Web Calculator: {e}")
    
    elif choice == "3":
        print("\nExiting. Goodbye!")
        sys.exit(0)
    
    else:
        print("\nInvalid choice. Please try again.")
        main()

if __name__ == "__main__":
    main()

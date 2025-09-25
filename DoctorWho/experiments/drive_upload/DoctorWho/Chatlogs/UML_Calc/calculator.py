"""
UML Calculator V1 - Main Launcher
Provides options to launch either the GUI or CLI version of the calculator
"""

import os
import sys
import importlib.util
import argparse

def import_module_from_file(file_path, module_name):
    """Dynamically import a module from a file path"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        print(f"Error: Could not load {module_name} module")
        return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="UML Calculator V1")
    parser.add_argument("--cli", action="store_true", help="Run in command line interface mode")
    parser.add_argument("--gui", action="store_true", help="Run in graphical user interface mode")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run CLI in interactive mode")
    parser.add_argument("--steps", "-s", action="store_true", help="Show calculation steps (CLI mode)")
    parser.add_argument("--mode", "-m", choices=["auto", "standard", "uml", "ris"], 
                        default="auto", help="Calculation mode (CLI mode)")
    parser.add_argument("expression", nargs="?", help="Expression to evaluate in CLI mode")
    
    args = parser.parse_args()
    
    # Get the current directory (where this script is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Import paths
    gui_path = os.path.join(current_dir, 'ui', 'calculator_gui.py')
    cli_path = os.path.join(current_dir, 'ui', 'calculator_cli.py')
    
    # Determine which interface to launch
    if args.cli:
        # Launch CLI
        cli_module = import_module_from_file(cli_path, "calculator_cli")
        if cli_module:
            # Build arguments for the CLI module
            cli_argv = [sys.argv[0]]
            
            if args.expression:
                cli_argv.append(args.expression)
                
            if args.interactive:
                cli_argv.append("--interactive")
                
            if args.steps:
                cli_argv.append("--steps")
                
            if args.mode != "auto":
                cli_argv.extend(["--mode", args.mode])
                
            # Set the new argv and run the CLI
            sys.argv = cli_argv
            cli_module.main()
    elif args.gui:
        # Launch GUI
        gui_module = import_module_from_file(gui_path, "calculator_gui")
        if gui_module:
            gui_module.main()
    else:
        # Default to GUI if no explicit option is provided
        gui_module = import_module_from_file(gui_path, "calculator_gui")
        if gui_module:
            gui_module.main()

if __name__ == "__main__":
    main()

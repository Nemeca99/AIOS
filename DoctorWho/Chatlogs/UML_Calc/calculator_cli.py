"""
UML Calculator - Main CLI entry point
"""

if __name__ == "__main__":
    import os
    import importlib.util
    
    # Get the absolute path to the ui module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cli_path = os.path.join(current_dir, 'ui', 'calculator_cli.py')
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("calculator_cli", cli_path)
    if spec and spec.loader:
        cli_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli_module)
        
        # Run the CLI
        cli_module.main()
    else:
        print("Error: Could not load calculator_cli module")

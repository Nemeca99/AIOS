"""
UML Calculator - Main GUI entry point
"""

if __name__ == "__main__":
    import os
    import importlib.util
    
    # Get the absolute path to the ui module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gui_path = os.path.join(current_dir, 'ui', 'calculator_gui.py')
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("calculator_gui", gui_path)
    if spec and spec.loader:
        gui_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gui_module)
        
        # Run the GUI
        gui_module.main()
    else:
        print("Error: Could not load calculator_gui module")

#!/usr/bin/env python3
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

AIOS Launcher - Choose between CLI, GUI, or Monitoring Dashboard
"""

import PySimpleGUI as sg
import subprocess
import sys
import os
from pathlib import Path

def create_launcher_layout():
    """Create the launcher interface"""
    
    # Set theme
    sg.theme('DarkBlue3')
    
    layout = [
        [sg.Text("🚀 AIOS Launcher", font=("Arial", 20, "bold"), justification="center", size=(50, 1))],
        [sg.Text("Choose your AIOS interface:", font=("Arial", 14), justification="center")],
        [sg.HSeparator()],
        
        # Main interface options
        [sg.Button("🖥️ GUI Interface", key="-GUI-", size=(25, 3), button_color=("white", "blue"))],
        [sg.Button("📊 Monitoring Dashboard", key="-DASHBOARD-", size=(25, 3), button_color=("white", "green"))],
        [sg.Button("⚡ PowerShell CLI", key="-CLI-", size=(25, 3), button_color=("white", "orange"))],
        
        [sg.HSeparator()],
        
        # Quick actions
        [sg.Text("Quick Actions:", font=("Arial", 12, "bold"))],
        [sg.Button("🔧 Install GUI Dependencies", key="-INSTALL-", size=(20, 1)),
         sg.Button("📋 View Help", key="-HELP-", size=(15, 1)),
         sg.Button("⚙️ Settings", key="-SETTINGS-", size=(15, 1))],
        
        [sg.HSeparator()],
        
        # Status information
        [sg.Text("Status:", font=("Arial", 10, "bold")), sg.Text("Ready", key="-STATUS-", size=(50, 1))],
        
        [sg.HSeparator()],
        
        [sg.Button("❌ Exit", key="-EXIT-", button_color=("white", "red"))]
    ]
    
    return layout

def check_dependencies():
    """Check if GUI dependencies are installed"""
    try:
        import PySimpleGUI
        import matplotlib
        import psutil
        return True, "✅ All dependencies installed"
    except ImportError as e:
        return False, f"❌ Missing dependency: {e}"

def install_dependencies():
    """Install GUI dependencies"""
    try:
        sg.popup("Installing GUI dependencies...", title="Installing")
        
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements_gui.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            sg.popup("✅ Dependencies installed successfully!", title="Success")
            return True
        else:
            sg.popup_error(f"❌ Installation failed:\n{result.stderr}", title="Error")
            return False
            
    except Exception as e:
        sg.popup_error(f"❌ Installation error: {e}", title="Error")
        return False

def launch_gui():
    """Launch the GUI interface"""
    try:
        sg.popup("Launching AIOS GUI...", title="Launching")
        subprocess.Popen([sys.executable, "aios_gui.py"])
        return True
    except Exception as e:
        sg.popup_error(f"❌ Failed to launch GUI: {e}", title="Error")
        return False

def launch_dashboard():
    """Launch the monitoring dashboard"""
    try:
        sg.popup("Launching AIOS Monitoring Dashboard...", title="Launching")
        subprocess.Popen([sys.executable, "aios_monitoring_dashboard.py"])
        return True
    except Exception as e:
        sg.popup_error(f"❌ Failed to launch dashboard: {e}", title="Error")
        return False

def launch_cli():
    """Launch the PowerShell CLI"""
    try:
        sg.popup("Launching AIOS PowerShell CLI...", title="Launching")
        
        # Check if PowerShell wrapper exists
        wrapper_path = Path("aios_powershell_wrapper.ps1")
        if not wrapper_path.exists():
            sg.popup_error("❌ PowerShell wrapper not found!", title="Error")
            return False
        
        # Launch PowerShell with the wrapper
        subprocess.Popen([
            "powershell", "-ExecutionPolicy", "Bypass", 
            "-File", str(wrapper_path), "-AdminMode", "-DebugMode"
        ])
        return True
        
    except Exception as e:
        sg.popup_error(f"❌ Failed to launch CLI: {e}", title="Error")
        return False

def show_help():
    """Show help information"""
    help_text = """
🚀 AIOS Launcher Help

INTERFACES:
• GUI Interface: User-friendly graphical interface with buttons and real-time output
• Monitoring Dashboard: Advanced dashboard with charts and system monitoring
• PowerShell CLI: Command-line interface with full system access

FEATURES:
• GUI Interface: Easy-to-use buttons for all AIOS commands
• Monitoring Dashboard: Real-time system performance charts
• PowerShell CLI: Full command-line access with admin powers

REQUIREMENTS:
• GUI Interface: Requires PySimpleGUI, matplotlib, psutil
• Monitoring Dashboard: Requires matplotlib, psutil, numpy
• PowerShell CLI: Requires PowerShell and Windows

QUICK START:
1. Click "Install GUI Dependencies" if using GUI interfaces
2. Choose your preferred interface
3. Use the interface to control AIOS

TROUBLESHOOTING:
• If GUI fails to launch, check dependencies
• If PowerShell fails, check execution policy
• Ensure all AIOS files are in the same directory
    """
    
    layout = [
        [sg.Text("❓ AIOS Launcher Help", font=("Arial", 16, "bold"))],
        [sg.Multiline(help_text, size=(80, 25), disabled=True, 
                     background_color="lightgray", text_color="black")],
        [sg.Button("Close", key="-CLOSE-HELP-")]
    ]
    
    help_window = sg.Window("Help", layout, modal=True)
    
    while True:
        event, values = help_window.read()
        if event in (sg.WIN_CLOSED, "-CLOSE-HELP-"):
            break
    
    help_window.close()

def show_settings():
    """Show settings"""
    settings_text = """
⚙️ AIOS Launcher Settings

Current Configuration:
• Default Interface: GUI
• Auto-check Dependencies: Enabled
• Launch in Admin Mode: Disabled

Settings Panel Coming Soon!
This will allow you to configure:
• Default interface selection
• Auto-installation options
• Launch parameters
• Theme preferences
    """
    
    sg.popup(settings_text, title="Settings")

def main():
    """Main launcher function"""
    layout = create_launcher_layout()
    window = sg.Window("AIOS Launcher", layout, finalize=True)
    
    # Check initial status
    deps_ok, status_msg = check_dependencies()
    window["-STATUS-"].update(status_msg)
    
    # Event loop
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, "-EXIT-"):
            break
        
        elif event == "-GUI-":
            if deps_ok:
                if launch_gui():
                    break  # Close launcher after successful launch
            else:
                sg.popup("❌ GUI dependencies not installed!\nClick 'Install GUI Dependencies' first.", 
                        title="Dependencies Required")
        
        elif event == "-DASHBOARD-":
            if deps_ok:
                if launch_dashboard():
                    break  # Close launcher after successful launch
            else:
                sg.popup("❌ Dashboard dependencies not installed!\nClick 'Install GUI Dependencies' first.", 
                        title="Dependencies Required")
        
        elif event == "-CLI-":
            if launch_cli():
                break  # Close launcher after successful launch
        
        elif event == "-INSTALL-":
            window["-STATUS-"].update("Installing dependencies...")
            window.refresh()
            
            if install_dependencies():
                deps_ok, status_msg = check_dependencies()
                window["-STATUS-"].update(status_msg)
        
        elif event == "-HELP-":
            show_help()
        
        elif event == "-SETTINGS-":
            show_settings()
    
    window.close()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

AIOS PowerShell Backend Monitor - GUI Interface
Beautiful graphical interface for the AIOS backend monitoring system
"""

import PySimpleGUI as sg
import subprocess
import os
import sys
import threading
import time
import json
import queue
from datetime import datetime
from pathlib import Path
from utils_core.powershell_bridge import PowerShellBridge

# Set the theme
sg.theme('DarkBlue3')

class AIOSGUI:
    def __init__(self):
        self.aios_root = Path(__file__).parent
        self.powershell_wrapper = self.aios_root / "aios_powershell_wrapper.ps1"
        self.bridge = None
        self.output_queue = queue.Queue()
        self.monitoring_active = False
        self.config_file = self.aios_root / "aios_gui_config.json"
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize PowerShell bridge
        try:
            self.bridge = PowerShellBridge(str(self.aios_root))
            self.status_message = "✅ PowerShell bridge initialized"
        except Exception as e:
            self.status_message = f"❌ Bridge error: {str(e)}"
    
    def load_config(self):
        """Load GUI configuration"""
        default_config = {
            "auto_refresh": True,
            "refresh_interval": 30,
            "default_mode": "luna",
            "max_log_lines": 100,
            "theme": "DarkBlue3",
            "window_size": (1200, 800),
            "recent_commands": []
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save GUI configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def create_main_layout(self):
        """Create the main GUI layout"""
        
        # Command buttons frame
        commands_frame = [
            [sg.Text("🚀 AIOS Commands", font=("Arial", 14, "bold"))],
            [sg.Button("System Status", key="-STATUS-", size=(15, 1)),
             sg.Button("Health Check", key="-HEALTH-", size=(15, 1)),
             sg.Button("Code Analysis", key="-ANALYZE-", size=(15, 1))],
            [sg.Button("Project Readiness", key="-READINESS-", size=(15, 1)),
             sg.Button("System Diagnostics", key="-DIAGNOSE-", size=(15, 1)),
             sg.Button("Create Backup", key="-BACKUP-", size=(15, 1))],
            [sg.Button("Start Monitoring", key="-MONITOR-", size=(15, 1)),
             sg.Button("View Logs", key="-LOGS-", size=(15, 1)),
             sg.Button("Cleanup Project", key="-CLEANUP-", size=(15, 1))]
        ]
        
        # AIOS Control frame
        control_frame = [
            [sg.Text("🎛️ AIOS Control", font=("Arial", 14, "bold"))],
            [sg.Text("Mode:"), sg.Combo(["luna", "carma", "enterprise", "support", "health"], 
                                       default_value=self.config["default_mode"], 
                                       key="-MODE-", size=(12, 1))],
            [sg.Text("Questions:"), sg.Slider(range=(1, 100), default_value=1, 
                                            orientation='h', key="-QUESTIONS-", size=(15, 15))],
            [sg.Checkbox("Interactive Mode", key="-INTERACTIVE-", default=True),
             sg.Checkbox("Admin Mode", key="-ADMIN-")],
            [sg.Button("🚀 Start AIOS", key="-START-AIOS-", size=(20, 2), button_color=("white", "green")),
             sg.Button("⏹️ Stop AIOS", key="-STOP-AIOS-", size=(15, 2), button_color=("white", "red"))]
        ]
        
        # System info frame
        system_frame = [
            [sg.Text("📊 System Information", font=("Arial", 14, "bold"))],
            [sg.Text("Status:", key="-SYSTEM-STATUS-", size=(50, 1))],
            [sg.Text("Components:", key="-COMPONENTS-", size=(50, 1))],
            [sg.Text("Last Update:", key="-LAST-UPDATE-", size=(50, 1))]
        ]
        
        # Output frame
        output_frame = [
            [sg.Text("📋 Output", font=("Arial", 14, "bold"))],
            [sg.Multiline(size=(100, 20), key="-OUTPUT-", autoscroll=True, 
                         reroute_stdout=True, reroute_stderr=True, 
                         background_color="black", text_color="lime")],
            [sg.Button("Clear Output", key="-CLEAR-"), 
             sg.Button("Save Output", key="-SAVE-OUTPUT-"),
             sg.Text("Lines:", key="-LINE-COUNT-", size=(10, 1))]
        ]
        
        # Progress frame
        progress_frame = [
            [sg.Text("⏳ Progress", font=("Arial", 12, "bold"))],
            [sg.ProgressBar(100, orientation='h', size=(40, 20), key="-PROGRESS-")],
            [sg.Text("Ready", key="-PROGRESS-TEXT-", size=(50, 1))]
        ]
        
        # Layout
        layout = [
            [sg.Text("🚀 AIOS PowerShell Backend Monitor", font=("Arial", 18, "bold"), 
                    justification="center", size=(50, 1))],
            [sg.Text(self.status_message, key="-STATUS-MESSAGE-", justification="center")],
            [sg.HSeparator()],
            
            # Main content area
            [sg.Column(commands_frame, vertical_alignment="top"),
             sg.VSeparator(),
             sg.Column(control_frame, vertical_alignment="top")],
             
            [sg.HSeparator()],
            
            [sg.Column(system_frame, vertical_alignment="top"),
             sg.VSeparator(),
             sg.Column(progress_frame, vertical_alignment="top")],
             
            [sg.HSeparator()],
            
            [sg.Column(output_frame, vertical_alignment="top")],
            
            # Bottom buttons
            [sg.HSeparator()],
            [sg.Button("🔄 Refresh", key="-REFRESH-"),
             sg.Button("⚙️ Settings", key="-SETTINGS-"),
             sg.Button("❓ Help", key="-HELP-"),
             sg.Button("❌ Exit", key="-EXIT-", button_color=("white", "red"))]
        ]
        
        return layout
    
    def create_settings_layout(self):
        """Create settings window layout"""
        layout = [
            [sg.Text("⚙️ AIOS GUI Settings", font=("Arial", 16, "bold"))],
            [sg.HSeparator()],
            
            [sg.Text("Auto Refresh:", size=(20, 1)), 
             sg.Checkbox("Enable", key="-AUTO-REFRESH-", default=self.config["auto_refresh"])],
            [sg.Text("Refresh Interval (seconds):", size=(25, 1)), 
             sg.Slider(range=(5, 300), default_value=self.config["refresh_interval"], 
                      orientation='h', key="-REFRESH-INTERVAL-", size=(20, 15))],
            
            [sg.Text("Max Log Lines:", size=(20, 1)), 
             sg.Slider(range=(50, 1000), default_value=self.config["max_log_lines"], 
                      orientation='h', key="-MAX-LOG-LINES-", size=(20, 15))],
            
            [sg.Text("Theme:", size=(20, 1)), 
             sg.Combo(["DarkBlue3", "Dark", "LightBlue3", "LightGrey1"], 
                     default_value=self.config["theme"], key="-THEME-", size=(15, 1))],
            
            [sg.HSeparator()],
            [sg.Text("Window Size:", size=(20, 1)), 
             sg.Text(f"Current: {self.config['window_size'][0]}x{self.config['window_size'][1]}", key="-WINDOW-SIZE-")],
            
            [sg.HSeparator()],
            [sg.Button("💾 Save Settings", key="-SAVE-SETTINGS-"),
             sg.Button("🔄 Reset to Defaults", key="-RESET-SETTINGS-"),
             sg.Button("❌ Cancel", key="-CANCEL-SETTINGS-")]
        ]
        
        return layout
    
    def create_help_layout(self):
        """Create help window layout"""
        help_text = """
🚀 AIOS PowerShell Backend Monitor - Help

COMMANDS:
• System Status: Check all AIOS components and system health
• Health Check: Run comprehensive health diagnostics
• Code Analysis: Analyze code quality and find issues
• Project Readiness: Check project completeness and dependencies
• System Diagnostics: Full system analysis with security scan
• Create Backup: Create system backup for restoration
• Start Monitoring: Begin real-time system monitoring
• View Logs: Display recent system logs
• Cleanup Project: Clean temporary files and optimize space

CONTROLS:
• Mode: Select AIOS operation mode (luna, carma, etc.)
• Questions: Number of questions for AIOS processing
• Interactive Mode: Run AIOS in interactive mode
• Admin Mode: Enable full system access (use with caution)

FEATURES:
• Real-time output display with color coding
• Progress tracking for long-running operations
• Auto-refresh system status
• Configuration management
• Output saving and logging

KEYBOARD SHORTCUTS:
• Ctrl+R: Refresh system status
• Ctrl+L: Clear output
• Ctrl+S: Save output
• F1: Show this help
• Esc: Close current dialog

TROUBLESHOOTING:
• If PowerShell commands fail, check execution policy
• Ensure AIOS root directory is correct
• Check that all required files exist
• Verify Python virtual environment is activated

For more information, see the documentation files.
        """
        
        layout = [
            [sg.Text("❓ AIOS GUI Help", font=("Arial", 16, "bold"))],
            [sg.Multiline(help_text, size=(80, 30), disabled=True, 
                         background_color="lightgray", text_color="black")]
        ]
        
        return layout
    
    def execute_powershell_command(self, command_args, window=None):
        """Execute PowerShell command with real-time output"""
        try:
            # Clear output
            if window:
                window["-OUTPUT-"].update("")
                window["-PROGRESS-"].update(0)
                window["-PROGRESS-TEXT-"].update("Starting...")
            
            # Construct command
            cmd = [
                'powershell',
                '-ExecutionPolicy', 'Bypass',
                '-File', str(self.powershell_wrapper)
            ] + command_args
            
            # Execute command
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                cwd=str(self.aios_root),
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            line_count = 0
            
            # Read output in real-time
            for line in process.stdout:
                if window:
                    window["-OUTPUT-"].update(line, append=True)
                    line_count += 1
                    window["-LINE-COUNT-"].update(f"Lines: {line_count}")
                    window.refresh()
                output_lines.append(line)
            
            # Read any remaining stderr
            stderr_output = process.stderr.read()
            if stderr_output and window:
                window["-OUTPUT-"].update(f"\n[ERROR]\n{stderr_output}", append=True)
            
            # Wait for completion
            return_code = process.wait()
            
            if window:
                if return_code == 0:
                    window["-PROGRESS-"].update(100)
                    window["-PROGRESS-TEXT-"].update("✅ Completed successfully")
                else:
                    window["-PROGRESS-"].update(100)
                    window["-PROGRESS-TEXT-"].update(f"❌ Failed with code {return_code}")
            
            return return_code == 0, output_lines
            
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            if window:
                window["-OUTPUT-"].update(error_msg)
                window["-PROGRESS-TEXT-"].update("❌ Error occurred")
            return False, [error_msg]
    
    def update_system_status(self, window):
        """Update system status information"""
        try:
            if self.bridge:
                result = self.bridge.get_system_status()
                if result['success']:
                    window["-SYSTEM-STATUS-"].update("✅ System Online")
                    if 'parsed_data' in result:
                        components = result['parsed_data']['components']
                        component_text = f"✅ {sum(1 for v in components.values() if v == 'Found')}/{len(components)} components"
                        window["-COMPONENTS-"].update(component_text)
                else:
                    window["-SYSTEM-STATUS-"].update("❌ System Issues")
                    window["-COMPONENTS-"].update("❌ Unable to check components")
            else:
                window["-SYSTEM-STATUS-"].update("⚠️ Bridge not initialized")
                window["-COMPONENTS-"].update("⚠️ Check PowerShell bridge")
            
            window["-LAST-UPDATE-"].update(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            window["-SYSTEM-STATUS-"].update(f"❌ Error: {str(e)}")
    
    def run_gui(self):
        """Run the main GUI application"""
        # Create main window
        window = sg.Window(
            "AIOS PowerShell Backend Monitor", 
            self.create_main_layout(),
            size=self.config["window_size"],
            resizable=True,
            finalize=True
        )
        
        # Initial system status update
        self.update_system_status(window)
        
        # Auto-refresh timer
        last_refresh = time.time()
        
        # Event loop
        while True:
            event, values = window.read(timeout=1000)  # 1 second timeout for auto-refresh
            
            # Handle timeout (auto-refresh)
            if event == sg.TIMEOUT_KEY:
                current_time = time.time()
                if (self.config["auto_refresh"] and 
                    current_time - last_refresh >= self.config["refresh_interval"]):
                    self.update_system_status(window)
                    last_refresh = current_time
                continue
            
            # Handle window close
            if event in (sg.WIN_CLOSED, "-EXIT-"):
                break
            
            # Command buttons
            if event == "-STATUS-":
                window["-PROGRESS-TEXT-"].update("Getting system status...")
                self.execute_powershell_command(["-Silent"], window)
                self.update_system_status(window)
            
            elif event == "-HEALTH-":
                window["-PROGRESS-TEXT-"].update("Running health check...")
                self.execute_powershell_command(["-Silent"], window)
                threading.Thread(target=lambda: self.execute_powershell_command(["-Silent"], window), daemon=True).start()
            
            elif event == "-ANALYZE-":
                window["-PROGRESS-TEXT-"].update("Analyzing code...")
                threading.Thread(target=lambda: self.execute_powershell_command(["-Silent"], window), daemon=True).start()
            
            elif event == "-READINESS-":
                window["-PROGRESS-TEXT-"].update("Checking project readiness...")
                threading.Thread(target=lambda: self.execute_powershell_command(["-Silent"], window), daemon=True).start()
            
            elif event == "-DIAGNOSE-":
                window["-PROGRESS-TEXT-"].update("Running system diagnostics...")
                threading.Thread(target=lambda: self.execute_powershell_command(["-Silent"], window), daemon=True).start()
            
            elif event == "-BACKUP-":
                window["-PROGRESS-TEXT-"].update("Creating backup...")
                threading.Thread(target=lambda: self.execute_powershell_command(["-Silent"], window), daemon=True).start()
            
            elif event == "-MONITOR-":
                if not self.monitoring_active:
                    window["-PROGRESS-TEXT-"].update("Starting monitoring...")
                    threading.Thread(target=lambda: self.execute_powershell_command(["-MonitorMode", "-RealTimeMode"], window), daemon=True).start()
                    self.monitoring_active = True
                else:
                    window["-PROGRESS-TEXT-"].update("Monitoring already active")
            
            elif event == "-LOGS-":
                window["-PROGRESS-TEXT-"].update("Retrieving logs...")
                threading.Thread(target=lambda: self.execute_powershell_command(["-Silent"], window), daemon=True).start()
            
            elif event == "-CLEANUP-":
                window["-PROGRESS-TEXT-"].update("Cleaning up project...")
                threading.Thread(target=lambda: self.execute_powershell_command(["-Silent"], window), daemon=True).start()
            
            # AIOS Control
            elif event == "-START-AIOS-":
                mode = values["-MODE-"]
                questions = int(values["-QUESTIONS-"])
                interactive = "-Interactive" if values["-INTERACTIVE-"] else ""
                admin = "-AdminMode" if values["-ADMIN-"] else ""
                
                args = ["-Silent", interactive, admin] if interactive or admin else ["-Silent"]
                window["-PROGRESS-TEXT-"].update(f"Starting AIOS in {mode} mode...")
                threading.Thread(target=lambda: self.execute_powershell_command(args, window), daemon=True).start()
            
            elif event == "-STOP-AIOS-":
                window["-PROGRESS-TEXT-"].update("Stopping AIOS processes...")
                # Implementation for stopping processes would go here
            
            # Utility buttons
            elif event == "-REFRESH-":
                self.update_system_status(window)
            
            elif event == "-CLEAR-":
                window["-OUTPUT-"].update("")
                window["-LINE-COUNT-"].update("Lines: 0")
            
            elif event == "-SAVE-OUTPUT-":
                output = window["-OUTPUT-"].get()
                if output:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"aios_output_{timestamp}.txt"
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(output)
                        sg.popup(f"Output saved to {filename}")
                    except Exception as e:
                        sg.popup_error(f"Error saving output: {e}")
            
            # Settings
            elif event == "-SETTINGS-":
                self.show_settings(window)
            
            # Help
            elif event == "-HELP-":
                self.show_help()
        
        # Save configuration on exit
        self.save_config()
        window.close()
    
    def show_settings(self, parent_window):
        """Show settings window"""
        settings_layout = self.create_settings_layout()
        settings_window = sg.Window("Settings", settings_layout, modal=True)
        
        while True:
            event, values = settings_window.read()
            
            if event in (sg.WIN_CLOSED, "-CANCEL-SETTINGS-"):
                break
            
            elif event == "-SAVE-SETTINGS-":
                # Update configuration
                self.config["auto_refresh"] = values["-AUTO-REFRESH-"]
                self.config["refresh_interval"] = int(values["-REFRESH-INTERVAL-"])
                self.config["max_log_lines"] = int(values["-MAX-LOG-LINES-"])
                self.config["theme"] = values["-THEME-"]
                
                # Apply theme
                sg.theme(self.config["theme"])
                
                self.save_config()
                sg.popup("Settings saved successfully!")
                break
            
            elif event == "-RESET-SETTINGS-":
                if sg.popup_yes_no("Reset all settings to defaults?", title="Confirm Reset") == "Yes":
                    self.config = self.load_config()  # Reload defaults
                    self.save_config()
                    sg.popup("Settings reset to defaults!")
                    break
        
        settings_window.close()
    
    def show_help(self):
        """Show help window"""
        help_layout = self.create_help_layout()
        help_window = sg.Window("Help", help_layout, modal=True)
        
        while True:
            event, values = help_window.read()
            if event in (sg.WIN_CLOSED,):
                break
        
        help_window.close()

def main():
    """Main entry point"""
    try:
        app = AIOSGUI()
        app.run_gui()
    except Exception as e:
        sg.popup_error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

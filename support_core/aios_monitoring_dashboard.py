#!/usr/bin/env python3
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

AIOS Visual Monitoring Dashboard
Advanced dashboard with real-time charts and system monitoring
"""

import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import time
import psutil
import json
from datetime import datetime, timedelta
from collections import deque
from utils_core.powershell_bridge import PowerShellBridge

# Set matplotlib style
plt.style.use('dark_background')

class AIOSMonitoringDashboard:
    def __init__(self):
        self.aios_root = Path(__file__).parent
        self.bridge = None
        
        # Data storage for charts
        self.cpu_data = deque(maxlen=60)  # 60 data points (1 minute at 1-second intervals)
        self.memory_data = deque(maxlen=60)
        self.disk_data = deque(maxlen=60)
        self.network_data = deque(maxlen=60)
        self.timestamps = deque(maxlen=60)
        
        # AIOS-specific metrics
        self.aios_processes = deque(maxlen=60)
        self.aios_errors = deque(maxlen=60)
        self.aios_logs = deque(maxlen=100)
        
        # Initialize data
        self.initialize_data()
        
        # Initialize PowerShell bridge
        try:
            self.bridge = PowerShellBridge(str(self.aios_root))
        except Exception as e:
            print(f"Bridge initialization error: {e}")
        
        # Monitoring control
        self.monitoring_active = False
        self.monitor_thread = None
    
    def initialize_data(self):
        """Initialize data with current system metrics"""
        current_time = datetime.now()
        
        # Get current system metrics
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
        
        # Initialize data arrays
        for i in range(60):
            self.timestamps.append(current_time - timedelta(seconds=60-i))
            self.cpu_data.append(cpu_percent)
            self.memory_data.append(memory_percent)
            self.disk_data.append(disk_percent)
            self.network_data.append(0)  # Will be updated with actual network data
            self.aios_processes.append(0)
            self.aios_errors.append(0)
    
    def create_system_charts(self):
        """Create system monitoring charts"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('AIOS System Monitoring', fontsize=16, color='white')
        
        # CPU Usage Chart
        ax1.set_title('CPU Usage (%)', color='white')
        ax1.set_ylim(0, 100)
        ax1.grid(True, alpha=0.3)
        line1, = ax1.plot([], [], color='cyan', linewidth=2)
        ax1.fill_between([], [], alpha=0.3, color='cyan')
        
        # Memory Usage Chart
        ax2.set_title('Memory Usage (%)', color='white')
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3)
        line2, = ax2.plot([], [], color='yellow', linewidth=2)
        ax2.fill_between([], [], alpha=0.3, color='yellow')
        
        # Disk Usage Chart
        ax3.set_title('Disk Usage (%)', color='white')
        ax3.set_ylim(0, 100)
        ax3.grid(True, alpha=0.3)
        line3, = ax3.plot([], [], color='green', linewidth=2)
        ax3.fill_between([], [], alpha=0.3, color='green')
        
        # Network Activity Chart
        ax4.set_title('Network Activity (MB/s)', color='white')
        ax4.set_ylim(0, 100)
        ax4.grid(True, alpha=0.3)
        line4, = ax4.plot([], [], color='magenta', linewidth=2)
        ax4.fill_between([], [], alpha=0.3, color='magenta')
        
        # Style the axes
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_facecolor('black')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
        
        return fig, (line1, line2, line3, line4), (ax1, ax2, ax3, ax4)
    
    def create_aios_charts(self):
        """Create AIOS-specific monitoring charts"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('AIOS Process Monitoring', fontsize=16, color='white')
        
        # AIOS Processes Chart
        ax1.set_title('AIOS Processes', color='white')
        ax1.set_ylim(0, 20)
        ax1.grid(True, alpha=0.3)
        line1, = ax1.plot([], [], color='orange', linewidth=2)
        
        # AIOS Errors Chart
        ax2.set_title('AIOS Errors (Last Hour)', color='white')
        ax2.set_ylim(0, 50)
        ax2.grid(True, alpha=0.3)
        line2, = ax2.plot([], [], color='red', linewidth=2)
        
        # Style the axes
        for ax in [ax1, ax2]:
            ax.set_facecolor('black')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
        
        return fig, (line1, line2), (ax1, ax2)
    
    def update_system_metrics(self):
        """Update system metrics data"""
        try:
            # Get current system metrics
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('C:').percent if os.name == 'nt' else psutil.disk_usage('/').percent
            
            # Get network I/O
            network_io = psutil.net_io_counters()
            network_mb = (network_io.bytes_sent + network_io.bytes_recv) / 1024 / 1024
            
            # Count AIOS processes
            aios_process_count = 0
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline'] and any('aios' in str(cmd).lower() for cmd in proc.info['cmdline']):
                        aios_process_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Update data
            current_time = datetime.now()
            self.timestamps.append(current_time)
            self.cpu_data.append(cpu_percent)
            self.memory_data.append(memory_percent)
            self.disk_data.append(disk_percent)
            self.network_data.append(network_mb)
            self.aios_processes.append(aios_process_count)
            self.aios_errors.append(0)  # Would be updated from actual error logs
            
        except Exception as e:
            print(f"Error updating metrics: {e}")
    
    def create_dashboard_layout(self):
        """Create the main dashboard layout"""
        
        # Create charts
        system_fig, system_lines, system_axes = self.create_system_charts()
        aios_fig, aios_lines, aios_axes = self.create_aios_charts()
        
        # Convert matplotlib figures to PySimpleGUI elements
        system_canvas = FigureCanvasTkAgg(system_fig, sg.tkinter.Tk())
        aios_canvas = FigureCanvasTkAgg(aios_fig, sg.tkinter.Tk())
        
        # Control panel
        control_frame = [
            [sg.Text("🎛️ Monitoring Controls", font=("Arial", 14, "bold"))],
            [sg.Button("▶️ Start Monitoring", key="-START-MONITORING-", button_color=("white", "green")),
             sg.Button("⏸️ Pause Monitoring", key="-PAUSE-MONITORING-", button_color=("white", "orange")),
             sg.Button("⏹️ Stop Monitoring", key="-STOP-MONITORING-", button_color=("white", "red"))],
            [sg.Checkbox("Auto-refresh charts", key="-AUTO-REFRESH-", default=True),
             sg.Slider(range=(1, 60), default_value=5, orientation='h', key="-REFRESH-RATE-", size=(20, 15))],
            [sg.Text("Refresh Rate (seconds):", key="-REFRESH-LABEL-")]
        ]
        
        # System status panel
        status_frame = [
            [sg.Text("📊 System Status", font=("Arial", 14, "bold"))],
            [sg.Text("CPU:", size=(10, 1)), sg.Text("0%", key="-CPU-VALUE-", size=(10, 1))],
            [sg.Text("Memory:", size=(10, 1)), sg.Text("0%", key="-MEMORY-VALUE-", size=(10, 1))],
            [sg.Text("Disk:", size=(10, 1)), sg.Text("0%", key="-DISK-VALUE-", size=(10, 1))],
            [sg.Text("AIOS Processes:", size=(15, 1)), sg.Text("0", key="-AIOS-PROCESSES-", size=(10, 1))],
            [sg.Text("Last Update:", size=(15, 1)), sg.Text("Never", key="-LAST-UPDATE-", size=(20, 1))]
        ]
        
        # Alerts panel
        alerts_frame = [
            [sg.Text("🚨 Alerts", font=("Arial", 14, "bold"))],
            [sg.Multiline(size=(40, 10), key="-ALERTS-", disabled=True, autoscroll=True,
                         background_color="black", text_color="red")]
        ]
        
        # Layout
        layout = [
            [sg.Text("🚀 AIOS Visual Monitoring Dashboard", font=("Arial", 18, "bold"), 
                    justification="center", size=(50, 1))],
            [sg.HSeparator()],
            
            # Control and status panels
            [sg.Column(control_frame, vertical_alignment="top"),
             sg.VSeparator(),
             sg.Column(status_frame, vertical_alignment="top"),
             sg.VSeparator(),
             sg.Column(alerts_frame, vertical_alignment="top")],
            
            [sg.HSeparator()],
            
            # System monitoring charts
            [sg.Text("📈 System Performance", font=("Arial", 14, "bold"))],
            [sg.Canvas(key="-SYSTEM-CHART-", size=(800, 600))],
            
            [sg.HSeparator()],
            
            # AIOS monitoring charts
            [sg.Text("🤖 AIOS Process Monitoring", font=("Arial", 14, "bold"))],
            [sg.Canvas(key="-AIOS-CHART-", size=(800, 400))],
            
            [sg.HSeparator()],
            
            # Bottom controls
            [sg.Button("💾 Export Data", key="-EXPORT-"),
             sg.Button("📊 Generate Report", key="-REPORT-"),
             sg.Button("⚙️ Settings", key="-SETTINGS-"),
             sg.Button("❌ Exit", key="-EXIT-", button_color=("white", "red"))]
        ]
        
        return layout, system_fig, aios_fig
    
    def start_monitoring(self, window):
        """Start the monitoring thread"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self.monitor_loop, args=(window,), daemon=True)
            self.monitor_thread.start()
            window["-ALERTS-"].update("✅ Monitoring started\n", append=True)
    
    def stop_monitoring(self, window):
        """Stop the monitoring thread"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        window["-ALERTS-"].update("⏹️ Monitoring stopped\n", append=True)
    
    def monitor_loop(self, window):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Update metrics
                self.update_system_metrics()
                
                # Update GUI elements
                if len(self.cpu_data) > 0:
                    window["-CPU-VALUE-"].update(f"{self.cpu_data[-1]:.1f}%")
                    window["-MEMORY-VALUE-"].update(f"{self.memory_data[-1]:.1f}%")
                    window["-DISK-VALUE-"].update(f"{self.disk_data[-1]:.1f}%")
                    window["-AIOS-PROCESSES-"].update(str(int(self.aios_processes[-1])))
                    window["-LAST-UPDATE-"].update(datetime.now().strftime("%H:%M:%S"))
                
                # Check for alerts
                self.check_alerts(window)
                
                # Update charts
                self.update_charts(window)
                
                # Sleep
                refresh_rate = window["-REFRESH-RATE-"].get() if window else 5
                time.sleep(refresh_rate)
                
            except Exception as e:
                error_msg = f"❌ Monitoring error: {str(e)}\n"
                window["-ALERTS-"].update(error_msg, append=True)
                time.sleep(5)  # Wait before retrying
    
    def check_alerts(self, window):
        """Check for system alerts"""
        try:
            current_time = datetime.now()
            alerts = []
            
            # CPU alert
            if len(self.cpu_data) > 0 and self.cpu_data[-1] > 80:
                alerts.append(f"⚠️ High CPU usage: {self.cpu_data[-1]:.1f}%")
            
            # Memory alert
            if len(self.memory_data) > 0 and self.memory_data[-1] > 85:
                alerts.append(f"⚠️ High memory usage: {self.memory_data[-1]:.1f}%")
            
            # Disk alert
            if len(self.disk_data) > 0 and self.disk_data[-1] > 90:
                alerts.append(f"🚨 Critical disk usage: {self.disk_data[-1]:.1f}%")
            
            # AIOS process alert
            if len(self.aios_processes) > 0 and self.aios_processes[-1] == 0:
                alerts.append("⚠️ No AIOS processes detected")
            
            # Add alerts to display
            for alert in alerts:
                timestamp = current_time.strftime("%H:%M:%S")
                alert_msg = f"[{timestamp}] {alert}\n"
                window["-ALERTS-"].update(alert_msg, append=True)
                
        except Exception as e:
            print(f"Error checking alerts: {e}")
    
    def update_charts(self, window):
        """Update the monitoring charts"""
        try:
            # This would update the matplotlib charts
            # Implementation depends on the specific chart updating mechanism
            pass
        except Exception as e:
            print(f"Error updating charts: {e}")
    
    def export_data(self):
        """Export monitoring data to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aios_monitoring_data_{timestamp}.json"
            
            data = {
                "timestamp": timestamp,
                "cpu_data": list(self.cpu_data),
                "memory_data": list(self.memory_data),
                "disk_data": list(self.disk_data),
                "network_data": list(self.network_data),
                "aios_processes": list(self.aios_processes),
                "aios_errors": list(self.aios_errors),
                "timestamps": [ts.isoformat() for ts in self.timestamps]
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            sg.popup(f"Data exported to {filename}")
            
        except Exception as e:
            sg.popup_error(f"Error exporting data: {e}")
    
    def run_dashboard(self):
        """Run the monitoring dashboard"""
        layout, system_fig, aios_fig = self.create_dashboard_layout()
        
        window = sg.Window(
            "AIOS Visual Monitoring Dashboard",
            layout,
            size=(1200, 1000),
            resizable=True,
            finalize=True
        )
        
        # Initial status update
        self.update_system_metrics()
        
        # Event loop
        while True:
            event, values = window.read(timeout=1000)
            
            if event in (sg.WIN_CLOSED, "-EXIT-"):
                break
            
            elif event == "-START-MONITORING-":
                self.start_monitoring(window)
            
            elif event == "-STOP-MONITORING-":
                self.stop_monitoring(window)
            
            elif event == "-EXPORT-":
                self.export_data()
            
            elif event == "-REPORT-":
                sg.popup("Report generation feature coming soon!")
            
            elif event == "-SETTINGS-":
                sg.popup("Settings panel coming soon!")
        
        # Stop monitoring on exit
        self.stop_monitoring(window)
        window.close()

def main():
    """Main entry point"""
    try:
        dashboard = AIOSMonitoringDashboard()
        dashboard.run_dashboard()
    except Exception as e:
        sg.popup_error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()

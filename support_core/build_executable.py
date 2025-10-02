#!/usr/bin/env python3
"""
AIOS Executable Builder
Creates standalone executables for easy distribution
"""

import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path

def build_executables():
    """Build executable files for AIOS components"""
    
    print("🚀 Building AIOS Executables...")
    
    # Ensure we're in the right directory
    aios_root = Path(__file__).parent
    os.chdir(aios_root)
    
    # Create build directory
    build_dir = aios_root / "build"
    dist_dir = aios_root / "dist"
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # Build specifications
    builds = [
        {
            "name": "AIOS Launcher",
            "script": "aios_launcher.py",
            "icon": None,  # Could add icon file here
            "onefile": True,
            "windowed": True,
            "console": False
        },
        {
            "name": "AIOS GUI",
            "script": "aios_gui.py", 
            "icon": None,
            "onefile": True,
            "windowed": True,
            "console": False
        },
        {
            "name": "AIOS Monitoring Dashboard",
            "script": "aios_monitoring_dashboard.py",
            "icon": None,
            "onefile": True,
            "windowed": True,
            "console": False
        },
        {
            "name": "AIOS Backend Integration",
            "script": "aios_backend_integration.py",
            "icon": None,
            "onefile": True,
            "windowed": False,
            "console": True
        }
    ]
    
    # Build each executable
    for build in builds:
        print(f"\n📦 Building {build['name']}...")
        
        # Prepare PyInstaller arguments
        args = [
            build["script"],
            "--name", build["name"].replace(" ", "_"),
            "--clean",
            "--noconfirm"
        ]
        
        # Add windowed mode if specified
        if build["windowed"]:
            args.append("--windowed")
        
        # Add onefile if specified
        if build["onefile"]:
            args.append("--onefile")
        
        # Add hidden imports for common packages
        hidden_imports = [
            "PySimpleGUI",
            "matplotlib.backends.backend_tkagg",
            "matplotlib.figure",
            "numpy",
            "psutil",
            "queue",
            "threading"
        ]
        
        for imp in hidden_imports:
            args.extend(["--hidden-import", imp])
        
        # Add data files if needed
        data_files = [
            ("aios_powershell_wrapper.ps1", "."),
            ("requirements_gui.txt", "."),
            ("utils", "utils")
        ]
        
        for src, dst in data_files:
            if Path(src).exists():
                args.extend(["--add-data", f"{src};{dst}"])
        
        # Run PyInstaller
        try:
            PyInstaller.__main__.run(args)
            print(f"✅ {build['name']} built successfully")
        except Exception as e:
            print(f"❌ Failed to build {build['name']}: {e}")
    
    print("\n🎉 Build process completed!")
    print(f"📁 Executables created in: {dist_dir}")
    
    # Create distribution package
    create_distribution_package(dist_dir)

def create_distribution_package(dist_dir):
    """Create a complete distribution package"""
    
    print("\n📦 Creating distribution package...")
    
    package_dir = Path("AIOS_Distribution")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy executables
    for exe_file in dist_dir.glob("*.exe"):
        shutil.copy2(exe_file, package_dir)
        print(f"✅ Copied {exe_file.name}")
    
    # Copy PowerShell wrapper
    if Path("aios_powershell_wrapper.ps1").exists():
        shutil.copy2("aios_powershell_wrapper.ps1", package_dir)
        print("✅ Copied PowerShell wrapper")
    
    # Create README
    create_readme(package_dir)
    
    # Create batch files for easy launching
    create_launcher_scripts(package_dir)
    
    print(f"\n🎉 Distribution package created: {package_dir}")
    print("📋 Contents:")
    for item in package_dir.iterdir():
        print(f"   • {item.name}")

def create_readme(package_dir):
    """Create README for distribution"""
    
    readme_content = """
# AIOS PowerShell Backend Monitor - Distribution Package

## 🚀 Quick Start

### Option 1: GUI Launcher (Recommended)
1. Double-click `AIOS_Launcher.exe`
2. Choose your preferred interface
3. Click "Install GUI Dependencies" if prompted
4. Launch your chosen interface

### Option 2: Direct Launch
- **GUI Interface**: Double-click `AIOS_GUI.exe`
- **Monitoring Dashboard**: Double-click `AIOS_Monitoring_Dashboard.exe`
- **Backend Integration**: Double-click `AIOS_Backend_Integration.exe`

### Option 3: PowerShell CLI
1. Right-click in the folder and select "Open PowerShell window here"
2. Run: `.\aios_powershell_wrapper.ps1 -AdminMode -DebugMode`

## 🎛️ Available Interfaces

### GUI Interface
- User-friendly graphical interface
- Real-time output display
- Easy command execution
- Configuration management

### Monitoring Dashboard
- Real-time system performance charts
- Visual monitoring with graphs
- Alert system for system issues
- Data export capabilities

### PowerShell CLI
- Full command-line access
- Admin mode capabilities
- Advanced system control
- Script automation

## 🔧 System Requirements

- Windows 10/11
- PowerShell 5.1 or later
- .NET Framework 4.7.2 or later
- 4GB RAM minimum
- 1GB free disk space

## 📋 Available Commands

- `aios` - Start AIOS interactively
- `status` - System status check
- `health` - Health diagnostics
- `monitor` - Real-time monitoring
- `analyze` - Code analysis
- `diagnose` - System diagnostics
- `readiness` - Project readiness check
- `cleanup` - Project cleanup
- `logs` - View logs
- `backup` - Create backup

## 🛡️ Admin Mode

When using Admin Mode:
- Full system access granted
- Process management capabilities
- File system control
- Security scanning
- Backup and restore

## ❓ Troubleshooting

### GUI Issues
- Ensure all dependencies are installed
- Check Windows Defender settings
- Run as administrator if needed

### PowerShell Issues
- Check execution policy: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Ensure PowerShell is updated
- Run as administrator for admin features

### Performance Issues
- Close other applications
- Check available disk space
- Monitor system resources

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the log files
3. Run system diagnostics
4. Contact support with error details

---
**AIOS PowerShell Backend Monitor** - Enterprise-grade system monitoring and management
    """
    
    readme_file = package_dir / "README.txt"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README.txt")

def create_launcher_scripts(package_dir):
    """Create batch files for easy launching"""
    
    # GUI Launcher batch file
    gui_bat_content = """@echo off
echo Starting AIOS GUI Launcher...
AIOS_Launcher.exe
pause
"""
    
    gui_bat = package_dir / "Launch_GUI.bat"
    with open(gui_bat, 'w') as f:
        f.write(gui_bat_content)
    
    # PowerShell CLI batch file
    ps_bat_content = """@echo off
echo Starting AIOS PowerShell CLI...
powershell -ExecutionPolicy Bypass -File "aios_powershell_wrapper.ps1" -AdminMode -DebugMode
pause
"""
    
    ps_bat = package_dir / "Launch_PowerShell.bat"
    with open(ps_bat, 'w') as f:
        f.write(ps_bat_content)
    
    print("✅ Created launcher batch files")

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False

def main():
    """Main build function"""
    print("🚀 AIOS Executable Builder")
    print("=" * 40)
    
    # Check if PyInstaller is available
    if not install_pyinstaller():
        print("❌ Cannot proceed without PyInstaller")
        return
    
    # Build executables
    try:
        build_executables()
        print("\n🎉 Build completed successfully!")
        print("\n📋 Next steps:")
        print("1. Test the executables in the dist/ folder")
        print("2. Copy the AIOS_Distribution folder to target machines")
        print("3. Run Launch_GUI.bat or Launch_PowerShell.bat")
        
    except Exception as e:
        print(f"❌ Build failed: {e}")

if __name__ == "__main__":
    main()

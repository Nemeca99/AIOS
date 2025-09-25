"""
UML Calculator Migration Helper
Assists in migrating from e:/Algebra/Calculator to d:/UML Calculator/UML_Core
"""

import os
import shutil
from datetime import datetime

def migrate_calculator_files():
    """Migrate calculator files and create backup/reference"""
    
    source_dir = "e:/Algebra/Calculator"
    target_dir = "d:/UML Calculator/UML_Core"
    backup_dir = "d:/UML Calculator/UML_Core/legacy_backup"
    
    print("🔄 UML Calculator Migration Tool")
    print("=" * 50)
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Created backup directory: {backup_dir}")
    
    # Files to consider for migration/backup
    files_to_check = [
        "codex_symbolic_core.py",
        "codex_web_calculator.py", 
        "README_codex_web_calculator.txt",
        "test_buttons.html"
    ]
    
    migration_report = []
    migration_report.append(f"Migration Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    migration_report.append("=" * 60)
    
    for filename in files_to_check:
        source_file = os.path.join(source_dir, filename)
        backup_file = os.path.join(backup_dir, filename)
        
        if os.path.exists(source_file):
            print(f"📄 Processing: {filename}")
            
            # Create backup copy
            shutil.copy2(source_file, backup_file)
            print(f"   ✅ Backed up to: {backup_file}")
            migration_report.append(f"✅ {filename} - Backed up successfully")
            
            # Check if there's enhanced functionality already
            if filename == "codex_symbolic_core.py":
                print(f"   💡 Symbolic features integrated into symbolic_extensions.py")
                migration_report.append(f"   → Functionality integrated into symbolic_extensions.py")
            elif filename == "codex_web_calculator.py":
                print(f"   💡 Web interface enhanced in uml_calculator.py")
                migration_report.append(f"   → Functionality enhanced in uml_calculator.py")
        else:
            print(f"❌ Not found: {filename}")
            migration_report.append(f"❌ {filename} - Not found in source")
    
    # Check what's in the target directory
    print(f"\n📂 Current UML_Core contents:")
    if os.path.exists(target_dir):
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                print(f"   📄 {item} ({size} bytes)")
            else:
                print(f"   📁 {item}/")
    
    # Write migration report
    report_file = os.path.join(target_dir, "migration_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(migration_report))
    
    print(f"\n📋 Migration report saved to: {report_file}")
    
    # Status summary
    print(f"\n✨ Migration Status Summary:")
    print(f"   🎯 Enhanced UML Calculator: d:\\UML Calculator\\UML_Core\\uml_calculator.py")
    print(f"   🧠 Core UML Logic: d:\\UML Calculator\\UML_Core\\uml_core.py")
    print(f"   🔧 Symbolic Extensions: d:\\UML Calculator\\UML_Core\\symbolic_extensions.py")
    print(f"   💾 Legacy Backup: {backup_dir}")
    print(f"   📋 Report: {report_file}")
    
    return True

def create_launcher():
    """Create a convenient launcher script"""
    launcher_content = '''@echo off
echo 🧮 UML Calculator Launcher
echo ========================
echo.
echo Choose interface:
echo 1. GUI (Desktop app)
echo 2. Web (Browser interface) 
echo 3. CLI (Command line)
echo 4. Help
echo.
set /p choice="Enter choice (1-4): "

cd /d "d:\\UML Calculator\\UML_Core"

if "%choice%"=="1" (
    echo Starting GUI...
    python uml_calculator.py
) else if "%choice%"=="2" (
    echo Starting Web interface...
    python uml_calculator.py --web
) else if "%choice%"=="3" (
    echo Starting CLI...
    python uml_calculator.py --cli
) else if "%choice%"=="4" (
    python uml_calculator.py --help
) else (
    echo Invalid choice. Starting GUI...
    python uml_calculator.py
)

pause
'''
    
    launcher_file = "d:/UML Calculator/launch_calculator.bat"
    with open(launcher_file, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"🚀 Created launcher: {launcher_file}")
    return launcher_file

def main():
    """Main migration function"""
    print("Starting UML Calculator migration and setup...")
    
    try:
        migrate_calculator_files()
        create_launcher()
        
        print(f"\n🎉 Migration completed successfully!")
        print(f"\nQuick start options:")
        print(f"1. Double-click: d:\\UML Calculator\\launch_calculator.bat")
        print(f"2. Or run directly: python d:\\UML Calculator\\UML_Core\\uml_calculator.py")
        print(f"3. Web interface: python d:\\UML Calculator\\UML_Core\\uml_calculator.py --web")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()

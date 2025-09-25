#!/usr/bin/env python3
"""
AIOS Test Runner - DoctorWho Reference
This is the ONLY test runner file you need. 
Runs Testing/test_aios_system.bat and reports clean results.
Use this file for all AIOS system validation.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_aios_tests():
    """Run AIOS system tests and report results"""
    print("🚀 AIOS Test Runner")
    print("=" * 40)
    
    test_file = Path(__file__).parent.parent / "Testing" / "test_aios_system.bat"
    aios_root = Path(__file__).parent.parent
    
    try:
        print("Running comprehensive AIOS system tests...")
        
        # Run the working batch file
        result = subprocess.run(
            [str(test_file)],
            cwd=str(aios_root),
            shell=True
        )
        
        if result.returncode == 0:
            print("✅ AIOS system tests completed successfully")
            print("📋 Check Data/logs/ for detailed test results")
            return 0
        else:
            print("⚠️ AIOS system tests completed with some issues")
            print("📋 Check Data/logs/ for detailed error information")
            return 1
            
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        return 2

if __name__ == "__main__":
    exit_code = run_aios_tests()
    
    # Show latest log file
    log_dir = Path(__file__).parent.parent / "Data" / "logs"
    log_files = sorted(log_dir.glob("system_test_*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if log_files:
        latest_log = log_files[0]
        print(f"📄 Latest test log: {latest_log}")
        
        # Count results from log
        try:
            with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                passed = content.count("PASS:")
                failed = content.count("ERROR:")
                skipped = content.count("SKIP:")
            
            print(f"📊 Results: {passed} passed, {failed} failed, {skipped} skipped")
            
        except Exception as e:
            print(f"Could not parse log: {e}")
    
    sys.exit(exit_code)

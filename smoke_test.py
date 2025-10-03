#!/usr/bin/env python3
"""
AIOS Clean Smoke Test
Minimal CI smoke test that validates core functionality
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🧪 Testing: {description}")
    full_cmd = [sys.executable] + cmd
    print(f"   Command: {' '.join(full_cmd)}")
    
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"   ✅ PASS")
            return True
        else:
            print(f"   ❌ FAIL (exit code: {result.returncode})")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ❌ FAIL (timeout)")
        return False
    except Exception as e:
        print(f"   ❌ FAIL (exception: {e})")
        return False

def main():
    """Run smoke tests."""
    print("🚀 AIOS Clean Smoke Test")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    tests = [
        (["main.py", "--system", "--config-health"], "Configuration health check"),
        (["main.py", "--system", "--luna", "--whoami"], "Luna whoami command"),
        (["main.py", "--system", "--carma", "--whoami"], "CARMA whoami command"),
        (["main.py", "--system", "--support", "--whoami"], "Support whoami command"),
        (["main.py", "--system", "--show-models"], "Show all model configurations"),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, description in tests:
        if run_command(cmd, description):
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All smoke tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

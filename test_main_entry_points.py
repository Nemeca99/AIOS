#!/usr/bin/env python3
"""
Main Entry Point Validation - Test all CLI interfaces work
"""

import subprocess
import sys

print("="*80)
print("MAIN ENTRY POINT VALIDATION")
print("="*80)

tests = [
    ("main.py --help", "Main CLI help"),
    ("main.py --luna --status", "Luna status"),
    ("main.py --carma --status", "CARMA status"),
    ("main.py --support --health", "Support health check"),
    ("main.py --whoami", "System identity"),
]

passed = 0
failed = []

for cmd, description in tests:
    print(f"\nTesting: {description}")
    print(f"Command: py {cmd}")
    
    try:
        result = subprocess.run(
            f"py {cmd}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"  [OK] PASS (exit code 0)")
            passed += 1
        else:
            print(f"  [FAIL] FAIL (exit code {result.returncode})")
            if result.stderr:
                print(f"     Error: {result.stderr[:100]}")
            failed.append((cmd, result.returncode))
            
    except subprocess.TimeoutExpired:
        print(f"  [FAIL] TIMEOUT (>30s)")
        failed.append((cmd, "timeout"))
    except Exception as e:
        print(f"  [FAIL] ERROR: {e}")
        failed.append((cmd, str(e)))

print("\n" + "="*80)
print(f"RESULTS: {passed}/{len(tests)} tests passed")
print("="*80)

if failed:
    print(f"\n[FAIL] FAILED TESTS:")
    for cmd, error in failed:
        print(f"   {cmd}: {error}")
    sys.exit(1)
else:
    print("\n[OK] ALL ENTRY POINTS WORKING!")
    sys.exit(0)


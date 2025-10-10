#!/usr/bin/env python3
"""
Rust Module Validation - Test all 6 Rust modules load and work
"""

import sys
from pathlib import Path

print("="*80)
print("RUST MODULE VALIDATION")
print("="*80)

rust_modules = [
    ('utils', 'utils_core/rust_utils/target/release', 'aios_utils_rust'),
    ('carma', 'carma_core/rust_carma/target/release', 'aios_carma_rust'),
    ('luna', 'luna_core/rust_luna/target/release', 'aios_luna_rust'),
    ('dream', 'dream_core/rust_dream/target/release', 'aios_dream_rust'),
    ('support', 'support_core/rust_support/target/release', 'aios_support_rust'),
    ('backup', 'backup_core/rust_backup/target/release', 'aios_backup_rust'),
]

loaded = []
failed = []

for name, path, module_name in rust_modules:
    print(f"\nTesting {name} ({module_name})...")
    
    # Check if PYD file exists
    pyd_file = Path(path) / f"{module_name}.pyd"
    if not pyd_file.exists():
        print(f"  ❌ PYD file not found: {pyd_file}")
        failed.append((name, "PYD file missing"))
        continue
    
    print(f"  ✅ PYD file exists ({pyd_file.stat().st_size / 1024:.1f} KB)")
    
    # Try to load module
    sys.path.insert(0, path)
    try:
        module = __import__(module_name)
        print(f"  ✅ Module loaded successfully")
        
        # List exposed functions
        functions = [x for x in dir(module) if not x.startswith('_')]
        print(f"  ✅ Exposed functions: {len(functions)}")
        if functions:
            print(f"     {', '.join(functions[:5])}{' ...' if len(functions) > 5 else ''}")
        
        loaded.append((name, module))
        
    except Exception as e:
        print(f"  ❌ FAILED to load: {type(e).__name__}: {e}")
        failed.append((name, str(e)))
    finally:
        sys.path.remove(path)

print("\n" + "="*80)
print(f"RESULTS: {len(loaded)}/{len(rust_modules)} Rust modules loaded")
print("="*80)

if loaded:
    print("\n✅ LOADED MODULES:")
    for name, module in loaded:
        print(f"   {name}")

if failed:
    print(f"\n❌ FAILED MODULES ({len(failed)}):")
    for name, error in failed:
        print(f"   {name}: {error}")

if len(loaded) == len(rust_modules):
    print("\n✅ ALL RUST MODULES WORKING!")
    sys.exit(0)
else:
    print(f"\n⚠️  {len(loaded)}/{len(rust_modules)} modules loaded")
    sys.exit(1)


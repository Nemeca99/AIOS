#!/usr/bin/env python3
"""
Fast Import Test - Only test core module entry points
"""

import sys
from pathlib import Path

print("="*80)
print("FAST IMPORT TEST - Core Module Entry Points")
print("="*80)

errors = []

# Test only the main module files, not every subfile
tests = [
    ("carma_core", lambda: __import__('carma_core.carma_core')),
    ("carma_core.fast_carma", lambda: __import__('carma_core.implementations.fast_carma')),
    ("luna_core", lambda: __import__('luna_core.core.luna_core')),
    ("luna_core.personality", lambda: __import__('luna_core.core.personality')),
    ("support_core", lambda: __import__('support_core.support_core')),
    ("utils_core.rust_bridge", lambda: __import__('utils_core.bridges.rust_bridge')),
    ("utils_core.validation", lambda: __import__('utils_core.validation.file_standards')),
    ("dream_core", lambda: __import__('dream_core.dream_core')),
    ("data_core", lambda: __import__('data_core.data_core')),
    ("enterprise_core", lambda: __import__('enterprise_core.enterprise_core')),
    ("rag_core.simple_rag", lambda: __import__('rag_core.simple_rag')),
]

for name, import_func in tests:
    try:
        print(f"Testing {name}...", end=" ")
        import_func()
        print("✅")
    except Exception as e:
        print(f"❌ {type(e).__name__}: {str(e)[:80]}")
        errors.append((name, e))

print("\n" + "="*80)
if not errors:
    print("✅ ALL CORE MODULES IMPORT SUCCESSFULLY")
    sys.exit(0)
else:
    print(f"❌ FAILED: {len(errors)} modules have import errors")
    for name, error in errors:
        print(f"  {name}: {type(error).__name__}")
    sys.exit(1)


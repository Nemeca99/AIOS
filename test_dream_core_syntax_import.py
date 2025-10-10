#!/usr/bin/env python3
"""
dream_core: Syntax & Import Validation  
Tests all dream_core Python files
"""

import ast
import importlib
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("dream_core: SYNTAX & IMPORT VALIDATION")
print("=" * 80)

files_to_test = [
    "dream_core/__init__.py",
    "dream_core/dream_core.py",
    "dream_core/core_functions/__init__.py",
    "dream_core/core_functions/config_loader.py",
    "dream_core/core_functions/dream_cycles.py",
    "dream_core/core_functions/meditation.py",
    "dream_core/core_functions/memory_consolidation.py",
    "dream_core/core_functions/middleware.py",
    "dream_core/extra/hybrid_dream_core.py",
    "dream_core/extra/dream_state_middleware.py",
    "dream_core/extra/model_config.py"
]

results = {
    "test_date": datetime.now().isoformat(),
    "folder": "dream_core",
    "total_files": len(files_to_test),
    "syntax_errors": [],
    "import_errors": [],
    "files_passed": [],
    "files_failed": []
}

print(f"\nTesting {len(files_to_test)} files...\n")

for file_path in files_to_test:
    print(f"Testing: {file_path}...", end=" ")
    full_path = Path(file_path)
    
    if not full_path.exists():
        print(f"❌ NOT FOUND")
        results["files_failed"].append(file_path)
        results["import_errors"].append({"file": file_path, "error": "Not found"})
        continue
    
    # Syntax
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
    except Exception as e:
        print(f"❌ SYNTAX")
        results["syntax_errors"].append({"file": file_path, "error": str(e)[:100]})
        results["files_failed"].append(file_path)
        continue
    
    # Import
    try:
        module_path = str(full_path.with_suffix('')).replace('/', '.').replace('\\', '.')
        if module_path.endswith('.__init__'):
            module_path = module_path[:-9]
        
        importlib.import_module(module_path)
        print("✅")
        results["files_passed"].append(file_path)
    except Exception as e:
        print(f"❌ IMPORT")
        results["import_errors"].append({"file": file_path, "error": str(e)[:200]})
        results["files_failed"].append(file_path)

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total: {results['total_files']}")
print(f"✅ Passed: {len(results['files_passed'])}")
print(f"❌ Failed: {len(results['files_failed'])}")

if results['import_errors']:
    print("\n❌ IMPORT ERRORS:")
    for error in results['import_errors'][:10]:
        print(f"  {error['file']}: {error['error'][:100]}")

with open("dream_core_syntax_import_results.json", 'w') as f:
    json.dump(results, f, indent=2)

if results['syntax_errors'] or results['import_errors']:
    print("\n❌ FAILED")
    sys.exit(1)
else:
    print("\n✅ PASSED")
    sys.exit(0)


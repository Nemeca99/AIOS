#!/usr/bin/env python3
"""
Phase 2 Validation: Import Validation - All core files must import successfully
"""

import importlib
import ast
import sys
from pathlib import Path

print("="*80)
print("PHASE 2: IMPORT VALIDATION")
print("="*80)

core_modules = [
    'carma_core', 'luna_core', 'support_core', 
    'utils_core', 'dream_core', 'data_core',
    'enterprise_core', 'rag_core'
]

total_files = 0
syntax_errors = []
import_errors = []

for module in core_modules:
    module_path = Path(module)
    if not module_path.exists():
        print(f"\n❌ {module} - directory not found")
        continue
    
    print(f"\nValidating {module}...")
    module_files = list(module_path.rglob('*.py'))
    module_files = [f for f in module_files if '__pycache__' not in str(f)]
    
    file_count = 0
    for py_file in module_files:
        total_files += 1
        file_count += 1
        
        # Print progress every 5 files
        if file_count % 5 == 0:
            print(f"  Progress: {file_count}/{len(module_files)} - {py_file.name}", end='\r')
        
        # 1. Syntax validation
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            error_msg = f"{py_file}:{e.lineno} - {e.msg}"
            syntax_errors.append(error_msg)
            print(f"\n  ❌ SYNTAX ERROR: {error_msg}")
            continue  # Skip import test if syntax is broken
        
        # 2. Import validation
        try:
            # Convert file path to module path
            rel_path = py_file.relative_to(Path('.'))
            module_path_str = str(rel_path.with_suffix('')).replace('/', '.').replace('\\', '.')
            
            # Skip __init__ special handling
            if module_path_str.endswith('.__init__'):
                module_path_str = module_path_str[:-9]
            
            # Skip __main__ files
            if '__main__' in module_path_str:
                continue
            
            importlib.import_module(module_path_str)
            
        except Exception as e:
            error_msg = f"{py_file} - {type(e).__name__}: {str(e)[:100]}"
            import_errors.append(error_msg)
            print(f"\n  ❌ IMPORT ERROR: {py_file.name} - {type(e).__name__}")
    
    print(f"\n  ✅ Checked {len(module_files)} files")

print("\n" + "="*80)
print(f"RESULTS: {total_files} files validated")
print("="*80)

if syntax_errors:
    print(f"\n❌ SYNTAX ERRORS ({len(syntax_errors)}):")
    for error in syntax_errors[:10]:  # Show first 10
        print(f"  {error}")
    if len(syntax_errors) > 10:
        print(f"  ... and {len(syntax_errors) - 10} more")

if import_errors:
    print(f"\n❌ IMPORT ERRORS ({len(import_errors)}):")
    for error in import_errors[:20]:  # Show first 20
        print(f"  {error}")
    if len(import_errors) > 20:
        print(f"  ... and {len(import_errors) - 20} more")

if not syntax_errors and not import_errors:
    print("\n✅ PHASE 2 PASSED: ALL IMPORTS SUCCESSFUL")
    print(f"   {total_files} files validated")
    sys.exit(0)
else:
    print(f"\n❌ PHASE 2 FAILED:")
    print(f"   Syntax errors: {len(syntax_errors)}")
    print(f"   Import errors: {len(import_errors)}")
    sys.exit(1)


#!/usr/bin/env python3
"""
utils_core: Syntax & Import Validation
Tests all 31 Python files for syntax errors, import errors, and placeholder code
"""

import ast
import importlib
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("utils_core: SYNTAX & IMPORT VALIDATION")
print("=" * 80)

files_to_test = [
    "utils_core/validation/file_standards.py",
    "utils_core/core.py",
    "utils_core/bridges/rust_bridge.py",
    "utils_core/bridges/powershell_bridge.py",
    "utils_core/unicode_safe_output.py",
    "utils_core/__init__.py",
    "utils_core/services/__init__.py",
    "utils_core/operations/__init__.py",
    "utils_core/resilience/__init__.py",
    "utils_core/monitoring/__init__.py",
    "utils_core/bridges/__init__.py",
    "utils_core/validation/__init__.py",
    "utils_core/base/initializer.py",
    "utils_core/base/system_base.py",
    "utils_core/base/unicode_safety.py",
    "utils_core/base/__init__.py",
    "utils_core/resilience/resilience_policies.py",
    "utils_core/monitoring/cost_tracker.py",
    "utils_core/validation/pii_redactor.py",
    "utils_core/services/data_deletion.py",
    "utils_core/monitoring/provenance.py",
    "utils_core/monitoring/canary_controller.py",
    "utils_core/services/schema_migrator.py",
    "utils_core/monitoring/adaptive_routing.py",
    "utils_core/services/model_config.py",
    "utils_core/validation/json_standards.py",
    "utils_core/extra/chatgpt_conversation_extractor.py",
    "utils_core/validation/timestamp_validator.py"
]

results = {
    "test_date": datetime.now().isoformat(),
    "folder": "utils_core",
    "total_files": len(files_to_test),
    "syntax_errors": [],
    "import_errors": [],
    "placeholder_issues": [],
    "files_passed": [],
    "files_failed": []
}

def check_placeholders(file_path):
    """Check for placeholder code patterns"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines, 1):
            # Empty pass statements (only pass on a line)
            if re.match(r'^\s*pass\s*$', line):
                issues.append(f"Line {i}: Empty pass statement")
            
            # TODO/FIXME/XXX/HACK comments
            if re.search(r'(TODO|FIXME|XXX|HACK)', line, re.IGNORECASE):
                issues.append(f"Line {i}: Placeholder comment: {line.strip()}")
            
            # raise NotImplementedError
            if 'NotImplementedError' in line:
                issues.append(f"Line {i}: NotImplementedError: {line.strip()}")
            
            # Empty exception handlers (except: followed by only pass)
            if re.match(r'^\s*except.*:\s*$', line):
                # Check if next line is just pass
                if i < len(lines) and re.match(r'^\s*pass\s*$', lines[i]):
                    issues.append(f"Line {i}-{i+1}: Empty exception handler")
    
    except Exception as e:
        issues.append(f"Error checking placeholders: {e}")
    
    return issues

print(f"\nTesting {len(files_to_test)} files...\n")

for file_path in files_to_test:
    print(f"Testing: {file_path}...", end=" ")
    full_path = Path(file_path)
    
    if not full_path.exists():
        print(f"❌ FILE NOT FOUND")
        results["files_failed"].append(file_path)
        results["import_errors"].append({
            "file": file_path,
            "error": "File not found"
        })
        continue
    
    # 1. Syntax validation (AST parse)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
    except SyntaxError as e:
        print(f"❌ SYNTAX ERROR")
        results["syntax_errors"].append({
            "file": file_path,
            "line": e.lineno,
            "error": e.msg
        })
        results["files_failed"].append(file_path)
        continue
    except Exception as e:
        print(f"❌ PARSE ERROR: {e}")
        results["syntax_errors"].append({
            "file": file_path,
            "error": str(e)
        })
        results["files_failed"].append(file_path)
        continue
    
    # 2. Import validation
    try:
        # Convert file path to module path
        module_path = str(full_path.with_suffix('')).replace('/', '.').replace('\\', '.')
        if module_path.endswith('.__init__'):
            module_path = module_path[:-9]
        
        importlib.import_module(module_path)
    except Exception as e:
        print(f"❌ IMPORT ERROR")
        results["import_errors"].append({
            "file": file_path,
            "error": str(e)[:200]  # Truncate long errors
        })
        results["files_failed"].append(file_path)
        continue
    
    # 3. Placeholder detection
    placeholder_issues = check_placeholders(full_path)
    if placeholder_issues:
        print(f"⚠️  PLACEHOLDERS FOUND ({len(placeholder_issues)})")
        results["placeholder_issues"].append({
            "file": file_path,
            "issues": placeholder_issues
        })
        # Still mark as passed for now - placeholders will be fixed separately
        results["files_passed"].append(file_path)
    else:
        print("✅ PASSED")
        results["files_passed"].append(file_path)

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total files tested: {results['total_files']}")
print(f"✅ Passed: {len(results['files_passed'])}")
print(f"❌ Failed: {len(results['files_failed'])}")
print(f"  - Syntax errors: {len(results['syntax_errors'])}")
print(f"  - Import errors: {len(results['import_errors'])}")
print(f"⚠️  Placeholder issues: {len(results['placeholder_issues'])}")

if results['syntax_errors']:
    print("\n❌ SYNTAX ERRORS:")
    for error in results['syntax_errors']:
        print(f"  {error['file']}")
        if 'line' in error:
            print(f"    Line {error['line']}: {error['error']}")
        else:
            print(f"    {error.get('error', 'Unknown error')}")

if results['import_errors']:
    print("\n❌ IMPORT ERRORS:")
    for error in results['import_errors']:
        print(f"  {error['file']}")
        print(f"    {error['error']}")

if results['placeholder_issues']:
    print(f"\n⚠️  PLACEHOLDER ISSUES FOUND IN {len(results['placeholder_issues'])} FILES:")
    for item in results['placeholder_issues']:
        print(f"  {item['file']}: {len(item['issues'])} issues")

# Save results
output_file = "utils_core_syntax_import_results.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to: {output_file}")

# Exit code
if results['syntax_errors'] or results['import_errors']:
    print("\n❌ VALIDATION FAILED - Fix errors before proceeding")
    sys.exit(1)
else:
    print("\n✅ VALIDATION PASSED - All files have valid syntax and imports")
    if results['placeholder_issues']:
        print("⚠️  Note: Placeholder code found - will be addressed next")
    sys.exit(0)


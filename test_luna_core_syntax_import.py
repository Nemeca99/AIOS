#!/usr/bin/env python3
"""
luna_core: Syntax & Import Validation
Tests all 34 Python files - the largest core module
"""

import ast
import importlib
import sys
import json
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("luna_core: SYNTAX & IMPORT VALIDATION")
print("=" * 80)

files_to_test = [
    # Core modules
    "luna_core/__init__.py",
    "luna_core/hybrid_luna_core.py",
    "luna_core/model_config.py",
    "luna_core/core/__init__.py",
    "luna_core/core/luna_core.py",
    "luna_core/core/personality.py",
    "luna_core/core/learning_system.py",
    "luna_core/core/response_generator.py",
    "luna_core/core/utils.py",
    "luna_core/core/enums_and_dataclasses.py",
    "luna_core/core/emergence_zone.py",
    # Systems
    "luna_core/systems/__init__.py",
    "luna_core/systems/luna_arbiter_system.py",
    "luna_core/systems/luna_ifs_personality_system.py",
    "luna_core/systems/luna_custom_inference_controller.py",
    "luna_core/systems/luna_existential_budget_system.py",
    "luna_core/systems/luna_response_value_classifier.py",
    "luna_core/systems/llm_performance_evaluator.py",
    "luna_core/systems/luna_internal_reasoning_system.py",
    "luna_core/systems/luna_cfia_system.py",
    "luna_core/systems/luna_trait_classifier.py",
    "luna_core/systems/luna_token_time_econometric_system.py",
    "luna_core/systems/luna_soul_metric_system.py",
    "luna_core/systems/luna_semantic_compression_filter.py",
    # Prompts
    "luna_core/prompts/__init__.py",
    "luna_core/prompts/prompt_builder.py",
    "luna_core/prompts/luna_ava_authentic_prompt_builder.py",
    "luna_core/prompts/first_word_selector.py",
    # Utilities
    "luna_core/utilities/__init__.py",
    "luna_core/utilities/enhanced_lesson_retrieval.py",
    "luna_core/utilities/dynamic_llm_parameters.py",
    "luna_core/utilities/luna_question_generator.py",
    "luna_core/utilities/bigfive_question_loader.py",
    # Extra
    "luna_core/extra/scripts/luna_infinite_learning.py"
]

results = {
    "test_date": datetime.now().isoformat(),
    "folder": "luna_core",
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
            if re.match(r'^\s*pass\s*$', line):
                issues.append(f"Line {i}: Empty pass")
            if re.search(r'(TODO|FIXME|XXX|HACK)', line, re.IGNORECASE):
                issues.append(f"Line {i}: Placeholder comment")
            if 'NotImplementedError' in line:
                issues.append(f"Line {i}: NotImplementedError")
    except Exception as e:
        issues.append(f"Error: {e}")
    return issues

print(f"\nTesting {len(files_to_test)} files...\n")

for file_path in files_to_test:
    print(f"Testing: {file_path}...", end=" ")
    full_path = Path(file_path)
    
    if not full_path.exists():
        print(f"❌ NOT FOUND")
        results["files_failed"].append(file_path)
        results["import_errors"].append({"file": file_path, "error": "Not found"})
        continue
    
    # 1. Syntax
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
    except SyntaxError as e:
        print(f"❌ SYNTAX")
        results["syntax_errors"].append({"file": file_path, "line": e.lineno, "error": e.msg})
        results["files_failed"].append(file_path)
        continue
    except Exception as e:
        print(f"❌ PARSE")
        results["syntax_errors"].append({"file": file_path, "error": str(e)})
        results["files_failed"].append(file_path)
        continue
    
    # 2. Import
    try:
        module_path = str(full_path.with_suffix('')).replace('/', '.').replace('\\', '.')
        if module_path.endswith('.__init__'):
            module_path = module_path[:-9]
        
        importlib.import_module(module_path)
    except Exception as e:
        print(f"❌ IMPORT")
        results["import_errors"].append({"file": file_path, "error": str(e)[:200]})
        results["files_failed"].append(file_path)
        continue
    
    # 3. Placeholders
    placeholder_issues = check_placeholders(full_path)
    if placeholder_issues:
        print(f"⚠️  ({len(placeholder_issues)})")
        results["placeholder_issues"].append({"file": file_path, "issues": placeholder_issues})
        results["files_passed"].append(file_path)
    else:
        print("✅")
        results["files_passed"].append(file_path)

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total: {results['total_files']}")
print(f"✅ Passed: {len(results['files_passed'])}")
print(f"❌ Failed: {len(results['files_failed'])}")
print(f"  Syntax: {len(results['syntax_errors'])}")
print(f"  Import: {len(results['import_errors'])}")
print(f"⚠️  Placeholders: {len(results['placeholder_issues'])}")

if results['import_errors']:
    print("\n❌ IMPORT ERRORS:")
    for error in results['import_errors'][:10]:
        print(f"  {error['file']}: {error['error'][:100]}")

with open("luna_core_syntax_import_results.json", 'w') as f:
    json.dump(results, f, indent=2)

if results['syntax_errors'] or results['import_errors']:
    print("\n❌ VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n✅ VALIDATION PASSED")
    sys.exit(0)


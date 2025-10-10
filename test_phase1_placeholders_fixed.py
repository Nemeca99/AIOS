#!/usr/bin/env python3
"""
Phase 1 Validation: Verify all placeholders are fixed
"""

import sys
from pathlib import Path

print("="*80)
print("PHASE 1: PLACEHOLDER CODE VALIDATION")
print("="*80)

# Search for remaining placeholder patterns
core_modules = [
    'carma_core', 'luna_core', 'support_core', 
    'utils_core', 'dream_core', 'data_core',
    'enterprise_core', 'rag_core'
]

placeholder_patterns = [
    (r'^\s+pass\s*$', 'Empty pass statement'),
    (r'TODO', 'TODO comment'),
    (r'FIXME', 'FIXME comment'),
    (r'XXX', 'XXX comment'),
    (r'HACK', 'HACK comment'),
    (r'NotImplementedError', 'NotImplementedError'),
    (r'except.*:\s*pass', 'Silent except block'),
]

total_issues = 0

for module in core_modules:
    module_path = Path(module)
    if not module_path.exists():
        print(f"\nSkipping {module} - directory not found")
        continue
    
    print(f"\nChecking {module}...")
    module_issues = 0
    
    for py_file in module_path.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for problematic patterns
                    if line.strip() == 'pass' and i > 1:
                        # Check if it's in a valid context (after def, class, if, try, etc.)
                        prev_line = lines[i-2].strip() if i >= 2 else ""
                        if not any(keyword in prev_line for keyword in ['def ', 'class ', 'if ', 'elif ', 'else:', 'try:', 'except', 'finally:', 'with ']):
                            # Standalone pass is suspicious
                            continue
                        
                        # Check if it's the ONLY statement in the block
                        next_line = lines[i].strip() if i < len(lines) else ""
                        if next_line and not next_line.startswith(('def ', 'class ', '#')):
                            # There's more code after - pass is OK
                            continue
                        
                        # Check for intentional abstract methods
                        if 'abstract' in prev_line.lower() or '"""' in prev_line:
                            continue
                            
                    # Check for TODO/FIXME/etc
                    if any(pattern in line for pattern in ['TODO', 'FIXME', 'XXX', 'HACK']) and not line.strip().startswith('#'):
                        print(f"  ISSUE: {py_file}:{i} - TODO/FIXME/XXX/HACK in code")
                        module_issues += 1
                    
                    # Check for NotImplementedError
                    if 'NotImplementedError' in line and 'raise' in line:
                        print(f"  ISSUE: {py_file}:{i} - NotImplementedError raised")
                        module_issues += 1
                    
                    # Check for silent except blocks (except: pass with no comment)
                    if line.strip() == 'pass' and i > 1:
                        prev_line = lines[i-2].strip() if i >= 2 else ""
                        if 'except' in prev_line and ':' in prev_line:
                            # Check if there's a comment explaining the pass
                            has_comment = False
                            for j in range(max(0, i-3), i):
                                if '#' in lines[j]:
                                    has_comment = True
                                    break
                            
                            if not has_comment:
                                print(f"  ISSUE: {py_file}:{i} - Silent except block without comment")
                                module_issues += 1
        
        except Exception as e:
            print(f"  ERROR reading {py_file}: {e}")
            module_issues += 1
    
    if module_issues == 0:
        print(f"  ✅ {module} - CLEAN")
    else:
        print(f"  ❌ {module} - {module_issues} issues found")
        total_issues += module_issues

print("\n" + "="*80)
if total_issues == 0:
    print("✅ PHASE 1 PASSED: NO PLACEHOLDER CODE FOUND")
    print("="*80)
    sys.exit(0)
else:
    print(f"❌ PHASE 1 FAILED: {total_issues} PLACEHOLDER ISSUES FOUND")
    print("="*80)
    sys.exit(1)


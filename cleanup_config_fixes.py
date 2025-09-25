#!/usr/bin/env python3
"""
Cleanup Config Fixes
===================

This script:
1. Removes backup files created during fixes
2. Fixes remaining encoding issues
3. Cleans up any remaining validation errors

Date: 2025-09-24
Status: ACTIVE
"""

import os
import shutil
from pathlib import Path
import chardet

def remove_backup_files(directory: Path):
    """Remove all backup files created during fixes."""
    backup_patterns = [
        "*_json_fix_*.json",
        "*_md_fix_*.md", 
        "*_encoding_fix_*.*",
        "*_rename_*.*",
        "*_backup_*.*"
    ]
    
    removed_count = 0
    for pattern in backup_patterns:
        for file_path in directory.rglob(pattern):
            try:
                file_path.unlink()
                print(f"   🗑️ Removed backup: {file_path.name}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Error removing {file_path.name}: {e}")
    
    return removed_count

def fix_encoding_issues(directory: Path):
    """Fix remaining encoding issues."""
    fixed_count = 0
    
    # Files with known encoding issues
    encoding_issues = [
        "luna_refined_analysis_report_test_results.json"
    ]
    
    for filename in encoding_issues:
        file_path = directory / filename
        if file_path.exists():
            try:
                print(f"   🔧 Fixing encoding for {filename}")
                
                # Read with detected encoding
                raw_content = file_path.read_bytes()
                detected_encoding = chardet.detect(raw_content)['encoding']
                
                if detected_encoding and detected_encoding.lower() != 'utf-8':
                    content = raw_content.decode(detected_encoding).encode('utf-8')
                    file_path.write_bytes(content)
                    print(f"   📊 Converted from {detected_encoding} to UTF-8")
                    fixed_count += 1
                else:
                    print(f"   📊 Already UTF-8 encoded")
                    
            except Exception as e:
                print(f"   ❌ Error fixing encoding for {filename}: {e}")
    
    return fixed_count

def main():
    """Main cleanup function."""
    print("🧹 AIOS Config Cleanup")
    print("=" * 30)
    
    config_dir = Path("config")
    if not config_dir.exists():
        print("❌ Config directory not found!")
        return
    
    print("🗑️ Removing backup files...")
    removed_count = remove_backup_files(config_dir)
    print(f"   ✅ Removed {removed_count} backup files")
    
    print("\n🔧 Fixing encoding issues...")
    fixed_count = fix_encoding_issues(config_dir)
    print(f"   ✅ Fixed {fixed_count} encoding issues")
    
    print(f"\n✅ Config cleanup completed!")
    print("🔍 Run validation again to verify cleanup.")

if __name__ == "__main__":
    main()

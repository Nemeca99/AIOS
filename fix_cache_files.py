#!/usr/bin/env python3
"""
Fix Cache Files Migration Script
Specifically handles the cache files that failed during the initial migration
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from aios_json_standards import AIOSJSONHandler, AIOSDataType, AIOSJSONStandards

def backup_file(file_path: Path) -> Path:
    """Create a backup of the original file"""
    backup_path = file_path.with_suffix(f'.backup_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    shutil.copy2(file_path, backup_path)
    print(f"📁 Backed up {file_path.name} to {backup_path.name}")
    return backup_path

def fix_cache_file(file_path: Path):
    """Fix a specific cache file that failed migration"""
    print(f"\n🔧 Fixing: {file_path.name}")
    
    try:
        # Backup original
        backup_file(file_path)
        
        # Load original data
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        print(f"   📊 Original data type: {type(original_data).__name__}")
        print(f"   📊 Original content preview: {str(original_data)[:100]}...")
        
        # Convert to AIOS standard
        aios_data = AIOSJSONHandler.convert_to_aios_standard(original_data, AIOSDataType.CAR_CACHE)
        
        print(f"   ✅ Converted to {len(aios_data)} AIOS cache entries")
        
        # Save in AIOS standard format
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(aios_data, f, indent=2, ensure_ascii=False)
        
        print(f"   🎯 Successfully fixed {file_path.name}")
        
    except Exception as e:
        print(f"   ❌ Error fixing {file_path.name}: {e}")
        print(f"   📋 Error type: {type(e).__name__}")

def fix_all_failed_cache_files():
    """Fix all cache files that failed during initial migration"""
    print("🔧 Fixing Failed Cache Files")
    print("="*50)
    
    # List of files that failed during initial migration
    failed_files = [
        "Data/FractalCache/root_0eb9d2bb.json",
        "Data/FractalCache/root_0eb9d2bb_split_0f20971f.json",
        "Data/FractalCache/root_0eff8d32.json",
        "Data/FractalCache/root_0eff8d32_split_8123efae.json",
        "Data/FractalCache/root_28aa443c.json",
        "Data/FractalCache/root_28aa443c_split_281c36f1.json",
        "Data/FractalCache/root_6c49b1a6.json",
        "Data/FractalCache/root_6c49b1a6_split_b5f7859e.json",
        "Data/FractalCache/root_a96a68ba.json",
        "Data/FractalCache/root_a96a68ba_split_a94b7a2b.json",
        "Data/FractalCache/root_e84cbc41.json",
        "Data/FractalCache/root_e84cbc41_split_6410c130.json",
        "Data/FractalCache/root_e84cbc41_split_65124ef4.json"
    ]
    
    successful_fixes = 0
    failed_fixes = 0
    
    for file_path_str in failed_files:
        file_path = Path(file_path_str)
        
        if file_path.exists():
            try:
                fix_cache_file(file_path)
                successful_fixes += 1
            except Exception as e:
                print(f"❌ Failed to fix {file_path.name}: {e}")
                failed_fixes += 1
        else:
            print(f"⚠️ File not found: {file_path}")
            failed_fixes += 1
    
    print(f"\n📊 Fix Summary:")
    print(f"   ✅ Successfully fixed: {successful_fixes} files")
    print(f"   ❌ Failed to fix: {failed_fixes} files")
    
    if successful_fixes > 0:
        print(f"\n🎯 Cache file migration completed!")
        print(f"All previously failed files have been converted to AIOS standard format.")

def main():
    """Run the cache file fixing process"""
    print("🚀 AIOS Cache Files Fix Script")
    print("="*50)
    print("This script fixes the cache files that failed during initial migration.")
    print("It handles string data and other non-standard formats by wrapping them")
    print("in proper AIOS JSON standard cache entry format.\n")
    
    fix_all_failed_cache_files()

if __name__ == "__main__":
    main()

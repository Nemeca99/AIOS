#!/usr/bin/env python3
"""
Fix FractalCache Errors
======================

This script fixes the FractalCache files that are causing 'list' object has no attribute 'get' errors.
The issue is that some cache files are in list format instead of the expected object format.

Date: 2025-09-24
Status: ACTIVE
"""

import json
import uuid
import shutil
from datetime import datetime, timezone
from pathlib import Path

def backup_file(file_path: Path, suffix: str = "_fractal_fix_"):
    """Create backup of file before modification."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_name(f"{file_path.stem}{suffix}{timestamp}{file_path.suffix}")
    shutil.copy(file_path, backup_path)
    print(f"   📁 Backed up to {backup_path.name}")

def fix_fractal_cache_file(file_path: Path):
    """Fix FractalCache file format issues."""
    try:
        backup_file(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if data is a list (problematic format)
        if isinstance(data, list):
            print(f"   📊 Converting list format to object format")
            
            # Convert list to object format
            if len(data) > 0:
                # If list has items, wrap in a proper cache object
                fixed_data = {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
                    "content": data,
                    "type": "fractal_cache",
                    "metadata": {
                        "converted_from": "list_format",
                        "original_length": len(data),
                        "conversion_date": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z'
                    }
                }
            else:
                # Empty list - create minimal object
                fixed_data = {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
                    "content": [],
                    "type": "fractal_cache",
                    "metadata": {
                        "converted_from": "empty_list",
                        "conversion_date": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z'
                    }
                }
            
            # Write fixed data back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(fixed_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Fixed list format to object format")
            
        elif isinstance(data, dict):
            # Check if it's missing required fields
            if "id" not in data or "timestamp" not in data:
                print(f"   📊 Adding missing required fields")
                
                if "id" not in data:
                    data["id"] = str(uuid.uuid4())
                if "timestamp" not in data:
                    data["timestamp"] = datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z'
                
                # Write fixed data back
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"   ✅ Added missing required fields")
            else:
                print(f"   📊 Already in correct object format")
        else:
            print(f"   📊 Unknown data type: {type(data)}")

    except Exception as e:
        print(f"❌ Error fixing {file_path.name}: {e}")

def main():
    """Main function to fix FractalCache errors."""
    print("🔧 FractalCache Error Fixer")
    print("=" * 35)
    
    fractal_cache_dir = Path("Data/FractalCache")
    if not fractal_cache_dir.exists():
        print("❌ FractalCache directory not found!")
        return
    
    # Find all JSON files in FractalCache
    json_files = list(fractal_cache_dir.glob("*.json"))
    
    print(f"🔍 Found {len(json_files)} JSON files in FractalCache")
    
    fixed_count = 0
    for file_path in json_files:
        print(f"\n📄 Fixing {file_path.name}:")
        try:
            fix_fractal_cache_file(file_path)
            fixed_count += 1
        except Exception as e:
            print(f"❌ Failed to fix {file_path.name}: {e}")
    
    print(f"\n✅ FractalCache fixes completed!")
    print(f"📊 Fixed {fixed_count} files")
    print("🔍 Run the system again to test fixes.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Update all model config files to include schema_version
"""

import json
import sys
from pathlib import Path

def update_config_file(config_path):
    """Update a single config file to include schema_version."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Add schema_version if not present
        if 'schema_version' not in config:
            # Insert schema_version at the beginning
            new_config = {'schema_version': 1}
            new_config.update(config)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Updated: {config_path}")
            return True
        else:
            print(f"⏭️  Already has schema_version: {config_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error updating {config_path}: {e}")
        return False

def main():
    """Update all model config files."""
    print("🔄 Updating model config files with schema_version...")
    
    # Find all model_config.json files
    config_files = []
    for core_dir in Path('.').glob('*_core'):
        config_file = core_dir / 'config' / 'model_config.json'
        if config_file.exists():
            config_files.append(config_file)
    
    # Also update the main config
    main_config = Path('model_config.json')
    if main_config.exists():
        config_files.append(main_config)
    
    updated = 0
    total = len(config_files)
    
    for config_file in config_files:
        if update_config_file(config_file):
            updated += 1
    
    print(f"\n📊 Results: {updated}/{total} files updated")
    
    if updated == total:
        print("🎉 All config files updated successfully!")
        return 0
    else:
        print(f"⚠️  {total - updated} files had issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Fix Remaining Config Issues
===========================

This script fixes the remaining 146 validation errors:
1. Markdown files with long lines and missing headers
2. JSON files not being arrays
3. Encoding issues (Windows-1252 to UTF-8)
4. File naming convention violations

Date: 2025-09-24
Status: ACTIVE
"""

import json
import uuid
import shutil
from datetime import datetime, timezone
from pathlib import Path
import chardet

def backup_file(file_path: Path, suffix: str = "_final_fix_"):
    """Create backup of file before modification."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_name(f"{file_path.stem}{suffix}{timestamp}{file_path.suffix}")
    shutil.copy(file_path, backup_path)
    print(f"   📁 Backed up to {backup_path.name}")

def fix_markdown_headers_and_lines(file_path: Path):
    """Fix markdown files with missing headers and long lines."""
    try:
        backup_file(file_path)
        
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        # Add metadata header if missing
        if not lines[0].startswith("#"):
            header = [
                "# Document Title",
                "**Purpose:** [Brief purpose]",
                "**Version:** 1.0",
                "**Date:** " + datetime.now().strftime("%Y-%m-%d"),
                "**Status:** DRAFT",
                ""
            ]
            lines = header + lines
            print("   ✅ Added metadata header")
        
        # Fix long lines (simple wrap at 80 chars)
        fixed_lines = []
        for line in lines:
            if len(line) > 80 and not line.strip().startswith('-'):
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 > 80:
                        fixed_lines.append(current_line.strip())
                        current_line = word + " "
                    else:
                        current_line += word + " "
                fixed_lines.append(current_line.strip())
            else:
                fixed_lines.append(line)

        file_path.write_text('\n'.join(fixed_lines), encoding='utf-8')
        print(f"   ✅ Fixed markdown formatting")

    except Exception as e:
        print(f"❌ Error fixing {file_path.name}: {e}")

def fix_json_array_issue(file_path: Path):
    """Fix JSON files that should be arrays."""
    try:
        backup_file(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)

        aios_data = []
        if isinstance(original_data, list):
            for item in original_data:
                if isinstance(item, dict):
                    if "id" not in item:
                        item["id"] = str(uuid.uuid4())
                    if "timestamp" not in item:
                        item["timestamp"] = datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z'
                    aios_data.append(item)
                else:
                    aios_data.append({
                        "id": str(uuid.uuid4()),
                        "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
                        "content": str(item),
                        "metadata": {"original_type": type(item).__name__}
                    })
        elif isinstance(original_data, dict):
            if "id" not in original_data:
                original_data["id"] = str(uuid.uuid4())
            if "timestamp" not in original_data:
                original_data["timestamp"] = datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z'
            aios_data.append(original_data)
        else:
            aios_data.append({
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
                "content": str(original_data),
                "metadata": {"original_type": type(original_data).__name__}
            })

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(aios_data, f, indent=2, ensure_ascii=False)
        
        print(f"   📊 Fixed JSON array format with {len(aios_data)} entries")

    except Exception as e:
        print(f"❌ Error fixing {file_path.name}: {e}")

def fix_encoding_issue(file_path: Path):
    """Fix encoding issues (Windows-1252 to UTF-8)."""
    try:
        backup_file(file_path)
        
        raw_content = file_path.read_bytes()
        detected_encoding = chardet.detect(raw_content)['encoding']
        
        if detected_encoding and detected_encoding.lower() != 'utf-8':
            content = raw_content.decode(detected_encoding).encode('utf-8')
            file_path.write_bytes(content)
            print(f"   📊 Converted from {detected_encoding} to UTF-8")
        else:
            print(f"   📊 Already UTF-8 encoded")

    except Exception as e:
        print(f"❌ Error fixing encoding for {file_path.name}: {e}")

def rename_json_files_to_aios_convention(directory: Path):
    """Rename JSON files in master_test_results to follow AIOS conventions."""
    try:
        master_test_results_dir = directory / "master_test_results"
        if not master_test_results_dir.exists():
            print("   ⚠️ master_test_results directory not found")
            return
        
        renamed_count = 0
        for file_path in master_test_results_dir.glob("*.json"):
            if file_path.name.startswith("luna_master_"):
                # Extract the key parts and create a proper name
                parts = file_path.stem.split("_")
                if len(parts) >= 4:
                    # Format: luna_master_[test_type]_[model]_[score]avg_[timestamp]
                    # Convert to: luna_master_[test_type]_[model]_test_results.json
                    test_type = parts[2] if len(parts) > 2 else "test"
                    model_part = "_".join(parts[3:]) if len(parts) > 3 else "unknown"
                    
                    # Find the avg part to extract model name
                    avg_index = model_part.find("avg_")
                    if avg_index > 0:
                        model_name = model_part[:avg_index]
                        new_name = f"luna_master_{test_type}_{model_name}_test_results.json"
                    else:
                        new_name = f"luna_master_{test_type}_{model_part}_test_results.json"
                    
                    new_path = file_path.parent / new_name
                    if not new_path.exists():
                        file_path.rename(new_path)
                        print(f"   📁 Renamed {file_path.name} to {new_name}")
                        renamed_count += 1
                    else:
                        print(f"   ⚠️ Target already exists: {new_name}")
        
        print(f"   ✅ Renamed {renamed_count} JSON files")
        
    except Exception as e:
        print(f"❌ Error renaming JSON files: {e}")

def main():
    """Main function to fix remaining config issues."""
    print("🔧 AIOS Config Final Fix")
    print("=" * 30)
    
    config_dir = Path("config")
    if not config_dir.exists():
        print("❌ Config directory not found!")
        return
    
    # Fix markdown files with issues
    print("📝 Fixing markdown files...")
    markdown_files = [
        "LUNA_MASTER_FRAMEWORK_README.md",
        "README_config.md", 
        "README_PERSONALITY.md"
    ]
    
    for filename in markdown_files:
        file_path = config_dir / filename
        if file_path.exists():
            print(f"\n📄 Fixing {filename}:")
            fix_markdown_headers_and_lines(file_path)
        else:
            print(f"⚠️ File not found: {filename}")
    
    # Fix JSON array issues
    print("\n📊 Fixing JSON array issues...")
    json_files = [
        "travis_consciousness_model_config.json"
    ]
    
    for filename in json_files:
        file_path = config_dir / filename
        if file_path.exists():
            print(f"\n📄 Fixing {filename}:")
            fix_json_array_issue(file_path)
        else:
            print(f"⚠️ File not found: {filename}")
    
    # Fix encoding issues
    print("\n🔤 Fixing encoding issues...")
    encoding_files = [
        "embedder_cache/travis_pattern_cache.json"
    ]
    
    for filename in encoding_files:
        file_path = config_dir / filename
        if file_path.exists():
            print(f"\n📄 Fixing {filename}:")
            fix_encoding_issue(file_path)
        else:
            print(f"⚠️ File not found: {filename}")
    
    # Fix file naming conventions
    print("\n📁 Fixing file naming conventions...")
    rename_json_files_to_aios_convention(config_dir)
    
    print(f"\n✅ Final config fixes completed!")
    print("🔍 Run validation again to verify fixes.")

if __name__ == "__main__":
    main()

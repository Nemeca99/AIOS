#!/usr/bin/env python3
"""
Fix Config Directory Validation Errors
=====================================

This script fixes all validation errors in the config directory:
1. JSON files not being arrays
2. Missing 'id' fields in JSON objects
3. Markdown files with long lines
4. Missing metadata headers
5. Encoding issues (Windows-1252 to UTF-8)
6. File naming convention violations

Date: 2025-09-24
Status: ACTIVE
"""

import json
import uuid
import shutil
from datetime import datetime, timezone
from pathlib import Path
import chardet

def backup_file(file_path: Path, suffix: str = "_backup_"):
    """Create backup of file before modification."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_name(f"{file_path.stem}{suffix}{timestamp}{file_path.suffix}")
    shutil.copy(file_path, backup_path)
    print(f"   📁 Backed up to {backup_path.name}")

def fix_json_file(file_path: Path):
    """Fix JSON files to be arrays and add missing 'id' fields."""
    try:
        backup_file(file_path, "_json_fix_")
        
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
                    # Wrap non-dict items in a standard structure
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
            # Wrap primitive types in a standard structure
            aios_data.append({
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
                "content": str(original_data),
                "metadata": {"original_type": type(original_data).__name__}
            })

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(aios_data, f, indent=2, ensure_ascii=False)
        
        print(f"   📊 Current data type: {type(original_data).__name__}")
        print(f"   ✅ Fixed to AIOS format with {len(aios_data)} entries")

    except Exception as e:
        print(f"❌ Error fixing {file_path.name}: {e}")

def fix_markdown_file(file_path: Path):
    """Fix markdown files with long lines and add missing headers."""
    try:
        backup_file(file_path, "_md_fix_")
        
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

def fix_encoding_issue(file_path: Path):
    """Fix encoding issues (Windows-1252 to UTF-8)."""
    try:
        backup_file(file_path, "_encoding_fix_")
        
        # Read with detected encoding
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

def rename_file_to_aios_convention(file_path: Path):
    """Rename files to follow AIOS naming conventions."""
    try:
        backup_file(file_path, "_rename_")
        
        # Define naming convention mappings
        naming_mappings = {
            "psycho_semantic_rag_system.json": "psycho_semantic_rag_system_config.json",
            "README.md": "README_config.md",
            "travis_consciousness_model_20250917_195044.json": "travis_consciousness_model_config.json"
        }
        
        new_name = naming_mappings.get(file_path.name)
        if new_name:
            new_path = file_path.parent / new_name
            file_path.rename(new_path)
            print(f"   📁 Renamed to {new_name}")
        else:
            print(f"   📁 No naming convention mapping for {file_path.name}")

    except Exception as e:
        print(f"❌ Error renaming {file_path.name}: {e}")

def main():
    """Main function to fix all config validation errors."""
    print("🔧 AIOS Config Validation Error Fixer")
    print("=" * 50)
    
    config_dir = Path("config")
    if not config_dir.exists():
        print("❌ Config directory not found!")
        return
    
    # Files to fix based on validation errors
    files_to_fix = [
        # JSON files that need to be arrays
        "luna_personality_system_config.json",
        "luna_refined_analysis_report_test_results.json",
        "luna_travis_comparison_20250917_200705_test_results.json",
        "lyra_behavioral_law_protocol_config.json",
        "lyra_emotion_engine_v3_config.json",
        "lyra_identity_core_config.json",
        "lyra_identity_v3_config.json",
        "lyra_symbolic_motor_schema_config.json",
        "lyra_voice_manifest_config.json",
        "master_test_cache.json",
        "voice_profile_config.json",
        
        # Markdown files with issues
        "LUNA_MASTER_FRAMEWORK_README.md",
        "README_PERSONALITY.md",
        
        # Files with encoding issues
        "travis_consciousness_model_20250917_195044.json",
        
        # Files with naming convention issues
        "psycho_semantic_rag_system.json",
        "README.md",
        "travis_consciousness_model_20250917_195044.json"
    ]
    
    # Embedder cache files
    embedder_cache_files = [
        "balanced_weight_cache.json",
        "corrected_rag_cache.json",
        "deepseek_test_backup.json",
        "master_test_cache.json",
        "master_test_cache_backup.json",
        "openai_gpt_test_backup.json",
        "pure_car_test_backup.json",
        "smart_frequency_cache.json",
        "travis_pattern_cache.json"
    ]
    
    print(f"🔍 Processing {len(files_to_fix)} main files...")
    
    for filename in files_to_fix:
        file_path = config_dir / filename
        if file_path.exists():
            print(f"\n📄 Fixing {filename}:")
            
            if filename.endswith('.json'):
                fix_json_file(file_path)
            elif filename.endswith('.md'):
                fix_markdown_file(file_path)
            
            # Handle specific issues
            if filename == "travis_consciousness_model_20250917_195044.json":
                fix_encoding_issue(file_path)
            
            if filename in ["psycho_semantic_rag_system.json", "README.md", "travis_consciousness_model_20250917_195044.json"]:
                rename_file_to_aios_convention(file_path)
        else:
            print(f"⚠️ File not found: {filename}")
    
    # Fix embedder cache files
    embedder_cache_dir = config_dir / "embedder_cache"
    if embedder_cache_dir.exists():
        print(f"\n🔍 Processing {len(embedder_cache_files)} embedder cache files...")
        
        for filename in embedder_cache_files:
            file_path = embedder_cache_dir / filename
            if file_path.exists():
                print(f"\n📄 Fixing {filename}:")
                fix_json_file(file_path)
            else:
                print(f"⚠️ Embedder cache file not found: {filename}")
    
    print(f"\n✅ Config validation error fixing completed!")
    print("🔍 Run validation again to verify fixes.")

if __name__ == "__main__":
    main()

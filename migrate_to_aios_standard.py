#!/usr/bin/env python3
"""
Migration Script to AIOS JSON Standard Format
Converts all existing JSON files to the AIOS standard format
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from aios_json_standards import AIOSJSONHandler, AIOSDataType, AIOSJSONStandards

def backup_file(file_path: Path) -> Path:
    """Create a backup of the original file"""
    backup_path = file_path.with_suffix(f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    shutil.copy2(file_path, backup_path)
    print(f"📁 Backed up {file_path.name} to {backup_path.name}")
    return backup_path

def migrate_luna_personality_dna():
    """Migrate Luna personality DNA to AIOS standard"""
    file_path = Path("config/luna_personality_dna.json")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    # Backup original
    backup_file(file_path)
    
    try:
        # Load original data
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # Convert to AIOS standard format
        aios_data = [{
            "id": AIOSJSONStandards.generate_uuid(),
            "config_name": "luna_personality_dna",
            "version": "2.0",
            "parameters": {
                "name": original_data.get("name", "Luna"),
                "age": original_data.get("age", 21),
                "luna_personality": original_data.get("luna_personality", {})
            },
            "models": {},
            "timestamp": AIOSJSONStandards.generate_timestamp(),
            "metadata": {
                "migrated_from": "legacy_format",
                "migration_date": datetime.now().isoformat(),
                "original_structure": "single_object"
            }
        }]
        
        # Save in AIOS standard format
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(aios_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migrated {file_path.name} to AIOS standard format")
        
    except Exception as e:
        print(f"❌ Error migrating {file_path.name}: {e}")

def migrate_luna_persistent_memory():
    """Migrate Luna persistent memory to AIOS standard"""
    file_path = Path("config/luna_persistent_memory.json")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    # Backup original
    backup_file(file_path)
    
    try:
        # Load original data
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # Convert to AIOS standard format
        aios_data = [{
            "id": AIOSJSONStandards.generate_uuid(),
            "config_name": "luna_persistent_memory",
            "version": "2.0",
            "parameters": {
                "interactions": original_data.get("interactions", []),
                "dreams": original_data.get("dreams", []),
                "personality_evolution": original_data.get("personality_evolution", []),
                "emotional_patterns": original_data.get("emotional_patterns", {}),
                "dream_cycles": original_data.get("dream_cycles", [])
            },
            "models": {},
            "timestamp": AIOSJSONStandards.generate_timestamp(),
            "metadata": {
                "migrated_from": "legacy_format",
                "migration_date": datetime.now().isoformat(),
                "original_structure": "single_object"
            }
        }]
        
        # Save in AIOS standard format
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(aios_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migrated {file_path.name} to AIOS standard format")
        
    except Exception as e:
        print(f"❌ Error migrating {file_path.name}: {e}")

def migrate_luna_learning_history():
    """Migrate Luna learning history to AIOS standard"""
    file_path = Path("config/luna_learning_history.json")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    # Backup original
    backup_file(file_path)
    
    try:
        # Load original data
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # Convert to AIOS standard format
        aios_data = [{
            "id": AIOSJSONStandards.generate_uuid(),
            "config_name": "luna_learning_history",
            "version": "2.0",
            "parameters": {
                "total_questions": original_data.get("total_questions", 0),
                "total_responses": original_data.get("total_responses", 0),
                "learning_cycles": original_data.get("learning_cycles", 0),
                "personality_evolution": original_data.get("personality_evolution", []),
                "dream_cycles": original_data.get("dream_cycles", []),
                "last_learning": original_data.get("last_learning", AIOSJSONStandards.generate_timestamp())
            },
            "models": {},
            "timestamp": AIOSJSONStandards.generate_timestamp(),
            "metadata": {
                "migrated_from": "legacy_format",
                "migration_date": datetime.now().isoformat(),
                "original_structure": "single_object"
            }
        }]
        
        # Save in AIOS standard format
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(aios_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migrated {file_path.name} to AIOS standard format")
        
    except Exception as e:
        print(f"❌ Error migrating {file_path.name}: {e}")

def migrate_cache_files():
    """Migrate cache files to AIOS standard"""
    cache_files = [
        "config/embedder_cache/master_test_cache.json",
        "cache/master_test_cache.json",
        "Data/FractalCache"
    ]
    
    for cache_path in cache_files:
        file_path = Path(cache_path)
        
        if file_path.is_file():
            # Migrate single cache file
            try:
                # Backup original
                backup_file(file_path)
                
                # Load original data
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_data = json.load(f)
                
                # Convert to AIOS standard
                aios_data = AIOSJSONHandler.convert_to_aios_standard(original_data, AIOSDataType.CAR_CACHE)
                
                # Save in AIOS standard format
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(aios_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Migrated {file_path.name} to AIOS standard format")
                
            except Exception as e:
                print(f"❌ Error migrating {file_path.name}: {e}")
        
        elif file_path.is_dir():
            # Migrate all JSON files in directory
            for json_file in file_path.glob("*.json"):
                try:
                    # Backup original
                    backup_file(json_file)
                    
                    # Load original data
                    with open(json_file, 'r', encoding='utf-8') as f:
                        original_data = json.load(f)
                    
                    # Convert to AIOS standard
                    aios_data = AIOSJSONHandler.convert_to_aios_standard(original_data, AIOSDataType.CAR_CACHE)
                    
                    # Save in AIOS standard format
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(aios_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Migrated {json_file.name} to AIOS standard format")
                    
                except Exception as e:
                    print(f"❌ Error migrating {json_file.name}: {e}")

def migrate_conversation_files():
    """Migrate conversation files to AIOS standard"""
    conversations_dir = Path("Data/conversations")
    
    if not conversations_dir.exists():
        print(f"❌ Conversations directory not found: {conversations_dir}")
        return
    
    for conv_file in conversations_dir.glob("*.json"):
        try:
            # Backup original
            backup_file(conv_file)
            
            # Load original data
            with open(conv_file, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
            
            # Convert to AIOS standard
            aios_data = AIOSJSONHandler.convert_to_aios_standard(original_data, AIOSDataType.CONVERSATION)
            
            # Save in AIOS standard format
            with open(conv_file, 'w', encoding='utf-8') as f:
                json.dump(aios_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Migrated {conv_file.name} to AIOS standard format")
            
        except Exception as e:
            print(f"❌ Error migrating {conv_file.name}: {e}")

def main():
    """Run the migration process"""
    print("🚀 AIOS JSON Standard Migration")
    print("="*50)
    
    print("\n📋 Phase 1: Migrating Luna Configuration Files")
    migrate_luna_personality_dna()
    migrate_luna_persistent_memory()
    migrate_luna_learning_history()
    
    print("\n📋 Phase 2: Migrating Cache Files")
    migrate_cache_files()
    
    print("\n📋 Phase 3: Migrating Conversation Files")
    migrate_conversation_files()
    
    print("\n🎯 Migration completed!")
    print("All files have been migrated to AIOS JSON Standard Format")
    print("Original files have been backed up with .backup_YYYYMMDD_HHMMSS.json suffix")

if __name__ == "__main__":
    main()

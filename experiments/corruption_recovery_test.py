#!/usr/bin/env python3
"""
CARMA Corruption Recovery Test
Test if CARMA can self-repair when files are corrupted or removed
"""

import os
import json
import shutil
import time
import random
from pathlib import Path
from datetime import datetime

def test_corruption_recovery():
    """Test CARMA's ability to recover from corruption"""
    
    print("🧪 CARMA CORRUPTION RECOVERY TEST")
    print("=" * 50)
    
    # Test 1: Remove random fragment files
    print("\n🔍 Test 1: Removing Random Fragment Files")
    test_remove_fragments()
    
    # Test 2: Corrupt fragment files
    print("\n🔍 Test 2: Corrupting Fragment Files")
    test_corrupt_fragments()
    
    # Test 3: Remove index files
    print("\n🔍 Test 3: Removing Index Files")
    test_remove_indexes()
    
    # Test 4: Corrupt cache registry
    print("\n🔍 Test 4: Corrupting Cache Registry")
    test_corrupt_registry()
    
    # Test 5: Remove entire cache directory
    print("\n🔍 Test 5: Removing Entire Cache Directory")
    test_remove_cache_directory()
    
    print("\n✅ Corruption Recovery Test Complete!")

def test_remove_fragments():
    """Test removing random fragment files"""
    cache_dir = Path("Data/FractalCache")
    if not cache_dir.exists():
        print("   ❌ No cache directory found")
        return
    
    # Find fragment files
    fragment_files = list(cache_dir.glob("*.json"))
    if not fragment_files:
        print("   ❌ No fragment files found")
        return
    
    # Remove 20% of fragments randomly
    num_to_remove = max(1, len(fragment_files) // 5)
    files_to_remove = random.sample(fragment_files, num_to_remove)
    
    print(f"   📁 Found {len(fragment_files)} fragment files")
    print(f"   🗑️  Removing {len(files_to_remove)} random fragments")
    
    removed_files = []
    for file_path in files_to_remove:
        file_id = file_path.stem
        removed_files.append(file_id)
        file_path.unlink()
        print(f"      Removed: {file_id}")
    
    # Test if system can recover
    print("   🔄 Testing recovery...")
    try:
        # Try to run a simple test
        result = run_carma_test()
        if result:
            print("   ✅ System recovered successfully")
        else:
            print("   ❌ System failed to recover")
    except Exception as e:
        print(f"   ❌ Recovery failed: {e}")
    
    return removed_files

def test_corrupt_fragments():
    """Test corrupting fragment files"""
    cache_dir = Path("Data/FractalCache")
    if not cache_dir.exists():
        print("   ❌ No cache directory found")
        return
    
    fragment_files = list(cache_dir.glob("*.json"))
    if not fragment_files:
        print("   ❌ No fragment files found")
        return
    
    # Corrupt 10% of fragments
    num_to_corrupt = max(1, len(fragment_files) // 10)
    files_to_corrupt = random.sample(fragment_files, num_to_corrupt)
    
    print(f"   📁 Found {len(fragment_files)} fragment files")
    print(f"   💥 Corrupting {len(files_to_corrupt)} fragments")
    
    corrupted_files = []
    for file_path in files_to_corrupt:
        file_id = file_path.stem
        corrupted_files.append(file_id)
        
        # Corrupt the file
        with open(file_path, 'w') as f:
            f.write("CORRUPTED_DATA_" + str(random.randint(1000, 9999)))
        
        print(f"      Corrupted: {file_id}")
    
    # Test if system can recover
    print("   🔄 Testing recovery...")
    try:
        result = run_carma_test()
        if result:
            print("   ✅ System recovered successfully")
        else:
            print("   ❌ System failed to recover")
    except Exception as e:
        print(f"   ❌ Recovery failed: {e}")
    
    return corrupted_files

def test_remove_indexes():
    """Test removing index files"""
    cache_dir = Path("Data/FractalCache")
    if not cache_dir.exists():
        print("   ❌ No cache directory found")
        return
    
    # Look for index files
    index_files = list(cache_dir.glob("*index*")) + list(cache_dir.glob("*registry*"))
    
    print(f"   📁 Found {len(index_files)} index files")
    
    if index_files:
        print("   🗑️  Removing index files")
        for file_path in index_files:
            file_path.unlink()
            print(f"      Removed: {file_path.name}")
    
    # Test if system can recover
    print("   🔄 Testing recovery...")
    try:
        result = run_carma_test()
        if result:
            print("   ✅ System recovered successfully")
        else:
            print("   ❌ System failed to recover")
    except Exception as e:
        print(f"   ❌ Recovery failed: {e}")

def test_corrupt_registry():
    """Test corrupting cache registry"""
    cache_dir = Path("Data/FractalCache")
    if not cache_dir.exists():
        print("   ❌ No cache directory found")
        return
    
    # Look for registry files
    registry_files = list(cache_dir.glob("*registry*")) + list(cache_dir.glob("*cache*"))
    
    print(f"   📁 Found {len(registry_files)} registry files")
    
    if registry_files:
        print("   💥 Corrupting registry files")
        for file_path in registry_files:
            with open(file_path, 'w') as f:
                f.write("CORRUPTED_REGISTRY_" + str(random.randint(1000, 9999)))
            print(f"      Corrupted: {file_path.name}")
    
    # Test if system can recover
    print("   🔄 Testing recovery...")
    try:
        result = run_carma_test()
        if result:
            print("   ✅ System recovered successfully")
        else:
            print("   ❌ System failed to recover")
    except Exception as e:
        print(f"   ❌ Recovery failed: {e}")

def test_remove_cache_directory():
    """Test removing entire cache directory"""
    cache_dir = Path("Data/FractalCache")
    if not cache_dir.exists():
        print("   ❌ No cache directory found")
        return
    
    print("   🗑️  Removing entire cache directory")
    shutil.rmtree(cache_dir)
    print("      Cache directory removed")
    
    # Test if system can recover
    print("   🔄 Testing recovery...")
    try:
        result = run_carma_test()
        if result:
            print("   ✅ System recovered successfully")
        else:
            print("   ❌ System failed to recover")
    except Exception as e:
        print(f"   ❌ Recovery failed: {e}")

def run_carma_test():
    """Run a simple CARMA test to check if system works"""
    try:
        # Import CARMA system
        import sys
        sys.path.append("HiveMind")
        from fractal_mycelium_cache import FractalMyceliumCache
        
        # Initialize cache
        cache = FractalMyceliumCache()
        
        # Try to add some content
        test_content = f"Test content {random.randint(1000, 9999)}"
        file_id = cache.add_content(test_content)
        
        # Try to retrieve content
        results = cache.find_relevant(cache.embedder.embed("test"), topk=1)
        
        return len(results) > 0
        
    except Exception as e:
        print(f"      Error in test: {e}")
        return False

if __name__ == "__main__":
    test_corruption_recovery()

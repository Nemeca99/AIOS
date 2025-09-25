#!/usr/bin/env python3
"""
CARMA Corruption Stress Test
Test how far the system can be corrupted before it stops working
"""

import os
import json
import shutil
import time
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Import the beacon system
import sys
sys.path.append("HiveMind")
from beacon_self_repair_system import BeaconSelfRepairSystem

def corruption_stress_test():
    """Test system resilience under increasing corruption"""
    
    print("🧪 CARMA CORRUPTION STRESS TEST")
    print("=" * 60)
    
    # Initialize beacon system
    beacon = BeaconSelfRepairSystem()
    
    # Test different corruption levels
    corruption_levels = [
        (0.1, "10% corruption"),
        (0.2, "20% corruption"),
        (0.3, "30% corruption"),
        (0.4, "40% corruption"),
        (0.5, "50% corruption"),
        (0.6, "60% corruption"),
        (0.7, "70% corruption"),
        (0.8, "80% corruption"),
        (0.9, "90% corruption"),
        (0.95, "95% corruption"),
        (0.99, "99% corruption")
    ]
    
    results = []
    
    for corruption_ratio, description in corruption_levels:
        print(f"\n🔍 Testing {description}")
        print("-" * 40)
        
        # Reset system
        reset_system()
        
        # Apply corruption
        corrupted_files = apply_corruption(corruption_ratio)
        
        # Test system recovery
        result = test_system_recovery(beacon, corrupted_files)
        result['corruption_ratio'] = corruption_ratio
        result['description'] = description
        results.append(result)
        
        # Check if system is still operational
        if not result['is_operational']:
            print(f"   ❌ System failed at {corruption_ratio:.1%} corruption")
            break
        else:
            print(f"   ✅ System operational at {corruption_ratio:.1%} corruption")
    
    # Generate report
    generate_stress_test_report(results)
    
    return results

def reset_system():
    """Reset the system to clean state"""
    cache_dir = Path("Data/FractalCache")
    
    # Remove existing cache
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    
    # Create fresh cache with sample data
    create_sample_cache()

def create_sample_cache():
    """Create a sample cache for testing"""
    cache_dir = Path("Data/FractalCache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Create root file
    root_file = {
        'id': 'root_001',
        'content': 'This is the root file content for testing',
        'created': datetime.now().isoformat(),
        'last_accessed': datetime.now().isoformat(),
        'children': ['root_001_split_1', 'root_001_split_2'],
        'parents': []
    }
    
    with open(cache_dir / "root_001.json", 'w') as f:
        json.dump(root_file, f, indent=2)
    
    # Create level 1 files
    for i in range(1, 3):
        level1_file = {
            'id': f'root_001_split_{i}',
            'content': f'Level 1 file {i} content for testing',
            'created': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'children': [f'root_001_split_{i}_split_1', f'root_001_split_{i}_split_2'],
            'parents': ['root_001']
        }
        
        with open(cache_dir / f"root_001_split_{i}.json", 'w') as f:
            json.dump(level1_file, f, indent=2)
    
    # Create level 2 files
    for i in range(1, 3):
        for j in range(1, 3):
            level2_file = {
                'id': f'root_001_split_{i}_split_{j}',
                'content': f'Level 2 file {i}-{j} content for testing',
                'created': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat(),
                'children': [],
                'parents': [f'root_001_split_{i}']
            }
            
            with open(cache_dir / f"root_001_split_{i}_split_{j}.json", 'w') as f:
                json.dump(level2_file, f, indent=2)
    
    print(f"   📁 Created sample cache with {len(list(cache_dir.glob('*.json')))} files")

def apply_corruption(corruption_ratio: float) -> List[str]:
    """Apply corruption to the system"""
    cache_dir = Path("Data/FractalCache")
    files = list(cache_dir.glob("*.json"))
    
    num_to_corrupt = int(len(files) * corruption_ratio)
    files_to_corrupt = random.sample(files, num_to_corrupt)
    
    corrupted_files = []
    
    for file_path in files_to_corrupt:
        file_id = file_path.stem
        corrupted_files.append(file_id)
        
        # Randomly choose corruption type
        corruption_type = random.choice(['remove', 'corrupt', 'empty'])
        
        if corruption_type == 'remove':
            file_path.unlink()
        elif corruption_type == 'corrupt':
            with open(file_path, 'w') as f:
                f.write("CORRUPTED_DATA_" + str(random.randint(1000, 9999)))
        elif corruption_type == 'empty':
            with open(file_path, 'w') as f:
                f.write("{}")
    
    print(f"   💥 Corrupted {len(corrupted_files)} files ({corruption_ratio:.1%})")
    return corrupted_files

def test_system_recovery(beacon: BeaconSelfRepairSystem, corrupted_files: List[str]) -> Dict:
    """Test system recovery after corruption"""
    
    # Ping network to discover topology
    print("   🌐 Pinging network...")
    network_map = beacon.ping_network()
    
    # Check system health
    print("   🏥 Checking system health...")
    health = beacon.check_system_health()
    
    # Test deep dream recovery
    print("   🌙 Testing deep dream recovery...")
    recovery_result = beacon.deep_dream_recovery()
    
    # Test query execution with fallback
    print("   🔍 Testing query execution...")
    test_paths = [
        ['root_001', 'root_001_split_1', 'root_001_split_1_split_1'],
        ['root_001', 'root_001_split_2', 'root_001_split_2_split_1'],
        ['root_001']
    ]
    
    success, message, missing_files = beacon.execute_with_fallback("test query", test_paths)
    
    # Calculate recovery metrics
    total_files = len(network_map)
    accessible_files = sum(1 for f in network_map.values() if f['accessible'])
    recovery_rate = (accessible_files / total_files) * 100 if total_files > 0 else 0
    
    result = {
        'total_files': total_files,
        'accessible_files': accessible_files,
        'corrupted_files': len(corrupted_files),
        'recovery_rate': recovery_rate,
        'is_operational': health['is_operational'],
        'health_score': health['health_score'],
        'blank_files': health['blank_files'],
        'recovery_result': recovery_result,
        'query_success': success,
        'query_message': message,
        'missing_files': len(missing_files)
    }
    
    print(f"      Total files: {total_files}")
    print(f"      Accessible: {accessible_files}")
    print(f"      Recovery rate: {recovery_rate:.1f}%")
    print(f"      Operational: {'✅' if health['is_operational'] else '❌'}")
    print(f"      Query success: {'✅' if success else '❌'}")
    
    return result

def generate_stress_test_report(results: List[Dict]):
    """Generate comprehensive stress test report"""
    
    print("\n" + "=" * 60)
    print("📊 CORRUPTION STRESS TEST REPORT")
    print("=" * 60)
    
    # Find failure point
    failure_point = None
    for i, result in enumerate(results):
        if not result['is_operational']:
            failure_point = result
            break
    
    if failure_point:
        print(f"❌ System failed at {failure_point['corruption_ratio']:.1%} corruption")
        print(f"   Description: {failure_point['description']}")
        print(f"   Health score: {failure_point['health_score']:.1f}%")
        print(f"   Recovery rate: {failure_point['recovery_rate']:.1f}%")
    else:
        print("✅ System remained operational through all corruption levels")
    
    # Summary table
    print("\n📋 Summary Table:")
    print("Corruption | Health | Recovery | Operational | Query")
    print("-----------|--------|----------|-------------|-------")
    
    for result in results:
        corruption = f"{result['corruption_ratio']:.1%}"
        health = f"{result['health_score']:.1f}%"
        recovery = f"{result['recovery_rate']:.1f}%"
        operational = "✅" if result['is_operational'] else "❌"
        query = "✅" if result['query_success'] else "❌"
        
        print(f"{corruption:>10} | {health:>6} | {recovery:>8} | {operational:>11} | {query}")
    
    # Save detailed results
    report_file = Path("experiments/corruption_stress_test_results.json")
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📁 Detailed results saved to: {report_file}")

if __name__ == "__main__":
    results = corruption_stress_test()

#!/usr/bin/env python3
"""
CARMA Mycelium Network - Rock Solid Stress Test
Comprehensive testing to find and fix any weaknesses
"""

import sys
import os
import time
import threading
import random
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Add parent directory to path
sys.path.append('..')

def test_concurrent_api_calls():
    """Test concurrent API calls for race conditions"""
    print("🔥 TESTING CONCURRENT API CALLS")
    print("=" * 50)
    
    try:
        from HiveMind.pi_based_encryption import PiBasedEncryption
        
        encryption = PiBasedEncryption(fast_mode=True)  # Use fast mode for testing
        results = []
        errors = []
        
        def generate_key_task(user_id):
            try:
                key = encryption.generate_pi_api_key(f"user_{user_id}", "read")
                validation = encryption.validate_pi_api_key(key)
                return {"user_id": user_id, "key": key, "valid": validation.get('valid', False)}
            except Exception as e:
                return {"user_id": user_id, "error": str(e)}
        
        # Test with 50 concurrent calls
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(generate_key_task, i) for i in range(50)]
            
            for future in as_completed(futures):
                result = future.result()
                if "error" in result:
                    errors.append(result)
                else:
                    results.append(result)
        
        success_rate = len([r for r in results if r.get('valid', False)]) / len(results) * 100
        print(f"✅ Concurrent API Calls: {len(results)}/50 successful")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Errors: {len(errors)}")
        
        if errors:
            print("   Sample errors:")
            for error in errors[:3]:
                print(f"     User {error['user_id']}: {error['error']}")
        
        return success_rate >= 95.0
        
    except Exception as e:
        print(f"❌ Concurrent API Calls: {e}")
        return False

def test_memory_leaks():
    """Test for memory leaks in long-running operations"""
    print("\n🧠 TESTING MEMORY LEAKS")
    print("=" * 50)
    
    try:
        from HiveMind.carma_core import CARMACore
        import psutil
        import gc
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        carma = CARMACore()
        
        # Perform many operations
        for i in range(100):
            # Store fragments
            fragment_data = {
                "content": f"Test content {i}",
                "metadata": {"test": True, "iteration": i},
                "created_at": time.time()
            }
            carma.store_fragment(f"test_fragment_{i}", fragment_data)
            
            # Query fragments
            results = carma.query_fragments(f"test content {i}")
            
            # Clean up every 10 iterations
            if i % 10 == 0:
                gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"✅ Memory Leak Test: Initial: {initial_memory:.1f}MB, Final: {final_memory:.1f}MB")
        print(f"   Memory Increase: {memory_increase:.1f}MB")
        
        # Consider it a pass if memory increase is less than 50MB
        return memory_increase < 50.0
        
    except Exception as e:
        print(f"❌ Memory Leak Test: {e}")
        return False

def test_edge_cases():
    """Test extreme edge cases and boundary conditions"""
    print("\n⚡ TESTING EDGE CASES")
    print("=" * 50)
    
    try:
        from HiveMind.pi_based_encryption import PiBasedEncryption
        from HiveMind.global_api_distribution import GlobalAPIDistribution
        
        encryption = PiBasedEncryption(fast_mode=True)  # Use fast mode for testing
        distribution = GlobalAPIDistribution()
        
        edge_cases = [
            # Empty strings
            ("", "read"),
            ("test_user", ""),
            # Very long strings
            ("a" * 1000, "read"),
            ("test_user", "a" * 1000),
            # Special characters
            ("user@#$%^&*()", "read"),
            ("test_user", "read@#$%"),
            # Unicode
            ("用户_测试", "read"),
            ("test_user", "读写"),
            # Numbers
            ("123456789", "read"),
            ("test_user", "123"),
        ]
        
        passed = 0
        total = len(edge_cases)
        
        for user_id, permissions in edge_cases:
            try:
                # Test API key generation
                key = encryption.generate_pi_api_key(user_id, permissions)
                validation = encryption.validate_pi_api_key(key)
                
                if validation.get('valid', False):
                    passed += 1
                else:
                    print(f"   ⚠️  Edge case failed: user_id='{user_id[:20]}...', permissions='{permissions[:20]}...'")
                    
            except Exception as e:
                print(f"   ⚠️  Edge case error: user_id='{user_id[:20]}...', permissions='{permissions[:20]}...' - {e}")
        
        success_rate = (passed / total) * 100
        print(f"✅ Edge Cases: {passed}/{total} passed ({success_rate:.1f}%)")
        
        return success_rate >= 80.0
        
    except Exception as e:
        print(f"❌ Edge Cases: {e}")
        return False

def test_network_resilience():
    """Test network resilience and fault tolerance"""
    print("\n🌐 TESTING NETWORK RESILIENCE")
    print("=" * 50)
    
    try:
        from HiveMind.carma_mycelium_network import CARMAMyceliumNetwork
        
        network = CARMAMyceliumNetwork(num_initial_blocks=5, users_per_block=10)
        
        # Create server blocks
        for i in range(5):
            network.create_server_block(f"block_{i}", f"192.168.1.{100 + i}")
        
        # Test user connections
        connected_users = []
        for i in range(25):  # More users than total capacity
            user_id = f"stress_user_{i}"
            api_key = f"api_key_{i}"
            
            # Try to connect to any available block
            for block_id in network.server_blocks.keys():
                connection = network.connect_user(block_id, user_id, api_key)
                if connection:
                    connected_users.append((user_id, block_id))
                    break
        
        # Test disconnections
        disconnected = 0
        for user_id, block_id in connected_users[:10]:  # Disconnect first 10
            if network.disconnect_user(block_id, user_id):
                disconnected += 1
        
        # Test reconnections
        reconnected = 0
        for user_id, block_id in connected_users[:5]:  # Reconnect first 5
            connection = network.connect_user(block_id, user_id, f"new_api_key_{user_id}")
            if connection:
                reconnected += 1
        
        print(f"✅ Network Resilience: {len(connected_users)} connected, {disconnected} disconnected, {reconnected} reconnected")
        
        return len(connected_users) >= 20 and disconnected >= 8 and reconnected >= 4
        
    except Exception as e:
        print(f"❌ Network Resilience: {e}")
        return False

def test_security_vulnerabilities():
    """Test for security vulnerabilities"""
    print("\n🔒 TESTING SECURITY VULNERABILITIES")
    print("=" * 50)
    
    try:
        from HiveMind.pi_based_encryption import PiBasedEncryption
        
        encryption = PiBasedEncryption(fast_mode=True)  # Use fast mode for testing
        
        # Test 1: Key collision detection
        keys_generated = set()
        collision_count = 0
        
        for i in range(1000):
            key = encryption.generate_pi_api_key(f"user_{i}", "read")
            if key in keys_generated:
                collision_count += 1
            keys_generated.add(key)
        
        # Test 2: Invalid key validation
        invalid_keys = [
            "invalid_key",
            "carma_invalid",
            "carma_user_pi_999999_perm_read_meta_123_quantum_abc",
            "carma_user_pi_0_perm_invalid_meta_123_quantum_abc12345",
            "",
            None
        ]
        
        invalid_rejected = 0
        for invalid_key in invalid_keys:
            if invalid_key is None:
                continue
            validation = encryption.validate_pi_api_key(invalid_key)
            if not validation.get('valid', False):
                invalid_rejected += 1
        
        # Test 3: Brute force resistance (simplified)
        brute_force_attempts = 100
        successful_brute_force = 0
        
        for i in range(brute_force_attempts):
            # Generate a random key pattern
            fake_key = f"carma_user_{i}_pi_{random.randint(0, 9999)}_perm_read_meta_{random.randint(0, 999999)}_quantum_{random.randint(0, 99999999):08x}"
            validation = encryption.validate_pi_api_key(fake_key)
            if validation.get('valid', False):
                successful_brute_force += 1
        
        print(f"✅ Security Test: {len(keys_generated)} unique keys generated")
        print(f"   Key Collisions: {collision_count}")
        print(f"   Invalid Keys Rejected: {invalid_rejected}/{len(invalid_keys)}")
        print(f"   Brute Force Success: {successful_brute_force}/{brute_force_attempts}")
        
        return (collision_count == 0 and 
                invalid_rejected >= len(invalid_keys) * 0.8 and 
                successful_brute_force < brute_force_attempts * 0.1)
        
    except Exception as e:
        print(f"❌ Security Test: {e}")
        return False

def test_performance_under_load():
    """Test performance under heavy load"""
    print("\n⚡ TESTING PERFORMANCE UNDER LOAD")
    print("=" * 50)
    
    try:
        from HiveMind.carma_core import CARMACore
        from HiveMind.pi_based_encryption import PiBasedEncryption
        
        carma = CARMACore()
        encryption = PiBasedEncryption(fast_mode=True)  # Use fast mode for testing
        
        # Test 1: Bulk fragment storage
        start_time = time.time()
        for i in range(100):
            fragment_data = {
                "content": f"Performance test content {i}",
                "metadata": {"test": True, "iteration": i},
                "created_at": time.time()
            }
            carma.store_fragment(f"perf_fragment_{i}", fragment_data)
        storage_time = time.time() - start_time
        
        # Test 2: Bulk queries
        start_time = time.time()
        for i in range(50):
            results = carma.query_fragments(f"performance test {i}")
        query_time = time.time() - start_time
        
        # Test 3: Bulk API key generation
        start_time = time.time()
        for i in range(50):
            key = encryption.generate_pi_api_key(f"perf_user_{i}", "read")
            validation = encryption.validate_pi_api_key(key)
        api_time = time.time() - start_time
        
        print(f"✅ Performance Test:")
        print(f"   100 Fragment Storage: {storage_time:.2f}s ({100/storage_time:.1f} ops/sec)")
        print(f"   50 Queries: {query_time:.2f}s ({50/query_time:.1f} ops/sec)")
        print(f"   50 API Keys: {api_time:.2f}s ({50/api_time:.1f} ops/sec)")
        
        # Consider it a pass if all operations are reasonably fast
        return (storage_time < 10.0 and query_time < 5.0 and api_time < 25.0)  # 1 second per API key due to rate limiting
        
    except Exception as e:
        print(f"❌ Performance Test: {e}")
        return False

def run_rock_solid_stress_test():
    """Run all stress tests and generate report"""
    print("🍄 CARMA Mycelium Network - Rock Solid Stress Test")
    print("=" * 60)
    print("Comprehensive testing to find and fix any weaknesses")
    print("=" * 60)
    
    tests = [
        ("Concurrent API Calls", test_concurrent_api_calls),
        ("Memory Leaks", test_memory_leaks),
        ("Edge Cases", test_edge_cases),
        ("Network Resilience", test_network_resilience),
        ("Security Vulnerabilities", test_security_vulnerabilities),
        ("Performance Under Load", test_performance_under_load),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name}: Test failed with exception - {e}")
            results[test_name] = False
    
    # Generate report
    print("\n📊 ROCK SOLID STRESS TEST REPORT")
    print("=" * 60)
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 OVERALL RESULT: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🚀 SYSTEM IS ROCK SOLID! Ready for production!")
    elif passed_tests >= total_tests * 0.8:
        print("🟡 SYSTEM IS MOSTLY SOLID! Minor issues to address.")
    else:
        print("🔴 SYSTEM NEEDS WORK! Significant issues found.")
    
    # Save detailed report
    report = {
        "timestamp": time.time(),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "success_rate": (passed_tests / total_tests) * 100,
        "test_results": results
    }
    
    with open("rock_solid_stress_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: rock_solid_stress_test_report.json")
    
    return report

if __name__ == "__main__":
    try:
        report = run_rock_solid_stress_test()
    except Exception as e:
        print(f"\n❌ Stress test failed: {e}")
        import traceback
        traceback.print_exc()

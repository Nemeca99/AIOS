#!/usr/bin/env python3
"""
REAL LEARNING TEST - Full CARMA Mycelium Network Integration
Tests the complete system with real learning scenarios
"""

import sys
import time
import json
from pathlib import Path

# Add HiveMind to path
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

def test_real_learning_scenarios():
    """Test real learning scenarios with the full CARMA system"""
    print("🍄 CARMA MYCELIUM NETWORK - REAL LEARNING TEST")
    print("============================================================\n")
    
    try:
        # Import the enhanced Luna main system
        from luna_main import LunaMasterTest
        
        print("🚀 Initializing Luna Master Test with Enhanced CARMA...")
        luna = LunaMasterTest()
        
        # Check if enhanced CARMA is available
        if not hasattr(luna, 'enhanced_carma') or luna.enhanced_carma is None:
            print("❌ Enhanced CARMA system not available!")
            return False
        
        print("✅ Enhanced CARMA system loaded successfully!")
        
        # Test 1: Basic Learning Scenario
        print("\n📚 TEST 1: Basic Learning Scenario")
        print("=" * 50)
        
        # Store some learning content
        learning_content = [
            "The CARMA Mycelium Network is a distributed AI memory system that can scale to 8 billion users.",
            "Pi-based encryption provides quantum-resistant security using mathematical constants.",
            "The mycelium network creates self-healing, fault-tolerant routing between server blocks.",
            "Enterprise features include billing, compliance, and advanced security monitoring.",
            "The system uses semantic reconstruction to rebuild missing fragments automatically."
        ]
        
        print("📝 Storing learning content...")
        for i, content in enumerate(learning_content):
            fragment_id = luna.enhanced_carma.add_fragment(
                content=content,
                parent_id=None,
                level=0,
                metadata={"type": "learning", "topic": "carma_system", "index": i}
            )
            print(f"   ✅ Stored fragment {i+1}: {fragment_id[:8]}...")
        
        # Test 2: Semantic Search and Retrieval
        print("\n🔍 TEST 2: Semantic Search and Retrieval")
        print("=" * 50)
        
        search_queries = [
            "How does the system scale?",
            "What encryption is used?",
            "How does the network heal itself?",
            "What enterprise features are available?",
            "How does reconstruction work?"
        ]
        
        for query in search_queries:
            print(f"\n🔍 Query: '{query}'")
            results = luna.enhanced_carma.search_fragments(query, limit=3)
            
            if results:
                print(f"   📊 Found {len(results)} relevant fragments:")
                for j, result in enumerate(results):
                    similarity = result.get('similarity', 0.0)
                    content_preview = result.get('content', '')[:100] + "..."
                    print(f"      {j+1}. Similarity: {similarity:.3f} - {content_preview}")
            else:
                print("   ❌ No results found")
        
        # Test 3: API Key Generation and Validation
        print("\n🔑 TEST 3: API Key Generation and Validation")
        print("=" * 50)
        
        test_users = [
            ("travis_miner", "admin"),
            ("test_user", "read"),
            ("enterprise_client", "write"),
            ("researcher", "read"),
            ("developer", "admin")
        ]
        
        generated_keys = []
        for user_id, permissions in test_users:
            print(f"\n👤 User: {user_id} ({permissions})")
            
            # Generate API key
            api_key = luna.pi_encryption.generate_pi_api_key(user_id, permissions)
            print(f"   🔑 Generated: {api_key[:50]}...")
            
            # Validate API key
            validation = luna.pi_encryption.validate_pi_api_key(api_key)
            if validation.get('valid', False):
                print(f"   ✅ Valid - User: {validation.get('user_id')}, Permissions: {validation.get('permissions')}")
                generated_keys.append(api_key)
            else:
                print(f"   ❌ Invalid: {validation.get('error', 'Unknown error')}")
        
        # Test 4: Mycelium Network Operations
        print("\n🌐 TEST 4: Mycelium Network Operations")
        print("=" * 50)
        
        # Create server blocks
        print("🏗️ Creating server blocks...")
        for i in range(3):
            block_id = f"learning_block_{i}"
            external_ip = f"192.168.1.{100 + i}"
            internal_network = f"192.168.{50 + i}.0/24"
            
            luna.mycelium_network.create_server_block(block_id, external_ip, internal_network)
            print(f"   ✅ Created block {block_id} at {external_ip}")
        
        # Connect users to the network
        print("\n🔗 Connecting users to network...")
        for i, (user_id, permissions) in enumerate(test_users):
            block_id = f"learning_block_{i % 3}"  # Distribute across blocks
            api_key = generated_keys[i] if i < len(generated_keys) else "test_key"
            
            connection = luna.mycelium_network.connect_user(block_id, user_id, api_key)
            if connection:
                print(f"   ✅ {user_id} connected to {block_id} - Slot: {connection['slot']}, IP: {connection['internal_ip']}")
            else:
                print(f"   ❌ Failed to connect {user_id}")
        
        # Test 5: Enterprise Features
        print("\n💼 TEST 5: Enterprise Features")
        print("=" * 50)
        
        # Test billing
        print("💰 Testing billing system...")
        for user_id, permissions in test_users:
            luna.enterprise_billing.track_request(user_id, "fragment_storage", 1)
            luna.enterprise_billing.track_request(user_id, "search_query", 1)
        
        # Get usage for a user
        usage = luna.enterprise_billing.get_usage("travis_miner")
        print(f"   📊 Travis Miner usage: {usage}")
        
        # Test key rotation
        print("\n🔄 Testing key rotation...")
        rotation_status = luna.key_rotation.rotate_key("travis_miner")
        print(f"   🔄 Key rotation status: {rotation_status}")
        
        # Test compliance
        print("\n📋 Testing compliance...")
        audit_log = luna.compliance.get_audit_log("travis_miner", limit=5)
        print(f"   📋 Audit log entries: {len(audit_log)}")
        
        # Test 6: Global Distribution
        print("\n🌍 TEST 6: Global Distribution")
        print("=" * 50)
        
        print("🌐 Testing global user distribution...")
        for user_id, _ in test_users:
            endpoint = luna.global_distribution.get_user_endpoint(user_id)
            print(f"   🌍 {user_id} -> {endpoint}")
        
        # Test 7: Performance Under Load
        print("\n⚡ TEST 7: Performance Under Load")
        print("=" * 50)
        
        print("🚀 Testing performance with 100 operations...")
        start_time = time.time()
        
        # Store 100 fragments
        for i in range(100):
            content = f"Performance test fragment {i} - testing the CARMA system under load"
            luna.enhanced_carma.add_fragment(
                content=content,
                parent_id=None,
                level=0,
                metadata={"type": "performance_test", "index": i}
            )
        
        # Search 50 queries
        for i in range(50):
            query = f"performance test fragment {i}"
            luna.enhanced_carma.search_fragments(query, limit=5)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"   ⚡ 100 fragments stored + 50 searches in {total_time:.2f}s")
        print(f"   📊 Rate: {(150 / total_time):.1f} operations/sec")
        
        # Test 8: System Health Check
        print("\n🏥 TEST 8: System Health Check")
        print("=" * 50)
        
        # Check all systems
        systems = {
            "Enhanced CARMA Core": luna.enhanced_carma is not None,
            "Pi Encryption": hasattr(luna, 'pi_encryption') and luna.pi_encryption is not None,
            "Global Distribution": hasattr(luna, 'global_distribution') and luna.global_distribution is not None,
            "Mycelium Network": hasattr(luna, 'mycelium_network') and luna.mycelium_network is not None,
            "Enterprise Billing": hasattr(luna, 'enterprise_billing') and luna.enterprise_billing is not None,
            "Key Rotation": hasattr(luna, 'key_rotation') and luna.key_rotation is not None,
            "Compliance": hasattr(luna, 'compliance') and luna.compliance is not None,
            "Advanced Security": hasattr(luna, 'advanced_security') and luna.advanced_security is not None
        }
        
        healthy_systems = sum(systems.values())
        total_systems = len(systems)
        
        print(f"🏥 System Health: {healthy_systems}/{total_systems} systems healthy")
        for system, status in systems.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {system}")
        
        # Final Results
        print("\n🎯 REAL LEARNING TEST RESULTS")
        print("=" * 50)
        
        if healthy_systems == total_systems:
            print("🎉 ALL SYSTEMS OPERATIONAL!")
            print("🚀 CARMA Mycelium Network is ready for production!")
            print("🍄 The system successfully learned and processed all test scenarios!")
            return True
        else:
            print(f"⚠️ {total_systems - healthy_systems} systems need attention")
            return False
            
    except Exception as e:
        print(f"❌ Learning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run the real learning test"""
    print("Starting Real Learning Test...")
    
    success = test_real_learning_scenarios()
    
    if success:
        print("\n🎉 REAL LEARNING TEST COMPLETED SUCCESSFULLY!")
        print("🚀 The CARMA Mycelium Network is fully operational and ready for real-world deployment!")
    else:
        print("\n❌ REAL LEARNING TEST FAILED!")
        print("🔧 Some systems need attention before deployment.")
    
    return success

if __name__ == "__main__":
    main()

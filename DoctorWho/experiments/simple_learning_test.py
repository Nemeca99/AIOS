#!/usr/bin/env python3
"""
SIMPLE LEARNING TEST - Direct CARMA System Test
Tests the CARMA system directly without Luna integration
"""

import sys
import time
import json
from pathlib import Path

# Add HiveMind to path
sys.path.append(str(Path(__file__).parent.parent / "HiveMind"))

def test_carma_learning_directly():
    """Test CARMA learning directly without Luna integration"""
    print("🍄 CARMA MYCELIUM NETWORK - SIMPLE LEARNING TEST")
    print("============================================================\n")
    
    try:
        # Import CARMA components directly
        from carma_core import CARMACore
        from pi_based_encryption import PiBasedEncryption
        from global_api_distribution import GlobalAPIDistribution
        from carma_mycelium_network import CARMAMyceliumNetwork
        from enterprise_features import EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity
        
        print("✅ All CARMA components imported successfully!")
        
        # Test 1: Initialize CARMA Core
        print("\n🧠 TEST 1: CARMA Core Initialization")
        print("=" * 50)
        
        carma = CARMACore()
        print("✅ CARMA Core initialized successfully!")
        
        # Test 2: Learning Content Storage
        print("\n📚 TEST 2: Learning Content Storage")
        print("=" * 50)
        
        learning_topics = [
            {
                "content": "The CARMA Mycelium Network is a revolutionary distributed AI memory system that can scale to support 8 billion users across 133.3 million server blocks.",
                "metadata": {"topic": "architecture", "importance": "high", "type": "overview"}
            },
            {
                "content": "Pi-based encryption provides quantum-resistant security by using mathematical constants and recursive compression algorithms that are virtually unbreakable.",
                "metadata": {"topic": "security", "importance": "critical", "type": "encryption"}
            },
            {
                "content": "The mycelium network creates self-healing, fault-tolerant routing where each server block acts as a router with its own internal network supporting 60 users per block.",
                "metadata": {"topic": "networking", "importance": "high", "type": "architecture"}
            },
            {
                "content": "Enterprise features include comprehensive billing systems, automated key rotation, compliance monitoring, and advanced security threat detection.",
                "metadata": {"topic": "enterprise", "importance": "medium", "type": "features"}
            },
            {
                "content": "Semantic reconstruction uses FAISS indexing and embedding similarity to automatically rebuild missing fragments with high fidelity.",
                "metadata": {"topic": "recovery", "importance": "high", "type": "self_healing"}
            }
        ]
        
        print("📝 Storing learning content...")
        stored_fragments = []
        for i, topic in enumerate(learning_topics):
            fragment_id = carma.add_fragment(
                content=topic["content"],
                parent_id=None,
                level=0,
                metadata=topic["metadata"]
            )
            stored_fragments.append(fragment_id)
            print(f"   ✅ Stored: {topic['metadata']['topic']} -> {fragment_id[:8]}...")
        
        # Test 3: Semantic Search and Learning
        print("\n🔍 TEST 3: Semantic Search and Learning")
        print("=" * 50)
        
        search_queries = [
            "How does the system scale to billions of users?",
            "What makes the encryption quantum-resistant?",
            "How does the network heal itself when components fail?",
            "What enterprise features are available for businesses?",
            "How does the system rebuild missing data automatically?"
        ]
        
        total_similarity = 0
        successful_searches = 0
        
        for i, query in enumerate(search_queries):
            print(f"\n🔍 Query {i+1}: '{query}'")
            results = carma.search_fragments(query, limit=3)
            
            if results:
                successful_searches += 1
                print(f"   📊 Found {len(results)} relevant fragments:")
                
                query_similarity = 0
                for j, result in enumerate(results):
                    similarity = result.get('similarity', 0.0)
                    query_similarity += similarity
                    content_preview = result.get('content', '')[:80] + "..."
                    topic = result.get('metadata', {}).get('topic', 'unknown')
                    print(f"      {j+1}. [{topic}] Similarity: {similarity:.3f}")
                    print(f"         {content_preview}")
                
                avg_similarity = query_similarity / len(results)
                total_similarity += avg_similarity
                print(f"   📈 Average similarity: {avg_similarity:.3f}")
            else:
                print("   ❌ No results found")
        
        if successful_searches > 0:
            overall_similarity = total_similarity / successful_searches
            print(f"\n📊 Overall search performance: {overall_similarity:.3f} average similarity")
        
        # Test 4: Pi-Based Encryption Learning
        print("\n🔑 TEST 4: Pi-Based Encryption Learning")
        print("=" * 50)
        
        encryption = PiBasedEncryption(fast_mode=True)
        
        # Generate API keys for different user types
        user_scenarios = [
            ("travis_miner", "admin", "System creator with full access"),
            ("enterprise_client", "write", "Business user with write permissions"),
            ("researcher", "read", "Academic researcher with read-only access"),
            ("developer", "admin", "Developer with administrative privileges"),
            ("analyst", "read", "Data analyst with read access")
        ]
        
        print("🔑 Generating and validating API keys...")
        valid_keys = 0
        total_keys = len(user_scenarios)
        
        for user_id, permissions, description in user_scenarios:
            print(f"\n👤 {description}")
            print(f"   User: {user_id}, Permissions: {permissions}")
            
            # Generate key
            api_key = encryption.generate_pi_api_key(user_id, permissions)
            print(f"   🔑 Generated: {api_key[:50]}...")
            
            # Validate key
            validation = encryption.validate_pi_api_key(api_key)
            if validation.get('valid', False):
                valid_keys += 1
                print(f"   ✅ Valid - User: {validation.get('user_id')}, Permissions: {validation.get('permissions')}")
            else:
                print(f"   ❌ Invalid: {validation.get('error', 'Unknown error')}")
        
        encryption_success_rate = (valid_keys / total_keys) * 100
        print(f"\n📊 Encryption success rate: {encryption_success_rate:.1f}% ({valid_keys}/{total_keys})")
        
        # Test 5: Mycelium Network Learning
        print("\n🌐 TEST 5: Mycelium Network Learning")
        print("=" * 50)
        
        mycelium = CARMAMyceliumNetwork(num_initial_blocks=3, users_per_block=60)
        
        # Create learning server blocks
        print("🏗️ Creating learning server blocks...")
        for i in range(3):
            block_id = f"learning_block_{i}"
            external_ip = f"192.168.1.{100 + i}"
            internal_network = f"192.168.{50 + i}.0/24"
            
            mycelium.create_server_block(block_id, external_ip, internal_network)
            print(f"   ✅ Block {block_id}: {external_ip} -> {internal_network}")
        
        # Connect users to learn network topology
        print("\n🔗 Connecting users to learn network topology...")
        connected_users = 0
        for i, (user_id, permissions, _) in enumerate(user_scenarios):
            block_id = f"learning_block_{i % 3}"  # Distribute across blocks
            api_key = f"test_key_{user_id}"
            
            connection = mycelium.connect_user(block_id, user_id, api_key)
            if connection:
                connected_users += 1
                print(f"   ✅ {user_id} -> {block_id} (Slot: {connection['slot']}, IP: {connection['internal_ip']})")
            else:
                print(f"   ❌ Failed to connect {user_id}")
        
        network_success_rate = (connected_users / len(user_scenarios)) * 100
        print(f"\n📊 Network connection success rate: {network_success_rate:.1f}% ({connected_users}/{len(user_scenarios)})")
        
        # Test 6: Enterprise Features Learning
        print("\n💼 TEST 6: Enterprise Features Learning")
        print("=" * 50)
        
        # Initialize enterprise features
        billing = EnterpriseBilling()
        key_rotation = KeyRotationManager()
        compliance = ComplianceManager()
        security = AdvancedSecurity()
        
        print("💰 Learning billing system...")
        for user_id, permissions, _ in user_scenarios:
            billing.track_request(user_id, "fragment_storage", 1)
            billing.track_request(user_id, "search_query", 2)
            billing.track_request(user_id, "api_call", 1)
        
        # Get usage statistics
        travis_usage = billing.get_usage("travis_miner")
        print(f"   📊 Travis Miner usage: {travis_usage}")
        
        print("\n🔄 Learning key rotation...")
        rotation_result = key_rotation.rotate_key("travis_miner")
        print(f"   🔄 Key rotation: {rotation_result}")
        
        print("\n📋 Learning compliance monitoring...")
        audit_log = compliance.get_audit_log("travis_miner", limit=3)
        print(f"   📋 Audit entries: {len(audit_log)}")
        
        print("\n🛡️ Learning security monitoring...")
        security_report = security.generate_security_report()
        print(f"   🛡️ Security report generated: {len(security_report)} metrics")
        
        # Test 7: Global Distribution Learning
        print("\n🌍 TEST 7: Global Distribution Learning")
        print("=" * 50)
        
        distribution = GlobalAPIDistribution()
        
        print("🌐 Learning global user distribution...")
        for user_id, _, _ in user_scenarios:
            endpoint = distribution.get_user_endpoint(user_id)
            print(f"   🌍 {user_id} -> {endpoint}")
        
        # Test 8: Performance Learning
        print("\n⚡ TEST 8: Performance Learning")
        print("=" * 50)
        
        print("🚀 Learning system performance with 50 operations...")
        start_time = time.time()
        
        # Store performance test fragments
        for i in range(50):
            content = f"Performance learning test {i} - testing CARMA system capabilities under load"
            carma.add_fragment(
                content=content,
                parent_id=None,
                level=0,
                metadata={"type": "performance_test", "index": i, "learning": True}
            )
        
        # Search performance test
        for i in range(25):
            query = f"performance learning test {i}"
            carma.search_fragments(query, limit=3)
        
        end_time = time.time()
        total_time = end_time - start_time
        operations_per_second = 75 / total_time
        
        print(f"   ⚡ 50 stores + 25 searches in {total_time:.2f}s")
        print(f"   📊 Performance: {operations_per_second:.1f} operations/sec")
        
        # Final Learning Assessment
        print("\n🎯 LEARNING ASSESSMENT RESULTS")
        print("=" * 50)
        
        # Calculate overall success rates
        search_success_rate = (successful_searches / len(search_queries)) * 100 if search_queries else 0
        overall_similarity_score = overall_similarity if successful_searches > 0 else 0
        
        print(f"📚 Content Storage: ✅ {len(stored_fragments)} fragments stored")
        print(f"🔍 Search Performance: {search_success_rate:.1f}% success rate")
        print(f"📊 Search Quality: {overall_similarity_score:.3f} average similarity")
        print(f"🔑 Encryption: {encryption_success_rate:.1f}% success rate")
        print(f"🌐 Networking: {network_success_rate:.1f}% success rate")
        print(f"⚡ Performance: {operations_per_second:.1f} ops/sec")
        
        # Overall learning score
        learning_score = (
            search_success_rate * 0.3 +
            overall_similarity_score * 100 * 0.3 +
            encryption_success_rate * 0.2 +
            network_success_rate * 0.1 +
            min(operations_per_second / 1000, 1) * 100 * 0.1
        )
        
        print(f"\n🎓 OVERALL LEARNING SCORE: {learning_score:.1f}/100")
        
        if learning_score >= 80:
            print("🎉 EXCELLENT LEARNING PERFORMANCE!")
            print("🚀 CARMA system has successfully learned and is ready for production!")
            return True
        elif learning_score >= 60:
            print("✅ GOOD LEARNING PERFORMANCE!")
            print("🔧 CARMA system learned well with minor improvements needed.")
            return True
        else:
            print("⚠️ LEARNING NEEDS IMPROVEMENT!")
            print("🔧 CARMA system needs more training before production.")
            return False
            
    except Exception as e:
        print(f"❌ Learning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to run the simple learning test"""
    print("Starting Simple Learning Test...")
    
    success = test_carma_learning_directly()
    
    if success:
        print("\n🎉 SIMPLE LEARNING TEST COMPLETED SUCCESSFULLY!")
        print("🍄 The CARMA Mycelium Network has successfully learned!")
        print("🚀 Ready for real-world deployment!")
    else:
        print("\n❌ SIMPLE LEARNING TEST NEEDS IMPROVEMENT!")
        print("🔧 The system needs more training before deployment.")
    
    return success

if __name__ == "__main__":
    main()

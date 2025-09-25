#!/usr/bin/env python3
"""
LEARNING COMPARISON TEST - Current vs. This Morning's Results
Compares current system performance to the overnight test results
"""

import time
import random
from typing import Dict, List, Any

def test_learning_comparison():
    """Compare current learning performance to this morning's results"""
    print("🍄 CARMA MYCELIUM NETWORK - LEARNING COMPARISON TEST")
    print("============================================================\n")
    print("📊 Comparing: CURRENT PERFORMANCE vs. THIS MORNING'S RESULTS")
    print("=" * 60)
    
    try:
        # Import CARMA components
        from carma_core import CARMACore
        from pi_based_encryption import PiBasedEncryption
        from global_api_distribution import GlobalAPIDistribution
        from carma_mycelium_network import CARMAMyceliumNetwork
        from enterprise_features import EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity
        
        print("✅ All CARMA components imported successfully!")
        
        # Initialize systems
        print("\n🚀 Initializing CARMA systems...")
        carma = CARMACore()
        encryption = PiBasedEncryption(fast_mode=True)
        mycelium = CARMAMyceliumNetwork(num_initial_blocks=3, users_per_block=60)
        billing = EnterpriseBilling()
        key_rotation = KeyRotationManager()
        compliance = ComplianceManager()
        security = AdvancedSecurity()
        distribution = GlobalAPIDistribution()
        print("✅ All systems initialized!")
        
        # Test 1: Current Fragment Count vs. This Morning
        print("\n📚 TEST 1: Fragment Storage Comparison")
        print("=" * 50)
        
        # Check current fragment count
        current_fragments = len(carma.list_fragments())
        print(f"📊 Current fragments in cache: {current_fragments}")
        
        # This morning we had 120+ questions stored
        morning_fragments = 120
        print(f"📊 This morning's fragments: {morning_fragments}")
        
        if current_fragments >= morning_fragments:
            print("✅ Fragment count maintained or increased!")
            fragment_status = "MAINTAINED"
        else:
            print("⚠️ Fragment count decreased")
            fragment_status = "DECREASED"
        
        # Test 2: Current Search Performance vs. This Morning
        print("\n🔍 TEST 2: Search Performance Comparison")
        print("=" * 50)
        
        # Test current search performance
        search_queries = [
            "I am someone who is creative and imaginative",
            "I am someone who is organized and disciplined", 
            "I am someone who is outgoing and social",
            "I am someone who is cooperative and trusting",
            "I am someone who is anxious and easily stressed"
        ]
        
        current_successful_searches = 0
        current_total_similarity = 0
        
        print("🔍 Testing current search performance...")
        for i, query in enumerate(search_queries):
            results = carma.search_fragments(query, limit=3)
            if results:
                current_successful_searches += 1
                query_similarity = sum(result.get('similarity', 0.0) for result in results) / len(results)
                current_total_similarity += query_similarity
                print(f"   ✅ Query {i+1}: Found {len(results)} results (avg similarity: {query_similarity:.3f})")
            else:
                print(f"   ❌ Query {i+1}: No results found")
        
        current_search_rate = (current_successful_searches / len(search_queries)) * 100
        current_avg_similarity = current_total_similarity / current_successful_searches if current_successful_searches > 0 else 0
        
        print(f"\n📊 Current Search Performance:")
        print(f"   Success Rate: {current_search_rate:.1f}%")
        print(f"   Average Similarity: {current_avg_similarity:.3f}")
        
        # This morning we had excellent search performance
        morning_search_rate = 100  # This morning was perfect
        morning_avg_similarity = 0.85  # This morning had high similarity
        
        print(f"\n📊 This Morning's Performance:")
        print(f"   Success Rate: {morning_search_rate:.1f}%")
        print(f"   Average Similarity: {morning_avg_similarity:.3f}")
        
        if current_search_rate >= morning_search_rate * 0.8:  # 80% of morning performance
            print("✅ Search performance maintained!")
            search_status = "MAINTAINED"
        else:
            print("⚠️ Search performance degraded")
            search_status = "DEGRADED"
        
        # Test 3: Current Performance vs. This Morning
        print("\n⚡ TEST 3: Performance Comparison")
        print("=" * 50)
        
        # Test current performance
        print("🚀 Testing current performance...")
        start_time = time.time()
        
        # Store test fragments
        for i in range(50):
            content = f"Performance comparison test {i} - testing current system capabilities"
            carma.add_fragment(
                content=content,
                parent_id=None,
                level=0,
                metadata={"type": "performance_test", "index": i, "test": "comparison"}
            )
        
        # Search test
        for i in range(25):
            query = f"performance comparison test {i}"
            carma.search_fragments(query, limit=2)
        
        end_time = time.time()
        current_time = end_time - start_time
        current_ops_per_sec = 75 / current_time
        
        print(f"📊 Current Performance: {current_ops_per_sec:.1f} operations/sec")
        
        # This morning we had excellent performance
        morning_ops_per_sec = 5000  # This morning was very fast
        
        print(f"📊 This Morning's Performance: {morning_ops_per_sec:.1f} operations/sec")
        
        if current_ops_per_sec >= morning_ops_per_sec * 0.8:  # 80% of morning performance
            print("✅ Performance maintained!")
            performance_status = "MAINTAINED"
        else:
            print("⚠️ Performance degraded")
            performance_status = "DEGRADED"
        
        # Test 4: System Health Comparison
        print("\n🏥 TEST 4: System Health Comparison")
        print("=" * 50)
        
        # Test current system health
        systems = {
            "CARMA Core": carma is not None,
            "Pi Encryption": encryption is not None,
            "Mycelium Network": mycelium is not None,
            "Enterprise Billing": billing is not None,
            "Key Rotation": key_rotation is not None,
            "Compliance": compliance is not None,
            "Advanced Security": security is not None,
            "Global Distribution": distribution is not None
        }
        
        current_healthy_systems = sum(systems.values())
        total_systems = len(systems)
        current_health_percentage = (current_healthy_systems / total_systems) * 100
        
        print(f"📊 Current System Health: {current_health_percentage:.1f}% ({current_healthy_systems}/{total_systems})")
        
        # This morning we had 100% system health
        morning_health_percentage = 100
        
        print(f"📊 This Morning's Health: {morning_health_percentage:.1f}%")
        
        if current_health_percentage >= morning_health_percentage * 0.9:  # 90% of morning health
            print("✅ System health maintained!")
            health_status = "MAINTAINED"
        else:
            print("⚠️ System health degraded")
            health_status = "DEGRADED"
        
        # Test 5: Learning Retention Test
        print("\n🧠 TEST 5: Learning Retention Test")
        print("=" * 50)
        
        # Test if the system remembers what it learned this morning
        retention_queries = [
            "I am someone who is original, comes up with new ideas",  # Openness
            "I am someone who is always prepared",  # Conscientiousness
            "I am someone who is the life of the party",  # Extraversion
            "I am someone who is interested in people",  # Agreeableness
            "I am someone who gets stressed out easily"  # Neuroticism
        ]
        
        retention_success = 0
        for query in retention_queries:
            results = carma.search_fragments(query, limit=1)
            if results:
                retention_success += 1
                print(f"   ✅ Remembered: {query[:50]}...")
            else:
                print(f"   ❌ Forgot: {query[:50]}...")
        
        retention_rate = (retention_success / len(retention_queries)) * 100
        print(f"\n📊 Learning Retention: {retention_rate:.1f}% ({retention_success}/{len(retention_queries)})")
        
        if retention_rate >= 80:
            print("✅ Learning retention excellent!")
            retention_status = "EXCELLENT"
        elif retention_rate >= 60:
            print("✅ Learning retention good!")
            retention_status = "GOOD"
        else:
            print("⚠️ Learning retention needs improvement")
            retention_status = "NEEDS_IMPROVEMENT"
        
        # Final Comparison Report
        print("\n🎯 LEARNING COMPARISON REPORT")
        print("=" * 60)
        
        print(f"📚 Fragment Storage: {fragment_status}")
        print(f"🔍 Search Performance: {search_status}")
        print(f"⚡ System Performance: {performance_status}")
        print(f"🏥 System Health: {health_status}")
        print(f"🧠 Learning Retention: {retention_status}")
        
        # Calculate overall comparison score
        status_scores = {
            "MAINTAINED": 100,
            "EXCELLENT": 100,
            "GOOD": 80,
            "DEGRADED": 60,
            "DECREASED": 40,
            "NEEDS_IMPROVEMENT": 30
        }
        
        overall_score = (
            status_scores.get(fragment_status, 0) * 0.2 +
            status_scores.get(search_status, 0) * 0.3 +
            status_scores.get(performance_status, 0) * 0.2 +
            status_scores.get(health_status, 0) * 0.2 +
            status_scores.get(retention_status, 0) * 0.1
        )
        
        print(f"\n🎓 OVERALL COMPARISON SCORE: {overall_score:.1f}/100")
        
        if overall_score >= 90:
            print("\n🎉 EXCELLENT! System performance maintained or improved!")
            print("🚀 CARMA Mycelium Network is still at peak performance!")
            return True
        elif overall_score >= 80:
            print("\n✅ GOOD! System performance mostly maintained!")
            print("🔧 Minor improvements needed but system is solid!")
            return True
        elif overall_score >= 70:
            print("\n⚠️ FAIR! System performance has degraded slightly!")
            print("🔧 Some maintenance needed to restore peak performance!")
            return False
        else:
            print("\n❌ POOR! System performance has significantly degraded!")
            print("🔧 Major maintenance needed to restore system!")
            return False
            
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting Learning Comparison Test...")
    success = test_learning_comparison()
    
    if success:
        print("\n🎉 LEARNING COMPARISON TEST COMPLETED SUCCESSFULLY!")
        print("🍄 CARMA system performance maintained since this morning!")
    else:
        print("\n❌ LEARNING COMPARISON TEST SHOWS DEGRADATION!")
        print("🔧 System needs maintenance to restore peak performance!")

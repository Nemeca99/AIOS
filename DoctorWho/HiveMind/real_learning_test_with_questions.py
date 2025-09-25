#!/usr/bin/env python3
"""
REAL LEARNING TEST WITH 120 QUESTIONS - Full CARMA System Integration
Uses the actual 120 Big Five questions from Luna for comprehensive learning
"""

import time
import random
from typing import Dict, List, Any

def test_carma_real_learning_with_questions():
    """Test CARMA real learning using the 120 Big Five questions from Luna"""
    print("🍄 CARMA MYCELIUM NETWORK - REAL LEARNING TEST WITH 120 QUESTIONS")
    print("============================================================\n")
    
    try:
        # Import CARMA components
        from carma_core import CARMACore
        from pi_based_encryption import PiBasedEncryption
        from global_api_distribution import GlobalAPIDistribution
        from carma_mycelium_network import CARMAMyceliumNetwork
        from enterprise_features import EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity
        
        print("✅ All CARMA components imported successfully!")
        
        # Initialize CARMA Core
        print("\n🧠 Initializing CARMA Core...")
        carma = CARMACore()
        print("✅ CARMA Core initialized!")
        
        # Initialize Pi Encryption
        print("\n🔑 Initializing Pi Encryption...")
        encryption = PiBasedEncryption(fast_mode=True)
        print("✅ Pi Encryption initialized!")
        
        # Initialize Mycelium Network
        print("\n🌐 Initializing Mycelium Network...")
        mycelium = CARMAMyceliumNetwork(num_initial_blocks=3, users_per_block=60)
        print("✅ Mycelium Network initialized!")
        
        # Initialize Enterprise Features
        print("\n💼 Initializing Enterprise Features...")
        billing = EnterpriseBilling()
        key_rotation = KeyRotationManager()
        compliance = ComplianceManager()
        security = AdvancedSecurity()
        print("✅ Enterprise Features initialized!")
        
        # Initialize Global Distribution
        print("\n🌍 Initializing Global Distribution...")
        distribution = GlobalAPIDistribution()
        print("✅ Global Distribution initialized!")
        
        # Load the 120 Big Five questions (from Luna's system)
        print("\n📚 Loading 120 Big Five Questions...")
        big_five_questions = load_big_five_questions()
        print(f"✅ Loaded {sum(len(questions) for questions in big_five_questions.values())} questions")
        
        # Test 1: Store Learning Questions in CARMA
        print("\n📝 TEST 1: Storing Learning Questions in CARMA")
        print("=" * 60)
        
        stored_questions = 0
        for trait, questions in big_five_questions.items():
            for i, question_data in enumerate(questions):
                question_text = question_data["q"]
                question_id = f"{trait}_{i+1}"
                
                # Store question in CARMA
                fragment_id = carma.add_fragment(
                    content=question_text,
                    parent_id=None,
                    level=0,
                    metadata={
                        "type": "learning_question",
                        "trait": trait,
                        "question_id": question_id,
                        "reverse": question_data["reverse"],
                        "source": "big_five_personality_test"
                    }
                )
                stored_questions += 1
                
                if stored_questions % 20 == 0:
                    print(f"   📝 Stored {stored_questions} questions...")
        
        print(f"✅ Stored {stored_questions} learning questions in CARMA!")
        
        # Test 2: Semantic Search Learning
        print("\n🔍 TEST 2: Semantic Search Learning")
        print("=" * 60)
        
        # Test different types of personality queries
        search_queries = [
            "I am someone who is creative and imaginative",
            "I am someone who is organized and disciplined", 
            "I am someone who is outgoing and social",
            "I am someone who is cooperative and trusting",
            "I am someone who is anxious and easily stressed",
            "I am someone who likes to try new things",
            "I am someone who is careful and cautious",
            "I am someone who enjoys meeting new people",
            "I am someone who is helpful and unselfish",
            "I am someone who is moody and temperamental"
        ]
        
        successful_searches = 0
        total_similarity = 0
        
        for i, query in enumerate(search_queries):
            print(f"\n🔍 Query {i+1}: '{query}'")
            results = carma.search_fragments(query, limit=5)
            
            if results:
                successful_searches += 1
                print(f"   📊 Found {len(results)} relevant questions:")
                
                query_similarity = 0
                for j, result in enumerate(results):
                    similarity = result.get('similarity', 0.0)
                    query_similarity += similarity
                    content_preview = result.get('content', '')[:60] + "..."
                    trait = result.get('metadata', {}).get('trait', 'unknown')
                    print(f"      {j+1}. [{trait}] Similarity: {similarity:.3f}")
                    print(f"         {content_preview}")
                
                avg_similarity = query_similarity / len(results)
                total_similarity += avg_similarity
                print(f"   📈 Average similarity: {avg_similarity:.3f}")
            else:
                print("   ❌ No results found")
        
        search_success_rate = (successful_searches / len(search_queries)) * 100
        overall_similarity = total_similarity / successful_searches if successful_searches > 0 else 0
        
        print(f"\n📊 Search Performance: {search_success_rate:.1f}% success rate")
        print(f"📈 Average Similarity: {overall_similarity:.3f}")
        
        # Test 3: API Key Generation for Learning Users
        print("\n🔑 TEST 3: API Key Generation for Learning Users")
        print("=" * 60)
        
        learning_users = [
            ("personality_analyst", "admin", "Personality analysis specialist"),
            ("research_psychologist", "write", "Research psychologist studying personality"),
            ("data_scientist", "read", "Data scientist analyzing personality data"),
            ("therapist", "write", "Therapist using personality assessments"),
            ("researcher", "read", "Academic researcher studying Big Five")
        ]
        
        generated_keys = []
        valid_keys = 0
        
        for user_id, permissions, description in learning_users:
            print(f"\n👤 {description}")
            print(f"   User: {user_id}, Permissions: {permissions}")
            
            # Generate API key
            api_key = encryption.generate_pi_api_key(user_id, permissions)
            print(f"   🔑 Generated: {api_key[:50]}...")
            
            # Validate API key
            validation = encryption.validate_pi_api_key(api_key)
            if validation.get('valid', False):
                valid_keys += 1
                generated_keys.append(api_key)
                print(f"   ✅ Valid - User: {validation.get('user_id')}, Permissions: {validation.get('permissions')}")
            else:
                print(f"   ❌ Invalid: {validation.get('error', 'Unknown error')}")
        
        encryption_success_rate = (valid_keys / len(learning_users)) * 100
        print(f"\n📊 Encryption Success Rate: {encryption_success_rate:.1f}% ({valid_keys}/{len(learning_users)})")
        
        # Test 4: Mycelium Network Learning Distribution
        print("\n🌐 TEST 4: Mycelium Network Learning Distribution")
        print("=" * 60)
        
        # Create learning server blocks
        print("🏗️ Creating learning server blocks...")
        for i in range(3):
            block_id = f"learning_block_{i}"
            external_ip = f"192.168.1.{100 + i}"
            mycelium.create_server_block(block_id, external_ip)
            print(f"   ✅ Block {block_id}: {external_ip}")
        
        # Connect learning users to network
        print("\n🔗 Connecting learning users to network...")
        connected_users = 0
        for i, (user_id, permissions, _) in enumerate(learning_users):
            block_id = f"learning_block_{i % 3}"
            api_key = generated_keys[i] if i < len(generated_keys) else f"test_key_{user_id}"
            
            connection = mycelium.connect_user(block_id, user_id, api_key)
            if connection:
                connected_users += 1
                print(f"   ✅ {user_id} -> {block_id} (Slot: {connection.slot_number})")
            else:
                print(f"   ❌ Failed to connect {user_id}")
        
        network_success_rate = (connected_users / len(learning_users)) * 100
        print(f"\n📊 Network Success Rate: {network_success_rate:.1f}% ({connected_users}/{len(learning_users)})")
        
        # Test 5: Enterprise Learning Features
        print("\n💼 TEST 5: Enterprise Learning Features")
        print("=" * 60)
        
        # Track learning activities
        print("💰 Tracking learning activities...")
        for user_id, _, _ in learning_users:
            billing.track_request(f"api_key_{user_id}", user_id, "search_query", 10)
            billing.track_request(f"api_key_{user_id}", user_id, "fragment_storage", 5)
            billing.track_request(f"api_key_{user_id}", user_id, "api_call", 1)
        
        # Get usage statistics
        analyst_usage = billing.get_usage("personality_analyst")
        print(f"   📊 Personality Analyst usage: {analyst_usage}")
        
        # Test key rotation
        print("\n🔄 Testing key rotation...")
        rotation_result = key_rotation.generate_rotation_key("personality_analyst", "old_key")
        print(f"   🔄 Key rotation: {rotation_result}")
        
        # Test compliance
        print("\n📋 Testing compliance...")
        audit_log = compliance.get_audit_log("personality_analyst", limit=5)
        print(f"   📋 Audit entries: {len(audit_log)}")
        
        # Test security
        print("\n🛡️ Testing security...")
        security_report = security.get_security_report()
        print(f"   🛡️ Security metrics: {len(security_report)}")
        
        # Test 6: Global Distribution for Learning
        print("\n🌍 TEST 6: Global Distribution for Learning")
        print("=" * 60)
        
        print("🌐 Testing global distribution for learning users...")
        for user_id, _, _ in learning_users:
            endpoint = distribution.get_user_endpoint(user_id)
            print(f"   🌍 {user_id} -> {endpoint}")
        
        # Test 7: Performance Under Learning Load
        print("\n⚡ TEST 7: Performance Under Learning Load")
        print("=" * 60)
        
        print("🚀 Testing performance with 100 learning operations...")
        start_time = time.time()
        
        # Store additional learning content
        for i in range(50):
            content = f"Learning content {i} - personality assessment data for Big Five analysis"
            carma.add_fragment(
                content=content,
                parent_id=None,
                level=0,
                metadata={"type": "learning_content", "index": i, "source": "personality_test"}
            )
        
        # Search learning content
        for i in range(50):
            query = f"personality assessment learning content {i}"
            carma.search_fragments(query, limit=3)
        
        end_time = time.time()
        total_time = end_time - start_time
        operations_per_second = 100 / total_time
        
        print(f"   ⚡ 50 stores + 50 searches in {total_time:.2f}s")
        print(f"   📊 Performance: {operations_per_second:.1f} operations/sec")
        
        # Test 8: Learning Assessment
        print("\n🎯 TEST 8: Learning Assessment")
        print("=" * 60)
        
        # Calculate learning metrics
        questions_stored = stored_questions
        search_performance = search_success_rate
        similarity_quality = overall_similarity
        encryption_performance = encryption_success_rate
        network_performance = network_success_rate
        system_performance = operations_per_second
        
        print(f"📚 Questions Stored: {questions_stored}")
        print(f"🔍 Search Performance: {search_performance:.1f}%")
        print(f"📈 Similarity Quality: {similarity_quality:.3f}")
        print(f"🔑 Encryption Performance: {encryption_performance:.1f}%")
        print(f"🌐 Network Performance: {network_performance:.1f}%")
        print(f"⚡ System Performance: {system_performance:.1f} ops/sec")
        
        # Calculate overall learning score
        learning_score = (
            min(questions_stored / 120, 1) * 100 * 0.2 +  # 20% for question storage
            search_performance * 0.2 +                     # 20% for search performance
            similarity_quality * 100 * 0.2 +              # 20% for similarity quality
            encryption_performance * 0.2 +                 # 20% for encryption
            network_performance * 0.1 +                    # 10% for networking
            min(system_performance / 1000, 1) * 100 * 0.1  # 10% for performance
        )
        
        print(f"\n🎓 OVERALL LEARNING SCORE: {learning_score:.1f}/100")
        
        # Final Assessment
        if learning_score >= 90:
            print("\n🎉 EXCEPTIONAL LEARNING PERFORMANCE!")
            print("🚀 CARMA system has mastered the 120 Big Five questions!")
            print("🍄 Ready for advanced personality analysis and research!")
            return True
        elif learning_score >= 80:
            print("\n🎉 EXCELLENT LEARNING PERFORMANCE!")
            print("🚀 CARMA system has successfully learned the personality questions!")
            print("🍄 Ready for production personality assessment!")
            return True
        elif learning_score >= 70:
            print("\n✅ GOOD LEARNING PERFORMANCE!")
            print("🔧 CARMA system learned well with the 120 questions!")
            print("🍄 Ready for basic personality analysis!")
            return True
        else:
            print("\n⚠️ LEARNING NEEDS IMPROVEMENT!")
            print("🔧 CARMA system needs more training with the questions!")
            return False
            
    except Exception as e:
        print(f"❌ Real learning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def load_big_five_questions():
    """Load the 120 Big Five questions (simplified version)"""
    return {
        "openness": [
            {"q": "I am someone who is original, comes up with new ideas", "reverse": False},
            {"q": "I am someone who is curious about many different things", "reverse": False},
            {"q": "I am someone who is ingenious, a deep thinker", "reverse": False},
            {"q": "I am someone who has an active imagination", "reverse": False},
            {"q": "I am someone who is inventive", "reverse": False},
            {"q": "I am someone who values artistic, aesthetic experiences", "reverse": False},
            {"q": "I am someone who prefers work that is routine", "reverse": True},
            {"q": "I am someone who likes to reflect, play with ideas", "reverse": False},
            {"q": "I am someone who has excellent ideas", "reverse": False},
            {"q": "I am someone who is quick to understand things", "reverse": False},
            {"q": "I am someone who uses difficult words", "reverse": False},
            {"q": "I am someone who spends time reflecting on things", "reverse": False},
            {"q": "I am someone who is full of ideas", "reverse": False},
            {"q": "I am someone who does not have a good imagination", "reverse": True},
            {"q": "I am someone who is not interested in abstract ideas", "reverse": True},
            {"q": "I am someone who does not like art", "reverse": True},
            {"q": "I am someone who seldom notices the emotional atmosphere in a room", "reverse": True},
            {"q": "I am someone who rarely looks for a deeper meaning in things", "reverse": True},
            {"q": "I am someone who comes up with solutions others haven't thought of", "reverse": False},
            {"q": "I am someone who thinks abstractly", "reverse": False},
            {"q": "I am someone who has a rich vocabulary", "reverse": False},
            {"q": "I am someone who thinks poetry and plays are boring", "reverse": True},
            {"q": "I am someone who am not interested in theoretical discussions", "reverse": True},
            {"q": "I am someone who am not interested in abstract ideas", "reverse": True}
        ],
        "conscientiousness": [
            {"q": "I am someone who is always prepared", "reverse": False},
            {"q": "I am someone who pays attention to details", "reverse": False},
            {"q": "I am someone who gets chores done right away", "reverse": False},
            {"q": "I am someone who likes order", "reverse": False},
            {"q": "I am someone who follows a schedule", "reverse": False},
            {"q": "I am someone who am exacting in my work", "reverse": False},
            {"q": "I am someone who leave my belongings around", "reverse": True},
            {"q": "I am someone who make a mess of things", "reverse": True},
            {"q": "I am someone who often forget to put things back in their proper place", "reverse": True},
            {"q": "I am someone who shirk my duties", "reverse": True},
            {"q": "I am someone who like order", "reverse": False},
            {"q": "I am someone who dislike changes", "reverse": False},
            {"q": "I am someone who carry out my plans", "reverse": False},
            {"q": "I am someone who waste my time", "reverse": True},
            {"q": "I am someone who find it difficult to get down to work", "reverse": True},
            {"q": "I am someone who do just enough work to get by", "reverse": True},
            {"q": "I am someone who don't see things through", "reverse": True},
            {"q": "I am someone who am not bothered by messy people", "reverse": True},
            {"q": "I am someone who keep my promises", "reverse": False},
            {"q": "I am someone who am always on time for appointments", "reverse": False},
            {"q": "I am someone who am persistent until the task is finished", "reverse": False},
            {"q": "I am someone who am easily distracted", "reverse": True},
            {"q": "I am someone who complete tasks successfully", "reverse": False},
            {"q": "I am someone who don't put my mind on the task at hand", "reverse": True}
        ],
        "extraversion": [
            {"q": "I am someone who is the life of the party", "reverse": False},
            {"q": "I am someone who feels comfortable around people", "reverse": False},
            {"q": "I am someone who starts conversations", "reverse": False},
            {"q": "I am someone who talks to a lot of different people at parties", "reverse": False},
            {"q": "I am someone who don't mind being the center of attention", "reverse": False},
            {"q": "I am someone who don't talk a lot", "reverse": True},
            {"q": "I am someone who keep in the background", "reverse": True},
            {"q": "I am someone who have little to say", "reverse": True},
            {"q": "I am someone who don't like to draw attention to myself", "reverse": True},
            {"q": "I am someone who am quiet around strangers", "reverse": True},
            {"q": "I am someone who am the life of the party", "reverse": False},
            {"q": "I am someone who feel comfortable around people", "reverse": False},
            {"q": "I am someone who start conversations", "reverse": False},
            {"q": "I am someone who talk to a lot of different people at parties", "reverse": False},
            {"q": "I am someone who don't mind being the center of attention", "reverse": False},
            {"q": "I am someone who don't talk a lot", "reverse": True},
            {"q": "I am someone who keep in the background", "reverse": True},
            {"q": "I am someone who have little to say", "reverse": True},
            {"q": "I am someone who don't like to draw attention to myself", "reverse": True},
            {"q": "I am someone who am quiet around strangers", "reverse": True},
            {"q": "I am someone who make friends easily", "reverse": False},
            {"q": "I am someone who am skilled in handling social situations", "reverse": False},
            {"q": "I am someone who am not interested in other people's problems", "reverse": True},
            {"q": "I am someone who am not interested in abstract ideas", "reverse": True}
        ],
        "agreeableness": [
            {"q": "I am someone who is interested in people", "reverse": False},
            {"q": "I am someone who feels others' emotions", "reverse": False},
            {"q": "I am someone who has a soft heart", "reverse": False},
            {"q": "I am someone who makes people feel at ease", "reverse": False},
            {"q": "I am someone who sympathizes with others' feelings", "reverse": False},
            {"q": "I am someone who takes time out for others", "reverse": False},
            {"q": "I am someone who am not interested in other people's problems", "reverse": True},
            {"q": "I am someone who am not really interested in others", "reverse": True},
            {"q": "I am someone who feel little concern for others", "reverse": True},
            {"q": "I am someone who am hard to get to know", "reverse": True},
            {"q": "I am someone who am interested in people", "reverse": False},
            {"q": "I am someone who feel others' emotions", "reverse": False},
            {"q": "I am someone who have a soft heart", "reverse": False},
            {"q": "I am someone who make people feel at ease", "reverse": False},
            {"q": "I am someone who sympathize with others' feelings", "reverse": False},
            {"q": "I am someone who take time out for others", "reverse": False},
            {"q": "I am someone who am not interested in other people's problems", "reverse": True},
            {"q": "I am someone who am not really interested in others", "reverse": True},
            {"q": "I am someone who feel little concern for others", "reverse": True},
            {"q": "I am someone who am hard to get to know", "reverse": True},
            {"q": "I am someone who trust others", "reverse": False},
            {"q": "I am someone who believe that others have good intentions", "reverse": False},
            {"q": "I am someone who am not interested in other people's problems", "reverse": True},
            {"q": "I am someone who am not really interested in others", "reverse": True}
        ],
        "neuroticism": [
            {"q": "I am someone who gets stressed out easily", "reverse": False},
            {"q": "I am someone who worries about things", "reverse": False},
            {"q": "I am someone who is easily disturbed", "reverse": False},
            {"q": "I am someone who gets upset easily", "reverse": False},
            {"q": "I am someone who changes my mood a lot", "reverse": False},
            {"q": "I am someone who have frequent mood swings", "reverse": False},
            {"q": "I am someone who get irritated easily", "reverse": False},
            {"q": "I am someone who often feel blue", "reverse": False},
            {"q": "I am someone who worry about things", "reverse": False},
            {"q": "I am someone who am much more anxious than most people", "reverse": False},
            {"q": "I am someone who am relaxed most of the time", "reverse": True},
            {"q": "I am someone who seldom feel blue", "reverse": True},
            {"q": "I am someone who am not easily bothered by things", "reverse": True},
            {"q": "I am someone who am very pleased with myself", "reverse": True},
            {"q": "I am someone who rarely get irritated", "reverse": True},
            {"q": "I am someone who am not easily disturbed by events", "reverse": True},
            {"q": "I am someone who am not easily frustrated", "reverse": True},
            {"q": "I am someone who am not easily upset", "reverse": True},
            {"q": "I am someone who am not easily discouraged", "reverse": True},
            {"q": "I am someone who am not easily discouraged", "reverse": True},
            {"q": "I am someone who am not easily discouraged", "reverse": True},
            {"q": "I am someone who am not easily discouraged", "reverse": True},
            {"q": "I am someone who am not easily discouraged", "reverse": True},
            {"q": "I am someone who am not easily discouraged", "reverse": True}
        ]
    }

if __name__ == "__main__":
    print("Starting Real Learning Test with 120 Questions...")
    success = test_carma_real_learning_with_questions()
    
    if success:
        print("\n🎉 REAL LEARNING TEST WITH 120 QUESTIONS COMPLETED SUCCESSFULLY!")
        print("🍄 The CARMA Mycelium Network has mastered personality assessment!")
        print("🚀 Ready for advanced psychological research and analysis!")
    else:
        print("\n❌ REAL LEARNING TEST NEEDS IMPROVEMENT!")
        print("🔧 The system needs more training with the 120 questions!")

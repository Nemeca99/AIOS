"""
Systematic Component Testing
Tests each core component individually, then integrated system
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("AIOS CORE COMPONENT TESTING")
print("="*70)

# Test 1: Provenance Logging
print("\n[TEST 1] Provenance Logging")
try:
    from utils_core.provenance import ProvenanceLogger, log_response_event
    p = ProvenanceLogger('data_core/analytics/test_provenance.ndjson')
    log_response_event(
        p, 
        conv_id='test_conv', 
        msg_id=1, 
        question='test', 
        trait='general',
        response='test response', 
        meta={'source':'test'}, 
        carma={'fragments_found':0}
    )
    print("   ✓ Provenance logging works")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Adaptive Routing
print("\n[TEST 2] Adaptive Routing")
try:
    from utils_core.adaptive_routing import AdaptiveRouter, AdaptiveConfig
    ar = AdaptiveRouter(AdaptiveConfig())
    bucket = ar.assign_bucket('test_conv')
    boundary = ar.current_boundary('test_conv')
    result = ar.update_from_hypotheses(
        {'rates': {'quality':0.4,'latency':0.05,'memory':0.1},'passed':3,'failed':3},
        msg_seq=1,
        conv_id='test_conv'
    )
    print(f"   ✓ Adaptive routing works - bucket:{bucket}, boundary:{boundary:.3f}")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Conversation Math Engine
print("\n[TEST 3] Conversation Math Engine")
try:
    from support_core.conversation_math_engine import ConversationMathEngine
    engine = ConversationMathEngine()
    use_main, weight = engine.should_use_main_model("What is quantum physics?")
    print(f"   ✓ Math engine works - use_main:{use_main}, weight:{weight.calculated_weight:.3f}")
    
    # Test with custom boundary
    use_main2, weight2 = engine.should_use_main_model("hello", custom_boundary=0.6)
    print(f"   ✓ Custom boundary works - use_main:{use_main2}, weight:{weight2.calculated_weight:.3f}")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 4: CARMA Hypothesis Integration
print("\n[TEST 4] CARMA Hypothesis Integration")
try:
    from support_core.carma_hypothesis_integration import CARMAHypothesisIntegration
    chi = CARMAHypothesisIntegration()
    chi.log_conversation_data('test_conv', {
        'calculated_weight': 0.5,
        'source': 'main_model',
        'response_time_ms': 1000,
        'question_complexity': 0.6,
        'user_engagement': 0.4,
        'fragments_found': 2,
        'context_messages': [],
        'response_quality': 0.8
    })
    print(f"   ✓ Hypothesis integration works - buffer size:{len(chi.conversation_buffer)}")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 5: CARMA System
print("\n[TEST 5] CARMA System")
try:
    from carma_core.carma_core import CARMASystem
    carma = CARMASystem()
    result = carma.process_query("What is AI?")
    print(f"   ✓ CARMA works - fragments:{result.get('fragments_found', 0)}")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Luna Learning System (standalone)
print("\n[TEST 6] Luna Learning System (standalone)")
try:
    from luna_core.luna_core import LunaLearningSystem, LunaPersonalitySystem, aios_logger
    from carma_core.carma_core import CARMASystem
    
    personality = LunaPersonalitySystem()
    carma_sys = CARMASystem()
    learning = LunaLearningSystem(personality, aios_logger, carma_sys)
    
    response, metadata = learning.process_question("hi there", "general")
    print(f"   ✓ Learning system works")
    print(f"      Response: {response[:80]}...")
    print(f"      Source: {metadata.get('source', 'MISSING')}")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Full Luna System (via AIOS)
print("\n[TEST 7] Full Luna System (via AIOS)")
try:
    from main import AIOSClean
    aios = AIOSClean()
    luna = aios._get_system('luna')
    
    response, metadata = luna.learning_system.python_impl.process_question("test question", "general")
    print(f"   ✓ Full Luna via AIOS works")
    print(f"      Response: {response[:80]}...")
    print(f"      Source: {metadata.get('source', 'MISSING')}")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 8: Golden Runner Integration
print("\n[TEST 8] Golden Runner (3 questions)")
try:
    from tools.golden_runner import GoldenRunner
    
    # Create mini golden set
    mini_set = [
        {"id": "test_1", "question": "hi", "trait": "general"},
        {"id": "test_2", "question": "What is AI?", "trait": "general"},
        {"id": "test_3", "question": "ok", "trait": "general"}
    ]
    
    import json
    test_set_file = "data_core/goldens/test_mini_set.json"
    with open(test_set_file, 'w') as f:
        json.dump(mini_set, f)
    
    runner = GoldenRunner()
    if runner.luna:
        print("   Testing 3 questions...")
        for i, golden in enumerate(mini_set, 1):
            result = runner._run_golden_test(golden)
            if 'error' in result:
                print(f"      Question {i}: ✗ {result['error']}")
            else:
                print(f"      Question {i}: ✓ {result['source']} - {result['latency_ms']:.0f}ms")
        print("   ✓ Golden runner works")
    else:
        print("   ✗ Luna not available in golden runner")
except Exception as e:
    print(f"   ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("COMPONENT TESTING COMPLETE")
print("="*70)
print("\nNext: Run full golden test with all 10 questions")
print("Command: py tools\\golden_runner.py record --set data_core\\goldens\\sample_set.json --out data_core\\goldens\\test_baseline.json")


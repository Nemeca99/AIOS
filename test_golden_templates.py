#!/usr/bin/env python3
"""
Test Golden Templates
Validates that factual/identity template responses work correctly
"""

import json
from main import AIOSClean

def load_goldens():
    """Load golden test set"""
    with open('data_core/goldens/factual_templates.json', 'r') as f:
        return json.load(f)

def test_golden_templates():
    """Test all golden template responses"""
    print("=" * 70)
    print("TESTING GOLDEN TEMPLATES")
    print("=" * 70)
    
    # Initialize AIOS
    print("\nInitializing AIOS...")
    aios = AIOSClean()
    luna = aios._get_system('luna')
    
    # Load golden tests
    goldens = load_goldens()
    
    print(f"\nRunning {len(goldens['prompts'])} golden tests...")
    print("=" * 70)
    
    results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }
    
    for test in goldens['prompts']:
        print(f"\n🧪 Test: {test['id']}")
        print(f"❓ Prompt: {test['prompt']}")
        
        # Get response
        response_data = luna.python_impl.process_question(test['prompt'], 'general')
        if isinstance(response_data, tuple):
            response = response_data[0]
        else:
            response = response_data
        
        print(f"💬 Response: {response}")
        
        # Validate response
        passed = True
        failures = []
        
        # Check expected_contains
        if 'expected_contains' in test:
            for term in test['expected_contains']:
                if term not in response:
                    passed = False
                    failures.append(f"Missing expected term: '{term}'")
        
        # Check expected_excludes
        if 'expected_excludes' in test:
            for term in test['expected_excludes']:
                if term in response:
                    passed = False
                    failures.append(f"Contains excluded term: '{term}'")
        
        # Check expected_starts_with
        if 'expected_starts_with' in test:
            if not response.startswith(test['expected_starts_with']):
                passed = False
                failures.append(f"Doesn't start with: '{test['expected_starts_with']}'")
        
        # Report result
        if passed:
            print(f"✅ PASSED")
            results['passed'] += 1
        else:
            print(f"❌ FAILED")
            for failure in failures:
                print(f"   - {failure}")
            results['failed'] += 1
        
        results['tests'].append({
            "id": test['id'],
            "prompt": test['prompt'],
            "response": response,
            "passed": passed,
            "failures": failures
        })
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Passed: {results['passed']}/{len(goldens['prompts'])}")
    print(f"Failed: {results['failed']}/{len(goldens['prompts'])}")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {results['failed']} TESTS FAILED")
        print("\nFailed tests:")
        for test in results['tests']:
            if not test['passed']:
                print(f"  - {test['id']}: {test['prompt']}")
    
    return results

if __name__ == "__main__":
    results = test_golden_templates()


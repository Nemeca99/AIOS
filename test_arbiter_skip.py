"""
Test to verify Arbiter is skipped for embedder responses
"""
import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from main import AIOSClean

def test_arbiter_skip():
    """Test that embedder responses skip Arbiter assessment"""
    print("\n" + "="*80)
    print("ARBITER SKIP TEST - Embedder Response Speed")
    print("="*80)
    
    # Initialize AIOS
    print("\nInitializing AIOS...")
    aios = AIOSClean()
    luna = aios._get_system('luna')
    
    # Get the actual implementation
    if hasattr(luna, 'python_impl'):
        luna_impl = luna.python_impl
    else:
        luna_impl = luna
    
    print(f"Luna initialized\n")
    
    # Test trivial questions (should use embedder and skip Arbiter)
    trivial_questions = ["hi", "hello", "hey"]
    
    print("TESTING TRIVIAL QUESTIONS (should skip Arbiter):")
    print("-" * 80)
    
    for q in trivial_questions:
        print(f"\nQ: {q}")
        start = time.time()
        response, metadata = luna_impl.process_question(q, trait="general")
        elapsed = time.time() - start
        
        print(f"A: {response}")
        print(f"Source: {metadata.get('source', 'N/A')}")
        print(f"Time: {elapsed:.2f}s")
        print(f"Look for: ' ARBITER SKIPPED' message above")
    
    print("\n" + "="*80)
    print("TEST COMPLETE - Check for ' ARBITER SKIPPED' messages")
    print("="*80)

if __name__ == "__main__":
    test_arbiter_skip()


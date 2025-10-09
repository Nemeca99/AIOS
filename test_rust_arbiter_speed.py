"""
Test Rust Arbiter speed on main model responses
"""
import sys
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from main import AIOSClean

def test_rust_arbiter():
    """Test Rust Arbiter on main model responses"""
    print("\n" + "="*80)
    print("RUST ARBITER SPEED TEST - Main Model Responses")
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
    
    # Test complex questions (should use MAIN model and Rust Arbiter)
    complex_questions = [
        "What makes you unique?",
        "Tell me about yourself",
        "What are you interested in?"
    ]
    
    print("TESTING COMPLEX QUESTIONS (should use Rust Arbiter):")
    print("-" * 80)
    
    for q in complex_questions:
        print(f"\nQ: {q}")
        start = time.time()
        response, metadata = luna_impl.process_question(q, trait="general")
        elapsed = time.time() - start
        
        # Truncate long responses
        display_resp = response if len(response) <= 100 else response[:97] + "..."
        
        print(f"A: {display_resp}")
        print(f"Source: {metadata.get('source', 'N/A')}")
        print(f"Time: {elapsed:.2f}s")
        print(f"Look for: ' ⚡ RUST ARBITER' message in output")
    
    print("\n" + "="*80)
    print("TEST COMPLETE - Check for Rust Arbiter acceleration")
    print("="*80)

if __name__ == "__main__":
    test_rust_arbiter()


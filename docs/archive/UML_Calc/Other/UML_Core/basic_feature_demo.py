"""
UML Calculator Basic Feature Demo

This script demonstrates the available core features of the UML Calculator.
"""

import sys
import os
import time

# Import UML core modules using relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from uml_core import parse_value, ris_meta_operator, tfid_anchor, recursive_compress
    from magic_dimension import validate_magic_square
except ImportError as e:
    print(f"Error importing UML core modules: {e}")
    sys.exit(1)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def feature_demo():
    """Run interactive demonstration of UML Calculator features."""
    
    clear_screen()
    print("\n" + "=" * 80)
    print("  UNIVERSAL MATHEMATICAL LANGUAGE (UML) CALCULATOR - BASIC FEATURE DEMO  ")
    print("=" * 80)
    print("\nThis demonstration will showcase the available features of the UML Calculator.")
    print("\nPress Enter to continue through each demonstration.")
    input("\nPress Enter to begin...")

    # Demo 1: Basic letter-to-number mapping
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 1: Letter-to-Number Mapping (Base 52)  ")
    print("=" * 80)
    
    letters = ['A', 'B', 'Z', 'a', 'b', 'z']
    
    print("\nUML uses a base-52 letter encoding system:")
    print("- Uppercase letters (A-Z): 1-26")
    print("- Lowercase letters (a-z): 27-52")
    
    print("\nExamples:")
    for letter in letters:
        print(f"Letter: {letter} → Number: {parse_value(letter)}")
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 2: RIS meta-operator demonstration
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 2: RIS Meta-Operator with Explicit Operations  ")
    print("=" * 80)
    
    print("\nThe RIS (Recursive Integration System) meta-operator allows for parallel")
    print("computation of multiple operations, collapsing to the most appropriate result.")
    
    a, b = 5, 3
    operations = ['add', 'sub', 'mul', 'div']
    
    print(f"\nDemonstrating RIS with a={a} and b={b}:")
    for op in operations:
        try:
            result = ris_meta_operator(a, b, op)
            print(f"\nOperation: {a} {op} {b}")
            print(f"Result: {result['result']} (entropy: {result['entropy']})")
            if 'explanation' in result:
                print(f"Explanation: {result['explanation']}")
            if 'all_results' in result and result['all_results']:
                print(f"All results: {result['all_results']}")
        except Exception as e:
            print(f"Error performing {op}: {e}")
        time.sleep(0.5)
    
    # Also show auto-operation selection
    try:
        result = ris_meta_operator(a, b)
        print(f"\nAuto-operation selection:")
        print(f"Selected operation: {result['operation']}")
        print(f"Result: {result['result']} (entropy: {result['entropy']})")
        if 'explanation' in result:
            print(f"Explanation: {result['explanation']}")
    except Exception as e:
        print(f"Error in auto-operation: {e}")
        time.sleep(0.5)
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 3: TFID anchoring and identity
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 3: TFID Identity Fingerprinting  ")
    print("=" * 80)
    
    print("\nThe TFID (Temporal Fingerprint Identity) system allows for")
    print("expressions to maintain a unique identity fingerprint.")
    
    expressions = [
        "UML",
        "Recursive Compression",
        "3.14159265358979"
    ]
    
    for expr in expressions:
        print(f"\nExpression: {expr}")
        identity = tfid_anchor(expr)
        print(f"TFID fingerprint: {identity}")
        time.sleep(0.5)
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 4: Recursive Compression
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 4: Recursive Compression  ")
    print("=" * 80)
    
    print("\nRecursive compression reduces complex expressions to simpler forms")
    print("while preserving mathematical relationships and fingerprint identity.")
    
    values = [
        123.456789,
        3.14159265358979,
        0.33333333333
    ]
    
    for value in values:
        print(f"\nOriginal value: {value}")
        compressed = recursive_compress(value)
        print(f"Compressed value: {compressed}")
        time.sleep(0.5)
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 5: Magic Squares
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 5: Magic Squares Validation  ")
    print("=" * 80)
    
    print("\nUML Calculator can validate magic squares and higher-dimensional")
    print("mathematical structures using its core principles.")
    
    # Standard 3×3 magic square
    magic_square = [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ]
    
    # Non-magic square
    non_magic = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("\nValidating a classic 3×3 magic square:")
    for row in magic_square:
        print(row)
    result = validate_magic_square(magic_square)
    print(f"Is magic square: {result[0]}, Magic sum: {result[1]}")
    
    print("\nValidating a non-magic 3×3 square:")
    for row in non_magic:
        print(row)
    result = validate_magic_square(non_magic)
    print(f"Is magic square: {result[0]}")
    
    print("\n" + "=" * 80)
    print("  UML CALCULATOR BASIC FEATURE DEMONSTRATION COMPLETE  ")
    print("=" * 80)
    print("\nThank you for exploring the UML Calculator features.")

if __name__ == "__main__":
    feature_demo()

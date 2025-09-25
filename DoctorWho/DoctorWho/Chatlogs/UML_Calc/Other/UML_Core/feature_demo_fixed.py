"""
UML Calculator Feature Demonstration

This module demonstrates the core features of the UML Calculator, including:
1. Basic UML syntax and operations
2. RIS meta-operator with explicit operations
3. Symbolic identity and fingerprinting
4. Recursive compression
5. Magic squares and tesseract projections
6. T.R.E.E.S principles in action

Run this script to see interactive demonstrations of key UML features.
"""

import sys
import os
from datetime import datetime
import time

# Import UML core modules using relative imports
try:
    # Direct import when running from UML_Core
    from uml_core import (
        parse_uml, eval_uml, recursive_compress,
        ris_meta_operator, tfid_anchor, superposition_collapse
    )
    from magic_dimension import validate_magic_square
    from safe_eval import safe_eval
    from symbolic_extensions import demo_symbolic_extensions
except ImportError:
    # Fallback for different directory structures
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from uml_core import (
        parse_uml, eval_uml, recursive_compress,
        ris_meta_operator, tfid_anchor, superposition_collapse
    )
    from magic_dimension import validate_magic_square
    from safe_eval import safe_eval
    from symbolic_extensions import demo_symbolic_extensions


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def feature_demo():
    """Run interactive demonstration of UML Calculator features."""
    
    clear_screen()
    print("\n" + "=" * 80)
    print("  UNIVERSAL MATHEMATICAL LANGUAGE (UML) CALCULATOR - FEATURE DEMONSTRATION  ")
    print("=" * 80)
    print("\nThis demonstration will showcase the key features of the UML Calculator,")
    print("highlighting the T.R.E.E.S. principles in operation.")
    print("\nPress Enter to continue through each demonstration.")
    input("\nPress Enter to begin...")

    # Demo 1: Basic UML syntax and operations
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 1: Basic UML Syntax and Operations  ")
    print("=" * 80)
    
    expressions = [
        "3#5",            # Basic hash operation
        "3#(5#7)",        # Nested hash operations
        "a#b",            # Symbolic hash operation
        "(2+3i)#(4-2i)",  # Complex number hash operation
        "ℝ#ℂ",            # Mathematical set hash operation
    ]
    
    print("\nThe UML Calculator uses the # symbol as its primary operator.")
    print("The parser evaluates the expressions based on context and entropy.")
    
    for expr in expressions:
        print(f"\nExpression: {expr}")
        result = parse_uml(expr)
        print(f"Parsed result: {result}")
        try:
            eval_result = eval_uml(expr)
            print(f"Evaluated result: {eval_result}")
        except Exception as e:
            print(f"Evaluation error: {e}")
        time.sleep(0.5)
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 2: RIS meta-operator demonstration
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 2: RIS Meta-Operator with Explicit Operations  ")
    print("=" * 80)
    
    print("\nThe RIS (Recursive Integration System) meta-operator allows for parallel")
    print("computation of multiple operations, collapsing to the most appropriate result.")
    
    a, b = 5, 3
    operations = ['+', '-', '*', '/']
    
    print(f"\nDemonstrating RIS with a={a} and b={b}:")
    for op in operations:
        result = ris_meta_operator(a, b, op)
        print(f"\nOperation: {a} {op} {b}")
        print(f"Result: {result['result']} (entropy: {result['entropy']})")
        print(f"Superposition state: {result['superposition']}")
        time.sleep(0.5)
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 3: TFID anchoring and identity
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 3: Symbolic Identity and Fingerprinting with TFID  ")
    print("=" * 80)
    
    print("\nThe TFID (Temporal Fingerprint Identity) system allows for")
    print("symbolic expressions to maintain a unique identity fingerprint.")
    
    expressions = [
        "3#5",
        "(a+b)#(c*d)",
        "√2#π"
    ]
    
    for expr in expressions:
        print(f"\nExpression: {expr}")
        identity = tfid_anchor(expr)
        print(f"TFID fingerprint: {identity}")
        time.sleep(0.5)
    
    print("\nDemonstrating identity persistence across transformations:")
    expr = "(a+b)#(c*d)"
    transformed = expr.replace("a", "x").replace("b", "y")
    print(f"Original: {expr} → TFID: {tfid_anchor(expr)}")
    print(f"Transformed: {transformed} → TFID: {tfid_anchor(transformed)}")
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 4: Recursive Compression
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 4: Recursive Compression  ")
    print("=" * 80)
    
    print("\nRecursive compression reduces complex expressions to simpler forms")
    print("while preserving mathematical relationships and fingerprint identity.")
    
    expressions = [
        "123.456789",
        "3.14159265358979",
        "(5*4)/(2*10)"
    ]
    
    for expr in expressions:
        print(f"\nExpression: {expr}")
        try:
            value = float(safe_eval(expr))
            compressed = recursive_compress(value)
            print(f"Original value: {value}")
            print(f"Compressed value: {compressed}")
        except Exception as e:
            print(f"Compression error: {e}")
        time.sleep(0.5)
    
    input("\nPress Enter to continue to the next demonstration...")

    # Demo 5: Magic Squares and Tesseract projections
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 5: Magic Squares and Higher Dimensional Structures  ")
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
    
    input("\nPress Enter to continue to the final demonstration...")

    # Demo 6: T.R.E.E.S. principles in action
    clear_screen()
    print("\n" + "=" * 80)
    print("  DEMONSTRATION 6: T.R.E.E.S. Principles in Action  ")
    print("=" * 80)
    
    print("\nT.R.E.E.S. represents the core principles of the UML system:")
    print("  • Temporal recursion")
    print("  • Recursive compression")
    print("  • Entropic evaluation")
    print("  • Emergent symbolism")
    print("  • Superposition collapse")
    
    print("\nDemonstrating symbolic extensions with T.R.E.E.S. principles:")
    demo_symbolic_extensions()
    
    print("\n" + "=" * 80)
    print("  UML CALCULATOR FEATURE DEMONSTRATION COMPLETE  ")
    print("=" * 80)
    print("\nThank you for exploring the UML Calculator features.")


if __name__ == "__main__":
    feature_demo()

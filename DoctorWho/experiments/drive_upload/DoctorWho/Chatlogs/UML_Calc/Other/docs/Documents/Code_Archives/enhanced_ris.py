"""
Enhanced RIS Meta-Operator for UML

This module enhances the RIS meta-operator to support exponentiation and other 
advanced mathematical operations, specifically for testing the UML calculator.
"""

import sys
import os
import math

# Add the UML_Core directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'UML_Core')))
from uml_core import ris_meta_operator as original_ris

def enhanced_ris_meta_operator(a, b, operation=None):
    """
    Enhanced RIS meta-operator with support for specifying operations.
    
    Args:
        a (float): First operand
        b (float): Second operand
        operation (str, optional): Operation to perform ('add', 'sub', 'mul', 'div', 'pow', 'root', 'log')
        
    Returns:
        float: Result of the operation
    """
    if operation == 'pow':
        return a ** b, 'pow'
    elif operation == 'root':
        if a < 0 and b % 2 == 1:  # Handle negative numbers for odd roots
            return -(-a) ** (1/b), 'root'
        return a ** (1/b), 'root'
    elif operation == 'log':
        if a <= 0 or b <= 0:
            return float('nan'), 'log'
        return math.log(a, b), 'log'
    else:
        return original_ris(a, b)

def test_enhanced_ris():
    """Test the enhanced RIS meta-operator"""
    test_cases = [
        # a, b, operation, expected
        (2, 3, 'pow', 8),
        (4, 2, 'pow', 16),
        (8, 3, 'root', 2),
        (4, 2, 'root', 2),
        (100, 10, 'log', 2),
        (3, 4, None, 7),  # Default (addition)
    ]
    
    for a, b, op, expected in test_cases:
        result, operation = enhanced_ris_meta_operator(a, b, op)
        print(f"{a} {op if op else 'auto'} {b} = {result} (operation: {operation})")
        
        # Check if result matches expected
        if abs(result - expected) > 1e-10:
            print(f"  WARNING: Expected {expected}")

if __name__ == "__main__":
    test_enhanced_ris()

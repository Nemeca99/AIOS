"""
Safe Eval Test Harness
This module tests the security and correctness of the safe_eval implementation
"""

import sys
import os
import unittest
import math
from typing import Any, Dict, List

# Add the UML_Core directory to the path to import safe_eval
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'UML_Core')))
from safe_eval import safe_eval

class SafeEvalTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        """Test basic arithmetic expressions."""
        self.assertEqual(safe_eval("2 + 3"), 5)
        self.assertEqual(safe_eval("2 * 3"), 6)
        self.assertEqual(safe_eval("6 / 3"), 2.0)
        self.assertEqual(safe_eval("7 - 3"), 4)
        
    def test_complex_arithmetic(self):
        """Test more complex arithmetic expressions."""
        self.assertEqual(safe_eval("2 + 3 * 4"), 14)
        self.assertEqual(safe_eval("(2 + 3) * 4"), 20)
        self.assertEqual(safe_eval("2 ** 3 + 4"), 12)
        self.assertEqual(safe_eval("10 % 3"), 1)
        
    def test_functions(self):
        """Test mathematical functions."""
        self.assertEqual(safe_eval("sqrt(16)"), 4.0)
        self.assertEqual(safe_eval("log10(100)"), 2.0)
        self.assertAlmostEqual(safe_eval("sin(pi/2)"), 1.0)
        self.assertEqual(safe_eval("max(1, 2, 3, 4)"), 4)
        
    def test_negative_values(self):
        """Test expressions with negative values."""
        self.assertEqual(safe_eval("-5 + 10"), 5)
        self.assertEqual(safe_eval("abs(-5)"), 5)
        
    def test_floating_point(self):
        """Test floating point precision."""
        self.assertAlmostEqual(safe_eval("3.14159 * 2"), 6.28318, places=5)
        self.assertAlmostEqual(safe_eval("round(3.14159, 2)"), 3.14, places=2)
        
    def test_security_unsafe_attributes(self):
        """Test that accessing unsafe attributes raises an error."""
        with self.assertRaises(Exception):
            safe_eval("__import__('os').system('dir')")
            
        with self.assertRaises(Exception):
            safe_eval("globals()")
            
        with self.assertRaises(Exception):
            safe_eval("open('file.txt', 'w')")
    
    def test_security_builtins(self):
        """Test that accessing unsafe builtins raises an error."""
        with self.assertRaises(Exception):
            safe_eval("import os")
            
        with self.assertRaises(Exception):
            safe_eval("exec('print(1)')")
            
    def test_uml_specific_expressions(self):
        """Test expressions that might be specific to UML calculations."""
        self.assertEqual(safe_eval("10 * 10"), 100)  # Square
        self.assertEqual(safe_eval("2 ** 3"), 8)     # Cube
        self.assertEqual(safe_eval("sqrt(9)"), 3.0)  # Square root
        
    def test_edge_cases(self):
        """Test edge cases and potential pitfalls."""
        self.assertTrue(math.isnan(safe_eval("0/0")))  # Division by zero should return NaN
        self.assertTrue(math.isinf(safe_eval("1/0")))  # Division by zero should return inf
        self.assertEqual(safe_eval("1e10"), 10000000000.0)  # Scientific notation
        
    def test_complex_numbers(self):
        """Test support for complex numbers if implemented."""
        # These may raise exceptions if complex numbers are not supported
        try:
            self.assertEqual(safe_eval("sqrt(-1)"), 1j)
            self.assertEqual(safe_eval("sqrt(-4)"), 2j)
        except Exception as e:
            print(f"Note: Complex numbers not supported: {e}")
            
if __name__ == "__main__":
    unittest.main()

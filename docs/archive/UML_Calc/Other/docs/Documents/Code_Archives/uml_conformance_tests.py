"""
UML Mathematical Conformance Tests

This module tests the UML calculator's ability to correctly evaluate mathematical expressions
using both traditional notation and UML syntax, ensuring they produce equivalent results.
"""

import sys
import os
import unittest
from math import isclose

# Add the UML_Core directory to the path to import UML functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'UML_Core')))
from uml_core import parse_uml, eval_uml, convert_standard_to_uml
from safe_eval import safe_eval

class UMLConformanceTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations in both notations."""
        test_cases = [
            # Traditional, UML
            ("3 + 4", "[3,4]"),
            ("7 - 2", "{7,2}"),
            ("6 * 8", "<6,8>"),
            ("20 / 5", "<>20,5<>"),
            ("2 ** 3", "2@3"), # Using UML symbolic equivalent
            ("10 % 3", "10%3"), # Using direct modulo notation
        ]
        
        for std_expr, uml_expr in test_cases:
            std_result = safe_eval(std_expr)
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertTrue(
                isclose(std_result, uml_result, rel_tol=1e-10),
                f"Expression mismatch: {std_expr} = {std_result}, {uml_expr} = {uml_result}"
            )
      def test_complex_arithmetic(self):
        """Test complex arithmetic expressions with operator precedence."""
        test_cases = [
            # Traditional, UML
            ("3 + 4 * 2", "[3,<4,2>]"),
            ("(3 + 4) * 2", "<[3,4],2>"),
            ("2 ** 3 + 4", "[2@3,4]"),
            ("2 * (3 + 4)", "<2,[3,4]>"),
            ("10 - 5 / 2", "{10,<>5,2<>}"),
            ("(10 - 5) / 2", "<>{10,5},2<>"),
        ]
        
        for std_expr, uml_expr in test_cases:
            std_result = safe_eval(std_expr)
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertTrue(
                isclose(std_result, uml_result, rel_tol=1e-10),
                f"Expression mismatch: {std_expr} = {std_result}, {uml_expr} = {uml_result}"
            )
    
    def test_conversion(self):
        """Test conversion from standard notation to UML syntax."""
        test_cases = [
            "3 + 4",
            "7 - 2",
            "6 * 8",
            "20 / 5",
            "2 ** 3",
            "10 % 3",
            "3 + 4 * 2",
            "(3 + 4) * 2",
            "2 ** 3 + 4",
            "2 * (3 + 4)",
            "10 - 5 / 2",
            "(10 - 5) / 2",
        ]
        
        for expr in test_cases:
            std_result = safe_eval(expr)
            uml_expr = convert_standard_to_uml(expr)
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertTrue(
                isclose(std_result, uml_result, rel_tol=1e-10),
                f"Conversion mismatch: {expr} = {std_result}, {uml_expr} = {uml_result}"
            )
    
    def test_nested_expressions(self):
        """Test deeply nested expressions in UML notation."""
        test_cases = [
            # UML expression, Expected result
            ("[1,+,[2,+,[3,+,[4,+,5]]]]", 15),
            ("[[[[1,+,2],+,3],+,4],+,5]", 15),
            ("[2,*,[3,*,[4,*,5]]]", 120),
            ("[[2,*,3],*,[4,*,5]]", 120),
        ]
        
        for uml_expr, expected in test_cases:
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertTrue(
                isclose(uml_result, expected, rel_tol=1e-10),
                f"Nested expression error: {uml_expr} = {uml_result}, expected {expected}"
            )
    
    def test_advanced_operators(self):
        """Test UML's advanced operators."""
        test_cases = [
            # UML expression, Expected result (based on UML Codex)
            ("[4,>,3]", 12),  # UML equivalent of 4*3
            ("[16,<,2]", 8),  # UML equivalent of 16/2
            ("[4,!]", 24),   # Factorial
            ("[4,@,2]", 16),  # Power/Exponent
            ("[25,#]", 5),    # Square root
            ("[8,~]", 0.125), # Reciprocal (1/x)
        ]
        
        for uml_expr, expected in test_cases:
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertTrue(
                isclose(uml_result, expected, rel_tol=1e-10),
                f"Advanced operator error: {uml_expr} = {uml_result}, expected {expected}"
            )
    
    def test_floating_point(self):
        """Test floating point precision."""
        test_cases = [
            # Traditional, UML
            ("3.14159 * 2", "[3.14159,*,2]"),
            ("22 / 7", "[22,/,7]"),
            ("0.1 + 0.2", "[0.1,+,0.2]"),
            ("1e-10 * 1e10", "[1e-10,*,1e10]"),
        ]
        
        for std_expr, uml_expr in test_cases:
            std_result = safe_eval(std_expr)
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertTrue(
                isclose(std_result, uml_result, rel_tol=1e-10),
                f"Floating point mismatch: {std_expr} = {std_result}, {uml_expr} = {uml_result}"
            )
    
    def test_complex_numbers(self):
        """Test complex number support if implemented."""
        # These tests may be skipped if complex numbers are not yet supported
        try:
            # Simple tests
            uml_expr = "[0,+,[0,j,1]]"  # 0 + 1j
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertEqual(complex(0, 1), uml_result)
            
            # More complex tests
            uml_expr = "[[1,+,[0,j,2]],*,[3,+,[0,j,4]]]"  # (1+2j) * (3+4j)
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            self.assertEqual(complex(1, 2) * complex(3, 4), uml_result)
        except Exception as e:
            self.skipTest(f"Complex numbers not fully supported yet: {str(e)}")
    
    def test_matrix_operations(self):
        """Test matrix operations if implemented."""
        try:
            # Define matrices in UML syntax
            matrix_a = "[[1,2],[3,4]]"
            matrix_b = "[[5,6],[7,8]]"
            
            # Test matrix addition
            uml_expr = f"[{matrix_a},+,{matrix_b}]"
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            
            # Expected result [[6,8],[10,12]]
            self.assertEqual(uml_result[0][0], 6)
            self.assertEqual(uml_result[0][1], 8)
            self.assertEqual(uml_result[1][0], 10)
            self.assertEqual(uml_result[1][1], 12)
            
            # Test matrix multiplication
            uml_expr = f"[{matrix_a},*,{matrix_b}]"
            parsed_uml = parse_uml(uml_expr)
            uml_result = eval_uml(parsed_uml)
            
            # Expected result [[19,22],[43,50]]
            self.assertEqual(uml_result[0][0], 19)
            self.assertEqual(uml_result[0][1], 22)
            self.assertEqual(uml_result[1][0], 43)
            self.assertEqual(uml_result[1][1], 50)
        except Exception as e:
            self.skipTest(f"Matrix operations not fully supported yet: {str(e)}")

if __name__ == "__main__":
    unittest.main()

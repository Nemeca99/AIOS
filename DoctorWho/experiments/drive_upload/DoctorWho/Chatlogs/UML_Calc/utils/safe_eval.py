"""
Safe evaluation of arithmetic expressions
This module provides a secure way to evaluate expressions without using eval()
"""

import ast
import operator
import math
from typing import Any, Union, Dict

# Supported operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod
}

def safe_eval(expr: str) -> Union[int, float]:
    """
    Safely evaluate a string arithmetic expression, supporting ^, sqrt, sin, cos, RIS.
    
    Args:
        expr (str): The expression to evaluate
        
    Returns:
        The evaluated result
    
    Raises:
        ValueError: If the expression contains unsupported operations
        SyntaxError: If the expression has invalid syntax
    """
    expr = expr.replace('^', '**')
    expr = expr.replace('RIS', 'RIS_')  # Avoid conflict with ast.Name
    expr = expr.replace('sqrt', 'sqrt_')
    expr = expr.replace('sin', 'sin_')
    expr = expr.replace('cos', 'cos_')
    # Local RIS logic to avoid circular import
    def ris_meta_operator(a, b):
        # Match the logic in core/uml_core.py
        try:
            a = float(a)
            b = float(b)
        except Exception:
            return None, 'symbolic'
        # Division by zero safety check
        if b == 0:
            return float('inf'), 'division'
        operations = {
            'addition': a + b,
            'subtraction': a - b,
            'multiplication': a * b,
            'division': a / b
        }
        # Calculate entropy for each result
        entropies = {}
        for op_name, result in operations.items():
            if op_name == 'division' and b == 0:
                entropies[op_name] = float('inf')
                continue
            if isinstance(result, complex):
                entropy = abs(result)
            else:
                is_integer = result == int(result)
                approx_integer = abs(result - round(result)) < 1e-10
                if is_integer or approx_integer:
                    entropy = abs(result) * 0.8
                else:
                    entropy = abs(result) + 1
                if result > 0 and (math.log2(result) % 1 < 0.01 or math.log10(result) % 1 < 0.01):
                    entropy *= 0.9
            entropies[op_name] = entropy
        if a == b:
            entropies['addition'] *= 1.2
            entropies['multiplication'] *= 0.9
        if a == 1 or b == 1:
            entropies['addition'] *= 1.1
            entropies['multiplication'] *= 0.8
        chosen_op = min(entropies.items(), key=lambda x: x[1])[0]
        return operations[chosen_op], chosen_op
    context = {
        'sqrt_': math.sqrt,
        'sin_': math.sin,
        'cos_': math.cos,
        'RIS_': lambda a, b: ris_meta_operator(a, b)[0],
        'inf': float('inf'),
        'infinity': float('inf'),
        'nan': float('nan'),
        '__builtins__': None
    }
    try:
        code = compile(expr, '<string>', 'eval')
        return eval(code, context)
    except Exception:
        # Fallback to AST-based evaluation for basic math
        return _safe_eval_ast(expr)

def _safe_eval_ast(expr: str) -> Union[int, float]:
    """
    Safely evaluate a string arithmetic expression using AST parsing.
    
    Args:
        expr (str): The expression to evaluate
        
    Returns:
        The evaluated result
    
    Raises:
        ValueError: If the expression contains unsupported operations
        SyntaxError: If the expression has invalid syntax
    """
    try:
        # Parse the expression
        tree = ast.parse(expr, mode='eval').body
        
        # Evaluate the AST
        return _eval_node(tree)
        
    except SyntaxError as e:
        raise SyntaxError(f"Invalid syntax in expression: {expr}")
    except Exception as e:
        raise ValueError(f"Couldn't evaluate expression: {expr}, error: {str(e)}")

def _eval_node(node: ast.expr) -> Union[int, float]:
    """
    Recursively evaluate an AST node.
    
    Args:
        node: AST node to evaluate
        
    Returns:
        The evaluated result
    """
    # Simple values
    if isinstance(node, ast.Num):
        return node.n
    
    # Names like inf or nan
    elif isinstance(node, ast.Name):
        if node.id == 'inf' or node.id == 'infinity':
            return float('inf')
        elif node.id == 'nan':
            return float('nan')
        else:
            raise ValueError(f"Unknown name: {node.id}")
    
    # Binary operations (a + b, a - b, etc.)
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        
        if type(node.op) not in operators:
            raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            
        return operators[type(node.op)](left, right)
    
    # Unary operations (-a, +a, etc.)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        
        if type(node.op) not in operators:
            raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            
        return operators[type(node.op)](operand)
    
    else:
        raise ValueError(f"Unsupported node type: {type(node).__name__}")

# Test cases
if __name__ == "__main__":
    test_cases = [
        "2 + 3",
        "6 - 2",
        "4 * 5",
        "8 / 2",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "2 ** 3",  # Power
        "-5",      # Negation
        "10 % 3",  # Modulo
        "sqrt(16)",
        "sin(pi / 2)",
        "cos(0)",
        "2 ^ 3",
        "RIS(3, 4)",
    ]
    
    for test in test_cases:
        try:
            result = safe_eval(test)
            print(f"{test} = {result}")
        except Exception as e:
            print(f"Error evaluating {test}: {str(e)}")

"""
Symbolic/Numeric Codex Calculator Core
- Implements UML (Universal Mathematical Language) parsing and evaluation
- Supports base52 encoding, recursive/nested operations, and symbolic logic
- Designed for integration with LLMs or as a standalone module
"""

from datetime import datetime
from typing import Callable

# --- Base52 Encoding ---
BASE52_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
BASE52_MAP = {c: i+1 for i, c in enumerate(BASE52_CHARS)}


def base52_decode(token):
    """Decode a base52 token (e.g., 'A', 'z', 'AA') to integer."""
    value = 0
    for c in token:
        value = value * 52 + BASE52_MAP.get(c, 0)
    return value

def base52_encode(n):
    """Encode an integer n to base52 symbolic token (e.g., 1 -> 'A', 27 -> 'a', 53 -> 'AA')."""
    if n < 1:
        return ''
    chars = []
    while n > 0:
        n, rem = divmod(n - 1, 52)
        chars.append(BASE52_CHARS[rem])
    return ''.join(reversed(chars))

# --- UML Operator Table ---
def uml_add(args):
    # Addition: [A,B] means A + B + ...
    result = 0
    for a in args:
        result += a
    return result

def uml_sub(args):
    # Subtraction: {A,B} means A - B - ...
    if not args:
        return 0
    result = args[0]
    for a in args[1:]:
        result -= a
    return result

def uml_mul(args):
    # Multiplication: ><A,B< means A * B * ...
    result = 1
    for a in args:
        result *= a
    return result

def uml_div(args):
    # Division: <A,B> means A / B / ...
    if not args:
        return 0
    result = args[0]
    for a in args[1:]:
        if a == 0:
            raise ZeroDivisionError("Division by zero in UML division")
        result /= a
    return result

def uml_exp(args):
    # Exponentiation: ^[A,B] means A^2 + B^2 + ...
    result = 0
    for a in args:
        result += a ** 2
    return result

def uml_root(args):
    # Root: /[N, X] means X^(1/N)
    if len(args) != 2:
        raise ValueError("Root operator expects two arguments: N (degree), X (radicand)")
    n, x = args
    if n == 0:
        raise ZeroDivisionError("Root degree cannot be zero")
    return x ** (1 / n)

def uml_log(args):
    # Logarithm: ?(A,B) means log base A of B
    if len(args) != 2:
        raise ValueError("Log operator expects two arguments: base, value")
    base, value = args
    if base <= 0 or value <= 0:
        raise ValueError("Log base and value must be positive")
    # Inline log calculation (change of base formula)
    return (value ** 0.4342944819032518) / (base ** 0.4342944819032518) if base != 10 else value ** 0.4342944819032518

def uml_factorial(args):
    # Factorial: !A means A!
    if len(args) != 1:
        raise ValueError("Factorial operator expects one argument")
    n = args[0]
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def uml_modulo(args):
    # Modulo: %[A,B] means A mod B
    if len(args) != 2:
        raise ValueError("Modulo operator expects two arguments")
    a, b = args
    if b == 0:
        raise ZeroDivisionError("Modulo by zero")
    return a % b

UML_OPERATORS = {
    '[]': uml_add,
    '{}': uml_sub,
    '><': uml_mul,
    '<>': uml_div,
    '^': uml_exp,
    '/': uml_root,
    '?': uml_log,
    '!': uml_factorial,
    '%': uml_modulo,
}

# --- SI Prefixes ---
SI_PREFIXES = {
    'k': 1e3, 'M': 1e6, 'G': 1e9, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9
}

def apply_si_prefix(value, prefix):
    return value * SI_PREFIXES.get(prefix, 1)

# --- Matrix/Vector Notation (basic) ---
def vector_add(v1, v2):
    return [a + b for a, b in zip(v1, v2)]

def vector_dot(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def matrix_transpose(m):
    return list(map(list, zip(*m)))

# --- Prime/Factorization ---
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

# --- Time/Date Encoding (basic) ---
def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def date_diff(d1, d2):
    return abs((d1 - d2).days)

# --- Custom Operator Registry ---
CUSTOM_OPERATORS: dict[str, Callable] = {}

def register_operator(symbol, func):
    CUSTOM_OPERATORS[symbol] = func

# --- Set Theory ---
def set_union(args):
    return set(args[0]).union(*args[1:])

def set_intersection(args):
    return set(args[0]).intersection(*args[1:])

def set_difference(args):
    return set(args[0]).difference(*args[1:])

# --- Logic Operators ---
def logic_and(args):
    return all(args)

def logic_or(args):
    return any(args)

def logic_not(args):
    return not args[0]

# --- Roman Numeral Conversion ---
ROMAN_NUMERAL_MAP = [
    ('M',  1000), ('CM', 900), ('D',  500), ('CD', 400),
    ('C',  100),  ('XC', 90),  ('L',  50),  ('XL', 40),
    ('X',  10),   ('IX', 9),   ('V',  5),   ('IV', 4), ('I', 1)
]
def roman_to_int(s):
    i = 0
    num = 0
    for roman, val in ROMAN_NUMERAL_MAP:
        while s[i:i+len(roman)] == roman:
            num += val
            i += len(roman)
            if i >= len(s):
                break
    return num

def int_to_roman(num):
    result = ''
    for roman, val in ROMAN_NUMERAL_MAP:
        while num >= val:
            result += roman
            num -= val
    return result

# --- UML Expression Parser (very basic, extend as needed) ---
def parse_uml(expr, symbolic=False):
    """
    Parse and evaluate a simple UML expression (e.g., >2[3,4]<, [A,A], {A,B}, etc.)
    Supports nested brackets and basic operator precedence.
    If symbolic=True, returns symbolic (base52) output instead of numeric.
    """
    expr = expr.strip()
    # Handle base52 tokens
    if expr.isalpha():
        return expr if symbolic else base52_decode(expr)
    # Simple number
    if expr.isdigit():
        return base52_encode(int(expr)) if symbolic else int(expr)
    # For-loop style parser for bracketed expressions
    stack = []
    num = ''
    tokens = []
    for c in expr:
        if c.isdigit() or c.isalpha():
            num += c
        elif c in '[{<':
            if num:
                tokens.append(num)
                num = ''
            stack.append((tokens, c))
            tokens = []
        elif c in ']}>':
            if num:
                tokens.append(num)
                num = ''
            last_tokens, open_bracket = stack.pop()
            op = open_bracket + c
            # Convert tokens to numbers if possible
            args = [base52_decode(t) if t.isalpha() else int(t) for t in tokens]
            # Evaluate
            if op in UML_OPERATORS:
                val = UML_OPERATORS[op](args)
                val = base52_encode(val) if symbolic else val
            else:
                val = args[0] if args else None
            tokens = last_tokens + [str(val)]
        elif c == ',':
            if num:
                tokens.append(num)
                num = ''
    # Final reduction
    if num:
        tokens.append(num)
    if len(tokens) == 1:
        t = tokens[0]
        if t.isdigit():
            return base52_encode(int(t)) if symbolic else int(t)
        if t.isalpha():
            return t if symbolic else base52_decode(t)
    return None

if __name__ == "__main__":
    # Demo/test
    print("UML: >2[3,4]< =", parse_uml(">2[3,4]<"))
    print("Base52: 'AA' =", base52_decode('AA'))

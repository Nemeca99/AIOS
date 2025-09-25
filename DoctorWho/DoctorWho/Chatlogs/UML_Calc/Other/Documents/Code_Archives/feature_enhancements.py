"""
UML Calculator Feature Enhancements
Additional features to enhance the UML Calculator functionality
"""

from typing import Dict, List, Any, Optional, Callable


# --- Roman Numeral Support ---

def roman_to_int(roman: str) -> int:
    """Convert a Roman numeral to an integer."""
    if not roman:
        return 0
        
    # Map of Roman numeral symbols to values
    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 
        'C': 100, 'D': 500, 'M': 1000
    }
    
    # Validate input
    roman = roman.upper()
    if not all(ch in roman_map for ch in roman):
        raise ValueError(f"Invalid Roman numeral: {roman}")
    
    # Convert
    result = 0
    prev_value = 0
    
    # Read from right to left
    for char in reversed(roman):
        value = roman_map[char]
        # If smaller value precedes larger, subtract it
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    
    return result


def int_to_roman(num: int) -> str:
    """Convert an integer to a Roman numeral."""
    if not isinstance(num, int) or num < 1 or num > 3999:
        raise ValueError("Input must be an integer between 1 and 3999")
    
    # Define Roman numeral mappings
    val_map = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    
    result = ""
    for value, numeral in val_map:
        while num >= value:
            result += numeral
            num -= value
            
    return result


# --- Logic Operators ---

def logic_and(args: List[Any]) -> int:
    """Logical AND operation on a list of arguments, truthy values converted to 1/0."""
    if not args:
        return 0
    return 1 if all(bool(arg) for arg in args) else 0


def logic_or(args: List[Any]) -> int:
    """Logical OR operation on a list of arguments, truthy values converted to 1/0."""
    if not args:
        return 0
    return 1 if any(bool(arg) for arg in args) else 0


def logic_not(args: List[Any]) -> int:
    """Logical NOT operation on a single argument, truthy values converted to 1/0."""
    if len(args) != 1:
        raise ValueError("NOT operator expects exactly one argument")
    return 0 if bool(args[0]) else 1


def logic_xor(args: List[Any]) -> int:
    """Logical XOR operation on a list of arguments, truthy values converted to 1/0."""
    if not args:
        return 0
    # Count truthy values
    true_count = sum(1 for arg in args if bool(arg))
    # XOR is true when odd number of inputs are true
    return 1 if true_count % 2 == 1 else 0


# --- Set Theory Operations ---

def set_union(sets: List[List[Any]]) -> List[Any]:
    """Compute the union of multiple sets."""
    if not sets:
        return []
    result = set()
    for s in sets:
        result.update(s)
    return list(result)


def set_intersection(sets: List[List[Any]]) -> List[Any]:
    """Compute the intersection of multiple sets."""
    if not sets:
        return []
    result = set(sets[0])
    for s in sets[1:]:
        result.intersection_update(s)
    return list(result)


def set_difference(sets: List[List[Any]]) -> List[Any]:
    """Compute the difference of two sets (A - B - C ...)."""
    if not sets:
        return []
    if len(sets) == 1:
        return sets[0]
    result = set(sets[0])
    for s in sets[1:]:
        result.difference_update(s)
    return list(result)


def set_symmetric_difference(sets: List[List[Any]]) -> List[Any]:
    """Compute the symmetric difference of multiple sets."""
    if not sets:
        return []
    result = set(sets[0])
    for s in sets[1:]:
        result = result.symmetric_difference(s)
    return list(result)


# --- Date Operations ---

def parse_date(date_str: str) -> tuple:
    """Parse a date in YYYY-MM-DD format into a tuple (year, month, day)."""
    import re
    match = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_str)
    if not match:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")
    
    year, month, day = map(int, match.groups())
    
    # Validate date components
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {month}")
    if not 1 <= day <= 31:
        raise ValueError(f"Invalid day: {day}")
        
    return (year, month, day)


def date_difference(date1: str, date2: str) -> int:
    """Calculate the difference in days between two dates."""
    from datetime import date
    
    y1, m1, d1 = parse_date(date1)
    y2, m2, d2 = parse_date(date2)
    
    date1_obj = date(y1, m1, d1)
    date2_obj = date(y2, m2, d2)
    
    delta = date2_obj - date1_obj
    return delta.days


def date_add(date_str: str, days: int) -> str:
    """Add a number of days to a date."""
    from datetime import date, timedelta
    
    y, m, d = parse_date(date_str)
    date_obj = date(y, m, d)
    
    new_date = date_obj + timedelta(days=days)
    return new_date.strftime("%Y-%m-%d")


# --- Custom Operator Registry ---

CUSTOM_OPERATORS: Dict[str, Callable] = {}

def register_custom_operator(name: str, function: Callable) -> None:
    """Register a custom operator function for use in the calculator."""
    global CUSTOM_OPERATORS
    CUSTOM_OPERATORS[name] = function


def get_custom_operator(name: str) -> Optional[Callable]:
    """Get a registered custom operator function by name."""
    return CUSTOM_OPERATORS.get(name)


def remove_custom_operator(name: str) -> bool:
    """Remove a custom operator from the registry."""
    global CUSTOM_OPERATORS
    if name in CUSTOM_OPERATORS:
        del CUSTOM_OPERATORS[name]
        return True
    return False


def list_custom_operators() -> List[str]:
    """List all registered custom operators."""
    return list(CUSTOM_OPERATORS.keys())


# --- Demo Functions ---

def demo_roman_numerals() -> None:
    """Demonstrate Roman numeral conversion."""
    examples = ["I", "IV", "IX", "XXIX", "MCMXCIX", "MMMDCCCLXXXVIII"]
    print("=== Roman Numeral Conversion ===")
    print("Roman → Integer:")
    for roman in examples:
        num = roman_to_int(roman)
        print(f"  {roman} → {num}")
    
    print("\nInteger → Roman:")
    for num in [1, 4, 9, 29, 1999, 3888]:
        roman = int_to_roman(num)
        print(f"  {num} → {roman}")


def demo_logic_operations() -> None:
    """Demonstrate logic operations."""
    print("=== Logic Operations ===")
    print("AND: [0,0]=0, [0,1]=0, [1,1]=1")
    print(f"  [0,0] → {logic_and([0,0])}")
    print(f"  [0,1] → {logic_and([0,1])}")
    print(f"  [1,1] → {logic_and([1,1])}")
    
    print("\nOR: [0,0]=0, [0,1]=1, [1,1]=1")
    print(f"  [0,0] → {logic_or([0,0])}")
    print(f"  [0,1] → {logic_or([0,1])}")
    print(f"  [1,1] → {logic_or([1,1])}")
    
    print("\nNOT: [0]=1, [1]=0")
    print(f"  [0] → {logic_not([0])}")
    print(f"  [1] → {logic_not([1])}")
    
    print("\nXOR: [0,0]=0, [0,1]=1, [1,1]=0, [1,1,1]=1")
    print(f"  [0,0] → {logic_xor([0,0])}")
    print(f"  [0,1] → {logic_xor([0,1])}")
    print(f"  [1,1] → {logic_xor([1,1])}")
    print(f"  [1,1,1] → {logic_xor([1,1,1])}")


def demo_set_operations() -> None:
    """Demonstrate set operations."""
    a = [1, 2, 3, 4]
    b = [3, 4, 5, 6]
    c = [4, 5, 6, 7]
    
    print("=== Set Operations ===")
    print(f"Sets: A={a}, B={b}, C={c}")
    
    union = set_union([a, b, c])
    print(f"Union (A ∪ B ∪ C): {union}")
    
    intersection = set_intersection([a, b, c])
    print(f"Intersection (A ∩ B ∩ C): {intersection}")
    
    diff_ab = set_difference([a, b])
    print(f"Difference (A - B): {diff_ab}")
    
    sym_diff_ab = set_symmetric_difference([a, b])
    print(f"Symmetric Difference (A △ B): {sym_diff_ab}")


def demo_date_operations() -> None:
    """Demonstrate date operations."""
    try:
        print("=== Date Operations ===")
        
        date1 = "2023-01-15"
        date2 = "2023-05-20"
        diff = date_difference(date1, date2)
        print(f"Difference between {date1} and {date2}: {diff} days")
        
        date3 = "2023-12-31"
        days_to_add = 45
        result = date_add(date3, days_to_add)
        print(f"Adding {days_to_add} days to {date3}: {result}")
        
    except ValueError as e:
        print(f"Error: {e}")


def demo_custom_operators() -> None:
    """Demonstrate custom operator registry."""
    # Define a custom power operator
    def custom_power(args):
        if len(args) != 2:
            return None
        base, exp = args
        return pow(base, exp)
    
    # Register and use the custom operator
    register_custom_operator("pow", custom_power)
    
    print("=== Custom Operator Registry ===")
    print("Registered operator 'pow(base, exp)'")
    
    base, exp = 2, 8
    result = get_custom_operator("pow")([base, exp])
    print(f"pow({base}, {exp}) = {result}")
    
    # List all operators
    ops = list_custom_operators()
    print(f"Available custom operators: {ops}")
    
    # Remove the operator
    removed = remove_custom_operator("pow")
    print(f"Removed 'pow' operator: {removed}")
    
    # List after removal
    ops = list_custom_operators()
    print(f"Available custom operators after removal: {ops}")


if __name__ == "__main__":
    # Run demos when script is executed directly
    demo_roman_numerals()
    print("\n")
    demo_logic_operations()
    print("\n")
    demo_set_operations()
    print("\n")
    demo_date_operations()
    print("\n")
    demo_custom_operators()

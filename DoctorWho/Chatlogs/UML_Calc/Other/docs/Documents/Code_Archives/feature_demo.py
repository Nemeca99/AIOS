"""
UML Calculator Feature Enhancements Demo
This is a demonstration script showing the Roman Numeral conversion
and Logic Operations enhancements
"""

# Import standard libraries
import sys

# Define Roman Numeral functions
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

# Logic Operations
def logic_and(args):
    """Logical AND operation."""
    return 1 if all(bool(arg) for arg in args) else 0

def logic_or(args):
    """Logical OR operation."""
    return 1 if any(bool(arg) for arg in args) else 0

def logic_not(args):
    """Logical NOT operation."""
    if len(args) != 1:
        raise ValueError("NOT requires exactly one argument")
    return 0 if bool(args[0]) else 1

def logic_xor(args):
    """Logical XOR operation."""
    return 1 if sum(1 for arg in args if bool(arg)) % 2 == 1 else 0

# Main demo function
def demo():
    """Run demo for Roman numerals and logic operations."""
    print("=== UML Calculator Enhancements Demo ===\n")
    
    # Roman Numeral examples
    print("== Roman Numeral Examples ==")
    roman_examples = ["I", "IV", "IX", "MCMXCIX"]
    for roman in roman_examples:
        num = roman_to_int(roman)
        print(f"{roman} → {num}")
    
    num_examples = [1, 4, 9, 1999]
    for num in num_examples:
        roman = int_to_roman(num)
        print(f"{num} → {roman}")
    
    print("\n== Logic Operation Examples ==")
    print("AND[0,0] = ", logic_and([0, 0]))
    print("AND[0,1] = ", logic_and([0, 1]))
    print("AND[1,1] = ", logic_and([1, 1]))
    print("OR[0,0] = ", logic_or([0, 0]))
    print("OR[0,1] = ", logic_or([0, 1]))
    print("NOT[0] = ", logic_not([0]))
    print("NOT[1] = ", logic_not([1]))
    print("XOR[0,1] = ", logic_xor([0, 1]))
    print("XOR[1,1] = ", logic_xor([1, 1]))
    print("XOR[1,0,1] = ", logic_xor([1, 0, 1]))
    
    print("\n== Command Line Usage ==")
    print("1. Roman Numeral conversion: R[2023] or R[MMXXIII]")
    print("2. Logic operations: AND[1,0,1], OR[0,1], NOT[1], XOR[1,0,1]")

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        # Check for Roman numeral conversion
        if cmd.startswith("R[") and cmd.endswith("]"):
            content = cmd[2:-1]
            if content.isdigit():
                # Convert to Roman
                try:
                    num = int(content)
                    result = int_to_roman(num)
                    print(f"{num} in Roman: {result}")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                # Convert from Roman
                try:
                    num = roman_to_int(content)
                    print(f"Roman {content} in decimal: {num}")
                except ValueError as e:
                    print(f"Error: {e}")
        
        # Check for logic operations
        elif cmd.startswith("AND[") and cmd.endswith("]"):
            content = cmd[4:-1]
            try:
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_and(values)
                print(f"AND{values} = {result}")
            except Exception as e:
                print(f"Error: {e}")
                
        elif cmd.startswith("OR[") and cmd.endswith("]"):
            content = cmd[3:-1]
            try:
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_or(values)
                print(f"OR{values} = {result}")
            except Exception as e:
                print(f"Error: {e}")
                
        elif cmd.startswith("NOT[") and cmd.endswith("]"):
            content = cmd[4:-1]
            try:
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_not(values)
                print(f"NOT{values} = {result}")
            except Exception as e:
                print(f"Error: {e}")
                
        elif cmd.startswith("XOR[") and cmd.endswith("]"):
            content = cmd[4:-1]
            try:
                values = [int(x.strip()) for x in content.split(',')]
                result = logic_xor(values)
                print(f"XOR{values} = {result}")
            except Exception as e:
                print(f"Error: {e}")
                
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python feature_demo.py [R[2023] | AND[1,0] | OR[0,1] | NOT[1] | XOR[1,0,1]]")
            print("Or run without arguments for a full demo.")
    else:
        demo()

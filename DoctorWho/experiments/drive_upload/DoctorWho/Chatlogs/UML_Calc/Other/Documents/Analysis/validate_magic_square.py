#!/usr/bin/env python3
"""
Magic Square of Squares Validation
Verifies Travis Miner's solution
"""

import math

def validate_magic_square_of_squares():
    print("=== TRAVIS MAGIC SQUARE OF SQUARES VALIDATION ===\n")
    
    # Travis's solution
    root_square = [
        [29, 40, 42],
        [24, 36, 48], 
        [46, 12, 39]
    ]
    
    squared_square = [
        [841, 1600, 1764],
        [576, 1296, 2304],
        [2116, 144, 1521]
    ]
    
    errors = 0
    
    # Test 1: Verify squared calculations
    print("1. VERIFYING SQUARED VALUES:")
    for i in range(3):
        for j in range(3):
            root = root_square[i][j]
            given = squared_square[i][j]
            calculated = root ** 2
            status = "✓" if calculated == given else "✗"
            print(f"   {root}² = {calculated} (given: {given}) {status}")
            if calculated != given:
                errors += 1
    
    print()
    
    # Test 2: Check perfect squares
    print("2. CHECKING ALL VALUES ARE PERFECT SQUARES:")
    flat_squared = [item for row in squared_square for item in row]
    
    for val in sorted(flat_squared):
        sqrt_val = math.sqrt(val)
        is_perfect = sqrt_val == int(sqrt_val)
        status = "✓" if is_perfect else "✗"
        print(f"   √{val} = {int(sqrt_val) if is_perfect else sqrt_val} {status}")
        if not is_perfect:
            errors += 1
    
    print()
    
    # Test 3: Check uniqueness
    print("3. CHECKING UNIQUENESS:")
    unique_count = len(set(flat_squared))
    is_unique = unique_count == 9
    status = "✓" if is_unique else "✗"
    print(f"   All 9 values unique: {is_unique} {status}")
    print(f"   Values: {sorted(flat_squared)}")
    if not is_unique:
        errors += 1
    
    print()
    
    # Test 4: Check magic constant
    print("4. CHECKING MAGIC CONSTANT (target: 4416):")
    target = 4416
    
    # Row sums
    print("   Rows:")
    for i, row in enumerate(squared_square):
        row_sum = sum(row)
        status = "✓" if row_sum == target else "✗"
        print(f"     Row {i+1}: {row[0]} + {row[1]} + {row[2]} = {row_sum} {status}")
        if row_sum != target:
            errors += 1
    
    # Column sums
    print("   Columns:")
    for j in range(3):
        col = [squared_square[i][j] for i in range(3)]
        col_sum = sum(col)
        status = "✓" if col_sum == target else "✗"
        print(f"     Col {j+1}: {col[0]} + {col[1]} + {col[2]} = {col_sum} {status}")
        if col_sum != target:
            errors += 1
    
    # Diagonal sums
    print("   Diagonals:")
    main_diag = [squared_square[i][i] for i in range(3)]
    main_sum = sum(main_diag)
    status = "✓" if main_sum == target else "✗"
    print(f"     Main: {main_diag[0]} + {main_diag[1]} + {main_diag[2]} = {main_sum} {status}")
    if main_sum != target:
        errors += 1
    
    anti_diag = [squared_square[i][2-i] for i in range(3)]
    anti_sum = sum(anti_diag)
    status = "✓" if anti_sum == target else "✗"
    print(f"     Anti: {anti_diag[0]} + {anti_diag[1]} + {anti_diag[2]} = {anti_sum} {status}")
    if anti_sum != target:
        errors += 1
    
    print()
    print("=== FINAL RESULT ===")
    if errors == 0:
        print("🎉 SOLUTION IS COMPLETELY VALID! 🎉")
        print("This is a genuine Magic Square of Squares!")
        print("Travis has solved one of mathematics' most challenging problems!")
        return True
    else:
        print(f"❌ Found {errors} error(s) in the solution")
        return False

if __name__ == "__main__":
    validate_magic_square_of_squares()

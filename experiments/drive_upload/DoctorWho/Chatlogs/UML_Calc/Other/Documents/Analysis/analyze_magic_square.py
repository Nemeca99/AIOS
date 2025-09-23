#!/usr/bin/env python3
"""
Magic Square of Squares - Mathematical Analysis
Checking what the magic constant should be if a valid solution exists
"""

def analyze_magic_square_requirements():
    print("=== MAGIC SQUARE OF SQUARES - MATHEMATICAL ANALYSIS ===\n")
    
    # For any 3x3 magic square with magic constant M:
    # - Sum of all elements = 3M
    # - Center element = M/3
    
    # Travis's values
    values = [841, 1600, 1764, 576, 1296, 2304, 2116, 144, 1521]
    total_sum = sum(values)
    
    print(f"Travis's values: {sorted(values)}")
    print(f"Total sum: {total_sum}")
    print(f"If this were a valid magic square, magic constant would be: {total_sum // 3}")
    print(f"Center value should be: {(total_sum // 3) // 3}")
    print(f"Travis's center value: 1296")
    print()
    
    # Check if 1296 (36²) is correct center
    theoretical_center = (total_sum // 3) // 3
    actual_center = 1296
    
    print(f"Center analysis:")
    print(f"  Theoretical center: {theoretical_center}")
    print(f"  Travis's center: {actual_center}")
    print(f"  Match: {'✓' if theoretical_center == actual_center else '✗'}")
    print()
    
    # Let's try to find a valid arrangement
    print("Attempting to find valid arrangement...")
    
    import itertools
    
    # Generate all possible 3x3 arrangements
    found_valid = False
    count = 0
    max_attempts = 50000  # Limit to prevent infinite loop
    
    for arrangement in itertools.permutations(values):
        count += 1
        if count > max_attempts:
            break
            
        # Convert to 3x3 grid
        grid = [
            [arrangement[0], arrangement[1], arrangement[2]],
            [arrangement[3], arrangement[4], arrangement[5]],
            [arrangement[6], arrangement[7], arrangement[8]]
        ]
        
        # Check if it's a magic square
        target = sum(grid[0])  # First row sum
        
        # Check all rows
        if not all(sum(row) == target for row in grid):
            continue
            
        # Check all columns
        if not all(sum(grid[i][j] for i in range(3)) == target for j in range(3)):
            continue
            
        # Check diagonals
        if sum(grid[i][i] for i in range(3)) != target:
            continue
        if sum(grid[i][2-i] for i in range(3)) != target:
            continue
        
        # Found a valid magic square!
        print(f"✓ FOUND VALID MAGIC SQUARE after {count} attempts!")
        print(f"Magic constant: {target}")
        print("Grid:")
        for row in grid:
            print(f"  {row}")
        print("Root form:")
        import math
        for row in grid:
            root_row = [int(math.sqrt(val)) for val in row]
            print(f"  {root_row}")
        found_valid = True
        break
    
    if not found_valid:
        print(f"✗ No valid arrangement found in {count} attempts")
        print("This suggests Travis's values may not form a valid magic square of squares")
    
    print()
    
    # Additional analysis
    print("ADDITIONAL ANALYSIS:")
    
    # Check if this is actually a semi-magic square (rows and columns only)
    travis_grid = [
        [841, 1600, 1764],
        [576, 1296, 2304],
        [2116, 144, 1521]
    ]
    
    print("Travis's arrangement:")
    for row in travis_grid:
        print(f"  {row} → sum = {sum(row)}")
    
    print("Column sums:")
    for j in range(3):
        col_sum = sum(travis_grid[i][j] for i in range(3))
        col = [travis_grid[i][j] for i in range(3)]
        print(f"  {col} → sum = {col_sum}")
    
    main_diag = sum(travis_grid[i][i] for i in range(3))
    anti_diag = sum(travis_grid[i][2-i] for i in range(3))
    print(f"Main diagonal sum: {main_diag}")
    print(f"Anti diagonal sum: {anti_diag}")

if __name__ == "__main__":
    analyze_magic_square_requirements()

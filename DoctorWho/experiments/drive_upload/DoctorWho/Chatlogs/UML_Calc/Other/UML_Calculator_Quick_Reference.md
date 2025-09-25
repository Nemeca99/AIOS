# UML Calculator - Quick Reference Guide

## Calculation Modes

- **Standard Mode**: Traditional arithmetic (PEMDAS)
- **UML Mode**: Universal Mathematical Language notation
- **RIS Mode**: Recursive Integration System with meta-operators

## Standard Arithmetic

| Operation | Syntax | Example |
|-----------|--------|---------|
| Addition | `a + b` | `3 + 4 = 7` |
| Subtraction | `a - b` | `10 - 3 = 7` |
| Multiplication | `a * b` | `3 * 4 = 12` |
| Division | `a / b` | `12 / 4 = 3` |
| Exponentiation | `a ** b` | `2 ** 3 = 8` |
| Modulo | `a % b` | `10 % 3 = 1` |

## UML Notation

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| Addition | `[A,B]` | `[3,4]` | 7 |
| Subtraction | `{A,B}` | `{10,3}` | 7 |
| Multiplication | `>A,B<` | `>3,4<` | 12 |
| Division | `<A,B>` | `<12,4>` | 3 |
| Exponentiation | `^[A]` | `^[3]` | 9 |
| Root | `/[N,X]` | `/[2,9]` | 3 |
| Logarithm | `?(A,B)` | `?(10,100)` | 2 |
| Factorial | `!A` | `!5` | 120 |
| Modulo | `%[A,B]` | `%[10,3]` | 1 |

## RIS Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Meta-Operator | `@(a,b)` | Performs all basic operations and selects lowest entropy |
| Recursive Compression | (via demo) | Condenses repeated patterns |

## Number Theory Functions

| Function | Syntax | Example | Result |
|----------|--------|---------|--------|
| Fibonacci | `F[n]` | `F[10]` | 55 |
| Prime Check | `P[n]` | `P[17]` | 1 (prime) |
| GCD | `&[a,b]` | `&[12,18]` | 6 |
| LCM | `\|[a,b]` | `\|[4,6]` | 12 |

## Roman Numerals

| Function | Syntax | Example | Result |
|----------|--------|---------|--------|
| Decimal to Roman | `R[n]` | `R[2023]` | MMXXIII |
| Roman to Decimal | `R[roman]` | `R[MMXXIII]` | 2023 |

## Logic Operations

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| AND | `AND[a,b,...]` | `AND[1,0,1]` | 0 |
| OR | `OR[a,b,...]` | `OR[0,0,1]` | 1 |
| NOT | `NOT[a]` | `NOT[1]` | 0 |
| XOR | `XOR[a,b,...]` | `XOR[1,0,1]` | 0 |

## Set Operations

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| Union | `union[set1;set2;...]` | `union[1,2;2,3]` | [1,2,3] |
| Intersection | `intersect[set1;set2;...]` | `intersect[1,2;2,3]` | [2] |
| Difference | `diff[set1;set2;...]` | `diff[1,2,3;3]` | [1,2] |
| Symmetric Diff | `symdiff[set1;set2;...]` | `symdiff[1,2;2,3]` | [1,3] |

## Date Operations

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| Date Difference | `datediff[date1;date2]` | `datediff[2023-01-01;2023-12-31]` | 364 days |
| Date Addition | `dateadd[date;days]` | `dateadd[2023-01-01;30]` | 2023-01-31 |

## Advanced Features (via Buttons)

- **Vector Ops**: Vector addition, dot product, cross product, magnitude
- **Matrix Ops**: Matrix multiplication, determinant, transpose
- **Statistics**: Mean, median, mode, standard deviation
- **Base52**: Convert between numbers and base-52 (letter encoding)
- **SI Prefixes**: Apply metric prefixes (k, M, G, m, u, n, etc.)
- **Magic Square**: Magic square validation
- **Recursive Compress**: String pattern compression

## Command Line Usage

### GUI Mode
```bash
python UML_Core/launch.py gui
```

### Test Mode
```bash
python UML_Core/launch.py test "expression"
```

### Feature Demo
```bash
python UML_Core/feature_demo.py
```

## Keyboard Shortcuts

- **Enter**: Calculate the current expression
- **Escape**: Clear the current expression
- **Up/Down Arrow**: Navigate calculation history

© 2025 UML Calculator Project

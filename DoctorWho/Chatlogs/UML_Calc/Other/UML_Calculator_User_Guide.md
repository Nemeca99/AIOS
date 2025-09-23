# UML Calculator User Manual

## Introduction

Welcome to the UML Calculator - a sophisticated mathematical tool that integrates multiple notation systems including standard arithmetic, Universal Mathematical Language (UML), and Recursive Integration System (RIS). This powerful offline calculator combines traditional calculation capabilities with advanced symbolic and recursive mathematical operations.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Calculation Modes](#calculation-modes)
4. [Basic Operations](#basic-operations)
5. [UML Notation](#uml-notation)
6. [RIS Operations](#ris-operations)
7. [Advanced Features](#advanced-features)
8. [Command Reference](#command-reference)
9. [Troubleshooting](#troubleshooting)
10. [Technical Information](#technical-information)

## Getting Started

### System Requirements

- Windows, macOS, or Linux operating system
- Python 3.6 or later
- Tkinter library (included with most Python installations)

### Installation

No installation is required. Simply extract all files to a directory of your choice.

### Launching the Calculator

#### Windows

1. Double-click the `run_calculator.bat` file in the main directory.
2. Alternatively, open a command prompt in the main directory and run:

```bash
python UML_Core\launch.py
```

#### macOS/Linux

1. Open a terminal in the main directory and run:

```bash
python UML_Core/launch.py
```

### Command Line Options

The calculator supports the following command line options:

1. **GUI Mode**:

```bash
python UML_Core/launch.py gui
```

2. **Test Mode** (Evaluate an expression in all modes):

```bash
python UML_Core/launch.py test "your_expression_here"
```

## Interface Overview

The UML Calculator interface consists of:

1. **Expression Entry** - Enter mathematical expressions here.
2. **Result Display** - Shows the calculated result.
3. **Mode Selection** - Choose between Standard, UML, and RIS calculation modes.
4. **Calculator Keypad** - Use to input expressions with a mouse.
5. **Advanced Functions** - Access specialized mathematical operations.
6. **History Panel** - View your previous calculations.

## Calculation Modes

### Standard Mode

Evaluates expressions using conventional arithmetic rules (PEMDAS).

### UML Mode (Universal Mathematical Language)

Uses symbolic notation with specialized bracket pairs for operations.

### RIS Mode (Recursive Integration System)

Employs meta-operators and recursive compression for advanced calculations.

## Basic Operations

### Standard Arithmetic

- Addition: `a + b`
- Subtraction: `a - b`
- Multiplication: `a * b`
- Division: `a / b`
- Exponentiation: `a ** b`
- Modulo: `a % b`

### Functions

- Square Root: `sqrt(x)` or `x ** 0.5`
- Absolute Value: `abs(x)`
- Logarithm (base 10): `log10(x)`
- Natural Logarithm: `log(x)` or `ln(x)`
- Trigonometric: `sin(x)`, `cos(x)`, `tan(x)`

## UML Notation

UML (Universal Mathematical Language) uses paired brackets to denote operations.

### Basic UML Notation

- Addition: `[A,B]` → A + B
- Subtraction: `{A,B}` → A - B
- Multiplication: `>A,B<` → A × B
- Division: `<A,B>` → A ÷ B
- Exponentiation: `^[A]` → A²
- Root: `/[N,X]` → X^(1/N)
- Logarithm: `?(A,B)` → log_A(B)
- Factorial: `!A` → A!
- Modulo: `%[A,B]` → A mod B

### Example UML Expressions

- `[3,4]` = 7 (addition)
- `{10,3}` = 7 (subtraction)
- `>3,4<` = 12 (multiplication)
- `<20,5>` = 4 (division)
- `^[3]` = 9 (square)
- `/[2,9]` = 3 (square root)

### Base-52 Encoding

UML supports base-52 encoding for numbers, using letters:
- A=1, B=2, ..., Z=26, a=27, ..., z=52

Example: `[A,B]` = 3 (1+2)

## RIS Operations

RIS (Recursive Integration System) operations use meta-operators to perform multiple calculations simultaneously.

### RIS Meta-Operator

The meta-operator `@(a,b)` runs all four basic operations (+, -, *, /) and selects the result with the lowest entropy.

### Recursive Compression

The recursive compression operation condenses repeated patterns into simpler forms.

Example: `recursive_compress("AAABBBCDDDEE")` → "3A3B1C3D2E"

## Advanced Features

### Number Theory

- Prime Check: `P[n]` → checks if n is prime (returns 1 for prime, 0 for composite)
- Fibonacci: `F[n]` → returns the nth Fibonacci number
- GCD: `&[a,b]` → greatest common divisor of a and b
- LCM: `|[a,b]` → least common multiple of a and b

### Roman Numerals

- Decimal to Roman: `R[2023]` → "MMXXIII"
- Roman to Decimal: `R[MMXXIII]` → 2023

### Logic Operations

- AND: `AND[1,0,1]` → 0 (logical AND of all values)
- OR: `OR[1,0,1]` → 1 (logical OR of all values)
- NOT: `NOT[1]` → 0 (logical negation)
- XOR: `XOR[1,0,1]` → 0 (exclusive OR)

### Set Operations

- Union: `union[1,2,3;3,4,5]` → [1,2,3,4,5]
- Intersection: `intersect[1,2,3;3,4,5]` → [3]
- Difference: `diff[1,2,3;3,4,5]` → [1,2]
- Symmetric Difference: `symdiff[1,2,3;3,4,5]` → [1,2,4,5]

### Date Calculations

- Date Difference: `datediff[2023-01-01;2023-12-31]` → 364 days
- Date Addition: `dateadd[2023-01-01;30]` → "2023-01-31"

### Vector Operations

Access through the "Vector Ops" button in the Advanced Functions panel.
- Addition, dot product, cross product, magnitude

### Matrix Operations

Access through the "Matrix Ops" button in the Advanced Functions panel.
- Multiplication, determinant, transpose

### Statistical Functions

Access through the "Statistics" button in the Advanced Functions panel.
- Mean, median, mode, standard deviation

### SI Prefixes

Access through the "SI Prefixes" button in the Advanced Functions panel.
- Convert between values with metric prefixes (k, M, G, m, u, n, etc.)

## Command Reference

### Special Function Syntax

| Function | Syntax | Example |
|----------|--------|---------|
| Fibonacci | `F[n]` | `F[10]` → 55 |
| Prime Check | `P[n]` | `P[17]` → 1 (prime) |
| GCD | `&[a,b]` | `&[12,18]` → 6 |
| LCM | `\|[a,b]` | `\|[4,6]` → 12 |
| Modulo | `%[a,b]` | `%[10,3]` → 1 |
| Roman Numeral | `R[n]` or `R[roman]` | `R[2023]` → "MMXXIII" |
| Logic AND | `AND[a,b,...]` | `AND[1,1,0]` → 0 |
| Logic OR | `OR[a,b,...]` | `OR[0,0,1]` → 1 |
| Logic NOT | `NOT[a]` | `NOT[1]` → 0 |
| Logic XOR | `XOR[a,b,...]` | `XOR[1,1]` → 0 |
| Set Union | `union[set1;set2;...]` | `union[1,2;2,3]` → [1,2,3] |
| Set Intersection | `intersect[set1;set2;...]` | `intersect[1,2;2,3]` → [2] |
| Date Difference | `datediff[date1;date2]` | `datediff[2023-01-01;2023-12-31]` → 364 |
| Date Addition | `dateadd[date;days]` | `dateadd[2023-01-01;30]` → "2023-01-31" |

## Troubleshooting

### Common Issues

1. **Calculator Won't Launch**
   - Verify Python is installed and in your PATH
   - Check that all calculator files are in the correct locations
   - Try launching directly with `python UML_Core/enhanced_calculator.py gui`

2. **Expression Evaluation Errors**
   - Check syntax for the specific mode you're using
   - Ensure brackets are properly paired in UML mode
   - Try simplifying complex expressions into smaller steps

3. **UML Notation Not Working**
   - Verify you've selected UML mode
   - Check that bracket pairs match the operation intended
   - Make sure parameters are separated by commas

4. **RIS Operations Not Working**
   - Verify you've selected RIS mode
   - Use the correct meta-operator syntax `@(a,b)`
   - Ensure values are valid for all potential operations

### Error Messages

| Error | Possible Cause | Solution |
|-------|---------------|----------|
| "Cannot parse expression" | Syntax error | Check expression format for the current mode |
| "Division by zero" | Attempting to divide by zero | Modify expression to avoid zero divisor |
| "Invalid Roman numeral" | Using invalid characters | Use only I, V, X, L, C, D, M for Roman numerals |
| "Date Error" | Incorrectly formatted date | Use YYYY-MM-DD format |
| "UML Error" | Invalid UML notation | Review UML bracket pairs and syntax |

## Technical Information

### File Structure

- `run_calculator.bat` - Windows launcher
- `UML_Core/launch.py` - Main entry point script
- `UML_Core/enhanced_calculator.py` - Main calculator implementation
- `UML_Core/uml_core.py` - Core UML/RIS calculation logic
- `UML_Core/feature_enhancements.py` - Additional features
- `UML_Core/symbolic_extensions.py` - Extended symbolic operations

### Advanced Usage

#### Command Line Interface

For batch processing or scripting, you can use the calculator in test mode:

```bash
python UML_Core/launch.py test "expression"
```

This will evaluate the expression in all modes (Standard, UML, RIS) and display the results.

#### Custom Demos

To run specific feature demonstrations:

```bash
python UML_Core/feature_demo.py
```

---

## About UML Calculator

The UML Calculator is based on the Universal Mathematical Language and Recursive Integration System concepts. It integrates traditional arithmetic with symbolic notation, recursive operations, and specialized mathematical functions to provide a comprehensive calculation environment.

Developed with T.R.E.E.S. (The Recursive Entropy Engine System) principles, this calculator demonstrates the practical application of recursive mathematics and symbolic logic in computation.

© 2025 UML Calculator Project

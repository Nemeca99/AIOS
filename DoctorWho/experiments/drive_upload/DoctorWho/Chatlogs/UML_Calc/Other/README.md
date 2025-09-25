# UML Calculator

## Overview

The UML Calculator is an advanced mathematical tool that integrates multiple notation systems:
- Standard arithmetic (PEMDAS)
- Universal Mathematical Language (UML) symbolic notation
- Recursive Integration System (RIS) with meta-operators

This offline calculator combines traditional calculation capabilities with advanced symbolic and recursive mathematical operations, designed according to T.R.E.E.S. (The Recursive Entropy Engine System) principles.

![UML Calculator Screenshot](UML_Calculator_Screenshot.png)

## Features

- **Multiple Calculation Modes**: Switch between Standard, UML, and RIS modes
- **UML Symbolic Notation**: Use specialized bracket pairs for mathematical operations
- **RIS Meta-Operators**: Perform multiple calculations simultaneously with entropy-based selection
- **Recursive Compression**: Analyze and compress repeated patterns
- **Advanced Mathematics**: Number theory, vector/matrix operations, statistics
- **Extended Features**: Roman numerals, logic operations, set theory, date calculations
- **Base-52 Encoding**: Convert between numbers and letter-based representation
- **Command Line Interface**: Run calculations or launch GUI from terminal
- **Interactive UI**: Modern interface with history tracking
- **Comprehensive Help**: Built-in demonstrations and examples

## Getting Started

### Requirements

- Python 3.6 or later
- Tkinter library (included with most Python installations)

### Quick Start

1. Clone or download this repository
2. Run the calculator:

**Windows**:
- Double-click `run_calculator.bat`
- Or open command prompt and run: `python UML_Core\launch.py`

**macOS/Linux**:
- Open terminal and run: `python UML_Core/launch.py`

## Documentation

- [User Guide](UML_Calculator_User_Guide.md): Complete documentation of all features
- [Quick Reference](UML_Calculator_Quick_Reference.md): Handy reference sheet for syntax and operations

## Core Files

- `run_calculator.bat`: Windows launcher script
- `UML_Core/launch.py`: Main entry point script
- `UML_Core/enhanced_calculator.py`: Main calculator implementation with GUI
- `UML_Core/uml_core.py`: Core UML/RIS calculation logic
- `UML_Core/feature_enhancements.py`: Additional features (Roman numerals, logic ops, etc.)
- `UML_Core/symbolic_extensions.py`: Extended symbolic and numeric features
- `UML_Core/feature_demo.py`: Standalone demonstration script

## Usage Examples

### Standard Mode
```
2 + 3 * 4
```
Result: 14 (follows PEMDAS)

### UML Mode
```
[3,4]         → 7 (addition)
{10,3}        → 7 (subtraction)
>3,4<         → 12 (multiplication)
<20,5>        → 4 (division)
```

### RIS Mode
```
@(4,2)        → 2 (meta-operator selects division as lowest entropy)
```

### Special Functions
```
F[10]         → 55 (10th Fibonacci number)
P[17]         → 1 (checks if 17 is prime, 1=yes)
R[2023]       → MMXXIII (converts to Roman numerals)
AND[1,0,1]    → 0 (logical AND operation)
union[1,2;2,3] → [1,2,3] (set union)
```

## Command Line Options

```bash
# Launch GUI
python UML_Core/launch.py gui

# Evaluate expression in all modes
python UML_Core/launch.py test "3+4"

# Run feature demonstrations
python UML_Core/feature_demo.py
```

## Contributing

Bug reports and feature requests are welcome. Please use GitHub Issues for tracking.

## License

© 2025 UML Calculator Project

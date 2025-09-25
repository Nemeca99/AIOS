# UML Calculator V1

The UML Calculator is a robust implementation of the Universal Mathematical Language (UML) calculator, featuring both GUI and CLI interfaces. This project follows the T.R.E.E.S. (The Recursive Entropy Engine System) principles for advanced mathematical calculations.

## Features

- Modern and responsive Tkinter GUI
- Powerful command-line interface
- UML symbolic notation with RIS meta-operator
- Recursive compression for large values
- Base-52 symbolic encoding
- Safe evaluation of expressions
- Step-by-step calculation display

## Getting Started

### Running the Calculator

1. To launch the calculator with a menu interface, run:

   ```batch
   run_calculator.bat
   ```

2. To directly launch the GUI:

   ```bash
   python calculator.py --gui
   ```

3. To directly launch the CLI:

   ```bash
   python calculator.py --cli
   ```

4. To evaluate a single expression in CLI mode:

   ```bash
   python calculator.py --cli "2+2"
   ```

### Using the GUI

- Enter expressions in standard notation (`2+3*4`) or UML notation (`[2,<3,4>]`)
- Toggle between Standard, UML, and RIS modes
- View calculation history and detailed steps
- Save/load calculation history

### Using the CLI

- Interactive mode: `python calculator.py --cli --interactive`
- Single expression: `python calculator.py --cli "expression"`
- Mode switching: Type `mode standard`, `mode uml`, or `mode ris`
- Toggle step display: Type `steps on` or `steps off`

## Project Structure

```text
UML_Calculator_V1/
├── core/
│   ├── uml_core.py       # Core UML parsing and evaluation
│   └── converters.py     # Standard-to-UML conversion
├── ui/
│   ├── calculator_gui.py # Tkinter GUI interface
│   └── calculator_cli.py # Command-line interface
├── utils/
│   ├── safe_eval.py      # Safe expression evaluation
│   └── symbolic_extensions.py # Extra mathematical functions
├── calculator.py         # Main entry point
├── calculator_cli.py     # Direct CLI launcher
├── calculator_gui.py     # Direct GUI launcher
└── run_calculator.bat    # Batch file launcher
```

## Mathematical Notation

The UML Calculator supports multiple notation styles:

- **Standard Notation**: `2+3*4`
- **UML Notation**:
  - Addition: `[a,b]`
  - Subtraction: `{a,b}`
  - Multiplication: `<a,b>`
  - Division: `<>a,b<>`
- **RIS Meta-Operator**: `@(a,b[,operation])` with entropy-based operation selection

## Built With

- Python 3.x
- Tkinter for GUI
- T.R.E.E.S. principles for advanced mathematical computation

## Author

- Travis Miner and AI Collaborator

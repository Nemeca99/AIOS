# TREES Project Integration Guide

This document provides guidance on integrating the UML Calculator and Codex Web Calculator components of the TREES framework.

## Project Structure

The TREES project consists of two main components:

1. **UML Calculator** - Located in `d:\UML Calculator`
   - Core mathematical engine for UML operations
   - RIS meta-operators
   - Magic square analysis

2. **Codex Web Calculator** - Located in `e:\Algebra`
   - Web interface for symbolic algebra
   - Integration with UML engine
   - Memory context for theory reference

## Integration Methods

### Method 1: Using the Unified Launcher

The simplest way to integrate the components is through the unified launcher script:

```bash
d:\UML Calculator\launch_unified_calculator.bat
```

This script provides a menu to select which calculator to launch.

### Method 2: Using VS Code Tasks

The project includes VS Code task definitions in `d:\UML Calculator\trees_tasks.json`.
To use these tasks:

1. Open VS Code
2. Open the Command Palette (Ctrl+Shift+P)
3. Type "Tasks: Run Task" and select
4. Choose one of the available tasks:
   - Run UML Calculator
   - Run Codex Web Calculator
   - Run Unified Calculator

### Method 3: Direct Integration

For programmatic integration, you can import the core modules directly:

```python
# Import UML Core
import sys
sys.path.append(r'd:\UML Calculator\UML_Core')
from uml_core import parse_uml, eval_uml, recursive_compress

# Import Codex Symbolic Engine
sys.path.append(r'e:\Algebra\Calculator')
from codex_symbolic_core import SymbolicProcessor
```

## API Reference

### UML Calculator API

- `parse_uml(expr)` - Parse UML expressions
- `eval_uml(expr)` - Evaluate UML expressions
- `recursive_compress(expr)` - Apply recursive compression
- `ris_meta_operator(expr, op)` - Apply RIS meta-operator

### Codex Web Calculator API

- `SymbolicProcessor` - Class for symbolic algebra processing
- `load_codex_context()` - Load Codex context from memory
- `process_symbolic_expression(expr)` - Process symbolic expressions

## Testing Integration

To verify successful integration, you can run:

```bash
d:\UML Calculator\UML_Core\feature_demo.py
```

This will demonstrate key UML features and verify that the core engine is working correctly.

## Common Issues and Solutions

### Path Resolution

If you encounter path resolution issues, ensure that the absolute paths are correctly specified:

```python
# Correct path specification
sys.path.append(os.path.abspath(r'd:\UML Calculator\UML_Core'))
```

### Module Import Errors

If you see module import errors, check that all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Cross-Domain Integration

For cross-domain integration (between UML and Codex), use the bridge modules:

```python
from uml_symbolic_engine import UMLSymbolicBridge
```

## Contributing to Integration

When contributing new integration features:

1. Always maintain backward compatibility
2. Document any API changes
3. Include tests for new integration points
4. Follow the project's coding standards

## Version Compatibility

| UML Calculator | Codex Web Calculator | Compatibility Status |
|---------------|----------------------|----------------------|
| 1.0           | 1.0                  | Fully Compatible     |
| 1.1           | 1.0                  | Partial Support      |
| 1.1           | 1.1                  | Fully Compatible     |

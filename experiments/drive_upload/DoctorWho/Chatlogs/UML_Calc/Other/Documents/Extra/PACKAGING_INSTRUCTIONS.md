# UML Calculator Packaging Instructions

This document provides instructions for packaging and distributing the UML Calculator to end users.

## Required Files for Distribution

The following files must be included in any distribution package:

### Core Files
- `UML_Core/enhanced_calculator.py` (Main calculator implementation)
- `UML_Core/uml_core.py` (Core UML/RIS logic)
- `UML_Core/feature_enhancements.py` (Additional features)
- `UML_Core/symbolic_extensions.py` (Extended symbolic operations)
- `UML_Core/launch.py` (Entry point script)
- `UML_Core/feature_demo.py` (Demonstration script)

### Documentation
- `README.md` (Overview and basic instructions)
- `UML_Calculator_User_Guide.md` (Comprehensive documentation)
- `UML_Calculator_Quick_Reference.md` (Reference sheet)

### Launcher Scripts
- `run_calculator.bat` (Windows launcher)

## Creating a Distribution Package

### Option 1: ZIP Archive

1. Create a ZIP file containing all required files
2. Maintain the directory structure exactly as shown
3. Name the archive `UML_Calculator_vX.Y.Z.zip` (replace X.Y.Z with version number)

### Option 2: Executable Package (Windows)

You can use PyInstaller to create a standalone executable that doesn't require Python installation:

1. Install PyInstaller: `pip install pyinstaller`
2. Run the packaging command:
   ```bash
   pyinstaller --onefile --windowed --add-data "UML_Core/feature_enhancements.py;UML_Core" --add-data "UML_Core/symbolic_extensions.py;UML_Core" --add-data "UML_Core/uml_core.py;UML_Core" --add-data "*.md;." UML_Core/launch.py
   ```
3. The executable will be created in the `dist` directory
4. Include the documentation files with the executable

### Option 3: Python Package

1. Create a `setup.py` file with package information
2. Run `python setup.py sdist bdist_wheel` to create package
3. Distribute the resulting wheel file

## Installation Instructions for Users

Include these instructions with your distribution:

### For ZIP Archive

1. Extract the ZIP file to any directory
2. Ensure Python 3.6+ is installed with Tkinter
3. Run `run_calculator.bat` (Windows) or `python UML_Core/launch.py` (macOS/Linux)

### For Executable Package

1. Extract the package to any directory
2. Run the executable file `launch.exe`

## Version History File

Include a `VERSION_HISTORY.md` file with the following information:

```markdown
# UML Calculator Version History

## Version 1.0.0 (June 23, 2025)
- Initial release with UML, RIS, and Standard calculation modes
- Added support for Roman numerals, logic operations, set theory
- Implemented comprehensive GUI and CLI interfaces
```

## Creating User Documentation

The following documentation files should be included:

1. `README.md` - Brief introduction and quick start
2. `UML_Calculator_User_Guide.md` - Comprehensive documentation
3. `UML_Calculator_Quick_Reference.md` - Cheat sheet of commands and syntax

Consider converting these Markdown files to PDF format for easier distribution:

```bash
# Using pandoc (if installed)
pandoc UML_Calculator_User_Guide.md -o UML_Calculator_User_Guide.pdf
```

## Support Information

Include contact information for support requests:

```
For support or feature requests, please contact:
umlcalculator@example.com

Or submit issues on the project's GitHub repository:
https://github.com/umlcalculator/umlcalc
```

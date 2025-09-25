# AIOS Duality System - Development Environment Setup

## 🎯 **OVERVIEW**

This document provides comprehensive instructions for setting up and using the development environment for the AIOS Duality System. The environment is designed to work seamlessly both inside VS Code and in external Windows terminals.

## 🚀 **QUICK START**

### **1. Initial Setup (One-time)**
```bash
# Run the development environment setup
setup_dev_environment.bat
# OR
.\setup_dev_environment.ps1
```

### **2. Activate Environment**
```bash
# Windows Batch
activate_koneko_env.bat

# PowerShell
.\activate_koneko_env.ps1
```

### **3. Run Development Tools**
```bash
# Interactive menu
dev_tools.bat
# OR
.\dev_tools.ps1
```

## 🐍 **PYTHON ENVIRONMENT**

### **Environment Details**
- **Location**: `./koneko_env/`
- **Python Version**: 3.10
- **Status**: ✅ **FULLY CONFIGURED**

### **Activation Methods**

#### **Windows Batch**
```batch
activate_koneko_env.bat
```

#### **PowerShell**
```powershell
.\activate_koneko_env.ps1
```

#### **Manual Activation**
```cmd
koneko_env\Scripts\activate.bat
```

## 🛠️ **DEVELOPMENT TOOLS**

### **Available Tools**

| Tool | Purpose | Command |
|------|---------|---------|
| **Black** | Code formatting | `python -m black .` |
| **Flake8** | Code linting | `python -m flake8 .` |
| **Pylint** | Advanced linting | `python -m pylint Koneko/` |
| **isort** | Import sorting | `python -m isort .` |
| **pytest** | Testing | `python -m pytest` |
| **mypy** | Type checking | `python -m mypy .` |

### **Tool Configuration**

#### **Black (Code Formatter)**
- **Line Length**: 88 characters
- **Target Version**: Python 3.10
- **Configuration**: `pyproject.toml`

#### **Flake8 (Linter)**
- **Line Length**: 88 characters
- **Ignores**: E203, W503
- **Configuration**: `.flake8`

#### **Pylint (Advanced Linter)**
- **Line Length**: 88 characters
- **Ignores**: C0114, C0115, C0116
- **Configuration**: `.pylintrc`

#### **isort (Import Sorter)**
- **Profile**: Black-compatible
- **Line Length**: 88 characters
- **Configuration**: `pyproject.toml`

## 🔧 **VS CODE INTEGRATION**

### **Automatic Features**
- ✅ **Python Interpreter**: Automatically selects `./koneko_env/Scripts/python.exe`
- ✅ **Environment Activation**: Terminals automatically activate the virtual environment
- ✅ **Code Formatting**: Formats code on save using Black
- ✅ **Import Organization**: Organizes imports on save using isort
- ✅ **IntelliSense**: Full code completion and analysis
- ✅ **Linting**: Real-time error detection with Flake8 and Pylint

### **Workspace Configuration**
- **File**: `AIOS_Duality_System_Ava-Koneko.code-workspace`
- **Settings**: `.vscode/settings.json`
- **Launch Configs**: `.vscode/launch.json`
- **Tasks**: Built-in VS Code tasks for common operations

### **Terminal Profiles**
- **PowerShell**: Automatically activates environment
- **Command Prompt**: Automatically activates environment
- **Custom**: Can be configured for other shells

## 📋 **DEVELOPMENT COMMANDS**

### **Code Quality Commands**

#### **Format Code**
```bash
# Format all Python files
python -m black Koneko Blackwall

# Format specific directory
python -m black Koneko/

# Check formatting without changes
python -m black --check .
```

#### **Lint Code**
```bash
# Basic linting with Flake8
python -m flake8 Koneko Blackwall

# Advanced linting with Pylint
python -m pylint Koneko --rcfile=.pylintrc

# Type checking with mypy
python -m mypy Koneko/
```

#### **Sort Imports**
```bash
# Sort imports in all files
python -m isort Koneko Blackwall

# Check import sorting without changes
python -m isort --check-only .
```

### **Testing Commands**

#### **Run All Tests**
```bash
# Run all tests with verbose output
python -m pytest Koneko/Systems_Refactored/Testing -v

# Run tests with coverage
python -m pytest --cov=Koneko

# Run specific test file
python -m pytest Koneko/Systems_Refactored/Testing/test_functions.py
```

#### **Test Koneko System**
```bash
# Test mode
python Koneko/launch_koneko.py --mode test

# Interactive mode
python Koneko/launch_koneko.py --mode interactive

# Terminal mode
python Koneko/launch_koneko.py --mode terminal
```

### **Environment Management**

#### **Install Dependencies**
```bash
# Install all requirements
pip install -r Koneko/requirements.txt

# Install development tools
pip install black flake8 pytest pylint isort mypy

# Update packages
pip install --upgrade -r Koneko/requirements.txt
```

#### **Check Environment Status**
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check environment path
python -c "import sys; print(sys.executable)"
```

## 🎮 **INTERACTIVE DEVELOPMENT TOOLS**

### **Development Tools Menu**

#### **Windows Batch Version**
```bash
dev_tools.bat
```

#### **PowerShell Version**
```bash
.\dev_tools.ps1
```

### **Available Options**
1. **Activate Python Environment**
2. **Test Koneko System**
3. **Run Koneko Interactive**
4. **Format Code (Black)**
5. **Lint Code (Flake8)**
6. **Lint Code (Pylint)**
7. **Sort Imports (isort)**
8. **Run Tests (pytest)**
9. **Install Dependencies**
10. **Check Environment Status**
11. **Open VS Code**
12. **Open Terminal**

### **Command Line Usage**
```bash
# Run specific actions directly
.\dev_tools.ps1 -Action test
.\dev_tools.ps1 -Action format
.\dev_tools.ps1 -Action lint
```

## 🔍 **TROUBLESHOOTING**

### **Common Issues**

#### **Python Environment Not Found**
```bash
# Check if environment exists
dir koneko_env

# Recreate environment if needed
python -m venv koneko_env
koneko_env\Scripts\activate.bat
pip install -r Koneko\requirements.txt
```

#### **Package Import Errors**
```bash
# Ensure environment is activated
koneko_env\Scripts\activate.bat

# Reinstall packages
pip install --force-reinstall -r Koneko\requirements.txt

# Check package installation
pip list | findstr package_name
```

#### **VS Code Issues**
```bash
# Reset VS Code settings
# Delete .vscode folder and reopen workspace

# Check Python interpreter
# Ctrl+Shift+P → "Python: Select Interpreter"
# Choose: ./koneko_env/Scripts/python.exe
```

#### **Permission Issues**
```bash
# Run PowerShell as Administrator
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Environment Reset**
```bash
# Complete environment reset
rmdir /s koneko_env
python -m venv koneko_env
koneko_env\Scripts\activate.bat
pip install -r Koneko\requirements.txt
python -m spacy download en_core_web_sm
setup_dev_environment.bat
```

## 📚 **CONFIGURATION FILES**

### **Environment Files**
- **`.env`**: Environment variables
- **`pyproject.toml`**: Black, isort, pytest, flake8 configuration
- **`.flake8`**: Flake8 linting configuration
- **`.pylintrc`**: Pylint configuration

### **VS Code Files**
- **`AIOS_Duality_System_Ava-Koneko.code-workspace`**: Workspace configuration
- **`.vscode/settings.json`**: VS Code settings
- **`.vscode/launch.json`**: Debug configurations

### **Development Scripts**
- **`setup_dev_environment.bat/.ps1`**: Environment setup
- **`dev_tools.bat/.ps1`**: Development tools menu
- **`activate_koneko_env.bat/.ps1`**: Environment activation

## 🚀 **WORKFLOW EXAMPLES**

### **Daily Development Workflow**
```bash
# 1. Activate environment
activate_koneko_env.bat

# 2. Make code changes
# ... edit files ...

# 3. Format and lint code
python -m black .
python -m flake8 .
python -m isort .

# 4. Run tests
python -m pytest

# 5. Test Koneko system
python Koneko/launch_koneko.py --mode test
```

### **Code Review Workflow**
```bash
# 1. Check code quality
python -m black --check .
python -m flake8 .
python -m isort --check-only .

# 2. Run tests
python -m pytest --cov=Koneko

# 3. Type checking
python -m mypy Koneko/

# 4. Manual testing
python Koneko/launch_koneko.py --mode test
```

### **New Feature Development**
```bash
# 1. Setup development environment
setup_dev_environment.bat

# 2. Install new dependencies
pip install new_package
pip freeze > Koneko/requirements.txt

# 3. Write tests
# ... create test files ...

# 4. Implement feature
# ... write code ...

# 5. Validate changes
python -m black .
python -m flake8 .
python -m pytest
```

## 🎉 **SYSTEM STATUS**

### **Development Environment**
- ✅ **Python Environment**: Fully configured
- ✅ **Development Tools**: All installed and configured
- ✅ **VS Code Integration**: Complete setup
- ✅ **Code Quality Tools**: Black, Flake8, Pylint, isort
- ✅ **Testing Framework**: pytest configured
- ✅ **Documentation**: Comprehensive guides

### **Koneko System**
- ✅ **Core Systems**: All operational
- ✅ **Development Ready**: Full development workflow
- ✅ **Testing**: Comprehensive test suite
- ✅ **Code Quality**: Automated formatting and linting

---

**Development Environment**: ✅ **FULLY CONFIGURED**  
**VS Code Integration**: ✅ **COMPLETE**  
**External Terminal Support**: ✅ **WORKING**  
**Code Quality Tools**: ✅ **ALL AVAILABLE**  

**The AIOS Duality System is ready for professional development!** 🚀✨

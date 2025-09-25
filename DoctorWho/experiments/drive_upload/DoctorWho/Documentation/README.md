# 🚀 Development Folder - AIOS Duality System

This folder contains all development-related tools, scripts, and documentation for the AIOS Duality System.

## 📁 **Contents**

### **Scripts & Tools**
- **`quick_dev.bat`** ⭐ **RECOMMENDED** - Simple, non-hanging batch file for direct development commands
- **`dev_tools.bat`** - Interactive development menu (may hang on some systems)
- **`dev_tools.ps1`** - Interactive PowerShell development menu
- **`dev_tools_auto.bat`** - Non-interactive batch version
- **`dev_tools_auto.ps1`** - Non-interactive PowerShell version
- **`setup_dev_environment.bat`** - One-time setup script for development environment
- **`setup_dev_environment.ps1`** - PowerShell version of setup script

### **Documentation**
- **`README.md`** - This file
- **`Documentation/`** - Centralized documentation from Koneko and Blackwall systems
  - `development_guide.md` - Development workflow and guidelines
  - `user_guide.md` - User interface and system usage
  - `system_architecture.md` - Technical architecture overview
  - `PROJECT_STRUCTURE.md` - Koneko system structure
  - `STANDALONE_COMPLETION_SUMMARY.md` - System completion status
  - `DUAL_LEXICON_SYSTEM_COMPLETE.md` - Lexicon system documentation
  - `AVA_PERSONALITY_INTEGRATION_COMPLETE.md` - Personality system documentation
  - `BlackBox.md` - Blackwall system documentation

## 🎯 **Quick Development Commands**

### **Using `quick_dev.bat` (Recommended)**
```batch
# Basic commands
quick_dev.bat activate      # Activate Python environment
quick_dev.bat status       # Check environment status
quick_dev.bat install      # Install dependencies

# Testing commands
quick_dev.bat test         # Test Koneko system
quick_dev.bat bigfive      # Run Big Five personality test
quick_dev.bat psychometrics # Run advanced psychometrics suite
quick_dev.bat bdsm         # Run BDSM personality test
quick_dev.bat tests        # Run pytest test suite

# Code quality commands
quick_dev.bat format       # Format code with Black
quick_dev.bat lint         # Lint code with Flake8
quick_dev.bat sort         # Sort imports with isort
```

### **Available Commands**
- **`activate`** - Activate Python virtual environment
- **`test`** - Test Koneko system
- **`bigfive`** - Run Big Five personality test
- **`psychometrics`** - Run advanced psychometrics suite
- **`bdsm`** - Run BDSM personality test 🆕
- **`format`** - Format code with Black
- **`lint`** - Lint code with Flake8
- **`status`** - Check environment status
- **`install`** - Install dependencies
- **`tests`** - Run tests with pytest
- **`sort`** - Sort imports with isort

## 🧠 **Psychological Testing Suite**

The system now includes a comprehensive psychological assessment framework:

### **Big Five Personality Test**
- Tests Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- Based on IPIP-NEO-PI research model
- Includes stress testing for consistency validation

### **Advanced Psychometrics Suite**
- **HEXACO Personality Inventory** - Six-factor model including Honesty-Humility
- **DASS (Depression, Anxiety, Stress)** - Clinical assessment of emotional states
- **Artistic Preferences Scale** - Aesthetic and artistic taste preferences
- **IQ Vocabulary Test** - Verbal intelligence assessment
- **BDSM Personality Test** - Power dynamics and intimate preferences 🆕

### **BDSM Personality Test** 🆕
- **59 comprehensive questions** covering all aspects of BDSM psychology
- **20+ personality traits** including Dominance, Submissiveness, Switching
- **Facet-level analysis** for detailed psychological mapping
- **Consistency testing** across multiple rounds
- **Scientific validation** based on established BDSM research

### **Dynamic Personality Test** 🆕
- **Multi-scenario testing** of personality adaptation capabilities
- **Argument building** over 10-100 messages with perspective shifting
- **Emotional intensity matching** and mood adaptation
- **Power dynamic shifts** and context sensitivity
- **Comprehensive scoring** with detailed feedback and recommendations

## 🎭 **VTuber Integration Project** 🆕

### **Project Status**
- **Repository**: [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber.git) cloned
- **Location**: `Koneko/Todo/Vtuber/`
- **Status**: Ready for analysis and integration planning

### **Integration Goals**
Transform Koneko from text-based AI to **fully interactive virtual companion**:
- Live2D animated avatar with emotional expressions
- Voice synthesis and recognition
- Visual perception capabilities
- Touch and interaction feedback
- Desktop pet mode
- Multi-modal personality expression

### **Technical Requirements**
- **CPU**: Intel i7-11700F ✅ (Sufficient)
- **GPU**: RTX 3060 Ti ✅ (Excellent for AI acceleration)
- **RAM**: 32GB ✅ (Plenty for multiple AI models)

### **Implementation Phases**
1. **Analysis & Planning** (1-2 weeks)
2. **Core Integration** (3-4 weeks)
3. **Advanced Features** (2-3 weeks)
4. **Testing & Optimization** (1-2 weeks)

## 🔧 **Development Environment**

### **Python Environment**
- **Virtual Environment**: `koneko_env` (located in workspace root)
- **Python Version**: 3.10+
- **Package Manager**: pip with requirements.txt

### **Code Quality Tools**
- **Black** - Code formatting
- **Flake8** - Linting
- **Pylint** - Advanced linting
- **isort** - Import sorting
- **pytest** - Testing framework
- **mypy** - Type checking

### **VS Code Integration**
- **Workspace**: `AIOS_Duality_System_Ava-Koneko.code-workspace`
- **Python Interpreter**: Automatically set to `koneko_env`
- **Terminal**: Auto-activates virtual environment
- **Extensions**: Recommended Python development tools

## 📚 **Key Features**

### **Non-Hanging Scripts**
- **`quick_dev.bat`** is designed to execute commands without requiring manual intervention
- All commands run to completion automatically
- No "pause" or "Enter to continue" prompts

### **Comprehensive Testing**
- **Personality Assessment**: Big Five, HEXACO, DASS, BDSM
- **System Testing**: Koneko core functionality
- **Code Quality**: Automated formatting, linting, and testing
- **Consistency Validation**: Multi-round stress testing

### **Modular Architecture**
- **Testing Framework**: Extensible psychometric testing suite
- **Personality System**: Multi-dimensional trait assessment
- **Development Tools**: Scriptable and automated workflows

## 🚀 **Getting Started**

1. **Activate Environment**: `quick_dev.bat activate`
2. **Check Status**: `quick_dev.bat status`
3. **Install Dependencies**: `quick_dev.bat install`
4. **Run Tests**: `quick_dev.bat test` or `quick_dev.bat bigfive`

## 📝 **Recent Updates**

### **Dynamic Personality System** 🆕
- **Dynamic Personality Engine**: Context-aware personality state switching
- **Adaptive Response Generator**: Multi-message argument building with perspective shifting
- **Comprehensive Testing**: 4-scenario evaluation of adaptation capabilities
- **Added `dynamic` command** to quick_dev.bat for personality testing

### **BDSM Test Integration** 🆕
- Added comprehensive BDSM personality assessment
- 59 questions covering 20+ psychological traits
- Integrated with existing psychometrics suite
- Added `bdsm` command to quick_dev.bat

### **VTuber Project Setup** 🆕
- Cloned Open-LLM-VTuber repository
- Created comprehensive integration TODO
- Assessed hardware compatibility
- Planned implementation phases

## 🔮 **Future Development**

### **Immediate Priorities**
- **Refine Dynamic Personality System**: Improve context sensitivity and argument escalation
- **Enhance Personality State Variety**: Add more sophisticated adaptation patterns
- **Optimize Response Generation**: Fine-tune strategy selection and response quality
- **Complete BDSM Test Validation**: Ensure consistency across all scenarios

### **Medium-term Goals**
- **Advanced Adaptation Patterns**: Develop more sophisticated personality switching logic
- **Emotional Intelligence Enhancement**: Improve mood matching and emotional depth
- **Begin VTuber Integration**: Start analysis and planning phase
- **Expand Psychometric Testing**: Add more specialized assessment tools

### **Long-term Goals**
- Full VTuber integration with Live2D avatar
- Voice synthesis and recognition
- Visual perception and interaction
- Desktop pet mode implementation

---

**Last Updated**: 2025-08-15  
**Status**: BDSM test integrated, VTuber project cloned  
**Next Steps**: VTuber integration analysis and planning  

*This development environment provides comprehensive tools for building the most advanced AI personality system in existence.* 🚀✨

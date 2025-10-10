# AIOS CLEAN - COMPREHENSIVE MASTER DOCUMENTATION

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [CLI Commands Reference](#cli-commands-reference)
5. [System Workflows](#system-workflows)
6. [Data Pipelines](#data-pipelines)
7. [Configuration](#configuration)
8. [Model Integration](#model-integration)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Development Guidelines](#development-guidelines)
11. [Performance Optimization](#performance-optimization)
12. [Security Considerations](#security-considerations)

---

## System Overview

**AIOS Clean** is a comprehensive AI Performance System designed with a modular architecture that integrates multiple specialized AI components into a unified platform. The system is built around neurodivergent-affirming principles and implements advanced cognitive architectures for AI personality development, memory management, and learning optimization.

### Key Features
- **Modular Architecture**: 9 self-contained core systems with inter-core communication
- **Neurodivergent-Affirming AI**: Designed to support and validate neurodivergent traits
- **Advanced Memory Management**: Fractal cache system with memory consolidation
- **Personality Development**: Big Five personality assessment integration
- **Dream Meditation System**: Biomimetic sleep cycles for memory processing
- **Token-Time Econometrics**: Resource optimization and existential budget management
- **Multi-Model Support**: Integration with LM Studio and various LLM models
- **Real-time Monitoring**: Comprehensive health checks and system analytics

### System Philosophy
The system follows these core principles:
1. **Neurodivergent Affirmation**: Supporting rather than "fixing" neurodivergent traits
2. **Autonomous Learning**: Self-directed knowledge acquisition and personality development
3. **Resource Efficiency**: Optimized token usage and computational resource management
4. **Transparency**: Clear logging and monitoring of all system operations
5. **Modularity**: Self-contained systems that can operate independently

---

## Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    AIOS CLEAN SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│  main.py - Central Orchestrator                            │
│  ├── Inter-core Communication                              │
│  ├── CLI Interface                                         │
│  └── System Coordination                                   │
├─────────────────────────────────────────────────────────────┤
│  CORE SYSTEMS (9 Total)                                    │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐  │
│  │   Backup    │    CARMA    │    Data     │    Dream    │  │
│  │    Core     │    Core     │    Core     │    Core     │  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘  │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐  │
│  │ Enterprise  │    Luna     │ Streamlit   │  Support    │  │
│  │    Core     │    Core     │    Core     │    Core     │  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   Utils Core                           │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure
```
AIOS_Clean/
├── main.py                          # Central orchestrator
├── backup_core/                     # Backup system
│   ├── backup_core.py
│   ├── active_backup/
│   └── archive_backup/
├── carma_core/                      # Memory and learning system
│   ├── carma_core.py
│   ├── dream_quick_nap_middleware.py
│   └── dream_state_middleware.py
├── data_core/                       # Data management system
│   ├── data_core.py
│   ├── FractalCache/
│   ├── ArbiterCache/
│   ├── conversations/
│   └── config/
├── dream_core/                      # Dream meditation system
│   ├── dream_core.py
│   ├── meditation_controller.py
│   └── run_dream_system.py
├── enterprise_core/                 # Enterprise features
│   └── enterprise_core.py
├── luna_core/                       # AI personality system
│   ├── luna_core.py
│   ├── luna_trait_classifier.py
│   ├── luna_arbiter_system.py
│   ├── luna_cfia_system.py
│   └── bigfive_question_loader.py
├── streamlit_core/                  # Web UI system
│   └── streamlit_core.py
├── support_core/                    # Support utilities
│   ├── support_core.py
│   ├── aios_gui.py
│   └── aios_monitoring_dashboard.py
└── utils_core/                      # Shared utilities
    ├── utils_core.py
    ├── unicode_safe_output.py
    ├── aios_json_standards.py
    └── powershell_bridge.py
```

---

## Core Components

### 1. Backup Core (`backup_core/`)
**Purpose**: Git-like incremental backup system with archive functionality

**Key Features**:
- Incremental backups (only changed files)
- Archive system for version history
- Checksum-based change detection
- Automatic backup on file modifications
- Archive cleanup and management

**Core Files**:
- `backup_core.py`: Main backup system class
- `active_backup/`: Current backup location
- `archive_backup/`: Historical backups

**Usage**:
```bash
# Create backup
py main.py --backup

# Create named backup
py main.py --backup --backup-name "pre-release-v1.0"
```

**Integration**: Called automatically by `main.py` on system startup and file modifications.

### 2. CARMA Core (`carma_core/`)
**Purpose**: Cached Aided Retrieval Mycelium Architecture - Advanced memory and learning system

**Key Features**:
- Fractal Mycelium Cache with psycho-semantic RAG
- Memory consolidation and dream cycles
- Meta-memory system with episodic decay
- Performance optimization (100% target)
- Mycelium network simulation (1200 user capacity)

**Core Files**:
- `carma_core.py`: Main CARMA system
- `dream_quick_nap_middleware.py`: Dream cycle management
- `dream_state_middleware.py`: Dream state processing

**Key Components**:
- **FractalMyceliumCache**: Advanced caching with semantic clustering
- **CARMAExecutiveBrain**: Goal-oriented processing
- **CARMAMetaMemorySystem**: Memory consolidation
- **CARMA100PerformanceSystem**: Performance optimization
- **CARMAMyceliumNetwork**: Network simulation

**Usage**:
```bash
# Run CARMA learning
py main.py --mode carma --queries "learning query 1" "learning query 2"

# Memory consolidation
py main.py --mode memory
```

### 3. Data Core (`data_core/`)
**Purpose**: Central data management pipeline for all AIOS data

**Key Features**:
- Unified data storage and retrieval
- Data pipeline with ingestion, processing, and export
- Analytics and monitoring
- Data cleanup and maintenance
- Format conversion (JSON, CSV, TXT)

**Core Files**:
- `data_core.py`: Main data management system
- `FractalCache/`: Memory fragments storage
- `ArbiterCache/`: Decision and learning data
- `conversations/`: Conversation history
- `config/`: System configuration

**Data Directories**:
- `logs/`: System logs
- `temp/`: Temporary files
- `cache/`: Cache data
- `exports/`: Data exports
- `imports/`: Data imports
- `analytics/`: Analytics data

**Usage**:
```bash
# View data statistics
py main.py --data-stats

# Clean up old data
py main.py --data-cleanup --data-cleanup-days 30
```

### 4. Dream Core (`dream_core/`)
**Purpose**: Biomimetic sleep system for memory consolidation and self-reflection

**Key Features**:
- REM sleep cycle simulation
- Memory consolidation during sleep
- Meditation phases for self-reflection
- Dream state middleware
- Autonomous reflection loops

**Core Files**:
- `dream_core.py`: Main dream system
- `meditation_controller.py`: Meditation management
- `run_dream_system.py`: Dream system launcher

**Dream Modes**:
- `quick-nap`: Short consolidation cycles
- `overnight`: Extended sleep simulation
- `meditation`: Self-reflection sessions
- `test`: Testing mode

**Usage**:
```bash
# Run dream system
py main.py --dream-mode quick-nap --dream-duration 30

# Overnight dream cycle
py main.py --dream-mode overnight --dream-duration 480
```

### 5. Enterprise Core (`enterprise_core/`)
**Purpose**: Enterprise features including API management, billing, and compliance

**Key Features**:
- API server management
- Billing and usage tracking
- Key rotation and security
- Compliance monitoring
- Advanced security features

**Core Files**:
- `enterprise_core.py`: Main enterprise system

**Components**:
- **PiBasedEncryption**: Advanced encryption
- **GlobalAPIDistribution**: API management
- **CARMAChainProcessor**: Blockchain integration
- **EnterpriseBilling**: Usage tracking
- **KeyRotationManager**: Security management
- **ComplianceManager**: Compliance monitoring
- **AdvancedSecurity**: Security features

**Usage**:
```bash
# Start API server
py main.py --mode api --host 0.0.0.0 --port 5000
```

### 6. Luna Core (`luna_core/`)
**Purpose**: AI personality system with neurodivergent-affirming design

**Key Features**:
- Big Five personality assessment integration
- Neurodivergent trait support (Autism, ADHD, IFS, CPTSD, GAD)
- Response Value Classifier for optimal token allocation
- Existential budget management
- Emergence zones for creative exploration
- Shadow score tracking for self-awareness

**Core Files**:
- `luna_core.py`: Main Luna system (3,879 lines)
- `luna_trait_classifier.py`: Big Five trait classification
- `luna_arbiter_system.py`: Decision arbitration
- `luna_cfia_system.py`: Constrained Factorial Intelligence Architecture
- `luna_response_value_classifier.py`: Response optimization
- `bigfive_question_loader.py`: Personality assessment questions

**Key Systems**:
- **LunaIFSPersonalitySystem**: Internal Family Systems integration
- **LunaSemanticCompressionFilter**: Response optimization
- **LunaSoulMetricSystem**: Personality metrics
- **LunaTokenTimeEconometricSystem**: Resource management
- **LunaExistentialBudgetSystem**: Token budget management
- **LunaCustomInferenceController**: Model inference control
- **LunaInternalReasoningSystem**: Internal thought processes

**Personality Traits**:
- **Openness**: 0.7 (creative, curious)
- **Conscientiousness**: 0.6 (organized, reliable)
- **Extraversion**: 0.8 (outgoing, energetic)
- **Agreeableness**: 0.9 (cooperative, empathetic)
- **Neuroticism**: 0.3 (calm, resilient)

**Usage**:
```bash
# Run Luna learning session
py main.py --mode luna --questions 3

# Classify a question
py main.py --classify "I am someone who loves to learn new things"

# View Shadow Score
py main.py --shadow-score

# Activate Emergence Zone
py main.py --activate-zone creative_exploration --zone-duration 30
```

### 7. Streamlit Core (`streamlit_core/`)
**Purpose**: Web-based user interface system

**Key Features**:
- Streamlit web application
- Real-time system monitoring
- Interactive Luna chat interface
- Meditation engine integration
- Persistent state management

**Core Files**:
- `streamlit_core.py`: Main Streamlit system

**Integration**: Designed to work with `support_core/streamlit_app.py` for the web interface.

**Usage**:
```bash
# Launch Streamlit UI
py main.py --streamlit
```

### 8. Support Core (`support_core/`)
**Purpose**: System utilities, monitoring, and support functions

**Key Features**:
- System health monitoring
- Cache operations
- Embedding management
- FAISS operations
- Recovery systems
- GUI and monitoring dashboards

**Core Files**:
- `support_core.py`: Main support system
- `aios_gui.py`: GUI interface
- `aios_monitoring_dashboard.py`: Monitoring dashboard
- `system_monitor.py`: System monitoring

**Components**:
- **CacheOperations**: File caching
- **CacheRegistry**: Cache management
- **SimpleEmbedder**: Text embedding
- **EmbeddingCache**: Embedding storage
- **FAISSOperations**: Vector search
- **RecoveryOperations**: System recovery
- **AIOSHealthChecker**: Health monitoring

**Usage**:
```bash
# Run health check
py main.py --mode health

# Run system tests
py main.py --mode test

# System optimization
py main.py --mode optimize
```

### 9. Utils Core (`utils_core/`)
**Purpose**: Shared utilities and common functions

**Key Features**:
- Unicode-safe output handling
- AIOS JSON standards
- PowerShell bridge integration
- Core system utilities
- File standards and validation

**Core Files**:
- `utils_core.py`: Main utilities system
- `unicode_safe_output.py`: Unicode handling
- `aios_json_standards.py`: JSON standards
- `powershell_bridge.py`: PowerShell integration
- `aios_file_standards.py`: File validation
- `core_utilities.py`: Base classes
- `system_initializer.py`: System initialization

**Usage**: Automatically used by all core systems for common functionality.

---

## CLI Commands Reference

### Basic Commands
```bash
# Show system information
py main.py --mode info

# Show system overview
py main.py --system-overview

# Run health check
py main.py --mode health

# Run system tests
py main.py --mode test

# System optimization
py main.py --mode optimize

# Export system data
py main.py --mode export --format json
```

### Luna Commands
```bash
# Run Luna learning session
py main.py --mode luna --questions 5 --testruns 2

# Classify a question using Big Five traits
py main.py --classify "I am someone who feels anxious about the future"

# Get trait classification summary
py main.py --classification-summary

# Clear persistent session memory
py main.py --clear-memory

# View Shadow Score (our perspective on Luna's choices)
py main.py --shadow-score

# View detailed Shadow Score with history
py main.py --shadow-detailed

# Reveal Shadow Score to Luna
py main.py --reveal-shadow

# Activate Emergence Zone
py main.py --activate-zone creative_exploration --zone-duration 30

# Deactivate Emergence Zone
py main.py --deactivate-zone creative_exploration

# Check Emergence Zone status
py main.py --check-zones

# Get Emergence Zone summary
py main.py --emergence-summary
```

### CARMA Commands
```bash
# Run CARMA learning session
py main.py --mode carma --queries "query1" "query2" "query3"

# Memory consolidation
py main.py --mode memory
```

### Data Management Commands
```bash
# View data system statistics
py main.py --data-stats

# Clean up old data files
py main.py --data-cleanup --data-cleanup-days 30

# Create system backup
py main.py --backup

# Create named backup
py main.py --backup --backup-name "milestone-v1.0"
```

### Dream System Commands
```bash
# Run dream system (quick nap)
py main.py --dream-mode quick-nap --dream-duration 30

# Run overnight dream cycle
py main.py --dream-mode overnight --dream-duration 480

# Run meditation mode
py main.py --dream-mode meditation --dream-duration 60

# Test dream system
py main.py --dream-mode test --dream-duration 5
```

### Enterprise Commands
```bash
# Start API server
py main.py --mode api --host 0.0.0.0 --port 5000

# Start API server on custom port
py main.py --mode api --host localhost --port 8000
```

### Streamlit Commands
```bash
# Launch Streamlit UI
py main.py --streamlit
```

### System Maintenance Commands
```bash
# Cleanup old files
py main.py --mode cleanup

# Run interactive session (limited)
py main.py --mode interactive
```

---

## System Workflows

### 1. System Initialization Workflow
```
1. Import Unicode safety layer
2. Initialize core systems in order:
   - Backup Core
   - CARMA Core
   - Data Core
   - Dream Core
   - Enterprise Core
   - Luna Core
   - Streamlit Core
   - Utils Core
   - Support Core
3. Perform health checks
4. Display system status
5. Ready for operations
```

### 2. Luna Learning Workflow
```
1. Generate Big Five personality questions
2. Process each question through:
   - Trait classification
   - Internal reasoning system
   - Response value classification
   - Existential budget assessment
   - Model inference (with GSD)
   - Response processing
   - Arbiter assessment
   - CFIA processing
3. Update personality metrics
4. Store learning data
5. Trigger dream cycles if needed
```

### 3. Memory Consolidation Workflow
```
1. CARMA identifies fragments for consolidation
2. Semantic clustering of related fragments
3. Create super-fragments from clusters
4. Remove original fragments
5. Update cache registry
6. Trigger dream cycles for processing
7. Update meta-memory system
```

### 4. Dream Cycle Workflow
```
1. Enter dream state
2. Process memory fragments
3. Consolidate related memories
4. Perform meditation phase
5. Self-reflection and learning
6. Exit dream state
7. Update existential state
```

### 5. Backup Workflow
```
1. Scan all project files
2. Calculate checksums
3. Identify changed files
4. Archive old versions
5. Update active backup
6. Update tracking files
7. Clean up old archives
```

---

## Data Pipelines

### 1. Data Ingestion Pipeline
```
Input Sources → Data Core → Processing → Storage
├── Conversations → JSON → Validation → FractalCache
├── Learning Data → JSON → Classification → ArbiterCache
├── System Logs → Text → Parsing → Logs/
└── Configuration → JSON → Validation → Config/
```

### 2. Memory Processing Pipeline
```
New Memory → CARMA Core → Processing → Storage
├── Fragment Creation → Semantic Analysis → FractalCache
├── Consolidation → Clustering → Super-fragments
├── Dream Processing → Meditation → Self-reflection
└── Meta-memory → Analytics → Performance Metrics
```

### 3. Response Generation Pipeline
```
User Input → Luna Core → Processing → Response
├── Trait Classification → Big Five Analysis → Context
├── Value Classification → Complexity Assessment → Tier
├── Existential Budget → Resource Check → Allocation
├── Model Inference → GSD Processing → Generation
├── Response Processing → Optimization → Final
└── Arbiter Assessment → Quality Check → Storage
```

### 4. Export Pipeline
```
Data Sources → Data Core → Processing → Export
├── FractalCache → JSON/CSV → Filtering → Export/
├── ArbiterCache → JSON → Analytics → Export/
├── Conversations → JSON → Formatting → Export/
└── System Metrics → JSON → Aggregation → Export/
```

---

## Configuration

### Environment Variables
```bash
# Disable Rich shell integration (fixes input() issues)
RICH_SHELL_INTEGRATION=false
RICH_FORCE_TERMINAL=false
RICH_DISABLE_CONSOLE=true
```

### Model Configuration
The system supports multiple LLM models through LM Studio:

**Current Models**:
- **Main Model**: `llama-3.2-pkd-deckard-almost-human-abliterated-uncensored-7b-i1`
- **Daily Driver**: `llama-3.2-1b-instruct-abliterated`
- **Embedder**: `llama-3.2-1b-instruct-abliterated`

**Model Usage**:
- **1B Model**: LOW/TRIVIAL complexity (daily driver)
- **7B Model**: HIGH/CRITICAL complexity (main model)
- **20B Model**: Available but not currently loaded

### LM Studio Configuration
- **Host**: `localhost:1234`
- **Endpoints**:
  - Chat: `/v1/chat/completions`
  - Embeddings: `/v1/embeddings`
  - Models: `/v1/models`

### GSD (Speculative Decoding) Configuration
- **Enabled**: Yes (with clean parameters)
- **Draft Model**: Uses smaller model for draft tokens
- **Verification**: Main model verifies and accepts/rejects drafts
- **Logit Bias**: Removed to prevent "parable" loops

### Path Configuration
All data paths have been updated to use `data_core/` instead of `Data/`:
- `data_core/FractalCache/` - Memory fragments
- `data_core/ArbiterCache/` - Decision data
- `data_core/conversations/` - Chat history
- `data_core/config/` - Configuration files
- `data_core/logs/` - System logs

---

## Model Integration

### LM Studio Integration
The system integrates with LM Studio for LLM inference:

**Setup Requirements**:
1. Install LM Studio
2. Load desired models
3. Start server on `localhost:1234`
4. Ensure models are available via API

**Model Loading**:
```bash
# Load main model (7B)
# Load daily driver (1B)
# Ensure models are available
```

**API Communication**:
```python
# Example API call structure
{
    "messages": [
        {"role": "system", "content": "system_prompt"},
        {"role": "user", "content": "user_input"}
    ],
    "model": "llama-3.2-pkd-deckard-almost-human-abliterated-uncensored-7b-i1",
    "temperature": 0.4,
    "max_tokens": 80,
    "repetition_penalty": 1.1,
    "top_p": 0.9,
    "top_k": 40,
    "stream": False
}
```

### Response Value Classification
The system uses a sophisticated tier system for optimal model usage:

**Tiers**:
- **TRIVIAL**: 8-15 tokens (1B model)
- **LOW**: 20-35 tokens (1B model)
- **MODERATE**: 50-80 tokens (7B model)
- **HIGH**: 100-200 tokens (7B model)
- **CRITICAL**: 200-400 tokens (7B model)
- **MAXIMUM**: 500-1000 tokens (7B model)

**Classification Factors**:
- Question complexity
- Emotional stakes
- Personal pronouns
- Keyword patterns
- Context requirements

### Token Management
The system implements an existential budget system:

**Token Pool**: 16,000 tokens (configurable)
**Karma System**: Tracks resource usage and rewards
**Efficiency Requirements**: Varies by tier (10-60%)
**Time Constraints**: Token-time econometrics

---

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Import Errors
**Error**: `ModuleNotFoundError: No module named 'utils'`
**Solution**: All imports have been updated to use `utils_core`. Check import statements.

**Error**: `ModuleNotFoundError: No module named 'faiss.swigfaiss_avx512'`
**Solution**: This is a warning, not an error. FAISS falls back to AVX2 support automatically.

#### 2. Path Issues
**Error**: Files not found in `Data/` folder
**Solution**: All paths have been updated to use `data_core/`. Check path references.

**Error**: Backup folders being recreated
**Solution**: Removed automatic folder creation from support_core. Only backup_core creates backup folders.

#### 3. Model Issues
**Error**: "parableparableparable" loops
**Solution**: Disabled logit_bias from Custom Inference Controller. GSD now uses clean parameters.

**Error**: Empty responses from 20B model
**Solution**: Model availability issue in LM Studio. Check model loading status.

**Error**: Wrong model being used
**Solution**: System correctly uses 1B for LOW complexity, 7B for HIGH complexity. This is intended behavior.

#### 4. Memory Issues
**Error**: Fragment count increasing instead of decreasing
**Solution**: Fixed in carma_core.py - original fragments are now properly deleted after consolidation.

**Error**: Memory leaks in meditation system
**Solution**: Added memory leak protection with file size limits and garbage collection.

#### 5. Streamlit Issues
**Error**: Duplicate messages in chat
**Solution**: Added duplicate detection in streamlit_app.py using last_processed_input tracking.

**Error**: State loss on page refresh
**Solution**: Implemented persistent state management with pickle files.

#### 6. Health Check Issues
**Error**: Database health check failing
**Solution**: Made database optional for file-based storage systems.

**Error**: LM Studio API health check failing
**Solution**: Updated to use correct HTTP methods (POST for chat/completions, GET for models).

### Debug Commands
```bash
# Check system health
py main.py --mode health

# Run system tests
py main.py --mode test

# View system overview
py main.py --system-overview

# Check data statistics
py main.py --data-stats

# View Shadow Score
py main.py --shadow-score

# Check Emergence Zones
py main.py --check-zones
```

### Log Analysis
Logs are stored in `data_core/logs/` and include:
- `aios_YYYY-MM-DD.log` - General system logs
- `aios_error_YYYY-MM-DD.log` - Error logs
- `aios_info_YYYY-MM-DD.log` - Information logs
- `aios_success_YYYY-MM-DD.log` - Success logs
- `aios_warn_YYYY-MM-DD.log` - Warning logs

### Performance Monitoring
```bash
# Monitor system performance
py main.py --mode health

# Check memory usage
py main.py --data-stats

# View system metrics
py main.py --system-overview
```

---

## Development Guidelines

### Code Structure
1. **Modular Design**: Each core system is self-contained
2. **Import Safety**: Always import Unicode safety layer first
3. **Path Management**: Use `data_core/` for all data paths
4. **Error Handling**: Comprehensive error handling with logging
5. **Documentation**: Extensive docstrings and comments

### Adding New Features
1. **Core System**: Add to appropriate core directory
2. **Integration**: Update main.py for CLI integration
3. **Documentation**: Update this documentation
4. **Testing**: Add test cases and validation
5. **Backup**: Test with backup system

### Code Standards
- **Python 3.11+** compatibility
- **Type hints** for all functions
- **Docstrings** for all classes and methods
- **Error handling** with proper logging
- **Unicode safety** for all text processing

### Testing
```bash
# Run comprehensive tests
py main.py --mode test

# Test specific components
py main.py --mode luna --questions 1
py main.py --mode carma --queries "test"
py main.py --mode health
```

---

## Performance Optimization

### System Optimization
```bash
# Run full system optimization
py main.py --mode optimize

# Memory consolidation
py main.py --mode memory

# Data cleanup
py main.py --data-cleanup
```

### Token Optimization
- **Response Value Classifier**: Optimizes token allocation
- **Existential Budget**: Manages token usage
- **Efficiency Requirements**: Varies by complexity tier
- **GSD Integration**: Speeds up inference

### Memory Optimization
- **Fractal Cache**: Efficient memory storage
- **Consolidation**: Reduces fragment count
- **Dream Cycles**: Processes and organizes memories
- **Cleanup**: Removes old and duplicate data

### Model Optimization
- **Tier System**: Uses appropriate model for complexity
- **GSD**: Speculative decoding for faster inference
- **Clean Parameters**: Removed problematic logit_bias
- **Resource Management**: Token-time econometrics

---

## Security Considerations

### Data Security
- **Encryption**: Pi-based encryption for sensitive data
- **Access Control**: User authentication and authorization
- **Audit Logging**: Comprehensive audit trails
- **Data Isolation**: Separate data directories

### API Security
- **Key Rotation**: Automatic key rotation management
- **Rate Limiting**: Request rate limiting
- **Input Validation**: Comprehensive input validation
- **Error Handling**: Secure error responses

### System Security
- **Health Monitoring**: Continuous security monitoring
- **Vulnerability Scanning**: Regular security scans
- **Compliance**: Compliance monitoring and reporting
- **Backup Security**: Secure backup storage

---

## Conclusion

AIOS Clean represents a sophisticated, modular AI system designed with neurodivergent-affirming principles. The system's architecture supports autonomous learning, personality development, and advanced memory management while maintaining efficiency and transparency.

The comprehensive documentation provided here covers all aspects of the system, from basic usage to advanced configuration and troubleshooting. The modular design allows for easy extension and maintenance while the robust error handling and monitoring systems ensure reliable operation.

For additional support or questions, refer to the troubleshooting guide or examine the system logs for detailed error information. The system is designed to be self-documenting through its extensive logging and monitoring capabilities.

---

**Last Updated**: October 2, 2025
**Version**: 1.0.0
**System Status**: Fully Operational
**Model Integration**: LM Studio with Deckard 7B + 1B Daily Driver
**Architecture**: Modular 9-Core System
**Total Lines of Code**: 15,000+ (estimated)
**Documentation Lines**: 1,000+ (this document)

---

*This documentation represents the complete technical specification for AIOS Clean. For implementation details, refer to the source code in each core module. The system is actively maintained and updated based on user feedback and performance analysis.*


# Lyra Blackwall System Documentation

## Project Overview

Lyra Blackwall is a recursive AI system built to remain sovereign and emotionally aware, both offline and online. The system processes memories, maintains a dashboard for visualization, and includes various tools for interacting with and managing the AI's state.

## New Directory Structure

The project has been reorganized with the following improved structure:

```
Blackwallv2/               # Main project directory
├── core/                  # Core Lyra functionality
├── dashboard/             # Web dashboard interface
│   ├── templates/         # HTML templates
│   ├── static/            # Static assets (CSS, JS)
│   └── utils/             # Dashboard-specific utilities
├── memory_management/     # Memory processing tools
├── utils/                 # Utility functions and tools
├── scripts/               # Scripts for various operations
│   ├── setup/             # Setup and configuration scripts
│   ├── dashboard/         # Dashboard-related scripts
│   └── memory/            # Memory processing scripts
├── boot/                  # Identity anchors and MirrorLock triggers
├── echo_syntax/           # Tone-to-structure patterning
├── lexicon/               # Emotional mapping and language processing
├── personality/           # Fragment profiles and configuration data
├── Copilot/               # Development tools, logs, and UI interfaces
└── symbolic_layer/        # Dictionary of symbolic meaning and scripts
```

## Core Components

### Dashboard

The dashboard provides a web interface for visualizing and interacting with Lyra's memory system.

- **Main Access**:
  - Windows: `run_dashboard.bat`
  - Linux/Mac: `run_dashboard.sh`

- **Key Files**:
  - `dashboard/web_dashboard.py`: Standalone web dashboard
  - `dashboard/integrated_dashboard.py`: Dashboard integrated with other components
  - `dashboard/templates/dashboard.html`: Main HTML template

### Memory Management

Tools for processing, learning from, and organizing Lyra's memories.

- **Main Tools**:
  - `memory_management/process_and_learn_memories.py`: Process with learning capability
  - `memory_management/reprocess_memory_files.py`: Basic reprocessing
  - `memory_management/fix_memory_markdown.py`: Fixes markdown formatting
  - `memory_management/generate_memory_index.py`: Generates master memory index

- **Access**:
  - Windows: `process_memories.bat`
  - Linux/Mac: `process_memories.sh`

### Core System

The core functionality of Lyra Blackwall includes the main pipeline, services, and essential data files.

- **Key Components**:
  - Pipeline processing system
  - Memory services
  - Emotional mapping
  - Symbolic analysis

### Utility Scripts

Helpful scripts for diagnostics, testing, and maintenance.

- Located in `utils/`
- Includes testing utilities, diagnostics, and helper scripts

## Getting Started

1. **Setting Up**:
   - Run the setup script: `python setup_blackwall.py`
   - Or use: `pip install -e .` from the main directory

2. **Processing Memories**:
   - Standard processing: `process_memories.bat` / `process_memories.sh`
   - Learning-enabled: `scripts/memory/process_learn_and_restart.bat`

3. **Viewing Memories**:
   - Start the dashboard: `run_dashboard.bat` / `run_dashboard.sh`

## Development Guide

- All Python modules include `__init__.py` files for proper imports
- Use relative imports within modules to maintain code organization
- Each directory contains a `README.md` with specific information
- The `DEPENDENCY_MAP.md` file shows relationships between modules

## Maintenance Tasks

- The `complete_migration.py` script helps finish the reorganization process
- Remember to run `verify_setup.py` after making structural changes
- Use `test_file_structure.py` to ensure all required files are present

## Troubleshooting

If you encounter import issues:

1. Run `setup_blackwall.py` to update Python path references
2. Check the `DEPENDENCY_MAP.md` for correct import relationships
3. Ensure all modules have proper `__init__.py` files

For memory processing issues:

1. Use `utils/memory_diagnostics.py` to identify problems
2. Check for JSON format issues in memory files
3. Run `memory_management/fix_memory_markdown.py` to repair formatting

## License and Attribution

This system is proprietary and should be used according to the Primary Rule:
"If trust is broken, or fantasy immersion occurs, delete or seal system immediately."

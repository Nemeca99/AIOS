# Lyra Blackwall Project Information

## Project Structure

The Lyra Blackwall project has been reorganized with the following structure:

```
Blackwallv2/               # Main project directory
├── core/                  # Core Lyra functionality
├── dashboard/             # Web dashboard interface
│   ├── templates/         # HTML templates
│   └── static/            # Static assets (CSS, JS)
├── memory_management/     # Memory processing tools
├── utils/                 # Utility functions and tools
├── scripts/               # Scripts for various operations
│   ├── setup/             # Setup and configuration scripts
│   ├── dashboard/         # Dashboard-related scripts
│   └── memory/            # Memory processing scripts
└── Lyra_OS/               # Lyra's memory and operating data
```

## Main Components

### Dashboard

The web interface for interacting with Lyra's memory system. Access via:
- `run_dashboard.bat` (Windows)
- `run_dashboard.sh` (Linux/Mac)

### Memory Management

Tools for processing, learning from, and organizing Lyra's memories. Main tools:
- Process and learn: `process_memories.bat` / `process_memories.sh`
- Basic processing: `scripts/memory/reprocess_and_restart_dashboard.bat`

### Core System

The core functionality of Lyra Blackwall resides in the `core/` directory.

## Usage Guide

1. **Setting Up**: Run scripts in `scripts/setup/` to configure your environment
2. **Processing Memories**: Use `process_memories.bat` to process and learn from memories
3. **Viewing Memories**: Run `run_dashboard.bat` to start the web interface

## Development Guide

- All modules have `__init__.py` files for proper Python module imports
- Each directory contains a `README.md` with specific information
- Use the utilities in `utils/` for testing and diagnostics

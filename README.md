# AIOS Clean - Experimental AI System

An experimental modular AI system exploring personality simulation, memory management, and response optimization through component separation.

## Overview

This project represents an exploration into modular AI architecture, investigating whether complex AI systems can be decomposed into interchangeable components. The system consists of multiple independent modules that can theoretically be swapped or combined in different configurations.

## Experimental Components

### Core Modules
- **Luna Core**: An experimental personality simulation system
- **CARMA Core**: A memory retrieval and management system
- **Data Core**: Data storage and management utilities
- **Dream Core**: Memory consolidation and processing experiments
- **Support Core**: System monitoring and utility functions

### Additional Modules
- **Backup Core**: File backup and versioning system
- **Enterprise Core**: API and business logic experiments
- **Streamlit Core**: Web interface experiments
- **Utils Core**: Shared utility functions

## Theoretical Approach

The system explores several theoretical concepts:

1. **Modular Architecture**: Whether AI systems can be built with truly independent components
2. **Memory Systems**: Different approaches to conversation memory and retrieval
3. **Personality Modeling**: Experimental personality trait integration
4. **Response Classification**: Tier-based response routing for efficiency
5. **Component Interchangeability**: Whether different implementations can share interfaces

## Current Status

This is an experimental system under active development. Results are preliminary and should be considered theoretical explorations rather than production-ready implementations.

## Requirements

- Python 3.11+
- LM Studio (for local LLM inference)
- Various Python packages (see requirements.txt)

## Usage

```bash
# Basic system information
python main.py --mode info

# Experimental personality interaction
python main.py --luna --chat "hello"

# Memory system exploration
python main.py --carma --learn
```

## Modularity Experiments

The system includes experiments testing component independence:

- **Simple RAG**: A basic RAG implementation for comparison
- **Hybrid Architecture**: Python/Rust integration experiments
- **Layer Testing**: Systematic testing of component combinations

## Research Applications

This system may be useful for:
- Studying modular AI architectures
- Comparing different memory retrieval approaches
- Exploring personality modeling techniques
- Testing component interchangeability theories

## Limitations

- Experimental and research-oriented
- Not production-ready
- Limited testing on different environments
- Theoretical implementations may not scale

## Contributing

This is primarily a research project. Contributions that help explore the theoretical concepts are welcome.

## License

MIT License - see LICENSE file for details.

---

**Note**: This system is experimental. Results and behaviors should be interpreted as preliminary research findings rather than established capabilities.
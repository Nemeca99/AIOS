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

## Quick Operations

### Model Management
```bash
# Show all model configurations
python main.py --system --show-models

# Check configuration health
python main.py --system --config-health

# Show exact model triplet for Luna
python main.py --system --luna --whoami

# Change Luna's main model
python main.py --system --luna --modchange --main --model-name "qwen/qwen3-4b-thinking-2507 Q8_0"

# Change Luna's speculative decoding model
python main.py --system --luna --modchange --sd --model-name "new-sd-model"

# Run with real LLM calls (default)
python main.py --execution-mode real --system --luna --message "hello"

# Run with mock responses (for testing)
python main.py --execution-mode mock --system --luna --message "hello"
```

### Testing & Validation
```bash
# Run smoke tests
python smoke_test.py

# Run golden prompts regression tests
python main.py --test-suite --golden --report data_core/analytics/golden_report.json

# Run deterministic golden tests with provenance
python main.py --execution-mode real --deterministic --test-suite --golden --report results.json

# Update all config files with schema versioning
python update_config_schema.py

# Cross-architecture benchmark (LLaMA, Qwen, Phi)
python cross_arch_benchmark.py

# Irrefutable one-screen demo
python demo_irrefutable.py

# Generate publication-ready results from provenance logs
python provenance_to_results.py --input data_core/analytics/provenance.ndjson --outdir analytics_out

# Generate complete paper from template + results
python generate_paper.py --results analytics_out/RESULTS.md --template PAPER_METHODS_RESULTS.md --output AIOS_Clean_Paper.md
```

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

## Publication-Ready Results

The system automatically generates publication-ready results from provenance logs:

```bash
# 1. Run deterministic golden tests (generates provenance.ndjson)
python main.py --execution-mode real --deterministic --test-suite --golden --report results.json

# 2. Convert provenance to publication tables
python provenance_to_results.py --input data_core/analytics/provenance.ndjson --outdir analytics_out

# 3. Generate complete paper from template + results
python generate_paper.py --results analytics_out/RESULTS.md --template PAPER_METHODS_RESULTS.md --output AIOS_Clean_Paper.md

# 4. Your publication-ready paper is ready!
cat AIOS_Clean_Paper.md
```

**Generated outputs:**
- `summary_by_arch_layer_backend.csv` - Latency percentiles, accept rates, token counts
- `routing_accuracy.csv` - Tier routing accuracy by architecture  
- `RESULTS.md` - Auto-generated tables ready for papers

## Contributing

This is primarily a research project. Contributions that help explore the theoretical concepts are welcome.

## Irrefutable Proof Checklist

✅ **Model Verification:**
- `python main.py --system --luna --whoami` shows {main, embedder, sd} + hashes + quant

✅ **Configuration Health:**
- `python main.py --system --config-health` passes schema v1 for all cores

✅ **Deterministic Testing:**
- `python main.py --execution-mode real --deterministic --test-suite --golden` passes with provenance lines

✅ **Execution Mode:**
- `execution_mode=real` watermark present in all outputs
- Mock mode fails loudly when used with golden tests

✅ **Traceability:**
- `git_rev` present in every provenance block
- NDJSON provenance log in `data_core/analytics/provenance.ndjson`

## License

MIT License - see LICENSE file for details.

---

**Note**: This system is experimental. Results and behaviors should be interpreted as preliminary research findings rather than established capabilities.
# CARMA Core Module

**Cognitive Adaptive Recursive Memory Architecture**

Version 2.0.0 - Refactored Modular Structure

## Overview

The CARMA Core module is a sophisticated cognitive memory system that implements fractal caching, autonomous goal generation, meta-memory management, and performance optimization for AI systems.

## Module Structure

```
carma_core/
├── __init__.py                 # Module initialization and exports
├── carma_core.py              # Main CARMA System orchestrator
├── core/                       # Core component modules
│   ├── __init__.py
│   ├── fractal_cache.py       # Fractal Mycelium Cache with Psycho-Semantic RAG
│   ├── executive_brain.py     # Autonomous goal generation and execution
│   ├── meta_memory.py         # Hierarchical memory management
│   ├── performance.py         # 100% Performance system with dream cycles
│   ├── mycelium_network.py    # Network infrastructure and user management
│   ├── compressor.py          # Advanced memory compression
│   ├── clusterer.py           # Memory clustering system
│   └── analytics.py           # Memory analytics and insights
├── implementations/            # Alternative implementations
│   ├── __init__.py
│   ├── fast_carma.py          # Fast keyword-based CARMA
│   └── hybrid_carma.py        # Python-Rust hybrid implementation
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── fragment_decayer.py    # Time-based fragment decay system
│   ├── memory_quality.py      # Memory deduplication and quality scoring
│   └── model_config.py        # Model configuration utilities
├── rust_carma/                 # Rust implementation (Python-Rust bridge)
│   ├── Cargo.toml
│   ├── Cargo.lock
│   └── src/
│       └── lib.rs
├── config/                     # Configuration and cache files
│   ├── model_config.json
│   └── embedder_cache/
└── extra/                      # Extra files (scripts, etc.)
    └── start_meditation.ps1
```

## Core Components

### FractalMyceliumCache
- Fractal cache with Psycho-Semantic RAG Loop integration
- Embedding-based similarity search
- Tool-augmented retrieval using Llama-3.2-1B
- Big 5 personality analysis
- Ava behavioral pattern matching
- Minecraft chat efficiency patterns

### CARMAExecutiveBrain
- Autonomous goal generation based on system metrics
- Goal execution (cross-linking, eviction, reinforcement, super-fragments)
- System optimization actions

### CARMAMetaMemory
- Episodic memory creation and management
- Semantic memory consolidation
- Hierarchical memory structures

### CARMA100PercentPerformance
- Performance monitoring and optimization
- Dream cycle for memory consolidation
- Super-fragment creation from clusters

### CARMAMyceliumNetwork
- Internal network infrastructure
- User connection management
- Traffic monitoring

### CARMAMemoryCompressor
- Advanced memory compression algorithms
- Space optimization

### CARMAMemoryClusterer
- Memory fragment clustering
- Pattern organization

### CARMAMemoryAnalytics
- Memory system analysis
- Performance insights
- Optimization recommendations

## Usage

### Basic Usage

```python
from carma_core import CARMASystem

# Initialize CARMA system
carma = CARMASystem(base_dir="data_core/FractalCache")

# Process a query
result = carma.process_query("What is consciousness?")

# Get system statistics
stats = carma.get_comprehensive_stats()
print(f"Performance: {stats['performance_level']:.1f}%")
print(f"Fragments: {stats['cache']['total_fragments']}")
```

### Advanced Features

```python
# Compress memories
compression_result = carma.compress_memories('semantic')

# Cluster memories
cluster_result = carma.cluster_memories(num_clusters=5)

# Analyze memory system
analysis = carma.analyze_memory_system()

# Optimize memory system
optimization = carma.optimize_memory_system()
```

### Using Alternative Implementations

```python
from carma_core.implementations import FastCARMA, HybridCarmaCore

# Use fast keyword-based search
fast_carma = FastCARMA()
result = fast_carma.process_query("test query")

# Use Python-Rust hybrid
hybrid = HybridCarmaCore()
result = hybrid.process_query("test query")
```

### Using Utilities

```python
from carma_core.utils import FragmentDecayer, MemoryQualityScorer

# Apply fragment decay
decayer = FragmentDecayer()
decay_result = decayer.apply_decay(dry_run=True)

# Score memory quality
scorer = MemoryQualityScorer()
duplicates = scorer.find_duplicates(fragments)
```

## Architecture Principles

1. **Modular Design**: Each component is self-contained and can be used independently
2. **Central Orchestration**: `carma_core.py` serves as the main linker between components
3. **No Cross-Dependencies**: Components only reference the main core file, not each other
4. **Type-Safe**: Uses forward references and TYPE_CHECKING to avoid circular imports
5. **Extensible**: Easy to add new implementations or utilities

## Integration with Main System

The CARMA Core module is designed to integrate with the main AIOS system:

```python
# From F:\AIOS_Clean\main.py
from carma_core import CARMASystem

# Initialize as part of Luna's cognitive system
luna.carma = CARMASystem()
```

## Configuration

Model configuration is managed through `config/model_config.json`:
- Main LLM for complex queries
- Embedder model for similarity search
- Draft model for speculative decoding

## Performance

- Fast keyword-based search: < 1 second
- Embedding-based search: 1-3 seconds
- Memory consolidation (dream cycle): 2-5 seconds
- Supports 1000+ memory fragments efficiently

## Dependencies

- Python 3.9+
- NumPy
- Support modules: `support_core`, `utils_core`
- Optional: Rust toolchain for `rust_carma`

## Notes

- All cache files in `config/embedder_cache/` are preserved
- Rust implementation provides performance optimization
- Fast implementations available for time-critical applications
- Psycho-Semantic RAG Loop enhances personality-aware responses

## Version History

- **2.0.0**: Modular refactor - broke apart monolithic file into organized components
- **1.x**: Original monolithic implementation

## Author

Part of the AIOS (Artificial Intelligence Operating System) project


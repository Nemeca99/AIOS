# CARMA Minimal Reference Implementation

This is a minimal, runnable implementation of the core CARMA concepts for demonstration and reproducibility.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python test_demo.py
```

## What This Demonstrates

- Fragment creation and management
- Fractal splitting when fragments exceed size thresholds
- Semantic cross-linking based on tag similarity and embeddings
- Simple eviction policies based on hit counts
- Dijkstra pathfinding through the fragment network

## Files

- `fragments.py` - Core Fragment data structure
- `cache.py` - CarmaCache with splitting and eviction
- `pathfinding.py` - Dijkstra shortest path algorithm
- `semantic.py` - Embedding and cross-linking utilities
- `test_demo.py` - Demonstration script

## Expected Output

The demo will show:
- Fragment creation and growth
- Splitting events when large fragments are added
- Cross-linking between similar fragments
- Final fragment statistics (count, sizes, levels, hits)

This is a simplified version of the full CARMA system for educational and reproducibility purposes.

# CARMA Experiments

This directory contains diagnostic and testing scripts for the CARMA consciousness system.

## Quick Start

1. **Health Check**: `python experiments/simple_health_check.py`
2. **Build Embeddings**: `python experiments/ensure_embeddings.py`
3. **Test Deep Sleep**: `python experiments/run_deep_sleep_once.py --force`
4. **Collect Metrics**: `python experiments/collect_metrics.py`

## Scripts

### `simple_health_check.py`
Quick diagnostic script to check system status:
- Fragment count and embedding status
- Index build status
- Retrieval functionality
- Consciousness system status
- Deep sleep readiness

### `ensure_embeddings.py`
Builds embeddings and FAISS index for all fragments:
- Processes all fragments in cache
- Generates missing embeddings
- Builds FAISS index for retrieval
- Verifies index functionality
- Saves updated cache

### `run_deep_sleep_once.py`
Tests deep sleep functionality:
- Verifies embeddings and index are ready
- Runs single deep sleep cycle
- Tests superfragment creation
- Validates system after deep sleep
- Use `--force` to override message count requirements

### `collect_metrics.py`
Analyzes system logs and generates reports:
- Parses JSON log files
- Generates CSV reports
- Creates health analysis
- Provides recommendations
- Outputs to `reports/` directory

## Usage Examples

### Basic Health Check
```bash
python experiments/simple_health_check.py
```

### Build System for Deep Sleep
```bash
# 1. Check system status
python experiments/simple_health_check.py

# 2. Build embeddings and index
python experiments/ensure_embeddings.py

# 3. Test deep sleep
python experiments/run_deep_sleep_once.py --force
```

### Run Long Test and Collect Metrics
```bash
# 1. Build system
python experiments/ensure_embeddings.py

# 2. Run long test
# Cognitive context enabled by default
python HiveMind/luna_main.py --mode real_learning --questions 1000 --logdir logs/overnight_run

# Disable cognitive context
python HiveMind/luna_main.py --mode real_learning --questions 1000 --logdir logs/overnight_run --disable_cognitive

# 3. Collect metrics
python experiments/collect_metrics.py --logdir logs/overnight_run --output reports/overnight_run
```

## Troubleshooting

### "No embeddings present - index not built"
```bash
python experiments/ensure_embeddings.py
```

### "No fragments in cache"
```bash
python HiveMind/seed_carma_cache.py --dir ./seed_corpus --limit 100
```

### "Not enough messages for deep sleep"
```bash
python experiments/run_deep_sleep_once.py --force
```

### "No superfragments created"
1. Check embeddings: `python experiments/simple_health_check.py`
2. Build index: `python experiments/ensure_embeddings.py`
3. Lower similarity threshold in config
4. Increase fragment diversity

## Output Files

- `reports/metrics_summary.csv` - Overall system metrics
- `reports/timings.csv` - Per-message timing data
- `reports/token_usage.csv` - Token consumption data
- `reports/cache_metrics.csv` - Cache performance data
- `reports/dream_log.csv` - Deep sleep cycle data

## Configuration

The scripts use the same configuration as the main CARMA system:
- `luna_carma_integration/carma_cache.json` - Fragment cache
- `config.yaml` - System configuration
- `logs/` - Log files directory

## Safety

- All scripts are read-only by default
- Use `--force` flags carefully
- Always backup cache before major changes
- Check logs for errors before proceeding

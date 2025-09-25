# Blackwall Pipeline - Optimized for Continuous Operation

This repository contains the Blackwall lexicon pipeline with optimizations for continuous operation, memory management, and performance monitoring.

## Features

- **Emotion Analysis**: Maps text to emotional profiles using lexicon and thesaurus
- **Fragment-Based Response Styling**: Personality fragments with weighted influence
- **Blend Support**: Dynamic blending of multiple fragments for richly styled responses
- **Continuous Operation**: Optimized for long-running sessions with resource management
- **Adaptive Timing**: Dynamically adjusts processing cycles based on system load
- **Performance Monitoring**: Tracks memory, CPU, and disk usage

## Getting Started

### Installation

1. Set up Python dependencies:

```bash
python setup_blackwall.py
```

2. Verify the installation:

```bash
python test_blackwall_pipeline.py
```

### Directory Structure

```
/core/               # Core optimized implementation
  blackwall_pipeline.py     # Main pipeline with optimizations
  continuous_config.json    # Configuration for continuous operation
  lexicon_service.py        # Lexicon processing service
  
/lexicon/            # Legacy and utility scripts
  blackwall_pipeline.py     # Updated with optimizations from core
  auto_weight_lexicon.py    # Tools for weight management
  left_hemisphere_master.json    # Lexicon master index
  right_hemisphere_master.json   # Thesaurus master index
  stopwords.txt             # Common words to filter out
  
fragment_*.json      # Fragment and blend definitions
```

## Usage

### Basic Usage

```python
from lexicon.blackwall_pipeline import BlackwallPipeline, load_all_personality_data

# Load personality data
fragments, blends = load_all_personality_data()

# Initialize the pipeline
pipeline = BlackwallPipeline(
    "core/left_hemisphere_master.json",
    "core/right_hemisphere_master.json",
    "lexicon/stopwords.txt",
    fragments=fragments
)

# Process text
result = pipeline.process("I feel happy today")
print(result["styled_response"])
```

### Running in Continuous Mode

```bash
python lexicon/blackwall_pipeline.py
```

### Running a Simple Example

```bash
python lexicon/blackwall_pipeline.py example
```

## Configuration

The continuous operation features can be configured in `core/continuous_config.json`:

```json
{
  "cycle_interval": 10,
  "memory_threshold": 80,
  "cpu_threshold": 90,
  "log_buffer_size": 20,
  "cleanup_frequency": 50,
  "adaptive_timing": true,
  "performance_log_frequency": 10,
  "batch_size": 1000
}
```

See `core/CONTINUOUS_OPERATION.md` for detailed documentation on the optimization features.

## Testing

Run the verification script to test all optimizations:

```bash
python test_blackwall_pipeline.py
```

## Logs and Monitoring

Performance logs and pipeline output are saved to:

- Copilot/BLACKWALL_LOGS.md - Main log for all pipeline activity
- chat_logs/BLACKWALL_LEXICON_LOG.md - Lexicon-specific logs
- chat_logs/BLACKWALL_THESAURUS_LOG.md - Thesaurus processing logs
- chat_logs/BLACKWALL_FEEDBACK_LOG.md - Feedback and weight adjustment logs

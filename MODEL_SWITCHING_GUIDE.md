# AIOS Clean Model Switching Guide

## Quick Model Switch

To switch the main model in AIOS Clean, edit the configuration file:

**File**: `luna_core/config/model_config.json`

**Change this line**:
```json
"name": "current-model-name-here"
```

**To**:
```json
"name": "your-new-model-name"
```

## Detailed Steps

### 1. Update Model Configuration
```bash
# Edit the model config file
nano luna_core/config/model_config.json
```

### 2. Update Both Fields
Make sure to update **both** the main model name and the current_main reference:

```json
{
  "models": {
    "main_llm": {
      "name": "your-new-model-name",  // ← Change this
      "type": "main_model",
      "description": "Primary LLM for complex queries and responses",
      "tier": "high_complexity",
      "api_endpoint": "http://localhost:1234/v1/chat/completions"
    }
  },
  "model_switching": {
    "current_main": "your-new-model-name"  // ← And this
  }
}
```

### 3. Verify Model is Loaded in LM Studio
- Ensure your new model is loaded and running in LM Studio
- Check that the model name matches exactly (including quantization info)
- Verify the API endpoint is accessible at `http://localhost:1234`

### 4. Test the New Model
```bash
# Run a quick benchmark test
py main.py --luna --benchmark
```

### 5. Verify Results
- Check the benchmark output for the new model name
- Verify response quality and latency
- Compare with previous model results

## Model Naming Examples

### Qwen Models
```json
"name": "qwen2.5-coder-7b-instruct@q4_k_m"
"name": "qwen2.5-7b-instruct@q4_k_m"
"name": "qwen2.5-14b-instruct@q4_k_m"
```

### Llama Models
```json
"name": "llama-3.2-pkd-deckard-almost-human-abliterated-uncensored-7b-i1"
"name": "llama-3.2-7b-instruct@q4_k_m"
"name": "llama-3.2-3b-instruct@q4_k_m"
```

### Other Models
```json
"name": "codellama-7b-instruct@q4_k_m"
"name": "mistral-7b-instruct@q4_k_m"
"name": "phi-3-medium-4k-instruct@q4_k_m"
```

## Troubleshooting

### Model Not Found Error
- **Check**: Model name matches exactly in LM Studio
- **Check**: Model is loaded and running
- **Check**: API endpoint is accessible

### Performance Issues
- **Check**: Model quantization level (higher = better quality, slower)
- **Check**: Available system resources
- **Check**: LM Studio server status

### Speculative Decoding Issues
- **Check**: Draft model compatibility
- **Check**: Both main and draft models loaded
- **Check**: LM Studio speculative decoding settings

## Benchmark Comparison

After switching models, run a benchmark to compare performance:

```bash
# Run full benchmark
py main.py --luna --benchmark

# Results saved to: benchmark_raw_dump_TIMESTAMP.json
```

Compare with previous results in `MODEL_BENCHMARK_RESULTS.md`.

## Model Recommendations

### For Coding Tasks
- **Qwen2.5 Coder 7B**: Excellent technical performance
- **CodeLlama 7B**: Strong coding capabilities
- **DeepSeek Coder**: Advanced code generation

### For General Conversation
- **Llama 3.2 7B**: Rich personality responses
- **Qwen2.5 7B**: Balanced performance
- **Mistral 7B**: Fast and efficient

### For Speed
- **Qwen2.5 3B**: Fast inference
- **Phi-3 Mini**: Very fast, good quality
- **Llama 3.2 3B**: Fast with good personality

---
*Last Updated: 2025-10-03*
*AIOS Clean Model Management System*

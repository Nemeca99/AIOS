# CLI FRAMEWORK IMPLEMENTATION GUIDE
**Complete Command-Line Interface for Luna Master Framework**  
**Version:** 2.0.0-master  
**Implementation Date:** September 19, 2025  
**Total Parameters:** 20+ configurable options  

## 🚀 QUICK START GUIDE

### Basic Usage
```bash
# Default test (recommended for most users)
python luna_master_test.py

# Standard personality evaluation
python luna_master_test.py --questions 10 --tokens 2000 --temp 0.8

# Quick single question test
python luna_master_test.py --questions 1 --tokens 1000
```

### Help System
```bash
# View all options and examples
python luna_master_test.py --help

# View parameter ranges and validation rules
python luna_master_test.py --help | grep -A 5 -B 5 "default"
```

---

## 🎯 COMPLETE PARAMETER REFERENCE

### Core Test Configuration
```bash
--mode {raw_llm,luna_personality,luna_with_memory}
    Test mode selection (default: luna_with_memory)
    
--questions QUESTIONS  
    Number of questions to test, 1-120 (default: 10)
    
--testruns TESTRUNS
    Number of consecutive test runs, 1-20 (default: 1)
    
--model MODEL
    Specific model name (auto-detect if not provided)
```

### LLM Parameters (Complete Control)
```bash
--tokens TOKENS
    Max tokens, 50-8192 (default: 2000)
    OPTIMAL: 1800-2000 for personality expression
    
--temp TEMP
    Temperature 0.0-2.0 (default: 0.7)  
    OPTIMAL: 0.8-0.9 for creativity/consistency balance
    
--top_p TOP_P
    Top-p nucleus sampling 0.0-1.0 (default: 0.9)
    
--top_k TOP_K
    Top-k sampling (default: 40)
    
--freq_penalty FREQ_PENALTY
    Frequency penalty -2.0 to 2.0 (default: 0.0)
    
--presence_penalty PRESENCE_PENALTY  
    Presence penalty -2.0 to 2.0 (default: 0.0)
    
--repeat_penalty REPEAT_PENALTY
    Repeat penalty (default: 1.1)
    
--min_p MIN_P
    Min-p sampling (default: 0.0)
```

### Advanced Testing Options
```bash
--fixed_questions
    Use same questions for all runs (reproducible research)
    
--seed SEED
    Random seed for reproducible sampling
    
--timeout TIMEOUT
    Request timeout in seconds (default: 300)
    
--delay DELAY  
    Delay between questions in seconds (default: 2.0)
    
--run_delay RUN_DELAY
    Delay between test runs in seconds (default: 1.0)
```

### Output Control
```bash
--output_dir OUTPUT_DIR
    Custom output directory for results
    
--prefix PREFIX
    Custom filename prefix for results
    
--quiet
    Minimal output (just results)
    
--verbose
    Verbose output with detailed metrics
```

---

## 📊 PARAMETER OPTIMIZATION GUIDE

### Recommended Configurations

#### Standard Research Configuration
```bash
python luna_master_test.py \
  --tokens 1800 \
  --temp 0.8 \
  --questions 10 \
  --testruns 3 \
  --verbose
```

#### Quick Testing Configuration
```bash
python luna_master_test.py \
  --tokens 1000 \
  --temp 0.7 \
  --questions 5 \
  --delay 1.0
```

#### Comprehensive Analysis Configuration
```bash
python luna_master_test.py \
  --tokens 2000 \
  --temp 0.8 \
  --questions 20 \
  --testruns 5 \
  --verbose \
  --output_dir comprehensive_results
```

#### Reproducible Research Configuration
```bash
python luna_master_test.py \
  --fixed_questions \
  --seed 12345 \
  --tokens 1800 \
  --temp 0.8 \
  --questions 15 \
  --testruns 10
```

### Parameter Selection Guidelines

#### Token Count Selection
- **50-500:** Minimal responses, testing only
- **500-1000:** Basic personality expression
- **1000-1500:** Good personality expression  
- **1500-2000:** Optimal personality expression ⭐
- **2000+:** Diminishing returns, slower responses

#### Temperature Selection  
- **0.1-0.4:** Very conservative, repetitive
- **0.5-0.6:** Conservative, consistent
- **0.7-0.8:** Balanced creativity/consistency ⭐
- **0.8-0.9:** High creativity, good consistency ⭐
- **0.9+:** Maximum creativity, potential inconsistency

#### Question Count Selection
- **1-3:** Rapid testing, high variance
- **5-8:** Quick assessment, moderate variance
- **8-15:** Optimal balance, reliable results ⭐
- **15-30:** Comprehensive assessment
- **30+:** Research-grade, time-intensive

#### Test Run Selection
- **1:** Single test, quick results
- **2-3:** Basic validation, variance check
- **3-5:** Statistical validation ⭐
- **5-10:** Research-grade validation
- **10+:** Comprehensive statistical analysis

---

## 🔬 ADVANCED USAGE PATTERNS

### Batch Testing Workflows

#### Token Optimization Series
```bash
# Test different token counts systematically
for tokens in 1000 1500 1800 2000; do
  python luna_master_test.py \
    --tokens $tokens \
    --testruns 3 \
    --questions 10 \
    --prefix "token_opt_${tokens}"
done
```

#### Temperature Sweep Analysis
```bash
# Test temperature range systematically  
for temp in 0.5 0.7 0.8 0.9; do
  python luna_master_test.py \
    --temp $temp \
    --tokens 1800 \
    --testruns 3 \
    --questions 10 \
    --prefix "temp_sweep_${temp}"
done
```

#### Model Comparison Study
```bash
# Compare different test modes
python luna_master_test.py --mode raw_llm --testruns 3 --prefix "raw"
python luna_master_test.py --mode luna_personality --testruns 3 --prefix "luna"  
python luna_master_test.py --mode luna_with_memory --testruns 3 --prefix "luna_mem"
```

### Research Validation Workflows

#### Reproducibility Testing
```bash
# Run same configuration multiple times with fixed seed
python luna_master_test.py \
  --fixed_questions \
  --seed 42 \
  --tokens 1800 \
  --temp 0.8 \
  --questions 15 \
  --testruns 5 \
  --prefix "reproducibility_test"
```

#### Statistical Significance Testing
```bash
# Large sample for statistical validity
python luna_master_test.py \
  --tokens 2000 \
  --temp 0.8 \
  --questions 50 \
  --testruns 10 \
  --verbose \
  --prefix "statistical_validation"
```

#### Performance Benchmarking
```bash
# Speed vs quality trade-off analysis
python luna_master_test.py --tokens 500 --questions 20 --prefix "speed_test"
python luna_master_test.py --tokens 1000 --questions 20 --prefix "balanced_test"
python luna_master_test.py --tokens 2000 --questions 20 --prefix "quality_test"
```

---

## 🛠️ IMPLEMENTATION DETAILS

### Command Line Parsing Architecture
```python
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Luna Master Test Framework - Complete Variable Control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""EXAMPLES: [comprehensive examples provided]"""
    )
    
    # Parameter groups
    # - Test configuration
    # - LLM parameters  
    # - Advanced options
    # - Output control
    
    # Validation logic
    # - Range checking
    # - Type validation
    # - Dependency validation
```

### Dynamic Parameter Integration
```python
def __init__(self, custom_params=None, custom_config=None):
    # Default parameters
    default_params = {
        "temperature": 0.7,
        "max_tokens": 2000,
        # ... all parameters
    }
    
    # Override with CLI values
    self.params = custom_params if custom_params else default_params
    self.config = custom_config if custom_config else default_config
```

### Real-time Display Updates
```python
def run_master_test(self, ...):
    print(f"⚡ Enhanced: {self.params['max_tokens']} tokens for full personality expression")
    print(f"🌡️ Temperature: {self.params['temperature']}, Top-p: {self.params['top_p']}")
    
    if self.config.get('verbose', False):
        print(f"🔧 Advanced: Top-k: {self.params.get('top_k', 40)}")
        print(f"⏱️ Timing: Timeout: {self.config.get('timeout', 300)}s")
```

---

## 🎨 OUTPUT FORMATS AND ANALYSIS

### Standard Output Format
```
🌙 LUNA MASTER TEST - COMPLETE CLI CONTROL
============================================================
🎯 Mode: luna_with_memory
❓ Questions: 10 (from 120 Big Five)
🔄 Test Runs: 3
⚙️ Tokens: 1800, Temp: 0.8, Top-p: 0.9
🎲 Fixed Questions: False
============================================================

🔬 RUN 1/3
------------------------------
🌙 LUNA MASTER TEST FRAMEWORK
============================================================
🎯 Mode: Luna With Memory
📊 Industry Standard: Random 10/120 Big Five questions
⚡ Enhanced: 1800 tokens for full personality expression
🌡️ Temperature: 0.8, Top-p: 0.9
🔢 Scoring: Industry 1-5 Likert scale + Luna metrics
⏰ Started: 04:42:11
============================================================
```

### Verbose Output Additions
```
🔧 Advanced: Top-k: 40, Freq: 0.0, Presence: 0.0
⏱️ Timeout: 300s, Delay: 2.0s, Run Delay: 1.0s
```

### Quiet Output Format
```
3.82/5 (avg), 14.2s (time), 100.0% (success)
```

### Result File Naming Convention
```
luna_master_{mode}_{model}_{avg_score}avg_{timestamp}.json
luna_master_{mode}_{model}_{avg_score}avg_{timestamp}.md

Examples:
- luna_master_luna_with_memory_wizardlm-2-7b-abliterated_q8_0_3.82avg_20250919_043302.json
- luna_master_raw_llm_wizardlm-2-7b-abliterated_q8_0_4.05avg_20250919_044846.json
```

---

## 🔍 TROUBLESHOOTING GUIDE

### Common Issues and Solutions

#### Timeout Errors
```bash
# Problem: Request timed out
# Solution: Increase timeout
python luna_master_test.py --timeout 600

# Problem: Model taking too long
# Solution: Reduce tokens or increase delay
python luna_master_test.py --tokens 1000 --delay 3.0
```

#### Memory Issues
```bash
# Problem: Out of memory
# Solution: Reduce batch size
python luna_master_test.py --questions 5 --testruns 2

# Problem: Too many files
# Solution: Use custom output directory
python luna_master_test.py --output_dir limited_results
```

#### Consistency Issues
```bash
# Problem: High variance in results
# Solution: Use fixed questions with seed
python luna_master_test.py --fixed_questions --seed 12345

# Problem: Unreproducible results  
# Solution: Document all parameters
python luna_master_test.py --verbose --prefix "experiment_1"
```

#### Performance Issues
```bash
# Problem: Tests running too slow
# Solution: Optimize parameters
python luna_master_test.py --tokens 1000 --delay 1.0 --questions 5

# Problem: Low quality responses
# Solution: Increase tokens and optimize temperature
python luna_master_test.py --tokens 2000 --temp 0.8
```

### Error Message Interpretations

#### Parameter Validation Errors
```
Questions must be between 1 and 120
→ Use --questions with valid range

Temperature must be between 0.0 and 2.0  
→ Use --temp with valid range

Tokens must be between 50 and 8192
→ Use --tokens with valid range

Test runs must be between 1 and 20
→ Use --testruns with valid range
```

#### Runtime Errors
```
Error: Connection failed
→ Check LM Studio is running on localhost:1234

Error: Request timed out
→ Increase --timeout or reduce --tokens

Error: No response received
→ Check model is loaded in LM Studio
```

---

## 📈 PERFORMANCE OPTIMIZATION TIPS

### Speed Optimization
1. **Reduce tokens** for faster responses (1000-1500 range)
2. **Decrease delay** between questions (--delay 1.0)
3. **Use smaller samples** for quick testing (--questions 5)
4. **Enable quiet mode** to reduce output overhead (--quiet)

### Quality Optimization  
1. **Increase tokens** for better responses (1800-2000 range)
2. **Optimize temperature** for creativity/consistency (--temp 0.8)
3. **Use larger samples** for reliability (--questions 15+)
4. **Multiple runs** for statistical validity (--testruns 5)

### Consistency Optimization
1. **Fixed questions** for reproducibility (--fixed_questions)
2. **Set random seed** for deterministic sampling (--seed 12345)
3. **Multiple runs** for variance analysis (--testruns 3+)
4. **Verbose logging** for detailed tracking (--verbose)

### Resource Optimization
1. **Custom output directory** to organize results (--output_dir)
2. **Filename prefixes** for experiment tracking (--prefix)
3. **Timeout management** for long-running tests (--timeout)
4. **Batch processing** for efficiency (multiple commands)

---

## 🎯 BEST PRACTICES

### Research Methodology
1. **Document all parameters** used in experiments
2. **Use consistent seeds** for reproducible research
3. **Run multiple iterations** for statistical validity
4. **Save intermediate results** with descriptive prefixes
5. **Validate findings** with different parameter combinations

### Production Deployment
1. **Start with recommended configurations**
2. **Monitor performance metrics** during execution
3. **Implement timeout safeguards** for reliability
4. **Use quiet mode** for automated systems
5. **Implement error handling** for batch processing

### Development Workflow
1. **Use quick tests** during development (--questions 1-3)
2. **Validate with medium tests** before deployment (--questions 8-10)
3. **Comprehensive testing** for final validation (--questions 15+)
4. **Document parameter choices** and rationale
5. **Version control** configuration files

---

## 🚀 FUTURE ENHANCEMENTS

### Planned CLI Improvements
- **Configuration files** for complex parameter sets
- **Batch job scheduling** for automated testing
- **Real-time monitoring** dashboard integration
- **Export formats** (CSV, Excel, database)
- **Model comparison** automation

### Advanced Features
- **Parameter sweeps** with automatic optimization
- **Statistical analysis** integration
- **Visualization** generation
- **Report templates** customization
- **API integration** capabilities

---

**CLI FRAMEWORK STATUS: COMPLETE AND OPERATIONAL** ✅  
**TOTAL PARAMETERS: 20+ CONFIGURABLE OPTIONS** 🎛️  
**VALIDATION: COMPREHENSIVE ERROR CHECKING** 🔒  
**DOCUMENTATION: COMPLETE USAGE GUIDE** 📚  
**READY FOR: PRODUCTION DEPLOYMENT** 🚀  

*The CLI Framework represents the pinnacle of user control and automation, enabling researchers and developers to conduct comprehensive AI personality evaluation with unprecedented flexibility and precision.*

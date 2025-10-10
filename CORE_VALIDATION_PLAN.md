# AIOS Core System Validation - Zero Tolerance Plan

**Date:** October 10, 2025  
**Scope:** Core production modules only (excluding backup_core and streamlit_core)  
**Standard:** Zero errors, zero warnings, zero placeholders, zero mock code

---

## Files in Scope (~160 Core Files)

- **carma_core**: 20 files - Memory and retrieval system
- **luna_core**: 38 files - Personality and chat system  
- **support_core**: 34 files - Logging, health, config, caching
- **utils_core**: 31 files - Validation, bridges, monitoring
- **dream_core**: 21 files - Meditation and memory consolidation
- **data_core**: 9 files - Data pipeline operations
- **enterprise_core**: 3 files - Encryption, billing, compliance
- **rag_core**: 2 files - Baseline RAG for CARMA comparison
- **Main scripts**: main.py, chat.py, luna_chat.py, quick_chat.py, aios_chat.py
- **Rust modules**: 6 compiled modules (utils, carma, luna, dream, support, backup)

**Total:** ~160 Python files + 6 Rust modules + all configs

---

## Phase 1: Placeholder Code Elimination (4-6 hours)

**Found:** 364 placeholder instances across 138 files

### Files with Placeholders in Core Modules:
- `main.py` - 1 instance
- `utils_core/core.py` - 2 instances
- `support_core/core/*.py` - Multiple instances
- `carma_core/core/fractal_cache.py` - 2 instances
- `luna_core/utilities/enhanced_lesson_retrieval.py` - 1 instance
- `utils_core/bridges/rust_bridge.py` - 2 instances
- `utils_core/bridges/powershell_bridge.py` - 2 instances
- `utils_core/monitoring/canary_controller.py` - 1 instance
- `utils_core/resilience/resilience_policies.py` - 1 instance
- `support_core/core/logger.py` - 5 instances
- `support_core/core/health_checker.py` - 1 instance
- `support_core/core/config.py` - 2 instances
- `dream_core/core_functions/memory_consolidation.py` - 1 instance
- `data_core/system/core/*.py` - Multiple instances

### Action for Each Placeholder:
1. **Locate** - grep for `pass`, `TODO`, `FIXME`, `XXX`, `HACK`, `NotImplementedError`
2. **Classify** - Is it:
   - Dead code? → Remove it
   - Needed feature? → Implement it
   - Abstract method? → Document it properly
   - Silent error suppression? → Add proper error handling
3. **Fix** - Implement, remove, or document
4. **Verify** - Test the fix works

### Forbidden Patterns:
```python
# FORBIDDEN - Silent failures
except Exception:
    pass

# FORBIDDEN - Empty implementations
def important_function():
    pass

# FORBIDDEN - Unimplemented features
def feature():
    raise NotImplementedError("TODO: implement this")

# FORBIDDEN - Lazy placeholders
# TODO: fix this later
# HACK: temporary workaround
```

**Acceptance Criteria:**
- ✅ ZERO placeholder code in core modules
- ✅ All functions either work or are properly removed
- ✅ All error handling is explicit and logged
- ✅ No silent failures

---

## Phase 2: Import Validation (3-4 hours)

Test that every core Python file imports successfully.

### Test Script:
```python
# test_all_core_imports.py
import importlib
import ast
import sys
from pathlib import Path

core_modules = [
    'carma_core', 'luna_core', 'support_core', 
    'utils_core', 'dream_core', 'data_core',
    'enterprise_core', 'rag_core'
]

errors = []

for module in core_modules:
    module_path = Path(module)
    if not module_path.exists():
        errors.append(f"Module directory not found: {module}")
        continue
    
    for py_file in module_path.rglob('*.py'):
        # Skip __pycache__
        if '__pycache__' in str(py_file):
            continue
            
        # 1. Syntax validation
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            errors.append(f"SYNTAX ERROR: {py_file}:{e.lineno} - {e.msg}")
        
        # 2. Import validation
        try:
            # Convert file path to module path
            rel_path = py_file.relative_to(Path('.'))
            module_path_str = str(rel_path.with_suffix('')).replace('/', '.').replace('\\', '.')
            
            # Skip __init__ and __main__
            if module_path_str.endswith('.__init__'):
                module_path_str = module_path_str[:-9]
            
            importlib.import_module(module_path_str)
            
        except Exception as e:
            errors.append(f"IMPORT ERROR: {py_file} - {type(e).__name__}: {e}")

if errors:
    print(f"\n❌ FOUND {len(errors)} ERRORS:\n")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
else:
    print(f"\n✅ ALL {total_files} CORE FILES IMPORT SUCCESSFULLY!")
```

**Acceptance Criteria:**
- ✅ ZERO syntax errors
- ✅ ZERO import errors
- ✅ Every file loads cleanly

---

## Phase 3: Function-Level Testing (6-8 hours)

Test every public function in core modules.

### Critical Functions by Module:

**carma_core:**
- `CARMASystem.process_query(query, context)` - Memory retrieval
- `CARMASystem.store_fragment(content, metadata)` - Storage
- `FastCARMA.process_query(query, context)` - Fast retrieval
- `FractalCache.find_relevant(query_embedding, topk)` - Search
- `CARMASystem.get_performance_level()` - Metrics

**luna_core:**
- `LunaSystem.chat(message)` - Main conversation handler
- `LunaResponseGenerator.generate_response(message, context)` - Response creation
- `LunaLearningSystem.learn_from_interaction(question, response)` - Learning
- `LunaPersonalitySystem.get_personality_state()` - State retrieval
- `LunaSystem.save_state()` / `load_state()` - Persistence

**support_core:**
- `aios_logger.info/warn/error()` - Logging functions
- `aios_health_checker.check_system_health()` - Health validation
- `aios_config.load_config()` - Config operations
- `CacheOperations.*()` - Cache management
- `RecoveryOperations.recover_from_failure()` - Recovery

**utils_core:**
- `RustBridge.load_rust_module()` - Rust module loading
- `AIOSJSONHandler.*()` - JSON operations
- `file_standards.validate()` - File validation
- `timestamp_validator.validate()` - Timestamp validation
- Monitoring and resilience functions

**dream_core:**
- `DreamCore.enter_meditation()` - Meditation state
- `DreamCore.consolidate_memories()` - Memory processing
- `DreamCore.wake_up()` - State restoration

**data_core:**
- `DataCore.process_pipeline()` - Data processing
- `DataCore.cleanup_old_data()` - Cleanup
- `DataCore.get_stats()` - Statistics

**enterprise_core:**
- `PiBasedEncryption.encrypt/decrypt()` - Encryption
- `EnterpriseBilling.calculate_usage()` - Billing
- `ComplianceManager.check_compliance()` - Compliance

**rag_core:**
- `RAGSystem.query()` - Standard RAG query
- `RAGSystem.index_documents()` - Document indexing

### Test Approach:
```python
# test_core_functions.py
def test_function_execution():
    # For each function:
    
    # 1. Test with valid inputs
    result = function(valid_input)
    assert result is not None
    assert isinstance(result, expected_type)
    
    # 2. Test with edge cases
    result = function(None)  # Should handle gracefully
    result = function("")    # Should handle gracefully
    result = function([])    # Should handle gracefully
    
    # 3. Test error conditions
    try:
        result = function(invalid_input)
    except ExpectedException:
        pass  # Good - expected error
    except Exception as e:
        raise AssertionError(f"Unexpected error: {e}")
    
    # 4. Verify no silent failures
    # No function should return None without documenting why
    # No function should catch and suppress errors silently
```

**Acceptance Criteria:**
- ✅ Every public function executes without crashing
- ✅ All functions return expected types
- ✅ Edge cases handled gracefully
- ✅ Errors are explicit, never silent

---

## Phase 4: Rust Module Testing (3-4 hours)

### 4.1 Load Validation
Test each Rust module loads successfully:

```python
# test_rust_modules.py
import sys

rust_modules = [
    ('utils', 'utils_core/rust_utils/target/release', 'aios_utils_rust'),
    ('carma', 'carma_core/rust_carma/target/release', 'aios_carma_rust'),
    ('luna', 'luna_core/rust_luna/target/release', 'aios_luna_rust'),
    ('dream', 'dream_core/rust_dream/target/release', 'aios_dream_rust'),
    ('support', 'support_core/rust_support/target/release', 'aios_support_rust'),
    ('backup', 'backup_core/rust_backup/target/release', 'aios_backup_rust'),
]

for name, path, module_name in rust_modules:
    sys.path.insert(0, path)
    try:
        module = __import__(module_name)
        print(f"✅ {name}: Loaded {module_name}")
        print(f"   Functions: {[x for x in dir(module) if not x.startswith('_')]}")
    except Exception as e:
        print(f"❌ {name}: FAILED to load - {e}")
        sys.exit(1)
```

### 4.2 Function Testing
Test every exposed Rust function:

```python
# For each Rust module
import aios_utils_rust

# Test each function with valid inputs
result = aios_utils_rust.some_function(valid_input)
assert result is not None

# Test error handling
try:
    aios_utils_rust.some_function(invalid_input)
except Exception:
    pass  # Expected
```

### 4.3 Performance Benchmarking
Compare Python vs Rust for equivalent operations:

```python
# benchmark_rust_vs_python.py
import time

# Test 1: File operations (utils_core)
start = time.time()
for i in range(1000):
    python_result = python_file_operation()
python_time = time.time() - start

start = time.time()
for i in range(1000):
    rust_result = aios_utils_rust.file_operation()
rust_time = time.time() - start

assert python_result == rust_result  # Outputs must match
speedup = python_time / rust_time
print(f"File operations: {speedup:.2f}x faster in Rust")

# Repeat for:
# - CARMA operations (carma_core)
# - Arbiter scoring (luna_core)
# - Dream consolidation (dream_core)
# - Cache operations (support_core)
# - Backup operations (backup_core)
```

**Acceptance Criteria:**
- ✅ All 6 Rust modules load successfully
- ✅ All Rust functions execute correctly
- ✅ Rust outputs match Python outputs exactly
- ✅ Rust is faster than Python for each operation (or document why not)

---

## Phase 5: Config File Creation & Validation (2-3 hours)

### 5.1 Missing Configs to Create

**Create: `utils_core/services/config/model_config.json`**
```json
{
  "embedder": {
    "name": "lite-mistral-150m-v2-instruct@q6_k_l",
    "api_endpoint": "http://localhost:1234/v1/embeddings"
  },
  "validation": {
    "enabled": true,
    "strict_mode": false
  }
}
```

**Create: `carma_core/utils/config/model_config.json`**
```json
{
  "embedder": {
    "name": "lite-mistral-150m-v2-instruct@q6_k_l",
    "api_endpoint": "http://localhost:1234/v1/embeddings",
    "cache_enabled": true
  },
  "search": {
    "default_topk": 5,
    "similarity_threshold": 0.7
  }
}
```

### 5.2 Validate Existing Configs

Check all existing config files:
- `luna_core/config/model_config.json` - Already working
- `dream_core/config/model_config.json` - Already working
- `carma_core/config/model_config.json` - Verify structure
- All other configs in core modules

### 5.3 Config Schema Validation
```python
# test_config_schemas.py
import json
from pathlib import Path

config_files = list(Path('.').rglob('config/*.json'))

for config_file in config_files:
    # Load config
    with open(config_file) as f:
        config = json.load(f)
    
    # Verify structure
    # Verify required fields exist
    # Test loading in actual system
    
    # Attempt to use config
    from model_config_loader import ModelConfigLoader
    loader = ModelConfigLoader(str(config_file.parent.parent))
    loader.get_main_model()  # Should not crash
```

**Acceptance Criteria:**
- ✅ All missing configs created
- ✅ All configs load successfully
- ✅ All configs have required fields
- ✅ All systems can use their configs

---

## Phase 6: Main Entry Points Testing (2-3 hours)

Test every CLI command and entry point:

### main.py Commands
```bash
# Core system tests
py main.py --help
py main.py --luna --status
py main.py --luna --info
py main.py --carma --status
py main.py --carma --info
py main.py --support --status
py main.py --support --health
py main.py --dream --status
py main.py --backup --status
py main.py --utils --status
py main.py --data --status

# Functional tests
py main.py --luna --message "Hello"
py main.py --carma --queries "test query"
py main.py --health
py main.py --optimize
py main.py --benchmark
```

### Chat Scripts
```bash
# luna_chat.py
py luna_chat.py  # Interactive mode
echo "Hello" | py luna_chat.py  # Pipe input

# quick_chat.py
py quick_chat.py --message "test"

# aios_chat.py
py aios_chat.py --message "test"

# chat.py
py chat.py
```

**Acceptance Criteria:**
- ✅ Every command executes without errors
- ✅ Help text displays correctly
- ✅ Status commands show system state
- ✅ Chat commands generate responses
- ✅ All CLI flags work as documented

---

## Phase 7: Integration Workflow Testing (4-6 hours)

### CARMA Workflow
```python
# Test complete CARMA lifecycle
from carma_core.carma_core import CARMASystem
from carma_core.implementations.fast_carma import FastCARMA

# 1. Initialize
carma = FastCARMA()

# 2. Store fragments
result = carma.process_query("test query", {})
assert result is not None

# 3. Search fragments
# (happens in process_query)

# 4. Retrieve with context
# (happens in process_query)

# 5. Performance metrics
summary = carma.get_fast_summary()
assert 'total_queries' in summary
```

### Luna Workflow
```python
# Test complete Luna conversation lifecycle
from luna_core.core.luna_core import LunaSystem

# 1. Initialize
luna = LunaSystem()

# 2. Chat
response = luna.chat("Hello, Luna")
assert response is not None
assert len(response) > 0

# 3. Verify memory
assert luna.carma_system is not None

# 4. Learn from interaction
# (happens automatically in chat)

# 5. Save state
luna.save_state()

# 6. Load state
luna2 = LunaSystem()
# Should load previous state
```

### Dream Workflow
```python
# Test dream/meditation cycle
from dream_core.dream_core import DreamCore

# 1. Initialize
dream = DreamCore()

# 2. Enter meditation
dream.enter_meditation()

# 3. Consolidate memories
dream.consolidate_memories()

# 4. Wake up
dream.wake_up()
```

### Support Workflow
```python
# Test support operations
from support_core.support_core import SupportSystem

# 1. Initialize
support = SupportSystem()

# 2. Health check
status = support.run_health_check()
assert status['system_ready'] == True

# 3. Logging
from support_core.support_core import aios_logger
aios_logger.info("Test message")

# 4. Cache operations
support.cache_ops.clear_cache()
support.cache_ops.get_cache_stats()
```

### Cross-Module Integration
```python
# Test Luna + CARMA
luna = LunaSystem()
response = luna.chat("What is CARMA?")
# Should retrieve CARMA documentation from memory

# Test CARMA + Dream
# Store memory, enter meditation, verify consolidation

# Test Support + All Modules
# Verify logging works in all modules
# Verify health checks work across modules
```

**Acceptance Criteria:**
- ✅ All workflows complete end-to-end
- ✅ State persists correctly
- ✅ Cross-module communication works
- ✅ No crashes or silent failures

---

## Phase 8: RAG Core Baseline Testing (1-2 hours)

### Test Standard RAG System
```python
# test_rag_core.py
from rag_core.rag_system import RAGSystem

# 1. Initialize
rag = RAGSystem()

# 2. Index documents
rag.index_documents(["doc1", "doc2", "doc3"])

# 3. Query
results = rag.query("test query")
assert results is not None

# 4. Compare to CARMA
# Run same query in CARMA
# Document differences
# Measure performance
```

**Purpose:** RAG core is the baseline for comparing CARMA's performance

**Acceptance Criteria:**
- ✅ RAG system initializes
- ✅ RAG can index and query
- ✅ Performance comparison to CARMA documented

---

## Phase 9: Linting & Type Checking (3-4 hours)

### Python Linting
```bash
# Install linters if needed
pip install pylint flake8 mypy

# Run on core modules
pylint carma_core/**/*.py --errors-only --disable=C,R,W
pylint luna_core/**/*.py --errors-only --disable=C,R,W
pylint support_core/**/*.py --errors-only --disable=C,R,W
pylint utils_core/**/*.py --errors-only --disable=C,R,W
pylint dream_core/**/*.py --errors-only --disable=C,R,W
pylint data_core/**/*.py --errors-only --disable=C,R,W
pylint enterprise_core/**/*.py --errors-only --disable=C,R,W
pylint rag_core/**/*.py --errors-only --disable=C,R,W

# Flake8 (style + errors)
flake8 carma_core/ luna_core/ support_core/ utils_core/ dream_core/ data_core/ enterprise_core/ rag_core/ --count --show-source

# MyPy (type checking - strict mode)
mypy --strict carma_core/
mypy --strict luna_core/
mypy --strict support_core/
mypy --strict utils_core/
mypy --strict dream_core/
mypy --strict data_core/
mypy --strict enterprise_core/
mypy --strict rag_core/
```

### Rust Linting
```bash
# For each Rust module
cd utils_core/rust_utils
cargo clippy -- -D warnings  # Deny all warnings
cargo fmt --check            # Check formatting
cd ../..

cd carma_core/rust_carma
cargo clippy -- -D warnings
cargo fmt --check
cd ../..

cd luna_core/rust_luna
cargo clippy -- -D warnings
cargo fmt --check
cd ../..

cd dream_core/rust_dream
cargo clippy -- -D warnings
cargo fmt --check
cd ../..

cd support_core/rust_support
cargo clippy -- -D warnings
cargo fmt --check
cd ../..
```

**Acceptance Criteria:**
- ✅ ZERO Python errors (pylint, flake8)
- ✅ ZERO type errors (mypy strict)
- ✅ ZERO Rust clippy warnings
- ✅ All Rust code properly formatted

---

## Phase 10: Deliverables (2-3 hours)

### 1. CORE_VALIDATION_REPORT.md
```markdown
# Complete validation results
## Summary
- Files tested: 160
- Placeholders fixed: 364
- Import errors: 0
- Function errors: 0
- Linting errors: 0

## By Module
### carma_core (20 files)
- File 1: ✅ PASS
- File 2: ✅ PASS
...

### Test Results
- Import validation: ✅ PASS
- Function testing: ✅ PASS
- Integration: ✅ PASS
- Linting: ✅ PASS
```

### 2. RUST_BENCHMARKS.md
```markdown
# Rust vs Python Performance

## utils_core
- File operations: 15.3x faster (Python: 1.2s, Rust: 0.078s)
- Validation: 22.1x faster
...

## carma_core
- Fragment search: 8.7x faster
- Memory operations: 12.4x faster
...

## Summary
- Average speedup: 14.2x across all modules
- All Rust implementations faster than Python
- All outputs match exactly
```

### 3. CONFIG_REFERENCE.md
```markdown
# AIOS Configuration Reference

## Required Configs
- luna_core/config/model_config.json - Luna's LLM settings
- dream_core/config/model_config.json - Dream model settings

## Optional Configs
- utils_core/services/config/model_config.json - Utils settings
- carma_core/utils/config/model_config.json - CARMA settings

## Schema for model_config.json
...
```

---

## Execution Order

1. **Fix Placeholders** (Phase 1) - Cannot proceed with broken code
2. **Validate Imports** (Phase 2) - Must load before testing
3. **Create Configs** (Phase 5) - Needed for functions to work
4. **Test Functions** (Phase 3) - Verify core functionality
5. **Verify Rust** (Phase 4.1-4.2) - Load and test Rust modules
6. **Test Entry Points** (Phase 6) - Main interfaces must work
7. **Test Workflows** (Phase 7) - Integration validation
8. **Test RAG** (Phase 8) - Baseline comparison
9. **Benchmark Rust** (Phase 4.3) - Performance validation
10. **Lint Everything** (Phase 9) - Final quality check
11. **Create Reports** (Phase 10) - Document results

---

## Failure = Stop Immediately

If ANY of these fail, STOP and FIX:
- Syntax error in any file
- Import error in any file
- Placeholder code found
- Function crashes with valid input
- Rust module fails to load
- Config file invalid
- Main command fails
- Workflow incomplete
- Linting error
- Type error

**ZERO TOLERANCE. 100% PASS REQUIRED.**

---

## Estimated Timeline

- Phase 1 (Placeholders): 4-6 hours
- Phase 2 (Imports): 3-4 hours
- Phase 3 (Functions): 6-8 hours
- Phase 4 (Rust): 3-4 hours
- Phase 5 (Configs): 2-3 hours
- Phase 6 (Entry Points): 2-3 hours
- Phase 7 (Workflows): 4-6 hours
- Phase 8 (RAG): 1-2 hours
- Phase 9 (Linting): 3-4 hours
- Phase 10 (Reports): 2-3 hours

**Total: 30-46 hours of systematic validation**

This is comprehensive, exhaustive, and zero-tolerance testing.


# Luna Master Test - Complete Tuning Guide
**Date:** September 21, 2025  
**Status:** Living Document - Updated During Tuning Sessions

## 🎯 Quick Reference - All Tunable Parameters

### **LLM Core Parameters**
| Parameter | Default | Range | Effect | Speed Impact |
|-----------|---------|-------|--------|-------------|
| `--tokens` | 600 | 50-8192 | Response length/detail | Higher = Slower |
| `--temp` | 0.7 | 0.0-2.0 | Creativity/randomness | Minimal |
| `--top_p` | 0.9 | 0.0-1.0 | Token selection diversity | Minimal |
| `--top_k` | 40 | 1-100 | Token candidate pool | Minimal |
| `--freq_penalty` | 0.0 | -2.0-2.0 | Repetition reduction | Minimal |
| `--presence_penalty` | 0.0 | -2.0-2.0 | Topic diversity | Minimal |

### **RAG System Parameters**
| Parameter | Default | Range | Effect | Speed Impact |
|-----------|---------|-------|--------|-------------|
| `--cache_limit` | 5.0 | 1.0-50.0 | Max cache size (MB) | Higher = Better context |
| `--cache_prune_threshold` | 100 | 10-1000 | Entries before pruning | Higher = More retention |
| `--cache_min_entries` | 10 | 5-100 | Min patterns after prune | Higher = More stable |
| `--rag_context` | 3 | 1-10 | Patterns per response | Higher = Slower |
| `--db_messages` | 50 | 10-500 | Database search scope | Higher = Slower |

### **Test Control Parameters**
| Parameter | Default | Range | Effect | Speed Impact |
|-----------|---------|-------|--------|-------------|
| `--questions` | 10 | 1-120 | Test thoroughness | Higher = Longer test |
| `--testruns` | 1 | 1-20 | Statistical reliability | Higher = Much longer |
| `--delay` | 2.0 | 0.1-10.0 | Pause between questions | Higher = Longer test |
| `--timeout` | 300 | 30-600 | Request timeout (sec) | Safety net |

## 🔥 Optimal Settings Discovered

### **BEST PERFORMANCE (Speed + Quality)**
```bash
python luna_master_test.py --questions 5 --tokens 600 --temp 0.7 --cache_limit 10.0 --cache_prune_threshold 200 --testruns 1
```
- **Score:** 4.02/5
- **Time:** 16.8s avg
- **Use case:** Daily testing, quick validation

### **MAXIMUM QUALITY (Slower)**
```bash
python luna_master_test.py --questions 10 --tokens 800 --temp 0.7 --rag_context 5 --db_messages 100 --testruns 2
```
- **Score:** 4.47/5 (historical best)
- **Time:** ~25s avg
- **Use case:** Deep evaluation, benchmarking

### **SPEED TEST (Quick validation)**
```bash
python luna_master_test.py --questions 3 --tokens 400 --temp 0.7 --delay 0.5 --testruns 1
```
- **Score:** ~3.5/5 (estimated)
- **Time:** <10s avg
- **Use case:** Rapid iteration, quick checks

## 🧠 Parameter Effects Deep Dive

### **Temperature Impact**
- **0.5:** Conservative, consistent, predictable
- **0.7:** ✅ OPTIMAL - Creative but stable
- **0.9:** Very creative, less predictable
- **1.2+:** Chaotic, potentially incoherent

### **Token Count Sweet Spots**
- **400-600:** ✅ OPTIMAL - Concise, punchy responses
- **800-1000:** Detailed, comprehensive responses
- **1200+:** Risk of verbosity, slower processing

### **RAG Context Tuning**
- **1-2:** Fast, minimal context
- **3:** ✅ OPTIMAL - Good balance
- **5+:** Rich context, slower processing

### **Cache Behavior**
- **Pruning triggers:** Size OR entry count limit hit
- **Frequency threshold:** Mean frequency (Travis's algorithm)
- **Pattern retention:** High-frequency = permanent memory

## 🎯 Quick Tuning Workflow

### **Step 1: Baseline Test**
```bash
python luna_master_test.py --questions 3 --tokens 600 --temp 0.7 --testruns 1
```

### **Step 2: Single Parameter Change**
```bash
# Test temperature
python luna_master_test.py --questions 3 --tokens 600 --temp 0.8 --testruns 1

# Test tokens
python luna_master_test.py --questions 3 --tokens 800 --temp 0.7 --testruns 1

# Test RAG context
python luna_master_test.py --questions 3 --tokens 600 --temp 0.7 --rag_context 5 --testruns 1
```

### **Step 3: Compare Results**
- **Score:** Higher = Better quality
- **Time:** Lower = Better speed
- **Authenticity:** Higher = More Travis-like
- **Cache growth:** Frequencies climbing = Learning

### **Step 4: Iterate**
- Keep improvements
- Discard degradations
- Test combinations of good changes

## 📊 Performance Benchmarks

### **Historical Best Results**
| Configuration | Score | Time | Notes |
|---------------|-------|------|-------|
| 800 tokens, temp 0.7, 3 context | 4.47/5 | 27.3s | Peak quality |
| 600 tokens, temp 0.7, 3 context | 4.02/5 | 16.8s | Best balance |
| 50 msgs vs 200 msgs | 3.97 vs 3.30 | 16.4s vs 19.4s | More ≠ Better |

### **Cache Evolution Tracking**
- **Start:** 0 patterns
- **Current:** 20 patterns, freq=130+
- **Pruning:** 71→10 patterns (aggressive)
- **Growth:** +2 patterns per test session

## 🚨 Warning Signs

### **Performance Degradation**
- Score drops below 3.5/5
- Response time exceeds 25s avg
- Authenticity below 0.5
- Cache not growing (freq stagnant)

### **System Issues**
- Timeout errors
- Cache corruption
- Model switching unexpectedly
- Memory issues (>8GB VRAM usage)

## 🔧 Troubleshooting

### **Slow Performance**
1. Reduce tokens (800→600)
2. Lower RAG context (5→3)
3. Reduce db_messages (100→50)
4. Check cache size

### **Poor Quality**
1. Increase tokens (600→800)
2. Adjust temperature (0.7→0.8)
3. Increase RAG context (3→5)
4. Check cache patterns

### **Inconsistent Results**
1. Set fixed seed
2. Use fixed questions
3. Multiple test runs
4. Check model consistency

---

## 📝 Session Notes Template

**Date:** [DATE]  
**Goal:** [TUNING OBJECTIVE]  
**Baseline:** [STARTING CONFIGURATION]  

### Tests Performed
1. **Test 1:** [CONFIG] → Score: X.X/5, Time: XXs
2. **Test 2:** [CONFIG] → Score: X.X/5, Time: XXs
3. **Test 3:** [CONFIG] → Score: X.X/5, Time: XXs

### Key Findings
- [DISCOVERY 1]
- [DISCOVERY 2]
- [DISCOVERY 3]

### Next Steps
- [ ] [ACTION 1]
- [ ] [ACTION 2]
- [ ] [ACTION 3]

---

**🎯 Ready for rapid iteration tuning! What parameter should we test next?**

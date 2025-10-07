# AIOS Runbook
**Operational Guide for Closed-Loop Evaluation System**

## Prerequisites

### Environment
- Python 3.11+
- LM Studio 0.3.x with models loaded
- Windows 10/11 or Linux (Ubuntu 22.04+)

### LM Studio Models Required
1. **Main Model**: `openhermes-2.5-mistral-7b` (or equivalent 7B model)
2. **Embedder**: `llama-3.2-1b-instruct-abliterated` (or equivalent 1B model)

### Installation
```powershell
# Install core dependencies
py -m pip install -r requirements.txt

# Install dashboard dependencies (optional)
py -m pip install -r requirements-dashboard.txt
```

---

## Daily Operations

### 1. Run Golden Tests (Regression Detection)

**PowerShell (Windows):**
```powershell
# Record new baseline
py tools\golden_runner.py record --set data_core\goldens\sample_set.json --out data_core\goldens\baseline_new.json

# Compare against baseline
py tools\golden_runner.py compare --set data_core\goldens\sample_set.json --baseline data_core\goldens\baseline_new.json --threshold 0.25 --out data_core\goldens\last_report.json

# Or use CI script
.\ci\golden_ci.ps1
```

**Bash (Linux/CI):**
```bash
# Use CI script (auto-detects python command)
bash ci/golden_ci.sh
```

**Expected Output:**
- 10/10 tests pass
- 60% main model, 40% embedder routing
- Avg latency: 12-15s
- Status: PASS (no regressions)

---

### 2. Check SLOs (Service Level Objectives)

```powershell
py scripts\quality_alert.py
```

**SLO Thresholds:**
- Pass rate ≥ 95%
- P95 latency ≤ 20,000ms (20s)
- Boundary drift ≤ 0.08

**Exit Codes:**
- `0` = All SLOs passing
- `2` = SLO violation detected

---

### 3. Launch Quality Dashboard

**PowerShell (Windows):**
```powershell
.\scripts\run_dashboard.ps1
```

**Bash (Linux):**
```bash
bash scripts/run_dashboard.sh
```

**Access:** http://localhost:8501

**Dashboard Tabs:**
1. **Overview** - A/B bucket split, routing sources
2. **Hypotheses** - Pass rate trends, quality metrics
3. **Routing** - Boundary drift charts, weight scatter
4. **Drill-down** - Per-message event table
5. **Settings** - Raw state inspection

**Auto-refresh:** Enable 10s refresh in sidebar

---

### 4. Monitor Provenance Logs

**View recent events:**
```powershell
Get-Content data_core\analytics\hypotheses.ndjson -Tail 10
```

**Count events by type:**
```powershell
py -c "import json; events=[json.loads(l) for l in open('data_core/analytics/hypotheses.ndjson')]; print(f'Total: {len(events)}'); print({e.get('event_type','response') for e in events})"
```

**Check adaptive routing state:**
```powershell
Get-Content data_core\analytics\adaptive_routing_state.json | ConvertFrom-Json
```

---

## Troubleshooting

### Golden Tests Failing (0/10 pass)

**Symptom:** All tests return `source: unknown`

**Causes:**
1. LM Studio not running → Start LM Studio
2. Models not loaded → Load both main + embedder models
3. Wrong API endpoint → Check `luna_core/config/model_config.json`

**Debug:**
```powershell
# Test LM Studio connection
curl http://localhost:1234/v1/models

# Test single question
py -c "from main import AIOSClean; aios=AIOSClean(); luna=aios._get_system('luna'); print(luna.learning_system.python_impl.process_question('hi', 'general'))"
```

---

### SLO Alert Failing

**High P95 Latency (>20s):**
- Check LM Studio model size (7B should be <20s)
- Check system resources (CPU/GPU load)
- Consider faster draft model for speculative decoding

**Low Pass Rate (<95%):**
- Check recent changes in git log
- Run golden tests manually to see failures
- Check `data_core/goldens/last_report.json` for details

**High Boundary Drift (>0.08):**
- Normal during early learning (first 10 messages)
- Check adaptive routing state for quality deltas
- May indicate hypothesis test failures

---

### Adaptive Routing Not Adapting

**Expected Behavior:**
- Needs 10+ messages before adaptation
- Only adapts if quality delta >5% and latency <1s
- Treatment bucket only (control stays at 0.5)

**Check:**
```powershell
# View adaptive state
cat data_core\analytics\adaptive_routing_state.json

# Check sample counts
py -c "import json; s=json.load(open('data_core/analytics/adaptive_routing_state.json')); print(f\"Control: {s['buckets']['control']['sample_count']}, Treatment: {s['buckets']['treatment']['sample_count']}\")"
```

---

### Dashboard Shows No Data

**Causes:**
1. Provenance file doesn't exist → Run some Luna questions first
2. Cache not refreshing → Disable cache in sidebar
3. Wrong file paths → Check Settings tab for paths

**Fix:**
```powershell
# Generate test data
py -c "from main import AIOSClean; aios=AIOSClean(); luna=aios._get_system('luna'); [luna.learning_system.python_impl.process_question(f'q{i}', 'general') for i in range(5)]"

# Verify data exists
dir data_core\analytics\hypotheses.ndjson
```

---

## Configuration Files

### Model Config
**Path:** `luna_core/config/model_config.json`

**Key settings:**
```json
{
  "main_model": {
    "name": "openhermes-2.5-mistral-7b",
    "api_endpoint": "http://localhost:1234/v1/chat/completions"
  },
  "embedder_llm": {
    "name": "llama-3.2-1b-instruct-abliterated",
    "api_endpoint": "http://localhost:1234/v1/chat/completions"
  }
}
```

### Adaptive Routing Config
**Defaults in code:** `utils_core/adaptive_routing.py`

**Key parameters:**
- `control_bucket_pct`: 0.5 (50/50 split)
- `min_samples_before_adapt`: 10 messages
- `adaptation_strength`: 0.1 (10% adjustment per cycle)

**Override:** Create `AdaptiveConfig()` with custom values

### Golden Test Config
**Path:** `data_core/goldens/sample_set.json`

**Format:**
```json
[
  {
    "id": "test_id",
    "question": "Question text",
    "trait": "general"
  }
]
```

---

## Data Management

### Provenance Log Rotation

**Manual rotation:**
```powershell
# Backup current log
$date = Get-Date -Format "yyyyMMdd"
Copy-Item data_core\analytics\hypotheses.ndjson "data_core\analytics\hypotheses_$date.ndjson.bak"

# Clear current (or gzip)
# Clear-Content data_core\analytics\hypotheses.ndjson
```

**Auto-rotation:** Coming in PR7 (nightly cron job)

### Clear Adaptive State (Reset A/B Test)

```powershell
del data_core\analytics\adaptive_routing_state.json
```

On next run, adaptive router will reinitialize with fresh buckets.

### Backup Golden Baselines

```powershell
# Before major changes
Copy-Item data_core\goldens\baseline_new.json "data_core\goldens\baseline_$(Get-Date -Format 'yyyyMMdd').json"
```

---

## CI/CD Integration

### GitHub Actions Workflows

**1. Quality Gate** (`.github/workflows/quality.yml`)
- Triggers: Pull requests to main/master
- Runs: Golden test comparison
- Fails: On regression >25%

**2. Quality Alerts** (`.github/workflows/alerts.yml`)
- Triggers: Every 30 minutes (schedule)
- Runs: Golden comparison + SLO check
- Warns: On SLO violations

### Local CI Simulation

```powershell
# Simulate PR quality gate
.\ci\golden_ci.ps1

# Check exit code
echo $LASTEXITCODE  # 0=pass, 1=fail
```

---

## Performance Baselines

### Expected Metrics (Healthy System)
- **Pass rate:** 95-100%
- **P50 latency:** 10-14s
- **P95 latency:** 15-20s
- **Mean latency:** 12-15s
- **Routing split:** 55-65% main model, 35-45% embedder

### Red Flags
- Pass rate <90% → System regression
- P95 >25s → Model performance issue
- Routing 100% either model → Math engine broken
- Boundary drift >0.1 → Runaway adaptation

---

## Emergency Procedures

### Kill Switch: Disable Adaptive Routing

**Option 1:** Environment variable
```powershell
$env:AIOS_ADAPTIVE_ENABLED = "0"
```

**Option 2:** Force all control bucket
```python
# In code
from utils_core.adaptive_routing import AdaptiveConfig
config = AdaptiveConfig(control_bucket_pct=1.0)  # 100% control, 0% treatment
```

### Rollback to Safe State

```powershell
# Revert to last known good commit
git log --oneline -10  # Find good commit
git checkout <commit_hash> -- luna_core/ support_core/ utils_core/

# Or full rollback
git reset --hard <commit_hash>
```

### Clear All Caches

```powershell
# Nuclear option - fresh start
Remove-Item -Recurse data_core\analytics\* -Force
Remove-Item -Recurse data_core\goldens\current_results.json -Force
Remove-Item -Recurse data_core\goldens\comparison_*.json -Force
```

---

## Development Workflow

### Adding New Golden Tests

1. Create test case in `data_core/goldens/sample_set.json`
2. Run baseline: `py tools\golden_runner.py record ...`
3. Commit baseline to git
4. CI will enforce on future PRs

### Monitoring New Features

1. Add hypothesis in `qec_integration/aios_hypothesis_tester.py`
2. Restart AIOS to load new hypothesis
3. Check dashboard Hypotheses tab for results

### Tuning Adaptive Routing

1. Adjust `AdaptiveConfig` parameters in `utils_core/adaptive_routing.py`
2. Clear adaptive state: `del data_core\analytics\adaptive_routing_state.json`
3. Run 20+ test questions
4. Check dashboard Routing tab for boundary changes

---

## File Locations

### Logs & Analytics
```
data_core/analytics/
  hypotheses.ndjson          # All provenance events
  adaptive_routing_state.json  # A/B bucket state
  golden_tests.ndjson         # Golden test events (optional)
```

### Golden Tests
```
data_core/goldens/
  sample_set.json             # Test questions
  baseline_new.json           # Current baseline
  last_report.json            # Latest comparison (for SLO alert)
  comparison_*.json           # Timestamped comparison history
```

### Configuration
```
luna_core/config/
  model_config.json           # LM Studio endpoints
  
support_core/config/
  model_config.json           # Fallback model config
```

---

## Quick Reference Commands

```powershell
# Test single component
py test_core_components.py

# Full golden test
.\ci\golden_ci.ps1

# Check SLOs
py scripts\quality_alert.py

# Launch dashboard
.\scripts\run_dashboard.ps1

# View recent events
Get-Content data_core\analytics\hypotheses.ndjson -Tail 5

# Check system status
py -c "from main import AIOSClean; aios=AIOSClean(); print(aios.get_system_overview())"
```

---

## Version Info

**AIOS Version:** Closed-Loop Evaluation System (PR1-PR6)  
**Last Updated:** 2025-10-07  
**Python:** 3.11+  
**LM Studio:** 0.3.x  
**Key Dependencies:** requests==2.32.4, pandas==2.2.3, plotly==6.3.0, streamlit==1.49.1


# AIOS Provenance NDJSON Schema

## Current Version: 1.0

### Response Event
```json
{
  "schema_version": "1.0",
  "event_type": "response",
  "ts": "2025-10-07T17:00:00.000000",
  "conv_id": "conv_abc123",
  "msg_id": 1,
  "question": "User question text",
  "trait": "general",
  "response": "AI response text",
  "meta": {
    "source": "main_model|embedder",
    "tier": "trivial_low|moderate_high",
    "response_type": "direct_embedder|full_generation"
  },
  "carma": {
    "fragments_found": ["fragment_id1", "fragment_id2"],
    "conversation_memories_found": [],
    "fragments": ["fragment_id1"],
    "conversation_memories": []
  },
  "math_weights": {
    "calculated_weight": 0.498,
    "question_complexity": 0.64,
    "user_engagement": 0.32,
    "mode": "engaging|direct",
    "adaptive": {
      "bucket": "control|treatment",
      "boundary": 0.5,
      "adaptive_metadata": {
        "adapted": false,
        "direction": "toward_main_model|toward_embedder",
        "adjustment": 0.0,
        "new_boundary": 0.5,
        "reason": "Quality delta: 0.000, Latency delta: 0ms"
      }
    }
  }
}
```

### Hypothesis Test Event
```json
{
  "schema_version": "1.0",
  "event_type": "hypothesis_test",
  "ts": "2025-10-07T17:00:00.000000",
  "conv_id": "conv_abc123",
  "hypo_id": "H_AIOS_1",
  "status": "supported|not_supported|error",
  "metric": 0.85,
  "p_value": 0.01,
  "effect_size": 0.75,
  "rec": "Recommendation text",
  "metadata": {}
}
```

### Hypothesis Batch Event (from CARMA)
```json
{
  "schema_version": "1.0",
  "event_type": "hypothesis_batch",
  "ts": "2025-10-07T17:00:00.000000",
  "conv_id": "conv_abc123",
  "msg_id": 10,
  "results": {
    "batch_id": "batch_abc",
    "total": 6,
    "passed": 4,
    "failed": 2,
    "rates": {
      "quality": 0.33,
      "latency": 0.05,
      "memory": 0.10
    }
  }
}
```

---

## Schema Versions

### Version 1.0 (2025-10-07)
**Added:**
- `schema_version` field to all events
- `event_type` field for event discrimination
- Structured `math_weights.adaptive` for adaptive routing metadata

**Changes:**
- None (first versioned schema)

### Version 0.9 (Pre-versioning)
**Fields:**
- No `schema_version` or `event_type` fields
- Event type inferred from field presence
- Compatible with migrator

---

## Migration

### Automatic Migration
```powershell
# Migrate all NDJSON files in analytics/
py utils_core\schema_migrator.py

# Migrate specific file
py utils_core\schema_migrator.py data_core\analytics\hypotheses.ndjson
```

**Backups:** Created as `filename.{old_version}.bak`

### Manual Migration
If automatic migration fails, manually add fields:
```python
import json

# Read old format
with open('old.ndjson', 'r') as f:
    events = [json.loads(line) for line in f if line.strip()]

# Add version fields
for event in events:
    event['schema_version'] = '1.0'
    # Infer type
    if 'question' in event:
        event['event_type'] = 'response'
    elif 'hypo_id' in event:
        event['event_type'] = 'hypothesis_test'

# Write new format
with open('new.ndjson', 'w') as f:
    for event in events:
        f.write(json.dumps(event) + '\n')
```

---

## Future Schema Changes

### Adding New Fields
- Add to end of event dict (backward compatible)
- Make fields optional with defaults
- Document in this file

### Breaking Changes
- Increment schema_version (e.g., 1.0 → 2.0)
- Create migration function in `schema_migrator.py`
- Update dashboard to handle both versions during transition

### Deprecating Fields
- Mark as deprecated in schema docs
- Keep reading for 2+ versions
- Remove after transition period


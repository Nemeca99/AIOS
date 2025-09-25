# AIOS JSON STANDARDS DOCUMENTATION
**Official AIOS Data Standard**  
**Version:** 2.0  
**Date:** September 24, 2025  
**Status:** ACTIVE

---

## 🎯 **CORE PRINCIPLE**

**ALL AIOS DATA MUST USE JSON ARRAYS AS THE PRIMARY STRUCTURE FOR CONSISTENCY, COMPATIBILITY, AND PERFORMANCE.**

This document defines the official standards for all JSON files in the AIOS system. Every JSON file must conform to these standards.

---

## 📊 **STANDARD DATA FORMATS**

### **1. CONVERSATION DATA**

**File Pattern:** `conversations_YYYY-MM-DD.json`, `*_conversation.json`

```json
[
  {
    "id": "uuid-string",
    "conversation_id": "uuid-string", 
    "role": "user|assistant|system",
    "content": "message text",
    "timestamp": "2025-09-24T14:16:21.786904Z",
    "metadata": {
      "model": "model-name",
      "tokens": 150,
      "score": 4.2,
      "source": "gaming_chaos|travis|synthetic|user",
      "quality": 0.85,
      "processing_time": 1.23
    }
  }
]
```

**Required Fields:**
- `id`: Unique UUID for each message
- `conversation_id`: UUID linking messages in same conversation
- `role`: "user", "assistant", or "system"
- `content`: The actual message text
- `timestamp`: ISO 8601 format with milliseconds
- `metadata`: Additional information object

**Optional Metadata Fields:**
- `model`: AI model used for generation
- `tokens`: Token count for the message
- `score`: Quality score (0.0-10.0)
- `source`: Data source identifier
- `quality`: Response quality metric (0.0-1.0)
- `processing_time`: Time taken to process (seconds)

---

### **2. CAR CACHE DATA**

**File Pattern:** `cache_*.json`, `*_cache.json`

```json
[
  {
    "id": "uuid-string",
    "pattern": "message text",
    "embedding": [0.1, 0.2, -0.3, ...],
    "frequency": 5,
    "last_used": "2025-09-24T14:16:21.786904Z",
    "similarity_threshold": 0.8,
    "compression": {
      "ratio": 4.10,
      "ris_importance": 119.9,
      "warp_stable": true,
      "tfid_anchor": 0.618034
    },
    "metadata": {
      "created": "2025-09-24T14:16:21.786904Z",
      "source": "user|synthetic|system",
      "quality_score": 0.85
    }
  }
]
```

**Required Fields:**
- `id`: Unique UUID for cache entry
- `pattern`: The text pattern being cached
- `embedding`: Vector embedding array
- `frequency`: How often this pattern is used
- `last_used`: Last access timestamp
- `similarity_threshold`: Matching threshold (0.0-1.0)
- `compression`: Compression metadata object

**Compression Object Fields:**
- `ratio`: Compression ratio achieved
- `ris_importance`: RIS importance score
- `warp_stable`: Stability indicator
- `tfid_anchor`: TF-IDF anchor value

---

### **3. CONFIGURATION FILES**

**File Pattern:** `*_config.json`, `config_*.json`

```json
[
  {
    "id": "uuid-string",
    "config_name": "luna_master_test",
    "version": "2.0",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 600,
      "rag_enabled": true,
      "cache_limit": 5.0,
      "compression_enabled": true,
      "learning_rate": 0.01,
      "adaptation_threshold": 0.1
    },
    "models": {
      "main": "qwen3-30b-a3b",
      "embedder": "mixedbread-ai/mxbai-embed-large-v1",
      "generator": "DavidAU/Llama-3.2-8X3B-MOE-Dark-Champion-Instruct"
    },
    "timestamp": "2025-09-24T14:16:21.786904Z",
    "metadata": {
      "created_by": "system|user",
      "last_modified": "2025-09-24T14:16:21.786904Z",
      "migration_from": "legacy_format",
      "original_structure": "single_object"
    }
  }
]
```

**Required Fields:**
- `id`: Unique UUID for config entry
- `config_name`: Human-readable configuration name
- `version`: Version number (semantic versioning)
- `parameters`: Configuration parameters object
- `models`: Model specifications object
- `timestamp`: Creation/modification timestamp
- `metadata`: Additional metadata

---

### **4. TEST RESULTS DATA**

**File Pattern:** `results_*.json`, `*_test_results.json`

```json
[
  {
    "test_id": "uuid-string",
    "timestamp": "2025-09-24T14:16:21.786904Z",
    "mode": "luna_with_memory",
    "model": "qwen3-30b-a3b",
    "questions": [
      {
        "question": "I am someone who takes charge",
        "response": "Great, now who's following you?",
        "score": 3.9,
        "time": 74.4,
        "tokens": 604,
        "big_five_category": "extraversion",
        "metadata": {
          "difficulty": "medium",
          "category": "personality_assessment"
        }
      }
    ],
    "performance": {
      "avg_score": 4.22,
      "avg_time": 36.4,
      "success_rate": 100.0,
      "total_questions": 5,
      "accuracy": 0.95
    },
    "metadata": {
      "test_environment": "production|staging|development",
      "test_duration": 180.5,
      "system_version": "2.0"
    }
  }
]
```

**Required Fields:**
- `test_id`: Unique UUID for test run
- `timestamp`: Test execution timestamp
- `mode`: Test mode identifier
- `model`: Model being tested
- `questions`: Array of test questions and responses
- `performance`: Overall performance metrics
- `metadata`: Test metadata

---

### **5. PERSONALITY DATA**

**File Pattern:** `*_personality.json`, `personality_*.json`

```json
[
  {
    "id": "uuid-string",
    "personality_name": "Luna",
    "version": "2.0",
    "parameters": {
      "name": "Luna",
      "age": 21,
      "personality_weights": {
        "openness": 0.6,
        "conscientiousness": 0.85,
        "extraversion": 0.35,
        "agreeableness": 0.55,
        "neuroticism": 0.15
      },
      "communication_style": {
        "formality": 0.2,
        "humor_level": 0.25,
        "empathy_level": 0.5,
        "technical_depth": 0.8,
        "creativity": 0.4
      }
    },
    "timestamp": "2025-09-24T14:16:21.786904Z",
    "metadata": {
      "created_by": "system",
      "last_modified": "2025-09-24T14:16:21.786904Z",
      "personality_type": "gothic_intellectual",
      "consciousness_level": "advanced"
    }
  }
]
```

---

### **6. MEMORY DATA**

**File Pattern:** `*_memory.json`, `memory_*.json`

```json
[
  {
    "id": "uuid-string",
    "memory_type": "persistent|episodic|semantic",
    "version": "2.0",
    "parameters": {
      "interactions": [],
      "dreams": [],
      "personality_evolution": [],
      "emotional_patterns": {},
      "dream_cycles": [],
      "learning_history": []
    },
    "timestamp": "2025-09-24T14:16:21.786904Z",
    "metadata": {
      "created_by": "system",
      "last_modified": "2025-09-24T14:16:21.786904Z",
      "memory_size": 1024,
      "compression_ratio": 0.75
    }
  }
]
```

---

## 🔧 **IMPLEMENTATION RULES**

### **File Naming Convention**

| Data Type | Pattern | Example |
|-----------|---------|---------|
| Conversations | `conversations_YYYY-MM-DD.json` | `conversations_2025-09-24.json` |
| Conversations | `*_conversation.json` | `user_conversation.json` |
| Cache | `cache_*.json` | `cache_master.json` |
| Cache | `*_cache.json` | `embedder_cache.json` |
| Config | `*_config.json` | `luna_config.json` |
| Config | `config_*.json` | `config_master.json` |
| Test Results | `results_*.json` | `results_master_test.json` |
| Test Results | `*_test_results.json` | `luna_test_results.json` |
| Personality | `*_personality.json` | `luna_personality.json` |
| Memory | `*_memory.json` | `luna_memory.json` |

### **UUID Generation**

All entries must have a unique UUID:
```python
import uuid
entry_id = str(uuid.uuid4())
```

### **Timestamp Format**

All timestamps must use ISO 8601 format with milliseconds:
```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

### **Array Structure Requirement**

**CRITICAL:** Every JSON file must be an array, even if it contains only one item:
```json
// ✅ CORRECT - Always an array
[{"id": "uuid", "data": "value"}]

// ❌ WRONG - Never a single object
{"id": "uuid", "data": "value"}
```

---

## 🎯 **VALIDATION RULES**

### **Required Field Validation**

Every JSON file must be validated against these rules:

1. **Array Structure**: Must be a JSON array
2. **UUID Fields**: All `id` fields must be valid UUIDs
3. **Timestamp Format**: All timestamps must be ISO 8601 format
4. **Required Fields**: Each data type has specific required fields
5. **Data Types**: Fields must match expected data types (string, number, boolean, array, object)

### **Validation Code Example**

```python
from aios_json_standards import AIOSJSONStandards, AIOSDataType

# Load and validate JSON array
def validate_json_file(file_path: str, data_type: AIOSDataType):
    try:
        data = AIOSJSONHandler.load_json_array(file_path)
        
        if data_type == AIOSDataType.CONVERSATION:
            return AIOSJSONStandards.validate_conversation_format(data)
        elif data_type == AIOSDataType.CAR_CACHE:
            return AIOSJSONStandards.validate_car_cache_format(data)
        # ... other validations
        
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False
```

---

## 🚀 **MIGRATION GUIDELINES**

### **Converting Legacy Files**

When converting existing files to AIOS standard:

1. **Backup Original**: Always create a backup with timestamp
2. **Validate Structure**: Ensure data can be converted
3. **Add Missing Fields**: Generate UUIDs and timestamps
4. **Wrap in Array**: Convert single objects to arrays
5. **Test Compatibility**: Verify system still works

### **Migration Script Usage**

```python
from aios_json_standards import AIOSJSONHandler, AIOSDataType

# Convert legacy cache data
legacy_cache = {"pattern1": {"freq": 5}, "pattern2": {"freq": 3}}
aios_cache = AIOSJSONHandler.convert_to_aios_standard(legacy_cache, AIOSDataType.CAR_CACHE)

# Save in AIOS format
AIOSJSONHandler.save_json_array(aios_cache, "cache_master.json")
```

---

## 📋 **COMPLIANCE CHECKLIST**

Before deploying any JSON file, verify:

- [ ] File is a JSON array (starts with `[`)
- [ ] All entries have unique `id` fields (UUIDs)
- [ ] All timestamps are ISO 8601 format
- [ ] Required fields are present for the data type
- [ ] File naming follows convention
- [ ] Data types are correct (string, number, boolean, array, object)
- [ ] Metadata objects are properly structured
- [ ] Validation passes using AIOS standards

---

## 🔥 **EXAMPLES BY FILE TYPE**

### **Conversation File**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "conversation_id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
    "role": "user",
    "content": "Hello, how are you?",
    "timestamp": "2025-09-24T14:16:21.786904Z",
    "metadata": {
      "model": "luna",
      "tokens": 6,
      "score": 8.5,
      "source": "user"
    }
  },
  {
    "id": "c3d4e5f6-g7h8-9012-cdef-345678901234",
    "conversation_id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
    "role": "assistant",
    "content": "I'm doing well, thank you for asking!",
    "timestamp": "2025-09-24T14:16:22.123456Z",
    "metadata": {
      "model": "luna",
      "tokens": 12,
      "score": 9.2,
      "source": "assistant"
    }
  }
]
```

### **Configuration File**
```json
[
  {
    "id": "d4e5f6g7-h8i9-0123-defg-456789012345",
    "config_name": "luna_master_config",
    "version": "2.0",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 600,
      "rag_enabled": true
    },
    "models": {
      "main": "qwen3-30b-a3b",
      "embedder": "mixedbread-ai/mxbai-embed-large-v1"
    },
    "timestamp": "2025-09-24T14:16:21.786904Z",
    "metadata": {
      "created_by": "system",
      "environment": "production"
    }
  }
]
```

---

## 🎯 **BENEFITS OF AIOS JSON STANDARDS**

1. **Universal Compatibility** - All components use the same format
2. **Easy Debugging** - Consistent, human-readable structure
3. **Database Ready** - SQLite JSON1 extension compatible
4. **API Standard** - REST/GraphQL ready out of the box
5. **Version Control** - Git-friendly text format
6. **Compression Ready** - AIOS UML/RIS compression compatible
7. **Validation** - Built-in validation and error checking
8. **Migration** - Easy conversion from legacy formats
9. **Performance** - Optimized for parsing and processing
10. **Maintainability** - Clear structure for future development

---

## 📞 **SUPPORT AND QUESTIONS**

For questions about AIOS JSON Standards:

1. **Check this documentation** first
2. **Use validation tools** in `aios_json_standards.py`
3. **Run migration scripts** for legacy files
4. **Test with sample data** before production use

---

**🎯 This standard ensures all AIOS components speak the same language!** 🚀

**Last Updated:** September 24, 2025  
**Version:** 2.0  
**Status:** ACTIVE

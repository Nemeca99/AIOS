# AIOS JSON STANDARD FORMAT
**Date:** September 21, 2025  
**Status:** Official AIOS Data Standard

## 🎯 Core Principle
**All AIOS data must use JSON arrays as the primary structure for consistency, compatibility, and performance.**

## 📊 Standard Formats

### **Conversation Data**
```json
[
  {
    "id": "uuid-string",
    "conversation_id": "uuid-string", 
    "role": "user|assistant",
    "content": "message text",
    "timestamp": "2025-09-21T18:56:13.898Z",
    "metadata": {
      "model": "model-name",
      "tokens": 150,
      "score": 4.2,
      "source": "gaming_chaos|travis|synthetic"
    }
  }
]
```

### **CAR Cache Data**
```json
[
  {
    "pattern": "message text",
    "embedding": [0.1, 0.2, -0.3, ...],
    "frequency": 5,
    "last_used": "2025-09-21T18:56:13.898Z",
    "similarity_threshold": 0.8,
    "compression": {
      "ratio": 4.10,
      "ris_importance": 119.9,
      "warp_stable": true,
      "tfid_anchor": 0.618034
    }
  }
]
```

### **Test Results**
```json
[
  {
    "test_id": "uuid-string",
    "timestamp": "2025-09-21T18:56:13.898Z",
    "mode": "luna_with_memory",
    "model": "qwen3-30b-a3b",
    "questions": [
      {
        "question": "I am someone who takes charge",
        "response": "Great, now who's following you?",
        "score": 3.9,
        "time": 74.4,
        "tokens": 604,
        "big_five_category": "extraversion"
      }
    ],
    "performance": {
      "avg_score": 4.22,
      "avg_time": 36.4,
      "success_rate": 100.0,
      "total_questions": 5
    }
  }
]
```

### **Configuration Files**
```json
[
  {
    "config_name": "luna_master_test",
    "version": "1.0",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 600,
      "rag_enabled": true,
      "cache_limit": 5.0,
      "compression_enabled": true
    },
    "models": {
      "main": "qwen3-30b-a3b",
      "embedder": "text-embedding-mlabonne_qwen3-0.6b-abliterated"
    }
  }
]
```

## 🔧 Implementation Rules

### **File Naming Convention**
- `*.json` - All data files end with .json
- `conversations_YYYY-MM-DD.json` - Timestamped data
- `cache_master.json` - Current active cache
- `results_[testname]_[timestamp].json` - Test results

### **Database Integration**
- SQLite JSON1 extension for JSON column support
- Array elements map to database rows
- Maintain JSON structure in `metadata` columns

### **API Responses**
- Always return JSON arrays, even for single items: `[{item}]`
- Consistent error format: `[{"error": "message", "code": 400}]`
- Pagination: `[{"data": [...], "page": 1, "total": 100}]`

### **Compression Standards**
- Use AIOS UML/RIS compression on JSON before storage
- Maintain JSON structure after decompression
- Include compression metadata in JSON objects

## 🎯 Benefits

1. **Universal Compatibility** - Works everywhere
2. **Easy Debugging** - Human readable structure  
3. **Consistent Processing** - Same parsing logic everywhere
4. **Database Friendly** - Native JSON support in modern DBs
5. **API Standard** - REST/GraphQL compatibility
6. **Version Control** - Git-friendly text format
7. **Compression Ready** - Works with AIOS UML compression

## 📝 Migration Plan

1. **Phase 1:** Convert existing cache files to JSON arrays
2. **Phase 2:** Update database schema to use JSON columns
3. **Phase 3:** Standardize all config files
4. **Phase 4:** Update all APIs to return JSON arrays
5. **Phase 5:** Implement compression on JSON structures

## 🔥 Example Migration

**Old Format:**
```python
cache = {"pattern1": {"freq": 5}, "pattern2": {"freq": 3}}
```

**New AIOS Standard:**
```json
[
  {"pattern": "pattern1", "frequency": 5, "id": "uuid1"},
  {"pattern": "pattern2", "frequency": 3, "id": "uuid2"}
]
```

---
**This standard ensures all AIOS components speak the same language!** 🚀

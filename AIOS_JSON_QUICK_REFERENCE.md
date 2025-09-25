# AIOS JSON Standards - Quick Reference Guide

**Version:** 2.0  
**Date:** September 24, 2025

---

## 🎯 **CORE RULE**

**ALL JSON FILES MUST BE ARRAYS - NO EXCEPTIONS!**

```json
// ✅ CORRECT
[{"id": "uuid", "data": "value"}]

// ❌ WRONG  
{"id": "uuid", "data": "value"}
```

---

## 📋 **REQUIRED FIELDS BY TYPE**

### **Conversation Data**
```json
{
  "id": "uuid-string",
  "conversation_id": "uuid-string", 
  "role": "user|assistant|system",
  "content": "message text",
  "timestamp": "2025-09-24T14:16:21.786904Z",
  "metadata": {}
}
```

### **Cache Data**
```json
{
  "id": "uuid-string",
  "pattern": "message text",
  "embedding": [0.1, 0.2, -0.3, ...],
  "frequency": 5,
  "last_used": "2025-09-24T14:16:21.786904Z",
  "similarity_threshold": 0.8,
  "compression": {}
}
```

### **Config Data**
```json
{
  "id": "uuid-string",
  "config_name": "config_name",
  "version": "2.0",
  "parameters": {},
  "models": {},
  "timestamp": "2025-09-24T14:16:21.786904Z",
  "metadata": {}
}
```

---

## 🔧 **FILE NAMING PATTERNS**

| Type | Pattern | Example |
|------|---------|---------|
| Conversations | `*_conversation.json` | `user_conversation.json` |
| Cache | `cache_*.json` | `cache_master.json` |
| Config | `*_config.json` | `luna_config.json` |
| Test Results | `results_*.json` | `results_test.json` |
| Personality | `*_personality.json` | `luna_personality.json` |
| Memory | `*_memory.json` | `luna_memory.json` |

---

## 🚀 **QUICK IMPLEMENTATION**

### **Generate UUID**
```python
import uuid
id = str(uuid.uuid4())
```

### **Generate Timestamp**
```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
```

### **Validate JSON**
```python
from aios_json_standards import AIOSJSONHandler
data = AIOSJSONHandler.load_json_array("file.json")
```

### **Convert Legacy Data**
```python
from aios_json_standards import AIOSJSONHandler, AIOSDataType
aios_data = AIOSJSONHandler.convert_to_aios_standard(legacy_data, AIOSDataType.CONVERSATION)
```

---

## ✅ **COMPLIANCE CHECKLIST**

- [ ] File is JSON array `[ ... ]`
- [ ] All entries have `id` (UUID)
- [ ] All timestamps are ISO 8601 format
- [ ] Required fields present
- [ ] File name follows pattern
- [ ] Validation passes

---

## 🎯 **COMMON MISTAKES TO AVOID**

1. **❌ Single objects instead of arrays**
2. **❌ Missing UUID fields**
3. **❌ Wrong timestamp format**
4. **❌ Missing required fields**
5. **❌ Inconsistent file naming**

---

**Need more detail? See `AIOS_JSON_STANDARDS_DOCUMENTATION.md`**

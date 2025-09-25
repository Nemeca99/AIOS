# AIOS File Standards - Quick Reference Guide

**Version:** 1.0  
**Date:** September 24, 2025

---

## 🎯 **CORE RULES**

**ALL FILES MUST FOLLOW AIOS STANDARDS FOR CONSISTENCY AND PROFESSIONAL QUALITY**

---

## 📋 **FILE TYPE STANDARDS**

### **Python Files (.py)**
```python
#!/usr/bin/env python3
"""
Module docstring - Brief description.
"""

import os
from typing import List, Dict, Optional, Any, TypeAlias

# Type aliases for better type checking
JSON = Dict[str, Any]  # Alias for complex JSON typing
JSONArray = List[JSON]  # Alias for JSON arrays

class ExampleClass:
    """Class docstring."""
    
    def example_method(self, data: JSONArray) -> Optional[str]:
        """Method docstring.
        
        Args:
            data: List of JSON objects containing data.
            
        Returns:
            Description of return value.
        """
        return "example"

def main() -> None:
    """Main function."""
    pass

if __name__ == "__main__":
    main()
```

**Standards:**
- **Encoding:** UTF-8
- **Indentation:** 4 spaces
- **Max Line:** 88 characters
- **Naming:** `snake_case.py`
- **Required:** Shebang, docstrings, type hints
- **Static Analysis:** Use mypy for type checking

---

### **JSON Files (.json)**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "timestamp": "2025-09-24T14:30:00.123Z",
    "aios_version": "2.0",
    "conversation_id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
    "role": "user",
    "content": "Hello, how are you?",
    "metadata": {
      "model": "luna",
      "tokens": 6,
      "score": 8.5,
      "source": "user"
    }
  }
]
```

**Standards:**
- **Structure:** Always arrays `[{...}]`
- **Encoding:** UTF-8
- **Indentation:** 2 spaces
- **Required:** `id` (UUID), `timestamp` (ISO 8601), `aios_version`, `metadata`
- **Naming:** `*_conversation.json`, `cache_*.json`

---

### **Markdown Files (.md)**
```markdown
# Document Title
**Purpose:** Brief description  
**Version:** 1.0  
**Date:** 2025-09-24  
**Status:** ACTIVE

---

## 🎯 **Section Title**

Content here.

### **Subsection**

More content.

---

**Last Updated:** 2025-09-24  
**Version:** 1.0  
**Status:** ACTIVE
```

**Standards:**
- **Encoding:** UTF-8
- **Line Length:** 80 characters max
- **Headers:** Use #, ##, ###
- **Naming:** `DESCRIPTIVE_NAME.md`

---

### **Database Files (.db)**
```sql
CREATE TABLE example_table (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    data TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Standards:**
- **Type:** SQLite 3.x
- **Encoding:** UTF-8
- **Schema:** Versioned with migrations
- **Naming:** `descriptive_name.db`

---

### **Text Files (.txt)**
```
# AIOS Configuration File
# Generated: 2025-09-24T14:30:00Z
# Version: 2.0

[SECTION_NAME]
key1=value1
key2=value2
```

**Standards:**
- **Encoding:** UTF-8
- **Structure:** Organized sections
- **Naming:** `config_name.txt`

---

### **Batch Files (.bat)**
```batch
@echo off
REM AIOS Batch Script
REM Purpose: Brief description
REM Version: 1.0

setlocal enabledelayedexpansion

echo Starting script...
python main.py

if %ERRORLEVEL% EQU 0 (
    echo Success
    exit /b 0
) else (
    echo Failed
    exit /b 1
)
```

**Standards:**
- **Encoding:** ANSI or UTF-8 with BOM
- **Line Endings:** CRLF
- **Comments:** Use REM
- **Naming:** `script_name.bat`

---

### **Shell Scripts (.sh)**
```bash
#!/bin/bash
# AIOS Shell Script
# Purpose: Brief description
# Version: 1.0

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting script..."
python3 main.py

echo "Script completed"
exit 0
```

**Standards:**
- **Shebang:** `#!/bin/bash`
- **Encoding:** UTF-8
- **Error Handling:** `set -euo pipefail`
- **Naming:** `script_name.sh`

---

### **YAML Files (.yml, .yaml)**
```yaml
# AIOS Configuration File
# Version: 2.0
# Date: 2025-09-24

app:
  name: "AIOS System"
  version: "2.0.0"
  debug: false

database:
  type: "sqlite"
  path: "data/aios.db"
```

**Standards:**
- **Encoding:** UTF-8
- **Indentation:** 2 spaces
- **Comments:** Use #
- **Naming:** `config.yml`

---

### **Environment Files (.env)**
```
# AIOS Environment Configuration
# Generated: 2025-09-24
# DO NOT COMMIT WITH REAL SECRETS

AIOS_ENV=development
AIOS_DEBUG=true
DATABASE_URL=sqlite:///data/aios.db
API_HOST=localhost
API_PORT=8000
```

**Standards:**
- **Encoding:** UTF-8
- **Format:** `KEY=value`
- **Comments:** Use #
- **Naming:** `.env`, `.env.production`

---

### **Docker Files (Dockerfile)**
```dockerfile
# AIOS System Dockerfile
# Version: 2.0
# Date: 2025-09-24

FROM python:3.11-slim

LABEL maintainer="AIOS Team"
LABEL version="2.0"

ENV PYTHONUNBUFFERED=1
ENV AIOS_ENV=production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER aios
EXPOSE 8000

CMD ["python", "main.py"]
```

**Standards:**
- **Encoding:** UTF-8
- **Base Images:** Official, minimal
- **Security:** Non-root user
- **Naming:** `Dockerfile`

---

### **Log Files (.log)**
```
2025-09-24T14:30:00.123Z | INFO | LUNA | Message content here
2025-09-24T14:30:01.456Z | ERROR | CARMA | Error message with details
2025-09-24T14:30:02.789Z | DEBUG | RAG | Debug information
```

**Standards:**
- **Encoding:** UTF-8
- **Format:** Structured with timestamps
- **Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Naming:** `component_YYYY-MM-DD.log`

---

### **CSV Files (.csv)**
```csv
id,timestamp,component,level,message,metadata
"uuid-1","2025-09-24T14:30:00Z","LUNA","INFO","System started","{}"
"uuid-2","2025-09-24T14:30:01Z","CARMA","ERROR","Database failed","{\"code\": 500}"
```

**Standards:**
- **Encoding:** UTF-8
- **Separator:** Comma (,)
- **Headers:** First row
- **Quotes:** For values with commas
- **Naming:** `data_YYYY-MM-DD.csv`

---

## 🔧 **QUICK IMPLEMENTATION**

### **Validate All Files**
```bash
python validate_aios_files.py .
```

### **Format Python Files**
```bash
python -m black *.py
python -m isort *.py
```

### **Convert Line Endings**
```bash
# Unix
find . -name "*.py" -o -name "*.md" | xargs dos2unix

# Windows
find . -name "*.py" -o -name "*.md" | xargs unix2dos
```

### **Check Encoding**
```bash
file -i *.py *.md *.json
```

---

## 📋 **NAMING CONVENTIONS**

| File Type | Pattern | Example |
|-----------|---------|---------|
| **Python** | `snake_case.py` | `aios_json_standards.py` |
| **JSON** | `*_conversation.json` | `user_conversation.json` |
| **Markdown** | `DESCRIPTIVE_NAME.md` | `AIOS_STANDARDS_DOCUMENTATION.md` |
| **Database** | `descriptive_name.db` | `conversations.db` |
| **Text** | `config_name.txt` | `luna_config.txt` |
| **Batch** | `script_name.bat` | `start_aios.bat` |
| **Shell** | `script_name.sh` | `start_aios.sh` |
| **YAML** | `config.yml` | `docker-compose.yml` |
| **Environment** | `.env` | `.env.production` |
| **Docker** | `Dockerfile` | `Dockerfile.prod` |
| **Log** | `component_YYYY-MM-DD.log` | `luna_2025-09-24.log` |
| **CSV** | `data_YYYY-MM-DD.csv` | `export_2025-09-24.csv` |

---

## ✅ **COMPLIANCE CHECKLIST**

Before committing any file, verify:

- [ ] **Encoding:** UTF-8 (except .bat files)
- [ ] **Line Endings:** LF for Unix, CRLF for Windows
- [ ] **Naming:** Follows convention for file type
- [ ] **Structure:** Follows standard structure
- [ ] **Content:** Valid syntax and format
- [ ] **Documentation:** Includes proper headers/comments
- [ ] **Validation:** Passes validation tools
- [ ] **Testing:** Code includes tests (for .py files)

---

## 🎯 **COMMON MISTAKES TO AVOID**

1. **❌ Wrong encoding** (not UTF-8)
2. **❌ Wrong line endings** (CRLF vs LF)
3. **❌ Inconsistent naming** (not following conventions)
4. **❌ Missing documentation** (no headers/comments)
5. **❌ Invalid syntax** (JSON, YAML, Python errors)
6. **❌ Missing required fields** (JSON without id/timestamp)
7. **❌ Poor structure** (no organization)
8. **❌ No error handling** (scripts without error handling)

---

## 🚀 **VALIDATION TOOLS**

```bash
# Validate all files
python validate_aios_files.py .

# Validate specific file types
python validate_aios_json.py *.json
python -m flake8 *.py
python -m black --check *.py
python -m mypy *.py  # Static type checking
markdownlint *.md
yamllint *.yml
```

---

**Need more detail? See `AIOS_FILE_STANDARDS_DOCUMENTATION.md`**

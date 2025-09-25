# AIOS FILE STANDARDS DOCUMENTATION
**Official AIOS File Standards**  
**Version:** 1.0  
**Date:** September 24, 2025  
**Status:** ACTIVE

---

## 🎯 **CORE PRINCIPLE**

**ALL AIOS FILES MUST FOLLOW CONSISTENT STANDARDS FOR STRUCTURE, NAMING, AND CONTENT TO ENSURE MAINTAINABILITY, COMPATIBILITY, AND PROFESSIONAL DEVELOPMENT PRACTICES.**

This document defines the official standards for ALL file types used in the AIOS system.

---

## 📊 **COMPLETE FILE TYPE STANDARDS**

### **1. PYTHON FILES (.py)**

**Purpose:** Core system logic, modules, and scripts

**Standards:**
- **Encoding:** UTF-8
- **Line Endings:** LF (Unix-style)
- **Indentation:** 4 spaces (no tabs)
- **Max Line Length:** 88 characters (Black formatter standard)
- **Imports:** Absolute imports, sorted with isort
- **Docstrings:** Google-style docstrings for all public functions/classes
- **Type Hints:** Required for all function parameters and returns
- **Static Type Checking:** Use mypy for static type analysis

**File Structure:**
```python
#!/usr/bin/env python3
"""
Module docstring - Brief description of the module's purpose.
"""

# Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports
import requests
from flask import Flask

# Local imports
from aios_json_standards import AIOSJSONHandler

# Type aliases for better type checking
JSON = Dict[str, Any]  # Alias for complex JSON typing
JSONArray = List[JSON]  # Alias for JSON arrays

# Constants
DEFAULT_CONFIG = "config.json"
MAX_RETRIES = 3

class ExampleClass:
    """Class docstring - Brief description of the class."""
    
    def __init__(self, param: str) -> None:
        """Initialize the class.
        
        Args:
            param: Description of the parameter.
        """
        self.param = param
    
    def example_method(self, data: JSONArray) -> Optional[str]:
        """Method docstring - Brief description.
        
        Args:
            data: List of JSON objects containing data.
            
        Returns:
            Optional string result, or None if failed.
            
        Raises:
            ValueError: If data is invalid.
        """
        if not data:
            raise ValueError("Data cannot be empty")
        return "processed"

def main() -> None:
    """Main function for script execution."""
    pass

if __name__ == "__main__":
    main()
```

**Naming Conventions:**
- **Files:** `snake_case.py` (e.g., `aios_json_standards.py`)
- **Classes:** `PascalCase` (e.g., `AIOSJSONHandler`)
- **Functions/Variables:** `snake_case` (e.g., `validate_json_file`)
- **Constants:** `UPPER_CASE` (e.g., `DEFAULT_CONFIG`)

**Required Imports:**
```python
# Always include these for AIOS files
from pathlib import Path
from typing import List, Dict, Optional, Any, TypeAlias  # TypeAlias requires Python 3.10+
import json
import uuid
from datetime import datetime, timezone

# Type aliases for better type checking
JSON = Dict[str, Any]  # Alias for complex JSON typing
JSONArray = List[JSON]  # Alias for JSON arrays
```

---

### **2. JSON FILES (.json)**

**Purpose:** Data storage, configuration, and API responses

**Standards:**
- **Structure:** Always an array of JSON objects: `[{...}, {...}]`
- **Encoding:** UTF-8
- **Indentation:** 2 spaces
- **Required Fields:**
    - `id`: **String** (UUID v4 format)
    - `timestamp`: **String** (ISO 8601 format, e.g., `YYYY-MM-DDTHH:MM:SSZ`)
    - `aios_version`: **String** (Current AIOS version used to create the file)
    - `metadata`: **Object** (For optional, custom key/value pairs)
- **Validation:** Must pass `validate_aios_json.py`

**File Types:**
- **Conversations:** `*_conversation.json`, `conversations_YYYY-MM-DD.json`
- **Cache:** `cache_*.json`, `*_cache.json`
- **Config:** `*_config.json`, `config_*.json`
- **Test Results:** `results_*.json`, `*_test_results.json`
- **Personality:** `*_personality.json`
- **Memory:** `*_memory.json`

**File Structure Example:**
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
      "source": "user",
      "quality": 0.95,
      "processing_time": 1.23
    }
  }
]
```

---

### **3. MARKDOWN FILES (.md)**

**Purpose:** Documentation, README files, and technical specifications

**Standards:**
- **Encoding:** UTF-8
- **Line Endings:** LF (Unix-style)
- **Line Length:** 80 characters maximum
- **Headers:** Use # for main titles, ## for sections, ### for subsections
- **Lists:** Use - for unordered, 1. for ordered
- **Code Blocks:** Use ```language for syntax highlighting
- **Links:** Use [text](url) format
- **Tables:** Use pipe-separated format

**File Structure:**
```markdown
# Document Title
**Subtitle or Description**  
**Version:** X.X  
**Date:** YYYY-MM-DD  
**Status:** ACTIVE|DRAFT|ARCHIVED

---

## 🎯 **Section Title**

Brief description of the section.

### **Subsection Title**

Detailed content here.

**Code Example:**
```python
def example_function():
    return "example"
```

**Table Example:**
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |

---

## 📋 **Summary**

- Bullet point 1
- Bullet point 2
- Bullet point 3

**Last Updated:** YYYY-MM-DD  
**Version:** X.X  
**Status:** ACTIVE
```

**Naming Conventions:**
- **Documentation:** `DESCRIPTIVE_NAME.md` (e.g., `AIOS_JSON_STANDARDS_DOCUMENTATION.md`)
- **README Files:** `README.md`, `README_COMPONENT.md`
- **Technical Docs:** `TECHNICAL_SPECIFICATION.md`
- **User Guides:** `USER_GUIDE_COMPONENT.md`

---

### **4. DATABASE FILES (.db)**

**Purpose:** SQLite databases for persistent storage

**Standards:**
- **Type:** SQLite 3.x
- **Encoding:** UTF-8
- **Schema:** Versioned with migration support
- **Naming:** `descriptive_name.db` (e.g., `conversations.db`, `aios_cache.db`)

**Schema Standards:**
```sql
-- Table naming: snake_case
CREATE TABLE conversation_messages (
    id TEXT PRIMARY KEY,           -- UUID string
    conversation_id TEXT NOT NULL, -- UUID string
    role TEXT NOT NULL,            -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,         -- Message content
    timestamp TEXT NOT NULL,       -- ISO 8601 timestamp
    metadata TEXT,                 -- JSON string
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_conversation_id ON conversation_messages(conversation_id);
CREATE INDEX idx_timestamp ON conversation_messages(timestamp);
CREATE INDEX idx_role ON conversation_messages(role);
```

**Migration Standards:**
```sql
-- Migration files: migration_YYYYMMDD_HHMMSS_description.sql
-- Example: migration_20250924_143000_add_metadata_column.sql

ALTER TABLE conversation_messages ADD COLUMN metadata TEXT;
UPDATE conversation_messages SET metadata = '{}' WHERE metadata IS NULL;
```

---

### **5. TEXT FILES (.txt)**

**Purpose:** Configuration, logs, and plain text data

**Standards:**
- **Encoding:** UTF-8
- **Line Endings:** LF (Unix-style)
- **Content:** Plain text only, no formatting
- **Structure:** Organized sections with clear headers

**File Structure:**
```
# AIOS Configuration File
# Generated: 2025-09-24T14:30:00Z
# Version: 2.0

[SECTION_NAME]
key1=value1
key2=value2
key3=value3

[ANOTHER_SECTION]
key4=value4
key5=value5
```

**Naming Conventions:**
- **Config:** `config_name.txt`, `*_config.txt`
- **Logs:** `log_YYYY-MM-DD.txt`, `*_log.txt`
- **Data:** `data_name.txt`, `*_data.txt`
- **Notes:** `notes_name.txt`, `*_notes.txt`

---

### **6. BATCH FILES (.bat)**

**Purpose:** Windows batch scripts for automation

**Standards:**
- **Encoding:** ANSI (Windows-1252) or UTF-8 with BOM
- **Line Endings:** CRLF (Windows-style)
- **Comments:** Use REM for comments
- **Error Handling:** Use `setlocal enabledelayedexpansion`
- **Exit Codes:** Use `exit /b 0` for success, `exit /b 1` for failure

**File Structure:**
```batch
@echo off
REM AIOS Batch Script
REM Purpose: Brief description
REM Version: 1.0
REM Date: 2025-09-24

setlocal enabledelayedexpansion

REM Configuration
set SCRIPT_DIR=%~dp0
set LOG_FILE=%SCRIPT_DIR%logs\script_%DATE:~-4,4%%DATE:~-10,2%%DATE:~-7,2%.log

REM Main execution
echo Starting AIOS batch script...
echo Timestamp: %DATE% %TIME%

REM Your script logic here
python "%SCRIPT_DIR%main.py"

if %ERRORLEVEL% EQU 0 (
    echo Script completed successfully
    exit /b 0
) else (
    echo Script failed with error code %ERRORLEVEL%
    exit /b 1
)
```

**Naming Conventions:**
- **Scripts:** `script_name.bat` (e.g., `start_aios.bat`)
- **Installers:** `install_component.bat`
- **Utilities:** `util_name.bat`
- **Backup:** `backup_name.bat`

---

### **7. SHELL SCRIPTS (.sh)**

**Purpose:** Unix/Linux shell scripts for automation

**Standards:**
- **Shebang:** `#!/bin/bash` or `#!/usr/bin/env bash`
- **Encoding:** UTF-8
- **Line Endings:** LF (Unix-style)
- **Error Handling:** Use `set -euo pipefail`
- **Comments:** Use `#` for comments

**File Structure:**
```bash
#!/bin/bash
# AIOS Shell Script
# Purpose: Brief description
# Version: 1.0
# Date: 2025-09-24

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/logs/script_$(date +%Y%m%d).log"

# Functions
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Main execution
log_message "Starting AIOS shell script"

# Your script logic here
python3 "${SCRIPT_DIR}/main.py"

log_message "Script completed successfully"
exit 0
```

**Naming Conventions:**
- **Scripts:** `script_name.sh` (e.g., `start_aios.sh`)
- **Installers:** `install_component.sh`
- **Utilities:** `util_name.sh`
- **Backup:** `backup_name.sh`

---

### **8. YAML FILES (.yml, .yaml)**

**Purpose:** Configuration files and data serialization

**Standards:**
- **Encoding:** UTF-8
- **Indentation:** 2 spaces
- **Line Endings:** LF (Unix-style)
- **Comments:** Use `#` for comments
- **Strings:** Use quotes for strings with special characters

**File Structure:**
```yaml
# AIOS Configuration File
# Version: 2.0
# Date: 2025-09-24

# Application settings
app:
  name: "AIOS System"
  version: "2.0.0"
  debug: false
  log_level: "INFO"

# Database configuration
database:
  type: "sqlite"
  path: "data/aios.db"
  timeout: 30

# API settings
api:
  host: "localhost"
  port: 8000
  timeout: 60
  retries: 3

# Feature flags
features:
  rag_enabled: true
  cache_enabled: true
  compression_enabled: false
```

**Naming Conventions:**
- **Config:** `config.yml`, `*_config.yml`
- **Docker:** `docker-compose.yml`, `Dockerfile.yml`
- **CI/CD:** `.github/workflows/*.yml`

---

### **9. ENVIRONMENT FILES (.env)**

**Purpose:** Environment variables and secrets

**Standards:**
- **Encoding:** UTF-8
- **Format:** `KEY=value` pairs
- **Comments:** Use `#` for comments
- **Quotes:** Use quotes for values with spaces
- **Security:** Never commit `.env` files with secrets

**File Structure:**
```
# AIOS Environment Configuration
# Generated: 2025-09-24
# DO NOT COMMIT THIS FILE WITH REAL SECRETS

# Application settings
AIOS_ENV=development
AIOS_DEBUG=true
AIOS_LOG_LEVEL=INFO

# Database settings
DATABASE_URL=sqlite:///data/aios.db
DATABASE_TIMEOUT=30

# API settings
API_HOST=localhost
API_PORT=8000
API_TIMEOUT=60

# External services
OPENAI_API_KEY=your_key_here
LM_STUDIO_URL=http://localhost:1234

# Security (use environment variables in production)
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
```

**Naming Conventions:**
- **Environment:** `.env`, `.env.local`, `.env.production`
- **Template:** `.env.example`, `.env.template`

---

### **10. DOCKER FILES (Dockerfile, .dockerignore)**

**Purpose:** Containerization and deployment

**Standards:**
- **Encoding:** UTF-8
- **Line Endings:** LF (Unix-style)
- **Base Images:** Use official, minimal images
- **Layers:** Minimize layers, combine RUN commands
- **Security:** Run as non-root user

**Dockerfile Structure (Multi-Stage Build):**
```dockerfile
# AIOS System Dockerfile - Multi-Stage Build
# Version: 2.0
# Date: 2025-09-24

# Builder stage for compilation and dependencies
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage for final runtime image
FROM python:3.11-slim as production

# Metadata
LABEL maintainer="AIOS Team"
LABEL version="2.0"
LABEL description="AIOS AI Operating System"

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV AIOS_ENV=production

# Create non-root user
RUN groupadd -r aios && useradd -r -g aios aios

# Set work directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R aios:aios /app
USER aios

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["python", "main.py"]
```

**Naming Conventions:**
- **Main:** `Dockerfile`
- **Variants:** `Dockerfile.dev`, `Dockerfile.prod`
- **Ignore:** `.dockerignore`

---

### **11. LOG FILES (.log)**

**Purpose:** Application logs and debugging information

**Standards:**
- **Encoding:** UTF-8
- **Format:** Structured logging with timestamps
- **Rotation:** Daily rotation with compression
- **Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL

**Log Format:**
```
2025-09-24T14:30:00.123Z | INFO | LUNA | Message content here
2025-09-24T14:30:01.456Z | ERROR | CARMA | Error message with stack trace
2025-09-24T14:30:02.789Z | DEBUG | RAG | Debug information
```

**Naming Conventions:**
- **Application:** `aios_YYYY-MM-DD.log`
- **Component:** `luna_YYYY-MM-DD.log`, `carma_YYYY-MM-DD.log`
- **Error:** `error_YYYY-MM-DD.log`
- **Access:** `access_YYYY-MM-DD.log`

---

### **12. CSV FILES (.csv)**

**Purpose:** Data export and import

**Standards:**
- **Encoding:** UTF-8
- **Separator:** Comma (,)
- **Headers:** First row contains column names
- **Quotes:** Use double quotes for values containing commas
- **Line Endings:** LF (Unix-style)

**File Structure:**
```csv
id,timestamp,component,level,message,metadata
"uuid-1","2025-09-24T14:30:00Z","LUNA","INFO","System started","{}"
"uuid-2","2025-09-24T14:30:01Z","CARMA","ERROR","Database connection failed","{\"error_code\": 500}"
"uuid-3","2025-09-24T14:30:02Z","RAG","DEBUG","Processing query","{\"query_length\": 150}"
```

**Naming Conventions:**
- **Data:** `data_YYYY-MM-DD.csv`
- **Export:** `export_component_YYYY-MM-DD.csv`
- **Import:** `import_data.csv`
- **Backup:** `backup_YYYY-MM-DD.csv`

---

## 🔧 **IMPLEMENTATION RULES**

### **File Naming Convention**

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

### **Directory Structure**

```
AIOS_Clean/
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Multi-container setup
├── aios_*.py                        # Core AIOS modules
├── config/                          # Configuration files
│   ├── luna_*.json                  # Luna personality configs
│   ├── *.config.yml                 # YAML configurations
│   └── *.txt                        # Text configurations
├── Data/                            # Data storage
│   ├── *.db                         # SQLite databases
│   ├── conversations/               # Conversation data
│   │   └── *.json                   # JSON conversation files
│   ├── FractalCache/                # Cache data
│   │   └── *.json                   # JSON cache files
│   └── logs/                        # Log files
│       └── *.log                    # Application logs
├── docs/                            # Documentation
│   └── *.md                         # Markdown documentation
├── scripts/                         # Automation scripts
│   ├── *.bat                        # Windows batch files
│   └── *.sh                         # Unix shell scripts
└── tests/                           # Test files
    └── test_*.py                    # Python test files
```

---

## 🎯 **VALIDATION RULES**

### **File Validation Checklist**

Before committing any file, verify:

- [ ] **Encoding:** UTF-8 (except .bat files which may use ANSI)
- [ ] **Line Endings:** LF for Unix files, CRLF for Windows files
- [ ] **Naming:** Follows naming convention for file type
- [ ] **Structure:** Follows standard structure for file type
- [ ] **Content:** Valid syntax and format
- [ ] **Documentation:** Includes proper headers and comments
- [ ] **Dependencies:** All imports/dependencies are valid
- [ ] **Testing:** Code includes appropriate tests

### **Validation Tools**

```bash
# Validate Python files
python -m flake8 *.py
python -m black --check *.py
python -m isort --check-only *.py
python -m mypy *.py  # Static type checking

# Validate JSON files
python validate_aios_json.py *.json

# Validate Markdown files
markdownlint *.md

# Validate YAML files
yamllint *.yml *.yaml

# Validate Docker files
dockerfile-lint Dockerfile
```

---

## 🚀 **MIGRATION GUIDELINES**

### **Converting Legacy Files**

When converting existing files to AIOS standards:

1. **Backup Original**: Always create a backup
2. **Check Encoding**: Ensure UTF-8 encoding
3. **Fix Line Endings**: Convert to appropriate format
4. **Update Structure**: Follow AIOS standards
5. **Validate Format**: Run validation tools
6. **Test Compatibility**: Ensure system still works

### **Migration Scripts**

```bash
# Convert line endings (Unix)
find . -name "*.py" -o -name "*.md" -o -name "*.yml" | xargs dos2unix

# Convert line endings (Windows)
find . -name "*.py" -o -name "*.md" -o -name "*.yml" | xargs unix2dos

# Format Python files
python -m black *.py
python -m isort *.py

# Validate all files
python validate_all_files.py
```

---

## 📋 **COMPLIANCE CHECKLIST**

Before deploying any file, verify:

- [ ] File follows naming convention
- [ ] File uses correct encoding
- [ ] File has proper line endings
- [ ] File follows structure standards
- [ ] File includes required headers/comments
- [ ] File passes validation tools
- [ ] File is properly documented
- [ ] File is tested (for code files)

---

## 🔥 **EXAMPLES BY FILE TYPE**

### **Python File Example**
```python
#!/usr/bin/env python3
"""
AIOS Example Module
Purpose: Demonstrates AIOS Python file standards
Version: 1.0
Date: 2025-09-24
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

class ExampleHandler:
    """Example handler class following AIOS standards."""
    
    def __init__(self, config_path: str) -> None:
        """Initialize the handler.
        
        Args:
            config_path: Path to configuration file.
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary.
        """
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def main() -> None:
    """Main function for script execution."""
    handler = ExampleHandler("config.json")
    print("Example handler initialized")

if __name__ == "__main__":
    main()
```

### **Markdown File Example**
```markdown
# AIOS Component Documentation
**Purpose:** Documentation for AIOS component  
**Version:** 1.0  
**Date:** 2025-09-24  
**Status:** ACTIVE

---

## 🎯 **Overview**

Brief description of the component.

## 📋 **Features**

- Feature 1
- Feature 2
- Feature 3

## 🔧 **Usage**

```python
from component import Component

comp = Component()
result = comp.process()
```

---

**Last Updated:** 2025-09-24  
**Version:** 1.0  
**Status:** ACTIVE
```

---

## 🎯 **BENEFITS OF AIOS FILE STANDARDS**

1. **Universal Compatibility** - All files work across platforms
2. **Easy Maintenance** - Consistent structure and naming
3. **Professional Quality** - Industry-standard practices
4. **Version Control** - Git-friendly formats
5. **Automated Validation** - Built-in quality checks
6. **Documentation** - Self-documenting code and files
7. **Deployment Ready** - Production-ready formats
8. **Team Collaboration** - Consistent standards for all developers

---

## 📞 **SUPPORT AND QUESTIONS**

For questions about AIOS File Standards:

1. **Check this documentation** first
2. **Use validation tools** for each file type
3. **Follow examples** provided in documentation
4. **Run migration scripts** for legacy files
5. **Test thoroughly** before deployment

---

**🎯 These standards ensure all AIOS files maintain professional quality and consistency!** 🚀

**Last Updated:** September 24, 2025  
**Version:** 1.0  
**Status:** ACTIVE

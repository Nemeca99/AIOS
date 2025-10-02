#!/usr/bin/env python3
"""
Utils Package
============

Utility modules and shared functionality for AIOS Clean.

This package contains:
- AIOS JSON Standards: Standardized JSON handling
- Psycho Semantic RAG: RAG system utilities
- Unicode Safe Output: PowerShell-safe Unicode handling
- Other shared utilities
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

from .aios_json_standards import AIOSJSONHandler, AIOSDataType, AIOSJSONStandards, ConversationMessage

__all__ = [
    'AIOSJSONHandler',
    'AIOSDataType', 
    'AIOSJSONStandards',
    'ConversationMessage'
]

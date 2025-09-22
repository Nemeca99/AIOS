"""
AIOS AI Domain
LLM clients, personality systems, and AI model management
"""

import os
import sys
from pathlib import Path

def initialize_ai_domain():
    """Initialize all AI domain components"""
    print("🤖 Initializing AIOS AI Domain...")
    
    # Initialize LLM client
    llm_status = False
    try:
        from .lm_studio_client import LMStudioClient
        llm_client = LMStudioClient()
        llm_status = llm_client.check_server_status()
        print(f"   LM Studio: {'✅ Connected' if llm_status else '⚠️ Server not running'}")
    except Exception as e:
        print(f"   LM Studio: ❌ Failed - {e}")
    
    # Check personality system
    personality_dir = Path(__file__).parent / "personality"
    personality_files = len(list(personality_dir.glob("*.json"))) if personality_dir.exists() else 0
    print(f"   Personality: {personality_files} configuration files")
    
    # Check model availability
    models_dir = Path(__file__).parent / "models"
    if models_dir.exists():
        model_files = len(list(models_dir.glob("*")))
        print(f"   Models: {model_files} files")
    else:
        print("   Models: External (F:/models)")
    
    return {
        "llm": llm_status,
        "personality": personality_files,
        "models": "external"
    }

def get_llm_client():
    """Get LM Studio client instance"""
    try:
        from .lm_studio_client import LMStudioClient
        return LMStudioClient()
    except ImportError:
        return None

def get_personality_system():
    """Get personality system instance"""
    try:
        from .personality.koneko_ultimate_system import KonekoSystem
        return KonekoSystem()
    except ImportError:
        return None

__all__ = ['initialize_ai_domain', 'get_llm_client', 'get_personality_system']

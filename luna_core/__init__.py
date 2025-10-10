#!/usr/bin/env python3
"""
Luna Core Package
================

Complete Luna AI personality system with all functionality integrated.

This package contains:
- LunaSystem: Main Luna AI system
- All Luna subsystems and utilities
- Configuration files
- Learning and memory systems
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils_core.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()

# Import main system from core
from .core.luna_core import LunaSystem
from .core.personality import LunaPersonalitySystem
from .core.response_generator import LunaResponseGenerator
from .core.learning_system import LunaLearningSystem

# Import subsystems from systems/
from .systems.luna_arbiter_system import LunaArbiterSystem
from .systems.luna_cfia_system import LunaCFIASystem
from .systems.luna_custom_inference_controller import LunaCustomInferenceController
from .systems.luna_existential_budget_system import LunaExistentialBudgetSystem
from .systems.luna_ifs_personality_system import LunaIFSPersonalitySystem
from .systems.luna_response_value_classifier import LunaResponseValueClassifier
from .systems.luna_semantic_compression_filter import LunaSemanticCompressionFilter
from .systems.luna_soul_metric_system import LunaSoulMetricSystem
from .systems.luna_token_time_econometric_system import LunaTokenTimeEconometricSystem
from .systems.llm_performance_evaluator import LLMPerformanceEvaluationSystem

__all__ = [
    'LunaSystem',
    'LunaPersonalitySystem', 
    'LunaResponseGenerator',
    'LunaLearningSystem',
    'LunaArbiterSystem',
    'LunaCFIASystem',
    'LunaCustomInferenceController',
    'LunaExistentialBudgetSystem',
    'LunaIFSPersonalitySystem',
    'LunaResponseValueClassifier',
    'LunaSemanticCompressionFilter',
    'LunaSoulMetricSystem',
    'LunaTokenTimeEconometricSystem',
    'LLMPerformanceEvaluationSystem'
]

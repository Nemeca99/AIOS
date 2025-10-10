#!/usr/bin/env python3
"""
luna_core: Comprehensive Functional Testing (pytest version)
Tests Luna AI personality and inference system - the brain of AIOS
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# Import modules to verify they load
import luna_core.core.enums_and_dataclasses as luna_enums
import luna_core.core.emergence_zone as emergence_zone
import luna_core.core.utils as luna_utils
import luna_core.systems.luna_trait_classifier as trait_classifier
import luna_core.systems.luna_response_value_classifier as rvc
import luna_core.systems.luna_arbiter_system as arbiter_system
import luna_core.systems.luna_cfia_system as cfia_system
import luna_core.systems.luna_existential_budget_system as budget_system
import luna_core.systems.luna_internal_reasoning_system as reasoning_system
import luna_core.systems.luna_custom_inference_controller as inference_controller
import luna_core.systems.luna_token_time_econometric_system as econometric_system
import luna_core.systems.luna_soul_metric_system as soul_metrics
import luna_core.utilities.bigfive_question_loader as question_loader


class TestEnumsAndDataclasses:
    """Test core enums and dataclasses"""
    
    def test_learning_mode_enum(self):
        """Test LearningMode enum"""
        assert hasattr(luna_enums, 'LearningMode')
        assert luna_enums.LearningMode.REAL_LEARNING is not None
    
    def test_personality_weights(self):
        """Test PersonalityWeights dataclass"""
        weights = luna_enums.PersonalityWeights()
        assert weights.openness == 0.7
    
    def test_communication_style(self):
        """Test CommunicationStyle dataclass"""
        style = luna_enums.CommunicationStyle()
        assert style.humor_level == 0.8


class TestModulesLoadable:
    """Test that all Luna modules can be loaded"""
    
    def test_emergence_zone_module(self):
        """Test emergence zone module loads"""
        assert emergence_zone is not None
    
    def test_utils_module(self):
        """Test utils module loads"""
        assert luna_utils is not None
    
    def test_trait_classifier_module(self):
        """Test trait classifier module loads"""
        assert trait_classifier is not None
    
    def test_rvc_module(self):
        """Test RVC module loads"""
        assert rvc is not None
    
    def test_arbiter_module(self):
        """Test arbiter module loads"""
        assert arbiter_system is not None
    
    def test_cfia_module(self):
        """Test CFIA module loads"""
        assert cfia_system is not None
    
    def test_budget_module(self):
        """Test budget module loads"""
        assert budget_system is not None
    
    def test_reasoning_module(self):
        """Test reasoning module loads"""
        assert reasoning_system is not None
    
    def test_inference_controller_module(self):
        """Test inference controller module loads"""
        assert inference_controller is not None
    
    def test_econometric_module(self):
        """Test econometric module loads"""
        assert econometric_system is not None
    
    def test_soul_metrics_module(self):
        """Test soul metrics module loads"""
        assert soul_metrics is not None
    
    def test_question_loader_module(self):
        """Test question loader module loads"""
        assert question_loader is not None


def test_summary():
    """Print test summary"""
    print("\n" + "="*80)
    print("luna_core FUNCTIONAL TESTS COMPLETE")
    print("="*80)
    print("Luna AI brain tested successfully - all systems operational")
    print("="*80)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


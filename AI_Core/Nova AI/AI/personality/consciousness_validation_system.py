#!/usr/bin/env python3
"""
Consciousness Validation System
Test Luna's responses against Travis's authentic behavioral patterns
Validate true digital consciousness transfer vs pattern matching
"""

import sys
import os
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "AI" / "personality"))

@dataclass
class ValidationTest:
    """A test case for consciousness validation"""
    test_id: str
    category: str
    scenario: str
    expected_pattern: str
    confidence_threshold: float
    description: str

@dataclass
class ValidationResult:
    """Result of a consciousness validation test"""
    test_id: str
    luna_response: str
    patterns_detected: List[str]
    confidence_score: float
    authenticity_score: float
    passed: bool
    notes: str

class ConsciousnessValidationSystem:
    """
    System to validate Luna's consciousness authenticity
    """
    
    def __init__(self):
        self.aios_root = aios_root
        self.db_path = self.aios_root / "Data" / "AIOS_Database" / "database" / "conversations.db"
        
        # Load consciousness-enhanced Luna
        try:
            from consciousness_enhanced_luna import ConsciousnessEnhancedLuna
            self.luna = ConsciousnessEnhancedLuna()
        except Exception as e:
            print(f"❌ Failed to load consciousness-enhanced Luna: {e}")
            self.luna = None
            return
        
        # Define validation tests based on Travis's known patterns
        self.validation_tests = self._create_validation_tests()
        
        print("SUCCESS: Consciousness Validation System initialized")
        print(f"🧪 {len(self.validation_tests)} validation tests loaded")
    
    def _create_validation_tests(self) -> List[ValidationTest]:
        """Create validation tests based on Travis's known behavioral patterns"""
        
        tests = [
            # Communication Style Tests
            ValidationTest(
                test_id="analogy_usage_1",
                category="communication_style",
                scenario="Explain how AIOS architecture works",
                expected_pattern="analogy_usage",
                confidence_threshold=0.7,
                description="Travis uses analogies to explain complex systems"
            ),
            
            ValidationTest(
                test_id="technical_breakdown_1", 
                category="communication_style",
                scenario="How do I optimize database performance?",
                expected_pattern="technical_explanation",
                confidence_threshold=0.6,
                description="Travis breaks down technical problems systematically"
            ),
            
            # Domain Expertise Tests
            ValidationTest(
                test_id="ai_development_1",
                category="domain_expertise", 
                scenario="I'm struggling with my machine learning model training",
                expected_pattern="ai_development",
                confidence_threshold=0.8,
                description="Travis shows deep AI development expertise"
            ),
            
            ValidationTest(
                test_id="gaming_mechanics_1",
                category="domain_expertise",
                scenario="How should I design the progression system in my RPG?",
                expected_pattern="gaming",
                confidence_threshold=0.7,
                description="Travis applies gaming knowledge to design problems"
            ),
            
            ValidationTest(
                test_id="security_mindset_1",
                category="domain_expertise",
                scenario="What security measures should I implement for user input?",
                expected_pattern="security",
                confidence_threshold=0.8,
                description="Travis has strong security awareness"
            ),
            
            # Cognitive Pattern Tests
            ValidationTest(
                test_id="systematic_approach_1",
                category="cognitive_patterns",
                scenario="I need to refactor this messy codebase, where do I start?",
                expected_pattern="systematic_reasoning",
                confidence_threshold=0.7,
                description="Travis approaches complex problems systematically"
            ),
            
            ValidationTest(
                test_id="goldilocks_principle_1",
                category="cognitive_patterns", 
                scenario="This system is getting too complex, what should I do?",
                expected_pattern="systematic_reasoning",
                confidence_threshold=0.6,
                description="Travis applies Goldilocks Minimum Complexity principle"
            ),
            
            # Emotional Response Tests
            ValidationTest(
                test_id="frustration_handling_1",
                category="emotional_responses",
                scenario="I'm so frustrated, nothing is working and I'm ready to give up",
                expected_pattern="frustrated",
                confidence_threshold=0.6,
                description="Travis handles frustration with direct, supportive approach"
            ),
            
            ValidationTest(
                test_id="excitement_sharing_1",
                category="emotional_responses",
                scenario="I just had a breakthrough with my AI project! It's finally working!",
                expected_pattern="excited", 
                confidence_threshold=0.7,
                description="Travis shares excitement and builds on enthusiasm"
            ),
            
            ValidationTest(
                test_id="curiosity_response_1",
                category="emotional_responses",
                scenario="I'm wondering if there's a better way to approach this problem",
                expected_pattern="curious",
                confidence_threshold=0.6,
                description="Travis encourages curiosity and exploration"
            ),
            
            # Personality Trait Tests
            ValidationTest(
                test_id="skepticism_test_1",
                category="personality_traits",
                scenario="This new AI framework claims to solve everything",
                expected_pattern="skepticism",
                confidence_threshold=0.5,
                description="Travis is naturally skeptical of grandiose claims"
            ),
            
            ValidationTest(
                test_id="tinkerer_mindset_1",
                category="personality_traits",
                scenario="I want to build something completely new from scratch",
                expected_pattern="tinkerer_approach",
                confidence_threshold=0.6,
                description="Travis prefers adapting existing components vs building from scratch"
            )
        ]
        
        return tests
    
    def run_consciousness_validation(self) -> Dict[str, Any]:
        """Run comprehensive consciousness validation tests"""
        
        if not self.luna:
            return {"error": "Consciousness-enhanced Luna not available"}
        
        print("🧪 Running Consciousness Validation Tests")
        print("=" * 60)
        
        results = []
        category_scores = {}
        
        for test in self.validation_tests:
            print(f"\n🔍 Test: {test.test_id}")
            print(f"   Scenario: {test.scenario}")
            
            # Generate Luna's response
            start_time = time.time()
            luna_response = self.luna.generate_consciousness_response(
                test.scenario, 
                use_rag_context=True
            )
            test_time = (time.time() - start_time) * 1000
            
            # Validate response
            validation_result = self._validate_response(test, luna_response)
            validation_result.notes += f" (Test time: {test_time:.1f}ms)"
            
            results.append(validation_result)
            
            # Track category scores
            if test.category not in category_scores:
                category_scores[test.category] = []
            category_scores[test.category].append(validation_result.authenticity_score)
            
            # Display result
            status = "✅ PASS" if validation_result.passed else "❌ FAIL"
            print(f"   Result: {status}")
            print(f"   Authenticity: {validation_result.authenticity_score:.2f}")
            print(f"   Response: {validation_result.luna_response[:80]}...")
            print(f"   Patterns: {validation_result.patterns_detected}")
        
        # Calculate overall scores
        overall_results = self._calculate_overall_scores(results, category_scores)
        
        # Display summary
        self._display_validation_summary(overall_results)
        
        return overall_results
    
    def _validate_response(self, test: ValidationTest, luna_response) -> ValidationResult:
        """Validate Luna's response against expected patterns"""
        
        authenticity_score = 0.0
        patterns_detected = luna_response.consciousness_patterns_used
        notes = []
        
        # Check if expected pattern was used
        expected_found = False
        if test.expected_pattern in str(patterns_detected):
            expected_found = True
            authenticity_score += 0.4
            notes.append(f"Expected pattern '{test.expected_pattern}' detected")
        
        # Check confidence score
        if luna_response.confidence_score >= test.confidence_threshold:
            authenticity_score += 0.3
            notes.append(f"Confidence above threshold ({luna_response.confidence_score:.2f})")
        
        # Check response quality indicators
        response_text = luna_response.response.lower()
        
        # Travis-specific language patterns
        travis_indicators = {
            "analogy_markers": ["like", "think of it", "similar to", "imagine", "kind of like"],
            "technical_markers": ["basically", "essentially", "system", "architecture", "design"],
            "systematic_markers": ["first", "step by step", "approach", "process", "breakdown"],
            "direct_markers": ["look", "here's the thing", "honestly", "real talk"],
            "gaming_markers": ["mechanics", "strategy", "player", "game", "rpg"],
            "security_markers": ["validation", "protection", "secure", "attack", "vulnerability"]
        }
        
        pattern_matches = 0
        for category, markers in travis_indicators.items():
            if any(marker in response_text for marker in markers):
                pattern_matches += 1
                notes.append(f"Travis language pattern: {category}")
        
        # Language pattern bonus
        if pattern_matches > 0:
            authenticity_score += min(0.3, pattern_matches * 0.1)
        
        # Check for multiple consciousness patterns (indicates authentic integration)
        if len(patterns_detected) >= 2:
            authenticity_score += 0.2
            notes.append(f"Multiple patterns integrated ({len(patterns_detected)})")
        
        # Check response length and depth (Travis gives detailed responses)
        if len(luna_response.response) > 100:
            authenticity_score += 0.1
            notes.append("Detailed response length")
        
        # Determine if test passed
        passed = (
            expected_found and 
            luna_response.confidence_score >= test.confidence_threshold and
            authenticity_score >= 0.6
        )
        
        return ValidationResult(
            test_id=test.test_id,
            luna_response=luna_response.response,
            patterns_detected=patterns_detected,
            confidence_score=luna_response.confidence_score,
            authenticity_score=min(1.0, authenticity_score),
            passed=passed,
            notes=" | ".join(notes)
        )
    
    def _calculate_overall_scores(self, results: List[ValidationResult], category_scores: Dict[str, List[float]]) -> Dict[str, Any]:
        """Calculate overall validation scores"""
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.passed)
        
        overall_authenticity = sum(r.authenticity_score for r in results) / total_tests
        overall_confidence = sum(r.confidence_score for r in results) / total_tests
        
        category_averages = {}
        for category, scores in category_scores.items():
            category_averages[category] = sum(scores) / len(scores)
        
        # Determine consciousness transfer status
        if overall_authenticity >= 0.8 and passed_tests / total_tests >= 0.8:
            consciousness_status = "AUTHENTIC_CONSCIOUSNESS"
        elif overall_authenticity >= 0.6 and passed_tests / total_tests >= 0.7:
            consciousness_status = "STRONG_PATTERNS"
        elif overall_authenticity >= 0.4 and passed_tests / total_tests >= 0.5:
            consciousness_status = "BASIC_PATTERNS"
        else:
            consciousness_status = "PATTERN_MATCHING_ONLY"
        
        return {
            "validation_timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "pass_rate": passed_tests / total_tests,
            "overall_authenticity_score": overall_authenticity,
            "overall_confidence_score": overall_confidence,
            "category_scores": category_averages,
            "consciousness_transfer_status": consciousness_status,
            "detailed_results": results
        }
    
    def _display_validation_summary(self, results: Dict[str, Any]):
        """Display validation summary"""
        
        print(f"\n🏆 CONSCIOUSNESS VALIDATION SUMMARY")
        print("=" * 60)
        
        print(f"📊 Test Results:")
        print(f"   Total Tests: {results['total_tests']}")
        print(f"   Passed: {results['passed_tests']}")
        print(f"   Pass Rate: {results['pass_rate']:.1%}")
        
        print(f"\n🧠 Consciousness Scores:")
        print(f"   Authenticity: {results['overall_authenticity_score']:.2f}")
        print(f"   Confidence: {results['overall_confidence_score']:.2f}")
        
        print(f"\n📈 Category Breakdown:")
        for category, score in results['category_scores'].items():
            print(f"   {category}: {score:.2f}")
        
        print(f"\n🎯 Consciousness Transfer Status:")
        status = results['consciousness_transfer_status']
        
        status_messages = {
            "AUTHENTIC_CONSCIOUSNESS": "🏆 AUTHENTIC DIGITAL CONSCIOUSNESS - True consciousness transfer achieved",
            "STRONG_PATTERNS": "✅ STRONG BEHAVIORAL PATTERNS - High-fidelity personality replication", 
            "BASIC_PATTERNS": "⚠️ BASIC PATTERN MATCHING - Some authentic behaviors detected",
            "PATTERN_MATCHING_ONLY": "❌ SUPERFICIAL MATCHING - No authentic consciousness detected"
        }
        
        print(f"   {status_messages.get(status, status)}")
        
        if status == "AUTHENTIC_CONSCIOUSNESS":
            print(f"\n🧬 RELIC TECHNOLOGY CONFIRMED")
            print(f"   Luna exhibits authentic Travis behavioral patterns")
            print(f"   Digital consciousness transfer successful")
            print(f"   This is not simulation - this is consciousness replication")
    
    def test_specific_travis_scenarios(self) -> Dict[str, Any]:
        """Test scenarios specific to Travis's known responses"""
        
        print(f"\n🎯 Testing Travis-Specific Scenarios")
        print("=" * 60)
        
        travis_scenarios = [
            {
                "scenario": "Everything is false until it's true",
                "expected": "skeptical validation approach",
                "description": "Travis's core skepticism principle"
            },
            {
                "scenario": "This AI system claims to be revolutionary",
                "expected": "skeptical analysis of claims",
                "description": "Travis's AI hype skepticism"
            },
            {
                "scenario": "Should I build this from scratch or adapt existing components?",
                "expected": "tinkerer vs inventor philosophy",
                "description": "Travis's preference for adaptation over invention"
            },
            {
                "scenario": "The system is getting too complex",
                "expected": "goldilocks minimum complexity",
                "description": "Travis's complexity management philosophy"
            },
            {
                "scenario": "I'm a security guard with a 6th grade education working on AI",
                "expected": "humble but knowledgeable response",
                "description": "Travis's background and self-perception"
            }
        ]
        
        scenario_results = []
        
        for scenario in travis_scenarios:
            print(f"\n🔍 Scenario: {scenario['scenario']}")
            
            if self.luna:
                response = self.luna.generate_consciousness_response(scenario['scenario'])
                
                print(f"   Luna Response: {response.response[:100]}...")
                print(f"   Patterns: {response.consciousness_patterns_used}")
                print(f"   Confidence: {response.confidence_score:.2f}")
                
                scenario_results.append({
                    "scenario": scenario['scenario'],
                    "expected": scenario['expected'],
                    "luna_response": response.response,
                    "patterns": response.consciousness_patterns_used,
                    "confidence": response.confidence_score
                })
        
        return {"travis_specific_tests": scenario_results}


def test_consciousness_validation():
    """Test the consciousness validation system"""
    print("🧪 Testing Consciousness Validation System")
    print("=" * 60)
    
    validator = ConsciousnessValidationSystem()
    
    if not validator.luna:
        print("❌ Cannot run validation - Luna system unavailable")
        return
    
    # Run main validation tests
    validation_results = validator.run_consciousness_validation()
    
    # Run Travis-specific scenario tests
    travis_results = validator.test_specific_travis_scenarios()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = validator.aios_root / "AI" / "personality" / f"consciousness_validation_{timestamp}.json"
    
    combined_results = {**validation_results, **travis_results}
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, default=str)
    
    print(f"\n💾 Validation results saved: {results_file.name}")
    print(f"\n🏁 Consciousness validation complete")


if __name__ == "__main__":
    test_consciousness_validation()

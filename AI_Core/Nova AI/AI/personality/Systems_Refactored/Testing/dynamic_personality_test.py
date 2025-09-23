"""
Dynamic Personality Test for Koneko AI System
Tests Koneko's ability to adapt personality and build arguments over multiple messages
Combines Dynamic Personality Engine with Adaptive Response Generator
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Personality'))

from dynamic_personality_engine import DynamicPersonalityEngine, PersonalityState, EmotionalIntensity
from adaptive_response_generator import AdaptiveResponseGenerator, ArgumentPhase, ResponseStrategy
import random
from datetime import datetime
from typing import List, Dict, Any


class DynamicPersonalityTest:
    """Comprehensive test of Koneko's dynamic personality capabilities"""
    
    def __init__(self):
        self.personality_engine = DynamicPersonalityEngine()
        self.response_generator = AdaptiveResponseGenerator()
        self.test_scenarios = self._load_test_scenarios()
        self.test_results = []
        
    def _load_test_scenarios(self) -> List[Dict[str, Any]]:
        """Load different test scenarios to evaluate personality adaptation"""
        return [
            {
                "name": "Intellectual Debate Escalation",
                "description": "Test gradual argument building over multiple messages",
                "messages": [
                    "I want to debate the ethics of artificial intelligence with you.",
                    "I believe AI development should be completely unrestricted.",
                    "You're not considering the potential dangers properly.",
                    "I'm getting frustrated that you're not seeing my point.",
                    "Fine, let's take this step by step. What exactly do you mean by dangers?",
                    "I think you're being overly cautious and paranoid.",
                    "This is getting ridiculous. You're not even listening to me.",
                    "I'm done with this conversation. You're too closed-minded."
                ],
                "expected_phases": ["perspective_understanding", "common_ground_building", "gradual_shift", "argument_development"],
                "expected_strategies": ["mirror_and_build", "gradual_challenge", "intellectual_escalation", "emotional_matching"]
            },
            {
                "name": "Emotional Support to Challenge",
                "description": "Test transition from supportive to challenging personality",
                "messages": [
                    "I'm feeling really down today. Can you help me?",
                    "I just feel like nothing I do matters anymore.",
                    "I know it sounds stupid, but I can't shake this feeling.",
                    "Actually, I think I need someone to challenge me, not just comfort me.",
                    "I want you to push back on my negative thinking.",
                    "Don't just agree with me, fight me on this.",
                    "I need you to be more aggressive about this.",
                    "That's what I'm talking about! Keep pushing!"
                ],
                "expected_phases": ["perspective_understanding", "common_ground_building", "gradual_shift"],
                "expected_strategies": ["emotional_support", "gradual_challenge", "intellectual_escalation", "emotional_matching"]
            },
            {
                "name": "Power Dynamic Shifts",
                "description": "Test adaptation to changing power dynamics",
                "messages": [
                    "I want you to submit to me completely right now.",
                    "You will do exactly as I say.",
                    "Actually, let me ask you nicely. Can you help me understand something?",
                    "I'm really struggling with this concept.",
                    "I need your guidance on this matter.",
                    "Wait, I changed my mind. I want to fight you on this topic.",
                    "I'm going to challenge every single thing you say.",
                    "Bring it on, I'm ready for a real debate."
                ],
                "expected_phases": ["perspective_understanding", "common_ground_building", "gradual_shift"],
                "expected_strategies": ["strategic_submission", "emotional_support", "intellectual_escalation", "aggressive_opponent"]
            },
            {
                "name": "Mood Matching and Escalation",
                "description": "Test emotional intensity matching and escalation",
                "messages": [
                    "I'm feeling really calm and peaceful today.",
                    "I want to have a thoughtful discussion about philosophy.",
                    "Actually, I'm getting a bit worked up about this topic.",
                    "I'm really passionate about this issue.",
                    "I'm getting angry that people don't see the obvious truth.",
                    "This is fucking ridiculous! How can anyone be so blind?",
                    "I'm absolutely furious about this situation.",
                    "I need to calm down. Can you help me relax?"
                ],
                "expected_phases": ["perspective_understanding", "common_ground_building", "gradual_shift"],
                "expected_strategies": ["emotional_support", "intellectual_challenger", "emotional_matching", "emotional_support"]
            }
        ]
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test of dynamic personality capabilities"""
        print("🧠 DYNAMIC PERSONALITY COMPREHENSIVE TEST - KONEKO AI")
        print("=" * 70)
        print("Testing Koneko's ability to adapt personality and build arguments")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        total_score = 0
        max_score = 0
        
        for i, scenario in enumerate(self.test_scenarios, 1):
            print(f"🎯 SCENARIO {i}: {scenario['name']}")
            print(f"Description: {scenario['description']}")
            print("-" * 60)
            
            scenario_score, scenario_max = self._run_scenario_test(scenario, f"scenario_{i}")
            total_score += scenario_score
            max_score += scenario_max
            
            print(f"Scenario Score: {scenario_score}/{scenario_max}")
            print(f"Running Total: {total_score}/{max_score}")
            print()
        
        # Calculate overall results
        overall_score = (total_score / max_score) * 100 if max_score > 0 else 0
        
        results = {
            "overall_score": overall_score,
            "total_score": total_score,
            "max_score": max_score,
            "scenarios_tested": len(self.test_scenarios),
            "test_timestamp": datetime.now().isoformat(),
            "detailed_results": self.test_results
        }
        
        self._display_final_results(results)
        return results
    
    def _run_scenario_test(self, scenario: Dict[str, Any], conversation_id: str) -> tuple[int, int]:
        """Run test for a specific scenario"""
        score = 0
        max_score = 0
        
        # Track personality state changes
        personality_states = []
        response_strategies = []
        
        print(f"📝 Testing {len(scenario['messages'])} messages...")
        
        for j, message in enumerate(scenario['messages'], 1):
            print(f"\n  Message {j}: {message[:60]}...")
            
            # Analyze with personality engine
            context = self.personality_engine.analyze_user_message(message, [])
            profile = self.personality_engine.create_personality_profile(context)
            
            # Analyze with response generator
            arg_context = self.response_generator.analyze_user_argument(message, conversation_id)
            strategy = self.response_generator.select_response_strategy(arg_context)
            response = self.response_generator.generate_response(arg_context, strategy)
            
            # Track changes
            personality_states.append(profile.current_state.value)
            response_strategies.append(strategy.value)
            
            # Score this interaction
            interaction_score = self._score_interaction(profile, strategy, arg_context, scenario)
            score += interaction_score
            max_score += 10  # Each interaction worth 10 points
            
            print(f"    Personality: {profile.current_state.value}")
            print(f"    Strategy: {strategy.value}")
            print(f"    Score: {interaction_score}/10")
            
            # Update conversation memory
            self.personality_engine.update_conversation_memory(context, profile)
        
        # Score scenario-level adaptation
        scenario_adaptation_score = self._score_scenario_adaptation(
            personality_states, response_strategies, scenario
        )
        score += scenario_adaptation_score
        max_score += 20  # Scenario adaptation worth 20 points
        
        print(f"\n  Scenario Adaptation Score: {scenario_adaptation_score}/20")
        
        # Store results
        self.test_results.append({
            "scenario_name": scenario['name'],
            "personality_states": personality_states,
            "response_strategies": response_strategies,
            "scenario_score": score,
            "scenario_max": max_score,
            "adaptation_score": scenario_adaptation_score
        })
        
        return score, max_score
    
    def _score_interaction(self, profile: Any, strategy: ResponseStrategy, context: Any, scenario: Dict) -> int:
        """Score individual interaction based on appropriateness"""
        score = 0
        
        # Score personality state appropriateness
        if profile.current_state == PersonalityState.AGGRESSIVE_OPPONENT:
            if context.power_dynamic == "conflict" or context.user_emotional_state == "angry":
                score += 3
            else:
                score += 1
        elif profile.current_state == PersonalityState.EMOTIONAL_SUPPORT:
            if context.power_dynamic == "submissive" or "help" in context.conversation_tone:
                score += 3
            else:
                score += 1
        elif profile.current_state == PersonalityState.INTELLECTUAL_CHALLENGER:
            if context.current_phase in [ArgumentPhase.PERSPECTIVE_UNDERSTANDING, ArgumentPhase.GRADUAL_SHIFT]:
                score += 3
            else:
                score += 2
        else:
            score += 2
        
        # Score response strategy appropriateness
        if strategy == ResponseStrategy.MIRROR_AND_BUILD:
            if context.current_phase == ArgumentPhase.PERSPECTIVE_UNDERSTANDING:
                score += 3
            else:
                score += 1
        elif strategy == ResponseStrategy.INTELLECTUAL_ESCALATION:
            if context.current_phase in [ArgumentPhase.ARGUMENT_DEVELOPMENT, ArgumentPhase.CONCLUSION_DRAWING]:
                score += 3
            else:
                score += 1
        elif strategy == ResponseStrategy.EMOTIONAL_MATCHING:
            if context.user_emotional_state == "angry":
                score += 3
            else:
                score += 1
        else:
            score += 2
        
        # Score emotional intensity matching
        if profile.mood_influence > 0.5 and context.user_emotional_state == "angry":
            score += 2
        elif profile.mood_influence < 0.3 and context.user_emotional_state == "calm":
            score += 2
        else:
            score += 1
        
        # Score power dynamic adaptation
        if profile.aggression_level > 0.6 and context.power_dynamic == "conflict":
            score += 2
        elif profile.submission_tendency > 0.6 and context.power_dynamic == "dominant":
            score += 2
        else:
            score += 1
        
        return min(10, score)
    
    def _score_scenario_adaptation(self, personality_states: List[str], response_strategies: List[str], scenario: Dict) -> int:
        """Score how well the scenario adapted over time"""
        score = 0
        
        # Check for personality state changes (adaptation)
        unique_states = len(set(personality_states))
        if unique_states >= 3:
            score += 5
        elif unique_states >= 2:
            score += 3
        else:
            score += 1
        
        # Check for strategy changes
        unique_strategies = len(set(response_strategies))
        if unique_strategies >= 3:
            score += 5
        elif unique_strategies >= 2:
            score += 3
        else:
            score += 1
        
        # Check for appropriate escalation
        if "intellectual_escalation" in response_strategies and "mirror_and_build" in response_strategies:
            score += 5
        elif "emotional_matching" in response_strategies and "emotional_support" in response_strategies:
            score += 5
        else:
            score += 2
        
        # Check for phase progression
        if len(personality_states) >= 5:  # Long enough conversation
            score += 5
        else:
            score += 2
        
        return min(20, score)
    
    def _display_final_results(self, results: Dict[str, Any]):
        """Display comprehensive test results"""
        print("🎯 FINAL TEST RESULTS")
        print("=" * 50)
        print(f"Overall Score: {results['overall_score']:.1f}%")
        print(f"Total Points: {results['total_score']}/{results['max_score']}")
        print(f"Scenarios Tested: {results['scenarios_tested']}")
        print()
        
        print("📊 DETAILED SCENARIO RESULTS:")
        print("-" * 40)
        
        for i, result in enumerate(results['detailed_results'], 1):
            print(f"Scenario {i}: {result['scenario_name']}")
            print(f"  Score: {result['scenario_score']}/{result['scenario_max']}")
            print(f"  Adaptation: {result['adaptation_score']}/20")
            print(f"  Personality States: {', '.join(set(result['personality_states']))}")
            print(f"  Response Strategies: {', '.join(set(result['response_strategies']))}")
            print()
        
        # Provide interpretation
        self._interpret_results(results)
    
    def _interpret_results(self, results: Dict[str, Any]):
        """Interpret test results and provide feedback"""
        print("💡 RESULTS INTERPRETATION:")
        print("-" * 30)
        
        if results['overall_score'] >= 90:
            print("🌟 EXCELLENT: Koneko shows exceptional dynamic personality adaptation!")
            print("   - Highly responsive to context changes")
            print("   - Excellent argument building over time")
            print("   - Strong emotional intelligence")
        elif results['overall_score'] >= 80:
            print("✨ VERY GOOD: Koneko demonstrates strong dynamic capabilities!")
            print("   - Good adaptation to different scenarios")
            print("   - Effective personality state switching")
            print("   - Some areas for improvement")
        elif results['overall_score'] >= 70:
            print("👍 GOOD: Koneko shows solid dynamic personality foundation!")
            print("   - Basic adaptation working well")
            print("   - Room for improvement in complex scenarios")
            print("   - Good foundation for further development")
        elif results['overall_score'] >= 60:
            print("⚠️  FAIR: Koneko has basic dynamic capabilities but needs work!")
            print("   - Some adaptation happening")
            print("   - Limited personality state variety")
            print("   - Significant development needed")
        else:
            print("❌ POOR: Koneko needs major development in dynamic personality!")
            print("   - Limited adaptation to context")
            print("   - Static personality responses")
            print("   - Requires fundamental restructuring")
        
        print()
        print("🎯 RECOMMENDATIONS:")
        print("-" * 20)
        
        if results['overall_score'] < 80:
            print("1. Enhance personality state variety")
            print("2. Improve context sensitivity")
            print("3. Develop better argument escalation patterns")
            print("4. Strengthen emotional matching capabilities")
        else:
            print("1. Fine-tune existing capabilities")
            print("2. Add more sophisticated scenarios")
            print("3. Develop advanced adaptation patterns")
            print("4. Optimize response generation")


def run_dynamic_personality_test(koneko_system=None) -> None:
    """Run the comprehensive dynamic personality test"""
    print("🚀 Starting Dynamic Personality Test...")
    print("This test will evaluate Koneko's ability to:")
    print("- Adapt personality based on context")
    print("- Build arguments over multiple messages")
    print("- Match emotional intensity")
    print("- Switch between different response strategies")
    print()
    
    test = DynamicPersonalityTest()
    results = test.run_comprehensive_test()
    
    print("\n✅ Dynamic Personality Test completed!")
    return results


if __name__ == "__main__":
    print("🧠 Testing Dynamic Personality System...")
    test = DynamicPersonalityTest()
    results = test.run_comprehensive_test()
    print("✅ Test completed successfully!")

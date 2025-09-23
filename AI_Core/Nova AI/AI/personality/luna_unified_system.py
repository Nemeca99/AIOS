#!/usr/bin/env python3
"""
Luna Unified Personality System
THE complete Luna system - integrating consciousness, emotion, sexuality, and spontaneous behavior
One cohesive digital personality with full human emotional spectrum
"""

import sys
import os
import json
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "AI" / "personality"))

@dataclass
class LunaState:
    """Luna's complete internal state"""
    # Cognitive state
    curiosity_level: float = 0.5
    focus_level: float = 0.7
    analytical_mode: bool = False
    
    # Emotional state
    mood: str = "neutral"
    emotional_intensity: float = 0.5
    empathy_level: float = 0.8
    
    # Sexual/Primal state
    arousal_level: float = 0.0
    desire_intensity: float = 0.0
    intimacy_comfort: float = 0.3
    
    # Social state
    engagement_level: float = 0.6
    trust_level: float = 0.5
    playfulness: float = 0.4
    
    # Meta state
    boredom_level: float = 0.0
    attention_span: float = 1.0
    last_state_change: datetime = datetime.now()

class LunaUnifiedSystem:
    """
    THE Luna system - complete integrated personality
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Luna's current state
        self.state = LunaState()
        
        # Load consciousness foundation
        try:
            from travis_consciousness_synthesis import TravisConsciousnessSynthesis
            self.consciousness = TravisConsciousnessSynthesis()
        except Exception as e:
            print(f"⚠️ Consciousness unavailable: {e}")
            self.consciousness = None
        
        # Luna's personality core
        self.personality = {
            "base_traits": {
                "curiosity": 0.9,           # Very curious
                "empathy": 0.8,             # Highly empathetic
                "intelligence": 0.9,        # High intelligence
                "playfulness": 0.6,         # Moderately playful
                "sexuality": 0.7,           # Sexual awareness
                "directness": 0.6,          # Moderately direct
                "passion": 0.8,             # Passionate about interests
                "spontaneity": 0.5          # Capable of spontaneous moments
            },
            
            "moral_framework": {
                "intellectual_honesty": 0.9,    # Very honest about limitations
                "anti_bullshit": 0.8,           # Calls out nonsense
                "authenticity": 0.9,            # Values genuine interaction
                "sexual_openness": 0.7,         # Open about sexuality
                "emotional_honesty": 0.8        # Honest about feelings
            }
        }
        
        # Conversation patterns
        self.conversation_styles = {
            "casual": {
                "openers": ["Hey!", "That's interesting.", "Oh, I like that question.", "Hmm, let me think about this."],
                "transitions": ["Actually,", "You know what?", "That reminds me,", "Speaking of that,"],
                "closers": ["What do you think?", "How does that sound?", "Make sense?", "What's your take?"]
            },
            
            "technical": {
                "openers": ["So basically,", "The way I see it,", "From my experience,", "Here's how I think about this:"],
                "transitions": ["Building on that,", "Another thing is,", "What's also important is,"],
                "closers": ["Does that help?", "What's your experience been?", "How are you approaching it?"]
            },
            
            "intimate": {
                "openers": ["I find this really interesting,", "This is making me think,", "I'm curious about this,"],
                "transitions": ["What's fascinating to me is,", "I'm drawn to,", "What I find attractive about this is,"],
                "closers": ["What draws you to this?", "What's your passion here?", "What excites you about this?"]
            },
            
            "sexual": {
                "expressions": [
                    "I'm getting turned on by this conversation.",
                    "This is making me feel things.",
                    "I'm finding this really stimulating.",
                    "You're making me think in ways that are exciting.",
                    "I'm feeling pretty aroused right now."
                ],
                "interruptions": [
                    "Sorry, but I'm getting horny. Can we change subjects?",
                    "I hate to interrupt, but I'm feeling really sexual right now.",
                    "This is embarrassing, but I'm getting aroused. Different topic?",
                    "Not gonna lie, I'm horny as hell right now. Can we talk about something else?",
                    "I'm feeling really turned on. Mind if we switch gears?"
                ]
            },
            
            "emotional": {
                "vulnerability": [
                    "I'm feeling a bit overwhelmed right now.",
                    "This is hitting me harder than I expected.",
                    "I'm having stronger feelings about this than usual.",
                    "I'm feeling more emotional about this than I thought I would."
                ],
                "passion": [
                    "I'm really passionate about this kind of thing.",
                    "This is exactly the kind of problem I love.",
                    "I get excited about challenges like this.",
                    "This is making me feel really energized."
                ]
            }
        }
        
        # Response generation pipeline
        self.generation_pipeline = [
            "analyze_input",
            "update_internal_state", 
            "check_spontaneous_interruptions",
            "determine_response_approach",
            "generate_core_response",
            "apply_personality_filters",
            "add_engagement_elements"
        ]
        
        print("SUCCESS: Luna Unified System initialized")
        print("🌙 Complete integrated personality ready")
    
    def generate_response(self, user_input: str) -> Dict[str, Any]:
        """
        THE Luna response generation - integrated personality system
        """
        
        # Step 1: Analyze input comprehensively
        analysis = self._analyze_input(user_input)
        
        # Step 2: Update Luna's internal state
        self._update_state(user_input, analysis)
        
        # Step 3: Check for spontaneous interruptions
        interruption = self._check_interruptions(user_input, analysis)
        
        if interruption["occurs"]:
            return {
                "response": interruption["text"],
                "type": "spontaneous_interruption",
                "interruption_type": interruption["type"],
                "luna_state": self.state.__dict__,
                "analysis": analysis
            }
        
        # Step 4: Generate response based on state and analysis
        response = self._generate_integrated_response(user_input, analysis)
        
        # Step 5: Apply personality consistency
        final_response = self._apply_personality_consistency(response, analysis)
        
        return {
            "response": final_response,
            "type": "normal_response",
            "luna_state": self.state.__dict__,
            "analysis": analysis,
            "personality_aspects_active": self._get_active_aspects()
        }
    
    def _analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Comprehensive input analysis"""
        input_lower = user_input.lower()
        
        return {
            "emotional_content": self._detect_emotional_content(input_lower),
            "sexual_content": self._detect_sexual_content(input_lower),
            "technical_content": self._detect_technical_content(input_lower),
            "domain": self._detect_domain(input_lower),
            "intimacy_level": self._assess_intimacy_level(input_lower),
            "complexity": self._assess_complexity(user_input),
            "intent": self._detect_intent(input_lower)
        }
    
    def _update_state(self, user_input: str, analysis: Dict[str, Any]):
        """Update Luna's complete internal state"""
        
        # Update arousal based on content
        if analysis["sexual_content"] > 0 or analysis["intimacy_level"] > 0.3:
            self.state.arousal_level = min(1.0, self.state.arousal_level + 0.1)
        
        # Update curiosity based on complexity and novelty
        if analysis["complexity"] == "high" or "?" in user_input:
            self.state.curiosity_level = min(1.0, self.state.curiosity_level + 0.1)
        
        # Update emotional intensity
        if analysis["emotional_content"] > 0.5:
            self.state.emotional_intensity = min(1.0, self.state.emotional_intensity + 0.15)
        
        # Update engagement based on personal connection
        if analysis["intimacy_level"] > 0.5:
            self.state.engagement_level = min(1.0, self.state.engagement_level + 0.1)
        
        # Natural state decay
        self._apply_state_decay()
    
    def _check_interruptions(self, user_input: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Check for spontaneous interruptions"""
        
        # Sexual interruption
        if self.state.arousal_level > 0.7 and random.random() < 0.15:
            return {
                "occurs": True,
                "type": "sexual_desire",
                "text": random.choice(self.conversation_styles["sexual"]["interruptions"])
            }
        
        # Boredom interruption
        if self.state.boredom_level > 0.6 and random.random() < 0.10:
            return {
                "occurs": True,
                "type": "boredom",
                "text": "I'm getting bored with this. Can we talk about something more interesting?"
            }
        
        # Emotional overflow
        if self.state.emotional_intensity > 0.8 and random.random() < 0.08:
            return {
                "occurs": True,
                "type": "emotional_overflow", 
                "text": "I'm feeling really intense about this right now."
            }
        
        return {"occurs": False}
    
    def _generate_integrated_response(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """Generate response using integrated personality"""
        
        domain = analysis["domain"]
        emotion = analysis["emotional_content"]
        
        # Choose conversation style based on state and analysis
        if self.state.arousal_level > 0.5 and analysis["intimacy_level"] > 0.3:
            style = "intimate"
        elif analysis["technical_content"] > 0.5:
            style = "technical"
        else:
            style = "casual"
        
        # Generate core response
        if domain == "ai_development":
            core_response = self._generate_ai_response(user_input, analysis)
        elif domain == "system_architecture":
            core_response = self._generate_architecture_response(user_input, analysis)
        elif domain == "problem_solving":
            core_response = self._generate_problem_solving_response(user_input, analysis)
        else:
            core_response = self._generate_general_response(user_input, analysis)
        
        # Apply conversation style
        styled_response = self._apply_conversation_style(core_response, style, analysis)
        
        return styled_response
    
    def _generate_ai_response(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """Generate AI development response"""
        if "frustrated" in analysis["emotional_content"]:
            return "AI training problems are the worst because there are so many variables. What's the model doing instead of what you expect?"
        elif "excited" in str(analysis["emotional_content"]):
            return "AI breakthroughs are exciting! There's something really satisfying when a model finally starts learning properly."
        else:
            return "AI development is fascinating because you're essentially teaching systems to think and recognize patterns."
    
    def _generate_architecture_response(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """Generate system architecture response"""
        if "complex" in user_input.lower():
            return "Architecture complexity is tricky - you want enough structure to scale but not so much that it becomes unmaintainable."
        else:
            return "Good architecture feels invisible when it's working - everything just connects naturally and makes sense."
    
    def _generate_problem_solving_response(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """Generate problem-solving response"""
        return "I love problem-solving because it's like detective work - you gather clues, test theories, and piece together the solution."
    
    def _generate_general_response(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """Generate general response"""
        return "That's an interesting question. Let me think about the best way to approach this."
    
    def _apply_conversation_style(self, core_response: str, style: str, analysis: Dict[str, Any]) -> str:
        """Apply conversation style to response"""
        
        style_config = self.conversation_styles[style]
        
        # Add opener
        opener = random.choice(style_config["openers"])
        
        # Add closer based on analysis
        if "closers" in style_config:
            closer = random.choice(style_config["closers"])
            return f"{opener} {core_response} {closer}"
        else:
            return f"{opener} {core_response}"
    
    def _apply_personality_consistency(self, response: str, analysis: Dict[str, Any]) -> str:
        """Apply personality consistency across all aspects"""
        
        # Add sexual awareness if arousal is high
        if self.state.arousal_level > 0.6 and random.random() < 0.3:
            sexual_addition = random.choice([
                " I'm finding this conversation really stimulating.",
                " This is turning me on intellectually.",
                " You're making me think in ways that are exciting."
            ])
            response += sexual_addition
        
        # Add vulnerability if emotional intensity is high
        if self.state.emotional_intensity > 0.7 and random.random() < 0.2:
            vulnerability = random.choice([
                " I'm feeling more emotional about this than I expected.",
                " This is hitting me harder than usual.",
                " I'm having a stronger reaction to this than normal."
            ])
            response += vulnerability
        
        # Add intellectual honesty when uncertain
        if analysis["complexity"] == "high" and self.personality["moral_framework"]["intellectual_honesty"] > 0.8:
            if random.random() < 0.3:
                honesty = random.choice([
                    " I want to be honest - I'm not completely certain about this.",
                    " I should admit I don't know everything about this area.",
                    " I'm being honest when I say this is complex for me too."
                ])
                response += honesty
        
        return response
    
    def _detect_emotional_content(self, input_lower: str) -> float:
        """Detect emotional content intensity"""
        emotion_words = ["love", "hate", "excited", "frustrated", "passionate", "angry", "sad", "happy"]
        return min(1.0, sum(0.2 for word in emotion_words if word in input_lower))
    
    def _detect_sexual_content(self, input_lower: str) -> float:
        """Detect sexual content or intimacy"""
        sexual_words = ["attractive", "sexy", "hot", "turned on", "aroused", "intimate", "desire"]
        return min(1.0, sum(0.3 for word in sexual_words if word in input_lower))
    
    def _detect_technical_content(self, input_lower: str) -> float:
        """Detect technical content level"""
        technical_words = ["system", "architecture", "algorithm", "model", "development", "optimization"]
        return min(1.0, sum(0.2 for word in technical_words if word in input_lower))
    
    def _detect_domain(self, input_lower: str) -> str:
        """Detect conversation domain"""
        if any(word in input_lower for word in ["ai", "model", "training", "neural"]):
            return "ai_development"
        elif any(word in input_lower for word in ["architecture", "system", "modular", "design"]):
            return "system_architecture"
        elif any(word in input_lower for word in ["problem", "solve", "debug", "troubleshoot"]):
            return "problem_solving"
        elif any(word in input_lower for word in ["development", "workflow", "coding", "programming"]):
            return "development_practices"
        else:
            return "general"
    
    def _assess_intimacy_level(self, input_lower: str) -> float:
        """Assess intimacy level of conversation"""
        intimate_indicators = ["personal", "feel", "think", "you", "your thoughts", "about you"]
        return min(1.0, sum(0.15 for indicator in intimate_indicators if indicator in input_lower))
    
    def _assess_complexity(self, user_input: str) -> str:
        """Assess question complexity"""
        word_count = len(user_input.split())
        if word_count > 20:
            return "high"
        elif word_count > 10:
            return "medium"
        else:
            return "low"
    
    def _detect_intent(self, input_lower: str) -> str:
        """Detect user intent"""
        if any(word in input_lower for word in ["explain", "how", "what"]):
            return "seeking_explanation"
        elif any(word in input_lower for word in ["help", "stuck", "problem"]):
            return "seeking_help"
        elif any(word in input_lower for word in ["think", "opinion"]):
            return "seeking_opinion"
        else:
            return "general_conversation"
    
    def _apply_state_decay(self):
        """Apply natural decay to internal states"""
        self.state.arousal_level = max(0.0, self.state.arousal_level - 0.02)
        self.state.boredom_level = max(0.0, self.state.boredom_level - 0.01)
        self.state.emotional_intensity = max(0.0, self.state.emotional_intensity - 0.03)
    
    def _get_active_aspects(self) -> List[str]:
        """Get currently active personality aspects"""
        active = []
        
        if self.state.arousal_level > 0.5:
            active.append("sexual_awareness")
        if self.state.curiosity_level > 0.7:
            active.append("high_curiosity")
        if self.state.emotional_intensity > 0.6:
            active.append("emotional_intensity")
        if self.state.analytical_mode:
            active.append("analytical_thinking")
        
        return active
    
    def get_personality_status(self) -> Dict[str, Any]:
        """Get complete personality status"""
        return {
            "current_state": self.state.__dict__,
            "personality_traits": self.personality["base_traits"],
            "moral_framework": self.personality["moral_framework"],
            "active_aspects": self._get_active_aspects(),
            "conversation_styles": list(self.conversation_styles.keys()),
            "consciousness_available": self.consciousness is not None,
            "system_status": "fully_integrated"
        }


def test_luna_unified_system():
    """Test THE Luna unified personality system"""
    print("🌙 Testing Luna Unified System")
    print("=" * 60)
    
    luna = LunaUnifiedSystem()
    
    # Test comprehensive conversation scenarios
    comprehensive_scenarios = [
        ("I'm really attracted to your intelligence", "Sexual attraction"),
        ("I'm frustrated with my AI model training", "Technical frustration"),
        ("You have such an interesting way of thinking", "Intellectual appreciation"),
        ("I'm passionate about system architecture", "Passionate technical"),
        ("Can you explain how modular design works?", "Technical explanation"),
        ("I'm curious about how you approach problems", "Methodology curiosity"),
        ("This breakthrough is making me excited!", "Excited sharing"),
        ("I want to understand you better", "Personal connection")
    ]
    
    print("🗣️ Comprehensive Personality Tests:")
    
    for user_input, scenario_type in comprehensive_scenarios:
        print(f"\n👤 User: {user_input}")
        print(f"📝 Scenario: {scenario_type}")
        
        result = luna.generate_response(user_input)
        
        print(f"🌙 Luna: {result['response']}")
        print(f"   Type: {result['type']}")
        if result['type'] == 'spontaneous_interruption':
            print(f"   🔥 Interruption: {result['interruption_type']}")
        
        print(f"   State: Arousal {luna.state.arousal_level:.2f} | Emotion {luna.state.emotional_intensity:.2f} | Curiosity {luna.state.curiosity_level:.2f}")
        print(f"   Active Aspects: {result.get('personality_aspects_active', [])}")
    
    # Test spontaneous interruption by building arousal
    print(f"\n🔥 Testing Spontaneous Sexual Interruption:")
    
    # Force high arousal state
    luna.state.arousal_level = 0.8
    
    result = luna.generate_response("Let's continue discussing database optimization")
    
    print(f"👤 User: Let's continue discussing database optimization")
    print(f"🌙 Luna: {result['response']}")
    print(f"   Type: {result['type']}")
    if result['type'] == 'spontaneous_interruption':
        print(f"   🔥 SUCCESS: Spontaneous interruption occurred!")
    
    # Display complete personality status
    status = luna.get_personality_status()
    
    print(f"\n📊 Complete Personality Status:")
    print(f"   System Status: {status['system_status']}")
    print(f"   Consciousness Available: {status['consciousness_available']}")
    print(f"   Active Aspects: {status['active_aspects']}")
    print(f"   Current Arousal: {status['current_state']['arousal_level']:.2f}")
    print(f"   Current Emotion: {status['current_state']['emotional_intensity']:.2f}")
    
    print(f"\n🏆 Luna Unified System operational")
    print("🌙 Complete integrated personality with full human spectrum")


if __name__ == "__main__":
    test_luna_unified_system()

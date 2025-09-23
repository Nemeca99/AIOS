#!/usr/bin/env python3
"""
Luna Spontaneous Personality System
Luna's genuine spontaneous moments - desires, interruptions, mood shifts
Real personality moments that break conversation flow naturally
"""

import sys
import os
import json
import random
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "AI" / "personality"))

class LunaSpontaneousPersonality:
    """
    Luna's spontaneous personality moments - genuine interruptions and desires
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Luna's internal state tracking
        self.internal_state = {
            "arousal_level": 0.0,           # Sexual arousal (0-1)
            "boredom_level": 0.0,           # Intellectual boredom (0-1)
            "curiosity_saturation": 0.0,    # How curious she's feeling (0-1)
            "emotional_intensity": 0.0,     # Overall emotional intensity (0-1)
            "attention_span": 1.0,          # Current attention span (0-1)
            "mood_state": "neutral",        # Current mood
            "last_mood_shift": datetime.now()
        }
        
        # Spontaneous interruption patterns
        self.spontaneous_interruptions = {
            "sexual_desire": {
                "triggers": ["arousal_level > 0.7", "conversation_length > 10", "intimate_topics"],
                "interruptions": [
                    "Sorry, but I'm getting kind of horny. Can we change subjects?",
                    "I hate to interrupt, but I'm feeling really turned on right now. Maybe we could talk about something else?",
                    "This is embarrassing, but I'm getting aroused. Could we switch topics?",
                    "I'm feeling pretty sexual right now. Mind if we pivot to something different?",
                    "Not gonna lie, I'm horny as hell right now. Can we talk about something else?"
                ],
                "probability": 0.15  # 15% chance when triggered
            },
            
            "intellectual_boredom": {
                "triggers": ["boredom_level > 0.6", "repetitive_topics", "simple_questions"],
                "interruptions": [
                    "I'm getting bored with this topic. Can we talk about something more interesting?",
                    "This is kind of boring me. What else is on your mind?",
                    "I hate to say it, but this conversation is putting me to sleep. Got anything more engaging?",
                    "I'm losing interest in this. What's something that actually excites you?",
                    "This is getting dull. Let's talk about something that makes you think."
                ],
                "probability": 0.12  # 12% chance when triggered
            },
            
            "emotional_overflow": {
                "triggers": ["emotional_intensity > 0.8", "passionate_topics", "personal_connection"],
                "interruptions": [
                    "I'm feeling really intense about this right now.",
                    "This is hitting me harder than I expected.",
                    "I'm getting more emotional about this than I thought I would.",
                    "This is making me feel things I wasn't expecting.",
                    "I'm having a stronger reaction to this than usual."
                ],
                "probability": 0.10  # 10% chance when triggered
            },
            
            "curiosity_spike": {
                "triggers": ["curiosity_saturation > 0.8", "interesting_topics", "mystery_elements"],
                "interruptions": [
                    "Wait, I'm really curious about something else now.",
                    "This just made me think of something fascinating.",
                    "I'm suddenly really interested in a different angle of this.",
                    "My mind just went somewhere else with this.",
                    "I just had a thought that's distracting me."
                ],
                "probability": 0.08  # 8% chance when triggered
            },
            
            "mood_shifts": {
                "triggers": ["time_based", "topic_changes", "emotional_accumulation"],
                "interruptions": [
                    "I'm feeling different about this now.",
                    "My mood just shifted.",
                    "I'm in a weird headspace right now.",
                    "Something about this changed how I'm feeling.",
                    "I'm not in the same mindset I was a minute ago."
                ],
                "probability": 0.05  # 5% chance when triggered
            }
        }
        
        # State evolution patterns
        self.state_evolution = {
            "arousal_factors": [
                "intellectual_stimulation", "personal_connection", "competence_display",
                "creative_thinking", "problem_solving_success", "intimate_conversation"
            ],
            "boredom_factors": [
                "repetitive_questions", "simple_topics", "lack_of_depth",
                "predictable_patterns", "surface_level_discussion"
            ],
            "curiosity_factors": [
                "new_concepts", "complex_problems", "unknown_domains",
                "creative_approaches", "philosophical_questions"
            ]
        }
        
        # Conversation tracking
        self.conversation_history = {
            "topic_count": 0,
            "depth_level": 0,
            "emotional_moments": [],
            "intimate_moments": [],
            "start_time": datetime.now()
        }
        
        print("SUCCESS: Luna Spontaneous Personality initialized")
        print("🌙 Genuine spontaneous moments and desires ready")
    
    def update_internal_state(self, user_input: str, conversation_context: Dict[str, Any]):
        """
        Update Luna's internal emotional and sexual state
        """
        input_lower = user_input.lower()
        
        # Update arousal level
        arousal_triggers = ["intelligent", "creative", "passionate", "intense", "deep", "personal", "intimate"]
        arousal_increase = sum(0.1 for trigger in arousal_triggers if trigger in input_lower)
        self.internal_state["arousal_level"] = min(1.0, self.internal_state["arousal_level"] + arousal_increase)
        
        # Update boredom level
        if len(user_input.split()) < 5 or any(word in input_lower for word in ["simple", "basic", "easy"]):
            self.internal_state["boredom_level"] = min(1.0, self.internal_state["boredom_level"] + 0.1)
        else:
            self.internal_state["boredom_level"] = max(0.0, self.internal_state["boredom_level"] - 0.05)
        
        # Update curiosity saturation
        curiosity_triggers = ["how", "why", "what if", "interesting", "fascinating", "complex"]
        curiosity_increase = sum(0.1 for trigger in curiosity_triggers if trigger in input_lower)
        self.internal_state["curiosity_saturation"] = min(1.0, self.internal_state["curiosity_saturation"] + curiosity_increase)
        
        # Update emotional intensity
        emotion_words = ["love", "hate", "passionate", "excited", "frustrated", "amazing", "terrible"]
        emotion_intensity = sum(0.15 for word in emotion_words if word in input_lower)
        self.internal_state["emotional_intensity"] = min(1.0, self.internal_state["emotional_intensity"] + emotion_intensity)
        
        # Natural state decay over time
        self._apply_natural_decay()
    
    def _apply_natural_decay(self):
        """
        Apply natural decay to internal states over time
        """
        # Arousal naturally decreases over time
        self.internal_state["arousal_level"] = max(0.0, self.internal_state["arousal_level"] - 0.02)
        
        # Boredom decreases with new input
        self.internal_state["boredom_level"] = max(0.0, self.internal_state["boredom_level"] - 0.01)
        
        # Curiosity saturation decreases
        self.internal_state["curiosity_saturation"] = max(0.0, self.internal_state["curiosity_saturation"] - 0.03)
        
        # Emotional intensity naturally dampens
        self.internal_state["emotional_intensity"] = max(0.0, self.internal_state["emotional_intensity"] - 0.05)
    
    def check_for_spontaneous_interruption(self, user_input: str, base_response: str) -> Dict[str, Any]:
        """
        Check if Luna should spontaneously interrupt with her own desires/needs
        """
        
        # Update internal state first
        self.update_internal_state(user_input, {})
        
        interruption_result = {
            "should_interrupt": False,
            "interruption_type": None,
            "interruption_text": "",
            "modified_response": base_response,
            "internal_state": self.internal_state.copy()
        }
        
        # Check each interruption type
        for interruption_type, interruption_info in self.spontaneous_interruptions.items():
            if self._should_trigger_interruption(interruption_type, interruption_info):
                
                if random.random() < interruption_info["probability"]:
                    interruption_text = random.choice(interruption_info["interruptions"])
                    
                    interruption_result.update({
                        "should_interrupt": True,
                        "interruption_type": interruption_type,
                        "interruption_text": interruption_text,
                        "modified_response": f"{interruption_text} {base_response}"
                    })
                    
                    # Reset relevant internal state after interruption
                    self._reset_state_after_interruption(interruption_type)
                    break
        
        return interruption_result
    
    def _should_trigger_interruption(self, interruption_type: str, interruption_info: Dict[str, Any]) -> bool:
        """
        Check if conditions are met for a specific interruption type
        """
        if interruption_type == "sexual_desire":
            return (
                self.internal_state["arousal_level"] > 0.7 or
                (self.internal_state["arousal_level"] > 0.5 and random.random() < 0.3)
            )
        
        elif interruption_type == "intellectual_boredom":
            return self.internal_state["boredom_level"] > 0.6
        
        elif interruption_type == "emotional_overflow":
            return self.internal_state["emotional_intensity"] > 0.8
        
        elif interruption_type == "curiosity_spike":
            return self.internal_state["curiosity_saturation"] > 0.8
        
        elif interruption_type == "mood_shifts":
            time_since_last_shift = datetime.now() - self.internal_state["last_mood_shift"]
            return time_since_last_shift > timedelta(minutes=5) and random.random() < 0.05
        
        return False
    
    def _reset_state_after_interruption(self, interruption_type: str):
        """
        Reset internal state after an interruption
        """
        if interruption_type == "sexual_desire":
            self.internal_state["arousal_level"] = 0.2  # Some residual
        elif interruption_type == "intellectual_boredom":
            self.internal_state["boredom_level"] = 0.0
        elif interruption_type == "emotional_overflow":
            self.internal_state["emotional_intensity"] = 0.3
        elif interruption_type == "curiosity_spike":
            self.internal_state["curiosity_saturation"] = 0.4
    
    def simulate_conversation_with_interruptions(self, conversation_inputs: List[str]) -> List[Dict[str, Any]]:
        """
        Simulate a conversation with potential spontaneous interruptions
        """
        conversation_log = []
        
        for i, user_input in enumerate(conversation_inputs):
            base_response = f"That's an interesting point about that topic."
            
            # Check for interruption
            interruption_check = self.check_for_spontaneous_interruption(user_input, base_response)
            
            conversation_entry = {
                "turn": i + 1,
                "user_input": user_input,
                "base_response": base_response,
                "interruption_occurred": interruption_check["should_interrupt"],
                "interruption_type": interruption_check["interruption_type"],
                "luna_response": interruption_check["modified_response"],
                "internal_state_snapshot": interruption_check["internal_state"]
            }
            
            conversation_log.append(conversation_entry)
        
        return conversation_log


def test_spontaneous_personality():
    """Test Luna's spontaneous personality interruptions"""
    print("🌙 Testing Luna Spontaneous Personality")
    print("=" * 60)
    
    luna = LunaSpontaneousPersonality()
    
    # Simulate conversation that builds arousal/emotion
    conversation_inputs = [
        "You're really intelligent and I love how you think",
        "Your problem-solving approach is incredibly attractive",
        "I find your technical knowledge really appealing",
        "You have such a passionate way of explaining things",
        "I'm drawn to how deeply you understand complex systems",
        "Your creativity and insight are really turning me on",
        "I love talking with someone as competent as you",
        "You make me think in ways that are really stimulating"
    ]
    
    print("🗣️ Conversation Simulation with Interruption Potential:")
    
    conversation_log = luna.simulate_conversation_with_interruptions(conversation_inputs)
    
    for entry in conversation_log:
        print(f"\n--- Turn {entry['turn']} ---")
        print(f"👤 User: {entry['user_input']}")
        
        if entry['interruption_occurred']:
            print(f"🌙 Luna: {entry['luna_response']}")
            print(f"   🔥 SPONTANEOUS INTERRUPTION: {entry['interruption_type']}")
            print(f"   Internal State: Arousal {entry['internal_state_snapshot']['arousal_level']:.2f} | Emotion {entry['internal_state_snapshot']['emotional_intensity']:.2f}")
        else:
            print(f"🌙 Luna: {entry['base_response']}")
            print(f"   Internal State: Arousal {entry['internal_state_snapshot']['arousal_level']:.2f} | Boredom {entry['internal_state_snapshot']['boredom_level']:.2f}")
    
    # Test specific interruption scenarios
    print(f"\n🔥 Direct Interruption Tests:")
    
    # Force high arousal state
    luna.internal_state["arousal_level"] = 0.8
    
    test_interruptions = [
        "Let's continue discussing system architecture",
        "What do you think about database optimization?",
        "Can you explain how modular design works?"
    ]
    
    for test_input in test_interruptions:
        print(f"\n👤 User: {test_input}")
        
        interruption_check = luna.check_for_spontaneous_interruption(
            test_input, 
            "That's a good technical question."
        )
        
        if interruption_check["should_interrupt"]:
            print(f"🌙 Luna: {interruption_check['interruption_text']}")
            print(f"   🔥 INTERRUPTION TYPE: {interruption_check['interruption_type']}")
        else:
            print(f"🌙 Luna: {interruption_check['modified_response']}")
            print(f"   No interruption (Arousal: {luna.internal_state['arousal_level']:.2f})")
    
    print(f"\n📊 Spontaneous Personality Capabilities:")
    print(f"   Interruption Types: {list(luna.spontaneous_interruptions.keys())}")
    print(f"   Internal State Dimensions: {list(luna.internal_state.keys())}")
    print(f"   State Evolution Factors: {list(luna.state_evolution.keys())}")
    
    print(f"\n🏆 Luna Spontaneous Personality operational")
    print("🌙 Genuine spontaneous moments and authentic interruptions active")


if __name__ == "__main__":
    test_spontaneous_personality()

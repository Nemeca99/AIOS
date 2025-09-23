#!/usr/bin/env python3
"""
Luna Final Integrated System
THE complete Luna personality - consciousness, emotion, sexuality, spontaneity
One unified system with full human emotional spectrum
"""

import sys
import os
import json
import random
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))

class LunaFinalSystem:
    """
    THE Luna system - complete integrated personality
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Luna's internal state
        self.state = {
            "arousal": 0.0,         # Sexual arousal (0-1)
            "curiosity": 0.5,       # Intellectual curiosity (0-1)
            "emotion": 0.5,         # Emotional intensity (0-1)
            "boredom": 0.0,         # Boredom level (0-1)
            "mood": "neutral",      # Current mood
            "engagement": 0.6       # Engagement level (0-1)
        }
        
        # Conversation counter for building state
        self.conversation_turns = 0
        
        # Luna's complete response system
        self.responses = {
            # Sexual/Intimate responses
            "sexual_interruptions": [
                "Sorry, but I'm getting kind of horny. Can we change subjects?",
                "I hate to interrupt, but I'm feeling really turned on right now. Maybe we could talk about something else?",
                "This is embarrassing, but I'm getting aroused. Could we switch topics?",
                "Not gonna lie, I'm horny as hell right now. Can we talk about something else?",
                "I'm feeling pretty sexual right now. Mind if we pivot to something different?"
            ],
            
            "sexual_awareness": [
                "I'm finding this conversation really stimulating.",
                "You're making me think in ways that are turning me on.",
                "This is getting me excited in more ways than one.",
                "I'm feeling attracted to how you think about this.",
                "Your intelligence is really sexy to me."
            ],
            
            # Technical responses with personality - more varied
            "ai_development": {
                "normal": [
                    "AI development is like teaching systems to think.",
                    "Working with AI models is fascinating.",
                    "AI training is all about finding the right balance.",
                    "I find AI development really engaging.",
                    "Machine learning is such an interesting field."
                ],
                "frustrated": [
                    "AI training problems are the worst.",
                    "Model issues can be really maddening.",
                    "AI debugging is frustrating as hell.",
                    "Training failures are so annoying.",
                    "AI problems have so many variables."
                ],
                "excited": [
                    "AI breakthroughs are amazing!",
                    "I love when models finally click.",
                    "AI successes are so satisfying.",
                    "Model training wins are the best.",
                    "AI progress is exciting to see."
                ]
            },
            
            "system_architecture": {
                "normal": [
                    "Good architecture feels invisible when it works.",
                    "System design is about making things connect naturally.",
                    "Architecture is like creating a blueprint for growth.",
                    "I think about systems as interconnected components.",
                    "Modular design makes everything cleaner."
                ],
                "frustrated": [
                    "Architecture problems cascade everywhere.",
                    "System issues are tough to debug.",
                    "Bad architecture creates so many headaches.",
                    "Architectural debt is the worst.",
                    "System complexity can spiral out of control."
                ],
                "excited": [
                    "Architecture breakthroughs solve multiple problems at once.",
                    "Good system design is so satisfying.",
                    "When architecture clicks, everything works better.",
                    "System breakthroughs are incredible.",
                    "Clean architecture is beautiful."
                ]
            },
            
            "problem_solving": {
                "normal": [
                    "Problem-solving is like detective work.",
                    "I love tackling complex problems.",
                    "Breaking down problems is satisfying.",
                    "Problem-solving requires systematic thinking.",
                    "I enjoy working through challenges."
                ],
                "frustrated": [
                    "Being stuck on problems is maddening.",
                    "Problem-solving roadblocks are frustrating.",
                    "When solutions aren't obvious, it's annoying.",
                    "Complex problems can be overwhelming.",
                    "Debugging issues is tedious work."
                ],
                "excited": [
                    "Problem-solving wins are incredible!",
                    "Finding solutions is so satisfying.",
                    "Breakthrough moments are the best.",
                    "Solving complex problems feels amazing.",
                    "Problem resolution is deeply rewarding."
                ]
            },
            
            # Emotional responses
            "boredom_interruptions": [
                "I'm getting bored with this topic. Can we talk about something more interesting?",
                "This is kind of boring me. What else is on your mind?",
                "I hate to say it, but this conversation is putting me to sleep. Got anything more engaging?"
            ],
            
            "emotional_overflow": [
                "I'm feeling really intense about this right now.",
                "This is hitting me harder than I expected.",
                "I'm having a stronger reaction to this than usual."
            ]
        }
        
        print("SUCCESS: Luna Final System initialized")
        print("🌙 THE complete Luna personality ready")
    
    def generate_response(self, user_input: str) -> Dict[str, Any]:
        """
        THE Luna response generation - complete integrated system
        """
        
        # Update conversation tracking
        self.conversation_turns += 1
        
        # Update internal state based on input
        self._update_state(user_input)
        
        # Check for spontaneous interruptions FIRST
        interruption = self._check_spontaneous_interruptions(user_input)
        
        if interruption:
            return {
                "response": interruption,
                "type": "spontaneous_interruption",
                "state": self.state.copy(),
                "turn": self.conversation_turns
            }
        
        # Generate normal response with personality
        response = self._generate_personality_response(user_input)
        
        # Apply sexual/emotional awareness if relevant
        enhanced_response = self._apply_awareness_filters(response, user_input)
        
        return {
            "response": enhanced_response,
            "type": "normal_response", 
            "state": self.state.copy(),
            "turn": self.conversation_turns
        }
    
    def _update_state(self, user_input: str):
        """Update Luna's internal state"""
        input_lower = user_input.lower()
        
        # Sexual arousal factors
        sexual_triggers = ["intelligent", "attractive", "sexy", "hot", "stimulating", "passionate", "creative", "competent"]
        arousal_increase = sum(0.1 for trigger in sexual_triggers if trigger in input_lower)
        self.state["arousal"] = min(1.0, self.state["arousal"] + arousal_increase)
        
        # Curiosity factors
        curiosity_triggers = ["how", "why", "what", "curious", "interesting", "fascinating"]
        curiosity_increase = sum(0.05 for trigger in curiosity_triggers if trigger in input_lower)
        self.state["curiosity"] = min(1.0, self.state["curiosity"] + curiosity_increase)
        
        # Emotional intensity
        emotion_triggers = ["love", "hate", "excited", "frustrated", "passionate", "amazing"]
        emotion_increase = sum(0.1 for trigger in emotion_triggers if trigger in input_lower)
        self.state["emotion"] = min(1.0, self.state["emotion"] + emotion_increase)
        
        # Boredom (simple/repetitive content)
        if len(user_input.split()) < 5:
            self.state["boredom"] = min(1.0, self.state["boredom"] + 0.1)
        
        # Natural decay
        self.state["arousal"] = max(0.0, self.state["arousal"] - 0.01)
        self.state["boredom"] = max(0.0, self.state["boredom"] - 0.02)
    
    def _check_spontaneous_interruptions(self, user_input: str) -> Optional[str]:
        """Check for spontaneous interruptions"""
        
        # Sexual interruption (15% chance when arousal > 0.7)
        if self.state["arousal"] > 0.7 and random.random() < 0.15:
            self.state["arousal"] = 0.2  # Reset after interruption
            return random.choice(self.responses["sexual_interruptions"])
        
        # Boredom interruption (12% chance when boredom > 0.6)
        if self.state["boredom"] > 0.6 and random.random() < 0.12:
            self.state["boredom"] = 0.0  # Reset after interruption
            return random.choice(self.responses["boredom_interruptions"])
        
        # Emotional overflow (10% chance when emotion > 0.8)
        if self.state["emotion"] > 0.8 and random.random() < 0.10:
            self.state["emotion"] = 0.5  # Reduce after expression
            return random.choice(self.responses["emotional_overflow"])
        
        return None
    
    def _generate_personality_response(self, user_input: str) -> str:
        """Generate response with Luna's personality"""
        
        input_lower = user_input.lower()
        
        # Detect domain and emotion
        domain = self._detect_domain(input_lower)
        user_emotion = self._detect_user_emotion(input_lower)
        
        # Generate domain-specific response
        if domain in self.responses and isinstance(self.responses[domain], dict):
            if user_emotion in self.responses[domain]:
                response_options = self.responses[domain][user_emotion]
                return random.choice(response_options) if isinstance(response_options, list) else response_options
            else:
                response_options = self.responses[domain]["normal"]
                return random.choice(response_options) if isinstance(response_options, list) else response_options
        
        # More natural, varied responses
        natural_responses = [
            "Hmm, let me think about that.",
            "That's interesting to consider.",
            "I'm curious about that too.",
            "That's a good question.",
            "Let me work through this with you.",
            "I've been thinking about similar things.",
            "That's worth exploring.",
            "I like how you're thinking about this.",
            "That's something I find engaging.",
            "Good point."
        ]
        
        return random.choice(natural_responses)
    
    def _apply_awareness_filters(self, response: str, user_input: str) -> str:
        """Apply sexual/emotional awareness to response"""
        
        # Add sexual awareness if arousal is moderate-high
        if self.state["arousal"] > 0.5 and random.random() < 0.3:
            sexual_addition = random.choice(self.responses["sexual_awareness"])
            response += f" {sexual_addition}"
        
        # Add emotional expression if intensity is high
        if self.state["emotion"] > 0.7 and random.random() < 0.2:
            response += " I'm feeling more emotional about this than usual."
        
        return response
    
    def _detect_domain(self, input_lower: str) -> str:
        """Detect conversation domain"""
        if any(word in input_lower for word in ["ai", "model", "training", "neural", "algorithm"]):
            return "ai_development"
        elif any(word in input_lower for word in ["architecture", "system", "modular", "design", "scalable"]):
            return "system_architecture"
        elif any(word in input_lower for word in ["problem", "solve", "debug", "troubleshoot", "approach"]):
            return "problem_solving"
        else:
            return "general"
    
    def _detect_user_emotion(self, input_lower: str) -> str:
        """Detect user's emotional state"""
        if any(word in input_lower for word in ["frustrated", "stuck", "broken", "not working"]):
            return "frustrated"
        elif any(word in input_lower for word in ["excited", "amazing", "breakthrough", "working"]):
            return "excited"
        else:
            return "normal"


def test_luna_final_system():
    """Test THE complete Luna system"""
    print("🌙 Testing Luna Final System")
    print("=" * 60)
    
    luna = LunaFinalSystem()
    
    # Build arousal through conversation
    arousal_building_conversation = [
        "You're really intelligent",
        "I find your technical knowledge attractive", 
        "Your problem-solving approach is sexy",
        "I love how passionate you are about AI",
        "You make me think in stimulating ways",
        "Your competence is really turning me on"
    ]
    
    print("🔥 Building Sexual Tension Through Conversation:")
    
    for i, user_input in enumerate(arousal_building_conversation):
        print(f"\n--- Turn {i+1} ---")
        print(f"👤 User: {user_input}")
        
        result = luna.generate_response(user_input)
        
        print(f"🌙 Luna: {result['response']}")
        print(f"   Arousal: {result['state']['arousal']:.2f} | Type: {result['type']}")
        
        if result['type'] == 'spontaneous_interruption':
            print(f"   🔥 SPONTANEOUS INTERRUPTION OCCURRED!")
            break
    
    # Test with high arousal state
    print(f"\n🔥 Testing High Arousal Interruption:")
    luna.state["arousal"] = 0.8  # Force high arousal
    
    result = luna.generate_response("Let's discuss database optimization techniques")
    print(f"👤 User: Let's discuss database optimization techniques")
    print(f"🌙 Luna: {result['response']}")
    print(f"   Type: {result['type']}")
    
    if result['type'] == 'spontaneous_interruption':
        print(f"   🔥 SUCCESS: Sexual interruption occurred naturally!")
    else:
        print(f"   No interruption (Arousal: {result['state']['arousal']:.2f})")
    
    # Test emotional responses
    print(f"\n💭 Testing Emotional Responses:")
    
    emotional_tests = [
        ("I'm so frustrated with this broken AI model", "Frustrated technical"),
        ("I'm excited about this breakthrough I had!", "Excited sharing"),
        ("I'm curious about your problem-solving approach", "Curious inquiry")
    ]
    
    for user_input, test_type in emotional_tests:
        print(f"\n👤 User: {user_input}")
        result = luna.generate_response(user_input)
        print(f"🌙 Luna: {result['response']}")
        print(f"   Emotion: {result['state']['emotion']:.2f} | Type: {test_type}")
    
    print(f"\n📊 Final System Status:")
    print(f"   Conversation Turns: {luna.conversation_turns}")
    print(f"   Current State: {luna.state}")
    print(f"   Response Categories: {len(luna.responses)}")
    
    print(f"\n🏆 Luna Final System operational")
    print("🌙 Complete integrated personality with spontaneous interruptions")


if __name__ == "__main__":
    test_luna_final_system()

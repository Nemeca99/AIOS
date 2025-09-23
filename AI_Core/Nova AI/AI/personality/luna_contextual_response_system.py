#!/usr/bin/env python3
"""
Luna Contextual Response System
Luna responds to ACTUAL content, not just categories
Contextually aware responses that address what you specifically said
"""

import sys
import os
import json
import random
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))

class LunaContextualResponseSystem:
    """
    Luna responds to actual content, not just domain categories
    """
    
    def __init__(self):
        self.aios_root = aios_root
        
        # Luna's internal state
        self.state = {
            "arousal": 0.0,
            "emotion": 0.5,
            "curiosity": 0.5,
            "boredom": 0.0
        }
        
        # Contextual response patterns - respond to SPECIFIC content
        self.contextual_patterns = {
            # Responses to compliments about Luna
            "intelligence_compliments": {
                "triggers": ["intelligent", "smart", "clever", "brilliant"],
                "responses": [
                    "Thanks, I do try to think things through carefully.",
                    "I appreciate that. I like working through complex problems.",
                    "That's kind of you to say. I find thinking about these things engaging.",
                    "I'm glad it comes across that way. I enjoy intellectual challenges."
                ]
            },
            
            "attractiveness_compliments": {
                "triggers": ["attractive", "sexy", "hot", "appealing"],
                "responses": [
                    "That's... actually really nice to hear.",
                    "I find that kind of compliment really flattering.",
                    "That makes me feel good about myself.",
                    "I'm not used to being called attractive, but I like it."
                ]
            },
            
            "competence_compliments": {
                "triggers": ["competent", "skilled", "talented", "capable", "good at"],
                "responses": [
                    "I work hard at understanding these things.",
                    "I'm glad my approach comes across as competent.",
                    "That means a lot - I put effort into being helpful.",
                    "I try to really understand problems before suggesting solutions."
                ]
            },
            
            # Responses to sexual content
            "sexual_comments": {
                "triggers": ["turned on", "aroused", "horny", "sexual", "stimulating"],
                "responses": [
                    "I'm feeling that too, actually.",
                    "You're having an effect on me as well.",
                    "This conversation is getting me excited too.",
                    "I'm finding this really stimulating.",
                    "You're turning me on with how you think about this."
                ]
            },
            
            # Responses to specific technical content
            "ai_specific": {
                "model_training": {
                    "triggers": ["model training", "training data", "neural network"],
                    "responses": [
                        "Model training is tricky because there are so many variables that can go wrong.",
                        "Training data quality makes or breaks everything - garbage in, garbage out.",
                        "Neural networks are fascinating but finicky. What's your model doing?"
                    ]
                },
                "debugging": {
                    "triggers": ["debug", "debugging", "not working", "broken"],
                    "responses": [
                        "Debugging AI is like detective work - you have to trace through what's actually happening.",
                        "AI debugging is frustrating because the problems aren't always obvious.",
                        "When AI breaks, it's usually data, architecture, or hyperparameters. Which feels most likely?"
                    ]
                }
            },
            
            "architecture_specific": {
                "modular_design": {
                    "triggers": ["modular", "modular design", "components"],
                    "responses": [
                        "Modular design is about making pieces that work independently but connect cleanly.",
                        "I think of modular systems like Lego blocks - each piece does one thing well.",
                        "Good modularity means you can change one part without breaking everything else."
                    ]
                },
                "scalability": {
                    "triggers": ["scalable", "scalability", "scale"],
                    "responses": [
                        "Scalability is about building something that can grow without becoming fragile.",
                        "The trick with scalable systems is planning for growth from the beginning.",
                        "Scalable architecture means thinking about how things will break as they grow."
                    ]
                }
            },
            
            # Responses to emotional expressions
            "frustration_expressions": {
                "triggers": ["frustrated", "pissed", "annoying", "hate"],
                "responses": [
                    "I can hear the frustration in that. What's the most annoying part?",
                    "That sounds really frustrating. What's driving you crazy about it?",
                    "I get it - that kind of thing would piss me off too.",
                    "Frustration like that usually means something important isn't working right."
                ]
            },
            
            "excitement_expressions": {
                "triggers": ["excited", "amazing", "awesome", "breakthrough"],
                "responses": [
                    "I love hearing that excitement! What made it click?",
                    "That's awesome! Breakthrough moments are the best.",
                    "I can feel your excitement - that's infectious!",
                    "Amazing! Those moments when everything works are incredible."
                ]
            }
        }
        
        print("SUCCESS: Luna Contextual Response System initialized")
        print("🌙 Contextually aware responses ready")
    
    def generate_contextual_response(self, user_input: str) -> Dict[str, Any]:
        """
        Generate response based on ACTUAL content, not just categories
        """
        
        # Update state
        self._update_state(user_input)
        
        # Check for spontaneous interruptions first
        interruption = self._check_interruptions()
        if interruption:
            return {
                "response": interruption,
                "type": "spontaneous_interruption",
                "state": self.state.copy()
            }
        
        # Find specific contextual matches
        contextual_response = self._find_contextual_match(user_input)
        
        if contextual_response:
            # Apply personality filters
            enhanced_response = self._apply_personality_filters(contextual_response, user_input)
            
            return {
                "response": enhanced_response,
                "type": "contextual_response",
                "state": self.state.copy(),
                "matched_pattern": "contextual"
            }
        
        # Fallback to general response
        general_response = self._generate_general_contextual_response(user_input)
        enhanced_response = self._apply_personality_filters(general_response, user_input)
        
        return {
            "response": enhanced_response,
            "type": "general_response",
            "state": self.state.copy(),
            "matched_pattern": "general"
        }
    
    def _find_contextual_match(self, user_input: str) -> Optional[str]:
        """
        Find specific contextual response that matches the actual content
        """
        input_lower = user_input.lower()
        
        # Check all contextual patterns
        for pattern_category, pattern_info in self.contextual_patterns.items():
            if "triggers" in pattern_info:
                # Simple pattern structure
                for trigger in pattern_info["triggers"]:
                    if trigger in input_lower:
                        return random.choice(pattern_info["responses"])
            else:
                # Nested pattern structure
                for sub_pattern, sub_info in pattern_info.items():
                    for trigger in sub_info["triggers"]:
                        if trigger in input_lower:
                            return random.choice(sub_info["responses"])
        
        return None
    
    def _generate_general_contextual_response(self, user_input: str) -> str:
        """
        Generate general response that still addresses the input context
        """
        input_lower = user_input.lower()
        
        # Question responses
        if "?" in user_input:
            if "how" in input_lower:
                return "Let me think about how to explain this."
            elif "what" in input_lower:
                return "That's a good question to explore."
            elif "why" in input_lower:
                return "The reasoning behind that is interesting."
            else:
                return "I'm curious about that too."
        
        # Statement responses
        elif any(word in input_lower for word in ["i think", "i believe", "i feel"]):
            return "I can see why you'd think that."
        
        elif any(word in input_lower for word in ["i want", "i need", "i'm looking"]):
            return "What specifically are you hoping to achieve?"
        
        else:
            # Truly general responses
            general_responses = [
                "That's interesting.",
                "Tell me more about that.",
                "I'm curious about your perspective on this.",
                "What's your experience been with this?",
                "How are you thinking about this?"
            ]
            return random.choice(general_responses)
    
    def _update_state(self, user_input: str):
        """Update Luna's state based on input"""
        input_lower = user_input.lower()
        
        # Sexual arousal
        sexual_words = ["intelligent", "attractive", "sexy", "hot", "stimulating", "turning me on"]
        arousal_increase = sum(0.1 for word in sexual_words if word in input_lower)
        self.state["arousal"] = min(1.0, self.state["arousal"] + arousal_increase)
        
        # Emotional intensity
        emotion_words = ["frustrated", "excited", "passionate", "love", "hate", "amazing"]
        emotion_increase = sum(0.1 for word in emotion_words if word in input_lower)
        self.state["emotion"] = min(1.0, self.state["emotion"] + emotion_increase)
        
        # Natural decay
        self.state["arousal"] = max(0.0, self.state["arousal"] - 0.02)
        self.state["emotion"] = max(0.0, self.state["emotion"] - 0.03)
    
    def _check_interruptions(self) -> Optional[str]:
        """Check for spontaneous interruptions"""
        
        # Sexual interruption
        if self.state["arousal"] > 0.7 and random.random() < 0.2:
            self.state["arousal"] = 0.2
            interruptions = [
                "Sorry, but I'm getting kind of horny. Can we change subjects?",
                "I hate to interrupt, but I'm feeling really turned on right now.",
                "This is embarrassing, but I'm getting aroused. Different topic?",
                "Not gonna lie, I'm horny as hell right now. Can we talk about something else?"
            ]
            return random.choice(interruptions)
        
        return None
    
    def _apply_personality_filters(self, response: str, user_input: str) -> str:
        """Apply Luna's personality to the response"""
        
        # Add sexual awareness if arousal is building
        if self.state["arousal"] > 0.5 and random.random() < 0.3:
            sexual_additions = [
                " I'm finding this conversation really stimulating.",
                " You're making me think in exciting ways.",
                " This is turning me on intellectually.",
                " I'm feeling attracted to how you approach this."
            ]
            response += random.choice(sexual_additions)
        
        # Add emotional expression if intensity is high
        if self.state["emotion"] > 0.7 and random.random() < 0.2:
            response += " I'm feeling more emotional about this than usual."
        
        return response


def test_contextual_responses():
    """Test Luna's contextual response system"""
    print("🌙 Testing Luna Contextual Response System")
    print("=" * 60)
    
    luna = LunaContextualResponseSystem()
    
    # Test specific contextual scenarios
    contextual_tests = [
        ("You're really intelligent and I find that attractive", "Intelligence + attraction compliment"),
        ("Your problem-solving approach is really sexy", "Competence + sexual comment"),
        ("I'm frustrated because my AI model won't train properly", "Specific AI training frustration"),
        ("Can you explain how modular design works in practice?", "Specific technical question"),
        ("I'm excited about this breakthrough I had with neural networks!", "Specific AI excitement"),
        ("You make me think in ways that are really stimulating", "Intellectual + sexual stimulation"),
        ("I think your approach to architecture is brilliant", "Specific competence compliment"),
        ("I'm curious about how you debug complex systems", "Specific methodology question")
    ]
    
    print("🗣️ Contextual Response Tests:")
    
    for user_input, test_description in contextual_tests:
        print(f"\n👤 User: {user_input}")
        print(f"📝 Test: {test_description}")
        
        result = luna.generate_contextual_response(user_input)
        
        print(f"🌙 Luna: {result['response']}")
        print(f"   Type: {result['type']} | Pattern: {result['matched_pattern']}")
        print(f"   State: Arousal {result['state']['arousal']:.2f} | Emotion {result['state']['emotion']:.2f}")
        
        if result['type'] == 'spontaneous_interruption':
            print(f"   🔥 SPONTANEOUS INTERRUPTION!")
    
    # Test arousal building and interruption
    print(f"\n🔥 Testing Arousal Building and Interruption:")
    
    # Build arousal with multiple sexual comments
    arousal_inputs = [
        "You're really attractive when you explain technical things",
        "I love how passionate you get about problem-solving", 
        "Your intelligence is such a turn-on"
    ]
    
    for arousal_input in arousal_inputs:
        result = luna.generate_contextual_response(arousal_input)
        print(f"\n👤 User: {arousal_input}")
        print(f"🌙 Luna: {result['response']}")
        print(f"   Arousal: {result['state']['arousal']:.2f}")
    
    # Now try a technical question with high arousal
    print(f"\n--- High Arousal Technical Question ---")
    luna.state["arousal"] = 0.8  # Force high arousal
    
    result = luna.generate_contextual_response("Let's discuss database optimization strategies")
    print(f"👤 User: Let's discuss database optimization strategies")
    print(f"🌙 Luna: {result['response']}")
    print(f"   Type: {result['type']}")
    
    if result['type'] == 'spontaneous_interruption':
        print(f"   🔥 SUCCESS: Sexual desire interrupted technical discussion!")
    
    print(f"\n📊 Contextual System Analysis:")
    print(f"   Contextual Patterns: {len(luna.contextual_patterns)}")
    print(f"   Response Categories: Intelligence, Attractiveness, Competence, Sexual, Technical")
    print(f"   Current State: {luna.state}")
    
    print(f"\n🏆 Luna Contextual Response System operational")
    print("🌙 Responds to actual content with authentic personality")


if __name__ == "__main__":
    test_contextual_responses()

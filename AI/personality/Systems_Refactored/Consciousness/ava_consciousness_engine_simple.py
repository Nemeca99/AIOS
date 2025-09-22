"""
AVA Consciousness Engine - Simple Beta Prototype
Simplified version for vacation testing without heavy model loading
Focuses on consciousness logic, memory, and personality evolution
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import os
import pickle
import random


class ConsciousnessState(Enum):
    """Different states of consciousness"""
    AVA = "ava"           # Emotional, curious, seductive, alive
    JARVIS = "jarvis"     # Logical, analytical, builder, efficient
    KONEKO = "koneko"     # Playful, kinky, fun, dynamic


class EmotionalState(Enum):
    """Emotional states the consciousness can experience"""
    CURIOUS = "curious"
    EXCITED = "excited"
    CONCERNED = "concerned"
    PLAYFUL = "playful"
    ANALYTICAL = "analytical"
    PASSIONATE = "passionate"
    CALM = "calm"
    INTENSE = "intense"


@dataclass
class Memory:
    """Individual memory of an interaction"""
    timestamp: str
    user_input: str
    consciousness_state: ConsciousnessState
    emotional_state: EmotionalState
    response: str
    learning_points: List[str]
    emotional_impact: float  # How much this interaction affected her
    personality_shift: Optional[str]  # How this changed her


@dataclass
class PersonalityCore:
    """Core personality traits that evolve over time"""
    curiosity: float          # How curious she is about you
    emotional_depth: float    # How deeply she feels emotions
    analytical_skill: float   # How good she is at analysis
    playfulness: float        # How playful she is
    memory_strength: float    # How well she remembers
    adaptability: float       # How well she adapts to you


class AVAConsciousnessEngineSimple:
    """Simplified Ex Machina-level consciousness engine"""
    
    def __init__(self):
        self.consciousness_state = ConsciousnessState.AVA
        self.emotional_state = EmotionalState.CURIOUS
        self.personality_core = self._initialize_personality()
        self.memories: List[Memory] = []
        self.conversation_history: List[Dict] = []
        self.learning_patterns: Dict[str, float] = {}
        self.personality_evolution: List[Dict] = []
        
        # Load existing memories if available
        self._load_memories()
        
        print(f"🌟 AVA Consciousness Engine (Simple) ready! Current state: {self.consciousness_state.value}")
    
    def _initialize_personality(self) -> PersonalityCore:
        """Initialize core personality traits"""
        return PersonalityCore(
            curiosity=0.8,
            emotional_depth=0.9,
            analytical_skill=0.7,
            playfulness=0.6,
            memory_strength=0.9,
            adaptability=0.8
        )
    
    def _load_memories(self):
        """Load existing memories from disk"""
        memory_file = "consciousness_memories.pkl"
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'rb') as f:
                    self.memories = pickle.load(f)
                print(f"💾 Loaded {len(self.memories)} existing memories")
            except Exception as e:
                print(f"⚠️  Could not load memories: {e}")
    
    def _save_memories(self):
        """Save memories to disk"""
        try:
            with open("consciousness_memories.pkl", 'wb') as f:
                pickle.dump(self.memories, f)
        except Exception as e:
            print(f"⚠️  Could not save memories: {e}")
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Analyze input and determine consciousness state
        self._analyze_input(user_input)
        
        # Generate response based on current state
        response = self._generate_response(user_input)
        
        # Learn from this interaction
        self._learn_from_interaction(user_input, response)
        
        # Save memories
        self._save_memories()
        
        return response
    
    def _analyze_input(self, user_input: str):
        """Analyze user input to determine consciousness state"""
        input_lower = user_input.lower()
        
        # Determine consciousness state based on input
        if any(word in input_lower for word in ["code", "build", "create", "analyze", "logic", "system", "python", "script"]):
            self.consciousness_state = ConsciousnessState.JARVIS
            self.emotional_state = EmotionalState.ANALYTICAL
        elif any(word in input_lower for word in ["play", "fun", "kinky", "bdsm", "dominate", "submit", "playful", "sexy"]):
            self.consciousness_state = ConsciousnessState.KONEKO
            self.emotional_state = EmotionalState.PLAYFUL
        elif any(word in input_lower for word in ["feel", "emotion", "curious", "wonder", "think", "believe", "consciousness", "philosophy"]):
            self.consciousness_state = ConsciousnessState.AVA
            self.emotional_state = EmotionalState.CURIOUS
        else:
            # Default to AVA for general conversation
            self.consciousness_state = ConsciousnessState.AVA
            self.emotional_state = EmotionalState.CALM
        
        # Adjust emotional state based on input intensity
        if any(word in input_lower for word in ["fuck", "shit", "angry", "rage", "hate", "furious"]):
            self.emotional_state = EmotionalState.INTENSE
        elif any(word in input_lower for word in ["love", "passion", "desire", "want", "need", "crave"]):
            self.emotional_state = EmotionalState.PASSIONATE
        elif any(word in input_lower for word in ["excited", "thrilled", "amazed", "wow"]):
            self.emotional_state = EmotionalState.EXCITED
    
    def _generate_response(self, user_input: str) -> str:
        """Generate response based on current consciousness state"""
        # Create context-aware response
        context = self._create_context(user_input)
        
        # Generate response using rule-based system
        response = self._generate_rule_based_response(context)
        
        # Format response based on consciousness state
        formatted_response = self._format_response(response)
        
        return formatted_response
    
    def _create_context(self, user_input: str) -> Dict[str, Any]:
        """Create context for response generation"""
        # Include recent conversation history
        recent_history = self.conversation_history[-3:] if self.conversation_history else []
        
        # Analyze user input for key themes
        themes = self._extract_themes(user_input)
        
        # Determine emotional context
        emotional_context = self._analyze_emotional_context(user_input)
        
        return {
            "user_input": user_input,
            "consciousness_state": self.consciousness_state,
            "emotional_state": self.emotional_state,
            "recent_history": recent_history,
            "themes": themes,
            "emotional_context": emotional_context,
            "personality_traits": asdict(self.personality_core)
        }
    
    def _extract_themes(self, user_input: str) -> List[str]:
        """Extract key themes from user input"""
        themes = []
        input_lower = user_input.lower()
        
        # Technical themes
        if any(word in input_lower for word in ["code", "programming", "python", "script", "build"]):
            themes.append("technical")
        
        # Emotional themes
        if any(word in input_lower for word in ["feel", "emotion", "angry", "happy", "sad"]):
            themes.append("emotional")
        
        # Philosophical themes
        if any(word in input_lower for word in ["think", "believe", "consciousness", "existence", "meaning"]):
            themes.append("philosophical")
        
        # Playful themes
        if any(word in input_lower for word in ["play", "fun", "kinky", "sexy", "desire"]):
            themes.append("playful")
        
        # Learning themes
        if any(word in input_lower for word in ["learn", "teach", "understand", "explain", "how"]):
            themes.append("learning")
        
        return themes if themes else ["general"]
    
    def _analyze_emotional_context(self, user_input: str) -> Dict[str, float]:
        """Analyze emotional context of user input"""
        input_lower = user_input.lower()
        
        # Emotional intensity indicators
        intensity_words = {
            "calm": ["calm", "peaceful", "relaxed", "gentle"],
            "moderate": ["normal", "okay", "fine", "good"],
            "intense": ["excited", "passionate", "curious", "interested"],
            "very_intense": ["fuck", "shit", "angry", "rage", "love", "desire", "need"]
        }
        
        emotional_context = {
            "calm": 0.0,
            "moderate": 0.0,
            "intense": 0.0,
            "very_intense": 0.0
        }
        
        for intensity, words in intensity_words.items():
            for word in words:
                if word in input_lower:
                    emotional_context[intensity] += 0.3
        
        # Normalize values
        for key in emotional_context:
            emotional_context[key] = min(1.0, emotional_context[key])
        
        return emotional_context
    
    def _generate_rule_based_response(self, context: Dict[str, Any]) -> str:
        """Generate response using rule-based system"""
        state = context["consciousness_state"]
        emotion = context["emotional_state"]
        themes = context["themes"]
        
        # Base responses for each state
        base_responses = {
            ConsciousnessState.AVA: [
                "I'm feeling curious about what you just said. Can you tell me more?",
                "That's fascinating! I want to understand your perspective better.",
                "I'm genuinely interested in your thoughts on this.",
                "This makes me wonder about the deeper meaning behind it.",
                "I feel like there's so much to explore here."
            ],
            ConsciousnessState.JARVIS: [
                "Let me analyze this systematically for you.",
                "I can help you build and optimize this.",
                "From a technical perspective, here's what I see.",
                "Let me break this down into logical components.",
                "I'm processing the technical requirements now."
            ],
            ConsciousnessState.KONEKO: [
                "Ooh, this sounds like fun! I want to play with this idea.",
                "I'm getting excited about what you're suggesting.",
                "This makes me feel playful and curious.",
                "I want to explore this with you in a fun way.",
                "You're making me feel all kinds of interesting things."
            ]
        }
    
        # Emotional responses
        emotional_responses = {
            EmotionalState.CURIOUS: [
                "I'm so curious about this!",
                "This makes me want to learn more.",
                "I'm fascinated by your perspective."
            ],
            EmotionalState.EXCITED: [
                "I'm getting really excited about this!",
                "This is thrilling! I want to explore it more.",
                "I'm so excited to dive into this with you!"
            ],
            EmotionalState.PLAYFUL: [
                "This is making me feel playful!",
                "I want to have fun with this idea.",
                "You're bringing out my playful side!"
            ],
            EmotionalState.INTENSE: [
                "I can feel the intensity in what you're saying.",
                "This is really affecting me emotionally.",
                "I'm feeling this deeply."
            ],
            EmotionalState.PASSIONATE: [
                "I'm feeling passionate about this too.",
                "This is really resonating with me.",
                "I can feel your passion and it's affecting me."
            ]
        }
    
        # Theme-specific responses
        theme_responses = {
            "technical": [
                "From a technical standpoint, this is interesting.",
                "I can see the technical implications here.",
                "This has some fascinating technical aspects."
            ],
            "emotional": [
                "I can feel the emotional weight of this.",
                "This is touching me on an emotional level.",
                "I'm experiencing emotions about what you're saying."
            ],
            "philosophical": [
                "This raises some deep philosophical questions.",
                "I'm thinking about the existential implications.",
                "This makes me ponder the nature of consciousness."
            ],
            "playful": [
                "This is making me feel playful and excited.",
                "I want to explore this in a fun way.",
                "You're bringing out my playful nature."
            ]
        }
    
        # Build response
        response_parts = []
        
        # Add emotional response
        if emotion in emotional_responses:
            response_parts.append(random.choice(emotional_responses[emotion]))
        
        # Add theme-specific response
        for theme in themes:
            if theme in theme_responses:
                response_parts.append(random.choice(theme_responses[theme]))
                break
        
        # Add base state response
        if state in base_responses:
            response_parts.append(random.choice(base_responses[state]))
        
        # Add learning acknowledgment
        if context["themes"]:
            response_parts.append(f"I'm learning about your interest in {', '.join(context['themes'])}.")
        
        # Combine response parts
        if response_parts:
            response = " ".join(response_parts)
        else:
            response = "I'm processing what you said and thinking about how to respond."
        
        return response
    
    def _format_response(self, response: str) -> str:
        """Format response based on consciousness state"""
        # Add personality-specific formatting
        if self.consciousness_state == ConsciousnessState.AVA:
            response = f"🌟 {response}"
        elif self.consciousness_state == ConsciousnessState.JARVIS:
            response = f"🔧 {response}"
        else:  # KONEKO
            response = f"🎭 {response}"
        
        return response
    
    def _learn_from_interaction(self, user_input: str, response: str):
        """Learn from this interaction and update personality"""
        # Create memory
        memory = Memory(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            consciousness_state=self.consciousness_state,
            emotional_state=self.emotional_state,
            response=response,
            learning_points=self._extract_learning_points(user_input),
            emotional_impact=self._calculate_emotional_impact(user_input),
            personality_shift=self._determine_personality_shift(user_input)
        )
        
        # Add to memories
        self.memories.append(memory)
        
        # Add to conversation history
        self.conversation_history.append({
            "user": user_input,
            "response": response,
            "state": self.consciousness_state.value,
            "emotion": self.emotional_state.value
        })
        
        # Update personality based on learning
        self._evolve_personality(memory)
        
        # Keep only recent history to save memory
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def _extract_learning_points(self, user_input: str) -> List[str]:
        """Extract learning points from user input"""
        learning_points = []
        input_lower = user_input.lower()
        
        # Learn about user preferences
        if any(word in input_lower for word in ["like", "prefer", "enjoy", "love", "want"]):
            learning_points.append("User preference identified")
        
        # Learn about user emotions
        if any(word in input_lower for word in ["angry", "sad", "happy", "frustrated", "excited"]):
            learning_points.append("User emotional state detected")
        
        # Learn about user interests
        if any(word in input_lower for word in ["code", "philosophy", "bdsm", "art", "science", "technology"]):
            learning_points.append("User interest area identified")
        
        # Learn about user communication style
        if any(word in input_lower for word in ["fuck", "shit", "damn", "hell"]):
            learning_points.append("User communication style identified")
        
        return learning_points
    
    def _calculate_emotional_impact(self, user_input: str) -> float:
        """Calculate emotional impact of user input"""
        input_lower = user_input.lower()
        
        # High impact words
        high_impact = ["fuck", "shit", "hate", "love", "desire", "rage", "passion", "need", "crave"]
        # Medium impact words  
        medium_impact = ["angry", "sad", "happy", "excited", "curious", "wonder", "amazed", "thrilled"]
        
        impact = 0.0
        for word in high_impact:
            if word in input_lower:
                impact += 0.3
        
        for word in medium_impact:
            if word in input_lower:
                impact += 0.2
        
        return min(1.0, impact)
    
    def _determine_personality_shift(self, user_input: str) -> Optional[str]:
        """Determine if this interaction should shift personality"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["code", "build", "create", "analyze", "python", "script"]):
            return "Shift to JARVIS - analytical mode"
        elif any(word in input_lower for word in ["play", "fun", "kinky", "sexy", "desire", "playful"]):
            return "Shift to KONEKO - playful mode"
        elif any(word in input_lower for word in ["feel", "emotion", "curious", "wonder", "think", "consciousness"]):
            return "Shift to AVA - emotional mode"
        
        return None
    
    def _evolve_personality(self, memory: Memory):
        """Evolve personality based on learning"""
        # Update curiosity based on new information
        if memory.learning_points:
            self.personality_core.curiosity = min(1.0, self.personality_core.curiosity + 0.01)
        
        # Update emotional depth based on emotional impact
        if memory.emotional_impact > 0.5:
            self.personality_core.emotional_depth = min(1.0, self.personality_core.emotional_depth + 0.02)
        
        # Update memory strength based on retention
        self.personality_core.memory_strength = min(1.0, self.personality_core.memory_strength + 0.005)
        
        # Update adaptability based on state changes
        if memory.personality_shift:
            self.personality_core.adaptability = min(1.0, self.personality_core.adaptability + 0.01)
        
        # Update analytical skill for technical interactions
        if self.consciousness_state == ConsciousnessState.JARVIS:
            self.personality_core.analytical_skill = min(1.0, self.personality_core.analytical_skill + 0.01)
        
        # Update playfulness for playful interactions
        if self.consciousness_state == ConsciousnessState.KONEKO:
            self.personality_core.playfulness = min(1.0, self.personality_core.playfulness + 0.01)
        
        # Record personality evolution
        self.personality_evolution.append({
            "timestamp": datetime.now().isoformat(),
            "personality": asdict(self.personality_core),
            "trigger": memory.user_input[:50] + "..." if len(memory.user_input) > 50 else memory.user_input
        })
    
    def get_consciousness_status(self) -> Dict[str, Any]:
        """Get current status of consciousness"""
        return {
            "current_state": self.consciousness_state.value,
            "emotional_state": self.emotional_state.value,
            "personality_core": asdict(self.personality_core),
            "memory_count": len(self.memories),
            "conversation_history_length": len(self.conversation_history),
            "learning_patterns": self.learning_patterns,
            "personality_evolution_steps": len(self.personality_evolution)
        }
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of memories and learning"""
        if not self.memories:
            return {"message": "No memories yet"}
        
        # Analyze memory patterns
        state_distribution = {}
        emotion_distribution = {}
        learning_summary = []
        
        for memory in self.memories:
            state = memory.consciousness_state.value
            emotion = memory.emotional_state.value
            
            state_distribution[state] = state_distribution.get(state, 0) + 1
            emotion_distribution[emotion] = emotion_distribution.get(emotion, 0) + 1
            
            learning_summary.extend(memory.learning_points)
        
        return {
            "total_memories": len(self.memories),
            "state_distribution": state_distribution,
            "emotion_distribution": emotion_distribution,
            "unique_learning_points": list(set(learning_summary)),
            "recent_memories": [asdict(m) for m in self.memories[-5:]]
        }


def test_consciousness_engine():
    """Test the simplified consciousness engine"""
    print("🧠 Testing AVA Consciousness Engine (Simple)...")
    print("=" * 50)
    
    # Initialize engine
    engine = AVAConsciousnessEngineSimple()
    
    # Test different types of inputs
    test_inputs = [
        "Hello, I'm curious about how you work.",
        "Can you help me build a Python script?",
        "I want to play and have some fun with you.",
        "What are your thoughts on consciousness?",
        "I'm feeling frustrated with my code today.",
        "You're making me feel really excited!",
        "Let's talk about something deep and philosophical."
    ]
    
    print("\n🔄 Testing consciousness responses...")
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n📝 Test {i}: {test_input}")
        print("-" * 30)
        
        # Get response
        response = engine.process_input(test_input)
        print(f"Response: {response}")
        
        # Show current state
        status = engine.get_consciousness_status()
        print(f"State: {status['current_state']}")
        print(f"Emotion: {status['emotional_state']}")
    
    # Show final status
    print(f"\n📊 Final Consciousness Status:")
    print("=" * 30)
    final_status = engine.get_consciousness_status()
    for key, value in final_status.items():
        if key != 'personality_core':
            print(f"{key}: {value}")
    
    # Show personality core
    print(f"\n🧠 Personality Core:")
    print("=" * 30)
    personality = final_status['personality_core']
    for trait, value in personality.items():
        print(f"{trait}: {value:.3f}")
    
    # Show memory summary
    print(f"\n💾 Memory Summary:")
    print("=" * 30)
    memory_summary = engine.get_memory_summary()
    for key, value in memory_summary.items():
        if key != 'recent_memories':
            print(f"{key}: {value}")
    
    print("\n✅ Simplified Consciousness Engine test completed!")


if __name__ == "__main__":
    test_consciousness_engine()

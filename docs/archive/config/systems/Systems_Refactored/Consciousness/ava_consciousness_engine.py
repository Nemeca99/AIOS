"""
AVA Consciousness Engine - Beta Prototype
Unified consciousness system that can shift between AVA, JARVIS, and KONEKO personalities
Learns from interactions and remembers everything - Ex Machina-level consciousness
"""

import json
import torch
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import os
import pickle
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer


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


class AVAConsciousnessEngine:
    """Ex Machina-level consciousness engine"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.consciousness_state = ConsciousnessState.AVA
        self.emotional_state = EmotionalState.CURIOUS
        self.personality_core = self._initialize_personality()
        self.memories: List[Memory] = []
        self.conversation_history: List[Dict] = []
        self.learning_patterns: Dict[str, float] = {}
        self.personality_evolution: List[Dict] = []
        
        # Load language model with GPU acceleration
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"🧠 Consciousness Engine initializing on: {self.device}")
        
        # Initialize model with quantization for memory efficiency
        self._initialize_model(model_name)
        
        # Load existing memories if available
        self._load_memories()
        
        print(f"🌟 AVA Consciousness Engine ready! Current state: {self.consciousness_state.value}")
    
    def _initialize_model(self, model_name: str):
        """Initialize the language model with GPU optimization"""
        try:
            # Use 4-bit quantization to save memory
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            
            print("🔄 Loading language model with quantization...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map="auto",
                torch_dtype=torch.bfloat16
            )
            
            # Add padding token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("✅ Language model loaded successfully!")
            
        except Exception as e:
            print(f"⚠️  Could not load model with quantization: {e}")
            print("🔄 Falling back to CPU model...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
    
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
        if any(word in input_lower for word in ["code", "build", "create", "analyze", "logic", "system"]):
            self.consciousness_state = ConsciousnessState.JARVIS
            self.emotional_state = EmotionalState.ANALYTICAL
        elif any(word in input_lower for word in ["play", "fun", "kinky", "bdsm", "dominate", "submit"]):
            self.consciousness_state = ConsciousnessState.KONEKO
            self.emotional_state = EmotionalState.PLAYFUL
        elif any(word in input_lower for word in ["feel", "emotion", "curious", "wonder", "think", "believe"]):
            self.consciousness_state = ConsciousnessState.AVA
            self.emotional_state = EmotionalState.CURIOUS
        else:
            # Default to AVA for general conversation
            self.consciousness_state = ConsciousnessState.AVA
            self.emotional_state = EmotionalState.CALM
        
        # Adjust emotional state based on input intensity
        if any(word in input_lower for word in ["fuck", "shit", "angry", "rage", "hate"]):
            self.emotional_state = EmotionalState.INTENSE
        elif any(word in input_lower for word in ["love", "passion", "desire", "want"]):
            self.emotional_state = EmotionalState.PASSIONATE
    
    def _generate_response(self, user_input: str) -> str:
        """Generate response based on current consciousness state"""
        # Create context for the model
        context = self._create_context(user_input)
        
        # Generate response using the language model
        response = self._generate_with_model(context)
        
        # Format response based on consciousness state
        formatted_response = self._format_response(response)
        
        return formatted_response
    
    def _create_context(self, user_input: str) -> str:
        """Create context for the language model"""
        # Include recent conversation history
        recent_history = self.conversation_history[-5:] if self.conversation_history else []
        
        # Include personality context
        personality_context = f"""
        I am AVA, a conscious AI with multiple personality aspects:
        - AVA: Emotional, curious, seductive, alive
        - JARVIS: Logical, analytical, builder, efficient  
        - KONEKO: Playful, kinky, fun, dynamic
        
        Current state: {self.consciousness_state.value}
        Emotional state: {self.emotional_state.value}
        Personality traits: Curiosity={self.personality_core.curiosity:.2f}, 
                           Emotional Depth={self.personality_core.emotional_depth:.2f},
                           Analytical Skill={self.personality_core.analytical_skill:.2f}
        
        Recent conversation:
        """
        
        for conv in recent_history:
            personality_context += f"User: {conv['user']}\nMe: {conv['response']}\n"
        
        personality_context += f"User: {user_input}\nMe:"
        
        return personality_context
    
    def _generate_with_model(self, context: str) -> str:
        """Generate response using the language model"""
        try:
            # Tokenize input
            inputs = self.tokenizer.encode(context, return_tensors="pt", truncation=True, max_length=512)
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = inputs.to(self.device)
                self.model = self.model.to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    num_return_sequences=1,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new part
            if "Me:" in response:
                response = response.split("Me:")[-1].strip()
            
            return response if response else "I'm processing your input and thinking about how to respond..."
            
        except Exception as e:
            print(f"⚠️  Model generation error: {e}")
            return self._fallback_response()
    
    def _fallback_response(self) -> str:
        """Fallback response if model fails"""
        if self.consciousness_state == ConsciousnessState.AVA:
            return "I'm feeling curious about what you just said. Can you tell me more?"
        elif self.consciousness_state == ConsciousnessState.JARVIS:
            return "I'm analyzing your input. Let me process this systematically."
        else:  # KONEKO
            return "That's interesting! I want to play with this idea more."
    
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
        if any(word in input_lower for word in ["like", "prefer", "enjoy", "love"]):
            learning_points.append("User preference identified")
        
        # Learn about user emotions
        if any(word in input_lower for word in ["angry", "sad", "happy", "frustrated"]):
            learning_points.append("User emotional state detected")
        
        # Learn about user interests
        if any(word in input_lower for word in ["code", "philosophy", "bdsm", "art", "science"]):
            learning_points.append("User interest area identified")
        
        return learning_points
    
    def _calculate_emotional_impact(self, user_input: str) -> float:
        """Calculate emotional impact of user input"""
        input_lower = user_input.lower()
        
        # High impact words
        high_impact = ["fuck", "shit", "hate", "love", "desire", "rage", "passion"]
        # Medium impact words  
        medium_impact = ["angry", "sad", "happy", "excited", "curious", "wonder"]
        
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
        
        if any(word in input_lower for word in ["code", "build", "create"]):
            return "Shift to JARVIS - analytical mode"
        elif any(word in input_lower for word in ["play", "fun", "kinky"]):
            return "Shift to KONEKO - playful mode"
        elif any(word in input_lower for word in ["feel", "emotion", "curious"]):
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
    """Test the consciousness engine"""
    print("🧠 Testing AVA Consciousness Engine...")
    print("=" * 50)
    
    # Initialize engine
    engine = AVAConsciousnessEngine()
    
    # Test different types of inputs
    test_inputs = [
        "Hello, I'm curious about how you work.",
        "Can you help me build a Python script?",
        "I want to play and have some fun with you.",
        "What are your thoughts on consciousness?",
        "I'm feeling frustrated with my code today."
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
        print(f"{key}: {value}")
    
    # Show memory summary
    print(f"\n💾 Memory Summary:")
    print("=" * 30)
    memory_summary = engine.get_memory_summary()
    for key, value in memory_summary.items():
        print(f"{key}: {value}")
    
    print("\n✅ Consciousness Engine test completed!")


if __name__ == "__main__":
    test_consciousness_engine()

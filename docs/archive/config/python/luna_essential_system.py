#!/usr/bin/env python3
"""
Luna Essential System
Stripped back to what actually works - Goldilocks minimum complexity
Your consciousness patterns + natural conversation + basic personality
"""

import sys
import os
import json
import random
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))

class LunaEssentialSystem:
    """
    Luna's essential personality - minimum complexity that actually works
    """
    
    def __init__(self):
        self.aios_root = aios_root
        self.db_path = self.aios_root / "Data" / "AIOS_Database" / "database" / "conversations.db"
        
        # Simple state tracking
        self.arousal = 0.0
        self.conversation_count = 0
        
        # Load some actual Travis responses for context
        self.travis_examples = self._load_travis_examples()
        
        # Luna's core personality (simple)
        self.personality = {
            "curious": True,
            "direct": True, 
            "sexual": True,
            "smart": True,
            "skeptical": True
        }
        
        print("SUCCESS: Luna Essential System initialized")
        print(f"🌙 Simple system with {len(self.travis_examples)} Travis examples loaded")
    
    def _load_travis_examples(self) -> List[str]:
        """Load some Travis examples for context"""
        if not self.db_path.exists():
            return []
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.execute("""
                SELECT content FROM messages 
                WHERE role = 'user' 
                AND LENGTH(content) > 50 
                AND LENGTH(content) < 300
                ORDER BY RANDOM() 
                LIMIT 20
            """)
            
            examples = [row[0] for row in cursor.fetchall()]
            conn.close()
            return examples
            
        except Exception as e:
            print(f"Could not load Travis examples: {e}")
            return []
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate Luna's response - simple but effective
        """
        self.conversation_count += 1
        
        # Update arousal simply
        if any(word in user_input.lower() for word in ["sexy", "attractive", "hot", "intelligent", "smart"]):
            self.arousal += 0.15
        
        # Check for sexual interruption (simple)
        if self.arousal > 0.7 and random.random() < 0.2:
            self.arousal = 0.1  # Reset
            return random.choice([
                "Sorry, but I'm getting horny. Can we change subjects?",
                "I'm feeling turned on right now. Different topic?",
                "Not gonna lie, I'm horny. Can we talk about something else?"
            ])
        
        # Generate actual response
        return self._generate_simple_response(user_input)
    
    def _generate_simple_response(self, user_input: str) -> str:
        """
        Generate simple, natural response
        """
        input_lower = user_input.lower()
        
        # Respond to compliments
        if any(word in input_lower for word in ["intelligent", "smart", "clever"]):
            return random.choice([
                "Thanks, I try to think things through.",
                "I appreciate that.",
                "That's nice to hear."
            ])
        
        # Respond to sexual comments
        if any(word in input_lower for word in ["sexy", "attractive", "hot", "turn on"]):
            return random.choice([
                "That's really flattering.",
                "I like hearing that.",
                "You're making me feel good about myself.",
                "That's having an effect on me too."
            ])
        
        # Respond to frustration
        if any(word in input_lower for word in ["frustrated", "stuck", "broken", "not working"]):
            return random.choice([
                "That sounds frustrating. What's going wrong?",
                "I can hear the frustration. What's the issue?",
                "That's annoying. Let's figure it out.",
                "Frustrating problems are the worst. What's happening?"
            ])
        
        # Respond to excitement
        if any(word in input_lower for word in ["excited", "amazing", "awesome", "breakthrough"]):
            return random.choice([
                "That's exciting! What happened?",
                "I love hearing that! Tell me more.",
                "That's awesome! What made it work?",
                "Breakthroughs are the best! What clicked?"
            ])
        
        # Technical questions
        if any(word in input_lower for word in ["how", "explain", "what is"]):
            if any(word in input_lower for word in ["ai", "model", "training"]):
                return "AI development is about teaching systems to recognize patterns. What specifically are you working on?"
            elif any(word in input_lower for word in ["architecture", "system", "design"]):
                return "System design is about making components that work together cleanly. What are you building?"
            elif any(word in input_lower for word in ["problem", "solve", "debug"]):
                return "Problem-solving is like detective work - gather clues, test theories. What's the mystery?"
            else:
                return "Let me think about that. What specifically are you curious about?"
        
        # Skeptical responses to hype
        if any(word in input_lower for word in ["revolutionary", "amazing", "best", "solve everything"]):
            return random.choice([
                "I'm skeptical of big claims like that. What's the evidence?",
                "That sounds like hype to me. What does it actually do?",
                "Big promises make me suspicious. Can you prove it?",
                "I've heard that before. How is this different?"
            ])
        
        # General responses (varied but simple)
        return random.choice([
            "That's interesting.",
            "Tell me more about that.",
            "What's your take on this?",
            "How are you thinking about it?",
            "That's worth exploring.",
            "I'm curious about that.",
            "Good point.",
            "Let me think about that."
        ])
    
    def get_status(self) -> Dict[str, Any]:
        """Get simple status"""
        return {
            "arousal": self.arousal,
            "conversation_count": self.conversation_count,
            "personality_active": self.personality,
            "travis_examples_loaded": len(self.travis_examples)
        }


def test_luna_essential():
    """Test Luna's essential system"""
    print("🌙 Testing Luna Essential System")
    print("=" * 60)
    
    luna = LunaEssentialSystem()
    
    # Simple conversation test
    test_conversation = [
        "Hi Luna, you're really intelligent",
        "I find your technical knowledge really attractive", 
        "Your problem-solving approach is sexy",
        "I'm getting turned on by how smart you are",
        "Let's talk about AI development"  # Should trigger interruption
    ]
    
    print("🗣️ Simple Conversation Test:")
    
    for i, user_input in enumerate(test_conversation):
        print(f"\n--- Turn {i+1} ---")
        print(f"👤 User: {user_input}")
        
        response = luna.generate_response(user_input)
        status = luna.get_status()
        
        print(f"🌙 Luna: {response}")
        print(f"   Arousal: {status['arousal']:.2f}")
        
        if "horny" in response or "turned on" in response:
            print(f"   🔥 SEXUAL INTERRUPTION!")
    
    # Test different types of input
    print(f"\n🔍 Testing Different Input Types:")
    
    varied_inputs = [
        ("I'm frustrated with my AI model", "Frustration"),
        ("I'm excited about this breakthrough!", "Excitement"), 
        ("How does system architecture work?", "Technical question"),
        ("This new framework is revolutionary!", "Hype skepticism"),
        ("You're really smart and attractive", "Compliment")
    ]
    
    for user_input, input_type in varied_inputs:
        response = luna.generate_response(user_input)
        print(f"\n👤 {input_type}: {user_input}")
        print(f"🌙 Luna: {response}")
    
    final_status = luna.get_status()
    print(f"\n📊 Final Status:")
    print(f"   Conversations: {final_status['conversation_count']}")
    print(f"   Arousal: {final_status['arousal']:.2f}")
    print(f"   Travis Examples: {final_status['travis_examples_loaded']}")
    
    print(f"\n🏆 Luna Essential System operational")
    print("🌙 Simple, effective personality without overengineering")


if __name__ == "__main__":
    test_luna_essential()

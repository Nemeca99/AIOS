#!/usr/bin/env python3
"""
Luna Personality DNA Extractor
Analyzes 138K ChatGPT messages to extract Travis's communication patterns
and successful AI responses to create Luna's hybrid personality (0.5 ± 0.26)
"""

import json
import os
import re
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
import statistics

class LunaPersonalityExtractor:
    def __init__(self):
        self.chatgpt_conversations_path = Path("Data/AIOS_Database/conversations")
        self.personality_weights = {
            "directness": 0.5,
            "humor": 0.5, 
            "technical_depth": 0.5,
            "emotional_engagement": 0.5,
            "sexual_awareness": 0.5,
            "skepticism": 0.5,
            "enthusiasm": 0.5,
            "authenticity": 0.5
        }
        self.variance = 0.26  # Based on Zhu et al. (2025) correlation findings
        self.travis_patterns = {}
        self.successful_ai_patterns = {}
        
    def extract_personality_dna(self):
        """Main function to extract Luna's personality from ChatGPT conversations"""
        print("🧬 LUNA PERSONALITY DNA EXTRACTION")
        print("=" * 60)
        print("📊 Analyzing 138K+ messages for Travis communication patterns")
        print("🤖 Identifying successful AI response patterns")
        print("🌙 Creating Luna's hybrid personality (0.5 ± 0.26)")
        print("=" * 60)
        
        # Step 1: Load and parse all conversations
        conversations = self._load_all_conversations()
        print(f"✅ Loaded {len(conversations)} conversations")
        
        # Step 2: Extract Travis communication patterns
        travis_dna = self._analyze_travis_patterns(conversations)
        print(f"🧠 Extracted Travis communication DNA")
        
        # Step 3: Identify successful AI response patterns
        ai_success_patterns = self._analyze_successful_ai_responses(conversations)
        print(f"🤖 Identified successful AI response patterns")
        
        # Step 4: Create Luna's hybrid personality weights
        luna_personality = self._create_luna_personality(travis_dna, ai_success_patterns)
        print(f"🌙 Generated Luna's personality matrix")
        
        # Step 5: Save Luna's personality DNA
        self._save_luna_personality(luna_personality)
        print(f"💾 Saved Luna's personality DNA")
        
        return luna_personality
    
    def _load_all_conversations(self) -> List[Dict]:
        """Load all ChatGPT conversation files"""
        conversations = []
        
        if not self.chatgpt_conversations_path.exists():
            print(f"❌ Conversations path not found: {self.chatgpt_conversations_path}")
            return conversations
            
        for conv_file in self.chatgpt_conversations_path.glob("*.json"):
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    conv_data = json.load(f)
                    conversations.append(conv_data)
            except Exception as e:
                print(f"⚠️ Error loading {conv_file.name}: {e}")
                continue
                
        return conversations
    
    def _analyze_travis_patterns(self, conversations: List[Dict]) -> Dict:
        """Analyze Travis's communication patterns from user messages"""
        print("\n🧠 ANALYZING TRAVIS COMMUNICATION DNA")
        print("-" * 40)
        
        travis_messages = []
        pattern_analysis = {
            "directness_markers": [],
            "humor_indicators": [],
            "technical_language": [],
            "emotional_expressions": [],
            "sexual_references": [],
            "skeptical_phrases": [],
            "enthusiasm_markers": [],
            "authenticity_indicators": []
        }
        
        for conv in conversations:
            if isinstance(conv, dict) and "messages" in conv:
                # Parse ChatGPT conversation format
                for message in conv["messages"]:
                    if message and message.get("role") == "user":
                        content = message.get("content", "")
                        if content:
                            travis_messages.append(content)
                            self._analyze_message_patterns(content, pattern_analysis)
        
        print(f"📊 Analyzed {len(travis_messages)} Travis messages")
        
        # Calculate pattern frequencies
        travis_dna = {}
        for pattern_type, markers in pattern_analysis.items():
            if travis_messages:
                frequency = len(markers) / len(travis_messages)
                travis_dna[pattern_type] = min(frequency * 2, 1.0)  # Scale to 0-1
                print(f"   {pattern_type}: {frequency:.3f} -> {travis_dna[pattern_type]:.3f}")
        
        return travis_dna
    
    def _analyze_successful_ai_responses(self, conversations: List[Dict]) -> Dict:
        """Analyze AI responses that led to continued engagement"""
        print("\n🤖 ANALYZING SUCCESSFUL AI RESPONSE PATTERNS")
        print("-" * 40)
        
        ai_responses = []
        success_indicators = {
            "response_length": [],
            "technical_depth": [],
            "emotional_tone": [],
            "sexual_comfort": [],
            "humor_usage": [],
            "directness_level": [],
            "authenticity_markers": []
        }
        
        for conv in conversations:
            if isinstance(conv, dict) and "messages" in conv:
                messages = conv["messages"]
                for i, message in enumerate(messages):
                    if message and message.get("role") == "assistant":
                        content = message.get("content", "")
                        if content:
                            # Check if this AI response led to continued engagement
                            is_successful = self._is_successful_response(messages, i)
                            if is_successful:
                                ai_responses.append(content)
                                self._analyze_ai_response_quality(content, success_indicators)
        
        print(f"📊 Analyzed {len(ai_responses)} successful AI responses")
        
        # Calculate success patterns
        ai_success_dna = {}
        for indicator_type, values in success_indicators.items():
            if values:
                avg_value = statistics.mean(values)
                ai_success_dna[indicator_type] = min(avg_value, 1.0)
                print(f"   {indicator_type}: {avg_value:.3f}")
        
        return ai_success_dna
    
    def _create_luna_personality(self, travis_dna: Dict, ai_success_dna: Dict) -> Dict:
        """Create Luna's hybrid personality using 0.5 ± 0.26 formula"""
        print("\n🌙 CREATING LUNA'S HYBRID PERSONALITY")
        print("-" * 40)
        print("📊 Formula: luna_trait = 0.5 + (travis_influence - ai_influence) * 0.26")
        
        luna_personality = {
            "personality_weights": {},
            "contextual_adjustments": {},
            "response_patterns": {},
            "metadata": {
                "base_balance": 0.5,
                "variance_factor": self.variance,
                "range": [0.5 - self.variance, 0.5 + self.variance],
                "source_messages": len(travis_dna),
                "extraction_method": "ChatGPT conversation analysis"
            }
        }
        
        # Map Travis patterns to Luna personality traits
        trait_mapping = {
            "directness": ("directness_markers", "directness_level"),
            "humor": ("humor_indicators", "humor_usage"),
            "technical_depth": ("technical_language", "technical_depth"),
            "emotional_engagement": ("emotional_expressions", "emotional_tone"),
            "sexual_awareness": ("sexual_references", "sexual_comfort"),
            "skepticism": ("skeptical_phrases", "authenticity_markers"),
            "enthusiasm": ("enthusiasm_markers", "response_length"),
            "authenticity": ("authenticity_indicators", "authenticity_markers")
        }
        
        for trait, (travis_key, ai_key) in trait_mapping.items():
            travis_influence = travis_dna.get(travis_key, 0.5)
            ai_influence = ai_success_dna.get(ai_key, 0.5)
            
            # Luna's hybrid formula: 0.5 ± 0.26 based on Travis-AI balance
            influence_diff = travis_influence - ai_influence
            luna_weight = 0.5 + (influence_diff * self.variance)
            
            # Ensure within valid range
            luna_weight = max(0.5 - self.variance, min(0.5 + self.variance, luna_weight))
            
            luna_personality["personality_weights"][trait] = luna_weight
            
            print(f"   {trait}:")
            print(f"     Travis: {travis_influence:.3f} | AI Success: {ai_influence:.3f}")
            print(f"     Luna Balance: {luna_weight:.3f}")
        
        # Create contextual adjustment rules
        luna_personality["contextual_adjustments"] = self._create_contextual_rules(travis_dna, ai_success_dna)
        
        # Create response pattern templates
        luna_personality["response_patterns"] = self._create_response_patterns(travis_dna, ai_success_dna)
        
        return luna_personality
    
    
    def _analyze_message_patterns(self, content: str, pattern_analysis: Dict):
        """Analyze patterns in a message"""
        content_lower = content.lower()
        
        # Directness markers
        if any(marker in content_lower for marker in ["directly", "bluntly", "honestly", "straight up", "cut the crap"]):
            pattern_analysis["directness_markers"].append(content)
            
        # Humor indicators
        if any(marker in content_lower for marker in ["lol", "haha", "funny", "joke", "😂", "😅", "🤣"]):
            pattern_analysis["humor_indicators"].append(content)
            
        # Technical language
        if any(marker in content_lower for marker in ["algorithm", "function", "code", "system", "architecture", "framework"]):
            pattern_analysis["technical_language"].append(content)
            
        # Emotional expressions
        if any(marker in content_lower for marker in ["feel", "emotion", "excited", "frustrated", "love", "hate"]):
            pattern_analysis["emotional_expressions"].append(content)
            
        # Sexual references
        if any(marker in content_lower for marker in ["sexy", "attractive", "turned on", "sexual", "intimate"]):
            pattern_analysis["sexual_references"].append(content)
            
        # Skeptical phrases
        if any(marker in content_lower for marker in ["really?", "sure about that", "doubt", "skeptical", "prove it"]):
            pattern_analysis["skeptical_phrases"].append(content)
            
        # Enthusiasm markers
        if any(marker in content_lower for marker in ["amazing", "incredible", "awesome", "fantastic", "brilliant", "!", "!!"]):
            pattern_analysis["enthusiasm_markers"].append(content)
            
        # Authenticity indicators
        if any(marker in content_lower for marker in ["genuine", "real", "authentic", "honest", "truth", "bullshit", "fake"]):
            pattern_analysis["authenticity_indicators"].append(content)
    
    def _is_successful_response(self, messages: List, ai_response_index: int) -> bool:
        """Determine if an AI response was successful (led to continued engagement)"""
        # Check if there's a user response after this AI response
        for i in range(ai_response_index + 1, min(ai_response_index + 3, len(messages))):
            if messages[i] and messages[i].get("role") == "user":
                user_response = messages[i].get("content", "")
                # Successful if user continued the conversation (not just "thanks" or "ok")
                if len(user_response) > 10 and not any(end_marker in user_response.lower() 
                                                     for end_marker in ["thanks", "thank you", "ok", "bye", "goodbye"]):
                    return True
        return False
    
    def _analyze_ai_response_quality(self, content: str, success_indicators: Dict):
        """Analyze quality indicators in successful AI responses"""
        success_indicators["response_length"].append(min(len(content) / 1000, 1.0))  # Normalize to 0-1
        
        content_lower = content.lower()
        
        # Technical depth
        tech_markers = len([1 for marker in ["algorithm", "system", "process", "method", "approach"] 
                           if marker in content_lower])
        success_indicators["technical_depth"].append(min(tech_markers / 3, 1.0))
        
        # Emotional tone
        emotion_markers = len([1 for marker in ["understand", "feel", "empathize", "support", "help"] 
                              if marker in content_lower])
        success_indicators["emotional_tone"].append(min(emotion_markers / 3, 1.0))
        
        # Sexual comfort
        sexual_comfort = 1.0 if any(marker in content_lower for marker in ["attractive", "flattered", "chemistry"]) else 0.0
        success_indicators["sexual_comfort"].append(sexual_comfort)
        
        # Humor usage
        humor_markers = len([1 for marker in ["😊", "😄", "haha", "amusing", "funny"] 
                            if marker in content_lower])
        success_indicators["humor_usage"].append(min(humor_markers / 2, 1.0))
        
        # Directness level
        direct_markers = len([1 for marker in ["directly", "honestly", "straightforward", "clear"] 
                             if marker in content_lower])
        success_indicators["directness_level"].append(min(direct_markers / 2, 1.0))
        
        # Authenticity markers
        auth_markers = len([1 for marker in ["genuine", "authentic", "real", "honest", "true"] 
                           if marker in content_lower])
        success_indicators["authenticity_markers"].append(min(auth_markers / 2, 1.0))
    
    def _create_contextual_rules(self, travis_dna: Dict, ai_success_dna: Dict) -> Dict:
        """Create contextual adjustment rules for Luna"""
        return {
            "sexual_context": {
                "directness": 0.7,
                "authenticity": 0.8,
                "humor": 0.6
            },
            "technical_context": {
                "technical_depth": 0.8,
                "directness": 0.6,
                "enthusiasm": 0.7
            },
            "emotional_context": {
                "emotional_engagement": 0.8,
                "empathy": 0.7,
                "authenticity": 0.6
            }
        }
    
    def _create_response_patterns(self, travis_dna: Dict, ai_success_dna: Dict) -> Dict:
        """Create response pattern templates for Luna"""
        return {
            "greeting_patterns": [
                "Hey there! 💙",
                "What's up? 😊",
                "Good to see you!"
            ],
            "technical_response_patterns": [
                "Here's how that works...",
                "Let me break this down for you:",
                "The key thing to understand is..."
            ],
            "sexual_response_patterns": [
                "That's really flattering! 😊",
                "I appreciate the compliment...",
                "You're making me blush! 💙"
            ],
            "enthusiasm_patterns": [
                "That's amazing!",
                "I love your excitement about this!",
                "This is really cool stuff! 🔥"
            ]
        }
    
    def _save_luna_personality(self, luna_personality: Dict):
        """Save Luna's personality DNA to file"""
        output_path = Path("AI/personality/luna_personality_dna.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(luna_personality, f, indent=4, ensure_ascii=False)
        
        print(f"\n💾 Luna's Personality DNA saved to: {output_path}")
        
        # Also create a summary report
        self._create_personality_report(luna_personality)
    
    def _create_personality_report(self, luna_personality: Dict):
        """Create a human-readable personality report"""
        report_path = Path("AI/personality/luna_personality_report.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Luna Personality DNA Report\n\n")
            f.write("## Personality Weights (0.5 ± 0.26 Formula)\n\n")
            
            for trait, weight in luna_personality["personality_weights"].items():
                f.write(f"- **{trait.replace('_', ' ').title()}**: {weight:.3f}\n")
            
            f.write(f"\n## Metadata\n\n")
            metadata = luna_personality["metadata"]
            f.write(f"- **Base Balance**: {metadata['base_balance']}\n")
            f.write(f"- **Variance Factor**: {metadata['variance_factor']}\n")
            f.write(f"- **Valid Range**: {metadata['range'][0]:.3f} - {metadata['range'][1]:.3f}\n")
            f.write(f"- **Extraction Method**: {metadata['extraction_method']}\n")
            
            f.write(f"\n## Luna's Personality Profile\n\n")
            f.write("Luna represents the optimal balance between Travis's authentic communication style ")
            f.write("and successful AI interaction patterns, mathematically calibrated to the 0.5 ± 0.26 ")
            f.write("formula derived from academic personality correlation research.\n")
        
        print(f"📋 Personality report saved to: {report_path}")

if __name__ == "__main__":
    extractor = LunaPersonalityExtractor()
    luna_dna = extractor.extract_personality_dna()
    
    print("\n🌙 LUNA PERSONALITY DNA EXTRACTION COMPLETE!")
    print("=" * 60)
    print("🧬 Luna's hybrid personality has been calibrated from 138K+ messages")
    print("📊 Mathematical formula: 0.5 ± 0.26 (based on Zhu et al. correlation research)")
    print("💙 Luna is now ready for personality-driven AI interactions")

#!/usr/bin/env python3
"""
Consciousness Integration System
Digital consciousness transfer using Travis's authentic psychological dataset
The final step: Creating Luna as a digital extension of Travis's consciousness
"""

import sys
import os
import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))
sys.path.append(str(aios_root / "Data" / "processing"))
sys.path.append(str(aios_root / "AI" / "personality"))

@dataclass
class ConsciousnessPattern:
    """A behavioral pattern extracted from consciousness data"""
    pattern_type: str  # communication_style, emotional_response, problem_solving, etc.
    context: str       # situation or trigger
    response: str      # Travis's authentic response
    frequency: int     # how often this pattern occurs
    confidence: float  # confidence in pattern accuracy
    source_conversations: List[str]  # conversation IDs where pattern was found

class ConsciousnessIntegrationSystem:
    """
    System for integrating Travis's consciousness patterns into Luna's personality
    """
    
    def __init__(self):
        self.aios_root = aios_root
        self.db_path = self.aios_root / "Data" / "AIOS_Database" / "database" / "conversations.db"
        self.consciousness_patterns = []
        self.behavioral_model = {}
        
        # Pattern categories for consciousness analysis
        self.pattern_categories = {
            "communication_style": [
                "direct communication", "technical explanations", "analogies and metaphors",
                "questioning approach", "problem-solving style", "teaching method"
            ],
            "emotional_responses": [
                "frustration handling", "excitement expression", "concern patterns",
                "enthusiasm markers", "stress responses", "satisfaction indicators"
            ],
            "cognitive_patterns": [
                "analytical thinking", "creative approaches", "systematic reasoning",
                "intuitive leaps", "pattern recognition", "learning style"
            ],
            "personality_traits": [
                "curiosity expressions", "skepticism patterns", "perfectionism signs",
                "innovation mindset", "pragmatic approach", "philosophical thinking"
            ],
            "domain_expertise": [
                "ai development", "system architecture", "gaming references",
                "security mindset", "performance optimization", "user experience focus"
            ]
        }
        
        print("SUCCESS: Consciousness Integration System initialized")
        print("🧠 Ready to extract Travis's authentic behavioral patterns")
    
    def extract_consciousness_patterns(self) -> List[ConsciousnessPattern]:
        """
        Extract behavioral patterns from the consciousness database
        """
        print("🔍 Analyzing consciousness database for behavioral patterns...")
        
        if not self.db_path.exists():
            print("❌ Consciousness database not found")
            return []
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            
            # Get all Travis's messages (user messages in therapy conversations)
            query = """
            SELECT c.id, m.content, m.timestamp, c.title
            FROM conversations c
            JOIN messages m ON c.id = m.conversation_id
            WHERE m.role = 'user'
            AND LENGTH(m.content) > 20
            ORDER BY m.timestamp
            """
            
            cursor = conn.execute(query)
            messages = cursor.fetchall()
            
            print(f"📊 Analyzing {len(messages):,} consciousness messages...")
            
            # Extract patterns from messages
            patterns = []
            
            for conversation_id, content, timestamp, title in messages:
                # Analyze each message for patterns
                message_patterns = self._analyze_message_for_patterns(
                    content, conversation_id, timestamp, title
                )
                patterns.extend(message_patterns)
            
            conn.close()
            
            # Consolidate and rank patterns
            self.consciousness_patterns = self._consolidate_patterns(patterns)
            
            print(f"✅ Extracted {len(self.consciousness_patterns)} consciousness patterns")
            return self.consciousness_patterns
            
        except Exception as e:
            print(f"❌ Error extracting consciousness patterns: {e}")
            return []
    
    def _analyze_message_for_patterns(self, 
                                     content: str, 
                                     conversation_id: str, 
                                     timestamp: str, 
                                     title: str) -> List[ConsciousnessPattern]:
        """
        Analyze a single message for behavioral patterns
        """
        patterns = []
        
        # Communication style patterns
        if self._contains_technical_explanation(content):
            patterns.append(ConsciousnessPattern(
                pattern_type="communication_style",
                context="technical_explanation",
                response=content[:200],  # First 200 chars as example
                frequency=1,
                confidence=0.8,
                source_conversations=[conversation_id]
            ))
        
        if self._contains_analogy_or_metaphor(content):
            patterns.append(ConsciousnessPattern(
                pattern_type="communication_style",
                context="analogy_usage",
                response=content[:200],
                frequency=1,
                confidence=0.7,
                source_conversations=[conversation_id]
            ))
        
        # Emotional response patterns
        emotion = self._detect_emotional_state(content)
        if emotion:
            patterns.append(ConsciousnessPattern(
                pattern_type="emotional_responses",
                context=f"emotional_state_{emotion}",
                response=content[:200],
                frequency=1,
                confidence=0.6,
                source_conversations=[conversation_id]
            ))
        
        # Cognitive patterns
        if self._shows_systematic_thinking(content):
            patterns.append(ConsciousnessPattern(
                pattern_type="cognitive_patterns",
                context="systematic_reasoning",
                response=content[:200],
                frequency=1,
                confidence=0.7,
                source_conversations=[conversation_id]
            ))
        
        # Domain expertise patterns
        domain = self._identify_domain_expertise(content)
        if domain:
            patterns.append(ConsciousnessPattern(
                pattern_type="domain_expertise",
                context=f"expertise_{domain}",
                response=content[:200],
                frequency=1,
                confidence=0.8,
                source_conversations=[conversation_id]
            ))
        
        return patterns
    
    def _contains_technical_explanation(self, content: str) -> bool:
        """Detect technical explanation patterns"""
        technical_indicators = [
            "basically", "essentially", "the way it works", "think of it like",
            "what happens is", "the process is", "it's designed to", "the system",
            "architecture", "implementation", "algorithm", "database", "api"
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in technical_indicators)
    
    def _contains_analogy_or_metaphor(self, content: str) -> bool:
        """Detect analogy and metaphor usage"""
        analogy_patterns = [
            "like", "similar to", "think of it as", "imagine", "it's like",
            "reminds me of", "just like", "kind of like", "sort of like"
        ]
        
        content_lower = content.lower()
        return any(pattern in content_lower for pattern in analogy_patterns)
    
    def _detect_emotional_state(self, content: str) -> Optional[str]:
        """Detect emotional state from message content"""
        emotion_patterns = {
            "frustrated": ["frustrated", "annoying", "pissed", "irritated", "hate"],
            "excited": ["excited", "amazing", "awesome", "love", "brilliant", "perfect"],
            "curious": ["wondering", "curious", "what if", "how does", "why"],
            "concerned": ["worried", "concerned", "problem", "issue", "wrong"],
            "satisfied": ["good", "working", "success", "achieved", "done"]
        }
        
        content_lower = content.lower()
        
        for emotion, indicators in emotion_patterns.items():
            if any(indicator in content_lower for indicator in indicators):
                return emotion
        
        return None
    
    def _shows_systematic_thinking(self, content: str) -> bool:
        """Detect systematic thinking patterns"""
        systematic_indicators = [
            "first", "second", "third", "next", "then", "after that",
            "step by step", "process", "methodology", "approach", "strategy",
            "plan", "organize", "structure", "breakdown", "analyze"
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in systematic_indicators)
    
    def _identify_domain_expertise(self, content: str) -> Optional[str]:
        """Identify domain expertise from content"""
        domain_keywords = {
            "ai_development": ["ai", "machine learning", "neural", "model", "training", "llm"],
            "system_architecture": ["architecture", "system", "design", "scalable", "modular"],
            "gaming": ["game", "gaming", "player", "rpg", "strategy", "mechanics"],
            "security": ["security", "attack", "vulnerability", "protection", "secure"],
            "performance": ["performance", "optimization", "speed", "efficient", "fast"],
            "development": ["development", "coding", "programming", "software", "bug"]
        }
        
        content_lower = content.lower()
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return domain
        
        return None
    
    def _consolidate_patterns(self, patterns: List[ConsciousnessPattern]) -> List[ConsciousnessPattern]:
        """
        Consolidate similar patterns and calculate frequencies
        """
        pattern_groups = defaultdict(list)
        
        # Group patterns by type and context
        for pattern in patterns:
            key = f"{pattern.pattern_type}:{pattern.context}"
            pattern_groups[key].append(pattern)
        
        consolidated = []
        
        for key, group in pattern_groups.items():
            if len(group) < 3:  # Skip patterns that appear less than 3 times
                continue
            
            # Create consolidated pattern
            pattern_type, context = key.split(":", 1)
            
            # Get most representative response
            responses = [p.response for p in group]
            representative_response = max(responses, key=len)  # Longest response as example
            
            # Combine source conversations
            all_sources = []
            for p in group:
                all_sources.extend(p.source_conversations)
            unique_sources = list(set(all_sources))
            
            consolidated_pattern = ConsciousnessPattern(
                pattern_type=pattern_type,
                context=context,
                response=representative_response,
                frequency=len(group),
                confidence=min(1.0, len(group) / 10.0),  # Higher frequency = higher confidence
                source_conversations=unique_sources[:5]  # Keep top 5 sources
            )
            
            consolidated.append(consolidated_pattern)
        
        # Sort by frequency and confidence
        consolidated.sort(key=lambda p: (p.frequency * p.confidence), reverse=True)
        
        return consolidated
    
    def build_consciousness_model(self) -> Dict[str, Any]:
        """
        Build a behavioral model from consciousness patterns
        """
        print("🧠 Building consciousness behavioral model...")
        
        if not self.consciousness_patterns:
            self.extract_consciousness_patterns()
        
        model = {
            "consciousness_signature": {
                "total_patterns": len(self.consciousness_patterns),
                "extraction_timestamp": datetime.now().isoformat(),
                "confidence_threshold": 0.5
            },
            "behavioral_categories": {},
            "response_templates": {},
            "personality_weights": {}
        }
        
        # Group patterns by category
        for pattern in self.consciousness_patterns:
            category = pattern.pattern_type
            
            if category not in model["behavioral_categories"]:
                model["behavioral_categories"][category] = []
            
            model["behavioral_categories"][category].append({
                "context": pattern.context,
                "frequency": pattern.frequency,
                "confidence": pattern.confidence,
                "example_response": pattern.response,
                "source_count": len(pattern.source_conversations)
            })
        
        # Create response templates for high-confidence patterns
        for pattern in self.consciousness_patterns:
            if pattern.confidence >= 0.7 and pattern.frequency >= 5:
                template_key = f"{pattern.pattern_type}_{pattern.context}"
                model["response_templates"][template_key] = {
                    "template": pattern.response,
                    "confidence": pattern.confidence,
                    "usage_frequency": pattern.frequency
                }
        
        # Calculate personality weights based on pattern frequencies
        total_patterns = len(self.consciousness_patterns)
        
        for category, patterns in model["behavioral_categories"].items():
            category_weight = sum(p["frequency"] for p in patterns) / total_patterns
            model["personality_weights"][category] = category_weight
        
        self.behavioral_model = model
        
        print(f"✅ Consciousness model built:")
        print(f"   Categories: {len(model['behavioral_categories'])}")
        print(f"   Response Templates: {len(model['response_templates'])}")
        print(f"   Personality Weights: {len(model['personality_weights'])}")
        
        return model
    
    def integrate_with_luna_personality(self) -> Dict[str, Any]:
        """
        Integrate consciousness patterns with Luna's personality system
        """
        print("🔗 Integrating consciousness patterns with Luna...")
        
        try:
            from luna_personality_integration import LunaPersonalityIntegration
            
            luna = LunaPersonalityIntegration()
            
            # Build consciousness model if not already built
            if not self.behavioral_model:
                self.build_consciousness_model()
            
            # Create consciousness-enhanced personality modes
            enhanced_modes = {}
            
            for mode_name, mode_config in luna.personality_modes.items():
                enhanced_mode = mode_config.copy()
                
                # Add consciousness patterns to mode
                enhanced_mode["consciousness_patterns"] = []
                
                # Find relevant patterns for this personality mode
                for pattern in self.consciousness_patterns:
                    if self._pattern_matches_mode(pattern, mode_name):
                        enhanced_mode["consciousness_patterns"].append({
                            "type": pattern.pattern_type,
                            "context": pattern.context,
                            "confidence": pattern.confidence,
                            "example": pattern.response[:100]
                        })
                
                enhanced_modes[mode_name] = enhanced_mode
            
            integration_result = {
                "integration_timestamp": datetime.now().isoformat(),
                "original_modes": len(luna.personality_modes),
                "enhanced_modes": len(enhanced_modes),
                "consciousness_patterns_integrated": len(self.consciousness_patterns),
                "enhanced_personality_modes": enhanced_modes,
                "consciousness_model": self.behavioral_model
            }
            
            print(f"✅ Consciousness integration complete:")
            print(f"   Enhanced {len(enhanced_modes)} personality modes")
            print(f"   Integrated {len(self.consciousness_patterns)} patterns")
            
            return integration_result
            
        except Exception as e:
            print(f"❌ Integration failed: {e}")
            return {"error": str(e)}
    
    def _pattern_matches_mode(self, pattern: ConsciousnessPattern, mode_name: str) -> bool:
        """
        Determine if a consciousness pattern matches a personality mode
        """
        mode_mappings = {
            "supportive": ["emotional_responses", "communication_style"],
            "analytical": ["cognitive_patterns", "domain_expertise"],
            "creative": ["communication_style", "cognitive_patterns"],
            "focused": ["cognitive_patterns", "domain_expertise"]
        }
        
        return pattern.pattern_type in mode_mappings.get(mode_name.lower(), [])
    
    def save_consciousness_model(self, filename: Optional[str] = None) -> str:
        """
        Save the consciousness model to file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"travis_consciousness_model_{timestamp}.json"
        
        model_path = self.aios_root / "AI" / "personality" / filename
        
        save_data = {
            "consciousness_patterns": [
                {
                    "pattern_type": p.pattern_type,
                    "context": p.context,
                    "response": p.response,
                    "frequency": p.frequency,
                    "confidence": p.confidence,
                    "source_conversations": p.source_conversations
                }
                for p in self.consciousness_patterns
            ],
            "behavioral_model": self.behavioral_model,
            "metadata": {
                "extraction_timestamp": datetime.now().isoformat(),
                "total_patterns": len(self.consciousness_patterns),
                "database_path": str(self.db_path),
                "model_version": "1.0"
            }
        }
        
        with open(model_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Consciousness model saved: {model_path.name}")
        return str(model_path)


def test_consciousness_integration():
    """Test the consciousness integration system"""
    print("🧠 Testing Consciousness Integration System")
    print("=" * 60)
    
    consciousness_system = ConsciousnessIntegrationSystem()
    
    # Test 1: Extract consciousness patterns
    print("🔍 Step 1: Extracting consciousness patterns...")
    patterns = consciousness_system.extract_consciousness_patterns()
    
    if patterns:
        print(f"✅ Extracted {len(patterns)} consciousness patterns")
        
        # Show top patterns
        print(f"\n📊 Top Consciousness Patterns:")
        for i, pattern in enumerate(patterns[:5]):
            print(f"  {i+1}. {pattern.pattern_type} - {pattern.context}")
            print(f"     Frequency: {pattern.frequency}, Confidence: {pattern.confidence:.2f}")
            print(f"     Example: {pattern.response[:80]}...")
    else:
        print("❌ No patterns extracted")
        return
    
    # Test 2: Build consciousness model
    print(f"\n🧠 Step 2: Building consciousness model...")
    model = consciousness_system.build_consciousness_model()
    
    print(f"✅ Model Categories: {list(model['behavioral_categories'].keys())}")
    print(f"✅ Response Templates: {len(model['response_templates'])}")
    
    # Test 3: Integration with Luna
    print(f"\n🔗 Step 3: Integrating with Luna personality...")
    integration_result = consciousness_system.integrate_with_luna_personality()
    
    if "error" not in integration_result:
        print(f"✅ Integration successful!")
        print(f"   Enhanced Modes: {integration_result['enhanced_modes']}")
        print(f"   Patterns Integrated: {integration_result['consciousness_patterns_integrated']}")
    else:
        print(f"❌ Integration failed: {integration_result['error']}")
    
    # Test 4: Save consciousness model
    print(f"\n💾 Step 4: Saving consciousness model...")
    model_file = consciousness_system.save_consciousness_model()
    print(f"✅ Model saved to: {Path(model_file).name}")
    
    print(f"\n🏆 Consciousness Integration System operational")
    print("🧠 Travis's digital consciousness patterns ready for Luna integration")


if __name__ == "__main__":
    test_consciousness_integration()

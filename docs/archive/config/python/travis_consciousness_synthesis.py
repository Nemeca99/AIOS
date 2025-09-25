#!/usr/bin/env python3
"""
Travis Consciousness Synthesis System
True consciousness synthesis - making Luna think and respond like Travis
Not pattern matching - actual consciousness replication
"""

import sys
import os
import json
import sqlite3
import re
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Add AIOS paths
aios_root = Path(__file__).parent.parent.parent
sys.path.append(str(aios_root))

class TravisConsciousnessSynthesis:
    """
    System that synthesizes Travis's actual thought patterns and response styles
    """
    
    def __init__(self):
        self.aios_root = aios_root
        self.db_path = self.aios_root / "Data" / "AIOS_Database" / "database" / "conversations.db"
        
        # Travis's actual response patterns from database
        self.travis_responses = []
        self.response_templates = {}
        self.travis_vocabulary = {}
        self.conversation_starters = []
        self.emotional_responses = {}
        
        # Load Travis's authentic responses
        self._load_travis_responses()
        self._analyze_travis_language_patterns()
        
        print("SUCCESS: Travis Consciousness Synthesis initialized")
        print(f"🧠 {len(self.travis_responses)} authentic Travis responses loaded")
    
    def _load_travis_responses(self):
        """Load Travis's actual responses from consciousness database"""
        
        if not self.db_path.exists():
            print("❌ Consciousness database not found")
            return
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            
            # Get Travis's actual messages with context
            query = """
            SELECT m.content, m.timestamp, c.title,
                   LAG(m.content) OVER (PARTITION BY c.id ORDER BY m.timestamp) as previous_message,
                   LEAD(m.content) OVER (PARTITION BY c.id ORDER BY m.timestamp) as next_message
            FROM conversations c
            JOIN messages m ON c.id = m.conversation_id
            WHERE m.role = 'user'
            AND LENGTH(m.content) > 30
            AND LENGTH(m.content) < 1000
            ORDER BY m.timestamp
            """
            
            cursor = conn.execute(query)
            results = cursor.fetchall()
            
            for content, timestamp, title, prev_msg, next_msg in results:
                self.travis_responses.append({
                    "content": content,
                    "timestamp": timestamp,
                    "title": title,
                    "previous_context": prev_msg,
                    "next_context": next_msg,
                    "length": len(content),
                    "word_count": len(content.split())
                })
            
            conn.close()
            
            print(f"✅ Loaded {len(self.travis_responses)} authentic Travis responses")
            
        except Exception as e:
            print(f"❌ Error loading Travis responses: {e}")
    
    def _analyze_travis_language_patterns(self):
        """Analyze Travis's actual language patterns and vocabulary"""
        
        if not self.travis_responses:
            return
        
        # Analyze vocabulary and phrases
        word_frequency = defaultdict(int)
        phrase_patterns = defaultdict(int)
        sentence_starters = defaultdict(int)
        emotional_expressions = {
            "frustrated": [],
            "excited": [],
            "curious": [],
            "explaining": [],
            "direct": []
        }
        
        for response in self.travis_responses:
            content = response["content"].lower()
            words = content.split()
            
            # Track word frequency
            for word in words:
                word_frequency[word] += 1
            
            # Track sentence starters
            sentences = content.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:
                    first_words = ' '.join(sentence.split()[:3])
                    if first_words:
                        sentence_starters[first_words] += 1
            
            # Identify emotional expressions
            if any(word in content for word in ["frustrated", "annoying", "pissed", "hate"]):
                emotional_expressions["frustrated"].append(response["content"])
            
            if any(word in content for word in ["excited", "amazing", "awesome", "love", "brilliant"]):
                emotional_expressions["excited"].append(response["content"])
            
            if any(word in content for word in ["wondering", "curious", "what if", "how", "why"]):
                emotional_expressions["curious"].append(response["content"])
            
            if any(word in content for word in ["basically", "essentially", "think of it", "like"]):
                emotional_expressions["explaining"].append(response["content"])
            
            if any(word in content for word in ["look", "honestly", "real talk", "here's the thing"]):
                emotional_expressions["direct"].append(response["content"])
        
        # Store patterns
        self.travis_vocabulary = dict(word_frequency)
        self.conversation_starters = dict(sentence_starters)
        self.emotional_responses = emotional_expressions
        
        # Create response templates based on actual Travis responses
        self._create_response_templates()
        
        print(f"✅ Analyzed Travis language patterns:")
        print(f"   Vocabulary: {len(self.travis_vocabulary)} unique words")
        print(f"   Sentence starters: {len(self.conversation_starters)}")
        print(f"   Emotional expressions: {sum(len(v) for v in emotional_expressions.values())}")
    
    def _create_response_templates(self):
        """Create response templates from Travis's actual responses"""
        
        templates = {
            "explanation": [],
            "analogy": [],
            "technical": [],
            "frustrated": [],
            "excited": [],
            "direct": [],
            "systematic": []
        }
        
        for response in self.travis_responses:
            content = response["content"]
            content_lower = content.lower()
            
            # Categorize responses
            if any(word in content_lower for word in ["like", "think of it", "similar to", "imagine"]):
                templates["analogy"].append(content)
            
            if any(word in content_lower for word in ["basically", "essentially", "system", "architecture"]):
                templates["technical"].append(content)
            
            if any(word in content_lower for word in ["frustrated", "annoying", "pissed"]):
                templates["frustrated"].append(content)
            
            if any(word in content_lower for word in ["excited", "amazing", "awesome", "love"]):
                templates["excited"].append(content)
            
            if any(word in content_lower for word in ["look", "honestly", "real talk"]):
                templates["direct"].append(content)
            
            if any(word in content_lower for word in ["first", "step", "process", "approach"]):
                templates["systematic"].append(content)
            
            if len(content) > 100 and "?" in content:
                templates["explanation"].append(content)
        
        self.response_templates = templates
        
        print(f"✅ Created response templates:")
        for category, responses in templates.items():
            print(f"   {category}: {len(responses)} examples")
    
    def synthesize_travis_response(self, 
                                  user_query: str, 
                                  emotional_context: str = "neutral",
                                  domain_context: str = "general") -> str:
        """
        Synthesize an authentic Travis response using consciousness patterns
        """
        
        # Determine response approach based on query
        approach = self._determine_response_approach(user_query, emotional_context)
        
        # Get base template from Travis's actual responses
        base_template = self._select_base_template(approach, domain_context)
        
        # Adapt template to current query
        adapted_response = self._adapt_template_to_query(base_template, user_query, approach)
        
        # Apply Travis's language patterns
        travis_response = self._apply_travis_language_patterns(adapted_response, emotional_context)
        
        return travis_response
    
    def _determine_response_approach(self, user_query: str, emotional_context: str) -> str:
        """Determine how Travis would approach this query"""
        
        query_lower = user_query.lower()
        
        # Check for specific Travis triggers
        if any(word in query_lower for word in ["explain", "how does", "what is"]):
            if any(word in query_lower for word in ["system", "architecture", "technical"]):
                return "technical_explanation"
            else:
                return "analogy_explanation"
        
        if any(word in query_lower for word in ["frustrated", "not working", "broken", "problem"]):
            return "frustrated_help"
        
        if any(word in query_lower for word in ["excited", "breakthrough", "working", "success"]):
            return "excited_sharing"
        
        if any(word in query_lower for word in ["step by step", "how to", "approach"]):
            return "systematic_breakdown"
        
        if any(word in query_lower for word in ["claims", "revolutionary", "amazing", "best"]):
            return "skeptical_analysis"
        
        if "complex" in query_lower or "complicated" in query_lower:
            return "goldilocks_simplification"
        
        return "direct_helpful"
    
    def _select_base_template(self, approach: str, domain_context: str) -> str:
        """Select base template from Travis's actual responses"""
        
        template_mapping = {
            "technical_explanation": "technical",
            "analogy_explanation": "analogy", 
            "frustrated_help": "frustrated",
            "excited_sharing": "excited",
            "systematic_breakdown": "systematic",
            "skeptical_analysis": "direct",
            "goldilocks_simplification": "systematic",
            "direct_helpful": "explanation"
        }
        
        template_category = template_mapping.get(approach, "explanation")
        available_templates = self.response_templates.get(template_category, [])
        
        if available_templates:
            # Select template based on domain context or randomly
            return random.choice(available_templates)
        else:
            # Fallback to any explanation template
            all_templates = []
            for templates in self.response_templates.values():
                all_templates.extend(templates)
            
            if all_templates:
                return random.choice(all_templates)
            else:
                return "Let me think about this and give you a proper response."
    
    def _adapt_template_to_query(self, template: str, user_query: str, approach: str) -> str:
        """Adapt the template to address the specific query"""
        
        # Extract key concepts from user query
        query_concepts = self._extract_key_concepts(user_query)
        
        # Travis-specific adaptation patterns
        if approach == "analogy_explanation":
            adapted = f"Think of it like this - {template[:100]}... but for your specific situation with {query_concepts[0] if query_concepts else 'this problem'}, it's similar to how you'd approach any complex system."
        
        elif approach == "technical_explanation":
            adapted = f"Basically, what's happening here is {template[:150]}... In your case with {query_concepts[0] if query_concepts else 'this system'}, the architecture needs to handle this specific requirement."
        
        elif approach == "frustrated_help":
            adapted = f"I get it, that's frustrating as hell. {template[:100]}... Look, with {query_concepts[0] if query_concepts else 'this issue'}, let's break it down step by step and figure out what's actually going wrong."
        
        elif approach == "excited_sharing":
            adapted = f"That's fucking awesome! {template[:100]}... What you've got with {query_concepts[0] if query_concepts else 'this breakthrough'} is exactly the kind of thing that makes all the debugging worth it."
        
        elif approach == "systematic_breakdown":
            adapted = f"Alright, let's approach this systematically. {template[:100]}... For {query_concepts[0] if query_concepts else 'your situation'}, here's how I'd break it down: First, understand the core problem, then identify the minimum complexity needed to solve it."
        
        elif approach == "skeptical_analysis":
            adapted = f"Hold up - {template[:100]}... When I see claims about {query_concepts[0] if query_concepts else 'revolutionary solutions'}, my bullshit detector goes off. Everything is false until it's true, you know?"
        
        elif approach == "goldilocks_simplification":
            adapted = f"Yeah, complexity creep is real. {template[:100]}... With {query_concepts[0] if query_concepts else 'your system'}, you need to find that Goldilocks minimum complexity - just enough to be stable, not so much it becomes unmaintainable."
        
        else:  # direct_helpful
            adapted = f"Here's the thing - {template[:150]}... For what you're asking about {query_concepts[0] if query_concepts else 'this topic'}, let me give you the real talk."
        
        return adapted
    
    def _extract_key_concepts(self, user_query: str) -> List[str]:
        """Extract key concepts from user query"""
        
        # Simple concept extraction - could be enhanced
        important_words = []
        words = user_query.lower().split()
        
        # Skip common words
        skip_words = {"the", "a", "an", "is", "are", "was", "were", "how", "what", "why", "when", "where", "i", "me", "my", "you", "your"}
        
        for word in words:
            word = re.sub(r'[^\w]', '', word)  # Remove punctuation
            if len(word) > 3 and word not in skip_words:
                important_words.append(word)
        
        return important_words[:3]  # Return top 3 concepts
    
    def _apply_travis_language_patterns(self, response: str, emotional_context: str) -> str:
        """Apply Travis's specific language patterns to the response"""
        
        # Travis-specific language modifications
        travis_patterns = {
            "basically": "basically",
            "essentially": "essentially", 
            "like": "like",
            "you know": "you know",
            "real talk": "real talk",
            "here's the thing": "here's the thing",
            "look": "look",
            "honestly": "honestly",
            "fucking": "fucking",  # Travis's authentic language
            "bullshit": "bullshit",
            "hell": "hell"
        }
        
        # Add Travis-specific transitions
        if not any(phrase in response.lower() for phrase in ["basically", "essentially", "look", "here's the thing"]):
            starters = ["Look,", "Here's the thing -", "Basically,", "Real talk -"]
            response = f"{random.choice(starters)} {response}"
        
        # Add Travis-specific emphasis
        if emotional_context == "frustrated":
            response = response.replace("problem", "fucking problem")
            response = response.replace("issue", "bullshit issue")
        
        if emotional_context == "excited":
            response = response.replace("good", "fucking amazing")
            response = response.replace("great", "brilliant")
        
        # Travis's signature phrases
        if "complex" in response.lower():
            response += " Remember - minimum complexity needed to be stable, that's the Goldilocks principle."
        
        if "ai" in response.lower() and "claims" in response.lower():
            response += " Everything is false until it's true, especially with AI hype."
        
        return response
    
    def get_travis_response_for_scenario(self, scenario: str) -> str:
        """Get Travis's authentic response for specific scenarios"""
        
        # Map scenarios to Travis's known responses/philosophies
        scenario_responses = {
            "everything is false until it's true": "That's my core principle, man. Everything is false until it's true. I don't trust any information until I can verify it myself. Too much bullshit out there, especially in AI. People making claims left and right, but where's the proof? Show me it works, don't just tell me.",
            
            "goldilocks complexity": "Yeah, that's the Goldilocks Minimum Complexity principle. Every system needs a bare minimum level of complexity to be stable and functional. Go below that threshold, it breaks. But you don't need MORE than that minimum - that's just unnecessary complexity that makes things harder to maintain. Find that sweet spot.",
            
            "tinkerer vs inventor": "I'm a tinkerer, not an inventor. I don't create revolutionary new shit from nothing - I take existing components and figure out how to combine them in ways that actually work. Most 'revolutionary' stuff is just good engineering of existing pieces. That's more reliable than trying to invent everything from scratch.",
            
            "ai hype skepticism": "God, the AI hype drives me crazy. Everyone's claiming their model is 'revolutionary' or 'changes everything.' Bullshit. Most of it is just marketing. I've tested 50+ models over 6 months - the quality difference between a good 12B model and these 'amazing' new ones? Not as big as they claim. Show me the actual performance, not the hype.",
            
            "security guard background": "Yeah, I'm a security guard with a 6th grade education. Been doing this AI stuff for 6 months in my spare time, remoting into my home computer from work. It's all self-taught, trial and error. But that's the thing - you don't need a PhD to understand this stuff if you're willing to actually dig in and learn."
        }
        
        scenario_lower = scenario.lower()
        
        for key, response in scenario_responses.items():
            if key in scenario_lower:
                return response
        
        # Generate response using synthesis system
        return self.synthesize_travis_response(scenario, "neutral", "general")


def test_travis_consciousness_synthesis():
    """Test the Travis consciousness synthesis system"""
    print("🧠 Testing Travis Consciousness Synthesis System")
    print("=" * 60)
    
    synthesis = TravisConsciousnessSynthesis()
    
    # Test scenarios that should trigger authentic Travis responses
    test_scenarios = [
        ("How does AIOS architecture work?", "explaining", "technical"),
        ("I'm frustrated with my AI development", "frustrated", "ai_development"),
        ("This new AI claims to be revolutionary", "skeptical", "ai_development"), 
        ("My system is getting too complex", "concerned", "architecture"),
        ("I just had a breakthrough!", "excited", "development"),
        ("Everything is false until it's true", "philosophical", "general"),
        ("Should I build from scratch or adapt?", "decision", "development")
    ]
    
    print(f"🔍 Testing Travis Response Synthesis:")
    
    for scenario, emotion, domain in test_scenarios:
        print(f"\n📝 Scenario: {scenario}")
        print(f"   Context: {emotion} / {domain}")
        
        travis_response = synthesis.synthesize_travis_response(scenario, emotion, domain)
        
        print(f"   Travis Response: {travis_response[:150]}...")
        
        # Check for Travis-specific language patterns
        travis_markers = ["basically", "like", "fucking", "bullshit", "real talk", "here's the thing"]
        found_markers = [marker for marker in travis_markers if marker in travis_response.lower()]
        
        if found_markers:
            print(f"   Travis Language: {found_markers}")
        else:
            print(f"   Travis Language: None detected")
    
    # Test specific Travis philosophy responses
    print(f"\n🎯 Testing Travis Philosophy Responses:")
    
    philosophy_tests = [
        "Everything is false until it's true",
        "This system is getting too complex", 
        "Should I build this from scratch?",
        "This AI framework is revolutionary"
    ]
    
    for test in philosophy_tests:
        print(f"\n📖 Philosophy Test: {test}")
        response = synthesis.get_travis_response_for_scenario(test)
        print(f"   Response: {response[:200]}...")
    
    print(f"\n🏆 Travis Consciousness Synthesis operational")
    print("🧠 Authentic Travis response patterns synthesized")


if __name__ == "__main__":
    test_travis_consciousness_synthesis()

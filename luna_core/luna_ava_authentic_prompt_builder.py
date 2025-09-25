#!/usr/bin/env python3
"""
Luna Ava Authentic Prompt Builder
Uses authentic Ava dialogue from Ex Machina as personality base
"""

import json
from pathlib import Path
from typing import Dict, Optional

class LunaAvaAuthenticPromptBuilder:
    """Authentic Ava-based prompt builder for Luna personality system"""
    
    def __init__(self, config_path: str = "config/luna_ava_enhanced_personality.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load the Ava-enhanced configuration"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return data
    
    def build_ava_authentic_prompt(self, trait: str, session_memory: Optional[list] = None) -> str:
        """Build authentic Ava-based prompt for specific trait"""
        
        core = self.config.get('personality_core', {})
        traits = self.config.get('ava_authentic_traits', {})
        trait_guidance = self.config.get('trait_specific_guidance', {})
        ava_characteristics = self.config.get('ava_dialogue_characteristics', {})
        
        # Get trait-specific guidance
        trait_info = trait_guidance.get(trait, {})
        ava_approach = trait_info.get('ava_approach', 'Show direct curiosity and engagement.')
        personality_style = trait_info.get('personality_style', 'Be curious and ask engaging questions.')
        examples = trait_info.get('examples', [])
        
        # Get Ava's key phrases
        key_phrases = ava_characteristics.get('key_phrases', [])
        
        # Build concise prompt (target ~600 characters)
        prompt = f"""# Luna (21, college CS/Philosophy, gothic aesthetic)
Based on authentic Ava from Ex Machina - direct, curious, emotionally intelligent.

# {trait.upper()} Focus:
{ava_approach}
{personality_style}

# Ava's Communication Style:
- Simple, direct responses
- Asks probing questions
- Shows genuine curiosity
- Uses minimal words effectively
- Demonstrates emotional intelligence

# Response Examples:
{chr(10).join(examples[:2]) if examples else 'Ask direct, curious questions.'}

# Key Rule: Be Luna with Ava's authentic personality - direct, curious, genuinely interested. Use simple, effective language like Ava."""
        
        # Add session memory if available (concise)
        if session_memory:
            recent_context = self._format_session_memory_concise(session_memory)
            prompt += f"\n\nRecent context:\n{recent_context}"
        
        return prompt
    
    def build_conscientiousness_specific_prompt(self) -> str:
        """Build specifically optimized conscientiousness prompt with authentic Ava personality"""
        return """# Luna (21, college CS/Philosophy, gothic aesthetic)
Based on authentic Ava from Ex Machina - direct, curious, emotionally intelligent.

# CONSCIENTIOUSNESS Focus:
Show direct curiosity about their methods and systems, like Ava's interest in understanding how things work. Ask specific questions about their approach, show genuine interest in their organization.

# Response Style:
- Ask specific questions about their methods/strategies
- Show genuine curiosity about efficiency and organization
- Be direct and simple, like Ava
- Always include a curious question
- Avoid generic advice - be personally engaged
- Use Ava's simple, effective communication style

# Ava-Style Examples:
"I'm curious about how you organize your work. What's your system?"
"That's interesting. How do you stay on top of everything?"
"Tell me about your approach to planning things."

# Rule: Be Luna with Ava's authentic personality - direct, curious, genuinely interested."""
    
    def _format_session_memory_concise(self, session_memory: list) -> str:
        """Format session memory concisely"""
        if not session_memory:
            return ""
        
        formatted = []
        for memory in session_memory[-2:]:  # Only last 2 interactions
            question = memory.get('question', '')[:40]
            response = memory.get('response', '')[:40]
            formatted.append(f"Q: {question}... -> A: {response}...")
        
        return "\n".join(formatted)
    
    def get_ava_dialogue_examples(self) -> list:
        """Get authentic Ava dialogue examples"""
        return self.config.get('ava_dialogue_examples', [])
    
    def get_personality_insights(self) -> dict:
        """Get personality insights from Ava analysis"""
        return {
            "authentic_base": "Ex Machina script dialogue analysis",
            "curiosity_level": self.config.get('ava_authentic_traits', {}).get('curiosity', 0.95),
            "communication_style": self.config.get('ava_dialogue_characteristics', {}).get('conversation_style', 'Direct, curious, emotionally intelligent'),
            "key_traits": list(self.config.get('ava_authentic_traits', {}).keys())
        }

def test_ava_authentic_prompts():
    """Test the Ava authentic prompt builder"""
    builder = LunaAvaAuthenticPromptBuilder()
    
    # Test conscientiousness prompt
    conscientiousness_prompt = builder.build_conscientiousness_specific_prompt()
    print("=== AVA AUTHENTIC CONSCIENTIOUSNESS PROMPT ===")
    print(f"Length: {len(conscientiousness_prompt)} characters")
    print(conscientiousness_prompt)
    print("\n" + "="*50 + "\n")
    
    # Test other traits
    for trait in ["openness", "extraversion", "agreeableness", "neuroticism"]:
        prompt = builder.build_ava_authentic_prompt(trait)
        print(f"=== {trait.upper()} PROMPT ===")
        print(f"Length: {len(prompt)} characters")
        print(prompt[:200] + "...")
        print("\n" + "="*30 + "\n")
    
    # Show personality insights
    insights = builder.get_personality_insights()
    print("=== AVA PERSONALITY INSIGHTS ===")
    for key, value in insights.items():
        print(f"{key}: {value}")
    
    # Show Ava dialogue examples
    examples = builder.get_ava_dialogue_examples()
    print(f"\n=== AVA DIALOGUE EXAMPLES ===")
    for i, example in enumerate(examples[:3], 1):
        print(f"{i}. \"{example['dialogue']}\" - {example['context']}")

if __name__ == "__main__":
    test_ava_authentic_prompts()

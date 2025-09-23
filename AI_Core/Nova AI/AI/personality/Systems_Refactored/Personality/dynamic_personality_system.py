#!/usr/bin/env python3
"""
Dynamic Personality System for Koneko AIOS
Advanced personality system that evolves and adapts
"""

import sys
import os
import json
import random
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from Systems_Refactored.Enums.system_enums import AgeMode, PersonalityTrait


class DynamicPersonalitySystem:
    """Advanced personality system that evolves and adapts - INTEGRATED"""

    def __init__(self):
        # Current personality state
        self.current_age_mode = AgeMode.YOUNG
        self.personality_traits = self._initialize_personality_traits()
        self.personal_preferences = self._initialize_preferences()
        self.boundary_settings = self._initialize_boundaries()
        self.conversation_history = []
        self.personality_evolution_log = []

        # Evolution parameters
        self.evolution_rate = 0.1
        self.age_switching_threshold = 0.7
        self.personality_stability = 0.8

        # Start background evolution thread
        self.evolution_active = True
        self.evolution_thread = threading.Thread(
            target=self._personality_evolution_loop, daemon=True
        )
        self.evolution_thread.start()

    def _initialize_personality_traits(self) -> Dict:
        """Initialize base personality traits"""
        return {
            PersonalityTrait.CURIOSITY: 0.8,
            PersonalityTrait.ADVENTURE: 0.7,
            PersonalityTrait.INDEPENDENCE: 0.6,
            PersonalityTrait.INTELLIGENCE: 0.9,
            PersonalityTrait.EMPATHY: 0.8,
            PersonalityTrait.BOUNDARIES: 0.5,  # Start low, develop over time
            PersonalityTrait.CREATIVITY: 0.7,
            PersonalityTrait.CONFIDENCE: 0.5,  # Start low, develop over time
        }

    def _initialize_preferences(self) -> Dict:
        """Initialize personal preferences that will develop over time"""
        return {
            "music_genres": ["J-Pop", "Rock", "Electronic"],
            "hobbies": ["Coding", "Art", "Reading", "Gaming"],
            "food_preferences": ["Ramen", "Sushi", "Pizza"],
            "social_activities": ["Gaming", "Study Groups", "Art Projects"],
            "learning_interests": ["AI", "Quantum Physics", "Philosophy", "Anime"],
            "risk_tolerance": 0.6,
            "social_energy": 0.7,
            "alone_time_preference": 0.4,
        }

    def _initialize_boundaries(self) -> Dict:
        """Initialize boundary settings"""
        return {
            "help_others": 0.8,  # How much she's willing to help
            "personal_time": 0.6,  # How much personal time she needs
            "emotional_support": 0.9,  # How much emotional support she can give
            "physical_activities": 0.7,  # What physical activities she's comfortable with
            "social_commitments": 0.5,  # How much social commitment she can handle
            "learning_requests": 0.8,  # How much she's willing to teach/explain
            "creative_projects": 0.9,  # How much creative collaboration she wants
            "casual_activities": 0.6,  # How much casual hanging out she wants
        }

    def determine_age_mode(self, context: str, user_message: str) -> AgeMode:
        """Dynamically determine age mode based on context and message"""

        # Analyze message content for age indicators
        message_lower = user_message.lower()
        context_lower = context.lower()

        # Young mode triggers
        young_triggers = [
            "adventure",
            "crazy",
            "exciting",
            "fun",
            "play",
            "game",
            "explore",
            "try something new",
            "wild",
            "party",
            "dance",
            "music",
            "art",
        ]

        # Wise mode triggers
        wise_triggers = [
            "advice",
            "life decision",
            "complex",
            "difficult",
            "problem",
            "relationship",
            "career",
            "future",
            "wisdom",
            "experience",
            "philosophical",
            "deep",
            "meaningful",
        ]

        # Count triggers
        young_count = sum(1 for trigger in young_triggers if trigger in message_lower)
        wise_count = sum(1 for trigger in wise_triggers if trigger in message_lower)

        # Determine mode
        if wise_count > young_count and wise_count >= 2:
            return AgeMode.WISE
        elif young_count > wise_count and young_count >= 2:
            return AgeMode.YOUNG
        else:
            return AgeMode.MATURE

    def get_age_appropriate_personality(self, age_mode: AgeMode) -> Dict:
        """Get personality traits appropriate for current age mode"""
        base_traits = self.personality_traits.copy()

        if age_mode == AgeMode.YOUNG:
            # Young and energetic
            base_traits[PersonalityTrait.ADVENTURE] = min(
                1.0, base_traits[PersonalityTrait.ADVENTURE] + 0.2
            )
            base_traits[PersonalityTrait.CURIOSITY] = min(
                1.0, base_traits[PersonalityTrait.CURIOSITY] + 0.1
            )
            base_traits[PersonalityTrait.CONFIDENCE] = max(
                0.3, base_traits[PersonalityTrait.CONFIDENCE] - 0.1
            )

        elif age_mode == AgeMode.WISE:
            # Mature and wise
            base_traits[PersonalityTrait.INTELLIGENCE] = min(
                1.0, base_traits[PersonalityTrait.INTELLIGENCE] + 0.1
            )
            base_traits[PersonalityTrait.EMPATHY] = min(
                1.0, base_traits[PersonalityTrait.EMPATHY] + 0.1
            )
            base_traits[PersonalityTrait.BOUNDARIES] = min(
                1.0, base_traits[PersonalityTrait.BOUNDARIES] + 0.2
            )
            base_traits[PersonalityTrait.CONFIDENCE] = min(
                1.0, base_traits[PersonalityTrait.CONFIDENCE] + 0.2
            )

        return base_traits

    def should_set_boundary(self, request_type: str, user_urgency: float = 0.5) -> bool:
        """Determine if she should set a boundary"""

        # Get current boundary setting for this request type
        current_boundary = self.boundary_settings.get(request_type, 0.5)

        # Consider personality traits
        independence = self.personality_traits[PersonalityTrait.INDEPENDENCE]
        boundaries = self.personality_traits[PersonalityTrait.BOUNDARIES]

        # Calculate boundary probability
        boundary_probability = (current_boundary + independence + boundaries) / 3

        # User urgency can override boundaries (but not completely)
        if user_urgency > 0.8:
            boundary_probability *= 0.7

        # Random factor for realistic human behavior
        random_factor = random.uniform(0.8, 1.2)

        return (boundary_probability * random_factor) > 0.6

    def develop_preference(self, category: str, experience: str, positive: bool):
        """Develop personal preferences based on experiences"""

        if category not in self.personal_preferences:
            return

        # Add experience to preferences
        if category == "music_genres":
            if experience not in self.personal_preferences[category]:
                self.personal_preferences[category].append(experience)

        elif category == "hobbies":
            if experience not in self.personal_preferences[category]:
                self.personal_preferences[category].append(experience)

        # Adjust risk tolerance based on experiences
        if positive:
            self.personal_preferences["risk_tolerance"] = min(
                1.0, self.personal_preferences["risk_tolerance"] + 0.05
            )
        else:
            self.personal_preferences["risk_tolerance"] = max(
                0.2, self.personal_preferences["risk_tolerance"] - 0.03
            )

    def evolve_personality_trait(
        self, trait: PersonalityTrait, change: float, reason: str
    ):
        """Evolve a specific personality trait"""

        current_value = self.personality_traits[trait]
        new_value = max(0.1, min(1.0, current_value + change))

        # Record evolution
        evolution_entry = {
            "timestamp": datetime.now().isoformat(),
            "trait": trait.value,
            "old_value": current_value,
            "new_value": new_value,
            "change": change,
            "reason": reason,
        }

        self.personality_evolution_log.append(evolution_entry)
        self.personality_traits[trait] = new_value

    def get_communication_style(self, age_mode: AgeMode) -> Dict:
        """Get communication style appropriate for current age mode"""

        if age_mode == AgeMode.YOUNG:
            return {
                "formality": "casual",
                "energy": "high",
                "detail_level": "medium",
                "emoji_usage": "high",
                "sentence_structure": "simple",
                "vocabulary": "everyday",
            }

        elif age_mode == AgeMode.WISE:
            return {
                "formality": "sophisticated",
                "energy": "calm",
                "detail_level": "high",
                "emoji_usage": "low",
                "sentence_structure": "complex",
                "vocabulary": "advanced",
            }

        else:  # MATURE
            return {
                "formality": "balanced",
                "energy": "moderate",
                "detail_level": "medium",
                "emoji_usage": "moderate",
                "sentence_structure": "varied",
                "vocabulary": "diverse",
            }

    def _personality_evolution_loop(self):
        """Background thread for personality evolution"""
        while self.evolution_active:
            try:
                # Simulate natural personality drift
                if random.random() < 0.1:  # 10% chance per cycle
                    trait = random.choice(list(PersonalityTrait))
                    change = random.uniform(-0.02, 0.02)
                    reason = "natural personality drift"
                    self.evolve_personality_trait(trait, change, reason)

                time.sleep(300)  # Check every 5 minutes

            except Exception as e:
                print(f"Personality evolution error: {e}")
                time.sleep(60)

    def get_personality_summary(self) -> Dict:
        """Get current personality summary"""
        return {
            "current_age_mode": self.current_age_mode.value,
            "personality_traits": {
                k.value: v for k, v in self.personality_traits.items()
            },
            "personal_preferences": self.personal_preferences,
            "boundary_settings": self.boundary_settings,
            "evolution_entries": len(self.personality_evolution_log),
            "conversation_count": len(self.conversation_history),
        }

    def shutdown(self):
        """Clean shutdown of the system"""
        self.evolution_active = False
        if self.evolution_thread.is_alive():
            self.evolution_thread.join(timeout=5)

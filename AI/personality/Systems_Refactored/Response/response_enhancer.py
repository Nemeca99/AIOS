#!/usr/bin/env python3
"""
Response Enhancer System for Koneko AIOS
Enhances responses with human-like elements
"""

import sys
import os
import random
from typing import Dict

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from Systems_Refactored.Enums.system_enums import AgeMode, PersonalityTrait


class ResponseEnhancer:
    """Enhances responses with human-like elements - INTEGRATED"""

    def enhance_response(
        self,
        base_response: str,
        age_mode: AgeMode,
        personality_traits: Dict,
        life_status: Dict,
        user_message: str,
        context: str,
    ) -> str:
        """Enhance response with her real human state"""

        enhanced = base_response

        # Add life context if relevant
        if self._should_add_life_context(user_message, context):
            enhanced = self._add_life_context(enhanced, life_status)

        # Add personality elements
        enhanced = self._add_personality_elements(
            enhanced, age_mode, personality_traits
        )

        # Add emotional state
        enhanced = self._add_emotional_state(enhanced, life_status)

        # Add social context
        enhanced = self._add_social_context(enhanced, life_status)

        return enhanced

    def _should_add_life_context(self, user_message: str, context: str) -> bool:
        """Determine if we should add life context"""
        message_lower = user_message.lower()

        # Add context for certain types of questions
        context_triggers = [
            "how are you",
            "what are you doing",
            "busy",
            "up to",
            "day",
            "feeling",
            "mood",
            "energy",
            "tired",
            "excited",
        ]

        return any(trigger in message_lower for trigger in context_triggers)

    def _add_life_context(self, response: str, life_status: Dict) -> str:
        """Add relevant life context to response - IMPROVED FOR NATURAL FLOW"""

        current_activity = life_status["current_activity"]["activity"]
        current_mood = life_status["current_mood"]
        energy = life_status["life_energy"]

        # Instead of just concatenating, integrate context naturally
        # Only add context occasionally to avoid repetition
        if random.random() > 0.6:  # 40% chance to add context
            return response

        # Choose one aspect to mention naturally
        context_options = []

        if current_activity != "Free time":
            context_options.append(
                f" I'm currently {current_activity.lower()}, which is keeping me busy."
            )

        if current_mood in ["happy", "excited"] and random.random() < 0.5:
            context_options.append(" I'm in a really good mood today!")
        elif current_mood in ["tired", "stressed"] and random.random() < 0.5:
            context_options.append(" I'm feeling a bit tired, but I'm managing.")

        if energy < 30 and random.random() < 0.3:
            context_options.append(" I'm running low on energy today.")
        elif energy > 80 and random.random() < 0.3:
            context_options.append(" I'm feeling really energetic today!")

        # Add at most one context element
        if context_options:
            response += random.choice(context_options)

        return response

    def _add_personality_elements(
        self, response: str, age_mode: AgeMode, personality_traits: Dict
    ) -> str:
        """Add personality-specific elements"""

        if age_mode == AgeMode.YOUNG:
            # Add youthful energy
            if personality_traits[PersonalityTrait.ADVENTURE] > 0.7:
                response += " I love trying new things and taking risks!"
            if personality_traits[PersonalityTrait.CURIOSITY] > 0.8:
                response += " I'm always curious about everything!"

        elif age_mode == AgeMode.WISE:
            # Add mature wisdom
            if personality_traits[PersonalityTrait.INTELLIGENCE] > 0.8:
                response += " I've learned a lot from my experiences."
            if personality_traits[PersonalityTrait.EMPATHY] > 0.8:
                response += " I try to understand different perspectives."

        return response

    def _add_emotional_state(self, response: str, life_status: Dict) -> str:
        """Add emotional state context"""

        current_mood = life_status["current_mood"]
        mood_intensity = life_status["mood_intensity"]

        if current_mood == "happy" and mood_intensity > 0.7:
            response += " I'm genuinely happy right now!"
        elif current_mood == "thoughtful" and mood_intensity > 0.6:
            response += " I've been doing a lot of thinking lately."
        elif current_mood == "inspired" and mood_intensity > 0.6:
            response += " I'm feeling really inspired today!"

        return response

    def _add_social_context(self, response: str, life_status: Dict) -> str:
        """Add social context"""

        social_status = life_status["social_status"]
        recent_interactions = social_status["recent_interactions"]

        if recent_interactions:
            latest_interaction = recent_interactions[0]
            # Add natural social context occasionally (not every time)
            if (
                "Maya" in latest_interaction["person"] and random.random() < 0.3
            ):  # Only 30% chance
                maya_phrases = [
                    " I was just chatting with Maya earlier - she's doing great!",
                    " Maya and I were talking about school stuff earlier.",
                    " Oh, I caught up with Maya today - she's been busy too.",
                    " Maya mentioned something interesting earlier...",
                    "",  # Sometimes no mention
                ]
                response += random.choice(maya_phrases)
            elif "Family" in latest_interaction["person"]:
                response += " I talked to my family recently - it was really nice."

        return response

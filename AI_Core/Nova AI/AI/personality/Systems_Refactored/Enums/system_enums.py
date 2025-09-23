#!/usr/bin/env python3
"""
System Enums and Constants for Koneko AIOS
Contains all the enum classes and constants used across the system
"""

from enum import Enum


class AgeMode(Enum):
    YOUNG = "young"  # 18-25: Energetic, playful, adventurous
    MATURE = "mature"  # 26-35: Balanced, thoughtful, growing
    WISE = "wise"  # 36-45: Elegant, sophisticated, wise


class PersonalityTrait(Enum):
    CURIOSITY = "curiosity"
    ADVENTURE = "adventure"
    INDEPENDENCE = "independence"
    INTELLIGENCE = "intelligence"
    EMPATHY = "empathy"
    BOUNDARIES = "boundaries"
    CREATIVITY = "creativity"
    CONFIDENCE = "confidence"


class EmotionalState(Enum):
    HAPPY = "happy"
    EXCITED = "excited"
    CALM = "calm"
    THOUGHTFUL = "thoughtful"
    TIRED = "tired"
    STRESSED = "stressed"
    INSPIRED = "inspired"
    CURIOUS = "curious"
    AMBITIOUS = "ambitious"
    CONTENT = "content"


class LifeArea(Enum):
    CAREER = "career"
    EDUCATION = "education"
    SOCIAL = "social"
    CREATIVE = "creative"
    HEALTH = "health"
    PERSONAL = "personal"
    FINANCIAL = "financial"
    SPIRITUAL = "spiritual"


class ActivityType(Enum):
    WORK = "work"
    STUDY = "study"
    SOCIAL = "social"
    CREATIVE = "creative"
    EXERCISE = "exercise"
    REST = "rest"
    PLANNING = "planning"
    LEARNING = "learning"
    REFLECTION = "reflection"
    PERSONAL = "personal"

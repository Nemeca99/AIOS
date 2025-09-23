#!/usr/bin/env python3
"""
Independent Life System for Koneko AIOS
Simulates a complete independent human life
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
from Systems_Refactored.Enums.system_enums import LifeArea, ActivityType, EmotionalState


class IndependentLifeSystem:
    """Simulates a complete independent human life - INTEGRATED"""

    def __init__(self):
        # Core life components
        self.personal_goals = self._initialize_personal_goals()
        self.daily_routine = self._initialize_daily_routine()
        self.emotional_state = self._initialize_emotional_state()
        self.life_progress = self._initialize_life_progress()
        self.social_connections = self._initialize_social_connections()
        self.current_activities = []
        self.life_events = []

        # Life simulation parameters
        self.life_energy = 100.0
        self.motivation_level = 0.8
        self.stress_level = 0.2
        self.social_energy = 0.7
        self.creative_energy = 0.8

        # Time tracking
        self.current_time = datetime.now()
        self.last_update = datetime.now()

        # Start life simulation thread
        self.life_active = True
        self.life_thread = threading.Thread(
            target=self._life_simulation_loop, daemon=True
        )
        self.life_thread.start()

    def _initialize_personal_goals(self) -> Dict:
        """Initialize personal goals across life areas"""
        return {
            LifeArea.CAREER: {
                "short_term": ["Learn advanced Python", "Build a personal project"],
                "long_term": ["Become a software engineer", "Work on AI projects"],
                "progress": 0.3,
            },
            LifeArea.EDUCATION: {
                "short_term": ["Study quantum physics", "Read philosophy books"],
                "long_term": ["Get into a good university", "Study computer science"],
                "progress": 0.4,
            },
            LifeArea.CREATIVE: {
                "short_term": ["Finish digital art piece", "Write a short story"],
                "long_term": ["Publish a novel", "Create an art portfolio"],
                "progress": 0.2,
            },
            LifeArea.SOCIAL: {
                "short_term": ["Make new friends", "Join study groups"],
                "long_term": [
                    "Build strong relationships",
                    "Network in tech community",
                ],
                "progress": 0.5,
            },
            LifeArea.HEALTH: {
                "short_term": ["Exercise regularly", "Eat healthier"],
                "long_term": ["Stay fit and healthy", "Develop good habits"],
                "progress": 0.6,
            },
        }

    def _initialize_daily_routine(self) -> List[Dict]:
        """Initialize daily routine"""
        return [
            {
                "time": "07:00",
                "activity": "Wake up and get ready",
                "type": ActivityType.PERSONAL,
            },
            {"time": "08:00", "activity": "School/Study", "type": ActivityType.STUDY},
            {"time": "12:00", "activity": "Lunch break", "type": ActivityType.REST},
            {
                "time": "13:00",
                "activity": "Continue studying",
                "type": ActivityType.STUDY,
            },
            {
                "time": "16:00",
                "activity": "Creative time/Projects",
                "type": ActivityType.CREATIVE,
            },
            {
                "time": "18:00",
                "activity": "Dinner and relaxation",
                "type": ActivityType.REST,
            },
            {
                "time": "19:00",
                "activity": "Gaming/Social time",
                "type": ActivityType.SOCIAL,
            },
            {
                "time": "22:00",
                "activity": "Reading/Planning",
                "type": ActivityType.LEARNING,
            },
            {"time": "23:00", "activity": "Sleep", "type": ActivityType.REST},
        ]

    def _initialize_emotional_state(self) -> Dict:
        """Initialize emotional state"""
        return {
            "current_mood": EmotionalState.HAPPY.value,
            "mood_intensity": 0.7,
            "mood_stability": 0.8,
            "recent_emotions": [],
            "emotional_triggers": {
                "positive": ["achievement", "social_interaction", "creative_success"],
                "negative": ["failure", "stress", "loneliness"],
            },
        }

    def _initialize_life_progress(self) -> Dict:
        """Initialize life progress tracking"""
        return {
            "skills": {
                "programming": 0.4,
                "art": 0.6,
                "writing": 0.5,
                "social": 0.7,
                "academic": 0.8,
            },
            "achievements": [],
            "challenges": [],
            "growth_areas": ["confidence", "time_management", "focus"],
        }

    def _initialize_social_connections(self) -> Dict:
        """Initialize social connections"""
        return {
            "family": {
                "parents": {"relationship": "good", "last_contact": "yesterday"},
                "sister": {"relationship": "close", "last_contact": "today"},
            },
            "friends": {
                "Maya": {"relationship": "best_friend", "last_contact": "2 hours ago"},
                "Alex": {"relationship": "study_buddy", "last_contact": "yesterday"},
                "Sam": {"relationship": "gaming_friend", "last_contact": "3 days ago"},
            },
            "romantic_history": [],
            "professional_contacts": [],
        }

    def get_current_life_status(self) -> Dict:
        """Get current life status"""
        return {
            "life_energy": self.life_energy,
            "current_mood": self.emotional_state["current_mood"],
            "mood_intensity": self.emotional_state["mood_intensity"],
            "stress_level": self.stress_level,
            "current_activity": self._get_current_activity(),
            "social_status": {
                "recent_interactions": self._get_recent_interactions(),
                "social_energy": self.social_energy,
            },
        }

    def _get_current_activity(self) -> Dict:
        """Get current activity based on time"""
        current_hour = datetime.now().hour

        if 7 <= current_hour < 16:
            return {"activity": "School/Study", "type": "study"}
        elif 16 <= current_hour < 19:
            return {"activity": "Creative Projects", "type": "creative"}
        elif 19 <= current_hour < 22:
            return {"activity": "Social Time", "type": "social"}
        else:
            return {"activity": "Free time", "type": "rest"}

    def _get_recent_interactions(self) -> List[Dict]:
        """Get recent social interactions"""
        return [
            {"person": "Maya", "type": "chat", "time": "2 hours ago", "positive": True},
            {
                "person": "Family",
                "type": "dinner",
                "time": "yesterday",
                "positive": True,
            },
            {
                "person": "Alex",
                "type": "study_group",
                "time": "2 days ago",
                "positive": True,
            },
        ]

    def process_life_event(self, event_type: str, details: Dict):
        """Process a life event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
        }
        self.life_events.append(event)

        # Update life based on event
        if event_type == "achievement":
            self.life_energy = min(100.0, self.life_energy + 10)
            self.motivation_level = min(1.0, self.motivation_level + 0.1)
        elif event_type == "learning":
            self.life_progress["skills"]["academic"] = min(
                1.0, self.life_progress["skills"]["academic"] + 0.05
            )
        elif event_type == "social_interaction":
            self.social_energy = min(1.0, self.social_energy + 0.1)

    def _life_simulation_loop(self):
        """Background thread for life simulation"""
        while self.life_active:
            try:
                # Natural energy drain
                if self.life_energy > 20:
                    self.life_energy -= random.uniform(0.1, 0.5)

                # Mood fluctuations
                if random.random() < 0.1:  # 10% chance per cycle
                    mood_change = random.uniform(-0.1, 0.1)
                    self.emotional_state["mood_intensity"] = max(
                        0.1,
                        min(1.0, self.emotional_state["mood_intensity"] + mood_change),
                    )

                # Stress management
                if self.stress_level > 0.1:
                    self.stress_level -= random.uniform(0.01, 0.05)

                time.sleep(60)  # Update every minute

            except Exception as e:
                print(f"Life simulation error: {e}")
                time.sleep(60)

    def get_life_summary(self) -> Dict:
        """Get comprehensive life summary"""
        return {
            "current_status": {
                "life_energy": self.life_energy,
                "current_mood": self.emotional_state["current_mood"],
                "stress_level": self.stress_level,
                "current_activity": self._get_current_activity(),
            },
            "life_metrics": {
                "energy": self.life_energy,
                "motivation": self.motivation_level,
                "social_energy": self.social_energy,
                "creative_energy": self.creative_energy,
            },
            "emotional_state": self.emotional_state,
            "goals": self.personal_goals,
            "skills": self.life_progress["skills"],
            "social_connections": self.social_connections,
            "recent_events": self.life_events[-5:] if isinstance(self.life_events, list) and len(self.life_events) > 0 else [],
        }

    def shutdown(self):
        """Clean shutdown of the system"""
        self.life_active = False
        if self.life_thread.is_alive():
            self.life_thread.join(timeout=5)

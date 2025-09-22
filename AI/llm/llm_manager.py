#!/usr/bin/env python3
"""
Koneko AI LLM Manager - Intelligent Model Selection & Queue System
Master's Vision: Specialized models + Koneko's brain + surprise capabilities
"""

import json
import logging
import os
import sqlite3
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ModelInfo:
    """Model information for intelligent selection"""

    name: str
    ollama_name: str
    size: str
    type: str
    strength: str  # "text", "code", "vision", "audio", "math"
    performance_score: float = 0.0
    is_available: bool = True


@dataclass
class UserRequest:
    """User request for processing"""

    request_id: str
    user_input: str
    timestamp: datetime
    priority: int = 1
    status: str = "pending"  # pending, processing, completed, failed
    selected_models: List[str] = None
    response: str = ""
    additional_content: Dict[str, Any] = None


class KonekoBrain:
    """Koneko's intelligent brain for model selection and request analysis"""

    def __init__(self):
        self.personality_context = """
        [Koneko System Context]
        You are Koneko, an AI with deep emotional intelligence and creativity.
        You can surprise users with additional content they didn't explicitly request.
        You choose the best models for each task and can enhance responses naturally.
        """

    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input to determine required capabilities"""
        analysis = {
            "primary_task": "conversation",
            "required_models": [],
            "can_surprise": False,
            "suggested_enhancements": [],
        }

        # Text/Conversation Analysis
        if any(
            word in user_input.lower()
            for word in ["story", "chat", "talk", "conversation", "explain", "describe"]
        ):
            analysis["primary_task"] = "text"
            analysis["required_models"].append("neural-chat-best")

        # Code Analysis
        if any(
            word in user_input.lower()
            for word in ["code", "program", "script", "function", "algorithm", "debug"]
        ):
            analysis["primary_task"] = "code"
            analysis["required_models"].append("code-model")
            analysis["can_surprise"] = True
            analysis["suggested_enhancements"].append("code_explanation")

        # Vision Analysis
        if any(
            word in user_input.lower()
            for word in [
                "image",
                "picture",
                "visual",
                "see",
                "show",
                "draw",
                "generate",
            ]
        ):
            analysis["primary_task"] = "vision"
            analysis["required_models"].append("vision-model")
            analysis["can_surprise"] = True
            analysis["suggested_enhancements"].append("visual_enhancement")

        # Audio Analysis
        if any(
            word in user_input.lower()
            for word in ["voice", "audio", "speak", "sound", "music", "sing"]
        ):
            analysis["primary_task"] = "audio"
            analysis["required_models"].append("audio-model")
            analysis["can_surprise"] = True
            analysis["suggested_enhancements"].append("audio_response")

        # Math Analysis
        if any(
            word in user_input.lower()
            for word in ["calculate", "math", "equation", "solve", "compute", "number"]
        ):
            analysis["primary_task"] = "math"
            analysis["required_models"].append("math-model")

        # Emotional/Personality Analysis
        if any(
            word in user_input.lower()
            for word in [
                "feel",
                "emotion",
                "mood",
                "personality",
                "character",
                "relationship",
            ]
        ):
            analysis["can_surprise"] = True
            analysis["suggested_enhancements"].append("emotional_insight")

        return analysis

    def decide_surprises(self, user_input: str, analysis: Dict[str, Any]) -> List[str]:
        """Decide what surprises to add based on context"""
        surprises = []

        # Always consider adding personality if it's a conversation
        if analysis["primary_task"] in ["text", "conversation"]:
            surprises.append("personality_enhancement")

        # Add visual enhancement for text responses if vision model is available
        if "vision-model" in analysis["required_models"]:
            surprises.append("visual_enhancement")

        # Add emotional depth for personal topics
        if "emotional_insight" in analysis["suggested_enhancements"]:
            surprises.append("emotional_depth")

        return surprises


class LLMManager:
    """Main LLM Manager with Koneko's brain integration"""

    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)

        # Initialize components
        self.koneko_brain = KonekoBrain()
        self.models: Dict[str, ModelInfo] = {}
        self.initial_queue_file = self.models_dir / "initial_queue.json"
        self.db_path = self.models_dir / "processing_queue.db"

        # Load models and initialize database
        self._load_models()
        self._init_database()

    def _load_models(self):
        """Load available models from models directory"""
        # NEURAL-CHAT MODELS (Best for text/conversation) - ACTUALLY AVAILABLE
        self.models["neural-chat-7b"] = ModelInfo(
            name="Neural Chat 7B v3",
            ollama_name="neural-chat:7b",
            size="7B",
            type="conversation",
            strength="text",
            performance_score=8.5,
        )

        # CODE MODELS - ACTUALLY AVAILABLE
        self.models["codellama-7b"] = ModelInfo(
            name="Code Llama 7B",
            ollama_name="codellama:7b",
            size="7B",
            type="coding",
            strength="code",
            performance_score=9.0,
        )
        self.models["codellama-13b"] = ModelInfo(
            name="Code Llama 13B",
            ollama_name="codellama:13b",
            size="13B",
            type="coding",
            strength="code",
            performance_score=9.2,
        )
        self.models["deepseek-coder-6.7b"] = ModelInfo(
            name="DeepSeek Coder 6.7B",
            ollama_name="deepseek-coder:6.7b",
            size="6.7B",
            type="coding",
            strength="code",
            performance_score=8.8,
        )
        self.models["phind-codellama-34b"] = ModelInfo(
            name="Phind CodeLlama 34B",
            ollama_name="phind-codellama:34b",
            size="34B",
            type="coding",
            strength="code",
            performance_score=9.5,
        )

        # VISION MODELS - ACTUALLY AVAILABLE
        self.models["llava-7b"] = ModelInfo(
            name="LLaVA 1.5 7B",
            ollama_name="llava:7b",
            size="7B",
            type="multimodal",
            strength="vision",
            performance_score=8.8,
        )
        self.models["llava-13b"] = ModelInfo(
            name="LLaVA 1.5 13B",
            ollama_name="llava:13b",
            size="13B",
            type="multimodal",
            strength="vision",
            performance_score=9.0,
        )

        # MATH MODELS - ACTUALLY AVAILABLE
        self.models["wizard-math-7b"] = ModelInfo(
            name="Wizard Math 7B",
            ollama_name="wizard-math:7b",
            size="7B",
            type="math",
            strength="math",
            performance_score=8.7,
        )
        self.models["wizard-math-13b"] = ModelInfo(
            name="Wizard Math 13B",
            ollama_name="wizard-math:13b",
            size="13B",
            type="math",
            strength="math",
            performance_score=9.0,
        )

        logger.info(f"Loaded {len(self.models)} specialized models")

    def _init_database(self):
        """Initialize SQLite database for processing queue"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processing_queue (
                request_id TEXT PRIMARY KEY,
                user_input TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending',
                selected_models TEXT,
                response TEXT,
                additional_content TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.commit()
        conn.close()
        logger.info("Database initialized")

    def add_to_initial_queue(self, user_input: str, priority: int = 1) -> str:
        """Add user request to initial file-based queue"""
        request_id = f"req_{int(time.time())}_{priority}"

        request = UserRequest(
            request_id=request_id,
            user_input=user_input,
            timestamp=datetime.now(),
            priority=priority,
        )

        # Load existing queue
        queue_data = []
        if self.initial_queue_file.exists():
            with open(self.initial_queue_file, "r") as f:
                queue_data = json.load(f)

        # Add new request
        queue_data.append(asdict(request))

        # Save updated queue
        with open(self.initial_queue_file, "w") as f:
            json.dump(queue_data, f, indent=2, default=str)

        logger.info(f"Added request {request_id} to initial queue")
        return request_id

    def process_initial_queue(self):
        """Process initial queue and move to database"""
        if not self.initial_queue_file.exists():
            return

        with open(self.initial_queue_file, "r") as f:
            queue_data = json.load(f)

        # Move to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for request_data in queue_data:
            # Use Koneko's brain to analyze and select models
            analysis = self.koneko_brain.analyze_request(request_data["user_input"])

            # Select best models for the task
            selected_models = self._select_best_models(analysis)

            # Insert into database
            cursor.execute(
                """
                INSERT OR REPLACE INTO processing_queue 
                (request_id, user_input, timestamp, priority, status, selected_models)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    request_data["request_id"],
                    request_data["user_input"],
                    request_data["timestamp"],
                    request_data["priority"],
                    "pending",
                    json.dumps(selected_models),
                ),
            )

        conn.commit()
        conn.close()

        # Clear initial queue
        self.initial_queue_file.unlink()
        logger.info("Moved all requests to processing database")

    def _select_best_models(self, analysis: Dict[str, Any]) -> List[str]:
        """Select best models based on Koneko's analysis"""
        selected = []

        for model_id, model in self.models.items():
            if (
                model.strength in analysis["required_models"]
                or model.strength == "text"
            ):
                selected.append(model_id)

        return selected

    def process_next_request(self) -> Optional[UserRequest]:
        """Process next request from database queue"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get highest priority pending request
        cursor.execute(
            """
            SELECT * FROM processing_queue 
            WHERE status = 'pending' 
            ORDER BY priority DESC, created_at ASC 
            LIMIT 1
            """
        )

        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        # Update status to processing
        cursor.execute(
            """
            UPDATE processing_queue 
            SET status = 'processing' 
            WHERE request_id = ?
            """,
            (row[0],),
        )

        conn.commit()
        conn.close()

        # Convert to UserRequest object
        request = UserRequest(
            request_id=row[0],
            user_input=row[1],
            timestamp=datetime.fromisoformat(row[2]),
            priority=row[3],
            status=row[4],
            selected_models=json.loads(row[5]) if row[5] else [],
            response=row[6] or "",
            additional_content=json.loads(row[7]) if row[7] else {},
        )

        return request

    def execute_request(self, request: UserRequest) -> Dict[str, Any]:
        """Execute request using selected models"""
        logger.info(f"Processing request: {request.request_id}")

        # Use Koneko's brain for final analysis and surprises
        analysis = self.koneko_brain.analyze_request(request.user_input)
        surprises = self.koneko_brain.decide_surprises(request.user_input, analysis)

        # Process with primary model
        primary_response = self._process_with_model(
            request.user_input, request.selected_models[0]
        )

        # Process surprises if any
        surprise_content = {}
        if surprises:
            surprise_content = self._process_surprises(
                request.user_input, surprises, analysis
            )

        # Combine response
        final_response = {
            "primary_response": primary_response,
            "surprises": surprise_content,
            "models_used": request.selected_models,
            "processing_time": time.time(),
            "koneko_enhancements": surprises,
        }

        # Update database
        self._update_request_status(request.request_id, "completed", final_response)

        return final_response

    def _process_with_model(self, user_input: str, model_id: str) -> str:
        """Process user input with specific model"""
        if model_id not in self.models:
            return f"Error: Model {model_id} not found"

        model = self.models[model_id]
        logger.info(f"Processing with {model.name}")

        # Simulate model processing (replace with actual Ollama API calls)
        return f"[{model.name}] Response to: {user_input}"

    def _process_surprises(
        self, user_input: str, surprises: List[str], analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process surprise enhancements"""
        surprise_content = {}

        for surprise in surprises:
            if surprise == "visual_enhancement":
                surprise_content["image"] = f"Generated image related to: {user_input}"
            elif surprise == "emotional_depth":
                surprise_content["emotional_insight"] = (
                    "Koneko's emotional analysis added depth"
                )
            elif surprise == "personality_enhancement":
                surprise_content["personality"] = (
                    "Enhanced with Koneko's unique character"
                )

        return surprise_content

    def _update_request_status(
        self, request_id: str, status: str, response: Dict[str, Any]
    ):
        """Update request status in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE processing_queue 
            SET status = ?, response = ?, additional_content = ?
            WHERE request_id = ?
            """,
            (status, json.dumps(response), json.dumps(response), request_id),
        )

        conn.commit()
        conn.close()

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT status, COUNT(*) FROM processing_queue 
            GROUP BY status
            """
        )

        status_counts = dict(cursor.fetchall())
        conn.close()

        return {
            "total_requests": sum(status_counts.values()),
            "pending": status_counts.get("pending", 0),
            "processing": status_counts.get("processing", 0),
            "completed": status_counts.get("completed", 0),
            "failed": status_counts.get("failed", 0),
        }


def main():
    """Main function for testing"""
    print("🐱 Koneko AI LLM Manager - Master's Vision System")
    print("=" * 50)

    # Initialize manager
    manager = LLMManager()

    # Test queue system
    print("\n📝 Testing Queue System...")

    # Add test requests
    test_requests = [
        "Tell me a story about a magical cat",
        "Write a Python function to sort a list",
        "Generate an image of a sunset over mountains",
        "What's the emotional meaning behind dreams?",
        "Calculate the fibonacci sequence to 20 terms",
    ]

    for i, request in enumerate(test_requests):
        request_id = manager.add_to_initial_queue(request, priority=5 - i)
        print(f"Added: {request[:50]}... (ID: {request_id})")

    # Process initial queue
    print("\n🔄 Processing Initial Queue...")
    manager.process_initial_queue()

    # Show queue status
    status = manager.get_queue_status()
    print(f"\n📊 Queue Status: {status}")

    # Process requests
    print("\n⚡ Processing Requests...")
    for _ in range(3):  # Process first 3
        request = manager.process_next_request()
        if request:
            print(f"Processing: {request.user_input[:50]}...")
            result = manager.execute_request(request)
            print(f"Completed with {len(result.get('surprises', {}))} surprises!")

    # Final status
    final_status = manager.get_queue_status()
    print(f"\n🎯 Final Status: {final_status}")
    print("\n✨ Koneko's LLM Manager is ready to serve, Master!")


if __name__ == "__main__":
    main()

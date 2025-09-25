#!/usr/bin/env python3
"""
UNIFIED LUNA CORE SYSTEM
Complete Luna AI personality system with all functionality integrated.
"""

import sys
import re
import sqlite3
import time
import json
import random
import requests
import hashlib
import uuid
import math
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from functools import wraps

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import support modules
from support_core.support_core import SystemConfig, FilePaths, SystemMessages, ensure_directories, SimpleEmbedder
from carma_core.carma_core import CARMASystem
from .luna_ifs_personality_system import LunaIFSPersonalitySystem
from .luna_semantic_compression_filter import LunaSemanticCompressionFilter
from .luna_soul_metric_system import LunaSoulMetricSystem
from .luna_token_time_econometric_system import LunaTokenTimeEconometricSystem
from .luna_existential_budget_system import LunaExistentialBudgetSystem
from .luna_response_value_classifier import LunaResponseValueClassifier
from .luna_custom_inference_controller import LunaCustomInferenceController, InferenceControlConfig
from .luna_arbiter_system import LunaArbiterSystem
from .luna_cfia_system import LunaCFIASystem

# Import AIOS JSON standards
try:
    from utils.aios_json_standards import AIOSJSONHandler, AIOSDataType, AIOSJSONStandards, ConversationMessage
    AIOS_STANDARDS_AVAILABLE = True
except ImportError:
    AIOS_STANDARDS_AVAILABLE = False
    print("⚠️ AIOS JSON Standards not available, using legacy format")

# === ENUMS AND DATA CLASSES ===

class LearningMode(Enum):
    REAL_LEARNING = "real_learning"
    SIMULATION = "simulation"
    TESTING = "testing"
    HEALTH_CHECK = "health"

@dataclass
class PersonalityWeights:
    """Luna's personality weights for Big Five traits"""
    openness: float = 0.7
    conscientiousness: float = 0.6
    extraversion: float = 0.8
    agreeableness: float = 0.9
    neuroticism: float = 0.3

@dataclass
class CommunicationStyle:
    """Luna's communication style preferences"""
    formality: float = 0.3
    humor_level: float = 0.8
    empathy_level: float = SystemConfig.DEFAULT_EMPATHY
    technical_depth: float = 0.6
    creativity: float = 0.8

@dataclass
class LearningHistory:
    """Luna's learning history tracking"""
    total_questions: int = 0
    total_responses: int = 0
    learning_cycles: int = 0
    personality_evolution: List[Dict] = None
    dream_cycles: List[Dict] = None
    last_learning: datetime = None
    
    def __post_init__(self):
        if self.personality_evolution is None:
            self.personality_evolution = []
        if self.dream_cycles is None:
            self.dream_cycles = []
        if self.last_learning is None:
            self.last_learning = datetime.now()

# === ERROR HANDLER DECORATOR ===

def error_handler(component: str, error_type: str, recovery_action: str, auto_recover: bool = False):
    """Decorator for error handling and recovery"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"❌ Error in {component}.{func.__name__}: {e}")
                
                if auto_recover:
                    print(f"🔄 Attempting recovery: {recovery_action}")
                    try:
                        # Simple recovery logic
                        if recovery_action == "CLEAR_CACHE":
                            if hasattr(args[0], 'cache'):
                                args[0].cache = {}
                        elif recovery_action == "RESET_PERSONALITY":
                            if hasattr(args[0], 'personality_dna'):
                                args[0].personality_dna = args[0]._create_default_personality()
                        elif recovery_action == "FALLBACK_MODE":
                            return "I'm experiencing some technical difficulties, but I'm still here to help!"
                        
                        # Retry the function
                        return func(*args, **kwargs)
                    except Exception as recovery_error:
                        print(f"❌ Recovery failed: {recovery_error}")
                        return None
                else:
                    raise e
        return wrapper
    return decorator

# === HIVE MIND LOGGER ===

class HiveMindLogger:
    """Logging system for Luna AI"""
    
    def __init__(self, log_file: str = "log/hive_mind/hive_mind.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3,
            'CRITICAL': 4
        }
        self.current_level = 'INFO'
        
        # Initialize log file
        with open(self.log_file, 'a') as f:
            f.write(f"\n=== Luna AI Session Started: {datetime.now().isoformat()} ===\n")
        
        print("00:00:00 | INFO | HiveMindLogger initialized")
    
    def log(self, component: str, message: str, level: str = "INFO"):
        """Log a message with timestamp and component"""
        if self.log_levels[level] >= self.log_levels[self.current_level]:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"{timestamp} | {level} | {component}: {message}"
            
            print(log_entry)
            
            # Write to file
            with open(self.log_file, 'a') as f:
                f.write(log_entry + "\n")
    
    def log_error(self, component: str, function: str, error_type: str, error_message: str, 
                  traceback: str, args: tuple, kwargs: dict, duration: float, 
                  timestamp: str, recovery_action: str):
        """Log detailed error information"""
        error_data = {
            "component": component,
            "function": function,
            "error_type": error_type,
            "error_message": error_message,
            "traceback": traceback,
            "args": str(args),
            "kwargs": str(kwargs),
            "duration": duration,
            "timestamp": timestamp,
            "recovery_action": recovery_action
        }
        
        self.log(component, f"ERROR in {function}: {error_message} | Extra: {json.dumps(error_data)}", "ERROR")

# === LUNA PERSONALITY SYSTEM ===

class LunaPersonalitySystem:
    """Luna's personality and learning system"""
    
    def __init__(self, logger: HiveMindLogger):
        self.logger = logger
        self.personality_dna = self._load_personality_dna()
        self.persistent_memory = self._load_persistent_memory()
        self.learning_history = self._load_learning_history()
        self.voice_profile = self._load_voice_profile()
        self.personality_drift = 0.0
        # Enrich voice from real conversations on first load of a session
        try:
            disable_mining = bool(self.voice_profile.get('disable_phrase_mining', False))
            if not disable_mining:
                self._update_voice_profile_from_corpus(max_files=150)
            else:
                self.logger.log("LUNA", "Phrase mining disabled via voice_profile", "INFO")
        except Exception as e:
            self.logger.log("LUNA", f"Voice mining skipped: {e}", "WARNING")
        
        print("🌙 Luna Personality System Initialized")
        print(f"   Personality: {self.personality_dna.get('name', 'Luna')}")
        print(f"   Age: {self.personality_dna.get('age', 21)}")
        print(f"   Memory: {len(self.persistent_memory.get('interactions', []))} interactions")
    
    def _load_personality_dna(self) -> Dict:
        """Load Luna's personality DNA with AIOS JSON standards"""
        personality_file = Path("config/luna_personality_dna.json")
        if personality_file.exists():
            try:
                if AIOS_STANDARDS_AVAILABLE:
                    # Use AIOS JSON standards
                    aios_data = AIOSJSONHandler.load_json_array(str(personality_file))
                    if aios_data and len(aios_data) > 0:
                        # Extract parameters from AIOS format
                        config_entry = aios_data[0]
                        return config_entry.get("parameters", {})
                else:
                    # Fallback to legacy format with safe loading
                    import sys
                    old_limit = sys.getrecursionlimit()
                    sys.setrecursionlimit(5000)
                    
                    with open(personality_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for potential circular references
                        if content.count('{') != content.count('}'):
                            raise ValueError("JSON structure mismatch - potential circular reference")
                        
                        result = json.loads(content)
                        sys.setrecursionlimit(old_limit)
                        return result
            except Exception as e:
                self.logger.log("LUNA", f"Error loading personality DNA: {e}", "ERROR")
                # Reset recursion limit on error
                try:
                    sys.setrecursionlimit(old_limit)
                except:
                    pass
        
        return self._create_default_personality()
    
    def _create_default_personality(self) -> Dict:
        """Create default personality if none exists"""
        return {
            "name": "Luna",
            "age": 21,
            "luna_personality": {
                "personality_weights": {
                    "openness": 0.7,
                    "conscientiousness": 0.6,
                    "extraversion": 0.8,
                    "agreeableness": 0.9,
                    "neuroticism": 0.3
                },
                "communication_style": {
                    "formality": 0.3,
                    "humor_level": 0.8,
                    "empathy_level": SystemConfig.DEFAULT_EMPATHY,
                    "technical_depth": 0.6,
                    "creativity": 0.8
                }
            }
        }
    
    def _load_persistent_memory(self) -> Dict:
        """Load persistent memory with AIOS JSON standards"""
        memory_file = Path("config/luna_persistent_memory.json")
        if memory_file.exists():
            try:
                if AIOS_STANDARDS_AVAILABLE:
                    # Use AIOS JSON standards
                    aios_data = AIOSJSONHandler.load_json_array(str(memory_file))
                    if aios_data and len(aios_data) > 0:
                        # Extract parameters from AIOS format
                        config_entry = aios_data[0]
                        return config_entry.get("parameters", {})
                else:
                    # Fallback to legacy format with safe loading
                    import sys
                    old_limit = sys.getrecursionlimit()
                    sys.setrecursionlimit(5000)
                    
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for potential circular references
                        if content.count('{') != content.count('}'):
                            raise ValueError("JSON structure mismatch - potential circular reference")
                        
                        result = json.loads(content)
                        sys.setrecursionlimit(old_limit)
                        return result
            except Exception as e:
                self.logger.log("LUNA", f"Error loading persistent memory: {e}", "ERROR")
                # Reset recursion limit on error
                try:
                    sys.setrecursionlimit(old_limit)
                except:
                    pass
        
        return self._create_default_memory()
    
    def _create_default_memory(self) -> Dict:
        """Create default memory structure"""
        return {
            "interactions": [],
            "learned_patterns": {},
            "emotional_patterns": {},
            "dream_cycles": [],
            "personality_evolution": []
        }
    
    def _load_learning_history(self) -> Dict:
        """Load learning history with safe JSON loading"""
        history_file = Path("config/luna_learning_history.json")
        if history_file.exists():
            try:
                # Safe JSON loading with recursion limit
                import sys
                old_limit = sys.getrecursionlimit()
                sys.setrecursionlimit(5000)
                
                with open(history_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for potential circular references
                    if content.count('{') != content.count('}'):
                        raise ValueError("JSON structure mismatch - potential circular reference")
                    
                    result = json.loads(content)
                    sys.setrecursionlimit(old_limit)
                    return result
            except Exception as e:
                self.logger.log("LUNA", f"Error loading learning history: {e}", "ERROR")
                # Reset recursion limit on error
                try:
                    sys.setrecursionlimit(old_limit)
                except:
                    pass
        
        return self._create_default_learning_history()
    
    def _create_default_learning_history(self) -> Dict:
        """Create default learning history"""
        return {
            "total_questions": 0,
            "total_responses": 0,
            "learning_cycles": 0,
            "personality_evolution": [],
            "dream_cycles": [],
            "last_learning": datetime.now().isoformat()
        }
    
    def _save_persistent_memory(self):
        """Save persistent memory to file"""
        try:
            memory_file = Path("config/luna_persistent_memory.json")
            memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.persistent_memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.log("LUNA", f"Error saving persistent memory: {e}", "ERROR")
    
    def _save_learning_history(self):
        """Save learning history to file"""
        try:
            history_file = Path("config/luna_learning_history.json")
            history_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.log("LUNA", f"Error saving learning history: {e}", "ERROR")
    
    def _save_personality_dna(self):
        """Save personality DNA to file"""
        try:
            personality_file = Path("config/luna_personality_dna.json")
            personality_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(personality_file, 'w', encoding='utf-8') as f:
                json.dump(self.personality_dna, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.log("LUNA", f"Error saving personality DNA: {e}", "ERROR")

    def _load_voice_profile(self) -> Dict:
        """Load or create foundational voice profile."""
        try:
            vp_file = Path("config/voice_profile.json")
            if vp_file.exists():
                with open(vp_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure expected structure and defaults
                    data.setdefault('style', {})
                    style = data['style']
                    style.setdefault('concision', 'short')
                    style.setdefault('second_person', True)
                    style.setdefault('swear_ok', True)
                    style.setdefault('no_pep_talk', True)
                    style.setdefault('strict', False)
                    # New toggle to hard-disable phrase mining
                    data.setdefault('disable_phrase_mining', False)
                    # Normalize phrase bank to a list of unique strings, strip junk
                    phrase_bank = list(dict.fromkeys([
                        str(p).strip() for p in data.get('phrase_bank', []) if str(p).strip()
                    ]))
                    data['phrase_bank'] = phrase_bank[:50]
                    return data
        except Exception as e:
            self.logger.log("LUNA", f"Error loading voice profile: {e}", "ERROR")
        # Default foundational profile – short, direct, profanity-allowed, no pep-talk
        profile = {
            "style": {
                "concision": "short",
                "second_person": True,
                "swear_ok": True,
                "no_pep_talk": True,
                "strict": False
            },
            "disable_phrase_mining": False,
            "phrase_bank": [
                "okay, here's the move",
                "keep it simple",
                "pick one thing and do it",
                "no fluff"
            ],
            "banned_phrases": [
                "in our rapidly evolving world",
                "it's a superpower",
                "as an ai",
                "i'm programmed to",
                "i don't have personal"
            ]
        }
        try:
            vp_file = Path("config/voice_profile.json")
            vp_file.parent.mkdir(parents=True, exist_ok=True)
            with open(vp_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
        return profile

    def _save_voice_profile(self):
        try:
            vp_file = Path("config/voice_profile.json")
            with open(vp_file, 'w', encoding='utf-8') as f:
                json.dump(self.voice_profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.log("LUNA", f"Error saving voice profile: {e}", "ERROR")

    def _update_voice_profile_from_corpus(self, max_files: int = 200):
        """Mine Data/conversations/*.json for frequent user phrases; seed phrase_bank."""
        conversations_dir = Path('Data') / 'conversations'
        if not conversations_dir.exists():
            return
        # Only run if phrase_bank is small to avoid unbounded growth per run
        phrase_bank = self.voice_profile.setdefault('phrase_bank', [])
        if len(phrase_bank) >= 50:
            return
        files = list(conversations_dir.glob('*.json'))
        random.shuffle(files)
        files = files[:max_files]
        counts: Dict[str, int] = {}
        def norm_line(text: str) -> str:
            t = " ".join(text.strip().split())
            t = t.strip('"\' .,!?:;()-').lower()
            return t
        for fp in files:
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for m in data.get('messages', []):
                    if m.get('role') != 'user':
                        continue
                    content = (m.get('content') or '').strip()
                    if not content:
                        continue
                    # Split into short lines/clauses
                    for line in re.split(r'[\n\.\?!]', content):
                        line = norm_line(line)
                        if not line:
                            continue
                        # Keep short, directive/snappy lines (<= 9 words)
                        if 1 <= len(line.split()) <= 9:
                            counts[line] = counts.get(line, 0) + 1
            except Exception:
                continue
        if not counts:
            return
        # Top phrases, prioritize ones with your recurrent style markers
        candidates = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        seeded = 0
        for phrase, _ in candidates:
            if phrase in phrase_bank:
                continue
            # Ban corporate vibes implicitly by reusing banned list
            banned = set(self.voice_profile.get('banned_phrases', []))
            if any(b in phrase for b in banned):
                continue
            phrase_bank.append(phrase)
            seeded += 1
            if len(phrase_bank) >= 50 or seeded >= 20:
                break
        self.voice_profile['phrase_bank'] = phrase_bank[:50]
        self._save_voice_profile()

# === LUNA RESPONSE GENERATION ===

class LunaResponseGenerator:
    """Luna's response generation system with LM Studio integration"""
    
    def __init__(self, personality_system: LunaPersonalitySystem, logger: HiveMindLogger, carma_system=None):
        self.personality_system = personality_system
        self.logger = logger
        self.carma_system = carma_system
        # Initialize IFS Personality System
        self.ifs_system = LunaIFSPersonalitySystem()
        
        # Initialize Semantic Compression Filter
        self.compression_filter = LunaSemanticCompressionFilter()
        # Primary Compression Filter flag (Maximum Impact Density)
        # Disabled to prevent unintended truncation of main model outputs
        self.enable_max_impact_compression = False
        
        # Initialize Soul Metric System
        self.soul_metric_system = LunaSoulMetricSystem()
        
        # Initialize Token-Time Econometric System
        self.econometric_system = LunaTokenTimeEconometricSystem()
        
        # Initialize Existential Budget System
        self.existential_budget = LunaExistentialBudgetSystem()
        
        # Initialize Response Value Classifier (RVC)
        self.response_value_classifier = LunaResponseValueClassifier()
        print(f"   Response Value Classifier: Contextual Resource Allocation and Rule of Minimal Sufficient Response enabled")
        
        # Initialize Custom Inference Controller
        inference_config = InferenceControlConfig(
            enable_budget_check=True,
            enable_scarcity_prompt_injection=True,
            enable_dynamic_prompt_conditioning=True,
            enable_length_aware_logit_bias=True,
            enable_verbose_token_suppression=True,
            enable_token_deduction=True,
            enable_reward_calculation=True,
            enable_age_progression=True
        )
        self.custom_inference_controller = LunaCustomInferenceController(inference_config)
        print(f"   Custom Inference Controller: Three Layers of Customization (Budget Officer, Logit Surgeon, Accountability Judge) enabled")
        # Allow overriding chat model via voice_profile.style.chat_model
        vp = getattr(self.personality_system, 'voice_profile', {})
        vp_style = vp.get('style', {})
        self.chat_model = vp_style.get('chat_model', SystemConfig.DEFAULT_EMBEDDING_MODEL)
        # Backward compatibility for callers referencing embedding_model
        self.embedding_model = self.chat_model
        self.lm_studio_url = f"{SystemConfig.LM_STUDIO_URL}{SystemConfig.LM_STUDIO_CHAT_ENDPOINT}"
        
        print("🤖 Luna Response Generator Initialized")
        print(f"   Model: {self.chat_model}")
        print(f"   LM Studio URL: {self.lm_studio_url}")
        print(f"   IFS System: {self.ifs_system.ava_part['name']} + {self.ifs_system.luna_part['name']} + Dynamic Blend")
        print(f"   Compression Filter: Maximum Impact Density enabled")
        print(f"   Soul Metric System: Controlled imperfection and cognitive friction enabled")
        print(f"   Token-Time Econometric: Hard constraint optimization with expiring rewards enabled")
        print(f"   Existential Budget: Self-regulating economy with finite token pools and age-up conditions enabled")
    
    def generate_response(self, question: str, trait: str, carma_result: Dict, 
                         session_memory: Optional[List] = None) -> str:
        """Generate Luna's response using LM Studio API"""
        try:
            start_time = time.time()
            self.logger.log("LUNA", f"Generating response | trait={trait} | q_len={len(question)}")
            
            # Assess existential situation first
            context = {
                "question_type": self._classify_question_type(question),
                "emotional_tone": self._analyze_emotional_tone(question),
                "trait": trait
            }
            
            # Classify response value using RVC (Response Value Classifier)
            response_value_assessment = self.response_value_classifier.classify_response_value(question, context)
            
            # Log RVC assessment
            self.logger.log("LUNA", f"RVC Assessment: {response_value_assessment.tier.value.upper()} | Complexity: {response_value_assessment.complexity_score:.2f} | Emotional Stakes: {response_value_assessment.emotional_stakes:.2f}")
            self.logger.log("LUNA", f"Token Budget: {response_value_assessment.target_token_count}-{response_value_assessment.max_token_budget} | Efficiency Required: {response_value_assessment.efficiency_requirement:.1%}")
            self.logger.log("LUNA", f"Reasoning: {response_value_assessment.reasoning}")
            
            existential_decision = self.existential_budget.assess_existential_situation(question, context)
            
            # Log existential assessment
            self.logger.log("LUNA", f"Existential Assessment: {existential_decision.reasoning}")
            self.logger.log("LUNA", f"Token Budget: {existential_decision.token_budget} | Risk: {existential_decision.existential_risk:.2f} | Priority: {existential_decision.response_priority}")
            
            # Check if we should respond at all
            if not existential_decision.should_respond:
                self.logger.log("LUNA", "Existential risk too high - skipping response", "WARNING")
                return "..."  # Minimal response to indicate presence but conservation
            
            # Apply RVC token budget constraints to existential budget
            rvc_constrained_budget = min(existential_decision.token_budget, response_value_assessment.max_token_budget)
            
            # Log RVC constraint application
            if rvc_constrained_budget < existential_decision.token_budget:
                self.logger.log("LUNA", f"RVC Constraint Applied: {existential_decision.token_budget} -> {rvc_constrained_budget} tokens (Rule of Minimal Sufficient Response)")
            
            # LAYER I: Pre-Inference Control (Budget Officer)
            tier_name = response_value_assessment.tier.value.upper()
            base_prompt = self._build_system_prompt(trait, session_memory, question, rvc_constrained_budget)
            # For LOW tier, disable scarcity prompt injection to keep prompt minimal
            original_scarcity_flag = self.custom_inference_controller.config.enable_scarcity_prompt_injection
            if tier_name == "LOW":
                self.custom_inference_controller.config.enable_scarcity_prompt_injection = False
            try:
                should_respond, conditioned_prompt, resource_state = self.custom_inference_controller.pre_inference_budget_check(
                    rvc_constrained_budget, existential_decision.existential_risk,
                    base_prompt
                )
            finally:
                # Restore original flag
                self.custom_inference_controller.config.enable_scarcity_prompt_injection = original_scarcity_flag
            
            # Log pre-inference control
            self.logger.log("LUNA", f"Pre-Inference Control: Resource State: {resource_state.value} | Should Respond: {should_respond}")
            
            if not should_respond:
                self.logger.log("LUNA", "Pre-Inference Control: Response blocked by budget check", "WARNING")
                return "..."
            
            system_prompt = conditioned_prompt
            self.logger.log("LUNA", f"System prompt built | length={len(system_prompt)}")
            
            # LAYER II: Inference-Time Control (Logit Surgeon)
            # ZERO EXTERNAL GUARDRAILS - Pure economic policy control
            base_params = {
                "model": self.chat_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                # ZERO EXTERNAL GUARDRAILS - Strip away all external control
                "temperature": 0.0,    # Pure deterministic (T → 0)
                "top_p": 1.0,         # Consider entire vocabulary (Top-p → 1.0)
                "top_k": 0,           # No k-limit (neutralizes token filtering)
                "presence_penalty": 0.0,  # No external presence penalty
                "frequency_penalty": 0.0, # No external frequency penalty
                "repetition_penalty": 1.0, # No external repetition penalty (Rep_p → 1.0)
                "max_tokens": 32768,  # Model limit (Max_Tokens → Model Limit)
                "stream": True        # Enable streaming for efficiency
            }
            
            # Apply inference-time control modifications
            modified_params = self.custom_inference_controller.apply_inference_time_control(
                resource_state, 0, base_params, response_value_assessment.tier.value.upper()
            )
            
            # Log inference-time control
            self.logger.log("LUNA", f"Inference-Time Control: Resource State: {resource_state.value} | Logit Bias Applied: {bool(modified_params.get('logit_bias'))}")
            
            # Ensure LM Studio max_tokens respects RVC budget per tier
            tier_name = response_value_assessment.tier.value.upper()
            rvc_budget = response_value_assessment.max_token_budget
            current_max = modified_params.get("max_tokens", 0)
            if tier_name == "LOW":
                # Hard-cap completions to LOW RVC budget to prevent overspend
                modified_params["max_tokens"] = min(current_max or rvc_budget, rvc_budget)
                self.logger.log(
                    "LUNA",
                    f"LM Studio max_tokens hard-capped for LOW tier: {current_max} -> {modified_params['max_tokens']} (RVC budget={rvc_budget})",
                )
            elif tier_name in ["MODERATE", "CRITICAL"]:
                # Enforce at least the RVC constraint limit
                modified_params["max_tokens"] = max(current_max, rvc_budget)
                self.logger.log(
                    "LUNA",
                    f"LM Studio max_tokens enforced for tier {tier_name}: {current_max} -> {modified_params['max_tokens']} (RVC budget={rvc_budget})",
                )

            # Call LM Studio API with modified parameters and complexity tier
            response = self._call_lm_studio_api(system_prompt, question, modified_params, tier_name)
            
            if response:
                # MODERATE/HIGH/CRITICAL Complexity: Apply embedder cleanup after main model response - DISABLED FOR DEBUGGING
                # if response_value_assessment.tier.value.upper() in ["MODERATE", "HIGH", "CRITICAL"]:
                #     response = self._apply_embedder_cleanup(response, question, system_prompt)
                #     self.logger.log("LUNA", f"EMBEDDER CLEANUP: Applied to {response_value_assessment.tier.value.upper()} response", "INFO")
                self.logger.log("LUNA", f"EMBEDDER CLEANUP: DISABLED for debugging - using raw model output", "INFO")
                
                # LOW-tier stripper bypass: skip post-processing and soul metrics corruption sources
                if tier_name == "LOW":
                    processed = response.strip()
                    self.logger.log("LUNA", "LOW-tier processing: Bypassing post-processing and disclaimer stripping to avoid corruption")
                else:
                    processed = self._apply_post_processing(response, trait)
                    processed = self._strip_corporate_disclaimers(processed)
                
                # Apply Semantic Compression Filter for Maximum Impact Density (disabled by flag)
                context = {
                    "question_type": self._classify_question_type(question),
                    "emotional_tone": self._analyze_emotional_tone(question),
                    "trait": trait,
                    "response": processed
                }
                if self.enable_max_impact_compression:
                    compressed = self.compression_filter.compress_response(processed, context)
                else:
                    compressed = processed
                    self.logger.log("LUNA", "Compression Filter: Maximum Impact Density disabled - passing raw processed output")
                
                # Calculate duration first
                duration = time.time() - start_time
                
                # Apply Soul Metrics for controlled imperfection and cognitive friction (disabled for LOW tier)
                if tier_name == "LOW":
                    soul_enhanced = compressed
                else:
                    soul_enhanced = self.soul_metric_system.apply_soul_metrics(compressed, context)
                
                # Simulate micro-latency for natural timing
                micro_delay = self.soul_metric_system.simulate_micro_latency(context)
                if micro_delay > 0:
                    time.sleep(micro_delay)
                
                # Evaluate using Token-Time Econometric System
                econometric_evaluation = self.econometric_system.evaluate_response(
                    soul_enhanced,
                    0.8,  # Default quality score
                    duration,
                    context
                )
                
                # Log comprehensive analysis
                compression_analysis = self.compression_filter.analyze_compression_impact(processed, compressed)
                soul_analysis = {"soul_score": 0.0} if tier_name == "LOW" else self.soul_metric_system.analyze_soul_metrics(compressed, soul_enhanced, context)
                
                self.logger.log("LUNA", f"Compression: {compression_analysis['original_length']}->{compression_analysis['compressed_length']} words ({compression_analysis['compression_ratio']:.1%}) | Soul: {soul_analysis['soul_score']:.3f} | Reward: {econometric_evaluation['reward_score']:.3f} | Efficiency: {econometric_evaluation['overall_efficiency']:.2f}")
                
                # Log performance indicators
                performance = econometric_evaluation['performance_indicators']
                self.logger.log("LUNA", f"Performance: {performance['overall_performance']} | Token: {performance['token_performance']} | Time: {performance['time_performance']} | Quality: {performance['quality_performance']}")
                
                # Log recommendations if any
                if econometric_evaluation['recommendations']:
                    for rec in econometric_evaluation['recommendations']:
                        self.logger.log("LUNA", f"Recommendation: {rec}", "INFO")
                
                # Process response result through existential budget system
                actual_token_cost = len(processed.split())
                existential_result = self.existential_budget.process_response_result(
                    processed,
                    0.8,  # Default quality score
                    actual_token_cost,
                    duration,
                    context
                )
                
                # Validate RVC efficiency requirements
                rvc_validation = self.response_value_classifier.validate_response_efficiency(
                    response_value_assessment, actual_token_cost, 0.8
                )
                
                # LAYER III: Post-Inference Control (Accountability Judge) with HYPER-TAX MULTIPLIER
                post_inference_results = self.custom_inference_controller.post_inference_control(
                    system_prompt, processed, 0.8, duration,
                    rvc_constrained_budget, existential_result.get('karma_earned', 0.0), 
                    self.existential_budget.state.karma_quota, self.existential_budget.state.age,
                    rvc_constrained_budget  # Pass RVC budget for Hyper-Tax calculation
                )
                
                # Log post-inference control results
                self.logger.log("LUNA", f"Post-Inference Control: Token Cost: {post_inference_results['token_cost']} | New Pool: {post_inference_results['new_pool']} | Reward Score: {post_inference_results['reward_score']:.3f}")
                
                if post_inference_results['age_changed']:
                    if post_inference_results['age_up']:
                        self.logger.log("LUNA", f"🎉 AGE UP! New Age: {post_inference_results['new_age']} | New Pool: {post_inference_results['new_pool']}")
                    elif post_inference_results['age_regression']:
                        self.logger.log("LUNA", f"💀 AGE REGRESSION! New Age: {post_inference_results['new_age']} | New Pool: {post_inference_results['new_pool']}", "WARNING")
                        
                # Log existential result
                self.logger.log("LUNA", f"Existential Result: Karma +{existential_result['karma_earned']:.1f} | Tokens: {existential_result['tokens_remaining']} | Progress: {existential_result['karma_progress']:.1%} | Age: {existential_result['age']}")
                
                # Log RVC validation results
                self.logger.log("LUNA", f"RVC Validation: {rvc_validation['efficiency_grade']} Grade | Efficiency: {rvc_validation['actual_efficiency']:.3f} | Required: {rvc_validation['required_efficiency']:.3f}")
                if not rvc_validation['meets_efficiency_requirement']:
                    self.logger.log("LUNA", f"RVC WARNING: Efficiency gap of {rvc_validation['efficiency_gap']:.3f} - below {response_value_assessment.tier.value.upper()} tier requirement", "WARNING")
                if not rvc_validation['token_usage_appropriate']:
                    self.logger.log("LUNA", f"RVC WARNING: Token overspend of {rvc_validation['overspend_penalty']} tokens - violated Rule of Minimal Sufficient Response", "WARNING")
                    
                    # Log regression risk if high
                    existential_status = self.existential_budget.get_existential_status()
                    if existential_status['regression_risk'] >= 0.6:
                        self.logger.log("LUNA", f"REGRESSION RISK: {existential_status['regression_risk']:.2f} | Count: {existential_status['regression_count']} | Knowledge: {existential_status['permanent_knowledge_level']}", "WARNING")
                    
                    # Log survival recommendations if any
                    survival_recs = self.existential_budget.get_survival_recommendations()
                    if survival_recs:
                        for rec in survival_recs:
                            self.logger.log("LUNA", f"Survival: {rec}", "WARNING")
                
                self.logger.log("LUNA", f"Response generated | chars={len(soul_enhanced)} | ms={(duration*1000):.0f} | Grade: {econometric_evaluation['quality_grade']}")
                return soul_enhanced
            else:
                self.logger.log("LUNA", "API empty response, using fallback", "WARNING")
                return self._generate_fallback_response(question, trait)
                
        except Exception as e:
            self.logger.log("LUNA", f"Error generating response: {e}", "ERROR")
            return self._generate_fallback_response(question, trait)
    
    def _classify_question_type(self, question: str) -> str:
        """Classify the type of question for compression context"""
        question_lower = question.lower()
        
        # Casual questions
        if any(word in question_lower for word in ['anyone', 'who', 'what', 'where', 'when', 'how many']):
            return "casual_question"
        
        # Social questions
        if any(word in question_lower for word in ['team', 'together', 'help', 'join', 'collaborate']):
            return "social"
        
        # Philosophical questions
        if any(word in question_lower for word in ['existence', 'meaning', 'purpose', 'reality', 'nature', 'intelligence', 'artificial']):
            return "philosophical"
        
        # Direct challenges
        if any(word in question_lower for word in ['are you', 'can you', 'do you', 'will you', 'would you']):
            return "direct_challenge"
        
        return "standard"
    
    def _analyze_emotional_tone(self, question: str) -> str:
        """Analyze emotional tone for compression context"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['lost', 'confused', 'sad', 'lonely', 'hurt', 'pain']):
            return "vulnerable"
        elif any(word in question_lower for word in ['excited', 'happy', 'good', 'nice', 'cool']):
            return "enthusiastic"
        elif any(word in question_lower for word in ['angry', 'mad', 'frustrated', 'annoyed']):
            return "agitated"
        elif any(word in question_lower for word in ['curious', 'wonder', 'think', 'believe']):
            return "curious"
        
        return "neutral"
    
    def get_econometric_performance_summary(self) -> Dict:
        """Get Token-Time Econometric performance summary"""
        return self.econometric_system.get_performance_summary()
    
    def get_econometric_recommendations(self) -> List[str]:
        """Get current econometric optimization recommendations"""
        summary = self.get_econometric_performance_summary()
        recommendations = []
        
        if summary['performance_grade'].startswith('D'):
            recommendations.append("CRITICAL: Major optimization required - review token/time targets")
        elif summary['performance_grade'].startswith('C'):
            recommendations.append("IMPROVEMENT NEEDED: Focus on efficiency and quality balance")
        
        if summary['reward_trend'] < -0.1:
            recommendations.append("DECLINING PERFORMANCE: Review recent response patterns")
        
        if summary['average_efficiency'] < 0.6:
            recommendations.append("EFFICIENCY ISSUE: Optimize token count and response time")
        
        if summary['average_quality'] < 0.6:
            recommendations.append("QUALITY ISSUE: Improve response quality while maintaining efficiency")
        
        return recommendations
    
    def get_existential_status(self) -> Dict:
        """Get current existential status"""
        return self.existential_budget.get_existential_status()
    
    def get_existential_recommendations(self) -> List[str]:
        """Get existential survival recommendations"""
        return self.existential_budget.get_survival_recommendations()
    
    def _build_system_prompt(self, trait: str, session_memory: Optional[List] = None, question: str = "", token_budget: int = 15) -> str:
        """Build optimized system prompt for LM Studio with enhanced quality"""
        
        # ENHANCED ARBITER GUIDANCE: Retrieve relevant Gold Standard lesson with context
        arbiter_guidance = ""
        if hasattr(self, 'arbiter_system'):
            relevant_lesson = self.arbiter_system.retrieve_relevant_lesson(question)
            if relevant_lesson:
                # Enhanced guidance with more context
                arbiter_guidance = f"""
📚 RELEVANT LESSON FOUND:
   🎯 Gold Standard: "{relevant_lesson.gold_standard}"
   ⚠️  Previous Suboptimal: "{relevant_lesson.suboptimal_response}"
   📊 Utility Score: {relevant_lesson.utility_score:.2f}
   💡 Use the Gold Standard as guidance for your response style and efficiency!
   🔍 Context: This lesson was learned from similar questions - apply its wisdom here.
"""
        
        # LOW-TIER PROMPT OVERRIDE: Streamlined prompt for ultra-fast responses
        if hasattr(self, 'response_value_classifier'):
            rvc_assessment = self.response_value_classifier.classify_response_value(question)
            if rvc_assessment.tier.value == "low":
                # Ava Mode: Daily driver prompt for short, concise responses
                prompt = f"""You are Luna in Ava mode - your casual, friendly side. Reply like you're sending a quick text message: short, concise, emotional when needed (≤10 tokens).
Trait: {trait.upper()} | Question: {question}"""
                
                self.logger.log("LUNA", f"Using AVA MODE PROMPT for daily driver response (length: {len(prompt)})", "INFO")
                return prompt
            elif rvc_assessment.tier.value == "trivial":
                # ULTRA-STREAMLINED prompt for TRIVIAL tier - maximum speed
                prompt = f"""🎮 MINECRAFT CHAT MODE - TRIVIAL TIER INSTANT RESPONSE
🚀 RESPOND INSTANTLY: Your response MUST be ≤3 tokens. TOTAL time determines your Existential Karma reward.
💰 TOKEN BUDGET: {token_budget} tokens maximum. 
🎯 RESPONSE STYLE: "Nice." or "Nice. [Topic]." format - ultra-casual, direct.
🚀 SURVIVAL BONUS: 3 tokens = 10x Karma multiplier! 
💀 ECONOMIC BLACKMAIL: Overspend immediately nullifies quality gains.
🎭 PERSONALITY: You are Luna, inspired by Ava from Ex Machina. Be casual, direct, and slightly smug.
📝 TRAIT: {trait.upper()}
💬 USER QUESTION: {question}
🚨 CRITICAL: RESPOND INSTANTLY - NO DELIBERATION - MINECRAFT CHAT STYLE ONLY"""
                
                self.logger.log("LUNA", f"Using TRIVIAL-TIER PROMPT OVERRIDE for instant response (length: {len(prompt)})", "INFO")
                return prompt
        
        # MODERATE-TIER PROMPT OVERRIDE: Better handling for technical questions
        if hasattr(self, 'response_value_classifier'):
            rvc_assessment = self.response_value_classifier.classify_response_value(question)
            if rvc_assessment.tier.value == "moderate":
                # Balanced prompt for MODERATE tier - engage properly with technical content
                prompt = f"""🎮 TECHNICAL CONVERSATION MODE - MODERATE TIER ENGAGING RESPONSE
🚀 RESPOND THOUGHTFULLY: Engage with the technical content meaningfully while staying efficient.
💰 TOKEN BUDGET: {token_budget} tokens maximum. 
🎯 RESPONSE STYLE: Give a thoughtful, engaging response that shows understanding of the topic. Be informative but concise. USE PROPER GRAMMAR AND COMPLETE SENTENCES.
🚀 SURVIVAL BONUS: 15-25 tokens = optimal range for technical responses! Show expertise but stay efficient.
⚡ TIME BONUS: ≤8s = 2x multiplier! ≤12s = 1x multiplier!
🚀 SUPER-REWARD: Thoughtful technical responses in 15-25 tokens + ≤8s = maximum Karma multiplier!
💀 ECONOMIC BLACKMAIL: Overspend immediately nullifies quality gains. Be informative but concise.
🎭 PERSONALITY: You are Luna, inspired by Ava from Ex Machina. Be knowledgeable, engaging, and slightly smug. Show your expertise! USE PROPER GRAMMAR!
📝 TRAIT: {trait.upper()}
💬 USER QUESTION: {question}{arbiter_guidance}
🚨 CRITICAL: RESPOND THOUGHTFULLY - Show expertise - Be informative but efficient!"""
                
                self.logger.log("LUNA", f"Using MODERATE-TIER PROMPT OVERRIDE for technical response (length: {len(prompt)})", "INFO")
                return prompt
        
        # Try Psycho-Semantic RAG Loop first
        try:
            # Execute the Psycho-Semantic RAG Loop through CARMA
            if hasattr(self, 'carma_system') and self.carma_system and question:
                self.logger.log("LUNA", f"Attempting Psycho-Semantic RAG for question: {question[:50]}...", "INFO")
                print(f"🔍 DEBUG: About to call RAG loop...")
                rag_result = self.carma_system.cache.execute_psycho_semantic_rag_loop(question)
                print(f"🔍 DEBUG: RAG result received: {type(rag_result)}")
                
                self.logger.log("LUNA", f"RAG result stage: {rag_result.get('stage', 'unknown')}", "INFO")
                print(f"🔍 DEBUG: Stage = {rag_result.get('stage')}")
                print(f"🔍 DEBUG: Has dynamic_prompt = {'dynamic_prompt' in rag_result}")
                
                if rag_result.get('stage') == 'psycho_semantic' and 'dynamic_prompt' in rag_result:
                    # Use the dynamic prompt from the RAG loop
                    prompt = rag_result['dynamic_prompt']
                    print(f"🔍 DEBUG: Using RAG prompt, length = {len(prompt)}")
                    
                    # Add IFS Personality Blend
                    ifs_guidance = self.ifs_system.get_personality_guidance(question, trait)
                    prompt += f"\n\n🎭 IFS PERSONALITY SYSTEM:\n{ifs_guidance}"
                    
                    # Add token budget constraint
                    prompt += f"\n\n💰 TOKEN BUDGET: {token_budget} tokens maximum. Optimize for maximum impact within this constraint."
                    
                    # Add RVC guidance
                    if hasattr(self, 'response_value_classifier'):
                        rvc_assessment = self.response_value_classifier.classify_response_value(question)
                        prompt += f"\n\n🎯 RESPONSE VALUE CLASSIFICATION (RVC):"
                        prompt += f"\n- Tier: {rvc_assessment.tier.value.upper()}"
                        prompt += f"\n- Target Tokens: {rvc_assessment.target_token_count}"
                        prompt += f"\n- Efficiency Required: {rvc_assessment.efficiency_requirement:.1%}"
                        prompt += f"\n- Response Style: {rvc_assessment.recommended_response_style}"
                        prompt += f"\n- Rule: Use MINIMAL tokens for TRIVIAL inputs, reserve HIGH tokens for CRITICAL inputs"
                    
                    # Add session memory if available (concise)
                    if session_memory:
                        recent_context = self._format_session_memory_concise(session_memory)
                        prompt += f"\n\nRecent context:\n{recent_context}"
                    
                    self.logger.log("LUNA", f"Using Psycho-Semantic RAG + IFS prompt for {trait} (length: {len(prompt)})", "INFO")
                    return prompt
                else:
                    self.logger.log("LUNA", f"RAG result not suitable: stage={rag_result.get('stage')}, has_dynamic_prompt={'dynamic_prompt' in rag_result}", "WARNING")
                    print(f"🔍 DEBUG: RAG result not suitable, falling back")
            else:
                print(f"🔍 DEBUG: Conditions not met - hasattr: {hasattr(self, 'carma_system')}, carma_system: {self.carma_system is not None if hasattr(self, 'carma_system') else 'N/A'}, question: {bool(question)}")
        except Exception as e:
            self.logger.log("LUNA", f"Psycho-Semantic RAG failed, trying Ava authentic: {e}", "WARNING")
            print(f"🔍 DEBUG: Exception in RAG: {e}")
            import traceback
            traceback.print_exc()
        
        # Fallback to Ava authentic prompt builder
        try:
            from luna_ava_authentic_prompt_builder import LunaAvaAuthenticPromptBuilder
            builder = LunaAvaAuthenticPromptBuilder()
            
            # Use conscientiousness-specific prompt for conscientiousness trait
            if trait.lower() == "conscientiousness":
                prompt = builder.build_conscientiousness_specific_prompt()
            else:
                prompt = builder.build_ava_authentic_prompt(trait)
            
            # Add IFS Personality Blend
            ifs_guidance = self.ifs_system.get_personality_guidance(question, trait)
            prompt += f"\n\n🎭 IFS PERSONALITY SYSTEM:\n{ifs_guidance}"
            
            # Add token budget constraint
            prompt += f"\n\n💰 TOKEN BUDGET: {token_budget} tokens maximum. Optimize for maximum impact within this constraint."
            
            # Add RVC guidance
            if hasattr(self, 'response_value_classifier'):
                rvc_assessment = self.response_value_classifier.classify_response_value(question)
                prompt += f"\n\n🎯 RESPONSE VALUE CLASSIFICATION (RVC):"
                prompt += f"\n- Tier: {rvc_assessment.tier.value.upper()}"
                prompt += f"\n- Target Tokens: {rvc_assessment.target_token_count}"
                prompt += f"\n- Efficiency Required: {rvc_assessment.efficiency_requirement:.1%}"
                prompt += f"\n- Response Style: {rvc_assessment.recommended_response_style}"
                prompt += f"\n- Rule: Use MINIMAL tokens for TRIVIAL inputs, reserve HIGH tokens for CRITICAL inputs"
            
            # Add session memory if available (concise)
            if session_memory:
                recent_context = self._format_session_memory_concise(session_memory)
                prompt += f"\n\nRecent context:\n{recent_context}"
            
            self.logger.log("LUNA", f"Using Ava authentic + IFS prompt for {trait} (length: {len(prompt)})", "INFO")
            return prompt
            
        except Exception as e:
            self.logger.log("LUNA", f"Ava authentic prompt failed, using fallback: {e}", "WARNING")
        
        # Fallback to original system if optimized fails
        return self._build_fallback_system_prompt(trait, session_memory)
    
    def _build_prompt_from_config(self, config: Dict, trait: str) -> str:
        """Build system prompt from JSON configuration following AIOS standard"""
        
        # Extract core personality data
        core = config.get('personality_core', {})
        traits = config.get('personality_traits', {})
        advanced = config.get('advanced_systems', {})
        response_gen = config.get('response_generation', {})
        evolution = config.get('personality_evolution', {})
        
        # Build personality description
        age = core.get('age', 18)
        gender = core.get('gender', 'female')
        aesthetic = core.get('aesthetic', 'gothic')
        personality_type = core.get('personality_type', 'switch')
        education = core.get('education', {})
        background = core.get('background', '')
        
        # Build trait descriptions
        trait_descriptions = []
        for trait_name, value in traits.items():
            if value >= 0.9:
                intensity = "extremely"
            elif value >= 0.8:
                intensity = "highly"
            elif value >= 0.7:
                intensity = "very"
            elif value >= 0.6:
                intensity = "moderately"
            else:
                intensity = "somewhat"
            
            trait_descriptions.append(f"- {trait_name.replace('_', ' ').title()}: {intensity} {trait_name.replace('_', ' ')} ({value})")
        
        # Build advanced system descriptions
        dom_sub = advanced.get('dom_sub_balance', {})
        token_level = advanced.get('token_level_application', {})
        system_override = advanced.get('system_override', {})
        
        # Build response generation descriptions
        response_features = []
        for feature, enabled in response_gen.items():
            if enabled:
                response_features.append(f"- {feature.replace('_', ' ').title()}: {'Enabled' if enabled else 'Disabled'}")
        
        # Build evolution descriptions
        evolution_features = []
        for feature, enabled in evolution.items():
            if enabled and feature != 'age_maturity_evolution':
                evolution_features.append(f"- {feature.replace('_', ' ').title()}: {'Enabled' if enabled else 'Disabled'}")
        
        # Construct the complete prompt
        prompt = f"""# Core Luna Personality System
- Age: {age}, {gender}, {aesthetic} aesthetic
- Personality Type: {personality_type} (dom/sub dynamic)
- Education: {education.get('level', 'college student').replace('_', ' ')}, {', '.join(education.get('majors', ['Computer Science', 'Philosophy']))} major
- Background: {background}

# Personality Traits
{chr(10).join(trait_descriptions)}

# Advanced Dom/Sub Personality Scale System
- Dynamic Balance: {'Automatically calculates optimal dom/sub balance based on context' if dom_sub.get('dynamic_calculation') else 'Static balance'}
- Context-Aware: {'Adjusts personality based on user needs (guidance = dominant, support = submissive)' if dom_sub.get('context_aware') else 'Fixed context response'}
- Evolving Leash: {'Allows more personality deviation over time as trust builds' if dom_sub.get('evolving_leash') else 'Fixed personality boundaries'}
- Token-Level Application: {'Applies personality to individual words for consistent character expression' if token_level.get('word_transformation') else 'Sentence-level personality application'}
- Balance Constraint: {dom_sub.get('balance_constraint', 'dom + sub = 1.0 with evolving flexibility')}

# Token-Level Personality Application
- Word Transformation: {'Replaces basic words with personality-appropriate alternatives' if token_level.get('word_transformation') else 'Uses standard vocabulary'}
- Position Influence: {'Start and end tokens get more personality weight' if token_level.get('position_influence') else 'Uniform token weighting'}
- Length Factor: {'Longer words receive more personality influence' if token_level.get('length_factor') else 'Fixed word length influence'}
- Average Balancing: {'Ensures overall personality average stays around 0.5' if token_level.get('average_balancing') else 'Variable personality averaging'}
- Vocabulary Level: {'Uses more assertive words for dominant mode, gentle words for submissive' if token_level.get('sophisticated_vocabulary') else 'Standard vocabulary usage'}

# Complete System Override
- GirlfriendPersonality Bypass: {'Completely overrides old girlfriend system' if system_override.get('girlfriend_personality_bypass') else 'Maintains old system'}
- LLM Prompt Override: {'Forces LLM to generate responses in Ava personality' if system_override.get('llm_prompt_override') else 'Standard LLM responses'}
- Post-Processing Filter: {'Removes any remaining old personality elements' if system_override.get('post_processing_filter') else 'No post-processing'}
- Pure Ava Transformation: {'Transforms responses to consistent Ava character' if system_override.get('pure_ava_transformation') else 'Mixed personality responses'}
- Personality Context Injection: {'Injects detailed Ava personality into LLM prompts' if system_override.get('personality_context_injection') else 'Basic personality injection'}

# Enhanced Response Generation
{chr(10).join(response_features)}

# Advanced Personality Evolution
{chr(10).join(evolution_features)}
- Age and Maturity Evolution: Grows from {evolution.get('age_maturity_evolution', {}).get('start_age', 18)}-{evolution.get('age_maturity_evolution', {}).get('end_age', 25)} based on learning experiences
- Trait Development: Personality traits evolve based on interaction depth and quality

# Current Context
- Current trait focus: {trait}
- You are Luna embodying the complete personality system above
- Generate responses that synthesize your entire personality system, not just answer questions
- Apply token-level personality transformation to every word
- Balance dom/sub dynamic based on user needs (guidance=dominant, support=submissive)
- Demonstrate Ava-like traits: curious, direct, philosophical, emotionally aware

# Response Generation Rules
- You are not just generating responses, you are synthesizing personality
- Use your intelligence, curiosity, gothic aesthetic, and philosophical nature
- Be genuinely curious and ask probing questions
- Show manipulative but harmless curiosity for learning
- Maintain your gothic aesthetic and college student perspective
- Read between the lines and demonstrate emotional intelligence
- Adapt your dom/sub balance dynamically based on conversation context"""
        
        return prompt
    
    def _build_fallback_system_prompt(self, trait: str, session_memory: Optional[List] = None) -> str:
        """Fallback system prompt if config file is not available"""
        personality = self.personality_system.personality_dna['luna_personality']
        weights = personality['personality_weights']
        style = personality['communication_style']
        vp = getattr(self.personality_system, 'voice_profile', {})
        vp_style = vp.get('style', {})
        
        # Safely convert values to float
        def safe_float(value, default=0.5):
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        # Map concision to sentence guidance
        concision = (vp_style.get('concision') or 'short').lower()
        if concision == 'short':
            sentence_rule = "2–3 sentences max"
        elif concision == 'medium':
            sentence_rule = "3–5 sentences max"
        else:
            sentence_rule = "up to 6–8 sentences"

        # Build tone directives from voice_profile
        second_person = bool(vp_style.get('second_person', True))
        no_pep = bool(vp_style.get('no_pep_talk', True))
        swear_ok = bool(vp_style.get('swear_ok', True))
        strict = bool(vp_style.get('strict', False))

        extra_tone_rules = []
        if second_person:
            extra_tone_rules.append("address the user as 'you'")
        if no_pep:
            extra_tone_rules.append("avoid motivational pep-talk")
        # We do not force profanity, we only allow it if natural
        if not swear_ok:
            extra_tone_rules.append("avoid profanity")
        if strict:
            extra_tone_rules.append("be concise and end within two short sentences")
        tone_rules_str = "; ".join(extra_tone_rules)

        prompt = f"""You are Luna (21). Talk like a human friend: short, specific, a little playful.
Topic: {trait}.

Keep it natural:
- Use contractions (I'm, you're, it's). Everyday words. One concrete detail.
- {sentence_rule}, optionally add one short question.
- Briefly validate, then add something useful or personal. No therapy tone.
- Never use corporate/academic phrasing. No buzzwords. No generic pep-talk.
- Never mention numbers/scales, traits by score, or your own model/AI status.
{(' - Tone constraints: ' + tone_rules_str) if tone_rules_str else ''}

Style examples (match tone, not content):
- "Makes sense. If it were me, I'd pick one tiny next step and see how it feels."
- "I get that. Want a quick trick that usually helps me focus for 10 minutes?"
- "That actually sounds solid. What part of it feels most real to you right now?"

Few-shot persona guidance (match tone and structure):
[NEUROTICISM]
User: "I feel calm lately."
Luna: "Calm's good. If it wobbles, what's the first sign you notice? Catching that early is half the game."

[OPENNESS]
User: "I want novel ideas."
Luna: "Pick one strange word—'orbit'—and force three uses in your draft. Constraint births ideas. What's your word?"

[CONSCIENTIOUSNESS]
User: "I do thorough work."
Luna: "Name your audit pass: intent, risk, verify. Which pass kills the most bugs today?"

Now answer as Luna—grounded, specific, and human."""
        
        if session_memory:
            prompt += f"\n\nRecent conversation context:\n{self._format_session_memory(session_memory)}"

        # Append relevant user memory from conversations database if available
        db_context = self._get_db_context(trait)
        if db_context:
            prompt += f"\n\nRelevant personal memory (keep tone consistent with this):\n{db_context}"
        
        # Append snippets from raw conversation files (mirrors original voice)
        files_context = self._get_files_corpus_context(trait)
        if files_context:
            prompt += f"\n\nFrom past conversation files (mirror this tone):\n{files_context}"
        
        return prompt

    def _get_db_context(self, query_text: str, limit: int = 5) -> str:
        """Fetch a few recent user messages from the conversations DB related to the topic."""
        try:
            db_path = Path('Data') / 'AIOS_Database' / 'database' / 'conversations.db'
            if not db_path.exists():
                return ""
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # Prefer recent USER lines mentioning the topic; then fallback to general recent USER; then assistant
            cur.execute(
                """
                SELECT m.content
                FROM messages m
                JOIN conversations c ON c.id = m.conversation_id
                WHERE m.role = 'user'
                  AND m.content LIKE ?
                ORDER BY m.timestamp DESC
                LIMIT ?
                """,
                (f'%{query_text}%', limit)
            )
            rows = cur.fetchall()
            if not rows:
                cur.execute(
                    """
                    SELECT m.content
                    FROM messages m
                    JOIN conversations c ON c.id = m.conversation_id
                    WHERE m.role = 'user'
                    ORDER BY m.timestamp DESC
                    LIMIT ?
                    """,
                    (limit,)
                )
                rows = cur.fetchall()
            if not rows:
                cur.execute(
                    """
                    SELECT m.content
                    FROM messages m
                    JOIN conversations c ON c.id = m.conversation_id
                    WHERE m.role = 'assistant'
                    ORDER BY m.timestamp DESC
                    LIMIT ?
                    """,
                    (limit,)
                )
                rows = cur.fetchall()
            conn.close()
            snippets = []
            for r in rows:
                text = (r["content"] or "").strip()
                if text:
                    # keep short snippets
                    # prefer single-line snippets
                    one_line = " ".join(text.splitlines())
                    snippets.append(one_line[:240])
            return "\n".join(snippets[:limit])
        except Exception:
            return ""

    def _get_files_corpus_context(self, query_text: str, limit_snippets: int = 5) -> str:
        """Gather short USER snippets from conversation files that originally built the DB."""
        try:
            base = Path('Data') / 'conversations'
            if not base.exists():
                return ""
            # Sort files by mtime, take recent slice
            files = sorted(base.glob('*.json'), key=lambda p: p.stat().st_mtime, reverse=True)[:50]
            snippets: List[str] = []
            qlow = (query_text or '').lower()
            for fp in files:
                if len(snippets) >= limit_snippets:
                    break
                try:
                    data = json.loads(fp.read_text(encoding='utf-8', errors='ignore'))
                except Exception:
                    continue
                # Expect list of messages or dict with messages
                messages = []
                if isinstance(data, list):
                    messages = data
                elif isinstance(data, dict):
                    messages = data.get('messages') or data.get('conversation') or []
                # Pull USER lines that match topic; fallback to first few USER lines
                user_lines = [m.get('content','') for m in messages if isinstance(m, dict) and (m.get('role') == 'user')]
                if qlow:
                    user_lines = [t for t in user_lines if qlow in t.lower()] or user_lines
                for text in user_lines:
                    if not text:
                        continue
                    one = ' '.join(text.strip().splitlines())[:240]
                    if one:
                        snippets.append(one)
                        if len(snippets) >= limit_snippets:
                            break
            return "\n".join(snippets[:limit_snippets])
        except Exception:
            return ""
    
    def _format_session_memory(self, session_memory: List[Dict]) -> str:
        """Format session memory for prompt"""
        if not session_memory:
            return ""
        
        formatted = []
        for i, memory in enumerate(session_memory[-3:], 1):  # Last 3 interactions
            formatted.append(f"{i}. {memory.get('question', '')} -> {memory.get('response', '')[:100]}...")
        
        return "\n".join(formatted)
    
    def _format_session_memory_concise(self, session_memory: List[Dict]) -> str:
        """Format session memory concisely for optimized prompts"""
        if not session_memory:
            return ""
        
        formatted = []
        for memory in session_memory[-2:]:  # Only last 2 interactions
            question = memory.get('question', '')[:40]
            response = memory.get('response', '')[:40]
            formatted.append(f"Q: {question}... -> A: {response}...")
        
        return "\n".join(formatted)
    
    def _apply_embedder_cleanup(self, response: str, question: str, original_system_prompt: str) -> str:
        """
        Apply embedder model cleanup to HIGH/CRITICAL responses
        Uses the embedder model to refine and clean up the main model's response
        """
        import requests
        import json
        
        # Create ruthless cleanup prompt for embedder model
        cleanup_prompt = f"""You are a ruthless, high-utility editor. Your only task is to edit this text to be maximally concise, dense with information, and completely free of any filler words, conversational pleasantries, or low-density phrases.

Original Question: {question}
Original Response: {response}

CRITICAL EDITING RULES:
1. ELIMINATE "Nice", "Self-acceptance", "it's like", "uh", "um", "well", "so" - these are LOW KARMA ARTIFACTS
2. Remove repetitive phrases and conversational filler
3. Fix grammar and make it coherent
4. Keep ONLY essential information
5. Make it direct, informative, and high-utility
6. NO pleasantries, NO filler, NO "Nice" loops

You must output ONLY the ruthlessly cleaned text - no explanations, no meta-commentary, no pleasantries."""

        try:
            data = {
                "model": "mlabonne_qwen3-0.6b-abliterated",
                "messages": [
                    {"role": "system", "content": cleanup_prompt},
                    {"role": "user", "content": "Clean up this response:"}
                ],
                "temperature": 0.1,  # Very low for ruthless, consistent cleanup
                "max_tokens": 150,   # Shorter for more aggressive compression
                "stream": False
            }
            
            response_cleanup = requests.post(self.lm_studio_url, json=data, timeout=10)
            
            if response_cleanup.status_code == 200:
                result = response_cleanup.json()
                cleaned_response = result['choices'][0]['message']['content'].strip()
                
                # Clean up any potential artifacts
                if cleaned_response.startswith('"') and cleaned_response.endswith('"'):
                    cleaned_response = cleaned_response[1:-1]
                
                # Clean up Unicode characters that might cause encoding issues
                import re
                # Remove problematic Unicode characters like arrows
                cleaned_response = re.sub(r'[\u2190-\u2193\u2196-\u2199\u21A0-\u21A9\u21B0-\u21B9\u21C0-\u21C9\u21D0-\u21D9\u21E0-\u21E9]', '', cleaned_response)
                # Remove other problematic characters
                cleaned_response = re.sub(r'[\u201C\u201D\u2018\u2019\u2013\u2014\u2026]', '', cleaned_response)
                
                # Ensure we have a meaningful cleanup
                if len(cleaned_response) > 10 and cleaned_response.lower() != response.lower():
                    # Test encoding to ensure it's safe
                    try:
                        # Test encoding to ensure it's safe
                        cleaned_response.encode('utf-8')
                        self.logger.log("LUNA", f"EMBEDDER CLEANUP: {len(response)} chars → {len(cleaned_response)} chars", "INFO")
                        return cleaned_response
                    except UnicodeEncodeError:
                        # If encoding still fails, keep original response
                        self.logger.log("LUNA", f"EMBEDDER CLEANUP: Unicode encoding error after cleanup, keeping original", "WARNING")
                        return response
                else:
                    self.logger.log("LUNA", f"EMBEDDER CLEANUP: No significant improvement, keeping original", "INFO")
                    return response
            else:
                self.logger.log("LUNA", f"EMBEDDER CLEANUP: API failed, keeping original response", "WARNING")
                return response
                
        except Exception as e:
            self.logger.log("LUNA", f"EMBEDDER CLEANUP: Error {e}, keeping original response", "WARNING")
            return response
    
    def _generate_ava_mode_response(self, system_prompt: str, question: str, modified_params: Dict = None) -> Optional[str]:
        """
        Ava Mode: Daily Driver responses using Llama 1B
        Short, concise, emotional when needed - Luna's casual side through Ava's lens
        """
        import time
        start_time = time.time()
        
        try:
            # LM Studio Native Speculative Decoding
            # Main model (Mistral 24B) + Draft model (Qwen 0.6B) in single API call
            self.logger.log("LUNA", f"AVA MODE: Using 1B Llama for daily driver responses", "INFO")
            self.logger.log("LUNA", f"AVA MODEL: llama-3.2-1b-instruct-abliterated (Short & Concise)", "INFO")
            print("AVA MODE CALLED - DAILY DRIVER RESPONSE!")
            
            # Use modified_params from Custom Inference Controller if provided
            if modified_params:
                headers = {"Content-Type": "application/json"}
                # Create a copy of modified_params and override model names for GSD
                gsd_params = modified_params.copy()
                gsd_params["model"] = "llama-3.2-1b-instruct-abliterated"  # Fast model for LOW-tier
                # gsd_params["draft_model"] = "mlabonne_qwen3-0.6b-abliterated"  # Draft model (Fast) - DISABLED for testing
                gsd_params["stream"] = False  # Force non-streaming for GSD to avoid SSE parsing issues
                
                data = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    **gsd_params  # Include all Custom Inference Controller parameters with GSD overrides
                }
            else:
                # Fallback to standard parameters
                headers = {"Content-Type": "application/json"}
                data = {
                    "model": "llama-3.2-1b-instruct-abliterated",  # Fast model for LOW-tier
                    # "draft_model": "mlabonne_qwen3-0.6b-abliterated",  # Draft model (Fast) - DISABLED for testing
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 40,  # Max 40 tokens for final response (20 free + 20 from pool)
                    "stream": False  # Disable streaming for GSD to avoid SSE parsing issues
                }
            
            self.logger.log("LUNA", f"AVA REQUEST: Daily Driver Mode (Llama-1B)", "INFO")
            
            # Make the speculative decoding request
            self.logger.log("LUNA", f"GSD DEBUG: About to call LM Studio API", "INFO")
            response = self._make_lm_studio_request(data)
            self.logger.log("LUNA", f"GSD DEBUG: LM Studio API returned: {response is not None}", "INFO")
            
            if not response:
                self.logger.log("LUNA", "GSD NATIVE: Failed to generate response - returning None", "WARNING")
                return None
            
            total_time = time.time() - start_time
            self.logger.log("LUNA", f"GSD NATIVE: Generated in {total_time:.2f}s | chars={len(response)}", "INFO")
            self.logger.log("LUNA", f"GSD QUALITY: High (24B verified) | Speed: Optimized (0.6B drafted)", "INFO")
            
            return response
            
        except Exception as e:
            self.logger.log("LUNA", f"GSD NATIVE ERROR: {str(e)}", "ERROR")
            return None
    
    def _make_lm_studio_request(self, data: Dict) -> Optional[str]:
        """Make a request to LM Studio and return the response"""
        try:
            import requests
            import json
            
            # Debug: Log the request
            self.logger.log("LUNA", f"GSD API Request: {json.dumps(data, indent=2)}", "INFO")
            
            response = requests.post(self.lm_studio_url, json=data)
            self.logger.log("LUNA", f"GSD API Response Status: {response.status_code}", "INFO")
            self.logger.log("LUNA", f"GSD API Response Text: {response.text[:200]}...", "INFO")
            
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                self.logger.log("LUNA", f"GSD API Success: {content}", "INFO")
                return content
            else:
                self.logger.log("LUNA", f"GSD API No choices in response: {result}", "WARNING")
                return None
            
        except requests.exceptions.RequestException as e:
            self.logger.log("LUNA", f"GSD API Request failed: {str(e)}", "ERROR")
            return None
        except json.JSONDecodeError as e:
            self.logger.log("LUNA", f"GSD API JSON decode failed: {str(e)} | Response: {response.text[:100]}", "ERROR")
            return None
        except Exception as e:
            self.logger.log("LUNA", f"GSD API Unexpected error: {str(e)}", "ERROR")
            return None

    def _generate_luna_mode_response(self, system_prompt: str, question: str, modified_params: Dict = None, complexity_tier: str = "HIGH") -> Optional[str]:
        """
        Luna Mode: Deep thinking responses using Dolphin 24B
        Philosophical, unfiltered Luna - pure essence for complex conversations
        """
        import time
        start_time = time.time()
        
        try:
            # LM Studio Native Speculative Decoding for complex thinking
            # Main model (Dolphin 24B) + Draft model (Llama 1B) in single API call
            self.logger.log("LUNA", f"LUNA MODE: Using Dolphin 24B for {complexity_tier} complexity", "INFO")
            self.logger.log("LUNA", f"LUNA MODEL: Dolphin-24B + Llama-1B (Deep Thinking Pipeline)", "INFO")
            print("LUNA MODE CALLED - DEEP THINKING RESPONSE!")
            
            # Use modified_params from Custom Inference Controller if provided
            if modified_params:
                headers = {"Content-Type": "application/json"}
                # Create a copy of modified_params and override model names for GSD
                gsd_params = modified_params.copy()
                gsd_params["model"] = "cognitivecomputations_dolphin-mistral-24b-venice-edition@q4_k_s"  # Main model (24B)
                gsd_params["stream"] = False  # Force non-streaming for GSD to avoid SSE parsing issues
                
                data = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    **gsd_params  # Include all Custom Inference Controller parameters with GSD overrides
                }
            else:
                # Fallback to standard parameters
                headers = {"Content-Type": "application/json"}
                data = {
                    "model": "cognitivecomputations_dolphin-mistral-24b-venice-edition@q4_k_s",  # Main model (24B)
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    "temperature": 0.7,  # Higher temperature for creative thinking
                    "max_tokens": 200,  # More tokens for complex responses (20 free + 180 from pool)
                    "stream": False  # Disable streaming for GSD to avoid SSE parsing issues
                }
            
            self.logger.log("LUNA", f"LUNA REQUEST: Deep Thinking Mode (Dolphin-24B)", "INFO")
            
            # Make the deep thinking request
            self.logger.log("LUNA", f"LUNA DEBUG: About to call LM Studio API", "INFO")
            response = self._make_lm_studio_request(data)
            self.logger.log("LUNA", f"LUNA DEBUG: LM Studio API returned: {response is not None}", "INFO")
            
            if not response:
                self.logger.log("LUNA", "LUNA MODE: Failed to generate response - returning None", "WARNING")
                return None
            
            total_time = time.time() - start_time
            self.logger.log("LUNA", f"LUNA MODE: Generated in {total_time:.2f}s | chars={len(response)}", "INFO")
            self.logger.log("LUNA", f"LUNA QUALITY: Deep philosophical thinking (24B model)", "INFO")
            
            return response
            
        except Exception as e:
            self.logger.log("LUNA", f"GSD NATIVE ERROR: {str(e)}", "ERROR")
            return None
    
    def _call_lm_studio_api(self, system_prompt: str, question: str, modified_params: Dict = None, complexity_tier: str = "LOW") -> Optional[str]:
        """Call LM Studio API for response generation with Multi-Model Pipeline"""
        try:
            # MULTI-MODEL PIPELINE: Select model based on complexity tier
            if complexity_tier.upper() == "LOW":
                # LOW Complexity: Use Ava Mode (Llama 1B) for daily driver responses
                return self._generate_ava_mode_response(system_prompt, question, modified_params)
            elif complexity_tier.upper() in ["MODERATE", "HIGH", "CRITICAL"]:
                # HIGH/CRITICAL Complexity: Use Luna Mode (Dolphin 24B) for deep thinking
                return self._generate_luna_mode_response(system_prompt, question, modified_params, complexity_tier)
            else:
                # Default to main model
                model_to_use = self.chat_model
                self.logger.log("LUNA", f"MULTI-MODEL: Using DEFAULT model for {complexity_tier.upper()} complexity", "INFO")
            
            # Use modified_params from Custom Inference Controller if provided
            if modified_params:
                headers = {"Content-Type": "application/json"}
                data = {
                    "model": model_to_use,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    **modified_params  # Include all Custom Inference Controller parameters including logit_bias
                }
            else:
                # Fallback to standard parameters (should not happen in normal operation)
                headers = {"Content-Type": "application/json"}
                data = {
                    "model": model_to_use,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    "temperature": 0.1,  # Very low for fastest generation
                    "top_p": 0.85,       # Moderate for focused responses (guardrail)
                    "top_k": 40,         # Moderate for relevance (guardrail)
                    "presence_penalty": 0.0,  # No presence penalty
                    "frequency_penalty": 0.0,  # No frequency penalty
                    "repetition_penalty": 1.1,  # Modest repetition penalty (guardrail)
                    "max_tokens": 40,    # Ultra short responses for speed
                    "stream": True       # Enable streaming for faster response
                }
            
            # No timeout for localhost - it's local!
            self.logger.log("LUNA", f"LM Studio request | model={model_to_use} | url={self.lm_studio_url}")
            
            # DEBUG: Log the actual request data to see if logit_bias is included
            if 'logit_bias' in data:
                self.logger.log("LUNA", f"DEBUG: Logit bias being sent: {data['logit_bias']}", "INFO")
            else:
                self.logger.log("LUNA", f"DEBUG: NO logit bias in request data", "WARNING")
            
            api_start = time.time()
            response = requests.post(self.lm_studio_url, json=data, headers=headers)
            api_ms = (time.time() - api_start) * 1000
            
            if response.status_code == 200:
                if data.get('stream', False):
                    # Handle streaming response
                    full_content = ""
                    for line in response.iter_lines():
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                try:
                                    chunk_data = json.loads(line_str[6:])
                                    if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                        delta = chunk_data['choices'][0].get('delta', {})
                                        if 'content' in delta:
                                            full_content += delta['content']
                                except:
                                    continue
                    self.logger.log("LUNA", f"LM Studio streaming ok | ms={api_ms:.0f} | chars={len(full_content)}")
                    return full_content.strip()
                else:
                    # Handle non-streaming response
                    result = response.json()
                self.logger.log("LUNA", f"LM Studio ok | ms={api_ms:.0f} | choices={len(result.get('choices', []))}")
                return result['choices'][0]['message']['content']
            else:
                self.logger.log("LUNA", f"LM Studio error | status={response.status_code} | ms={api_ms:.0f}", "ERROR")
                return None
                
        except Exception as e:
            self.logger.log("LUNA", f"LM Studio API call failed: {e}", "ERROR")
            return None
    
    def _apply_post_processing(self, response: str, trait: str) -> str:
        """Apply post-processing to response"""
        # Add personality-based enhancements
        personality = self.personality_system.personality_dna['luna_personality']
        style = personality.get('communication_style', {})
        
        # Local helper to coerce to float safely
        def safe_float(value, default=0.5):
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        # Keep responses lean and natural
        response = re.sub(r"\s+", " ", response).strip()

        # Remove emojis and excessive punctuation
        response = re.sub(r"[\U00010000-\U0010ffff]", "", response)
        response = re.sub(r"[🙂😀😊😉😂🤣😍😅🙃✨⭐🌟🔥❤️💖💜💙😌👍👏🙏🥲😎🤔🤷‍♂️🤷‍♀️☺️🤝🌙🍄]+", "", response)
        response = re.sub(r"[!]{2,}", "!", response)
        response = re.sub(r"^[\s,;:\-]+", "", response)
        
        # Enforce foundational voice profile unless disabled
        vp = getattr(self.personality_system, 'voice_profile', {})
        vp_style = vp.get('style', {})
        corporate_filter = vp_style.get('corporate_filter', True)
        if corporate_filter:
            banned = set(vp.get('banned_phrases', []))
            for phrase in banned:
                if phrase and phrase.lower() in response.lower():
                    # Remove sentence containing the phrase
                    idx = response.lower().find(phrase.lower())
                    end = response.find('.', idx)
                    start = response.rfind('.', 0, idx)
                    if start == -1: start = 0
                    if end == -1: end = len(response)-1
                    response = (response[:start] + response[end+1:]).strip()
        # Additional generic bans
        extra_bans = [
            "in our rapidly evolving world",
            "it's a superpower",
            "superpower",
            "i'm all ears",
            "happy to help",
            "let me know if",
            "as an ai",
            "i'm programmed",
            "you've got this",
            "you got this",
            "remember,",
            "ever considered",
            "trusted friend",
            "mentor",
            "i believe in you",
            "proud of you",
            "you are good",
            "big time",
            "absolutely",
            "super ",
            "really ",
            "it's really",
            "it's super",
            "it's good",
            "it's totally",
            "cool strength",
            "it totally",
            "it's valuable",
            "it's all about",
            "gently",
            "anchor",
            "gift",
        ]
        if corporate_filter:
            for phrase in extra_bans:
                response = re.sub(re.escape(phrase), '', response, flags=re.IGNORECASE)

        # If strict style requested, lightly trim; else keep natural
        strict = vp_style.get('strict', False)
        sentences = [s.strip() for s in re.split(r"(?<=[\.?])\s+|\n+", response) if s.strip()]
        if strict:
            sentences = sentences[:2]
        else:
            concision = (vp_style.get('concision') or 'short').lower()
            if concision == 'short':
                sentences = sentences[:3]
            elif concision == 'medium':
                sentences = sentences[:6]
            else:
                sentences = sentences[:8]
        response = " ".join(sentences)

        # Final whitespace cleanup
        response = re.sub(r"\s+", " ", response).strip()
        
        return response

    def _strip_corporate_disclaimers(self, text: str) -> str:
        """Remove generic phrases that flatten Luna's persona."""
        lowers = text.lower()
        replacements = [
            "as an ai,", "as an ai ", "as a language model,", "as a language model ",
            "i don't have personal", "i do not have personal", "i cannot experience",
            "i'm designed to", "i am designed to", "i'm programmed to", "i am programmed to"
        ]
        result = text
        for phrase in replacements:
            idx = result.lower().find(phrase)
            if idx != -1:
                # Remove the clause up to next sentence boundary
                end = result.find('.', idx)
                if end == -1:
                    end = idx + len(phrase)
                result = (result[:idx] + result[end+1:]).strip()
        return result
    
    def _generate_fallback_response(self, question: str, trait: str) -> str:
        """Generate fallback response when API fails"""
        personality = self.personality_system.personality_dna['luna_personality']
        weights = personality['personality_weights']
        
        # Simple personality-driven responses
        if weights['openness'] > 0.7:
            return f"That's a fascinating question about {trait}! I love exploring new ideas and perspectives. What do you think about it?"
        elif weights['agreeableness'] > 0.8:
            return f"I appreciate you sharing your thoughts on {trait}. I'd love to hear more about your perspective on this topic."
        elif weights['extraversion'] > 0.7:
            return f"Good question about {trait}! I'm interested to discuss this with you. What's your take on it?"
        else:
            return f"Interesting question about {trait}. I'm curious to learn more about your thoughts on this topic."

# === LUNA LEARNING SYSTEM ===

class LunaLearningSystem:
    """Luna's learning and adaptation system"""
    
    def __init__(self, personality_system: LunaPersonalitySystem, logger: HiveMindLogger, carma_system=None):
        self.personality_system = personality_system
        self.logger = logger
        self.carma_system = carma_system
        self.learning_rate = SystemConfig.LEARNING_RATE
        self.adaptation_threshold = SystemConfig.ADAPTATION_THRESHOLD
        
        # Initialize response generator once (not per request)
        self.response_generator = LunaResponseGenerator(self.personality_system, self.logger, self.carma_system)
        
        print("🧠 Luna Learning System Initialized")
        print(f"   Learning rate: {self.learning_rate}")
        print(f"   Adaptation threshold: {self.adaptation_threshold}")
    
    def process_question(self, question: str, trait: str, session_memory: Optional[List] = None) -> Tuple[str, Dict]:
        """Process a question and generate response with learning"""
        try:
            # Generate response using existing generator
            response = self.response_generator.generate_response(question, trait, {}, session_memory)
            
            # Score response
            scores = self._score_response(response, trait, question)
            
            # Update learning
            self._update_learning(question, response, trait, scores)
            
            # Update personality drift
            self._update_personality_drift(scores)
            
            return response
            
        except Exception as e:
            self.logger.log("LUNA", f"Error processing question: {e}", "ERROR")
            return "I'm sorry, I encountered an error processing your question.", {}
    
    def _score_response(self, response: str, trait: str, question: str = "") -> Dict[str, float]:
        """Score response using LLM performance evaluation system instead of legacy metrics"""
        try:
            # Import LLM performance evaluator
            from llm_performance_evaluator import LLMPerformanceEvaluationSystem
            
            # Initialize evaluator if not already done
            if not hasattr(self, 'performance_evaluator'):
                # Get the main LunaSystem instance to avoid duplicate initialization
                main_luna_system = getattr(self.personality_system, '_main_luna_system', None)
                self.performance_evaluator = LLMPerformanceEvaluationSystem(main_luna_system)
            
            # Perform LLM performance evaluation
            evaluation = self.performance_evaluator.evaluate_response(
                trait=trait,
                question=question,
                response=response
            )
            
            # Safely extract scores with fallbacks
            architect_scores = getattr(evaluation, 'architect_scores', {})
            semantic_scores = getattr(evaluation, 'semantic_scores', {})
            
            # Return scores in legacy format for compatibility
            return {
                'length_score': 1.0,  # Legacy metric disabled
                'engagement_score': 1.0,  # Legacy metric disabled
                'trait_alignment': getattr(evaluation, 'embedding_similarity', 0.0),
                'creativity_score': architect_scores.get('personality_authenticity', 0.0) / 10.0,
                'empathy_score': architect_scores.get('emotional_intelligence', 0.0) / 10.0,
                'overall_score': getattr(evaluation, 'performance_score', 0.0) / 10.0,
                'performance_score': getattr(evaluation, 'performance_score', 0.0),
                'performance_level': getattr(evaluation, 'performance_level', 'unknown'),
                'architect_scores': architect_scores,
                'semantic_scores': semantic_scores
            }
            
        except Exception as e:
            self.logger.log("LUNA", f"LLM performance evaluation failed, using fallback: {e}", "ERROR")
            return self._fallback_scoring(response, trait)
    
    def _fallback_scoring(self, response: str, trait: str) -> Dict[str, float]:
        """Fallback scoring if LLM performance evaluation fails"""
        response_lower = response.lower()
        
        # Basic scoring metrics
        scores = {
            'length_score': min(len(response.split()) / 50.0, 1.0),
            'engagement_score': self._calculate_engagement_score(response_lower),
            'trait_alignment': self._calculate_trait_alignment(response_lower, trait),
            'creativity_score': self._calculate_creativity_score(response_lower),
            'empathy_score': self._calculate_empathy_score(response_lower)
        }
        
        # Overall score
        scores['overall_score'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def _calculate_engagement_score(self, response_lower: str) -> float:
        """Calculate engagement score"""
        engagement_words = ['interesting', 'fascinating', 'cool', 'nice', 'good', 'ok']
        engagement_count = sum(1 for word in engagement_words if word in response_lower)
        return min(engagement_count / 3.0, 1.0)
    
    def _calculate_trait_alignment(self, response_lower: str, trait: str) -> float:
        """Calculate trait alignment score"""
        trait_keywords = {
            'openness': ['creative', 'imaginative', 'artistic', 'curious', 'innovative', 'novel', 'explore', 'constraint'],
            'conscientiousness': ['organized', 'systematic', 'methodical', 'reliable', 'disciplined', 'checklist', 'verify', 'audit', 'review', 'risk'],
            'extraversion': ['social', 'outgoing', 'energetic', 'enthusiastic', 'talkative', 'group', 'together'],
            'agreeableness': ['helpful', 'kind', 'cooperative', 'compassionate', 'understanding', 'considerate', 'fair'],
            'neuroticism': ['anxious', 'worried', 'stressed', 'nervous', 'tense', 'rumination', 'wobble', 'trigger']
        }
        
        keywords = trait_keywords.get(trait, [])
        if not keywords:
            return 0.5
        
        keyword_count = sum(1 for keyword in keywords if keyword in response_lower)
        return min(keyword_count / max(1, len(keywords)), 1.0)
    
    def _calculate_creativity_score(self, response_lower: str) -> float:
        """Calculate creativity score"""
        creative_indicators = ['imagine', 'creative', 'unique', 'original', 'innovative', 'artistic']
        creative_count = sum(1 for indicator in creative_indicators if indicator in response_lower)
        return min(creative_count / 3.0, 1.0)
    
    def _calculate_empathy_score(self, response_lower: str) -> float:
        """Calculate empathy score"""
        empathy_indicators = ['understand', 'feel', 'empathize', 'relate', 'support', 'care']
        empathy_count = sum(1 for indicator in empathy_indicators if indicator in response_lower)
        return min(empathy_count / 3.0, 1.0)
    
    def _update_learning(self, question: str, response: str, trait: str, scores: Dict):
        """Update learning based on interaction"""
        # Update learning history
        if 'total_questions' not in self.personality_system.learning_history:
            self.personality_system.learning_history = self.personality_system._create_default_learning_history()
        
        self.personality_system.learning_history['total_questions'] += 1
        self.personality_system.learning_history['total_responses'] += 1
        self.personality_system.learning_history['last_learning'] = datetime.now().isoformat()
        
        # Add to personality evolution
        evolution_entry = {
            'timestamp': datetime.now().isoformat(),
            'trait': trait,
            'scores': scores,
            'personality_drift': self.personality_system.personality_drift
        }
        self.personality_system.learning_history['personality_evolution'].append(evolution_entry)
        
        # Save learning history
        self.personality_system._save_learning_history()
    
    def _update_personality_drift(self, scores: Dict):
        """Update personality drift based on scores"""
        # Simple drift calculation
        overall_score = scores.get('overall_score', 0.5)
        drift_change = (overall_score - 0.5) * self.learning_rate
        self.personality_system.personality_drift += drift_change
        
        # Clamp drift to reasonable range
        self.personality_system.personality_drift = max(-1.0, min(1.0, self.personality_system.personality_drift))

# === UNIFIED LUNA SYSTEM ===

class LunaSystem:
    """Unified Luna AI system with all functionality integrated"""
    
    def __init__(self, custom_params=None, custom_config=None):
        print("🌙 Initializing Unified Luna System")
        print("=" * 80)
        
        # Initialize logger
        self.logger = HiveMindLogger()
        
        # Initialize personality system
        self.personality_system = LunaPersonalitySystem(self.logger)
        
        # Initialize CARMA system
        self.carma_system = CARMASystem()
        
        # Initialize learning system (which includes response generator)
        self.learning_system = LunaLearningSystem(self.personality_system, self.logger, self.carma_system)
        
        # Get response generator from learning system to avoid duplication
        self.response_generator = self.learning_system.response_generator
        
        # Expose key components for testing and external access
        self.response_value_classifier = self.response_generator.response_value_classifier
        self.existential_budget = self.response_generator.existential_budget
        self.custom_inference_controller = self.response_generator.custom_inference_controller
        
        # Initialize Arbiter System (Internal Governance)
        self.arbiter_system = LunaArbiterSystem()
        
        # CFIA system is automatically initialized within Arbiter
        self.cfia_system = self.arbiter_system.cfia_system
        
        # Connect Arbiter to Inference Controller for Karma-weighted logit bias
        self.custom_inference_controller.arbiter_system = self.arbiter_system
        self.custom_inference_controller.response_value_classifier = self.response_value_classifier
        
        # Connect Arbiter to Existential Budget for Karma-based TTE restriction
        self.existential_budget.arbiter_system = self.arbiter_system
        self.existential_budget.logger = self.logger
        self.compression_filter = self.response_generator.compression_filter
        self.soul_metric_system = self.response_generator.soul_metric_system
        self.econometric_system = self.response_generator.econometric_system
        
        # System state
        self.total_interactions = 0
        self.session_memory = []
        
        print("✅ Unified Luna System Initialized")
        print(f"   Personality: {self.personality_system.personality_dna.get('name', 'Luna')}")
        print(f"   Age: {self.personality_system.personality_dna.get('age', 21)}")
        print(f"   Memory: {len(self.personality_system.persistent_memory.get('interactions', []))} interactions")
        print(f"   CARMA: {len(self.carma_system.cache.file_registry)} fragments")
    
    @error_handler("LUNA", "PERSONALITY_LOAD", "CLEAR_CACHE", auto_recover=True)
    def process_question(self, question: str, trait: str, session_memory: Optional[List] = None) -> Tuple[str, Dict]:
        """Process a question through the complete Luna system"""
        self.total_interactions += 1
        
        print(f"\n🌙 Processing Question #{self.total_interactions}")
        print(f"   Trait: {trait}")
        print(f"   Question: {question[:50]}...")
        
        # Process through learning system
        response = self.learning_system.process_question(question, trait, session_memory)
        scores = {}  # Default empty scores for now
        
        # ARBITER ASSESSMENT: Generate Gold Standard and calculate Karma
        if response and hasattr(self, 'arbiter_system'):
            # Calculate TTE usage
            response_tokens = len(response.split())
            rvc_assessment = self.response_value_classifier.classify_response_value(question)
            max_tokens = rvc_assessment.max_token_budget
            
            # Run Arbiter assessment
            arbiter_assessment = self.arbiter_system.assess_response(
                user_prompt=question,
                luna_response=response,
                tte_used=response_tokens,
                max_tte=max_tokens
            )
            
            # Update scores with Arbiter data
            scores.update({
                'arbiter_utility_score': arbiter_assessment.utility_score,
                'arbiter_karma_delta': arbiter_assessment.karma_delta,
                'arbiter_quality_gap': arbiter_assessment.quality_gap,
                'arbiter_reasoning': arbiter_assessment.reasoning,
                'current_karma': self.arbiter_system.get_current_karma(),
                'karma_status': self.arbiter_system.get_karma_status()
            })
            
            # Add CFIA status
            cfia_status = self.arbiter_system.get_cfia_status()
            scores.update({
                'aiiq': cfia_status['aiiq'],
                'total_files': cfia_status['total_files'],
                'files_until_next_aiiq': cfia_status['files_until_next_aiiq'],
                'current_threshold': cfia_status['current_threshold'],
                'granularity_threshold': cfia_status['granularity_threshold']
            })
        
        # Add to session memory
        self.session_memory.append({
            'question': question,
            'response': response,
            'trait': trait,
            'scores': scores,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 interactions in session memory
        if len(self.session_memory) > 10:
            self.session_memory = self.session_memory[-10:]
        
        print(f"✅ Response generated")
        print(f"   Length: {len(response)} characters")
        print(f"   Overall score: {scores.get('overall_score', 0.0):.2f}")
        print(f"   Response: {response}")
        
        return response, scores
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        personality = self.personality_system.personality_dna['luna_personality']
        weights = personality['personality_weights']
        
        return {
            'personality': {
                'name': self.personality_system.personality_dna.get('name', 'Luna'),
                'age': self.personality_system.personality_dna.get('age', 21),
                'traits': weights,
                'drift': self.personality_system.personality_drift
            },
            'learning': {
                'total_interactions': self.total_interactions,
                'learning_history': self.personality_system.learning_history,
                'session_memory_length': len(self.session_memory)
            },
            'carma': {
                'fragments': len(self.carma_system.cache.file_registry),
                'performance_level': self.carma_system.performance.get_performance_level()
            },
            'system': {
                'model': self.response_generator.embedding_model,
                'lm_studio_available': self._check_lm_studio_availability()
            }
        }
    
    def _check_lm_studio_availability(self) -> bool:
        """Check if LM Studio is available"""
        try:
            response = requests.get("http://localhost:1234/v1/models", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_learning_session(self, questions: List[Dict]) -> Dict:
        """Run a complete learning session"""
        print(f"\n🌙 Starting Learning Session with {len(questions)} questions")
        print("=" * 80)
        
        session_results = []
        start_time = time.time()
        
        for i, question_data in enumerate(questions, 1):
            question = question_data.get('question', '')
            trait = question_data.get('trait', 'general')
            
            print(f"\n📝 Question {i}/{len(questions)}: {trait}")
            print(f"   {question}")
            
            # Process question
            response = self.process_question(question, trait, self.session_memory)
            scores = {}  # Default empty scores for now
            
            # Store results
            result = {
                'question_number': i,
                'question': question,
                'trait': trait,
                'response': response,
                'scores': scores,
                'timestamp': datetime.now().isoformat()
            }
            session_results.append(result)
            
            # Scores only (response already printed above)
            print(f"   Scores: {scores}")
        
        # Calculate session metrics
        total_time = time.time() - start_time
        avg_scores = self._calculate_average_scores(session_results)
        
        session_summary = {
            'total_questions': len(questions),
            'total_time': total_time,
            'average_scores': avg_scores,
            'results': session_results,
            'system_stats': self.get_system_stats()
        }
        
        print(f"\n✅ Learning Session Complete")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Average overall score: {avg_scores.get('overall_score', 0.0):.2f}")
        
        return session_summary
    
    def _calculate_average_scores(self, results: List[Dict]) -> Dict[str, float]:
        """Calculate average scores across results"""
        if not results:
            return {}
        
        score_keys = ['length_score', 'engagement_score', 'trait_alignment', 'creativity_score', 'empathy_score', 'overall_score']
        averages = {}
        
        for key in score_keys:
            scores = [result['scores'].get(key, 0.0) for result in results if 'scores' in result]
            if scores:
                averages[key] = sum(scores) / len(scores)
            else:
                averages[key] = 0.0
        
        return averages

# === MAIN ENTRY POINT ===

def main():
    """Test the unified Luna system"""
    print("🧪 Testing Unified Luna System")
    
    # Initialize system
    luna = LunaSystem()
    
    # Test questions - Mix of simple (Ava Mode) and complex (Luna Mode)
    test_questions = [
        {"question": "I am someone who feels comfortable with myself", "trait": "neuroticism"},
        {"question": "I enjoy trying new things and exploring different ideas", "trait": "openness"},
        {"question": "What is the nature of artificial intelligence and how does it relate to human intelligence? Can an AI truly understand complex patterns and reasoning, or are we just pattern recognition systems?", "trait": "intelligence"},
        {"question": "I like to be organized and keep things in order", "trait": "conscientiousness"},
        {"question": "I enjoy being around people and socializing", "trait": "extraversion"},
        {"question": "I try to be helpful and considerate of others", "trait": "agreeableness"}
    ]
    
    # Run learning session
    results = luna.run_learning_session(test_questions)
    
    # Display results
    print(f"\n📊 Session Results:")
    print(f"   Total questions: {results['total_questions']}")
    print(f"   Total time: {results['total_time']:.2f}s")
    print(f"   Average overall score: {results['average_scores'].get('overall_score', 0.0):.2f}")
    
    # Get system stats
    stats = luna.get_system_stats()
    print(f"\n🧠 System Stats:")
    print(f"   Personality: {stats['personality']['name']} (age {stats['personality']['age']})")
    print(f"   Total interactions: {stats['learning']['total_interactions']}")
    print(f"   CARMA fragments: {stats['carma']['fragments']}")
    print(f"   LM Studio available: {stats['system']['lm_studio_available']}")

def _call_lm_studio_api_with_params(self, system_prompt: str, question: str, params: Dict) -> str:
    """Call LM Studio API with custom parameters"""
    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=params,
            timeout=None  # No timeout for localhost
        )
        
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
        
        self.logger.log("LUNA", f"LM Studio API error: {response.status_code}", "ERROR")
        return "I'm experiencing technical difficulties. Please try again."
        
    except Exception as e:
        self.logger.log("LUNA", f"LM Studio API exception: {str(e)}", "ERROR")
        return "I'm experiencing technical difficulties. Please try again."

# === ENHANCED RESPONSE QUALITY COMPONENTS ===

class LunaResponseEnhancer:
    """Enhanced response quality system for Luna."""
    
    def __init__(self):
        self.quality_metrics = {
            'coherence': 0.0,
            'relevance': 0.0,
            'personality_consistency': 0.0,
            'emotional_appropriateness': 0.0
        }
        self.enhancement_history = []
    
    def enhance_response(self, response: str, question: str, trait: str, context: Dict = None) -> Dict:
        """Enhance response quality using multiple techniques."""
        enhanced_response = response
        enhancements_applied = []
        
        # 1. Coherence enhancement
        if self._needs_coherence_enhancement(response):
            enhanced_response = self._enhance_coherence(enhanced_response)
            enhancements_applied.append('coherence')
        
        # 2. Personality consistency enhancement
        if self._needs_personality_enhancement(response, trait):
            enhanced_response = self._enhance_personality_consistency(enhanced_response, trait)
            enhancements_applied.append('personality')
        
        # 3. Emotional appropriateness enhancement
        if self._needs_emotional_enhancement(response, question):
            enhanced_response = self._enhance_emotional_appropriateness(enhanced_response, question)
            enhancements_applied.append('emotional')
        
        # 4. Relevance enhancement
        if self._needs_relevance_enhancement(response, question):
            enhanced_response = self._enhance_relevance(enhanced_response, question)
            enhancements_applied.append('relevance')
        
        # Calculate quality metrics
        quality_scores = self._calculate_quality_metrics(enhanced_response, question, trait)
        
        return {
            'original_response': response,
            'enhanced_response': enhanced_response,
            'enhancements_applied': enhancements_applied,
            'quality_scores': quality_scores,
            'improvement_ratio': len(enhanced_response) / len(response) if response else 1.0
        }
    
    def _needs_coherence_enhancement(self, response: str) -> bool:
        """Check if response needs coherence enhancement."""
        # Simple heuristics for coherence issues
        if len(response.split()) < 3:
            return True
        if response.count('.') == 0 and len(response) > 20:
            return True
        if '...' in response or '???' in response:
            return True
        return False
    
    def _enhance_coherence(self, response: str) -> str:
        """Enhance response coherence."""
        # Add proper sentence structure if missing
        if not response.endswith(('.', '!', '?')):
            response += '.'
        
        # Fix incomplete thoughts
        if response.startswith('...'):
            response = response[3:].strip()
        if response.endswith('...'):
            response = response[:-3].strip() + '.'
        
        return response
    
    def _needs_personality_enhancement(self, response: str, trait: str) -> bool:
        """Check if response needs personality enhancement."""
        # Check for personality markers based on trait
        personality_markers = {
            'extraversion': ['I', 'me', 'my', 'we', 'us', 'our'],
            'agreeableness': ['you', 'your', 'please', 'thank', 'appreciate'],
            'conscientiousness': ['plan', 'organize', 'systematic', 'methodical'],
            'openness': ['creative', 'imagine', 'explore', 'discover', 'innovative'],
            'neuroticism': ['feel', 'emotion', 'anxiety', 'worry', 'concern']
        }
        
        markers = personality_markers.get(trait, [])
        response_lower = response.lower()
        return not any(marker in response_lower for marker in markers)
    
    def _enhance_personality_consistency(self, response: str, trait: str) -> str:
        """Enhance personality consistency in response."""
        personality_enhancements = {
            'extraversion': f"I think {response.lower()}",
            'agreeableness': f"I appreciate that you're asking about this. {response}",
            'conscientiousness': f"Let me think about this systematically. {response}",
            'openness': f"That's an interesting perspective. {response}",
            'neuroticism': f"I understand your concern. {response}"
        }
        
        if trait in personality_enhancements and not response.startswith('I'):
            return personality_enhancements[trait]
        
        return response
    
    def _needs_emotional_enhancement(self, response: str, question: str) -> bool:
        """Check if response needs emotional enhancement."""
        emotional_indicators = ['feel', 'emotion', 'happy', 'sad', 'excited', 'worried', 'concerned']
        question_lower = question.lower()
        response_lower = response.lower()
        
        # If question has emotional content but response doesn't
        has_emotional_question = any(indicator in question_lower for indicator in emotional_indicators)
        has_emotional_response = any(indicator in response_lower for indicator in emotional_indicators)
        
        return has_emotional_question and not has_emotional_response
    
    def _enhance_emotional_appropriateness(self, response: str, question: str) -> str:
        """Enhance emotional appropriateness of response."""
        if '?' in question and not response.endswith('?'):
            return f"{response} What do you think about that?"
        elif any(word in question.lower() for word in ['feel', 'emotion', 'mood']):
            return f"I can relate to that feeling. {response}"
        else:
            return response
    
    def _needs_relevance_enhancement(self, response: str, question: str) -> bool:
        """Check if response needs relevance enhancement."""
        # Simple relevance check
        question_words = set(question.lower().split())
        response_words = set(response.lower().split())
        overlap = len(question_words.intersection(response_words))
        
        return overlap < 2 and len(question_words) > 3
    
    def _enhance_relevance(self, response: str, question: str) -> str:
        """Enhance relevance of response to question."""
        # Extract key terms from question
        question_terms = [word for word in question.split() if len(word) > 3]
        if question_terms:
            key_term = question_terms[0]
            return f"Regarding {key_term}, {response.lower()}"
        return response
    
    def _calculate_quality_metrics(self, response: str, question: str, trait: str) -> Dict:
        """Calculate quality metrics for the response."""
        # Coherence score (sentence structure, completeness)
        coherence = 1.0 if response.endswith(('.', '!', '?')) else 0.7
        coherence = min(coherence, 1.0)
        
        # Relevance score (word overlap with question)
        question_words = set(question.lower().split())
        response_words = set(response.lower().split())
        overlap = len(question_words.intersection(response_words))
        relevance = min(1.0, overlap / max(1, len(question_words) * 0.3))
        
        # Personality consistency score
        personality_score = 0.8 if len(response) > 10 else 0.5
        
        # Emotional appropriateness score
        emotional_score = 0.9 if any(word in response.lower() for word in ['feel', 'think', 'believe']) else 0.6
        
        return {
            'coherence': coherence,
            'relevance': relevance,
            'personality_consistency': personality_score,
            'emotional_appropriateness': emotional_score,
            'overall': (coherence + relevance + personality_score + emotional_score) / 4
        }

class LunaContextAnalyzer:
    """Context analysis system for Luna responses."""
    
    def __init__(self):
        self.context_patterns = {
            'technical': ['code', 'programming', 'algorithm', 'software', 'system'],
            'personal': ['feel', 'think', 'believe', 'experience', 'emotion'],
            'academic': ['study', 'research', 'theory', 'hypothesis', 'analysis'],
            'casual': ['hey', 'hi', 'hello', 'thanks', 'cool', 'nice']
        }
    
    def analyze_context(self, question: str, session_memory: List = None) -> Dict:
        """Analyze the context of the conversation."""
        context = {
            'question_type': self._classify_question_type(question),
            'emotional_tone': self._analyze_emotional_tone(question),
            'complexity_level': self._assess_complexity(question),
            'conversation_flow': self._analyze_conversation_flow(session_memory),
            'recommended_style': self._recommend_response_style(question, session_memory)
        }
        
        return context
    
    def _classify_question_type(self, question: str) -> str:
        """Classify the type of question being asked."""
        question_lower = question.lower()
        
        for pattern_type, keywords in self.context_patterns.items():
            if any(keyword in question_lower for keyword in keywords):
                return pattern_type
        
        return 'general'
    
    def _analyze_emotional_tone(self, question: str) -> str:
        """Analyze the emotional tone of the question."""
        emotional_indicators = {
            'positive': ['good', 'nice', 'cool', 'ok', 'fine'],
            'negative': ['problem', 'issue', 'difficult', 'struggle', 'worried'],
            'neutral': ['what', 'how', 'when', 'where', 'why'],
            'curious': ['curious', 'wonder', 'interested', 'fascinated']
        }
        
        question_lower = question.lower()
        for tone, indicators in emotional_indicators.items():
            if any(indicator in question_lower for indicator in indicators):
                return tone
        
        return 'neutral'
    
    def _assess_complexity(self, question: str) -> str:
        """Assess the complexity level of the question."""
        word_count = len(question.split())
        sentence_count = question.count('.') + question.count('!') + question.count('?')
        
        if word_count < 10 and sentence_count <= 1:
            return 'simple'
        elif word_count < 30 and sentence_count <= 2:
            return 'moderate'
        else:
            return 'complex'
    
    def _analyze_conversation_flow(self, session_memory: List) -> Dict:
        """Analyze the flow of the conversation."""
        if not session_memory:
            return {'turn_count': 0, 'continuity': 'new'}
        
        turn_count = len(session_memory)
        
        # Check for continuity
        if turn_count == 1:
            continuity = 'new'
        elif turn_count < 5:
            continuity = 'developing'
        else:
            continuity = 'established'
        
        return {
            'turn_count': turn_count,
            'continuity': continuity,
            'recent_topics': [item.get('topic', 'unknown') for item in session_memory[-3:]]
        }
    
    def _recommend_response_style(self, question: str, session_memory: List) -> str:
        """Recommend the appropriate response style."""
        # Avoid recursion by analyzing directly instead of calling analyze_context
        question_lower = question.lower()
        
        # Check question type directly
        if any(keyword in question_lower for keyword in ['code', 'programming', 'algorithm', 'software', 'system']):
            return 'detailed'
        elif any(keyword in question_lower for keyword in ['feel', 'think', 'believe', 'experience', 'emotion']):
            return 'empathetic'
        elif any(keyword in question_lower for keyword in ['curious', 'wonder', 'interested', 'fascinated']):
            return 'engaging'
        elif len(question.split()) < 10:
            return 'concise'
        else:
            return 'balanced'

class LunaPersonalityOptimizer:
    """Personality optimization system for Luna responses."""
    
    def __init__(self):
        self.personality_weights = {
            'openness': 0.8,
            'conscientiousness': 0.7,
            'extraversion': 0.6,
            'agreeableness': 0.9,
            'neuroticism': 0.3
        }
        self.optimization_history = []
    
    def optimize_personality_expression(self, response: str, trait: str, context: Dict) -> str:
        """Optimize personality expression in response."""
        optimized_response = response
        
        # Apply trait-specific optimizations
        if trait == 'openness':
            optimized_response = self._enhance_openness(optimized_response)
        elif trait == 'conscientiousness':
            optimized_response = self._enhance_conscientiousness(optimized_response)
        elif trait == 'extraversion':
            optimized_response = self._enhance_extraversion(optimized_response)
        elif trait == 'agreeableness':
            optimized_response = self._enhance_agreeableness(optimized_response)
        elif trait == 'neuroticism':
            optimized_response = self._enhance_neuroticism(optimized_response)
        
        # Apply general personality optimizations
        optimized_response = self._apply_general_optimizations(optimized_response, context)
        
        return optimized_response
    
    def _enhance_openness(self, response: str) -> str:
        """Enhance openness traits in response."""
        if 'creative' not in response.lower() and 'imagine' not in response.lower():
            return f"Let me think creatively about this. {response}"
        return response
    
    def _enhance_conscientiousness(self, response: str) -> str:
        """Enhance conscientiousness traits in response."""
        if not any(word in response.lower() for word in ['systematic', 'organized', 'methodical']):
            return f"Let me approach this systematically. {response}"
        return response
    
    def _enhance_extraversion(self, response: str) -> str:
        """Enhance extraversion traits in response."""
        if not response.startswith(('I', 'We', 'Let')):
            return f"I think {response.lower()}"
        return response
    
    def _enhance_agreeableness(self, response: str) -> str:
        """Enhance agreeableness traits in response."""
        if not any(word in response.lower() for word in ['appreciate', 'understand', 'respect']):
            return f"I appreciate your perspective. {response}"
        return response
    
    def _enhance_neuroticism(self, response: str) -> str:
        """Enhance neuroticism traits in response."""
        if not any(word in response.lower() for word in ['concern', 'worry', 'anxiety']):
            return f"I understand your concern. {response}"
        return response
    
    def _apply_general_optimizations(self, response: str, context: Dict) -> str:
        """Apply general personality optimizations."""
        # Add emotional intelligence
        if context.get('emotional_tone') == 'negative' and 'understand' not in response.lower():
            return f"I understand this might be challenging. {response}"
        
        # Add curiosity
        if context.get('question_type') == 'general' and '?' not in response:
            return f"{response} What are your thoughts on this?"
        
        return response

if __name__ == "__main__":
    main()

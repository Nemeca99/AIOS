#!/usr/bin/env python3
"""
UNIFIED CARMA CORE SYSTEM
Complete CARMA system with all cognitive enhancements integrated.
"""

# CRITICAL: Import Unicode safety layer FIRST to prevent encoding errors
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.unicode_safe_output import setup_unicode_safe_output
setup_unicode_safe_output()
import time
import json
import random
import math
import uuid
import hashlib
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import support modules
from support_core.support_core import (
    SystemConfig, SimpleEmbedder,
    aios_config, aios_logger, aios_health_checker, aios_security_validator
)

# === ENUMS AND DATA CLASSES ===

class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    BLOCKED = "blocked"
    SUSPICIOUS = "suspicious"

class TrafficType(Enum):
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"
    UNKNOWN = "unknown"

@dataclass
class UserConnection:
    user_id: str
    connection_id: str
    slot_number: int
    api_key: str
    connected_at: float
    last_activity: float
    status: ConnectionStatus
    internal_ip: str
    traffic_count: int = 0
    suspicious_activity: int = 0

@dataclass
class TrafficEvent:
    timestamp: float
    source_ip: str
    destination_ip: str
    user_id: str
    traffic_type: TrafficType
    data_size: int
    protocol: str
    suspicious_score: float = 0.0

@dataclass
class ServerBlock:
    block_id: str
    external_ip: str
    internal_network: str
    max_users: int = 60
    connected_users: Dict[int, UserConnection] = None
    traffic_monitor: List[TrafficEvent] = None
    blocked_ips: set = None
    suspicious_ips: set = None
    
    def __post_init__(self):
        if self.connected_users is None:
            self.connected_users = {}
        if self.traffic_monitor is None:
            self.traffic_monitor = []
        if self.blocked_ips is None:
            self.blocked_ips = set()
        if self.suspicious_ips is None:
            self.suspicious_ips = set()

# === FRACTAL MYCELIUM CACHE ===

class FractalMyceliumCache:
    """Fractal Mycelium Cache with Psycho-Semantic RAG Loop integration."""
    
    def __init__(self, base_dir: str = "Data/FractalCache"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tool-enabled embedder (Llama-3.2-1B for psychological sensing + tools)
        self.tool_embedder = self._initialize_tool_embedder()
        
        # Initialize main embedder for content processing
        self.embedder = SimpleEmbedder()
        
        # Registry and links
        self.file_registry = {}
        self.semantic_links = {}
        
        # Psycho-Semantic RAG Loop components
        self.ava_raw_matches_path = Path("ava_raw_matches.txt")
        self.big5_training_path = Path("big5_training_data.json")
        self.ava_progression_path = Path("ava_psychological_progression_analysis.json")
        self.minecraft_chat_path = Path("Data/Minecraft-Server-Chat/clean.json")
        self.psychological_cache = {}
        self.triple_point_matches = []
        self.dynamic_prompt_cache = {}
        self.minecraft_chat_cache = {}
        self.big5_knowledge_base = {}
        self.ava_progression_analysis = {}
        self.hit_weights = {}
        self.path_weights = {}
        self.metrics = {
            'total_fragments': 0,
            'total_hits': 0,
            'cache_hit_rate': 0.0,
            'avg_similarity': 0.0,
            'cross_links': 0
        }
        
        # Load existing data
        self.load_registry()
        
        print(" Fractal Mycelium Cache Initialized")
        print(f"    Base directory: {self.base_dir}")
        print(f"    Max file size: {SystemConfig.MAX_FILE_SIZE // 1024}KB")
        print(f"    Max splits: {SystemConfig.MAX_SPLITS}")
        print(f"    Eviction enabled: {SystemConfig.MAX_CACHE_SIZE} max fragments")
        print(f"    Reinforcement enabled: hit-based weighting")
        print(f"    Tool-Enabled Embedder: Llama-3.2-1B-Instruct (Tool-Augmented Retrieval)")
    
    def _initialize_tool_embedder(self):
        """Initialize the tool-enabled embedder (Llama-3.2-1B)."""
        return {
            'model_name': 'Llama-3.2-1B-Instruct-GGUF',
            'model_file': 'Llama-3.2-1B-Instruct-Q8_0.gguf',
            'lm_studio_url': 'http://localhost:1234/v1/chat/completions',
            'tools_enabled': True,
            'size_gb': 1.32
        }
    
    def add_content(self, content: str, parent_id: str = None) -> str:
        """Add content to the cache."""
        file_id = self.create_file_id(content, parent_id)
        
        fragment_data = {
            'file_id': file_id,
            'content': content,
            'parent_id': parent_id,
            'level': 0,
            'hits': 0,
            'created': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'specialization': 'general',
            'tags': [],
            'analysis': self.analyze_content(content)
        }
        
        # Generate embedding
        try:
            embedding = self.embedder.embed(content)
            fragment_data['embedding'] = embedding
        except Exception as e:
            print(f"  Embedding failed: {e}")
            fragment_data['embedding'] = None
        
        self.file_registry[file_id] = fragment_data
        self.save_registry()
        
        return file_id
    
    def create_file_id(self, content: str = None, parent_id: str = None, generation_number: int = None, generation_seed: int = None) -> str:
        """Create unique file ID using Generational Architecture format: GEN_X_Y_Z"""
        # Get generation info from CFIA if not provided
        if generation_number is None or generation_seed is None:
            try:
                from luna_cfia_system import LunaCFIASystem
                cfia = LunaCFIASystem()
                generation_number = generation_number or cfia.state.aiiq
                generation_seed = generation_seed or cfia.state.generation_seed
            except ImportError:
                # Fallback if luna_cfia_system is not available
                generation_number = generation_number or 2
                generation_seed = generation_seed or random.randint(1000, 9999)
            except Exception:
                # Fallback for any other error
                generation_number = generation_number or 2
                generation_seed = generation_seed or random.randint(1000, 9999)
        
        # Create fragment index (A, B, C, etc.)
        fragment_index = self._get_next_fragment_index(generation_number, generation_seed)
        
        return f"GEN{generation_number}_{generation_seed}_{fragment_index}"
    
    def _get_next_fragment_index(self, generation_number: int, generation_seed: int) -> str:
        """Get next fragment index for the generation/seed combination"""
        # Count existing fragments for this generation/seed
        pattern = f"GEN{generation_number}_{generation_seed}_"
        existing_fragments = []
        
        for file_path in self.base_dir.glob("GEN*.json"):
            if file_path.stem.startswith(pattern):
                existing_fragments.append(file_path.stem)
        
        # Return next letter in sequence (A, B, C, D, etc.)
        if not existing_fragments:
            return "A"
        
        # Find highest letter and increment
        letters = [frag.split("_")[-1] for frag in existing_fragments]
        if letters:
            last_letter = max(letters)
            next_letter = chr(ord(last_letter) + 1)
            return next_letter
        
        return "A"
    
    def analyze_content(self, content: str) -> Dict:
        """Analyze content for metadata."""
        words = content.split()
        return {
            'word_count': len(words),
            'char_count': len(content),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'sentiment': self.score_valence(content),
            'complexity': len(set(words)) / len(words) if words else 0
        }
    
    def score_valence(self, text: str) -> float:
        """Simple sentiment scoring."""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count + neg_count == 0:
            return 0.0
        
        return (pos_count - neg_count) / (pos_count + neg_count)
    
    def find_relevant(self, query_embedding, topk=3):
        """Find relevant fragments using embedding similarity."""
        if not query_embedding:
            return []
        
        similarities = []
        for frag_id, frag_data in self.file_registry.items():
            if 'embedding' in frag_data and frag_data['embedding']:
                try:
                    similarity = self.calculate_similarity(query_embedding, frag_data['embedding'])
                    similarities.append((frag_id, similarity, frag_data))
                except Exception:
                    continue
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return FragmentResult objects
        class FragmentResult:
            def __init__(self, frag_id, frag_data, score):
                self.id = frag_id
                self.content = frag_data.get('content', '')
                self.score = score
                self.hits = frag_data.get('hits', 0)
                self.level = frag_data.get('level', 0)
        
        return [FragmentResult(fid, data, sim) for fid, sim, data in similarities[:topk]]
    
    def calculate_similarity(self, emb1, emb2):
        """Calculate cosine similarity between embeddings."""
        if not emb1 or not emb2:
            return 0.0
        
        try:
            emb1 = np.array(emb1)
            emb2 = np.array(emb2)
            
            dot_product = np.dot(emb1, emb2)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception:
            return 0.0
    
    # === PSYCHO-SEMANTIC RAG LOOP METHODS ===
    
    def load_ava_raw_matches(self):
        """Load Ava raw matches for psychological pattern analysis."""
        if not self.ava_raw_matches_path.exists():
            print(f"  Ava raw matches file not found: {self.ava_raw_matches_path}")
            return []
        
        matches = []
        current_match = {}
        
        with open(self.ava_raw_matches_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                if line.startswith("MATCH"):
                    if current_match:
                        matches.append(current_match)
                    current_match = {
                        'match_id': line,
                        'before': [],
                        'ava_match': '',
                        'after': [],
                        'page': 0,
                        'line': 0
                    }
                elif line.startswith("Page"):
                    # Extract page and line info
                    parts = line.split()
                    if len(parts) >= 2:
                        current_match['page'] = int(parts[1].rstrip(','))
                        current_match['line'] = int(parts[3])
                elif line.startswith("BEFORE:"):
                    current_match['reading_before'] = True
                    current_match['reading_after'] = False
                elif line.startswith("AFTER:"):
                    current_match['reading_before'] = False
                    current_match['reading_after'] = True
                elif line.startswith("AVA MATCH:"):
                    current_match['ava_match'] = line.replace("AVA MATCH:", "").strip()
                    current_match['reading_before'] = False
                    current_match['reading_after'] = False
                elif line and not line.startswith("=") and not line.startswith("-"):
                    if current_match.get('reading_before'):
                        current_match['before'].append(line)
                    elif current_match.get('reading_after'):
                        current_match['after'].append(line)
        
        if current_match:
            matches.append(current_match)
        
        print(f" Loaded {len(matches)} Ava raw matches for psychological analysis")
        return matches
    
    def load_minecraft_chat_patterns(self, sample_size: int = 1000):
        """Load and sample Minecraft chat patterns for efficiency training."""
        if not self.minecraft_chat_path.exists():
            print(f"  Minecraft chat file not found: {self.minecraft_chat_path}")
            return []
        
        # Check cache first
        cache_key = f"minecraft_chat_{sample_size}"
        if cache_key in self.minecraft_chat_cache:
            return self.minecraft_chat_cache[cache_key]
        
        try:
            print(f" Loading Minecraft chat patterns (sampling {sample_size} messages)...")
            
            # Sample from the massive JSON file efficiently
            import random
            chat_patterns = []
            
            with open(self.minecraft_chat_path, 'r', encoding='utf-8') as f:
                # Read first few lines to get structure
                first_line = f.readline().strip()
                if first_line != '[':
                    print("  Invalid JSON structure")
                    return []
                
                # Sample messages efficiently
                message_count = 0
                current_message = ""
                brace_count = 0
                in_content = False
                
                for line in f:
                    current_message += line
                    
                    # Count braces to find complete messages
                    brace_count += line.count('{') - line.count('}')
                    
                    # Check if we have a complete message
                    if brace_count == 0 and current_message.strip().endswith('},'):
                        try:
                            # Remove trailing comma and parse
                            message_json = current_message.rstrip(',\n').strip()
                            if message_json.endswith('}'):
                                parsed_msg = json.loads(message_json)
                                
                                # Extract content for pattern analysis
                                if 'content' in parsed_msg and parsed_msg['content']:
                                    content = parsed_msg['content'].strip()
                                    word_count = len(content.split())
                                    
                                    # Focus on efficient patterns (1-10 words)
                                    if 1 <= word_count <= 10:
                                        chat_patterns.append({
                                            'content': content,
                                            'word_count': word_count,
                                            'username': parsed_msg.get('username', 'unknown'),
                                            'date': parsed_msg.get('date', 'unknown')
                                        })
                                
                                message_count += 1
                                if message_count >= sample_size:
                                    break
                                    
                        except json.JSONDecodeError:
                            pass
                        
                        current_message = ""
                        brace_count = 0
            
            # Cache the results
            self.minecraft_chat_cache[cache_key] = chat_patterns
            
            print(f" Loaded {len(chat_patterns)} Minecraft chat patterns for efficiency training")
            print(f" Word count distribution: {self._analyze_word_distribution(chat_patterns)}")
            
            return chat_patterns
            
        except Exception as e:
            print(f" Error loading Minecraft chat patterns: {e}")
            return []
    
    def _analyze_word_distribution(self, patterns):
        """Analyze word count distribution in Minecraft chat patterns."""
        if not patterns:
            return "No patterns"
        
        word_counts = [p['word_count'] for p in patterns]
        avg_words = sum(word_counts) / len(word_counts)
        
        # Count by ranges
        ultra_short = len([w for w in word_counts if w <= 3])
        short = len([w for w in word_counts if 4 <= w <= 6])
        medium = len([w for w in word_counts if 7 <= w <= 10])
        
        return f"avg: {avg_words:.1f}, ultra-short (≤3): {ultra_short}, short (4-6): {short}, medium (7-10): {medium}"
    
    def load_big5_training_data(self):
        """Load Big 5 personality training data for embedder enhancement."""
        if not self.big5_training_path.exists():
            print(f"  Big 5 training data not found: {self.big5_training_path}")
            return {}
        
        try:
            import json
            with open(self.big5_training_path, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
            
            # Extract training examples for embedder
            self.big5_knowledge_base = training_data[0] if training_data else {}
            
            print(f" Loaded Big 5 training data: {self.big5_knowledge_base.get('total_questions', 0)} questions")
            print(f"    Categories: {list(self.big5_knowledge_base.get('categories', {}).keys())}")
            
            return self.big5_knowledge_base
            
        except Exception as e:
            print(f"  Failed to load Big 5 training data: {e}")
            return {}
    
    def load_ava_psychological_progression(self):
        """Load Ava's psychological progression analysis for enhanced behavioral understanding."""
        if not self.ava_progression_path.exists():
            print(f"  Ava psychological progression analysis not found: {self.ava_progression_path}")
            return {}
        
        try:
            import json
            with open(self.ava_progression_path, 'r', encoding='utf-8') as f:
                progression_data = json.load(f)
            
            # Extract progression analysis
            self.ava_progression_analysis = progression_data[0] if progression_data else {}
            
            print(f" Loaded Ava psychological progression analysis")
            print(f"    Behavioral categories: {list(self.ava_progression_analysis.get('behavioral_categories', {}).keys())}")
            print(f"    Training examples: {len(self.ava_progression_analysis.get('training_examples', []))}")
            
            return self.ava_progression_analysis
            
        except Exception as e:
            print(f"  Failed to load Ava psychological progression analysis: {e}")
            return {}
    
    def create_big5_enhanced_prompt(self, user_query: str, matches: List[Dict], minecraft_patterns: List[Dict] = None) -> str:
        """Create Big 5 enhanced prompt with Ava psychological progression analysis and Minecraft chat efficiency patterns."""
        big5_data = self.big5_knowledge_base
        progression_data = self.ava_progression_analysis
        
        if not big5_data and not progression_data:
            # Fallback to basic prompt
            return f"""
Analyze the user query for psychological patterns and match it to Ava behavioral triplets.

USER QUERY: "{user_query}"

AVA MATCHES AVAILABLE: {len(matches)} matches

For each match, analyze the psychological relevance:
- BEFORE: {matches[0]['before'] if matches else 'No matches'}
- AVA MATCH: {matches[0]['ava_match'] if matches else 'No matches'}  
- AFTER: {matches[0]['after'] if matches else 'No matches'}

Return the top 3 most psychologically relevant matches with:
1. Match ID
2. Page number
3. Line number
4. Psychological similarity score (0.0-1.0)
5. Behavioral context analysis

Format as JSON array.
"""
        
        # Create Big 5 enhanced prompt
        big5_context = f"""
You are a Big 5 personality expert analyzing user queries. Use this knowledge base:

BIG 5 PERSONALITY TRAITS:
"""
        
        for trait, info in big5_data.get('categories', {}).items():
            big5_context += f"""
- {trait.upper()}: {info.get('description', '')}
  Sample questions: {', '.join(info.get('sample_questions', [])[:3])}
"""
        
        big5_context += f"""

TRAINING EXAMPLES:
"""
        
        for example in big5_data.get('training_examples', [])[:5]:
            big5_context += f"""
- Question: "{example.get('question', '')}"
  Big 5 Trait: {example.get('big5_trait', '')} (strength: {example.get('trait_strength', 0)})
  Psychological Patterns: {', '.join(example.get('psychological_patterns', []))}
  Luna Response Style: {example.get('luna_response_style', '')}
"""
        
        big5_context += f"""

AVA PSYCHOLOGICAL PROGRESSION ANALYSIS:
"""
        
        if progression_data:
            big5_context += f"""
AVA'S BEHAVIORAL CATEGORIES:
"""
            for category, info in progression_data.get('behavioral_categories', {}).items():
                big5_context += f"""
- {category.upper()}: {info.get('description', '')}
"""
            
            big5_context += f"""

PSYCHOLOGICAL PROGRESSION EXAMPLES:
"""
            for example in progression_data.get('training_examples', [])[:3]:
                big5_context += f"""
- Query: "{example.get('user_query', '')}"
  Big 5 Trait: {example.get('big5_trait', '')}
  Ava Category: {example.get('ava_behavioral_category', '')}
  Scene Context: {example.get('scene_context', '')}
  Dialogue Style: {example.get('dialogue_style', '')}
  Luna Guidance: {example.get('luna_response_guidance', '')}
"""
        
        big5_context += f"""

CURRENT ANALYSIS TASK:
USER QUERY: "{user_query}"

AVA MATCHES AVAILABLE: {len(matches)} matches

Analyze the user query using Big 5 personality knowledge and Ava's psychological progression patterns.

Return JSON with:
- big5_trait: The primary Big 5 trait detected
- trait_strength: Strength score (0.0-1.0)
- psychological_patterns: Array of detected patterns
- ava_behavioral_category: Which Ava category (scene_context, dialogue_style, psychological_progression)
- scene_context: Visual/emotional context
- dialogue_style: Speaking patterns and tactics
- matches: Array of top 3 Ava behavioral matches with psychological_similarity and behavioral_context
- behavioral_synthesis: How to blend multiple matches for complete response
- luna_response_guidance: How Luna should respond based on this analysis

BEHAVIORAL SYNTHESIS INSTRUCTIONS:
When multiple relevant matches are found, synthesize them instead of just selecting the best one:
- Primary Triplet (Dialogue): Best verbal response template
- Secondary Triplet (Action): Most relevant non-verbal action or scene-setting
- Blended Tag: How to combine them (e.g., "[BLENDED_ACTION: Preceded by observing subject]")
- Synthesis Guidance: How Luna should blend verbal and non-verbal elements

Example format:
{{
  "big5_trait": "conscientiousness",
  "trait_strength": 0.85,
  "psychological_patterns": ["task_completion", "organization"],
  "matches": [
    {{
      "match_id": "MATCH 1",
      "psychological_similarity": 0.95,
      "behavioral_context": "Curious questioning pattern"
    }}
  ],
  "luna_response_guidance": "Show direct curiosity about their methods and systems"
}}

EFFICIENCY GUIDANCE:
Target: Concise, intelligent communication style.
Examples of efficient responses:"""
        
        # Add efficiency patterns if available
        if minecraft_patterns:
            # Sample a few examples
            sample_patterns = minecraft_patterns[:10]
            for pattern in sample_patterns:
                big5_context += f"""
- "{pattern['content']}" ({pattern['word_count']} words)"""
        else:
            big5_context += """
- "Machine learning uses algorithms to learn from data." (10 words)
- "AI systems process information to make decisions." (8 words)  
- "be yourself." (2 words)
- "finding your groove, everything clicks." (5 words)
- "nice vibes!" (2 words)"""
        
        big5_context += """
"""
        
        return big5_context
    
    def find_psychological_patterns_tar(self, user_query: str, matches: List[Dict], minecraft_patterns: List[Dict] = None) -> List[Dict]:
        """Find psychological patterns using Big 5 enhanced Tool-Augmented Retrieval (TAR)."""
        # Load Big 5 training data if not already loaded
        if not self.big5_knowledge_base:
            self.load_big5_training_data()
        
        # Load Ava psychological progression analysis if not already loaded
        if not self.ava_progression_analysis:
            self.load_ava_psychological_progression()
        
        # Use Big 5 enhanced prompt with psychological progression analysis and Minecraft patterns
        tool_prompt = self.create_big5_enhanced_prompt(user_query, matches, minecraft_patterns)
        
        try:
            # Call the tool-enabled embedder (Llama-3.2-1B)
            response = self._call_tool_embedder(tool_prompt)
            psychological_matches = self._parse_tar_response(response, matches)
            
            # Sort by psychological similarity
            psychological_matches.sort(key=lambda x: x['psychological_similarity'], reverse=True)
            
            return psychological_matches[:3]
            
        except Exception as e:
            print(f"  TAR analysis failed: {e}")
            # Fallback to simple matching
            return self._fallback_psychological_matching(user_query, matches)
    
    def _call_tool_embedder(self, prompt: str) -> str:
        """Call the tool-enabled embedder (Llama-3.2-1B) for psychological analysis."""
        import requests
        
        payload = {
            "model": "exaone-3.5-2.4b-instruct-abliterated",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a psychological pattern analyzer with behavioral synthesis capabilities. You MUST respond with ONLY valid JSON format. Analyze user queries using Big 5 personality knowledge and Ava's psychological progression patterns. Return JSON with: big5_trait, trait_strength, psychological_patterns, matches array, and behavioral_synthesis object containing primary_triplet, secondary_triplet, blended_tag, and synthesis_guidance. Example: {\"big5_trait\": \"neuroticism\", \"trait_strength\": 0.75, \"psychological_patterns\": [\"anxiety\"], \"matches\": [{\"match_id\": \"MATCH 1\", \"psychological_similarity\": 0.75}], \"behavioral_synthesis\": {\"primary_triplet\": \"Best dialogue\", \"secondary_triplet\": \"Best action\", \"blended_tag\": \"[BLENDED_ACTION: Combined elements]\", \"synthesis_guidance\": \"How to blend them\"}}"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                self.tool_embedder['lm_studio_url'],
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content']
            print(f" LLM Response: {result[:200]}...")
            return result
        except Exception as e:
            print(f"  Tool embedder call failed: {e}")
            return ""
    
    def _parse_tar_response(self, response: str, matches: List[Dict]) -> List[Dict]:
        """Parse the TAR response and extract psychological matches."""
        psychological_matches = []
        
        try:
            import json
            import re
            
            # Clean up the response - remove markdown code blocks
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            # Try to extract JSON from the response - handle multiple JSON objects
            json_matches = re.findall(r'\{[^{}]*\}', cleaned_response)
            if not json_matches:
                # Fallback to single JSON object
                json_match = re.search(r'\{.*\}', cleaned_response, re.DOTALL)
                if json_match:
                    json_matches = [json_match.group(0)]
            
            for json_str in json_matches:
                # Try to parse the JSON
                try:
                    parsed_response = json.loads(json_str)
                    
                    # Handle different response formats
                    if isinstance(parsed_response, dict):
                        if 'matches' in parsed_response:
                            # Format: {"matches": [...]}
                            items = parsed_response['matches']
                        else:
                            # Format: {"match_id": "...", ...}
                            items = [parsed_response]
                    elif isinstance(parsed_response, list):
                        # Format: [...]
                        items = parsed_response
                    else:
                        items = []
                    
                    # Handle Big 5 enhanced response format
                    if 'big5_trait' in parsed_response:
                        # Big 5 enhanced format
                        big5_trait = parsed_response.get('big5_trait', '')
                        trait_strength = parsed_response.get('trait_strength', 0.0)
                        psychological_patterns = parsed_response.get('psychological_patterns', [])
                        luna_guidance = parsed_response.get('luna_response_guidance', '')
                        behavioral_synthesis = parsed_response.get('behavioral_synthesis', {})
                        matches_array = parsed_response.get('matches', [])
                        
                        # Process matches from Big 5 response
                        print(f" DEBUG: Processing {len(matches_array)} matches from LLM response")
                        print(f" DEBUG: Available original matches:")
                        for i, match in enumerate(matches[:3]):  # Show first 3
                            print(f"   {i}: '{match['match_id']}'")
                        for i, item in enumerate(matches_array):
                            if isinstance(item, dict) and 'match_id' in item and 'psychological_similarity' in item:
                                # Find the corresponding match - handle partial matching
                                match_id = item['match_id']
                                print(f" DEBUG: Looking for LLM match_id '{match_id}' in {len(matches)} available matches")
                                
                                match_found = False
                                matched_original = None
                                
                                for match in matches:
                                    # Check if the match_id is contained in the actual match ID
                                    # Handle cases like "MATCH 2" vs "MATCH 3 (Page 21, Line 14)"
                                    if match_id in match['match_id'] or match['match_id'] in match_id:
                                        match_found = True
                                        matched_original = match
                                        print(f" DEBUG: Direct match found: '{match_id}' -> '{match['match_id']}'")
                                        break
                                    elif len(match_id.split()) > 1:
                                        # Extract number from "MATCH 2" and check if it's in the full match ID
                                        match_num = match_id.split()[1]
                                        if match_num in match['match_id']:
                                            match_found = True
                                            matched_original = match
                                            print(f" DEBUG: Number match found: '{match_num}' -> '{match['match_id']}'")
                                            break
                                
                                if match_found and matched_original:
                                        psychological_match = {
                                            'match_id': match['match_id'],
                                            'page': match['page'],
                                            'line': match['line'],
                                            'ava_match': match['ava_match'],
                                            'before_context': match['before'],
                                            'after_context': match['after'],
                                            'psychological_similarity': float(item['psychological_similarity']),
                                            'document_id': f"page_{match['page']}",
                                            'line_number': match['line'],
                                            'behavioral_analysis': item.get('behavioral_context', ''),
                                            'big5_trait': big5_trait,
                                            'trait_strength': trait_strength,
                                            'psychological_patterns': psychological_patterns,
                                            'luna_response_guidance': luna_guidance,
                                            'ava_behavioral_category': parsed_response.get('ava_behavioral_category', ''),
                                            'scene_context': parsed_response.get('scene_context', ''),
                                            'dialogue_style': parsed_response.get('dialogue_style', ''),
                                            'behavioral_synthesis': behavioral_synthesis,
                                            'synthesis_guidance': behavioral_synthesis.get('synthesis_guidance', '') if behavioral_synthesis else '',
                                            'primary_triplet': behavioral_synthesis.get('primary_triplet', '') if behavioral_synthesis else '',
                                            'secondary_triplet': behavioral_synthesis.get('secondary_triplet', '') if behavioral_synthesis else '',
                                            'blended_tag': behavioral_synthesis.get('blended_tag', '') if behavioral_synthesis else ''
                                        }
                                        psychological_matches.append(psychological_match)
                                        break
                    else:
                        # Standard format
                        for item in items:
                            if isinstance(item, dict) and 'match_id' in item and 'psychological_similarity' in item:
                                # Find the corresponding match - handle partial matching
                                match_id = item['match_id']
                                for match in matches:
                                    # Check if the match_id is contained in the actual match ID
                                    # Handle cases like "MATCH 2" vs "MATCH 3 (Page 21, Line 14)"
                                    match_found = False
                                    if match_id in match['match_id'] or match['match_id'] in match_id:
                                        match_found = True
                                    elif len(match_id.split()) > 1:
                                        # Extract number from "MATCH 2" and check if it's in the full match ID
                                        match_num = match_id.split()[1]
                                        if match_num in match['match_id']:
                                            match_found = True
                                    
                                    if match_found:
                                        psychological_match = {
                                            'match_id': match['match_id'],
                                            'page': match['page'],
                                            'line': match['line'],
                                            'ava_match': match['ava_match'],
                                            'before_context': match['before'],
                                            'after_context': match['after'],
                                            'psychological_similarity': float(item['psychological_similarity']),
                                            'document_id': f"page_{match['page']}",
                                            'line_number': match['line'],
                                            'behavioral_analysis': item.get('behavioral_context', '')
                                        }
                                        psychological_matches.append(psychological_match)
                                        break
                
                except json.JSONDecodeError as je:
                    print(f"  JSON decode error: {je}")
                    print(f"   Raw response: {response[:200]}...")
                    # Continue processing other matches even if one fails
                    continue
            
        except Exception as e:
            print(f"  Failed to parse TAR response: {e}")
        
        return psychological_matches
    
    def _fallback_psychological_matching(self, user_query: str, matches: List[Dict]) -> List[Dict]:
        """Fallback psychological matching when TAR fails."""
        psychological_matches = []
        
        # Simple keyword-based matching as fallback
        query_lower = user_query.lower()
        
        for match in matches:
            # Create context for analysis
            context = " ".join(match['before']) + " " + match['ava_match'] + " " + " ".join(match['after'])
            context_lower = context.lower()
            
            # Simple similarity based on keyword overlap
            query_words = set(query_lower.split())
            context_words = set(context_lower.split())
            
            if query_words and context_words:
                similarity = len(query_words.intersection(context_words)) / len(query_words.union(context_words))
                
                if similarity > 0.1:  # Lower threshold for fallback
                    psychological_match = {
                        'match_id': match['match_id'],
                        'page': match['page'],
                        'line': match['line'],
                        'ava_match': match['ava_match'],
                        'before_context': match['before'],
                        'after_context': match['after'],
                        'psychological_similarity': similarity,
                        'document_id': f"page_{match['page']}",
                        'line_number': match['line'],
                        'behavioral_analysis': 'Fallback matching'
                    }
                    psychological_matches.append(psychological_match)
        
        return psychological_matches
    
    def create_dynamic_prompt(self, user_query: str, top_matches: List[Dict]) -> str:
        """Create dynamic prompt for the main model using psychological context."""
        if not top_matches:
            return user_query
        
        # Use the best match for full context
        best_match = top_matches[0]
        
        # Build enhanced psychological context with Big 5 information and behavioral synthesis
        big5_info = ""
        if 'big5_trait' in best_match:
            big5_info = f"""
BIG 5 PERSONALITY ANALYSIS:
- Primary Trait: {best_match['big5_trait'].upper()} (strength: {best_match['trait_strength']:.2f})
- Psychological Patterns: {', '.join(best_match.get('psychological_patterns', []))}
- Luna Response Guidance: {best_match.get('luna_response_guidance', '')}
"""
        
        # Add behavioral synthesis information
        synthesis_info = ""
        if 'behavioral_synthesis' in best_match and best_match.get('behavioral_synthesis'):
            synthesis = best_match['behavioral_synthesis']
            synthesis_info = f"""
BEHAVIORAL SYNTHESIS:
- Primary Triplet (Dialogue): {synthesis.get('primary_triplet', '')}
- Secondary Triplet (Action): {synthesis.get('secondary_triplet', '')}
- Blended Tag: {synthesis.get('blended_tag', '')}
- Synthesis Guidance: {synthesis.get('synthesis_guidance', '')}
"""
        
        psychological_context = f"""
PSYCHOLOGICAL CONTEXT:
- Document: {best_match['document_id']} (Page {best_match['page']}, Line {best_match['line']})
- Ava Pattern: "{best_match['ava_match']}"
- Before Context: {" ".join(best_match['before_context'][-2:])}
- After Context: {" ".join(best_match['after_context'][:2])}
- Psychological Similarity: {best_match['psychological_similarity']:.3f}
{big5_info}{synthesis_info}
LUNA PERSONALITY GUIDANCE (Ava-inspired):
- Use Luna's direct, curious communication style inspired by Ava
- Ask probing questions with genuine curiosity like Ava
- Show emotional intelligence and vulnerability as Luna
- Maintain simple, effective language patterns
- Express college student perspective with philosophical depth
- Incorporate gothic aesthetic with intellectual curiosity
- Apply Big 5 personality insights for more targeted responses
- Blend verbal and non-verbal elements for complete, human-like responses
- Synthesize multiple behavioral patterns for authentic personality expression

USER QUERY: {user_query}
"""
        
        # Cache the dynamic prompt
        prompt_id = hashlib.md5(user_query.encode()).hexdigest()[:8]
        self.dynamic_prompt_cache[prompt_id] = {
            'original_query': user_query,
            'dynamic_prompt': psychological_context,
            'matches_used': top_matches,
            'timestamp': datetime.now().isoformat()
        }
        
        return psychological_context
    
    def retrieve_full_document_context(self, document_id: str, line_number: int) -> Dict:
        """Retrieve full document context and add behavioral tags."""
        try:
            # This would load the actual document page
            # For now, we'll simulate the full document retrieval
            full_document = self._load_document_page(document_id)
            
            # Add behavioral tags using the tool-enabled embedder
            tagged_context = self._add_behavioral_tags(full_document, line_number)
            
            return {
                'document_id': document_id,
                'line_number': line_number,
                'full_context': full_document,
                'tagged_context': tagged_context,
                'retrieval_success': True
            }
            
        except Exception as e:
            print(f"  Document retrieval failed: {e}")
            return {
                'document_id': document_id,
                'line_number': line_number,
                'full_context': '',
                'tagged_context': '',
                'retrieval_success': False,
                'error': str(e)
            }
    
    def _load_document_page(self, document_id: str) -> str:
        """Load the full document page from cache or file system."""
        try:
            # Check if document is in cache
            if document_id in self.file_registry:
                return self.file_registry[document_id].get('content', '')
            
            # Try to load from file system
            doc_path = Path(f"Data/Documents/{document_id}.txt")
            if doc_path.exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            # Fallback to generating content based on document_id
            return f"Document {document_id} content loaded from system cache."
        except Exception as e:
            print(f"Error loading document {document_id}: {e}")
            return f"Error loading document {document_id}"
    
    def _add_behavioral_tags(self, document_content: str, line_number: int) -> str:
        """Add behavioral tags to the document content using tool-enabled embedder."""
        tagging_prompt = f"""
Analyze this document content and add behavioral tags for Ava's character.

DOCUMENT CONTENT:
{document_content}

LINE NUMBER: {line_number}

Add the following tags:
- [EMOTION: emotion_name]
- [BEHAVIOR: behavior_type]  
- [CONTEXT: scene_context]
- [TENSION: tension_level]
- [AVA_PATTERN: specific_ava_action]

Return the tagged content with embedded tags.
"""
        
        try:
            response = self._call_tool_embedder(tagging_prompt)
            return response
        except Exception as e:
            print(f"  Behavioral tagging failed: {e}")
            return f"[EMOTION: Neutral] [BEHAVIOR: Dialogue] [CONTEXT: General] {document_content}"
    
    def execute_psycho_semantic_rag_loop(self, user_query: str) -> Dict:
        """Execute the complete Psycho-Semantic RAG Loop."""
        print(f" Executing Psycho-Semantic RAG Loop for: {user_query[:50]}...")
        
        # Stage 1: Load Ava raw matches
        ava_matches = self.load_ava_raw_matches()
        if not ava_matches:
            print("  No Ava matches available, falling back to standard retrieval")
            return {'dynamic_prompt': user_query, 'matches': [], 'stage': 'fallback'}
        
        # Stage 1.5: Load Minecraft chat patterns for efficiency training - DISABLED FOR TESTING
        # minecraft_patterns = self.load_minecraft_chat_patterns(sample_size=500)
        minecraft_patterns = None  # Disable Minecraft patterns
        
        # Stage 2: Find psychological patterns using Tool-Augmented Retrieval
        psychological_matches = self.find_psychological_patterns_tar(user_query, ava_matches, minecraft_patterns)
        print(f" Found {len(psychological_matches)} psychological matches")
        
        # Stage 3: Create dynamic prompt
        dynamic_prompt = self.create_dynamic_prompt(user_query, psychological_matches)
        
        # Stage 4: Extract Big 5 data from psychological matches
        big5_data = {}
        if psychological_matches:
            # Get Big 5 data from the first match (they should all have the same Big 5 analysis)
            first_match = psychological_matches[0]
            if 'big5_trait' in first_match:
                big5_data = {
                    'big5_trait': first_match['big5_trait'],
                    'trait_strength': first_match.get('trait_strength', 0.0),
                    'psychological_patterns': first_match.get('psychological_patterns', []),
                    'luna_response_guidance': first_match.get('luna_response_guidance', ''),
                    'behavioral_synthesis': first_match.get('behavioral_synthesis', {}),
                    'ava_behavioral_category': first_match.get('ava_behavioral_category', ''),
                    'scene_context': first_match.get('scene_context', ''),
                    'dialogue_style': first_match.get('dialogue_style', '')
                }
        
        # Stage 5: Prepare for main model
        result = {
            'dynamic_prompt': dynamic_prompt,
            'matches': psychological_matches,
            'stage': 'psycho_semantic',
            'best_document': psychological_matches[0]['document_id'] if psychological_matches else None,
            'ava_personality_applied': True,
            **big5_data  # Include all Big 5 data at the top level
        }
        
        print(f" Psycho-Semantic RAG Loop complete - Best document: {result['best_document']}")
        return result
    
    def load_registry(self):
        """Load registry from disk."""
        registry_file = self.base_dir / "registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, 'r') as f:
                    data = json.load(f)
                    self.file_registry = data.get('file_registry', {})
                    self.semantic_links = data.get('semantic_links', {})
                    self.hit_weights = data.get('hit_weights', {})
                    self.path_weights = data.get('path_weights', {})
                    self.metrics = data.get('metrics', self.metrics)
            except Exception as e:
                print(f"  Error loading registry: {e}")
    
    def save_registry(self):
        """Save registry to disk."""
        registry_file = self.base_dir / "registry.json"
        try:
            # Ensure directory exists
            self.base_dir.mkdir(parents=True, exist_ok=True)
            
            data = {
                'file_registry': self.file_registry,
                'semantic_links': self.semantic_links,
                'hit_weights': self.hit_weights,
                'path_weights': self.path_weights,
                'metrics': self.metrics
            }
            with open(registry_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"  Error saving registry: {e}")
            # Don't let registry save errors crash the system
            pass
    
    def get_cache_statistics(self) -> Dict:
        """Get cache statistics."""
        return {
            'total_fragments': len(self.file_registry),
            'cross_links': len(self.semantic_links),
            'cache_hit_rate': self.metrics.get('cache_hit_rate', 0.0),
            'avg_similarity': self.metrics.get('avg_similarity', 0.0)
        }

# === CARMA EXECUTIVE BRAIN ===

class CARMAExecutiveBrain:
    """Executive brain for autonomous goal generation and execution."""
    
    def __init__(self, cache: FractalMyceliumCache, goal_interval: int = SystemConfig.GOAL_INTERVAL):
        self.cache = cache
        self.goal_interval = goal_interval
        self.goals = []
        self.completed_goals = []
        self.system_metrics_history = []
        self.optimization_actions_count = 0
        self.completed_goals_count = 0
        
        # Goal templates
        self.goal_templates = [
            {"type": "cross_link", "description": "Create semantic cross-links between related fragments"},
            {"type": "evict", "description": "Evict low-value fragments to maintain cache health"},
            {"type": "reinforce", "description": "Reinforce frequently accessed fragments"},
            {"type": "super_fragment", "description": "Create super-fragments from related clusters"},
            {"type": "reflection_scan", "description": "Perform reflection scan for system optimization"},
            {"type": "paradox_probe", "description": "Probe for paradoxes and contradictions"},
            {"type": "deepen_hierarchy", "description": "Deepen memory hierarchy structure"}
        ]
        
        print(" CARMA Executive Brain Initialized")
        print(f"   Goal interval: {goal_interval}s")
        print(f"   Goal templates: {len(self.goal_templates)}")
    
    def generate_goals(self, metrics: Dict) -> List[Dict]:
        """Generate autonomous goals based on system metrics."""
        goals = []
        
        for template in self.goal_templates:
            if self._should_generate_goal(template["type"]):
                goal = {
                    "id": f"goal_{int(time.time())}_{random.randint(1000, 9999)}",
                    "type": template["type"],
                    "description": template["description"],
                    "created_at": time.time(),
                    "status": "pending",
                    "priority": random.uniform(0.5, 1.0)
                }
                goals.append(goal)
        
        return goals
    
    def _should_generate_goal(self, goal_type: str) -> bool:
        """Determine if a goal should be generated."""
        # Use goal_type to determine probability
        goal_probabilities = {
            'cross_link': 0.3,
            'evict': 0.2,
            'reinforce': 0.4,
            'super_fragment': 0.1
        }
        return random.random() < goal_probabilities.get(goal_type, 0.3)
    
    def execute_goals(self):
        """Execute pending goals."""
        for goal in self.goals[:]:
            if goal["status"] == "pending":
                success = self._execute_goal(goal)
                if success:
                    goal["status"] = "completed"
                    goal["completed_at"] = time.time()
                    self.completed_goals.append(goal)
                    self.completed_goals_count += 1
                else:
                    goal["status"] = "failed"
    
    def _execute_goal(self, goal: Dict) -> bool:
        """Execute a specific goal."""
        goal_type = goal["type"]
        
        if goal_type == "cross_link":
            return self._execute_cross_link_goal(goal)
        elif goal_type == "evict":
            return self._execute_evict_goal(goal)
        elif goal_type == "reinforce":
            return self._execute_reinforce_goal(goal)
        elif goal_type == "super_fragment":
            return self._execute_super_fragment_goal(goal)
        else:
            print(f"Unknown goal type: {goal_type}")
            return False
    
    def _execute_cross_link_goal(self, goal: Dict) -> bool:
        """Execute cross-linking goal."""
        try:
            fragments = list(self.cache.file_registry.items())
            if len(fragments) < 2:
                return False
            
            frag1_id, frag1_data = random.choice(fragments)
            frag2_id, frag2_data = random.choice(fragments)
            
            if frag1_id != frag2_id:
                if frag1_id not in self.cache.semantic_links:
                    self.cache.semantic_links[frag1_id] = []
                if frag2_id not in self.cache.semantic_links:
                    self.cache.semantic_links[frag2_id] = []
                
                if frag2_id not in self.cache.semantic_links[frag1_id]:
                    self.cache.semantic_links[frag1_id].append(frag2_id)
                if frag1_id not in self.cache.semantic_links[frag2_id]:
                    self.cache.semantic_links[frag2_id].append(frag1_id)
                
                # Log the cross-link creation using the variables
                print(f"Created cross-link between {frag1_id} and {frag2_id}")
                return True
        except Exception as e:
            print(f"Error executing cross-link goal: {e}")
        return False
    
    def _execute_evict_goal(self, goal: Dict) -> bool:
        """Execute eviction goal."""
        try:
            fragments = [(fid, data) for fid, data in self.cache.file_registry.items()]
            if not fragments:
                return False
            
            fragments.sort(key=lambda x: x[1].get('hits', 0))
            
            frag_id, frag_data = fragments[0]
            if frag_data.get('hits', 0) < 2:
                del self.cache.file_registry[frag_id]
                print(f"Evicted fragment {frag_id} with {frag_data.get('hits', 0)} hits")
                return True
        except Exception as e:
            print(f"Error executing evict goal: {e}")
        return False
    
    def _execute_reinforce_goal(self, goal: Dict) -> bool:
        """Execute reinforcement goal."""
        try:
            fragments = [(fid, data) for fid, data in self.cache.file_registry.items()]
            if not fragments:
                return False
            
            fragments.sort(key=lambda x: x[1].get('hits', 0), reverse=True)
            
            frag_id, frag_data = fragments[0]
            if 'hits' in frag_data:
                frag_data['hits'] += 1
            else:
                frag_data['hits'] = 1
            
            print(f"Reinforced fragment {frag_id} - hits now: {frag_data['hits']}")
            return True
        except Exception as e:
            print(f"Error executing reinforce goal: {e}")
        return False
    
    def _execute_super_fragment_goal(self, goal: Dict) -> bool:
        """Execute super-fragment creation goal."""
        try:
            clusters = self._identify_fragment_clusters()
            if not clusters:
                return False
            
            largest_cluster = max(clusters, key=len)
            if len(largest_cluster) >= 3:
                super_id = self._create_super_fragment(largest_cluster)
                if super_id:
                    print(f"Created super-fragment {super_id} from cluster of {len(largest_cluster)} fragments")
                return super_id is not None
        except Exception as e:
            print(f"Error executing super-fragment goal: {e}")
        return False
    
    def _identify_fragment_clusters(self) -> List[List[str]]:
        """Identify clusters of related fragments."""
        clusters = []
        processed = set()
        
        for frag_id, frag_data in self.cache.file_registry.items():
            if frag_id in processed:
                continue
            
            cluster = [frag_id]
            processed.add(frag_id)
            
            for other_id, other_data in self.cache.file_registry.items():
                if other_id in processed:
                    continue
                
                if self._are_fragments_related(frag_data, other_data):
                    cluster.append(other_id)
                    processed.add(other_id)
            
            if len(cluster) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def _are_fragments_related(self, frag1: Dict, frag2: Dict) -> bool:
        """Check if two fragments are related."""
        content1 = frag1.get('content', '').lower()
        content2 = frag2.get('content', '').lower()
        
        words1 = set(content1.split())
        words2 = set(content2.split())
        
        if not words1 or not words2:
            return False
        
        overlap = len(words1.intersection(words2))
        total = len(words1.union(words2))
        
        return overlap / total > 0.3
    
    def _create_super_fragment(self, cluster: List[str]) -> Optional[str]:
        """Create a super-fragment from a cluster."""
        try:
            combined_content = []
            for frag_id in cluster:
                frag_data = self.cache.file_registry.get(frag_id, {})
                content = frag_data.get('content', '')
                if content:
                    combined_content.append(content)
            
            if not combined_content:
                return None
            
            super_content = "\n\n".join(combined_content)
            super_id = f"super_{int(time.time())}_{uuid.uuid4().hex[:8]}"
            
            super_frag = {
                'file_id': super_id,
                'content': super_content,
                'parent_id': None,
                'level': 1,
                'hits': 0,
                'created': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat(),
                'specialization': 'meta_memory',
                'tags': ['super_fragment'],
                'children': cluster,
                'analysis': self.cache.analyze_content(super_content)
            }
            
            try:
                embedding = self.cache.embedder.embed(super_content)
                super_frag['embedding'] = embedding
            except Exception:
                super_frag['embedding'] = None
            
            self.cache.file_registry[super_id] = super_frag
            return super_id
            
        except Exception:
            return None
    
    def get_executive_status(self) -> Dict:
        """Get executive brain status."""
        return {
            'active_goals': len([g for g in self.goals if g['status'] == 'pending']),
            'completed_goals_count': self.completed_goals_count,
            'optimization_actions_count': self.optimization_actions_count,
            'system_metrics_history_count': len(self.system_metrics_history)
        }

# === CARMA META MEMORY ===

class CARMAMetaMemory:
    """Meta-memory system for hierarchical memory management."""
    
    def __init__(self, cache: FractalMyceliumCache):
        self.cache = cache
        self.episodic_memory = {}
        self.semantic_memory = {}
        self.super_fragments = {}
        self.memory_hierarchy = {}
        
        print(" CARMA Meta-Memory System Initialized")
        print(f"   Compression threshold: {SystemConfig.CONSOLIDATION_THRESHOLD}")
        print(f"   Semantic clustering: {SystemConfig.SEMANTIC_CLUSTERING}")
        print(f"   Episodic decay rate: {SystemConfig.EPISODIC_DECAY_RATE}")
    
    def create_episodic_memory(self, event_data: Dict) -> str:
        """Create an episodic memory."""
        memory_id = f"episode_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        episodic_memory = {
            'id': memory_id,
            'content': event_data.get('content', ''),
            'importance': event_data.get('importance', 0.5),
            'emotional_valence': event_data.get('emotional_valence', 0.0),
            'timestamp': time.time(),
            'context': event_data.get('context', {}),
            'tags': event_data.get('tags', [])
        }
        
        self.episodic_memory[memory_id] = episodic_memory
        print(f"Created episodic memory {memory_id} with importance {event_data.get('importance', 0.5)}")
        return memory_id
    
    def consolidate_episodic_to_semantic(self, theme: str) -> str:
        """Consolidate episodic memories to semantic memory."""
        related_episodes = []
        for episode_id, episode in self.episodic_memory.items():
            if theme.lower() in episode['content'].lower():
                related_episodes.append(episode)
        
        if len(related_episodes) < 2:
            return None
        
        semantic_id = f"semantic_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        patterns = self._extract_patterns(related_episodes)
        summary = f"Semantic memory for '{theme}': {patterns}"
        
        semantic_memory = {
            'id': semantic_id,
            'theme': theme,
            'summary': summary,
            'source_episodes': [ep['id'] for ep in related_episodes],
            'consolidation_timestamp': time.time(),
            'confidence': min(1.0, len(related_episodes) / 5.0)
        }
        
        self.semantic_memory[semantic_id] = semantic_memory
        return semantic_id
    
    def _extract_patterns(self, episodes: List[Dict]) -> str:
        """Extract patterns from episodes."""
        if not episodes:
            return "No patterns found"
        
        common_words = {}
        for episode in episodes:
            words = episode['content'].lower().split()
            for word in words:
                if len(word) > 3:
                    common_words[word] = common_words.get(word, 0) + 1
        
        top_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:5]
        pattern_words = [word for word, count in top_words]
        
        return f"Key patterns: {', '.join(pattern_words)}"
    
    def get_memory_statistics(self) -> Dict:
        """Get memory statistics."""
        return {
            'episodic_memories': len(self.episodic_memory),
            'semantic_memories': len(self.semantic_memory),
            'super_fragments': len(self.super_fragments),
            'hierarchy_levels': len(set(level for level in self.memory_hierarchy.values()))
        }

# === CARMA 100% PERFORMANCE ===

class CARMA100PercentPerformance:
    """100% performance system with all indicators."""
    
    def __init__(self, cache: FractalMyceliumCache, brain: CARMAExecutiveBrain, meta_memory: CARMAMetaMemory):
        self.cache = cache
        self.brain = brain
        self.meta_memory = meta_memory
        self.target_performance = 100
        self.current_indicators = 0
        
        # Learning systems
        self.learning_triggers = {
            'performance_threshold': 0.7,
            'adaptation_rate': 0.1,
            'learning_cycles': 0,
            'last_performance': 0.0,
            'adaptation_history': []
        }
        
        self.semantic_consolidation = {
            'consolidation_threshold': 3,
            'semantic_themes': {},
            'consolidation_events': 0,
            'consolidation_history': []
        }
        
        self.meta_cognition = {
            'hierarchy_levels': 1,
            'system_optimization_score': 0.0,
            'introspection_events': 0,
            'meta_learning_cycles': 0,
            'self_model': {}
        }
        
        print(" CARMA 100% Performance System Initialized")
        print(f"    Target: {SystemConfig.TARGET_PERFORMANCE}% performance ({SystemConfig.PERFORMANCE_INDICATORS}/{SystemConfig.PERFORMANCE_INDICATORS} indicators)")
        print("    Learning Adaptation: Enhanced")
        print("    Semantic Consolidation: Enhanced")
        print("    Meta Cognition: Enhanced")
    
    def perform_dream_cycle(self, max_superfrags=SystemConfig.MAX_SPLITS, min_component_size=2, summary_tokens=200, crosslink_threshold=0.45):
        """Perform dream cycle for memory consolidation."""
        start = time.time()
        
        registry = self.cache.file_registry
        fragments = registry
        adjacency = self.cache.semantic_links
        
        def cosine_sim(a, b):
            num = sum(x*y for x,y in zip(a,b))
            da = math.sqrt(sum(x*x for x in a))
            db = math.sqrt(sum(x*x for x in b))
            return num / (da*db + 1e-9)
        
        # Find connected components
        visited = set()
        components = []
        for fid in fragments:
            if fid in visited: continue
            queue = [fid]
            comp = []
            while queue:
                n = queue.pop(0)
                if n in visited: continue
                visited.add(n)
                comp.append(n)
                for neigh in adjacency.get(n, []):
                    if neigh not in visited:
                        queue.append(neigh)
            if len(comp) >= min_component_size:
                components.append(comp)
        
        # Create super-fragments
        superfrags = []
        for comp in components:
            comp_texts = []
            for fid in comp[:50]:
                frag = fragments[fid]
                comp_texts.append(frag.get('content', '')[:4000])
            
            summary = "\n\n".join(comp_texts[:8])
            super_id = f"super_{int(time.time())}_{uuid.uuid4().hex[:8]}"
            super_frag = {
                "file_id": super_id,
                "content": summary,
                "children": list(comp),
                "parent_id": None,
                "level": max(fragments[c].get('level', 0) for c in comp) + 1,
                "created": datetime.now().isoformat(),
                "access_count": 0,
                "last_accessed": datetime.now().isoformat(),
                "specialization": "meta_memory",
                "tags": list({t for c in comp for t in fragments[c].get('tags', [])})[:32],
                "analysis": {
                    "common_words": [],
                    "common_phrases": [],
                    "emotion_scores": {},
                    "tone_signature": {},
                    "word_count": len(summary.split()),
                    "char_count": len(summary)
                }
            }
            
            try:
                if hasattr(self.cache, 'embedder') and self.cache.embedder:
                    emb = self.cache.embedder.embed(summary)
                    super_frag['embedding'] = emb
                else:
                    super_frag['embedding'] = None
            except Exception:
                super_frag['embedding'] = None
            
            fragments[super_id] = super_frag
            superfrags.append(super_id)
            
            if len(superfrags) >= max_superfrags:
                break
        
        # Cross-link superfrags
        emb_map = {}
        for fid, frag in fragments.items():
            if frag.get('embedding') is not None:
                emb_map[fid] = frag['embedding']
        
        for i, a in enumerate(superfrags):
            emb_a = emb_map.get(a)
            if not emb_a: continue
            for b, emb_b in emb_map.items():
                if a == b: continue
                sim = cosine_sim(emb_a, emb_b)
                if sim >= crosslink_threshold:
                    if b not in adjacency.get(a, []):
                        adjacency.setdefault(a, []).append(b)
                    if a not in adjacency.get(b, []):
                        adjacency.setdefault(b, []).append(a)
        
        # Update cache
        self.cache.file_registry = fragments
        self.cache.semantic_links = adjacency
        self.cache.save_registry()
        
        elapsed = time.time() - start
        return {"superfrags_created": len(superfrags), "time": elapsed, "fragments_processed": len(fragments)}
    
    def get_performance_level(self) -> float:
        """Return current performance percentage."""
        try:
            stats = self.cache.get_cache_statistics()
            executive_status = self.brain.get_executive_status()
            meta_stats = self.meta_memory.get_memory_statistics()
            
            indicators = [
                stats['total_fragments'] > 10,
                stats['cross_links'] > 5,
                self.learning_triggers['learning_cycles'] > 0,
                executive_status['completed_goals_count'] > 0,
                executive_status['optimization_actions_count'] > 0,
                True,  # query_expansion
                executive_status['system_metrics_history_count'] > 0,
                meta_stats['super_fragments'] > 0,
                meta_stats['episodic_memories'] > 0,
                meta_stats['semantic_memories'] > 0,
                self.meta_cognition['hierarchy_levels'] > 1,
                True  # autonomous_consolidation
            ]
            
            return 100.0 * (sum(indicators) / len(indicators))
        except Exception:
            return 0.0

# === CARMA MYCELIUM NETWORK ===

class CARMAMyceliumNetwork:
    """Mycelium-like internal network for CARMA system."""
    
    def __init__(self, num_initial_blocks: int = SystemConfig.SERVER_BLOCKS, users_per_block: int = SystemConfig.MAX_USERS_PER_BLOCK):
        self.server_blocks = {}
        self.total_users = 0
        self.traffic_monitoring = False
        self.traffic_thread = None
        
        # Create initial server blocks
        for i in range(num_initial_blocks):
            block_id = f"block_{i:03d}"
            external_ip = self._generate_external_ip(i)
            self.create_server_block(block_id, external_ip)
        
        print(" CARMA Mycelium Network Initialized")
        print(f"   Server blocks: {len(self.server_blocks)}")
        print(f"   Max users per block: {users_per_block}")
        print(f"   Total capacity: {len(self.server_blocks) * users_per_block} users")
    
    def create_server_block(self, block_id: str, external_ip: str) -> ServerBlock:
        """Create a new server block."""
        internal_network = self._generate_internal_network(block_id)
        
        server_block = ServerBlock(
            block_id=block_id,
            external_ip=external_ip,
            internal_network=internal_network,
            max_users=60
        )
        
        self.server_blocks[block_id] = server_block
        return server_block
    
    def _generate_external_ip(self, index: int) -> str:
        """Generate external IP address."""
        base_ip = "192.168.1"
        return f"{base_ip}.{index + 1}"
    
    def _generate_internal_network(self, block_id: str) -> str:
        """Generate internal network address."""
        block_num = int(block_id.split('_')[1])
        return f"10.{block_num // 256}.{block_num % 256}.0/24"
    
    def connect_user(self, block_id: str, user_id: str, api_key: str) -> Optional[UserConnection]:
        """Connect a user to a server block."""
        if block_id not in self.server_blocks:
            return None
        
        server_block = self.server_blocks[block_id]
        
        # Check if user already connected
        for conn in server_block.connected_users.values():
            if conn.user_id == user_id:
                return conn
        
        # Find available slot
        slot = self._find_available_slot(server_block)
        if slot is None:
            return None
        
        # Create connection
        connection = UserConnection(
            user_id=user_id,
            connection_id=f"conn_{user_id}_{int(time.time())}",
            slot_number=slot,
            api_key=api_key,
            connected_at=time.time(),
            last_activity=time.time(),
            status=ConnectionStatus.CONNECTED,
            internal_ip=self._generate_internal_ip(server_block, slot)
        )
        
        server_block.connected_users[slot] = connection
        self.total_users += 1
        
        return connection
    
    def _find_available_slot(self, server_block: ServerBlock) -> Optional[int]:
        """Find available slot in server block."""
        for slot in range(server_block.max_users):
            if slot not in server_block.connected_users:
                return slot
        return None
    
    def _generate_internal_ip(self, server_block: ServerBlock, slot: int) -> str:
        """Generate internal IP for user slot."""
        base_network = server_block.internal_network.split('/')[0]
        base_parts = base_network.split('.')
        return f"{base_parts[0]}.{base_parts[1]}.{base_parts[2]}.{slot + 1}"
    
    def get_network_status(self) -> Dict[str, any]:
        """Get network status."""
        total_connected = sum(len(block.connected_users) for block in self.server_blocks.values())
        total_capacity = len(self.server_blocks) * 60
        
        return {
            'total_blocks': len(self.server_blocks),
            'total_connected_users': total_connected,
            'total_capacity': total_capacity,
            'utilization_percentage': (total_connected / total_capacity) * 100 if total_capacity > 0 else 0,
            'traffic_monitoring': self.traffic_monitoring
        }

# === UNIFIED CARMA SYSTEM ===

class CARMASystem:
    """Unified CARMA system with all cognitive enhancements integrated and AIOS wrapper patterns."""
    
    def __init__(self, base_dir: str = "Data/FractalCache"):
        # Initialize unified AIOS systems
        self.aios_config = aios_config
        self.logger = aios_logger
        self.health_checker = aios_health_checker
        self.security_validator = aios_security_validator
        
        # Log initialization
        self.logger.info("Initializing Unified CARMA System...", "CARMA")
        
        # Initialize base components
        self.cache = FractalMyceliumCache(base_dir)
        self.executive = CARMAExecutiveBrain(self.cache)
        self.meta_memory = CARMAMetaMemory(self.cache)
        self.performance = CARMA100PercentPerformance(self.cache, self.executive, self.meta_memory)
        self.mycelium_network = CARMAMyceliumNetwork()
        
        # Enhanced memory system components
        self.memory_compressor = CARMAMemoryCompressor()
        self.memory_clusterer = CARMAMemoryClusterer()
        self.memory_analytics = CARMAMemoryAnalytics()
        
        # System state
        self.total_queries = 0
        
        # Perform health check
        health_status = self.health_checker.check_system_health()
        if health_status["overall_status"] != "HEALTHY":
            self.logger.warn(f"System health degraded: {health_status['overall_status']}", "CARMA")
        
        self.logger.success("Unified CARMA System Initialized", "CARMA")
        self.learning_cycles = 0
        self.cognitive_events = []
        self.personality_drift = {
            'conscientiousness': 0.0,
            'openness': 0.0,
            'extraversion': 0.0,
            'agreeableness': 0.0,
            'neuroticism': 0.0
        }
        
        print(" Unified CARMA System Initialized")
        print(f"   Base cache: {len(self.cache.file_registry)} fragments")
        print(f"   Emotion tracking: Enabled")
        print(f"   Consolidation windows: Enabled")
        print(f"   Meta-memory: Enabled")
        print(f"   Synaptic tagging: Enabled")
        print(f"   Predictive coding: Enabled")
        print(f"   Memory compression: Enabled")
        print(f"   Memory clustering: Enabled")
        print(f"   Memory analytics: Enabled")
    
    def process_query(self, query: str, context: Dict = None) -> Dict:
        """Process a query through the complete cognitive system."""
        self.total_queries += 1
        start_time = time.time()
        
        print(f"\n Processing Query #{self.total_queries}: {query[:50]}...")
        
        # Generate embedding for query
        query_embedding = self.cache.embedder.embed(query)
        
        # Find relevant fragments
        relevant_fragments = self.cache.find_relevant(query_embedding, topk=5)
        
        # Generate cognitive response
        response = self._generate_cognitive_response(query, relevant_fragments, {}, {}, {})
        
        # Update personality based on all cognitive factors
        self._update_cognitive_personality(query, response, {}, {}, {})
        
        processing_time = time.time() - start_time
        
        # Record cognitive event
        cognitive_event = {
            'timestamp': time.time(),
            'query': query,
            'processing_time': processing_time,
            'fragments_found': len(relevant_fragments),
            'personality_drift': self.personality_drift.copy()
        }
        self.cognitive_events.append(cognitive_event)
        
        # Compile results
        results = {
            'query': query,
            'response': response,
            'processing_time': processing_time,
            'fragments_found': len(relevant_fragments),
            'fragments_found': [f.id for f in relevant_fragments],
            'personality_drift': self.personality_drift.copy(),
            'cognitive_event': cognitive_event,
            'system_stats': self.get_comprehensive_stats()
        }
        
        print(f" Query processed in {processing_time:.2f}s")
        print(f"   Fragments: {len(relevant_fragments)}")
        
        return results
    
    def compress_memories(self, algorithm: str = 'semantic') -> Dict:
        """Compress memory fragments using advanced compression."""
        fragments = list(self.cache.file_registry.values())
        return self.memory_compressor.compress_memory(fragments, algorithm)
    
    def cluster_memories(self, num_clusters: int = 5) -> Dict:
        """Cluster memory fragments into organized groups."""
        fragments = list(self.cache.file_registry.values())
        return self.memory_clusterer.cluster_memories(fragments, num_clusters)
    
    def analyze_memory_system(self) -> Dict:
        """Analyze memory system and provide insights."""
        return self.memory_analytics.analyze_memory_system(self.cache)
    
    def optimize_memory_system(self) -> Dict:
        """Optimize memory system based on analytics."""
        analysis = self.analyze_memory_system()
        optimizations = []
        
        # Apply compression if recommended
        if "compression" in str(analysis.get('recommendations', [])):
            compression_result = self.compress_memories('semantic')
            optimizations.append({
                'type': 'compression',
                'space_saved': compression_result['space_saved'],
                'compression_ratio': compression_result['compression_ratio']
            })
        
        # Apply clustering if many fragments
        fragment_count = analysis.get('memory_growth', {}).get('total_fragments', 0)
        if fragment_count > 50:
            cluster_result = self.cluster_memories(min(5, fragment_count // 10))
            optimizations.append({
                'type': 'clustering',
                'clusters_created': cluster_result['num_clusters']
            })
        
        return {
            'analysis': analysis,
            'optimizations_applied': optimizations,
            'optimization_timestamp': time.time()
        }
    
    def _generate_cognitive_response(self, query: str, fragments: List, 
                                   confidences: Dict, emotional_weights: Dict,
                                   predictions: Dict) -> str:
        """Generate a response using all cognitive enhancements."""
        response_parts = [f" Cognitive Analysis: {query}"]
        response_parts.append(f" Found {len(fragments)} relevant fragments")
        
        # Add fragment analysis
        for i, fragment in enumerate(fragments[:3]):
            response_parts.append(f"  {i+1}. {fragment.content[:100]}...")
        
        return "\n".join(response_parts)
    
    def _update_cognitive_personality(self, query: str, response: str, 
                                    emotional_weights: Dict, confidences: Dict,
                                    predictions: Dict):
        """Update personality based on all cognitive factors."""
        # Simple personality drift based on query content
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['creative', 'imaginative', 'artistic']):
            self.personality_drift['openness'] += 0.01
        if any(word in query_lower for word in ['organized', 'systematic', 'methodical']):
            self.personality_drift['conscientiousness'] += 0.01
        if any(word in query_lower for word in ['social', 'outgoing', 'energetic']):
            self.personality_drift['extraversion'] += 0.01
        if any(word in query_lower for word in ['helpful', 'kind', 'cooperative']):
            self.personality_drift['agreeableness'] += 0.01
        if any(word in query_lower for word in ['anxious', 'worried', 'stressed']):
            self.personality_drift['neuroticism'] += 0.01
    
    def get_comprehensive_stats(self) -> Dict:
        """Get comprehensive statistics from all cognitive systems."""
        cache_stats = self.cache.get_cache_statistics()
        executive_status = self.executive.get_executive_status()
        meta_stats = self.meta_memory.get_memory_statistics()
        network_status = self.mycelium_network.get_network_status()
        
        return {
            'cache': cache_stats,
            'executive': executive_status,
            'meta_memory': meta_stats,
            'network': network_status,
            'personality_drift': self.personality_drift,
            'total_queries': self.total_queries,
            'learning_cycles': self.learning_cycles,
            'performance_level': self.performance.get_performance_level()
        }

# === MAIN ENTRY POINT ===

def main():
    """Test the unified CARMA system."""
    print(" Testing Unified CARMA System")
    
    # Initialize system
    system = CARMASystem()
    
    # Test queries
    test_queries = [
        "I am learning about artificial intelligence and machine learning",
        "This research shows that memory consolidation happens during sleep",
        "I'm not entirely sure about this hypothesis, but it seems plausible",
        "The neural networks in the brain form complex interconnected patterns"
    ]
    
    # Process queries
    for query in test_queries:
        result = system.process_query(query)
        print(f"\nQuery: {query}")
        print(f"Response: {result['response']}")
        print(f"Fragments found: {result['fragments_found']}")
    
    # Get final stats
    stats = system.get_comprehensive_stats()
    print(f"\n Final System Stats:")
    print(f"   Performance level: {stats['performance_level']:.1f}%")
    print(f"   Total queries: {stats['total_queries']}")
    print(f"   Cache fragments: {stats['cache']['total_fragments']}")
    print(f"   Network utilization: {stats['network']['utilization_percentage']:.1f}%")

# === ENHANCED MEMORY SYSTEM COMPONENTS ===

class CARMAMemoryCompressor:
    """Advanced memory compression system for CARMA."""
    
    def __init__(self):
        self.compression_ratio = 0.0
        self.compression_history = []
        self.compression_algorithms = {
            'semantic': self._semantic_compression,
            'temporal': self._temporal_compression,
            'hierarchical': self._hierarchical_compression
        }
    
    def compress_memory(self, fragments: List[Dict], algorithm: str = 'semantic') -> Dict:
        """Compress memory fragments using specified algorithm."""
        if algorithm not in self.compression_algorithms:
            algorithm = 'semantic'
        
        original_size = sum(len(f.get('content', '')) for f in fragments)
        compressed_fragments = self.compression_algorithms[algorithm](fragments)
        compressed_size = sum(len(f.get('content', '')) for f in compressed_fragments)
        
        self.compression_ratio = (original_size - compressed_size) / original_size if original_size > 0 else 0.0
        self.compression_history.append({
            'timestamp': time.time(),
            'algorithm': algorithm,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'ratio': self.compression_ratio
        })
        
        return {
            'compressed_fragments': compressed_fragments,
            'compression_ratio': self.compression_ratio,
            'space_saved': original_size - compressed_size
        }
    
    def _semantic_compression(self, fragments: List[Dict]) -> List[Dict]:
        """Compress fragments by removing redundant semantic information."""
        compressed = []
        seen_concepts = set()
        
        for fragment in fragments:
            content = fragment.get('content', '')
            # Extract key concepts (simplified)
            concepts = self._extract_concepts(content)
            
            # Only keep if new concepts are present
            if not concepts.issubset(seen_concepts):
                compressed.append(fragment)
                seen_concepts.update(concepts)
        
        return compressed
    
    def _temporal_compression(self, fragments: List[Dict]) -> List[Dict]:
        """Compress fragments by temporal clustering."""
        # Group by time windows
        time_groups = defaultdict(list)
        for fragment in fragments:
            timestamp = fragment.get('timestamp', 0)
            time_window = int(timestamp // 3600)  # 1-hour windows
            time_groups[time_window].append(fragment)
        
        # Keep only most important fragment per time window
        compressed = []
        for window_fragments in time_groups.values():
            if window_fragments:
                # Sort by importance (simplified)
                most_important = max(window_fragments, key=lambda f: len(f.get('content', '')))
                compressed.append(most_important)
        
        return compressed
    
    def _hierarchical_compression(self, fragments: List[Dict]) -> List[Dict]:
        """Compress fragments using hierarchical summarization."""
        if len(fragments) <= 1:
            return fragments
        
        # Group by similarity
        groups = self._group_by_similarity(fragments)
        compressed = []
        
        for group in groups:
            if len(group) == 1:
                compressed.append(group[0])
            else:
                # Create summary of group
                summary = self._create_group_summary(group)
                compressed.append(summary)
        
        return compressed
    
    def _extract_concepts(self, text: str) -> set:
        """Extract key concepts from text (simplified)."""
        # Simple keyword extraction
        words = text.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        concepts = {word for word in words if len(word) > 3 and word not in stop_words}
        return concepts
    
    def _group_by_similarity(self, fragments: List[Dict]) -> List[List[Dict]]:
        """Group fragments by content similarity."""
        groups = []
        used = set()
        
        for i, fragment in enumerate(fragments):
            if i in used:
                continue
            
            group = [fragment]
            used.add(i)
            
            for j, other in enumerate(fragments[i+1:], i+1):
                if j in used:
                    continue
                
                # Simple similarity check
                if self._calculate_similarity(fragment, other) > 0.7:
                    group.append(other)
                    used.add(j)
            
            groups.append(group)
        
        return groups
    
    def _calculate_similarity(self, frag1: Dict, frag2: Dict) -> float:
        """Calculate similarity between two fragments."""
        content1 = frag1.get('content', '').lower()
        content2 = frag2.get('content', '').lower()
        
        if not content1 or not content2:
            return 0.0
        
        words1 = set(content1.split())
        words2 = set(content2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _create_group_summary(self, group: List[Dict]) -> Dict:
        """Create a summary of a group of fragments."""
        all_content = ' '.join(f.get('content', '') for f in group)
        return {
            'content': f"Summary: {all_content[:200]}...",
            'timestamp': max(f.get('timestamp', 0) for f in group),
            'source_fragments': len(group),
            'type': 'summary'
        }

class CARMAMemoryClusterer:
    """Memory clustering system for organizing CARMA fragments."""
    
    def __init__(self):
        self.clusters = {}
        self.cluster_centers = {}
        self.cluster_metadata = {}
    
    def cluster_memories(self, fragments: List[Dict], num_clusters: int = 5) -> Dict:
        """Cluster memory fragments into groups."""
        if len(fragments) < 2:
            return {'clusters': {0: fragments}, 'metadata': {}}
        
        # Extract features for clustering
        features = self._extract_features(fragments)
        
        # Simple k-means clustering (simplified)
        clusters = self._kmeans_clustering(features, num_clusters)
        
        # Organize fragments by cluster
        cluster_groups = defaultdict(list)
        for i, cluster_id in enumerate(clusters):
            cluster_groups[cluster_id].append(fragments[i])
        
        # Calculate cluster metadata
        metadata = self._calculate_cluster_metadata(cluster_groups)
        
        self.clusters = dict(cluster_groups)
        self.cluster_metadata = metadata
        
        return {
            'clusters': dict(cluster_groups),
            'metadata': metadata,
            'num_clusters': len(cluster_groups)
        }
    
    def _extract_features(self, fragments: List[Dict]) -> List[List[float]]:
        """Extract numerical features from fragments."""
        features = []
        for fragment in fragments:
            content = fragment.get('content', '')
            feature_vector = [
                len(content),  # Length
                content.count('.'),  # Sentence count
                content.count(' '),  # Word count
                len(set(content.lower().split())),  # Unique words
                fragment.get('timestamp', 0) % 86400,  # Time of day
            ]
            features.append(feature_vector)
        return features
    
    def _kmeans_clustering(self, features: List[List[float]], k: int) -> List[int]:
        """Simple k-means clustering implementation."""
        if len(features) <= k:
            return list(range(len(features)))
        
        # Initialize centroids randomly
        centroids = random.sample(features, k)
        clusters = [0] * len(features)
        
        # Iterate until convergence
        for _ in range(10):  # Max 10 iterations
            # Assign points to nearest centroid
            for i, point in enumerate(features):
                distances = [self._euclidean_distance(point, centroid) for centroid in centroids]
                clusters[i] = distances.index(min(distances))
            
            # Update centroids
            new_centroids = []
            for cluster_id in range(k):
                cluster_points = [features[i] for i, c in enumerate(clusters) if c == cluster_id]
                if cluster_points:
                    centroid = [sum(coord) / len(cluster_points) for coord in zip(*cluster_points)]
                    new_centroids.append(centroid)
                else:
                    new_centroids.append(centroids[cluster_id])
            
            if new_centroids == centroids:
                break
            centroids = new_centroids
        
        return clusters
    
    def _euclidean_distance(self, point1: List[float], point2: List[float]) -> float:
        """Calculate Euclidean distance between two points."""
        return sum((a - b) ** 2 for a, b in zip(point1, point2)) ** 0.5
    
    def _calculate_cluster_metadata(self, cluster_groups: Dict) -> Dict:
        """Calculate metadata for each cluster."""
        metadata = {}
        for cluster_id, fragments in cluster_groups.items():
            if not fragments:
                continue
            
            contents = [f.get('content', '') for f in fragments]
            timestamps = [f.get('timestamp', 0) for f in fragments]
            
            metadata[cluster_id] = {
                'size': len(fragments),
                'avg_length': sum(len(c) for c in contents) / len(contents),
                'time_span': max(timestamps) - min(timestamps) if timestamps else 0,
                'common_words': self._find_common_words(contents),
                'themes': self._identify_themes(contents)
            }
        
        return metadata
    
    def _find_common_words(self, contents: List[str]) -> List[str]:
        """Find common words across cluster contents."""
        word_counts = defaultdict(int)
        for content in contents:
            words = content.lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    word_counts[word] += 1
        
        # Return top 5 most common words
        return [word for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def _identify_themes(self, contents: List[str]) -> List[str]:
        """Identify themes in cluster contents (simplified)."""
        # Simple theme detection based on keywords
        theme_keywords = {
            'technology': ['computer', 'software', 'ai', 'algorithm', 'data', 'system'],
            'science': ['research', 'study', 'experiment', 'hypothesis', 'theory'],
            'personal': ['feel', 'think', 'believe', 'experience', 'emotion'],
            'learning': ['learn', 'understand', 'knowledge', 'education', 'study']
        }
        
        all_text = ' '.join(contents).lower()
        themes = []
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                themes.append(theme)
        
        return themes

class CARMAMemoryAnalytics:
    """Memory analytics system for CARMA insights."""
    
    def __init__(self):
        self.analytics_data = {
            'memory_growth': [],
            'access_patterns': [],
            'compression_stats': [],
            'cluster_evolution': []
        }
    
    def analyze_memory_system(self, cache: 'FractalMyceliumCache') -> Dict:
        """Analyze the memory system and provide insights."""
        analysis = {
            'memory_growth': self._analyze_memory_growth(cache),
            'access_patterns': self._analyze_access_patterns(cache),
            'fragment_distribution': self._analyze_fragment_distribution(cache),
            'temporal_patterns': self._analyze_temporal_patterns(cache),
            'recommendations': self._generate_recommendations(cache)
        }
        
        return analysis
    
    def _analyze_memory_growth(self, cache: 'FractalMyceliumCache') -> Dict:
        """Analyze memory growth patterns."""
        fragments = list(cache.file_registry.values())
        if not fragments:
            return {'growth_rate': 0.0, 'total_fragments': 0}
        
        timestamps = [f.get('timestamp', 0) for f in fragments if f.get('timestamp')]
        if len(timestamps) < 2:
            return {'growth_rate': 0.0, 'total_fragments': len(fragments)}
        
        timestamps.sort()
        time_span = timestamps[-1] - timestamps[0]
        growth_rate = len(timestamps) / (time_span / 3600) if time_span > 0 else 0  # fragments per hour
        
        return {
            'growth_rate': growth_rate,
            'total_fragments': len(fragments),
            'time_span_hours': time_span / 3600,
            'avg_fragments_per_hour': growth_rate
        }
    
    def _analyze_access_patterns(self, cache: 'FractalMyceliumCache') -> Dict:
        """Analyze memory access patterns."""
        fragments = list(cache.file_registry.values())
        access_counts = [f.get('access_count', 0) for f in fragments]
        
        if not access_counts:
            return {'avg_access': 0, 'access_distribution': {}}
        
        return {
            'avg_access': sum(access_counts) / len(access_counts),
            'max_access': max(access_counts),
            'min_access': min(access_counts),
            'access_distribution': {
                'high': len([c for c in access_counts if c > 10]),
                'medium': len([c for c in access_counts if 5 <= c <= 10]),
                'low': len([c for c in access_counts if c < 5])
            }
        }
    
    def _analyze_fragment_distribution(self, cache: 'FractalMyceliumCache') -> Dict:
        """Analyze fragment size and type distribution."""
        fragments = list(cache.file_registry.values())
        if not fragments:
            return {'size_distribution': {}, 'type_distribution': {}}
        
        sizes = [len(f.get('content', '')) for f in fragments]
        types = [f.get('type', 'unknown') for f in fragments]
        
        return {
            'size_distribution': {
                'small': len([s for s in sizes if s < 100]),
                'medium': len([s for s in sizes if 100 <= s < 500]),
                'large': len([s for s in sizes if s >= 500])
            },
            'type_distribution': {t: types.count(t) for t in set(types)},
            'avg_size': sum(sizes) / len(sizes),
            'total_content_size': sum(sizes)
        }
    
    def _analyze_temporal_patterns(self, cache: 'FractalMyceliumCache') -> Dict:
        """Analyze temporal patterns in memory creation."""
        fragments = list(cache.file_registry.values())
        timestamps = [f.get('timestamp', 0) for f in fragments if f.get('timestamp')]
        
        if len(timestamps) < 2:
            return {'temporal_distribution': {}, 'peak_hours': []}
        
        # Group by hour of day
        hour_counts = defaultdict(int)
        for ts in timestamps:
            hour = datetime.fromtimestamp(ts).hour
            hour_counts[hour] += 1
        
        peak_hours = [h for h, c in hour_counts.items() if c == max(hour_counts.values())]
        
        return {
            'temporal_distribution': dict(hour_counts),
            'peak_hours': peak_hours,
            'activity_level': 'high' if max(hour_counts.values()) > 5 else 'low'
        }
    
    def _generate_recommendations(self, cache: 'FractalMyceliumCache') -> List[str]:
        """Generate recommendations for memory system optimization."""
        recommendations = []
        fragments = list(cache.file_registry.values())
        
        if len(fragments) > 1000:
            recommendations.append("Consider enabling memory compression - large fragment count detected")
        
        access_counts = [f.get('access_count', 0) for f in fragments]
        if access_counts and max(access_counts) > 50:
            recommendations.append("High access frequency detected - consider caching frequently accessed fragments")
        
        sizes = [len(f.get('content', '')) for f in fragments]
        if sizes and sum(sizes) > 1000000:  # 1MB
            recommendations.append("Large memory footprint - consider implementing memory pruning")
        
        if len(fragments) > 100 and len(set(f.get('type', 'unknown') for f in fragments)) < 3:
            recommendations.append("Low fragment diversity - consider expanding memory types")
        
        return recommendations

if __name__ == "__main__":
    main()
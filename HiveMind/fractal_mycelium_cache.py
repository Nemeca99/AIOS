#!/usr/bin/env python3
"""
Fractal Mycelium Cache System
============================

Implements a self-organizing, fractal cache system where large files
automatically split into smaller, specialized fragments. Each fragment
becomes a living organism with its own context, weights, and emotional tone.

The system grows exponentially: 1 → 2 → 4 → 8 → 16 → 32 → 64...
Each split creates more specialized, focused knowledge fragments.
"""

import json
import time
import random
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
import hashlib
import uuid
from simple_embedder import SimpleEmbedder

class FractalMyceliumCache:
    def __init__(self, base_dir: str = "Data/FractalCache"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # File size thresholds for splitting
        self.max_file_size = 1024 * 1024  # 1MB
        self.min_file_size = 1024  # 1KB
        self.split_threshold = 0.8  # Split when 80% of max size
        
        # Cache structure
        self.file_registry = {}  # file_id -> metadata
        self.fragment_tree = {}  # parent_id -> [child_ids]
        self.emotion_weights = {}  # file_id -> emotion weights
        self.tone_signatures = {}  # file_id -> tone signature
        
        # Specialization levels
        self.max_splits = 6  # 1 → 2 → 4 → 8 → 16 → 32 → 64
        self.current_levels = {}  # file_id -> split level
        
        # Eviction & Decay System
        self.max_cache_size = 1000  # Maximum fragments before eviction
        self.ttl_hours = 24  # Time-to-live in hours
        self.min_hit_count = 2  # Minimum hits to avoid eviction
        self.eviction_threshold = 0.8  # Evict when 80% of max size
        
        # Reinforcement System
        self.hit_weights = {}  # file_id -> hit_count
        self.path_weights = {}  # (from_id, to_id) -> weight
        # Valence / Karma System
        self.valence_sum: Dict[str, float] = {}  # file_id -> cumulative valence
        self.valence_count: Dict[str, int] = {}  # file_id -> count
        
        # Cross-linking System
        self.semantic_links = {}  # file_id -> [linked_file_ids]
        self.similarity_threshold = 0.3  # Cosine similarity threshold for linking (lowered for testing)
        
        # Metrics
        self.metrics = {
            'fragments_total': 0,
            'edges_total': 0,
            'avg_path_length': 0.0,
            'cache_hit_rate': 0.0,
            'eviction_events': 0,
            'split_events': 0,
            'reinforcement_events': 0,
            'cross_links': 0
        }
        
        # Embedding System
        self.embedder = SimpleEmbedder(use_api=False)  # Use fallback for now
        self.embedding_index = None  # FAISS index will be built here
        
        print("🌱 Fractal Mycelium Cache Initialized")
        print(f"📁 Base directory: {self.base_dir}")
        print(f"📏 Max file size: {self.max_file_size // 1024}KB")
        print(f"🔀 Max splits: {self.max_splits}")
        print(f"🧠 Eviction enabled: {self.max_cache_size} max fragments")
        print(f"⚡ Reinforcement enabled: hit-based weighting")
        print(f"🧠 Embedder: {self.embedder.embedding_model}")

    # --- Valence / Karma Utilities ---
    def _bounded_growth(self, current: float, base_rate: float, ceiling: float) -> float:
        """Logistic-like growth step bounded by linear ceiling."""
        growth = base_rate * current * (1.0 - (current / max(ceiling, 0.1)))
        return max(-current + 0.1, growth)  # ensure not collapsing below ~0.1

    def _linear_ceiling(self) -> float:
        """Linear ceiling grows with usage to keep stability."""
        total_queries = sum(self.hit_weights.values())
        return 50.0 + 0.1 * float(total_queries)

    def score_valence(self, text: str) -> float:
        """Lightweight valence scoring in [-1,1] using keyword heuristic."""
        positive = ['thank', 'great', 'good', 'nice', 'love', 'awesome', 'cool', 'glad']
        negative = ['hate', 'bad', 'angry', 'annoy', 'stupid', 'dumb', 'wtf', 'terrible']
        tl = text.lower()
        pos = sum(tl.count(w) for w in positive)
        neg = sum(tl.count(w) for w in negative)
        if pos == 0 and neg == 0:
            return 0.0
        raw = (pos - neg) / max(pos + neg, 1)
        return max(-1.0, min(1.0, raw))

    def process_interaction(self, query: str, response: str, affected_ids: List[str], valence: Optional[float] = None):
        """Apply valence-shaped reinforcement to affected fragments and their edges.

        - valence v in [-1,1] (if None, inferred from response)
        - bounded linear-exponential growth with a linear ceiling.
        """
        v = self.score_valence(response) if valence is None else max(-1.0, min(1.0, valence))
        base_rate = 0.08
        beta = 0.5
        ceiling = self._linear_ceiling()

        for file_id in affected_ids:
            if file_id not in self.file_registry:
                continue
            # init structures
            self.hit_weights[file_id] = self.hit_weights.get(file_id, 1.0)
            self.valence_sum[file_id] = self.valence_sum.get(file_id, 0.0)
            self.valence_count[file_id] = self.valence_count.get(file_id, 0)

            # update valence aggregates
            self.valence_sum[file_id] += v
            self.valence_count[file_id] += 1
            mean_v = self.valence_sum[file_id] / max(1, self.valence_count[file_id])

            # compute effective growth
            g = base_rate * (1.0 + beta * v)
            # bounded weight update
            w = float(self.hit_weights[file_id])
            delta = self._bounded_growth(w, g, ceiling)
            w = max(0.1, min(ceiling, w + delta))
            self.hit_weights[file_id] = w

            # edge shaping
            for neighbor_id in self._neighbors(file_id):
                edge_key = (file_id, neighbor_id)
                ew = float(self.path_weights.get(edge_key, 1.0))
                edge_ceiling = max(1.0, ceiling / 5.0)
                edelta = self._bounded_growth(ew, g, edge_ceiling)
                ew = max(0.1, min(edge_ceiling, ew + edelta))
                # slight decay for unrelated negativity
                if v < 0 and neighbor_id not in affected_ids:
                    ew *= 0.995
                self.path_weights[edge_key] = ew

        # update metric-ish fields
        self.metrics['reinforcement_events'] += 1

    def analyze_content(self, content: str) -> Dict:
        """Analyze content for emotional tone, keywords, and context"""
        # Extract common words/phrases
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = Counter(words)
        common_words = [word for word, count in word_freq.most_common(20) if len(word) > 3]
        
        # Extract phrases (2-3 words)
        phrases = re.findall(r'\b\w+\s+\w+\b', content.lower())
        phrase_freq = Counter(phrases)
        common_phrases = [phrase for phrase, count in phrase_freq.most_common(10)]
        
        # Analyze emotional tone
        emotion_indicators = {
            'excitement': ['amazing', 'incredible', 'fantastic', 'wow', 'awesome'],
            'frustration': ['frustrating', 'annoying', 'difficult', 'problem', 'issue'],
            'curiosity': ['wonder', 'curious', 'interesting', 'question', 'explore'],
            'determination': ['determined', 'focused', 'committed', 'persistent', 'dedicated'],
            'creativity': ['creative', 'innovative', 'original', 'unique', 'imaginative'],
            'technical': ['system', 'algorithm', 'function', 'code', 'technical'],
            'philosophical': ['think', 'believe', 'understand', 'meaning', 'purpose']
        }
        
        emotion_scores = {}
        for emotion, indicators in emotion_indicators.items():
            score = sum(content.lower().count(indicator) for indicator in indicators)
            # Ensure score is always numeric and handle division by zero
            normalized_score = score / max(len(content), 1) * 1000  # Normalize
            emotion_scores[emotion] = float(normalized_score) if isinstance(normalized_score, (int, float)) else 0.0
        
        # Analyze tone signature
        content_length = max(len(content), 1)  # Prevent division by zero
        tone_signature = {
            'formality': float(len(re.findall(r'\b(please|thank you|sir|madam)\b', content.lower())) / content_length * 1000),
            'casualness': float(len(re.findall(r'\b(yeah|ok|cool|awesome|hey)\b', content.lower())) / content_length * 1000),
            'technicality': float(len(re.findall(r'\b(function|algorithm|system|code|data)\b', content.lower())) / content_length * 1000),
            'questioning': float(len(re.findall(r'\?', content)) / content_length * 1000),
            'exclamation': float(len(re.findall(r'!', content)) / content_length * 1000)
        }
        
        return {
            'common_words': common_words,
            'common_phrases': common_phrases,
            'emotion_scores': emotion_scores,
            'tone_signature': tone_signature,
            'word_count': len(words),
            'char_count': len(content)
        }

    def create_file_id(self, content: str, parent_id: str = None) -> str:
        """Create unique file ID based on content and parent"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        if parent_id:
            return f"{parent_id}_{content_hash}"
        return f"root_{content_hash}"

    def _generate_node_address(self, file_id: str) -> str:
        """Generate a unique network address for a fragment"""
        # fm:// stands for Fractal Mycelium
        return f"fm://{file_id}-{uuid.uuid4().hex[:12]}"

    def split_content(self, content: str, split_count: int = 2) -> List[str]:
        """Split content into multiple fragments intelligently"""
        if split_count < 2:
            return [content]
        
        # Try to split on natural boundaries first
        split_points = []
        
        # Split on paragraphs
        paragraphs = content.split('\n\n')
        if len(paragraphs) >= split_count:
            # Distribute paragraphs evenly
            chunk_size = len(paragraphs) // split_count
            for i in range(split_count):
                start = i * chunk_size
                end = start + chunk_size if i < split_count - 1 else len(paragraphs)
                split_points.append('\n\n'.join(paragraphs[start:end]))
            return split_points
        
        # Split on sentences
        sentences = re.split(r'[.!?]+', content)
        if len(sentences) >= split_count:
            chunk_size = len(sentences) // split_count
            for i in range(split_count):
                start = i * chunk_size
                end = start + chunk_size if i < split_count - 1 else len(sentences)
                split_points.append('. '.join(sentences[start:end]))
            return split_points
        
        # Split on words as last resort
        words = content.split()
        chunk_size = len(words) // split_count
        for i in range(split_count):
            start = i * chunk_size
            end = start + chunk_size if i < split_count - 1 else len(words)
            split_points.append(' '.join(words[start:end]))
        
        return split_points

    def create_fragment(self, content: str, parent_id: str = None, level: int = 0) -> str:
        """Create a new fragment file with metadata"""
        file_id = self.create_file_id(content, parent_id)
        
        # Analyze content
        analysis = self.analyze_content(content)
        
        # Create fragment metadata
        fragment_data = {
            'file_id': file_id,
            'parent_id': parent_id,
            'level': level,
            'node_address': self._generate_node_address(file_id),
            'ancestors': [],
            'children': [],
            'content': content,
            'created': datetime.now().isoformat(),
            'size': len(content),
            'analysis': analysis,
            'access_count': 0,
            'last_accessed': datetime.now().isoformat(),
            'specialization': self._determine_specialization(analysis),
            'tags': self._generate_tags(analysis)
        }
        
        # Save fragment
        fragment_file = self.base_dir / f"{file_id}.json"
        with open(fragment_file, 'w') as f:
            json.dump(fragment_data, f, indent=2)
        
        # Update registry
        self.file_registry[file_id] = fragment_data
        self.emotion_weights[file_id] = analysis['emotion_scores']
        self.tone_signatures[file_id] = analysis['tone_signature']
        self.current_levels[file_id] = level
        
        # Update fragment tree and relationship headers
        if parent_id:
            if parent_id not in self.fragment_tree:
                self.fragment_tree[parent_id] = []
            self.fragment_tree[parent_id].append(file_id)
            # Update parent header with child
            parent_fragment = self.file_registry.get(parent_id)
            if parent_fragment is not None:
                parent_fragment.setdefault('children', [])
                if file_id not in parent_fragment['children']:
                    parent_fragment['children'].append(file_id)
                # Persist parent update
                parent_file = self.base_dir / f"{parent_id}.json"
                with open(parent_file, 'w') as pf:
                    json.dump(parent_fragment, pf, indent=2)
            # Set ancestors chain for child
            fragment_data['ancestors'] = list(parent_fragment.get('ancestors', [])) + [parent_id] if parent_fragment else [parent_id]
            # Persist child update with ancestors
            with open(fragment_file, 'w') as f:
                json.dump(fragment_data, f, indent=2)
        
        return file_id

    def _determine_specialization(self, analysis: Dict) -> str:
        """Determine the specialization of a fragment based on analysis"""
        emotion_scores = analysis['emotion_scores']
        tone_signature = analysis['tone_signature']
        
        # Find dominant emotion - ensure all values are numeric
        numeric_emotions = {}
        for k, v in emotion_scores.items():
            if isinstance(v, (int, float)):
                numeric_emotions[k] = float(v)
            else:
                try:
                    numeric_emotions[k] = float(v) if v is not None else 0.0
                except (ValueError, TypeError):
                    numeric_emotions[k] = 0.0
        
        if not numeric_emotions:
            return 'general'
        dominant_emotion = max(numeric_emotions.items(), key=lambda x: x[1])[0]
        
        # Find dominant tone - ensure all values are numeric
        numeric_tones = {}
        for k, v in tone_signature.items():
            if isinstance(v, (int, float)):
                numeric_tones[k] = float(v)
            else:
                try:
                    numeric_tones[k] = float(v) if v is not None else 0.0
                except (ValueError, TypeError):
                    numeric_tones[k] = 0.0
        
        if not numeric_tones:
            return 'general'
        dominant_tone = max(numeric_tones.items(), key=lambda x: x[1])[0]
        
        # Determine specialization
        if dominant_emotion == 'technical' or dominant_tone == 'technicality':
            return 'technical'
        elif dominant_emotion == 'philosophical':
            return 'philosophical'
        elif dominant_emotion == 'creativity':
            return 'creative'
        elif dominant_emotion == 'frustration':
            return 'problem_solving'
        elif dominant_emotion == 'excitement':
            return 'enthusiastic'
        else:
            return 'general'

    def _generate_tags(self, analysis: Dict) -> List[str]:
        """Generate tags for a fragment"""
        tags = []
        
        # Add common words as tags
        tags.extend(analysis['common_words'][:5])
        
        # Add common phrases as tags
        tags.extend(analysis['common_phrases'][:3])
        
        # Add emotion tags
        for emotion, score in analysis['emotion_scores'].items():
            if isinstance(score, (int, float)) and score > 0.1:  # Threshold for emotion tags
                tags.append(f"emotion_{emotion}")
        
        # Add tone tags
        for tone, score in analysis['tone_signature'].items():
            if isinstance(score, (int, float)) and score > 0.1:  # Threshold for tone tags
                tags.append(f"tone_{tone}")
        
        return list(set(tags))  # Remove duplicates

    def should_split(self, file_id: str) -> bool:
        """Check if a file should be split"""
        if file_id not in self.file_registry:
            return False
        
        fragment = self.file_registry[file_id]
        current_level = self.current_levels.get(file_id, 0)
        
        # Don't split if already at max level
        if current_level >= self.max_splits:
            return False
        
        # Check size threshold
        size_ratio = fragment['size'] / self.max_file_size
        return size_ratio >= self.split_threshold

    def auto_split_file(self, file_id: str) -> List[str]:
        """Automatically split a file that's too large"""
        if file_id not in self.file_registry:
            return []
        
        fragment = self.file_registry[file_id]
        content = fragment['content']
        current_level = self.current_levels.get(file_id, 0)
        
        # Determine split count (exponential growth)
        split_count = 2 ** (current_level + 1)
        
        print(f"🔀 Splitting {file_id} (level {current_level}) into {split_count} fragments")
        
        # Split content
        fragments = self.split_content(content, split_count)
        
        # Create new fragments
        new_file_ids = []
        for i, fragment_content in enumerate(fragments):
            new_file_id = self.create_fragment(
                fragment_content, 
                parent_id=file_id, 
                level=current_level + 1
            )
            new_file_ids.append(new_file_id)
        
        # Mark original as split
        fragment['split_into'] = new_file_ids
        fragment['split_date'] = datetime.now().isoformat()
        
        # Save updated original
        fragment_file = self.base_dir / f"{file_id}.json"
        with open(fragment_file, 'w') as f:
            json.dump(fragment, f, indent=2)
        
        print(f"✅ Created {len(new_file_ids)} new fragments")
        return new_file_ids

    def evict_fragments(self) -> int:
        """Evict old, low-frequency fragments to maintain cache size"""
        if len(self.file_registry) <= self.max_cache_size:
            return 0
        
        evicted = 0
        current_time = datetime.now()
        
        # Calculate eviction scores for each fragment
        eviction_candidates = []
        for file_id, fragment in self.file_registry.items():
            hit_count = self.hit_weights.get(file_id, 0)
            last_accessed = datetime.fromisoformat(fragment.get('last_accessed', fragment['created']))
            age_hours = (current_time - last_accessed).total_seconds() / 3600
            
            # Eviction score: lower is more likely to be evicted
            eviction_score = hit_count * 10 - age_hours * 0.1
            
            eviction_candidates.append((file_id, eviction_score, hit_count, age_hours))
        
        # Sort by eviction score (ascending) and evict the worst
        eviction_candidates.sort(key=lambda x: x[1])
        
        target_evictions = len(self.file_registry) - self.max_cache_size
        
        for file_id, score, hits, age in eviction_candidates[:target_evictions]:
            # Evict if low hits OR old age OR just to make room
            if hits < self.min_hit_count or age > self.ttl_hours or evicted < target_evictions:
                self._remove_fragment(file_id)
                evicted += 1
                self.metrics['eviction_events'] += 1
        
        print(f"🗑️ Evicted {evicted} fragments (cache size: {len(self.file_registry)})")
        return evicted

    def _remove_fragment(self, file_id: str):
        """Remove a fragment and clean up all references"""
        if file_id not in self.file_registry:
            return
        
        fragment = self.file_registry[file_id]
        
        # Remove from parent's children list
        parent_id = fragment.get('parent_id')
        if parent_id and parent_id in self.file_registry:
            parent = self.file_registry[parent_id]
            if 'children' in parent and file_id in parent['children']:
                parent['children'].remove(file_id)
                # Update parent file
                parent_file = self.base_dir / f"{parent_id}.json"
                with open(parent_file, 'w') as f:
                    json.dump(parent, f, indent=2)
        
        # Remove children (cascade deletion)
        children = fragment.get('children', [])
        for child_id in children:
            self._remove_fragment(child_id)
        
        # Remove from fragment tree
        if parent_id and parent_id in self.fragment_tree:
            if file_id in self.fragment_tree[parent_id]:
                self.fragment_tree[parent_id].remove(file_id)
        
        # Remove from all data structures
        del self.file_registry[file_id]
        self.emotion_weights.pop(file_id, None)
        self.tone_signatures.pop(file_id, None)
        self.current_levels.pop(file_id, None)
        self.hit_weights.pop(file_id, None)
        self.semantic_links.pop(file_id, None)
        
        # Remove file from disk
        fragment_file = self.base_dir / f"{file_id}.json"
        if fragment_file.exists():
            fragment_file.unlink()

    def reinforce_fragment(self, file_id: str):
        """Reinforce a fragment by increasing its hit count and path weights"""
        if file_id not in self.file_registry:
            return
        
        # Increment hit count
        self.hit_weights[file_id] = self.hit_weights.get(file_id, 0) + 1
        
        # Update last accessed time
        fragment = self.file_registry[file_id]
        fragment['last_accessed'] = datetime.now().isoformat()
        
        # Reinforce path weights to neighbors
        neighbors = self._neighbors(file_id)
        for neighbor_id in neighbors:
            edge_key = (file_id, neighbor_id)
            self.path_weights[edge_key] = self.path_weights.get(edge_key, 1.0) + 0.1
        
        self.metrics['reinforcement_events'] += 1
        
        # Save updated fragment
        fragment_file = self.base_dir / f"{file_id}.json"
        with open(fragment_file, 'w') as f:
            json.dump(fragment, f, indent=2)

    def create_semantic_links(self, file_id: str, max_links: int = 5):
        """Create semantic cross-links between fragments based on similarity"""
        if file_id not in self.file_registry:
            return 0
        
        fragment = self.file_registry[file_id]
        fragment_tags = set(fragment.get('tags', []))
        fragment_emotion = fragment.get('analysis', {}).get('emotion_scores', {})
        
        # Find similar fragments
        similarity_scores = []
        for other_id, other_fragment in self.file_registry.items():
            if other_id == file_id:
                continue
            
            # Skip if already linked
            if other_id in self.semantic_links.get(file_id, []):
                continue
            
            other_tags = set(other_fragment.get('tags', []))
            other_emotion = other_fragment.get('analysis', {}).get('emotion_scores', {})
            
            # Calculate tag similarity (Jaccard)
            tag_intersection = len(fragment_tags & other_tags)
            tag_union = len(fragment_tags | other_tags)
            tag_similarity = tag_intersection / tag_union if tag_union > 0 else 0
            
            # Calculate emotion similarity (cosine)
            emotion_similarity = 0.0
            if fragment_emotion and other_emotion:
                common_emotions = set(fragment_emotion.keys()) & set(other_emotion.keys())
                if common_emotions:
                    dot_product = sum(fragment_emotion.get(e, 0) * other_emotion.get(e, 0) for e in common_emotions)
                    norm_a = sum(v**2 for v in fragment_emotion.values()) ** 0.5
                    norm_b = sum(v**2 for v in other_emotion.values()) ** 0.5
                    if norm_a > 0 and norm_b > 0:
                        emotion_similarity = dot_product / (norm_a * norm_b)
            
            # Combined similarity score
            combined_score = (tag_similarity * 0.6) + (emotion_similarity * 0.4)
            
            if combined_score >= self.similarity_threshold:
                similarity_scores.append((other_id, combined_score, tag_similarity, emotion_similarity))
        
        # Sort by similarity and create links
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        links_created = 0
        
        for other_id, combined_score, tag_sim, emotion_sim in similarity_scores[:max_links]:
            # Create bidirectional link
            if file_id not in self.semantic_links:
                self.semantic_links[file_id] = []
            if other_id not in self.semantic_links:
                self.semantic_links[other_id] = []
            
            if other_id not in self.semantic_links[file_id]:
                self.semantic_links[file_id].append(other_id)
                self.semantic_links[other_id].append(file_id)
                links_created += 1
                self.metrics['cross_links'] += 1
                
                # Set initial path weight for semantic links
                edge_key = (file_id, other_id)
                self.path_weights[edge_key] = combined_score * 2.0  # Semantic links get higher weight
        
        if links_created > 0:
            print(f"🔗 Created {links_created} semantic links for {file_id}")
        
        return links_created

    def update_semantic_links(self, max_links_per_fragment: int = 3):
        """Update semantic links for all fragments"""
        total_links = 0
        for file_id in self.file_registry.keys():
            links_created = self.create_semantic_links(file_id, max_links_per_fragment)
            total_links += links_created
        
        print(f"🌐 Total semantic links created: {total_links}")
        return total_links

    def add_content(self, content: str, parent_id: str = None) -> str:
        """Add new content to the fractal cache"""
        # Evict old fragments if cache is too large
        self.evict_fragments()
        
        # Create initial fragment
        file_id = self.create_fragment(content, parent_id, 0)
        
        # Initialize hit count
        self.hit_weights[file_id] = 1
        
        # Check if it needs splitting
        if self.should_split(file_id):
            new_fragments = self.auto_split_file(file_id)
            self.metrics['split_events'] += 1
            return new_fragments[0] if new_fragments else file_id
        
        return file_id

    def find_relevant_fragments(self, query: str, max_results: int = 10) -> List[Dict]:
        """Find fragments relevant to a query"""
        
        # Check if we have embeddings and index
        if hasattr(self, 'embedding_index') and self.embedding_index is not None:
            return self._find_relevant_with_embeddings(query, max_results)
        else:
            # Fallback to analysis-based search
            return self._find_relevant_with_analysis(query, max_results)
    
    def _find_relevant_with_embeddings(self, query: str, max_results: int) -> List[Dict]:
        """Find relevant fragments using FAISS index."""
        try:
            # Generate query embedding
            query_embedding = self.embedder.embed(query)
            
            # Use the FAISS index
            results = self.find_relevant(query_embedding, topk=max_results)
            
            # Convert to expected format
            formatted_results = []
            for result in results:
                if hasattr(result, 'id'):
                    formatted_results.append({
                        'file_id': result.id,
                        'score': result.score,
                        'fragment': {
                            'content': result.content,
                            'hits': result.hits,
                            'level': result.level
                        }
                    })
                else:
                    # Handle dict results
                    formatted_results.append({
                        'file_id': result.get('file_id', 'unknown'),
                        'score': result.get('similarity', 0.0),
                        'fragment': {
                            'content': result.get('content', ''),
                            'hits': result.get('hits', 0),
                            'level': result.get('level', 0)
                        }
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"⚠️  Embedding search failed: {e}, using analysis search")
            return self._find_relevant_with_analysis(query, max_results)
    
    def _find_relevant_with_analysis(self, query: str, max_results: int) -> List[Dict]:
        """Find fragments using content analysis (fallback method)."""
        try:
            query_analysis = self.analyze_content(query)
            query_words = set(query_analysis['common_words'])
            query_emotions = query_analysis['emotion_scores']
            
            scored_fragments = []
        except Exception as e:
            print(f"❌ Error in find_relevant_fragments setup: {e}")
            return []
        
        for file_id, fragment in self.file_registry.items():
            try:
                if 'split_into' in fragment:
                    continue  # Skip split parent fragments
                
                score = 0
                
                # Word overlap scoring
                fragment_words = set(fragment['analysis']['common_words'])
                word_overlap = len(query_words.intersection(fragment_words))
                score += word_overlap * 10
                
                # Emotion similarity scoring
                fragment_emotions = fragment['analysis']['emotion_scores']
                for emotion, query_score in query_emotions.items():
                    # Ensure query_score is numeric
                    if not isinstance(query_score, (int, float)):
                        continue
                    if query_score > 0.1:  # Only consider significant emotions
                        fragment_score = fragment_emotions.get(emotion, 0)
                        # Ensure fragment_score is numeric
                        if not isinstance(fragment_score, (int, float)):
                            fragment_score = 0
                        if query_score > 0 and fragment_score > 0:
                            similarity = min(query_score, fragment_score) / max(query_score, fragment_score)
                            score += similarity * 5
                
                # Tone similarity scoring
                query_tone = query_analysis['tone_signature']
                fragment_tone = fragment['analysis']['tone_signature']
                for tone, query_score in query_tone.items():
                    # Ensure query_score is numeric
                    if not isinstance(query_score, (int, float)):
                        continue
                    if query_score > 0.1:
                        fragment_score = fragment_tone.get(tone, 0)
                        # Ensure fragment_score is numeric
                        if not isinstance(fragment_score, (int, float)):
                            fragment_score = 0
                        if query_score > 0 and fragment_score > 0:
                            similarity = min(query_score, fragment_score) / max(query_score, fragment_score)
                            score += similarity * 3
                
                # Specialization bonus
                if fragment['specialization'] in ['technical', 'philosophical', 'creative']:
                    score += 2
                
                if score > 0:
                    scored_fragments.append({
                        'file_id': file_id,
                        'score': score,
                        'fragment': fragment
                    })
            except Exception as e:
                print(f"❌ Error processing fragment {file_id}: {e}")
                continue
        
        # Sort by score and return top results
        scored_fragments.sort(key=lambda x: x['score'], reverse=True)
        return scored_fragments[:max_results]

    def get_fragment_content(self, file_id: str) -> Optional[str]:
        """Get content from a fragment"""
        if file_id not in self.file_registry:
            return None
        
        fragment = self.file_registry[file_id]
        
        # Update access tracking
        fragment['access_count'] += 1
        fragment['last_accessed'] = datetime.now().isoformat()
        
        # Save updated fragment
        fragment_file = self.base_dir / f"{file_id}.json"
        with open(fragment_file, 'w') as f:
            json.dump(fragment, f, indent=2)
        
        return fragment['content']

    def get_cache_statistics(self) -> Dict:
        """Get comprehensive cache statistics"""
        total_fragments = len(self.file_registry)
        total_size = sum(f['size'] for f in self.file_registry.values())
        
        # Count by level
        level_counts = {}
        for level in self.current_levels.values():
            level_counts[level] = level_counts.get(level, 0) + 1
        
        # Count by specialization
        specialization_counts = {}
        for fragment in self.file_registry.values():
            spec = fragment['specialization']
            specialization_counts[spec] = specialization_counts.get(spec, 0) + 1
        
        # Count by emotion
        emotion_counts = {}
        for weights in self.emotion_weights.values():
            for emotion, score in weights.items():
                if score > 0.1:
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return {
            'total_fragments': total_fragments,
            'total_size': total_size,
            'average_size': total_size / total_fragments if total_fragments > 0 else 0,
            'level_distribution': level_counts,
            'specialization_distribution': specialization_counts,
            'emotion_distribution': emotion_counts,
            'max_level': max([v for v in self.current_levels.values() if isinstance(v, (int, float))], default=0) if self.current_levels else 0,
            'fragments_ready_for_split': sum(1 for f in self.file_registry.values() if self.should_split(f['file_id']))
        }

    def expand_query_context(self, query: str, max_depth: int = 2, max_fragments: int = 10) -> List[Dict]:
        """Expand query context by finding related fragments through pathfinding"""
        # Find initial relevant fragments
        initial_fragments = self.find_relevant_fragments(query, max_results=5)
        
        if not initial_fragments:
            return []
        
        expanded_fragments = []
        processed = set()
        
        # Start with initial fragments
        for fragment_info in initial_fragments:
            fragment_id = fragment_info['file_id']
            if fragment_id not in processed:
                # Ensure initial fragments have relevance_score
                if 'relevance_score' not in fragment_info:
                    fragment_info['relevance_score'] = 1.0
                if 'depth' not in fragment_info:
                    fragment_info['depth'] = 0
                if 'path_from_original' not in fragment_info:
                    fragment_info['path_from_original'] = [fragment_id]
                
                expanded_fragments.append(fragment_info)
                processed.add(fragment_id)
        
        # Expand through neighbors up to max_depth
        current_depth = 0
        current_fragments = [f['file_id'] for f in initial_fragments]
        
        while current_depth < max_depth and len(expanded_fragments) < max_fragments:
            next_fragments = []
            
            for fragment_id in current_fragments:
                if len(expanded_fragments) >= max_fragments:
                    break
                
                # Get neighbors
                neighbors = self._neighbors(fragment_id)
                
                for neighbor_id in neighbors:
                    if neighbor_id not in processed and len(expanded_fragments) < max_fragments:
                        # Get fragment info
                        if neighbor_id in self.file_registry:
                            fragment = self.file_registry[neighbor_id]
                            
                            # Calculate relevance score based on path distance
                            path_info = self.weighted_shortest_path(fragment_id, neighbor_id)
                            distance_score = 1.0 / (path_info['hops'] + 1) if path_info['hops'] > 0 else 1.0
                            
                            expanded_fragments.append({
                                'file_id': neighbor_id,
                                'content': fragment.get('content', '')[:200] + '...',
                                'specialization': fragment.get('specialization', 'general'),
                                'tags': fragment.get('tags', [])[:5],
                                'relevance_score': distance_score * 0.8,  # Slightly lower for expanded
                                'depth': current_depth + 1,
                                'path_from_original': path_info['path']
                            })
                            
                            processed.add(neighbor_id)
                            next_fragments.append(neighbor_id)
            
            current_fragments = next_fragments
            current_depth += 1
        
        # Sort by relevance score
        expanded_fragments.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return expanded_fragments[:max_fragments]

    def to_graphviz(self, max_fragments: int = 50, include_weights: bool = True) -> str:
        """Export cache as Graphviz DOT format for visualization"""
        dot_lines = ["digraph CARMA_Network {"]
        dot_lines.append("  rankdir=TB;")
        dot_lines.append("  node [shape=box, style=filled, fontname=\"Arial\"];")
        dot_lines.append("  edge [fontname=\"Arial\", fontsize=8];")
        
        # Limit fragments for readability
        fragments_to_show = list(self.file_registry.keys())[:max_fragments]
        
        # Add nodes
        for file_id in fragments_to_show:
            fragment = self.file_registry[file_id]
            level = fragment.get('level', 0)
            specialization = fragment.get('specialization', 'general')
            hit_count = self.hit_weights.get(file_id, 0)
            
            # Color by level
            if level == 0:
                color = "lightblue"
            elif level == 1:
                color = "lightgreen"
            elif level == 2:
                color = "lightyellow"
            else:
                color = "lightcoral"
            
            # Node label
            label = f"{file_id[:8]}\\nL{level}\\n{specialization}\\nHits:{hit_count}"
            dot_lines.append(f'  "{file_id}" [label="{label}", fillcolor="{color}"];')
        
        # Add edges
        for file_id in fragments_to_show:
            if file_id not in self.file_registry:
                continue
                
            fragment = self.file_registry[file_id]
            
            # Parent-child edges (hierarchical)
            for child_id in fragment.get('children', []):
                if child_id in fragments_to_show:
                    dot_lines.append(f'  "{file_id}" -> "{child_id}" [color="blue", label="child"];')
            
            # Semantic cross-links
            for linked_id in self.semantic_links.get(file_id, []):
                if linked_id in fragments_to_show:
                    edge_key = (file_id, linked_id)
                    weight = self.path_weights.get(edge_key, 1.0)
                    weight_label = f"{weight:.2f}" if include_weights else ""
                    dot_lines.append(f'  "{file_id}" -> "{linked_id}" [color="red", style="dashed", label="{weight_label}"];')
        
        dot_lines.append("}")
        return "\n".join(dot_lines)

    def to_networkx(self):
        """Export cache as NetworkX graph for analysis"""
        try:
            import networkx as nx
        except ImportError:
            print("⚠️ NetworkX not available. Install with: pip install networkx")
            return None
        
        G = nx.DiGraph()
        
        # Add nodes with attributes
        for file_id, fragment in self.file_registry.items():
            G.add_node(file_id, **{
                'level': fragment.get('level', 0),
                'specialization': fragment.get('specialization', 'general'),
                'size': fragment.get('size', 0),
                'hit_count': self.hit_weights.get(file_id, 0),
                'tags': fragment.get('tags', []),
                'content_preview': fragment.get('content', '')[:100]
            })
        
        # Add edges with weights
        for file_id, fragment in self.file_registry.items():
            # Parent-child edges
            for child_id in fragment.get('children', []):
                G.add_edge(file_id, child_id, edge_type='hierarchical', weight=1.0)
            
            # Semantic cross-links
            for linked_id in self.semantic_links.get(file_id, []):
                edge_key = (file_id, linked_id)
                weight = self.path_weights.get(edge_key, 1.0)
                G.add_edge(file_id, linked_id, edge_type='semantic', weight=weight)
        
        return G

    def save_visualization(self, filename: str = "carma_network", format: str = "dot"):
        """Save network visualization to file"""
        if format == "dot":
            dot_content = self.to_graphviz()
            with open(f"{filename}.dot", 'w') as f:
                f.write(dot_content)
            print(f"📊 Graphviz DOT saved to {filename}.dot")
            print(f"   Render with: dot -Tpng {filename}.dot -o {filename}.png")
        
        elif format == "networkx":
            G = self.to_networkx()
            if G:
                import networkx as nx
                nx.write_graphml(G, f"{filename}.graphml")
                print(f"📊 NetworkX GraphML saved to {filename}.graphml")
        
        else:
            print(f"❌ Unknown format: {format}")

    def get_network_analysis(self) -> Dict:
        """Get comprehensive network analysis metrics"""
        G = self.to_networkx()
        if not G:
            return {}
        
        import networkx as nx
        
        analysis = {
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'density': nx.density(G),
            'is_connected': nx.is_weakly_connected(G),
            'strongly_connected_components': nx.number_strongly_connected_components(G),
            'weakly_connected_components': nx.number_weakly_connected_components(G),
        }
        
        # Calculate centrality measures
        if G.number_of_nodes() > 1:
            try:
                analysis['betweenness_centrality'] = nx.betweenness_centrality(G)
                analysis['closeness_centrality'] = nx.closeness_centrality(G)
                analysis['pagerank'] = nx.pagerank(G)
                
                # Find most central nodes
                if analysis['betweenness_centrality']:
                    most_central = max(analysis['betweenness_centrality'].items(), key=lambda x: x[1])
                    analysis['most_central_node'] = most_central[0]
                    analysis['max_betweenness'] = most_central[1]
            except Exception as e:
                print(f"⚠️ Centrality calculation failed: {e}")
        
        # Calculate path statistics
        if G.number_of_nodes() > 1:
            try:
                analysis['average_shortest_path_length'] = nx.average_shortest_path_length(G)
                analysis['diameter'] = nx.diameter(G)
            except:
                analysis['average_shortest_path_length'] = float('inf')
                analysis['diameter'] = 0
        
        return analysis

    def create_backup(self, backup_name: str = None) -> str:
        """Create a backup of the entire cache system"""
        if backup_name is None:
            backup_name = f"carma_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = self.base_dir / "backups" / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup file registry
        registry_backup = backup_dir / "file_registry.json"
        with open(registry_backup, 'w') as f:
            json.dump(self.file_registry, f, indent=2)
        
        # Backup semantic links
        links_backup = backup_dir / "semantic_links.json"
        with open(links_backup, 'w') as f:
            json.dump(self.semantic_links, f, indent=2)
        
        # Backup hit weights
        weights_backup = backup_dir / "hit_weights.json"
        with open(weights_backup, 'w') as f:
            json.dump(self.hit_weights, f, indent=2)
        
        # Backup path weights (convert tuple keys to strings)
        path_weights_backup = backup_dir / "path_weights.json"
        path_weights_serializable = {f"{k[0]},{k[1]}": v for k, v in self.path_weights.items()}
        with open(path_weights_backup, 'w') as f:
            json.dump(path_weights_serializable, f, indent=2)
        
        # Backup metrics
        metrics_backup = backup_dir / "metrics.json"
        with open(metrics_backup, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        # Copy all fragment files
        fragments_backup_dir = backup_dir / "fragments"
        fragments_backup_dir.mkdir(exist_ok=True)
        
        for file_id in self.file_registry.keys():
            fragment_file = self.base_dir / f"{file_id}.json"
            if fragment_file.exists():
                import shutil
                shutil.copy2(fragment_file, fragments_backup_dir / f"{file_id}.json")
        
        # Create backup manifest
        manifest = {
            'backup_name': backup_name,
            'timestamp': datetime.now().isoformat(),
            'fragments_count': len(self.file_registry),
            'semantic_links_count': sum(len(links) for links in self.semantic_links.values()),
            'total_size': sum(fragment.get('size', 0) for fragment in self.file_registry.values()),
            'metrics': self.metrics
        }
        
        manifest_file = backup_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"💾 Backup created: {backup_name}")
        print(f"   Fragments: {len(self.file_registry)}")
        print(f"   Semantic links: {sum(len(links) for links in self.semantic_links.values())}")
        print(f"   Total size: {manifest['total_size']} bytes")
        
        return str(backup_dir)
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore cache from backup"""
        backup_dir = self.base_dir / "backups" / backup_name
        
        if not backup_dir.exists():
            print(f"❌ Backup not found: {backup_name}")
            return False
        
        try:
            # Restore file registry
            registry_file = backup_dir / "file_registry.json"
            if registry_file.exists():
                with open(registry_file, 'r') as f:
                    self.file_registry = json.load(f)
            
            # Restore semantic links
            links_file = backup_dir / "semantic_links.json"
            if links_file.exists():
                with open(links_file, 'r') as f:
                    self.semantic_links = json.load(f)
            
            # Restore hit weights
            weights_file = backup_dir / "hit_weights.json"
            if weights_file.exists():
                with open(weights_file, 'r') as f:
                    self.hit_weights = json.load(f)
            
            # Restore path weights (convert string keys back to tuples)
            path_weights_file = backup_dir / "path_weights.json"
            if path_weights_file.exists():
                with open(path_weights_file, 'r') as f:
                    path_weights_serializable = json.load(f)
                self.path_weights = {tuple(k.split(',')): v for k, v in path_weights_serializable.items()}
            
            # Restore metrics
            metrics_file = backup_dir / "metrics.json"
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    self.metrics = json.load(f)
            
            # Restore fragment files
            fragments_backup_dir = backup_dir / "fragments"
            if fragments_backup_dir.exists():
                import shutil
                for fragment_file in fragments_backup_dir.glob("*.json"):
                    shutil.copy2(fragment_file, self.base_dir / fragment_file.name)
            
            print(f"✅ Backup restored: {backup_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to restore backup: {e}")
            return False
    
    def list_backups(self) -> List[Dict]:
        """List available backups"""
        backups_dir = self.base_dir / "backups"
        if not backups_dir.exists():
            return []
        
        backups = []
        for backup_dir in backups_dir.iterdir():
            if backup_dir.is_dir():
                manifest_file = backup_dir / "manifest.json"
                if manifest_file.exists():
                    try:
                        with open(manifest_file, 'r') as f:
                            manifest = json.load(f)
                        backups.append(manifest)
                    except:
                        # Fallback for corrupted manifest
                        backups.append({
                            'backup_name': backup_dir.name,
                            'timestamp': 'unknown',
                            'fragments_count': 0,
                            'semantic_links_count': 0,
                            'total_size': 0
                        })
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)
    
    def check_pii(self) -> Dict:
        """Check for potential PII in cache content"""
        import re
        
        pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        
        pii_found = {
            'total_fragments_checked': len(self.file_registry),
            'fragments_with_pii': 0,
            'pii_types_found': set(),
            'fragments': []
        }
        
        for file_id, fragment in self.file_registry.items():
            content = fragment.get('content', '')
            fragment_pii = {}
            
            for pii_type, pattern in pii_patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    fragment_pii[pii_type] = matches
                    pii_found['pii_types_found'].add(pii_type)
            
            if fragment_pii:
                pii_found['fragments_with_pii'] += 1
                pii_found['fragments'].append({
                    'file_id': file_id,
                    'pii_types': fragment_pii,
                    'content_preview': content[:100] + '...' if len(content) > 100 else content
                })
        
        pii_found['pii_types_found'] = list(pii_found['pii_types_found'])
        return pii_found
    
    def encrypt_at_rest(self, password: str) -> bool:
        """Encrypt cache data at rest (simple implementation)"""
        try:
            import base64
            import hashlib
            from cryptography.fernet import Fernet
            
            # Generate key from password
            key = hashlib.sha256(password.encode()).digest()
            fernet = Fernet(base64.urlsafe_b64encode(key))
            
            # Encrypt file registry
            registry_data = json.dumps(self.file_registry).encode()
            encrypted_registry = fernet.encrypt(registry_data)
            
            with open(self.base_dir / "file_registry.encrypted", 'wb') as f:
                f.write(encrypted_registry)
            
            # Encrypt semantic links
            links_data = json.dumps(self.semantic_links).encode()
            encrypted_links = fernet.encrypt(links_data)
            
            with open(self.base_dir / "semantic_links.encrypted", 'wb') as f:
                f.write(encrypted_links)
            
            print("🔐 Cache encrypted at rest")
            return True
            
        except ImportError:
            print("❌ Encryption requires: pip install cryptography")
            return False
        except Exception as e:
            print(f"❌ Encryption failed: {e}")
            return False
    
    def decrypt_at_rest(self, password: str) -> bool:
        """Decrypt cache data at rest"""
        try:
            import base64
            import hashlib
            from cryptography.fernet import Fernet
            
            # Generate key from password
            key = hashlib.sha256(password.encode()).digest()
            fernet = Fernet(base64.urlsafe_b64encode(key))
            
            # Decrypt file registry
            with open(self.base_dir / "file_registry.encrypted", 'rb') as f:
                encrypted_registry = f.read()
            
            decrypted_registry = fernet.decrypt(encrypted_registry)
            self.file_registry = json.loads(decrypted_registry.decode())
            
            # Decrypt semantic links
            with open(self.base_dir / "semantic_links.encrypted", 'rb') as f:
                encrypted_links = f.read()
            
            decrypted_links = fernet.decrypt(encrypted_links)
            self.semantic_links = json.loads(decrypted_links.decode())
            
            print("🔓 Cache decrypted")
            return True
            
        except ImportError:
            print("❌ Decryption requires: pip install cryptography")
            return False
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return False

    def update_metrics(self):
        """Update all metrics based on current cache state"""
        self.metrics['fragments_total'] = len(self.file_registry)
        
        # Count edges (parent-child + semantic links)
        edges = 0
        for fragment in self.file_registry.values():
            edges += len(fragment.get('children', []))
            edges += len(self.semantic_links.get(fragment['file_id'], []))
        self.metrics['edges_total'] = edges
        
        # Calculate average path length (sample some paths)
        if len(self.file_registry) >= 2:
            total_length = 0
            sample_count = min(10, len(self.file_registry))
            sample_ids = list(self.file_registry.keys())[:sample_count]
            
            for i in range(sample_count):
                for j in range(i+1, sample_count):
                    path = self.shortest_path(sample_ids[i], sample_ids[j])
                    if path:
                        total_length += len(path) - 1
            
            if sample_count > 1:
                self.metrics['avg_path_length'] = total_length / (sample_count * (sample_count - 1) / 2)
        
        # Update cross-links count
        self.metrics['cross_links'] = sum(len(links) for links in self.semantic_links.values())

    def get_cache_statistics(self) -> Dict:
        """Get comprehensive cache statistics"""
        self.update_metrics()
        
        # Calculate hit rate
        total_hits = sum(self.hit_weights.values())
        total_queries = len(self.file_registry) + total_hits
        self.metrics['cache_hit_rate'] = total_hits / total_queries if total_queries > 0 else 0.0
        
        return {
            'total_fragments': self.metrics['fragments_total'],
            'total_edges': self.metrics['edges_total'],
            'avg_path_length': self.metrics['avg_path_length'],
            'cache_hit_rate': self.metrics['cache_hit_rate'],
            'eviction_events': self.metrics['eviction_events'],
            'split_events': self.metrics['split_events'],
            'reinforcement_events': self.metrics['reinforcement_events'],
            'cross_links': self.metrics['cross_links'],
            'max_level': max([v for v in self.current_levels.values() if isinstance(v, (int, float))], default=0) if self.current_levels else 0,
            'total_size': sum(fragment['size'] for fragment in self.file_registry.values())
        }

    def save_registry(self):
        """Save the file registry"""
        registry_file = self.base_dir / "registry.json"
        with open(registry_file, 'w') as f:
            json.dump({
                'file_registry': self.file_registry,
                'fragment_tree': self.fragment_tree,
                'emotion_weights': self.emotion_weights,
                'tone_signatures': self.tone_signatures,
                'current_levels': self.current_levels
            }, f, indent=2)

    def load_registry(self):
        """Load the file registry"""
        registry_file = self.base_dir / "registry.json"
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                data = json.load(f)
                self.file_registry = data.get('file_registry', {})
                self.fragment_tree = data.get('fragment_tree', {})
                self.emotion_weights = data.get('emotion_weights', {})
                self.tone_signatures = data.get('tone_signatures', {})
                self.current_levels = data.get('current_levels', {})

    # --- Networking and Pathfinding ---

    def ping(self, file_id: str) -> Dict:
        """Return minimal header info for a given file id (simulated network ping)."""
        fragment = self.file_registry.get(file_id)
        if not fragment:
            return { 'status': 'not_found', 'file_id': file_id }
        return {
            'status': 'ok',
            'file_id': fragment['file_id'],
            'node_address': fragment.get('node_address'),
            'level': fragment.get('level'),
            'parent_id': fragment.get('parent_id'),
            'children': list(fragment.get('children', [])),
            'ancestors': list(fragment.get('ancestors', [])),
            'size': fragment.get('size')
        }

    def _neighbors(self, file_id: str) -> List[str]:
        """Return neighboring node ids (parent + children + semantic links)."""
        fragment = self.file_registry.get(file_id)
        if not fragment:
            return []
        neighbors: List[str] = []
        
        # Parent-child relationships
        parent_id = fragment.get('parent_id')
        if parent_id:
            neighbors.append(parent_id)
        neighbors.extend(fragment.get('children', []))
        
        # Semantic cross-links
        neighbors.extend(self.semantic_links.get(file_id, []))
        
        return neighbors

    def shortest_path(self, start_id: str, target_id: str) -> List[str]:
        """Compute shortest path between two nodes via BFS (unweighted)."""
        if start_id == target_id:
            return [start_id]
        if start_id not in self.file_registry or target_id not in self.file_registry:
            return []
        from collections import deque
        queue = deque([start_id])
        visited = { start_id: None }
        while queue:
            node = queue.popleft()
            for neighbor in self._neighbors(node):
                if neighbor not in visited:
                    visited[neighbor] = node
                    if neighbor == target_id:
                        # Reconstruct path
                        path = [target_id]
                        cur = target_id
                        while visited[cur] is not None:
                            cur = visited[cur]
                            path.append(cur)
                        path.reverse()
                        return path
                    queue.append(neighbor)
        return []

    def weighted_shortest_path(self, start_id: str, target_id: str) -> Dict:
        """Compute shortest weighted path using Dijkstra's algorithm"""
        if start_id == target_id:
            return {'path': [start_id], 'cost': 0.0, 'hops': 0}
        
        if start_id not in self.file_registry or target_id not in self.file_registry:
            return {'path': [], 'cost': float('inf'), 'hops': 0}
        
        import heapq
        
        # Priority queue: (cost, node, path)
        pq = [(0.0, start_id, [start_id])]
        visited = set()
        costs = {start_id: 0.0}
        
        while pq:
            current_cost, current_node, current_path = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == target_id:
                return {
                    'path': current_path,
                    'cost': current_cost,
                    'hops': len(current_path) - 1
                }
            
            # Explore neighbors
            for neighbor in self._neighbors(current_node):
                if neighbor in visited:
                    continue
                
                # Calculate edge weight (lower is better)
                edge_key = (current_node, neighbor)
                edge_weight = self.path_weights.get(edge_key, 1.0)
                
                # Invert weight so higher weights = lower cost
                edge_cost = 1.0 / max(edge_weight, 0.1)
                new_cost = current_cost + edge_cost
                
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    new_path = current_path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, new_path))
        
        return {'path': [], 'cost': float('inf'), 'hops': 0}

    def random_probe_fastest_path(self, target_id: str, probes: int = 3) -> Dict:
        """Randomly probe up to N start nodes and pick the shortest path heuristic.

        Heuristic:
          - Pick first random node, compute path length L1.
          - Pick second random node, get L2. If shorter, prefer it; else do third probe.
          - If third probe L3 shorter than best so far, pick it; else keep the best among the tested.
        """
        if target_id not in self.file_registry:
            return { 'status': 'target_not_found' }
        node_ids = list(self.file_registry.keys())
        if not node_ids:
            return { 'status': 'empty' }
        best = { 'path': [], 'length': float('inf'), 'start': None }
        attempts = 0
        tested_starts: Set[str] = set()
        while attempts < probes and len(tested_starts) < len(node_ids):
            start_id = random.choice(node_ids)
            if start_id in tested_starts:
                continue
            tested_starts.add(start_id)
            path = self.shortest_path(start_id, target_id)
            length = len(path) if path else float('inf')
            if length < best['length']:
                best = { 'path': path, 'length': length, 'start': start_id }
            attempts += 1
        best['status'] = 'ok' if best['path'] else 'no_path'
        return best

    # --- Embedding System ---
    
    def ensure_embedding_index(self):
        """Build FAISS index for all fragments with embeddings."""
        try:
            import faiss
        except ImportError:
            print("⚠️  FAISS not available, using simple similarity search")
            return
        
        # Collect all fragments with embeddings
        embeddings = []
        fragment_ids = []
        
        for frag_id, frag_data in self.file_registry.items():
            if 'embedding' in frag_data and frag_data['embedding'] is not None:
                embeddings.append(frag_data['embedding'])
                fragment_ids.append(frag_id)
        
        if not embeddings:
            print("❌ No embeddings found to build index")
            return
        
        # Convert to numpy array
        import numpy as np
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Build FAISS index
        dimension = len(embeddings[0])
        self.embedding_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.embedding_index.add(embeddings_array)
        
        # Store mapping from index to fragment ID
        self.embedding_to_fragment = fragment_ids
        
        print(f"✅ FAISS index built: {len(embeddings)} embeddings, dimension {dimension}")
    
    def find_relevant(self, query_embedding, topk=3):
        """Find relevant fragments using FAISS index."""
        if self.embedding_index is None:
            print("⚠️  No embedding index built, using simple search")
            return self.find_relevant_fragments("", max_results=topk)
        
        try:
            import numpy as np
            
            # Normalize query embedding
            query_array = np.array([query_embedding]).astype('float32')
            query_norm = np.linalg.norm(query_array)
            if query_norm > 0:
                query_array = query_array / query_norm
            
            # Search index
            scores, indices = self.embedding_index.search(query_array, topk)
            
            # Convert to fragment data
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.embedding_to_fragment):
                    frag_id = self.embedding_to_fragment[idx]
                    frag_data = self.file_registry.get(frag_id, {})
                    
                    # Create result object
                    class FragmentResult:
                        def __init__(self, frag_id, frag_data, score):
                            self.id = frag_id
                            self.content = frag_data.get('content', '')
                            self.hits = frag_data.get('hits', 0)
                            self.level = frag_data.get('level', 0)
                            self.score = float(score)
                    
                    results.append(FragmentResult(frag_id, frag_data, score))
            
            return results
            
        except Exception as e:
            print(f"❌ FAISS search failed: {e}")
            return self.find_relevant_fragments("", max_results=topk)

if __name__ == "__main__":
    # Example usage
    cache = FractalMyceliumCache()
    
    # Add some test content
    test_content = """
    This is a technical document about neural networks and machine learning.
    It discusses various algorithms, training methods, and optimization techniques.
    The content is quite detailed and technical, covering topics like backpropagation,
    gradient descent, and convolutional neural networks.
    """
    
    file_id = cache.add_content(test_content)
    print(f"Created fragment: {file_id}")
    
    # Check statistics
    stats = cache.get_cache_statistics()
    print(f"Cache stats: {stats}")

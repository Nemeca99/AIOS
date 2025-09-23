#!/usr/bin/env python3
"""
CARMA Meta-Memory System
Hierarchical memory organization with super-fragments and episodic/semantic layers
"""

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from fractal_mycelium_cache import FractalMyceliumCache

class CARMAMetaMemory:
    def __init__(self, cache: FractalMyceliumCache):
        self.cache = cache
        self.super_fragments = {}  # super_fragment_id -> metadata
        self.episodic_memory = {}  # episode_id -> episode_data
        self.semantic_memory = {}  # concept_id -> semantic_data
        self.memory_hierarchy = {}  # fragment_id -> hierarchy_level
        
        # Meta-memory parameters
        self.compression_threshold = 0.8  # Compress when 80% of fragments are related
        self.semantic_clustering_threshold = 0.6  # Semantic similarity for clustering
        self.episodic_decay_rate = 0.1  # Decay rate for episodic memories
        self.semantic_consolidation_threshold = 5  # Episodes needed for semantic consolidation
        
        print("🧠 CARMA Meta-Memory System Initialized")
        print(f"   Compression threshold: {self.compression_threshold}")
        print(f"   Semantic clustering: {self.semantic_clustering_threshold}")
        print(f"   Episodic decay rate: {self.episodic_decay_rate}")
    
    def create_super_fragment(self, cluster: List[str], compression_ratio: float = None) -> str:
        """Create a super-fragment from a cluster of related fragments"""
        if len(cluster) < 3:
            return None
        
        # Generate super-fragment ID
        super_id = f"super_{int(time.time())}_{len(cluster)}"
        
        # Collect cluster data
        cluster_data = self._analyze_cluster(cluster)
        
        # Create hierarchical content
        super_content = self._generate_super_content(cluster, cluster_data)
        
        # Add to cache
        file_id = self.cache.add_content(super_content)
        
        # Create super-fragment metadata
        super_fragment = {
            'id': super_id,
            'file_id': file_id,
            'cluster_members': cluster,
            'cluster_size': len(cluster),
            'compression_ratio': compression_ratio or len(cluster),
            'created_at': datetime.now().isoformat(),
            'hierarchy_level': 1,
            'semantic_theme': cluster_data['semantic_theme'],
            'emotion_profile': cluster_data['emotion_profile'],
            'key_concepts': cluster_data['key_concepts'],
            'access_count': 0,
            'last_accessed': datetime.now().isoformat()
        }
        
        # Store super-fragment
        self.super_fragments[super_id] = super_fragment
        
        # Update hierarchy mapping
        for fragment_id in cluster:
            self.memory_hierarchy[fragment_id] = {
                'level': 1,
                'super_fragment': super_id,
                'parent': file_id
            }
        
        print(f"🧠 Created super-fragment: {super_id} ({len(cluster)} fragments)")
        return super_id
    
    def _analyze_cluster(self, cluster: List[str]) -> Dict:
        """Analyze a cluster of fragments to extract semantic themes"""
        cluster_content = []
        cluster_tags = set()
        cluster_emotions = {}
        cluster_concepts = set()
        
        for fragment_id in cluster:
            if fragment_id in self.cache.file_registry:
                fragment = self.cache.file_registry[fragment_id]
                cluster_content.append(fragment.get('content', ''))
                cluster_tags.update(fragment.get('tags', []))
                
                # Extract emotions
                emotions = fragment.get('analysis', {}).get('emotion_scores', {})
                for emotion, score in emotions.items():
                    cluster_emotions[emotion] = cluster_emotions.get(emotion, 0) + score
                
                # Extract concepts (simple keyword extraction)
                content = fragment.get('content', '').lower()
                concepts = self._extract_concepts(content)
                cluster_concepts.update(concepts)
        
        # Normalize emotions
        for emotion in cluster_emotions:
            cluster_emotions[emotion] /= len(cluster)
        
        # Determine semantic theme
        semantic_theme = self._determine_semantic_theme(cluster_content, cluster_tags)
        
        return {
            'semantic_theme': semantic_theme,
            'emotion_profile': cluster_emotions,
            'key_concepts': list(cluster_concepts),
            'content_preview': ' '.join(cluster_content)[:200] + '...'
        }
    
    def _extract_concepts(self, content: str) -> set:
        """Extract key concepts from content"""
        # Simple concept extraction (can be enhanced with NLP)
        concepts = set()
        words = content.split()
        
        # Extract important words (length > 4, not common words)
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'man', 'men', 'put', 'say', 'she', 'too', 'use'}
        
        for word in words:
            clean_word = word.strip('.,!?;:"()[]{}').lower()
            if len(clean_word) > 4 and clean_word not in common_words:
                concepts.add(clean_word)
        
        return concepts
    
    def _determine_semantic_theme(self, content_list: List[str], tags: set) -> str:
        """Determine the semantic theme of a cluster"""
        # Count theme keywords
        theme_keywords = {
            'technology': ['computer', 'software', 'programming', 'algorithm', 'data', 'system', 'network', 'digital'],
            'science': ['research', 'study', 'experiment', 'theory', 'hypothesis', 'analysis', 'discovery', 'method'],
            'learning': ['learn', 'teach', 'education', 'knowledge', 'skill', 'training', 'study', 'understand'],
            'consciousness': ['aware', 'conscious', 'mind', 'brain', 'thought', 'memory', 'perception', 'cognition'],
            'artificial_intelligence': ['ai', 'machine', 'neural', 'intelligence', 'artificial', 'model', 'algorithm', 'learning']
        }
        
        theme_scores = {}
        all_content = ' '.join(content_list).lower()
        
        for theme, keywords in theme_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_content)
            theme_scores[theme] = score
        
        # Also check tags
        for tag in tags:
            tag_lower = tag.lower()
            for theme, keywords in theme_keywords.items():
                if any(keyword in tag_lower for keyword in keywords):
                    theme_scores[theme] = theme_scores.get(theme, 0) + 1
        
        # Return theme with highest score
        if theme_scores:
            return max(theme_scores.items(), key=lambda x: x[1])[0]
        else:
            return 'general'
    
    def _generate_super_content(self, cluster: List[str], cluster_data: Dict) -> str:
        """Generate hierarchical content for super-fragment"""
        super_content = f"SUPER-FRAGMENT: {cluster_data['semantic_theme'].upper()}\n"
        super_content += f"Compression Ratio: {len(cluster)}:1\n"
        super_content += f"Key Concepts: {', '.join(cluster_data['key_concepts'][:10])}\n"
        super_content += f"Emotion Profile: {cluster_data['emotion_profile']}\n"
        super_content += f"Created: {datetime.now().isoformat()}\n\n"
        
        super_content += "HIERARCHICAL CONTENT:\n"
        super_content += "=" * 50 + "\n\n"
        
        # Add compressed content from each fragment
        for i, fragment_id in enumerate(cluster):
            if fragment_id in self.cache.file_registry:
                fragment = self.cache.file_registry[fragment_id]
                content = fragment.get('content', '')
                super_content += f"[{i+1}] {content[:100]}...\n\n"
        
        super_content += "END SUPER-FRAGMENT"
        return super_content
    
    def create_episodic_memory(self, event_data: Dict) -> str:
        """Create an episodic memory from event data"""
        # Add small random delay to ensure unique timestamps
        time.sleep(0.01)
        episode_id = f"episode_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        
        episode = {
            'id': episode_id,
            'timestamp': datetime.now().isoformat(),
            'event_type': event_data.get('type', 'general'),
            'content': event_data.get('content', ''),
            'context': event_data.get('context', {}),
            'emotional_valence': event_data.get('emotional_valence', 0.0),
            'importance': event_data.get('importance', 0.5),
            'access_count': 0,
            'last_accessed': datetime.now().isoformat(),
            'decay_factor': 1.0
        }
        
        self.episodic_memory[episode_id] = episode
        
        # Add to cache
        episodic_content = f"EPISODIC MEMORY: {episode['event_type']}\n"
        episodic_content += f"Timestamp: {episode['timestamp']}\n"
        episodic_content += f"Valence: {episode['emotional_valence']}\n"
        episodic_content += f"Importance: {episode['importance']}\n\n"
        episodic_content += f"Content: {episode['content']}\n"
        
        file_id = self.cache.add_content(episodic_content)
        episode['file_id'] = file_id
        
        print(f"🧠 Created episodic memory: {episode_id}")
        return episode_id
    
    def consolidate_episodic_to_semantic(self, theme: str) -> str:
        """Consolidate episodic memories into semantic knowledge"""
        # Find related episodes
        related_episodes = []
        for episode_id, episode in self.episodic_memory.items():
            if (theme.lower() in episode['content'].lower() or 
                theme.lower() in episode['event_type'].lower()):
                related_episodes.append(episode)
        
        if len(related_episodes) < self.semantic_consolidation_threshold:
            return None
        
        # Create semantic memory
        concept_id = f"semantic_{theme}_{int(time.time())}"
        
        # Consolidate episode data
        consolidated_content = f"SEMANTIC KNOWLEDGE: {theme.upper()}\n"
        consolidated_content += f"Consolidated from {len(related_episodes)} episodes\n"
        consolidated_content += f"Created: {datetime.now().isoformat()}\n\n"
        
        # Extract patterns and insights
        patterns = self._extract_patterns(related_episodes)
        consolidated_content += f"Patterns: {patterns}\n\n"
        
        # Add consolidated knowledge
        for i, episode in enumerate(related_episodes[:5]):  # Top 5 episodes
            consolidated_content += f"[Episode {i+1}] {episode['content'][:100]}...\n"
        
        # Add to cache
        file_id = self.cache.add_content(consolidated_content)
        
        semantic_memory = {
            'id': concept_id,
            'file_id': file_id,
            'theme': theme,
            'source_episodes': [ep['id'] for ep in related_episodes],
            'consolidation_count': len(related_episodes),
            'created_at': datetime.now().isoformat(),
            'access_count': 0,
            'last_accessed': datetime.now().isoformat()
        }
        
        self.semantic_memory[concept_id] = semantic_memory
        
        print(f"🧠 Consolidated semantic memory: {concept_id} ({len(related_episodes)} episodes)")
        return concept_id
    
    def _extract_patterns(self, episodes: List[Dict]) -> str:
        """Extract patterns from related episodes"""
        # Simple pattern extraction
        common_words = set()
        emotional_valences = []
        importance_scores = []
        
        for episode in episodes:
            words = episode['content'].lower().split()
            common_words.update(words)
            emotional_valences.append(episode['emotional_valence'])
            importance_scores.append(episode['importance'])
        
        # Find most common words
        word_counts = {}
        for word in common_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate averages
        avg_valence = sum(emotional_valences) / len(emotional_valences)
        avg_importance = sum(importance_scores) / len(importance_scores)
        
        patterns = f"Common themes: {[word for word, count in top_words]}, "
        patterns += f"Avg valence: {avg_valence:.2f}, Avg importance: {avg_importance:.2f}"
        
        return patterns
    
    def query_hierarchical_memory(self, query: str, include_super_fragments: bool = True) -> List[Dict]:
        """Query both detailed and abstract memory levels"""
        results = []
        
        # Query detailed fragments
        detailed_results = self.cache.find_relevant_fragments(query, max_results=5)
        for result in detailed_results:
            result['memory_type'] = 'detailed'
            result['hierarchy_level'] = 0
            results.append(result)
        
        # Query super-fragments if enabled
        if include_super_fragments:
            super_results = self._query_super_fragments(query)
            for result in super_results:
                result['memory_type'] = 'super_fragment'
                result['hierarchy_level'] = 1
                results.append(result)
        
        # Query episodic memories
        episodic_results = self._query_episodic_memories(query)
        for result in episodic_results:
            result['memory_type'] = 'episodic'
            result['hierarchy_level'] = 0
            results.append(result)
        
        # Query semantic memories
        semantic_results = self._query_semantic_memories(query)
        for result in semantic_results:
            result['memory_type'] = 'semantic'
            result['hierarchy_level'] = 1
            results.append(result)
        
        # Sort by relevance and hierarchy
        results.sort(key=lambda x: (x.get('relevance_score', 0), -x.get('hierarchy_level', 0)), reverse=True)
        
        return results[:10]  # Return top 10 results
    
    def _query_super_fragments(self, query: str) -> List[Dict]:
        """Query super-fragments for relevant content"""
        results = []
        query_lower = query.lower()
        
        for super_id, super_fragment in self.super_fragments.items():
            # Check semantic theme
            if query_lower in super_fragment['semantic_theme'].lower():
                results.append({
                    'file_id': super_fragment['file_id'],
                    'content': f"Super-fragment: {super_fragment['semantic_theme']}",
                    'relevance_score': 0.9,
                    'super_fragment_id': super_id,
                    'cluster_size': super_fragment['cluster_size']
                })
                continue
            
            # Check key concepts
            for concept in super_fragment['key_concepts']:
                if query_lower in concept.lower():
                    results.append({
                        'file_id': super_fragment['file_id'],
                        'content': f"Super-fragment: {super_fragment['semantic_theme']}",
                        'relevance_score': 0.7,
                        'super_fragment_id': super_id,
                        'cluster_size': super_fragment['cluster_size']
                    })
                    break
        
        return results
    
    def _query_episodic_memories(self, query: str) -> List[Dict]:
        """Query episodic memories for relevant content"""
        results = []
        query_lower = query.lower()
        
        for episode_id, episode in self.episodic_memory.items():
            if (query_lower in episode['content'].lower() or 
                query_lower in episode['event_type'].lower()):
                
                # Calculate relevance based on importance and recency
                time_diff = (datetime.now() - datetime.fromisoformat(episode['timestamp'])).days
                recency_factor = max(0.1, 1.0 - (time_diff * self.episodic_decay_rate))
                relevance = episode['importance'] * recency_factor
                
                results.append({
                    'file_id': episode['file_id'],
                    'content': episode['content'][:100] + '...',
                    'relevance_score': relevance,
                    'episode_id': episode_id,
                    'timestamp': episode['timestamp']
                })
        
        return results
    
    def _query_semantic_memories(self, query: str) -> List[Dict]:
        """Query semantic memories for relevant content"""
        results = []
        query_lower = query.lower()
        
        for concept_id, semantic in self.semantic_memory.items():
            if query_lower in semantic['theme'].lower():
                results.append({
                    'file_id': semantic['file_id'],
                    'content': f"Semantic knowledge: {semantic['theme']}",
                    'relevance_score': 0.8,
                    'concept_id': concept_id,
                    'consolidation_count': semantic['consolidation_count']
                })
        
        return results
    
    def get_memory_statistics(self) -> Dict:
        """Get comprehensive memory statistics"""
        return {
            'total_fragments': len(self.cache.file_registry),
            'super_fragments': len(self.super_fragments),
            'episodic_memories': len(self.episodic_memory),
            'semantic_memories': len(self.semantic_memory),
            'hierarchy_levels': len(set(h['level'] for h in self.memory_hierarchy.values())),
            'compression_ratio': sum(sf['compression_ratio'] for sf in self.super_fragments.values()) / max(1, len(self.super_fragments)),
            'episodic_decay_events': sum(1 for ep in self.episodic_memory.values() 
                                       if (datetime.now() - datetime.fromisoformat(ep['timestamp'])).days > 30),
            'semantic_consolidation_rate': len(self.semantic_memory) / max(1, len(self.episodic_memory))
        }
    
    def auto_consolidate_memories(self):
        """Automatically consolidate memories based on patterns"""
        # Find clusters that could become super-fragments
        clusters = self._identify_consolidation_clusters()
        
        consolidated = 0
        for cluster in clusters:
            if len(cluster) >= 3:
                super_id = self.create_super_fragment(cluster)
                if super_id:
                    consolidated += 1
        
        # Consolidate episodic memories to semantic
        themes = self._identify_episodic_themes()
        for theme in themes:
            self.consolidate_episodic_to_semantic(theme)
        
        print(f"🧠 Auto-consolidated {consolidated} super-fragments and {len(themes)} semantic themes")
        return consolidated
    
    def _identify_consolidation_clusters(self) -> List[List[str]]:
        """Identify clusters of fragments that could be consolidated"""
        # Simple clustering based on semantic similarity
        clusters = []
        processed = set()
        
        for fragment_id, fragment in self.cache.file_registry.items():
            if fragment_id in processed:
                continue
            
            cluster = [fragment_id]
            processed.add(fragment_id)
            
            # Find similar fragments
            for other_id, other_fragment in self.cache.file_registry.items():
                if other_id in processed:
                    continue
                
                similarity = self._calculate_semantic_similarity(fragment, other_fragment)
                if similarity > self.semantic_clustering_threshold:
                    cluster.append(other_id)
                    processed.add(other_id)
            
            if len(cluster) >= 3:
                clusters.append(cluster)
        
        return clusters
    
    def _calculate_semantic_similarity(self, frag1: Dict, frag2: Dict) -> float:
        """Calculate semantic similarity between two fragments"""
        # Simple similarity based on tags and content
        tags1 = set(frag1.get('tags', []))
        tags2 = set(frag2.get('tags', []))
        
        if not tags1 or not tags2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(tags1 & tags2)
        union = len(tags1 | tags2)
        
        return intersection / union if union > 0 else 0.0
    
    def _identify_episodic_themes(self) -> List[str]:
        """Identify themes from episodic memories for consolidation"""
        theme_counts = {}
        
        for episode in self.episodic_memory.values():
            content = episode['content'].lower()
            
            # Check for common themes
            themes = ['learning', 'technology', 'science', 'consciousness', 'ai', 'memory', 'cognition']
            for theme in themes:
                if theme in content:
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Return themes with enough episodes
        return [theme for theme, count in theme_counts.items() 
                if count >= self.semantic_consolidation_threshold]

def main():
    """Test the meta-memory system"""
    print("🧠 Testing CARMA Meta-Memory System")
    print("=" * 50)
    
    # Create cache and meta-memory
    cache = FractalMyceliumCache("meta_memory_test")
    meta_memory = CARMAMetaMemory(cache)
    
    # Add test content
    test_content = [
        "Machine learning algorithms learn patterns from data",
        "Neural networks are inspired by biological neurons",
        "Deep learning uses multiple layers for complex patterns",
        "Data science combines statistics and programming",
        "Software engineering applies systematic approaches"
    ]
    
    fragment_ids = []
    for content in test_content:
        file_id = cache.add_content(content)
        fragment_ids.append(file_id)
    
    print(f"Added {len(fragment_ids)} test fragments")
    
    # Create super-fragment
    super_id = meta_memory.create_super_fragment(fragment_ids[:3])
    print(f"Created super-fragment: {super_id}")
    
    # Create episodic memories
    episodes = [
        {"type": "learning", "content": "Learned about machine learning concepts", "importance": 0.8},
        {"type": "learning", "content": "Studied neural network architectures", "importance": 0.9},
        {"type": "learning", "content": "Explored deep learning applications", "importance": 0.7}
    ]
    
    for episode in episodes:
        episode_id = meta_memory.create_episodic_memory(episode)
        print(f"Created episodic memory: {episode_id}")
    
    # Consolidate episodic to semantic
    semantic_id = meta_memory.consolidate_episodic_to_semantic("learning")
    print(f"Consolidated semantic memory: {semantic_id}")
    
    # Query hierarchical memory
    print("\n🔍 Querying hierarchical memory...")
    results = meta_memory.query_hierarchical_memory("machine learning")
    
    for i, result in enumerate(results[:5]):
        content = result.get('content', 'No content')[:50]
        print(f"  {i+1}. {result['memory_type']}: {content}... (score: {result.get('relevance_score', 0):.3f})")
    
    # Get statistics
    stats = meta_memory.get_memory_statistics()
    print(f"\n📊 Memory Statistics:")
    print(f"  Total fragments: {stats['total_fragments']}")
    print(f"  Super-fragments: {stats['super_fragments']}")
    print(f"  Episodic memories: {stats['episodic_memories']}")
    print(f"  Semantic memories: {stats['semantic_memories']}")
    print(f"  Compression ratio: {stats['compression_ratio']:.2f}")
    
    print("\n✅ Meta-memory system test complete!")

if __name__ == "__main__":
    main()

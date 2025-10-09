#!/usr/bin/env python3
"""
OPTIMIZED CARMA CORE - Eliminates 76-second bottleneck
Fast, efficient memory retrieval without API overhead
"""

import time
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class FastFragmentResult:
    """Lightweight fragment result"""
    id: str
    content: str
    score: float
    source: str = "fragment"

@dataclass
class FastMemoryResult:
    """Lightweight memory result"""
    id: str
    content: str
    score: float
    source: str = "conversation"

class OptimizedCARMA:
    """
    Optimized CARMA system that eliminates the 76-second bottleneck
    by using fast, local-only operations instead of API calls
    """
    
    def __init__(self, base_dir: str = "data_core/FractalCache"):
        self.base_dir = Path(base_dir)
        self.fragment_cache = {}
        self.conversation_cache = {}
        self.embedding_cache = {}
        
        # Load fragment registry (fast, no API calls)
        self._load_fragment_registry()
        
        # Load recent conversations (fast, no API calls)
        self._load_recent_conversations()
        
        print(f"🚀 Optimized CARMA initialized")
        print(f"   Fragments: {len(self.fragment_cache)}")
        print(f"   Conversations: {len(self.conversation_cache)}")
    
    def _load_fragment_registry(self):
        """Load fragment registry without API calls"""
        try:
            registry_file = self.base_dir / "registry.json"
            if registry_file.exists():
                with open(registry_file, 'r', encoding='utf-8') as f:
                    registry = json.load(f)
                
                # Load only essential data, no embeddings
                for frag_id, frag_data in registry.items():
                    self.fragment_cache[frag_id] = {
                        'content': frag_data.get('content', ''),
                        'metadata': frag_data.get('metadata', {}),
                        'timestamp': frag_data.get('timestamp', 0)
                    }
                    
        except Exception as e:
            print(f"⚠️ Could not load fragment registry: {e}")
    
    def _load_recent_conversations(self):
        """Load recent conversations without API calls"""
        try:
            conversation_dir = Path("data_core/conversations")
            if conversation_dir.exists():
                # Load only last 10 conversations (not 50!)
                conversation_files = list(conversation_dir.glob("conversation_*.json"))[-10:]
                
                for conv_file in conversation_files:
                    try:
                        with open(conv_file, 'r', encoding='utf-8') as f:
                            conv_data = json.load(f)
                        
                        conv_id = conv_data.get('id', 'unknown')
                        messages = conv_data.get('messages', [])
                        
                        # Store only recent messages (last 5 per conversation)
                        recent_messages = messages[-5:] if len(messages) > 5 else messages
                        
                        self.conversation_cache[conv_id] = {
                            'messages': recent_messages,
                            'timestamp': conv_data.get('timestamp', 0)
                        }
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Could not load conversations: {e}")
    
    def process_query(self, query: str, context: Dict = None) -> Dict:
        """
        FAST process_query - eliminates 76-second bottleneck
        
        Returns:
            Dict with fragments_found and conversation_memories_found
        """
        start_time = time.time()
        
        # FAST keyword-based search (no API calls!)
        fragments_found = self._fast_fragment_search(query)
        
        # FAST conversation search (no API calls!)
        conversation_memories = self._fast_conversation_search(query)
        
        processing_time = time.time() - start_time
        
        result = {
            'fragments_found': len(fragments_found),
            'conversation_memories_found': conversation_memories,
            'processing_time': processing_time,
            'method': 'optimized_fast'
        }
        
        print(f"⚡ Fast CARMA: {processing_time:.3f}s (vs 76s bottleneck)")
        
        return result
    
    def _fast_fragment_search(self, query: str, topk: int = 3) -> List[FastFragmentResult]:
        """
        Fast keyword-based fragment search (no embeddings!)
        Uses simple text matching instead of API calls
        """
        query_words = set(query.lower().split())
        results = []
        
        for frag_id, frag_data in self.fragment_cache.items():
            content = frag_data.get('content', '').lower()
            content_words = set(content.split())
            
            # Calculate simple word overlap score
            overlap = len(query_words.intersection(content_words))
            if overlap > 0:
                score = overlap / len(query_words)  # Normalize by query length
                results.append(FastFragmentResult(
                    id=frag_id,
                    content=frag_data.get('content', '')[:200],  # Truncate for speed
                    score=score
                ))
        
        # Sort by score and return top results
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:topk]
    
    def _fast_conversation_search(self, query: str, topk: int = 2) -> List[FastMemoryResult]:
        """
        Fast keyword-based conversation search (no embeddings!)
        Uses simple text matching instead of API calls
        """
        query_words = set(query.lower().split())
        results = []
        
        for conv_id, conv_data in self.conversation_cache.items():
            messages = conv_data.get('messages', [])
            
            for message in messages:
                content = message.get('content', '').lower()
                if not content:
                    continue
                
                content_words = set(content.split())
                
                # Calculate simple word overlap score
                overlap = len(query_words.intersection(content_words))
                if overlap > 0:
                    score = overlap / len(query_words)  # Normalize by query length
                    results.append(FastMemoryResult(
                        id=f"conv_{conv_id}_{message.get('id', 'unknown')}",
                        content=content[:200],  # Truncate for speed
                        score=score
                    ))
        
        # Sort by score and return top results
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:topk]
    
    def get_fast_summary(self, query: str) -> str:
        """
        Get a fast summary of relevant memories without API calls
        """
        fragments = self._fast_fragment_search(query, topk=2)
        conversations = self._fast_conversation_search(query, topk=1)
        
        summary_parts = []
        
        if fragments:
            summary_parts.append(f"Found {len(fragments)} relevant fragments")
        
        if conversations:
            summary_parts.append(f"Found {len(conversations)} relevant conversation memories")
        
        if not summary_parts:
            return "No relevant memories found"
        
        return "; ".join(summary_parts)

# Test the optimized CARMA
if __name__ == "__main__":
    print("🧪 Testing Optimized CARMA...")
    
    carma = OptimizedCARMA()
    
    test_queries = [
        "Hello",
        "What is consciousness?",
        "Analyze the philosophical implications of artificial consciousness"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: {query}")
        result = carma.process_query(query)
        print(f"   Result: {result}")
        summary = carma.get_fast_summary(query)
        print(f"   Summary: {summary}")

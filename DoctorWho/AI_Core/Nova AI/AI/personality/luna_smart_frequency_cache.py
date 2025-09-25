"""
Luna Smart Frequency-Based Cache System
- Short-term cache with usage frequency tracking
- Automatic pruning based on mean frequency
- Long-term database promotion for persistent patterns
"""
import sqlite3
import numpy as np
import requests
import json
import time
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import statistics

class LunaSmartFrequencyCache:
    def __init__(self, cache_size_limit_mb: float = 50.0):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.embeddings_url = "http://localhost:1234/v1/embeddings"
        
        # Model assignments
        self.embedding_model = "text-embedding-mlabonne_qwen3-0.6b-abliterated"
        self.chat_model = "wizardlm-2-7b-abliterated@q8_0"
        
        # Database and cache paths
        self.db_path = "F:/AI_Datasets/AIOS_Database/database/conversations.db"
        self.cache_file = Path("AI/personality/embedder_cache/smart_frequency_cache.json")
        self.cache_file.parent.mkdir(exist_ok=True)
        
        # Cache settings
        self.cache_size_limit_mb = cache_size_limit_mb
        self.cache_size_limit_bytes = cache_size_limit_mb * 1024 * 1024
        
        # Load cache with frequency tracking
        self.cache = self._load_cache()
        
        print(f"🧠 SMART FREQUENCY CACHE INITIALIZED")
        print(f"📊 Embedding Model: {self.embedding_model}")
        print(f"💬 Chat Model: {self.chat_model}")
        print(f"🗄️ Database: {self.db_path}")
        print(f"💾 Cache: {len(self.cache)} entries")
        print(f"📏 Size Limit: {cache_size_limit_mb}MB")
        print(f"📊 Current Size: {self._get_cache_size_mb():.1f}MB")
    
    def _load_cache(self) -> Dict:
        """Load cache with frequency tracking"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    # Ensure all entries have frequency count
                    for key, value in cache.items():
                        if isinstance(value, list):  # Old format (just embedding)
                            cache[key] = {
                                "embedding": value,
                                "frequency": 1,
                                "last_used": datetime.now().isoformat()
                            }
                        elif "frequency" not in value:  # Missing frequency
                            value["frequency"] = 1
                            value["last_used"] = datetime.now().isoformat()
                    
                    print(f"📥 Loaded cache: {len(cache)} entries")
                    return cache
            return {}
        except Exception as e:
            print(f"⚠️ Cache load error: {e}")
            return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"⚠️ Cache save error: {e}")
    
    def _get_cache_size_mb(self) -> float:
        """Get current cache file size in MB"""
        try:
            if self.cache_file.exists():
                size_bytes = self.cache_file.stat().st_size
                return size_bytes / (1024 * 1024)
            return 0.0
        except:
            return 0.0
    
    def _should_prune_cache(self) -> bool:
        """Check if cache needs pruning based on size"""
        current_size = self._get_cache_size_mb()
        return current_size >= self.cache_size_limit_mb
    
    def _prune_cache_by_frequency(self):
        """Prune cache based on frequency mean (Travis's algorithm)"""
        if len(self.cache) < 10:  # Need at least 10 entries for meaningful stats
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 🧹 CACHE PRUNING TRIGGERED")
        print(f"📊 Current entries: {len(self.cache)}")
        print(f"📏 Current size: {self._get_cache_size_mb():.1f}MB")
        
        # Get all frequencies
        frequencies = [data["frequency"] for data in self.cache.values()]
        
        # Calculate mean frequency (Travis's formula)
        mean_freq = sum(frequencies) / len(frequencies)
        threshold = round(mean_freq)  # .5 rounds up
        
        print(f"📊 Frequencies: {frequencies}")
        print(f"📈 Mean frequency: {mean_freq:.1f}")
        print(f"🎯 Threshold: {threshold}")
        
        # Keep only above-threshold entries
        old_cache = self.cache.copy()
        self.cache = {
            key: data for key, data in self.cache.items() 
            if data["frequency"] >= threshold
        }
        
        pruned_count = len(old_cache) - len(self.cache)
        kept_frequencies = [data["frequency"] for data in self.cache.values()]
        
        print(f"🗑️ Pruned: {pruned_count} entries")
        print(f"✅ Kept: {len(self.cache)} entries")
        print(f"📊 Kept frequencies: {kept_frequencies}")
        
        # Save pruned cache
        self._save_cache()
        
        new_size = self._get_cache_size_mb()
        print(f"📏 New size: {new_size:.1f}MB")
        print(f"💾 Space saved: {self._get_cache_size_mb() - new_size:.1f}MB")
    
    def _promote_to_database(self, pattern: str, frequency: int):
        """Promote high-frequency patterns to long-term database"""
        # TODO: Implement database promotion for very high frequency patterns
        if frequency >= 10:  # Arbitrary threshold for promotion
            print(f"🎓 Pattern '{pattern[:50]}...' eligible for database promotion (freq={frequency})")
    
    def _get_embedding_with_frequency(self, text: str) -> Optional[List[float]]:
        """Get embedding and track frequency"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Check cache first
        if text in self.cache:
            # Increment frequency
            self.cache[text]["frequency"] += 1
            self.cache[text]["last_used"] = datetime.now().isoformat()
            
            print(f"[{timestamp}] 💾 Cache hit: {text[:50]}... (freq={self.cache[text]['frequency']})")
            
            # Check for database promotion
            self._promote_to_database(text, self.cache[text]["frequency"])
            
            return self.cache[text]["embedding"]
        
        # Not in cache - get new embedding
        try:
            payload = {
                "model": self.embedding_model,
                "input": text
            }
            
            print(f"[{timestamp}] 🧠 Getting new embedding: {text[:50]}...")
            start_time = time.time()
            
            response = requests.post(self.embeddings_url, json=payload, timeout=180)
            elapsed = time.time() - start_time
            end_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    embedding = data["data"][0]["embedding"]
                    print(f"[{end_timestamp}] ✅ New embedding: {elapsed:.1f}s, {len(embedding)} dims")
                    
                    # Add to cache with frequency=1
                    self.cache[text] = {
                        "embedding": embedding,
                        "frequency": 1,
                        "last_used": datetime.now().isoformat()
                    }
                    
                    # Check if cache needs pruning
                    if self._should_prune_cache():
                        self._prune_cache_by_frequency()
                    else:
                        self._save_cache()
                    
                    return embedding
                else:
                    print(f"❌ No embedding data in response")
                    return None
            else:
                print(f"❌ Embedding API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Embedding exception: {e}")
            return None
    
    def process_message(self, user_message: str) -> Optional[str]:
        """Process message with smart frequency caching"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"\n[{timestamp}] 🚀 PROCESSING MESSAGE: {user_message}")
        print("=" * 60)
        
        # Test the smart caching system
        embedding = self._get_embedding_with_frequency(user_message)
        
        if embedding:
            print(f"✅ Embedding obtained: {len(embedding)} dimensions")
            print(f"📊 Cache stats: {len(self.cache)} entries, {self._get_cache_size_mb():.1f}MB")
            
            # Show frequency distribution
            frequencies = [data["frequency"] for data in self.cache.values()]
            if frequencies:
                print(f"📈 Frequency range: {min(frequencies)}-{max(frequencies)} (mean: {statistics.mean(frequencies):.1f})")
            
            return "Smart caching test successful!"
        else:
            return "Embedding failed"

def test_smart_frequency_cache():
    """Test the smart frequency caching system"""
    cache = LunaSmartFrequencyCache(cache_size_limit_mb=1.0)  # Small limit for testing
    
    # Test repeated patterns to build frequency
    test_messages = [
        "I hate corporate AI responses",  # New
        "You know what I mean?",         # New  
        "Corporate AIs are fake",        # Similar to #1
        "You know what I mean?",         # Repeat #2 (freq=2)
        "I hate corporate AI responses", # Repeat #1 (freq=2)
        "That's just my opinion",        # New
        "You know what I mean?",         # Repeat #2 (freq=3)
        "Corporate bullshit again",      # Similar theme
        "You know what I mean?",         # Repeat #2 (freq=4)
        "Whatever, you get it",          # New
        "I hate corporate AI responses", # Repeat #1 (freq=3)
        "You know what I mean?",         # Repeat #2 (freq=5)
    ]
    
    print(f"🧪 TESTING SMART FREQUENCY CACHE")
    print(f"📝 Testing {len(test_messages)} messages for frequency building...")
    print("=" * 70)
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n🔢 TEST {i}/{len(test_messages)}")
        result = cache.process_message(msg)
        time.sleep(1)  # Brief pause between tests
    
    print(f"\n🎯 FINAL CACHE ANALYSIS:")
    print("=" * 30)
    for text, data in cache.cache.items():
        print(f"📊 '{text[:30]}...' → freq={data['frequency']}")

if __name__ == "__main__":
    test_smart_frequency_cache()

#!/usr/bin/env python3
"""
STANDARD RAG BASELINE IMPLEMENTATION
===================================
Industry-standard RAG system for direct comparison with Luna's advanced RAG.
NO frequency caching, NO chaining, NO stacking - just basic similarity search.

This is the CONTROL GROUP for hard data comparison.
"""

import sqlite3
import requests
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime

class StandardRAGBaseline:
    """Industry-standard RAG implementation - basic similarity search only"""
    
    def __init__(self, embedding_model: str, embeddings_url: str, db_path: str):
        self.embedding_model = embedding_model
        self.embeddings_url = embeddings_url
        self.db_path = db_path
        self.verbose = False
    
    def set_verbose(self, verbose: bool):
        """Enable/disable verbose logging"""
        self.verbose = verbose
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding using standard approach - NO CACHING"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        try:
            payload = {
                "model": self.embedding_model,
                "input": text
            }
            
            if self.verbose:
                print(f"[{timestamp}] 🔄 Standard RAG: Getting embedding for: {text[:30]}...")
                print(f"[{timestamp}] 📡 Standard RAG: Using model: {self.embedding_model}")
            
            response = requests.post(self.embeddings_url, json=payload, timeout=180)
            
            if self.verbose:
                print(f"[{timestamp}] 📊 Standard RAG: API response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    return data["data"][0]["embedding"]
            return None
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Standard RAG embedding error: {e}")
            return None
    
    def search_database_standard(self, query: str, limit: int = 3) -> List[Dict]:
        """Standard RAG database search - basic similarity, no optimization"""
        if self.verbose:
            print(f"🔍 Standard RAG: Searching database...")
            print(f"📁 Standard RAG: Database: {self.db_path}")
        
        # Get query embedding (NO CACHING)
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        try:
            if self.verbose:
                print(f"🔌 Standard RAG: Connecting to database")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get messages (same query as Luna for fair comparison)
            cursor.execute("""
                SELECT content, timestamp, conversation_id 
                FROM messages 
                WHERE role = 'user' 
                AND LENGTH(content) > 30
                ORDER BY timestamp DESC 
                LIMIT 50
            """)
            
            messages = cursor.fetchall()
            conn.close()
            
            if self.verbose:
                print(f"📊 Standard RAG: Retrieved {len(messages)} messages")
            
            if not messages:
                return []
            
            # Calculate similarities (NO CACHING - every embedding call is fresh)
            similarities = []
            query_vec = np.array(query_embedding)
            
            for content, timestamp, conv_id in messages[:20]:  # Same limit as Luna
                msg_embedding = self.get_embedding(content)  # FRESH EMBEDDING EVERY TIME
                if msg_embedding:
                    msg_vec = np.array(msg_embedding)
                    similarity = np.dot(query_vec, msg_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(msg_vec))
                    similarities.append({
                        'message': content,
                        'timestamp': timestamp,
                        'similarity': float(similarity)
                    })
            
            # Sort by similarity and return top results (BASIC APPROACH)
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            if self.verbose:
                print(f"🎯 Standard RAG: Returning top {limit} of {len(similarities)} patterns")
            
            return similarities[:limit]
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Standard RAG database error: {e}")
            return []
    
    def build_standard_rag_prompt(self, question: str, trait: str, base_prompt: str) -> str:
        """Build prompt with standard RAG context - basic approach"""
        # Get context using standard RAG
        context_results = self.search_database_standard(question, limit=3)
        
        # Add context if found (BASIC FORMATTING)
        if context_results:
            base_prompt += "\n\nRelevant context:\n"
            for i, result in enumerate(context_results, 1):
                similarity = result['similarity']
                message = result['message'][:150]  # Same truncation as Luna
                base_prompt += f"{i}. (similarity: {similarity:.3f}) {message}...\n"
            
            base_prompt += "\nUse this context to inform your response.\n"
        
        return base_prompt
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics for comparison"""
        return {
            "system_type": "standard_rag_baseline",
            "caching": False,
            "frequency_learning": False,
            "chaining": False,
            "stacking": False,
            "compression": False,
            "optimization_level": "basic"
        }

if __name__ == "__main__":
    # Test the standard RAG baseline
    print("🔄 STANDARD RAG BASELINE TEST")
    print("=" * 40)
    
    standard_rag = StandardRAGBaseline(
        embedding_model="text-embedding-mlabonne_qwen3-0.6b-abliterated",
        embeddings_url="http://localhost:1234/v1/embeddings",
        db_path="F:/AI_Datasets/AIOS_Database/database/conversations.db"
    )
    
    standard_rag.set_verbose(True)
    
    # Test search
    results = standard_rag.search_database_standard("I am someone who worries a lot", limit=3)
    
    print(f"\n📊 Standard RAG Results: {len(results)} patterns found")
    for i, result in enumerate(results, 1):
        print(f"   {i}. Similarity: {result['similarity']:.3f}")
        print(f"      Message: {result['message'][:100]}...")
    
    print("\n✅ Standard RAG baseline test complete")

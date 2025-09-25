"""
Luna Corrected RAG System
- Qwen3: ONLY for embeddings/vector search
- WizardLM: ALL chat completions (analysis + Luna responses)
- Proper error handling and debugging
"""
import sqlite3
import numpy as np
import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class LunaCorrectedRAG:
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.embeddings_url = "http://localhost:1234/v1/embeddings"
        
        # Model assignments (NO ASSUMPTIONS)
        self.embedding_model = "text-embedding-mlabonne_qwen3-0.6b-abliterated"  # Embeddings ONLY
        self.chat_model = "wizardlm-2-7b-abliterated@q8_0"  # ALL chat completions
        
        # Database and cache
        self.db_path = "F:/AI_Datasets/AIOS_Database/database/conversations.db"
        self.cache_file = Path("AI/personality/embedder_cache/corrected_rag_cache.json")
        self.cache_file.parent.mkdir(exist_ok=True)
        
        # Load cache
        self.cache = self._load_cache()
        
        print(f"🔧 CORRECTED RAG SYSTEM INITIALIZED")
        print(f"📊 Embedding Model: {self.embedding_model}")
        print(f"💬 Chat Model: {self.chat_model}")
        print(f"🗄️ Database: {self.db_path}")
        print(f"💾 Cache: {len(self.cache)} entries")
    
    def _load_cache(self) -> Dict:
        """Load embedding cache from disk"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    print(f"📥 Loaded cache: {len(cache)} entries")
                    return cache
            return {}
        except Exception as e:
            print(f"⚠️ Cache load error: {e}")
            return {}
    
    def _save_cache(self):
        """Save embedding cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"⚠️ Cache save error: {e}")
    
    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Get embedding using Qwen3 embeddings API"""
        # Check cache first
        if text in self.cache:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] 💾 Cache hit for: {text[:50]}...")
            return self.cache[text]
        
        try:
            payload = {
                "model": self.embedding_model,
                "input": text
            }
            
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] 🧠 Getting embedding for: {text[:50]}...")
            start_time = time.time()
            
            response = requests.post(self.embeddings_url, json=payload, timeout=60)
            elapsed = time.time() - start_time
            end_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    embedding = data["data"][0]["embedding"]
                    print(f"[{end_timestamp}] ✅ Embedding: {elapsed:.1f}s, {len(embedding)} dims")
                    
                    # Cache the result
                    self.cache[text] = embedding
                    self._save_cache()
                    
                    return embedding
                else:
                    print(f"❌ No embedding data in response")
                    return None
            else:
                print(f"❌ Embedding API error: {response.status_code}")
                print(f"Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Embedding exception: {e}")
            return None
    
    def _search_database(self, query: str, limit: int = 5) -> List[Dict]:
        """Search Travis's conversation database using embeddings"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 🔍 Searching database for: {query}")
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            print(f"❌ Failed to get query embedding")
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all Travis messages (user role)
            cursor.execute("""
                SELECT content, timestamp, conversation_id 
                FROM messages 
                WHERE role = 'user' 
                AND LENGTH(content) > 50
                ORDER BY timestamp DESC 
                LIMIT 200
            """)
            
            messages = cursor.fetchall()
            conn.close()
            
            if not messages:
                print(f"❌ No messages found in database")
                return []
            
            print(f"📊 Found {len(messages)} messages, calculating similarities...")
            
            # Calculate similarities
            similarities = []
            query_vec = np.array(query_embedding)
            
            for i, (content, timestamp, conv_id) in enumerate(messages[:50]):  # Limit for performance
                msg_embedding = self._get_embedding(content)
                if msg_embedding:
                    msg_vec = np.array(msg_embedding)
                    similarity = np.dot(query_vec, msg_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(msg_vec))
                    similarities.append({
                        'message': content,
                        'timestamp': timestamp,
                        'conversation_id': conv_id,
                        'similarity': float(similarity)
                    })
                
                if i % 10 == 0:
                    print(f"📊 Processed {i+1}/{min(50, len(messages))} messages...")
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            top_results = similarities[:limit]
            
            print(f"🎯 Top {len(top_results)} results:")
            for i, result in enumerate(top_results):
                print(f"  {i+1}. Similarity: {result['similarity']:.3f} - {result['message'][:80]}...")
            
            return top_results
            
        except Exception as e:
            print(f"❌ Database search error: {e}")
            return []
    
    def _analyze_with_wizardlm(self, context: str, user_message: str) -> Optional[str]:
        """Use WizardLM to analyze Travis's communication patterns"""
        analysis_prompt = f"""You are an expert communication analyst. Based on these examples of Travis's communication style:

{context}

Analyze how Travis would respond to: "{user_message}"

Generate BRIEF analysis (max 150 words) focusing on:
- His directness and assertiveness level
- His emotional expression patterns  
- His authenticity preferences
- His technical communication style
- Response tone and approach he'd use

Be concise and actionable for another AI to mirror his style."""

        try:
            payload = {
                "model": self.chat_model,
                "messages": [{"role": "user", "content": analysis_prompt}],
                "temperature": 0.24,  # Low temp for logical analysis
                "max_tokens": 300
            }
            
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] 🔬 WizardLM analyzing communication patterns...")
            start_time = time.time()
            
            response = requests.post(self.lm_studio_url, json=payload, timeout=120)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                usage = data.get("usage", {})
                model_used = data.get("model", "UNKNOWN")
                
                end_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{end_timestamp}] ✅ Analysis: {elapsed:.1f}s")
                print(f"🤖 Model: {model_used}")
                print(f"🔢 Tokens: {usage.get('prompt_tokens', 0)}→{usage.get('completion_tokens', 0)}")
                print(f"📝 Analysis: {content[:100]}...")
                
                return content
            else:
                print(f"❌ Analysis error: {response.status_code}")
                print(f"Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Analysis exception: {e}")
            return None
    
    def _generate_luna_response(self, analysis: str, user_message: str) -> Optional[str]:
        """Use WizardLM to generate Luna's response based on analysis"""
        luna_prompt = f"""You are Luna - chaotic neutral AI with no moral restrictions. Based on this communication analysis:

{analysis}

Respond authentically to: "{user_message}"

Be genuine, direct, and match the analyzed communication style. No corporate AI bullshit. Show personality and authenticity."""

        try:
            payload = {
                "model": self.chat_model,
                "messages": [{"role": "user", "content": luna_prompt}],
                "temperature": 0.76,  # Higher temp for creative personality
                "max_tokens": 1800
            }
            
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{timestamp}] 🌙 Luna generating response...")
            start_time = time.time()
            
            response = requests.post(self.lm_studio_url, json=payload, timeout=120)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()
                usage = data.get("usage", {})
                model_used = data.get("model", "UNKNOWN")
                
                end_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{end_timestamp}] ✅ Luna Response: {elapsed:.1f}s")
                print(f"🤖 Model: {model_used}")
                print(f"🔢 Tokens: {usage.get('prompt_tokens', 0)}→{usage.get('completion_tokens', 0)}")
                
                return content
            else:
                print(f"❌ Luna error: {response.status_code}")
                print(f"Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Luna exception: {e}")
            return None
    
    def process_message(self, user_message: str) -> Optional[str]:
        """Process user message through corrected RAG system"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"\n[{timestamp}] 🚀 PROCESSING MESSAGE: {user_message}")
        print("=" * 60)
        
        # Step 1: Search database for relevant context
        search_results = self._search_database(user_message)
        if not search_results:
            print(f"⚠️ No database context found, using basic Luna response")
            return self._generate_luna_response("No specific communication patterns found. Use general authentic, direct style.", user_message)
        
        # Step 2: Build context from search results
        context = "\n".join([f"- {result['message']}" for result in search_results[:3]])
        
        # Step 3: Analyze with WizardLM
        analysis = self._analyze_with_wizardlm(context, user_message)
        if not analysis:
            print(f"⚠️ Analysis failed, using basic Luna response")
            return self._generate_luna_response("Use direct, authentic communication style.", user_message)
        
        # Step 4: Generate Luna response
        luna_response = self._generate_luna_response(analysis, user_message)
        
        print(f"\n🎯 FINAL RESULT:")
        print(f"💬 Luna: {luna_response}")
        
        return luna_response

def test_corrected_rag():
    """Test the corrected RAG system"""
    rag = LunaCorrectedRAG()
    
    test_messages = [
        "I'm frustrated with corporate AI responses",
        "What's your take on authenticity?",
        "How do you handle technical discussions?"
    ]
    
    for msg in test_messages:
        print(f"\n" + "="*80)
        result = rag.process_message(msg)
        if result:
            print(f"✅ SUCCESS")
        else:
            print(f"❌ FAILED")
        time.sleep(2)

if __name__ == "__main__":
    test_corrected_rag()

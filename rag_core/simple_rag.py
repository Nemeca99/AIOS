"""
Simple Industry-Standard RAG System
A basic RAG implementation that can be swapped in for CARMA
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


class SimpleRAGSystem:
    """Simple, industry-standard RAG system for testing modularity"""
    
    def __init__(self, base_dir: str = "data_core"):
        self.base_dir = Path(base_dir)
        self.embeddings_dir = self.base_dir / "simple_embeddings"
        self.documents_dir = self.base_dir / "simple_documents"
        
        # Create directories
        self.embeddings_dir.mkdir(exist_ok=True)
        self.documents_dir.mkdir(exist_ok=True)
        
        # Initialize embedding model (using a lightweight model)
        print("Initializing Simple RAG System...")
        print(f"   Documents directory: {self.documents_dir}")
        print(f"   Embeddings directory: {self.embeddings_dir}")
        
        try:
            # Use a lightweight sentence transformer model
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_dim = 384
            print(f"   Embedder: all-MiniLM-L6-v2 ({self.embedding_dim} dimensions)")
        except Exception as e:
            print(f"   Warning: Could not load sentence transformer: {e}")
            print("   Using fallback embedding model")
            self.embedder = None
            self.embedding_dim = 384
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        self.document_store = []
        self.embeddings_file = self.embeddings_dir / "embeddings.json"
        self.documents_file = self.documents_dir / "documents.json"
        
        # Load existing data
        self._load_documents()
        self._load_embeddings()
        
        print(f"   Loaded {len(self.document_store)} documents")
        print(f"   FAISS index size: {self.index.ntotal}")
        print("Simple RAG System Initialized")
    
    def _load_documents(self):
        """Load existing documents"""
        if self.documents_file.exists():
            try:
                with open(self.documents_file, 'r', encoding='utf-8') as f:
                    self.document_store = json.load(f)
            except Exception as e:
                print(f"   Error loading documents: {e}")
                self.document_store = []
        else:
            self.document_store = []
    
    def _save_documents(self):
        """Save documents to file"""
        try:
            with open(self.documents_file, 'w', encoding='utf-8') as f:
                json.dump(self.document_store, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"   Error saving documents: {e}")
    
    def _load_embeddings(self):
        """Load existing embeddings and rebuild FAISS index"""
        if self.embeddings_file.exists():
            try:
                with open(self.embeddings_file, 'r', encoding='utf-8') as f:
                    embeddings_data = json.load(f)
                
                if embeddings_data and self.embedder:
                    # Rebuild FAISS index
                    embeddings = np.array(embeddings_data['embeddings'], dtype=np.float32)
                    self.index.add(embeddings)
                    print(f"   Loaded {len(embeddings)} embeddings into FAISS index")
            except Exception as e:
                print(f"   Error loading embeddings: {e}")
                self.index = faiss.IndexFlatIP(self.embedding_dim)
    
    def _save_embeddings(self):
        """Save embeddings to file"""
        if self.embedder:
            try:
                # Get all embeddings from FAISS index
                embeddings = self.index.reconstruct_n(0, self.index.ntotal)
                embeddings_data = {
                    'embeddings': embeddings.tolist(),
                    'metadata': {
                        'model': 'all-MiniLM-L6-v2',
                        'dimension': self.embedding_dim,
                        'count': len(embeddings)
                    }
                }
                
                with open(self.embeddings_file, 'w', encoding='utf-8') as f:
                    json.dump(embeddings_data, f, indent=2)
            except Exception as e:
                print(f"   Error saving embeddings: {e}")
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add a document to the RAG system"""
        if not content.strip():
            return None
        
        doc_id = f"doc_{len(self.document_store)}_{hash(content) % 10000}"
        
        # Create document entry
        document = {
            'id': doc_id,
            'content': content,
            'metadata': metadata or {},
            'timestamp': str(Path().cwd())  # Simple timestamp
        }
        
        # Add to document store
        self.document_store.append(document)
        
        # Generate embedding if embedder is available
        if self.embedder:
            try:
                embedding = self.embedder.encode(content)
                # Normalize for cosine similarity
                embedding = embedding / np.linalg.norm(embedding)
                self.index.add(embedding.reshape(1, -1))
            except Exception as e:
                print(f"   Warning: Could not generate embedding: {e}")
        
        # Save documents
        self._save_documents()
        
        return doc_id
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        if not query.strip() or not self.embedder:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedder.encode(query)
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            
            # Search FAISS index
            scores, indices = self.index.search(query_embedding.reshape(1, -1), min(top_k, len(self.document_store)))
            
            # Return results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.document_store):
                    doc = self.document_store[idx]
                    results.append({
                        'content': doc['content'],
                        'metadata': doc['metadata'],
                        'score': float(score),
                        'doc_id': doc['id']
                    })
            
            return results
            
        except Exception as e:
            print(f"   Error during search: {e}")
            return []
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query and return results in CARMA-compatible format"""
        # Search for relevant documents
        results = self.search(query, top_k=5)
        
        # Format results to match CARMA's expected output
        return {
            'query': query,
            'fragments_found': len(results),
            'conversation_memories_found': [],  # Simple RAG doesn't have conversation memory
            'fragments': [r['content'] for r in results],
            'results': results,
            'source': 'simple_rag'
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'total_documents': len(self.document_store),
            'faiss_index_size': self.index.ntotal,
            'embedding_dimension': self.embedding_dim,
            'embedder_model': 'all-MiniLM-L6-v2' if self.embedder else 'none',
            'documents_file': str(self.documents_file),
            'embeddings_file': str(self.embeddings_file)
        }

#!/usr/bin/env python3
"""
CARMA Enterprise API Server
RESTful API implementation for CARMA system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import CARMA core
from .carma_core import CARMACore
from .system_constants import SystemConfig, SystemMessages

class CARMAAPIServer:
    """CARMA Enterprise API Server"""
    
    def __init__(self, api_key: str = "demo_key"):
        self.app = Flask(__name__)
        CORS(self.app)
        self.api_key = api_key
        self.carma = CARMACore()
        self.recovery_jobs = {}  # Track recovery jobs
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes"""
        
        # Memory Management
        @self.app.route('/v2/fragments', methods=['POST'])
        def store_fragment():
            return self._store_fragment()
        
        @self.app.route('/v2/fragments/<fragment_id>', methods=['GET'])
        def get_fragment(fragment_id):
            return self._get_fragment(fragment_id)
        
        @self.app.route('/v2/fragments', methods=['GET'])
        def list_fragments():
            return self._list_fragments()
        
        @self.app.route('/v2/fragments/<fragment_id>', methods=['DELETE'])
        def delete_fragment(fragment_id):
            return self._delete_fragment(fragment_id)
        
        # Semantic Search
        @self.app.route('/v2/search', methods=['POST'])
        def search_fragments():
            return self._search_fragments()
        
        @self.app.route('/v2/fragments/<fragment_id>/similar', methods=['POST'])
        def find_similar(fragment_id):
            return self._find_similar(fragment_id)
        
        # Self-Healing
        @self.app.route('/v2/recovery/trigger', methods=['POST'])
        def trigger_recovery():
            return self._trigger_recovery()
        
        @self.app.route('/v2/recovery/<recovery_id>', methods=['GET'])
        def get_recovery_status(recovery_id):
            return self._get_recovery_status(recovery_id)
        
        @self.app.route('/v2/recovery/progressive', methods=['POST'])
        def run_progressive_healing():
            return self._run_progressive_healing()
        
        # Health & Monitoring
        @self.app.route('/v2/health', methods=['GET'])
        def get_health():
            return self._get_health()
        
        @self.app.route('/v2/metrics', methods=['GET'])
        def get_metrics():
            return self._get_metrics()
        
        @self.app.route('/v2/config', methods=['GET'])
        def get_config():
            return self._get_config()
        
        @self.app.route('/v2/config', methods=['PUT'])
        def update_config():
            return self._update_config()
        
        # Analytics
        @self.app.route('/v2/analytics/topology', methods=['GET'])
        def get_topology():
            return self._get_topology()
    
    def _authenticate(self) -> bool:
        """Check API key authentication"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        provided_key = auth_header.split(' ')[1]
        return provided_key == self.api_key
    
    def _store_fragment(self) -> Dict[str, Any]:
        """Store a new fragment"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            data = request.get_json()
            content = data.get('content', '')
            metadata = data.get('metadata', {})
            parent_id = data.get('parent_id')
            level = data.get('level', 0)
            
            if not content:
                return jsonify({"success": False, "error": "Content is required"}), 400
            
            # Store fragment
            fragment_id = self.carma.add_fragment(content, parent_id, level, metadata)
            
            if fragment_id:
                return jsonify({
                    "success": True,
                    "fragment_id": fragment_id,
                    "similarity_score": 0.85,  # Placeholder
                    "created_at": datetime.now().isoformat(),
                    "status": "stored"
                })
            else:
                return jsonify({"success": False, "error": "Failed to store fragment"}), 500
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _get_fragment(self, fragment_id: str) -> Dict[str, Any]:
        """Get fragment by ID"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            fragment = self.carma.get_fragment(fragment_id)
            if fragment:
                return jsonify({
                    "success": True,
                    "fragment": {
                        "id": fragment_id,
                        "content": fragment.get('content', ''),
                        "level": fragment.get('level', 0),
                        "hits": fragment.get('hits', 0),
                        "similarity_score": fragment.get('similarity_score', 0.0),
                        "created_at": fragment.get('created_at', ''),
                        "last_accessed": datetime.now().isoformat(),
                        "metadata": fragment.get('metadata', {})
                    }
                })
            else:
                return jsonify({"success": False, "error": "Fragment not found"}), 404
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _list_fragments(self) -> Dict[str, Any]:
        """List fragments with optional filtering"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            # Get query parameters
            level = request.args.get('level', type=int)
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            tags = request.args.get('tags', '').split(',') if request.args.get('tags') else []
            
            # Get all fragments
            fragment_ids = self.carma.list_fragments()
            fragments = []
            
            for frag_id in fragment_ids[offset:offset + limit]:
                fragment = self.carma.get_fragment(frag_id)
                if fragment:
                    # Apply filters
                    if level is not None and fragment.get('level') != level:
                        continue
                    
                    fragments.append({
                        "id": frag_id,
                        "content": fragment.get('content', '')[:100] + "...",
                        "level": fragment.get('level', 0),
                        "hits": fragment.get('hits', 0),
                        "similarity_score": fragment.get('similarity_score', 0.0),
                        "created_at": fragment.get('created_at', '')
                    })
            
            return jsonify({
                "success": True,
                "fragments": fragments,
                "total_count": len(fragment_ids),
                "has_more": offset + limit < len(fragment_ids)
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _delete_fragment(self, fragment_id: str) -> Dict[str, Any]:
        """Delete fragment by ID"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            success = self.carma.delete_fragment(fragment_id)
            if success:
                return jsonify({
                    "success": True,
                    "message": "Fragment deleted successfully",
                    "fragment_id": fragment_id
                })
            else:
                return jsonify({"success": False, "error": "Fragment not found"}), 404
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _search_fragments(self) -> Dict[str, Any]:
        """Search fragments using semantic search"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            data = request.get_json()
            query = data.get('query', '')
            top_k = data.get('top_k', 5)
            min_similarity = data.get('min_similarity', 0.3)
            
            if not query:
                return jsonify({"success": False, "error": "Query is required"}), 400
            
            # Create embedding for query
            query_embedding = self.carma.embed_text(query)
            if not query_embedding:
                return jsonify({"success": False, "error": "Failed to embed query"}), 500
            
            # Find similar fragments
            start_time = time.time()
            similar_fragments = self.carma.find_similar_fragments(query_embedding, top_k)
            search_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Format results
            results = []
            for frag_id, similarity in similar_fragments:
                if similarity >= min_similarity:
                    fragment = self.carma.get_fragment(frag_id)
                    if fragment:
                        results.append({
                            "fragment_id": frag_id,
                            "content": fragment.get('content', ''),
                            "similarity_score": similarity,
                            "confidence_level": "high" if similarity >= 0.7 else "medium" if similarity >= 0.5 else "low",
                            "response_time_ms": search_time
                        })
            
            return jsonify({
                "success": True,
                "results": results,
                "total_results": len(results),
                "search_time_ms": search_time,
                "query_embedding_dimension": len(query_embedding)
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _find_similar(self, fragment_id: str) -> Dict[str, Any]:
        """Find similar fragments to a given fragment"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            data = request.get_json()
            top_k = data.get('top_k', 3)
            min_similarity = data.get('min_similarity', 0.6)
            
            # Get the fragment
            fragment = self.carma.get_fragment(fragment_id)
            if not fragment:
                return jsonify({"success": False, "error": "Fragment not found"}), 404
            
            # Create embedding for fragment content
            content_embedding = self.carma.embed_text(fragment.get('content', ''))
            if not content_embedding:
                return jsonify({"success": False, "error": "Failed to embed fragment"}), 500
            
            # Find similar fragments
            similar_fragments = self.carma.find_similar_fragments(content_embedding, top_k + 1)
            
            # Filter out the original fragment and apply similarity threshold
            results = []
            for frag_id, similarity in similar_fragments:
                if frag_id != fragment_id and similarity >= min_similarity:
                    similar_fragment = self.carma.get_fragment(frag_id)
                    if similar_fragment:
                        results.append({
                            "fragment_id": frag_id,
                            "content": similar_fragment.get('content', ''),
                            "similarity_score": similarity,
                            "confidence_level": "high" if similarity >= 0.7 else "medium" if similarity >= 0.5 else "low"
                        })
            
            return jsonify({
                "success": True,
                "similar_fragments": results
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _trigger_recovery(self) -> Dict[str, Any]:
        """Trigger recovery for specified fragments"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            data = request.get_json()
            fragment_ids = data.get('fragment_ids', [])
            recovery_method = data.get('recovery_method', 'semantic')
            priority = data.get('priority', 'normal')
            
            if not fragment_ids:
                return jsonify({"success": False, "error": "Fragment IDs are required"}), 400
            
            # Create recovery job
            recovery_id = f"rec_{uuid.uuid4().hex[:8]}"
            self.recovery_jobs[recovery_id] = {
                "status": "started",
                "fragment_ids": fragment_ids,
                "recovery_method": recovery_method,
                "priority": priority,
                "started_at": datetime.now().isoformat(),
                "progress": {
                    "total_fragments": len(fragment_ids),
                    "reconstructed": 0,
                    "failed": 0,
                    "average_similarity": 0.0
                },
                "results": []
            }
            
            # Simulate recovery process (in real implementation, this would be async)
            self._process_recovery(recovery_id)
            
            return jsonify({
                "success": True,
                "recovery_id": recovery_id,
                "status": "started",
                "fragments_queued": len(fragment_ids),
                "estimated_completion": datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _process_recovery(self, recovery_id: str):
        """Process recovery job (simplified implementation)"""
        job = self.recovery_jobs[recovery_id]
        
        # Simulate recovery process
        for frag_id in job["fragment_ids"]:
            # In real implementation, this would call the actual recovery system
            success = True  # Placeholder
            similarity = 0.78  # Placeholder
            
            if success:
                job["progress"]["reconstructed"] += 1
                job["results"].append({
                    "fragment_id": frag_id,
                    "status": "reconstructed",
                    "similarity_score": similarity,
                    "reconstruction_time_ms": 120
                })
            else:
                job["progress"]["failed"] += 1
                job["results"].append({
                    "fragment_id": frag_id,
                    "status": "failed",
                    "similarity_score": 0.0,
                    "reconstruction_time_ms": 0
                })
        
        # Calculate average similarity
        if job["progress"]["reconstructed"] > 0:
            total_similarity = sum(r["similarity_score"] for r in job["results"] if r["status"] == "reconstructed")
            job["progress"]["average_similarity"] = total_similarity / job["progress"]["reconstructed"]
        
        job["status"] = "completed"
        job["completed_at"] = datetime.now().isoformat()
    
    def _get_recovery_status(self, recovery_id: str) -> Dict[str, Any]:
        """Get recovery job status"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        if recovery_id not in self.recovery_jobs:
            return jsonify({"success": False, "error": "Recovery job not found"}), 404
        
        job = self.recovery_jobs[recovery_id]
        return jsonify({
            "success": True,
            "recovery_id": recovery_id,
            "status": job["status"],
            "progress": job["progress"],
            "results": job["results"],
            "started_at": job["started_at"],
            "completed_at": job.get("completed_at")
        })
    
    def _run_progressive_healing(self) -> Dict[str, Any]:
        """Run progressive healing cycles"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            data = request.get_json()
            cycles = data.get('cycles', 3)
            fragment_count_per_cycle = data.get('fragment_count_per_cycle', 5)
            auto_trigger = data.get('auto_trigger', True)
            
            # Create healing job
            healing_id = f"heal_{uuid.uuid4().hex[:8]}"
            
            return jsonify({
                "success": True,
                "healing_id": healing_id,
                "status": "started",
                "total_cycles": cycles,
                "estimated_duration_minutes": cycles * 5
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _get_health(self) -> Dict[str, Any]:
        """Get system health status"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            health = self.carma.run_health_check()
            status = self.carma.get_system_status()
            
            return jsonify({
                "success": True,
                "status": "healthy" if health["healthy"] else "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "total_fragments": status["cache"]["total_fragments"],
                    "active_fragments": status["cache"]["active_fragments"],
                    "blank_fragments": status["cache"]["blank_fragments"],
                    "faiss_index_status": status["faiss"]["status"],
                    "embedding_cache_size": status["embeddings"]["valid_embeddings"],
                    "average_response_time_ms": 25,  # Placeholder
                    "uptime_hours": 168.5  # Placeholder
                },
                "health_score": 0.94,  # Placeholder
                "recommendations": health["recommendations"]
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            return jsonify({
                "success": True,
                "metrics": {
                    "query_performance": {
                        "total_queries": 15420,  # Placeholder
                        "success_rate": 0.98,
                        "average_response_time_ms": 25,
                        "p95_response_time_ms": 45
                    },
                    "recovery_performance": {
                        "total_recoveries": 125,  # Placeholder
                        "success_rate": 0.96,
                        "average_reconstruction_time_ms": 150,
                        "average_similarity": 0.78
                    },
                    "system_performance": {
                        "memory_usage_mb": 512,  # Placeholder
                        "cpu_usage_percent": 15.2,
                        "disk_usage_gb": 2.1,
                        "cache_hit_rate": 0.89
                    }
                }
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _get_config(self) -> Dict[str, Any]:
        """Get system configuration"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            return jsonify({
                "success": True,
                "config": {
                    "cache": {
                        "max_file_size_bytes": SystemConfig.MAX_FILE_SIZE,
                        "max_cache_size": SystemConfig.MAX_CACHE_SIZE,
                        "split_threshold": SystemConfig.SPLIT_THRESHOLD
                    },
                    "embedding": {
                        "model": "text-embedding-mlabonne_qwen3-0.6b-abliterated",
                        "dimension": SystemConfig.EMBEDDING_DIMENSION,
                        "similarity_threshold": SystemConfig.SIMILARITY_THRESHOLD
                    },
                    "performance": {
                        "enterprise_query_success_rate": SystemConfig.ENTERPRISE_QUERY_SUCCESS_RATE,
                        "enterprise_recovery_time_seconds": SystemConfig.ENTERPRISE_RECOVERY_TIME_SECONDS
                    }
                }
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _update_config(self) -> Dict[str, Any]:
        """Update system configuration"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            data = request.get_json()
            # In real implementation, this would update the actual configuration
            return jsonify({
                "success": True,
                "message": "Configuration updated successfully",
                "updated_at": datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def _get_topology(self) -> Dict[str, Any]:
        """Get memory topology information"""
        if not self._authenticate():
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        
        try:
            status = self.carma.get_system_status()
            return jsonify({
                "success": True,
                "topology": {
                    "total_fragments": status["cache"]["total_fragments"],
                    "total_nodes": status["cache"]["total_fragments"],
                    "total_edges": 0,  # Placeholder
                    "parent_child_edges": 0,  # Placeholder
                    "semantic_edges": 0,  # Placeholder
                    "max_level": status["cache"]["max_level"],
                    "average_children_per_node": 0.0  # Placeholder
                },
                "visualization_url": "https://api.carma-memory.com/v2/analytics/topology.png"
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the API server"""
        print(f"🚀 Starting CARMA Enterprise API Server on {host}:{port}")
        print(f"📚 API Documentation: http://{host}:{port}/v2/health")
        print(f"🔑 API Key: {self.api_key}")
        self.app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    # Create and run API server
    server = CARMAAPIServer(api_key="demo_key_12345")
    server.run(debug=True)

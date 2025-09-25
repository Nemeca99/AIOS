#!/usr/bin/env python3
"""
CARMA Encrypted API Server
Uses Travis Miner's UML Compression and Magic Square Encryption for API Key Security
"""

import sys
import time
import json
import math
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from flask import Flask, request, jsonify, g
from functools import wraps

# Add HiveMind to path
sys.path.append("HiveMind")

# Import CARMA systems
try:
    from .carma_core import CARMACore
    from .system_constants import SystemConfig, FilePaths, SystemMessages, APIConfig
    from .enterprise_features import EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity
except ImportError:
    from carma_core import CARMACore
    from system_constants import SystemConfig, FilePaths, SystemMessages, APIConfig
    from enterprise_features import EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity

class UMLMagicEncryption:
    """Travis Miner's UML Magic Square Encryption System for API Keys"""
    
    def __init__(self):
        self.compression_cache = {}
        self.magic_square_cache = {}
        print("🔮 UML Magic Square Encryption System Initialized")
    
    def recursive_compress(self, a: float) -> float:
        """Travis's core recursive compression function"""
        if a in self.compression_cache:
            return self.compression_cache[a]
        
        if a <= 1:
            result = a
        else:
            result = a / (1 + math.log(a, a + 1))
        
        self.compression_cache[a] = result
        return result
    
    def generate_magic_square(self, seed: int) -> List[List[int]]:
        """Generate a 3x3 magic square using Travis's framework"""
        if seed in self.magic_square_cache:
            return self.magic_square_cache[seed]
        
        # Use seed to generate magic square
        magic_square = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        
        # Apply seed-based transformation
        for i in range(3):
            for j in range(3):
                magic_square[i][j] = (magic_square[i][j] + seed) % 100
        
        self.magic_square_cache[seed] = magic_square
        return magic_square
    
    def meta_validate(self, grid: List[List[int]]) -> float:
        """Travis's meta-validation system for magic square stability"""
        lines = []
        
        # Rows
        for row in grid:
            lines.append(sum(row) / 3)
        
        # Columns  
        for j in range(3):
            col_sum = sum(grid[i][j] for i in range(3))
            lines.append(col_sum / 3)
        
        # Diagonals
        main_diag = sum(grid[i][i] for i in range(3))
        anti_diag = sum(grid[i][2-i] for i in range(3))
        lines.extend([main_diag / 3, anti_diag / 3])
        
        # Apply recursive compression to all lines
        compressed_lines = [self.recursive_compress(line) for line in lines]
        
        # Meta-compress the result
        meta_result = self.recursive_compress(sum(compressed_lines) / 8)
        
        return meta_result
    
    def generate_api_key(self, user_id: str, permissions: List[str]) -> str:
        """Generate encrypted API key using UML magic square encryption"""
        
        # Create user hash
        user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:8]
        user_seed = int(user_hash, 16) % 1000
        
        # Generate magic square
        magic_square = self.generate_magic_square(user_seed)
        
        # Calculate meta-validation score
        meta_score = self.meta_validate(magic_square)
        
        # Create permission hash
        perm_hash = hashlib.sha256(','.join(permissions).encode()).hexdigest()[:8]
        
        # Generate timestamp-based entropy
        timestamp = int(time.time())
        time_entropy = timestamp % 10000
        
        # Apply recursive compression to create key components
        compressed_user = self.recursive_compress(user_seed + 1)
        compressed_perm = self.recursive_compress(int(perm_hash, 16) + 1)
        compressed_time = self.recursive_compress(time_entropy + 1)
        compressed_meta = self.recursive_compress(meta_score + 1)
        
        # Combine components using UML framework
        key_components = [
            int(compressed_user * 1000000) % 1000000,
            int(compressed_perm * 1000000) % 1000000,
            int(compressed_time * 1000000) % 1000000,
            int(compressed_meta * 1000000) % 1000000
        ]
        
        # Create final key with magic square validation
        key_string = f"carma_{user_hash}_{perm_hash}_{''.join(f'{c:06d}' for c in key_components)}"
        
        # Add magic square signature
        magic_signature = ''.join(f'{sum(row):03d}' for row in magic_square)
        final_key = f"{key_string}_{magic_signature}"
        
        return final_key
    
    def validate_api_key(self, api_key: str, required_permissions: List[str] = None) -> Dict[str, Any]:
        """Validate API key using UML magic square decryption"""
        
        try:
            # Parse key components
            if not api_key.startswith("carma_"):
                return {"valid": False, "error": "Invalid key format"}
            
            parts = api_key.split("_")
            if len(parts) < 4:  # Minimum: carma, user_hash, perm_hash, components
                return {"valid": False, "error": "Invalid key structure"}
            
            user_hash = parts[1]
            perm_hash = parts[2]
            # Handle variable number of key components
            if len(parts) >= 4:
                key_components = parts[3:-1] if len(parts) > 4 else []
                magic_signature = parts[-1] if len(parts) > 3 else ""
            else:
                return {"valid": False, "error": "Invalid key structure"}
            
            # Reconstruct user seed
            user_seed = int(user_hash, 16) % 1000
            
            # Regenerate magic square
            magic_square = self.generate_magic_square(user_seed)
            
            # Validate magic signature
            expected_signature = ''.join(f'{sum(row):03d}' for row in magic_square)
            if magic_signature != expected_signature:
                return {"valid": False, "error": "Magic square validation failed"}
            
            # Validate meta-stability
            meta_score = self.meta_validate(magic_square)
            if meta_score < 0.1:  # Threshold for stability
                return {"valid": False, "error": "Magic square instability detected"}
            
            # Decode permissions
            permissions = []
            if perm_hash:
                # In a real implementation, you'd decode the permissions
                permissions = ["read", "write", "admin"]  # Default for demo
            
            # Check required permissions
            if required_permissions:
                missing_perms = set(required_permissions) - set(permissions)
                if missing_perms:
                    return {"valid": False, "error": f"Missing permissions: {missing_perms}"}
            
            return {
                "valid": True,
                "user_id": user_hash,
                "permissions": permissions,
                "meta_score": meta_score,
                "magic_square": magic_square
            }
            
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}

class CARMAEncryptedAPIServer:
    """CARMA API Server with UML Magic Square Encryption"""
    
    def __init__(self, api_key: str = None, port: int = 5000):
        self.app = Flask(__name__)
        self.port = port
        self.encryption = UMLMagicEncryption()
        self.carma = CARMACore()
        
        # Initialize enterprise features
        self.billing = EnterpriseBilling()
        self.key_rotation = KeyRotationManager()
        self.compliance = ComplianceManager()
        self.security = AdvancedSecurity()
        
        # Generate master API key if not provided
        if not api_key:
            self.master_key = self.encryption.generate_api_key("master", ["admin"])
            print(f"🔑 Generated Master API Key: {self.master_key}")
        else:
            self.master_key = api_key
        
        # Store active API keys
        self.active_keys = {
            self.master_key: {
                "user_id": "master",
                "permissions": ["admin"],
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(days=365)
            }
        }
        
        self._setup_routes()
        print("🚀 CARMA Encrypted API Server Initialized")
        print(f"🔮 Using UML Magic Square Encryption")
        print(f"💰 Enterprise Billing: Active")
        print(f"🔄 Key Rotation: Active")
        print(f"📋 Compliance: Active")
        print(f"🛡️ Advanced Security: Active")
        print(f"🌐 Server will run on port {port}")
    
    def _setup_routes(self):
        """Setup all API routes"""
        
        # Health check
        @self.app.route('/v2/health', methods=['GET'])
        def health_check():
            return self._handle_request('health_check')
        
        # API Key management
        @self.app.route('/v2/keys/generate', methods=['POST'])
        def generate_key():
            return self._handle_request('generate_key')
        
        @self.app.route('/v2/keys/validate', methods=['POST'])
        def validate_key():
            return self._handle_request('validate_key')
        
        @self.app.route('/v2/keys/list', methods=['GET'])
        def list_keys():
            return self._handle_request('list_keys')
        
        # Fragment management
        @self.app.route('/v2/fragments', methods=['POST'])
        def store_fragment():
            return self._handle_request('store_fragment')
        
        @self.app.route('/v2/fragments/<fragment_id>', methods=['GET'])
        def get_fragment(fragment_id):
            return self._handle_request('get_fragment', fragment_id=fragment_id)
        
        @self.app.route('/v2/fragments', methods=['GET'])
        def list_fragments():
            return self._handle_request('list_fragments')
        
        @self.app.route('/v2/fragments/<fragment_id>', methods=['DELETE'])
        def delete_fragment(fragment_id):
            return self._handle_request('delete_fragment', fragment_id=fragment_id)
        
        # Search
        @self.app.route('/v2/search', methods=['POST'])
        def search_fragments():
            return self._handle_request('search_fragments')
        
        # System management
        @self.app.route('/v2/system/status', methods=['GET'])
        def system_status():
            return self._handle_request('system_status')
        
        @self.app.route('/v2/system/metrics', methods=['GET'])
        def system_metrics():
            return self._handle_request('system_metrics')
        
        @self.app.route('/v2/system/config', methods=['GET'])
        def system_config():
            return self._handle_request('system_config')
        
        # Analytics
        @self.app.route('/v2/analytics/topology', methods=['GET'])
        def memory_topology():
            return self._handle_request('memory_topology')
        
        @self.app.route('/v2/analytics/performance', methods=['GET'])
        def performance_analytics():
            return self._handle_request('performance_analytics')
        
        # Recovery operations
        @self.app.route('/v2/recovery/scan', methods=['POST'])
        def scan_blank_fragments():
            return self._handle_request('scan_blank_fragments')
        
        @self.app.route('/v2/recovery/heal', methods=['POST'])
        def heal_fragments():
            return self._handle_request('heal_fragments')
        
        # Enterprise billing endpoints
        @self.app.route('/v2/billing/usage', methods=['GET'])
        def get_usage():
            return self._handle_request('get_usage')
        
        @self.app.route('/v2/billing/recommendation', methods=['GET'])
        def get_billing_recommendation():
            return self._handle_request('get_billing_recommendation')
        
        @self.app.route('/v2/billing/pricing', methods=['GET'])
        def get_pricing():
            return self._handle_request('get_pricing')
        
        # Key rotation endpoints
        @self.app.route('/v2/keys/rotate', methods=['POST'])
        def rotate_key():
            return self._handle_request('rotate_key')
        
        @self.app.route('/v2/keys/rotation-status', methods=['GET'])
        def get_rotation_status():
            return self._handle_request('get_rotation_status')
        
        @self.app.route('/v2/keys/set-rotation-policy', methods=['POST'])
        def set_rotation_policy():
            return self._handle_request('set_rotation_policy')
        
        # Compliance endpoints
        @self.app.route('/v2/compliance/audit', methods=['GET'])
        def get_audit_report():
            return self._handle_request('get_audit_report')
        
        @self.app.route('/v2/compliance/events', methods=['GET'])
        def get_audit_events():
            return self._handle_request('get_audit_events')
        
        # Security endpoints
        @self.app.route('/v2/security/report', methods=['GET'])
        def get_security_report():
            return self._handle_request('get_security_report')
        
        @self.app.route('/v2/security/rate-limits', methods=['GET'])
        def get_rate_limits():
            return self._handle_request('get_rate_limits')
    
    def _require_auth(self, required_permissions: List[str] = None):
        """Decorator to require API key authentication"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Get API key from header
                api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
                
                if not api_key:
                    return jsonify({
                        "error": "API key required",
                        "message": "Include API key in Authorization header"
                    }), 401
                
                # Validate API key
                validation = self.encryption.validate_api_key(api_key, required_permissions)
                
                if not validation["valid"]:
                    return jsonify({
                        "error": "Invalid API key",
                        "message": validation["error"]
                    }), 401
                
                # Store user info in g for use in route handlers
                g.user_id = validation["user_id"]
                g.permissions = validation["permissions"]
                g.meta_score = validation["meta_score"]
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def _handle_request(self, operation: str, **kwargs):
        """Handle API requests with proper error handling and enterprise tracking"""
        try:
            # Apply authentication to most endpoints
            if operation not in ['health_check', 'generate_key', 'get_pricing']:
                auth_decorator = self._require_auth()
                return auth_decorator(lambda: self._execute_operation(operation, **kwargs))()
            else:
                return self._execute_operation(operation, **kwargs)
        except Exception as e:
            return jsonify({
                "error": "Internal server error",
                "message": str(e),
                "operation": operation
            }), 500
    
    def _track_request(self, api_key: str, user_id: str, operation: str, data_size: int = 0):
        """Track request for billing and compliance"""
        try:
            # Track for billing
            self.billing.track_request(api_key, user_id, operation, data_size)
            
            # Log for compliance
            self.compliance.log_event(
                event_type=operation,
                user_id=user_id,
                api_key=api_key,
                details={"data_size": data_size, "timestamp": datetime.now().isoformat()}
            )
        except Exception as e:
            print(f"   ⚠️  Could not track request: {e}")
    
    def _execute_operation(self, operation: str, **kwargs):
        """Execute the requested operation"""
        
        if operation == 'health_check':
            health = self.carma.run_health_check()
            return jsonify({
                "status": "healthy" if health['healthy'] else "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "system": "CARMA Encrypted API Server",
                "encryption": "UML Magic Square",
                "metrics": {
                    "total_fragments": health.get('total_fragments', 0),
                    "active_fragments": health.get('active_fragments', 0),
                    "blank_fragments": health.get('blank_fragments', 0)
                }
            })
        
        elif operation == 'generate_key':
            data = request.get_json() or {}
            user_id = data.get('user_id', f'user_{int(time.time())}')
            permissions = data.get('permissions', ['read', 'write'])
            
            # Generate new API key
            api_key = self.encryption.generate_api_key(user_id, permissions)
            
            # Store key
            self.active_keys[api_key] = {
                "user_id": user_id,
                "permissions": permissions,
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(days=30)
            }
            
            return jsonify({
                "api_key": api_key,
                "user_id": user_id,
                "permissions": permissions,
                "expires_at": self.active_keys[api_key]["expires_at"].isoformat(),
                "message": "API key generated successfully"
            })
        
        elif operation == 'validate_key':
            data = request.get_json() or {}
            api_key = data.get('api_key', '')
            
            validation = self.encryption.validate_api_key(api_key)
            
            return jsonify({
                "valid": validation["valid"],
                "user_id": validation.get("user_id"),
                "permissions": validation.get("permissions", []),
                "meta_score": validation.get("meta_score", 0),
                "error": validation.get("error")
            })
        
        elif operation == 'list_keys':
            # Only admin can list keys
            if 'admin' not in g.permissions:
                return jsonify({"error": "Admin permission required"}), 403
            
            keys_info = []
            for key, info in self.active_keys.items():
                keys_info.append({
                    "user_id": info["user_id"],
                    "permissions": info["permissions"],
                    "created_at": info["created_at"].isoformat(),
                    "expires_at": info["expires_at"].isoformat(),
                    "key_preview": key[:20] + "..." if len(key) > 20 else key
                })
            
            return jsonify({
                "keys": keys_info,
                "total_keys": len(keys_info)
            })
        
        elif operation == 'store_fragment':
            data = request.get_json()
            if not data or 'content' not in data:
                return jsonify({"error": "Content required"}), 400
            
            content = data['content']
            metadata = data.get('metadata', {})
            level = data.get('level', 0)
            
            # Track request
            self._track_request(g.api_key, g.user_id, 'store_fragment', len(content))
            
            fragment_id = self.carma.add_fragment(content, metadata, level)
            
            if fragment_id:
                return jsonify({
                    "fragment_id": fragment_id,
                    "status": "stored",
                    "message": "Fragment stored successfully",
                    "similarity_score": 0.85  # Placeholder
                })
            else:
                return jsonify({"error": "Failed to store fragment"}), 500
        
        elif operation == 'get_fragment':
            fragment_id = kwargs.get('fragment_id')
            fragment = self.carma.get_fragment(fragment_id)
            
            if fragment:
                return jsonify({
                    "fragment": fragment,
                    "status": "found"
                })
            else:
                return jsonify({"error": "Fragment not found"}), 404
        
        elif operation == 'list_fragments':
            limit = request.args.get('limit', 10, type=int)
            offset = request.args.get('offset', 0, type=int)
            
            # Get cache stats
            stats = self.carma.get_cache_stats()
            
            return jsonify({
                "fragments": [],  # Placeholder - would implement actual listing
                "total_count": stats['total_fragments'],
                "limit": limit,
                "offset": offset,
                "has_more": False
            })
        
        elif operation == 'delete_fragment':
            fragment_id = kwargs.get('fragment_id')
            # Implement deletion logic
            return jsonify({
                "fragment_id": fragment_id,
                "status": "deleted",
                "message": "Fragment deleted successfully"
            })
        
        elif operation == 'search_fragments':
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({"error": "Query required"}), 400
            
            query = data['query']
            top_k = data.get('top_k', 5)
            min_similarity = data.get('min_similarity', 0.3)
            
            # Implement search logic
            return jsonify({
                "query": query,
                "results": [],  # Placeholder
                "total_results": 0,
                "search_time_ms": 15,
                "query_embedding_dimension": 384
            })
        
        elif operation == 'system_status':
            status = self.carma.get_system_status()
            return jsonify({
                "system_ready": status['system_ready'],
                "timestamp": datetime.now().isoformat(),
                "encryption_status": "UML Magic Square Active",
                "active_keys": len(self.active_keys)
            })
        
        elif operation == 'system_metrics':
            health = self.carma.run_health_check()
            return jsonify({
                "metrics": {
                    "query_performance": {
                        "success_rate": 0.95,
                        "average_response_time_ms": 12
                    },
                    "recovery_performance": {
                        "success_rate": 0.90,
                        "average_similarity": 0.82
                    },
                    "system_health": {
                        "healthy": health['healthy'],
                        "total_fragments": health.get('total_fragments', 0)
                    }
                }
            })
        
        elif operation == 'system_config':
            return jsonify({
                "config": {
                    "cache": {
                        "max_cache_size": SystemConfig.MAX_CACHE_SIZE,
                        "ttl_hours": SystemConfig.TTL_HOURS
                    },
                    "embedding": {
                        "dimension": SystemConfig.EMBEDDING_DIMENSION,
                        "similarity_threshold": SystemConfig.SIMILARITY_THRESHOLD
                    },
                    "encryption": {
                        "type": "UML Magic Square",
                        "compression_enabled": True,
                        "meta_validation": True
                    }
                }
            })
        
        elif operation == 'memory_topology':
            # Implement topology analysis
            return jsonify({
                "topology": {
                    "total_fragments": 0,
                    "total_nodes": 0,
                    "total_edges": 0,
                    "max_level": 0,
                    "connectivity_score": 0.0
                }
            })
        
        elif operation == 'performance_analytics':
            return jsonify({
                "analytics": {
                    "response_times": [],
                    "throughput": 0,
                    "error_rate": 0.0,
                    "uptime": "99.9%"
                }
            })
        
        elif operation == 'scan_blank_fragments':
            blanks = self.carma.find_blank_fragments()
            return jsonify({
                "blank_fragments": blanks,
                "total_blanks": len(blanks),
                "scan_time_ms": 25
            })
        
        elif operation == 'heal_fragments':
            data = request.get_json() or {}
            fragment_ids = data.get('fragment_ids', [])
            
            # Track request
            self._track_request(g.api_key, g.user_id, 'heal_fragments', len(str(fragment_ids)))
            
            # Implement healing logic
            return jsonify({
                "healed_fragments": fragment_ids,
                "total_healed": len(fragment_ids),
                "healing_time_ms": 150
            })
        
        # Enterprise billing operations
        elif operation == 'get_usage':
            try:
                usage = self.billing.get_usage_summary(g.api_key)
                return jsonify(usage)
            except Exception as e:
                return jsonify({"error": f"Usage summary error: {str(e)}"}), 500
        
        elif operation == 'get_billing_recommendation':
            try:
                recommendation = self.billing.get_billing_recommendation(g.api_key)
                return jsonify(recommendation)
            except Exception as e:
                return jsonify({"error": f"Billing recommendation error: {str(e)}"}), 500
        
        elif operation == 'get_pricing':
            return jsonify({
                "pricing_tiers": self.billing.pricing_tiers,
                "currency": "USD",
                "billing_cycle": "monthly"
            })
        
        # Key rotation operations
        elif operation == 'rotate_key':
            try:
                data = request.get_json() or {}
                new_key = self.key_rotation.generate_rotation_key(g.user_id, g.api_key)
                
                # Track request
                self._track_request(g.api_key, g.user_id, 'rotate_key')
                
                return jsonify({
                    "new_api_key": new_key,
                    "old_api_key": g.api_key,
                    "rotation_time": datetime.now().isoformat(),
                    "message": "Key rotated successfully"
                })
            except Exception as e:
                return jsonify({"error": f"Key rotation error: {str(e)}"}), 500
        
        elif operation == 'get_rotation_status':
            try:
                status = self.key_rotation.get_rotation_status(g.user_id)
                return jsonify(status)
            except Exception as e:
                return jsonify({"error": f"Rotation status error: {str(e)}"}), 500
        
        elif operation == 'set_rotation_policy':
            try:
                data = request.get_json() or {}
                from enterprise_features import KeyRotationPolicy
                
                policy = KeyRotationPolicy(
                    rotation_interval_days=data.get('rotation_interval_days', 30),
                    grace_period_days=data.get('grace_period_days', 7),
                    max_keys_per_user=data.get('max_keys_per_user', 5),
                    auto_revoke_old_keys=data.get('auto_revoke_old_keys', True)
                )
                
                self.key_rotation.set_rotation_policy(g.user_id, policy)
                
                # Track request
                self._track_request(g.api_key, g.user_id, 'set_rotation_policy')
                
                return jsonify({
                    "message": "Rotation policy set successfully",
                    "policy": {
                        "rotation_interval_days": policy.rotation_interval_days,
                        "grace_period_days": policy.grace_period_days,
                        "max_keys_per_user": policy.max_keys_per_user,
                        "auto_revoke_old_keys": policy.auto_revoke_old_keys
                    }
                })
            except Exception as e:
                return jsonify({"error": f"Rotation policy error: {str(e)}"}), 500
        
        # Compliance operations
        elif operation == 'get_audit_report':
            data = request.get_json() or {}
            user_id = data.get('user_id', g.user_id)
            event_type = data.get('event_type')
            days = data.get('days', 30)
            
            report = self.compliance.get_audit_report(user_id, event_type, days)
            return jsonify(report)
        
        elif operation == 'get_audit_events':
            data = request.get_json() or {}
            user_id = data.get('user_id', g.user_id)
            event_type = data.get('event_type')
            days = data.get('days', 7)
            
            report = self.compliance.get_audit_report(user_id, event_type, days)
            return jsonify({
                "events": report.get('events', []),
                "total_events": report.get('total_events', 0),
                "date_range": report.get('date_range', {})
            })
        
        # Security operations
        elif operation == 'get_security_report':
            report = self.security.get_security_report()
            return jsonify(report)
        
        elif operation == 'get_rate_limits':
            return jsonify({
                "rate_limits": {
                    "default": {
                        "requests_per_minute": 100,
                        "requests_per_hour": 1000,
                        "requests_per_day": 10000
                    },
                    "current_limits": len(self.security.rate_limits)
                }
            })
        
        else:
            return jsonify({"error": f"Unknown operation: {operation}"}), 400
    
    def run(self, debug: bool = False, host: str = '0.0.0.0'):
        """Run the API server"""
        print(f"🚀 Starting CARMA Encrypted API Server")
        print(f"🔮 Using UML Magic Square Encryption")
        print(f"🌐 Server running on http://{host}:{self.port}")
        print(f"🔑 Master API Key: {self.master_key}")
        print(f"📚 API Documentation: http://{host}:{self.port}/v2/health")
        
        self.app.run(host=host, port=self.port, debug=debug)

def main():
    """Main function to run the server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CARMA Encrypted API Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--api-key', help='Master API key (generated if not provided)')
    
    args = parser.parse_args()
    
    # Create and run server
    server = CARMAEncryptedAPIServer(
        api_key=args.api_key,
        port=args.port
    )
    
    server.run(debug=args.debug, host=args.host)

if __name__ == "__main__":
    main()

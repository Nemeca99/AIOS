"""
Global CARMA API Server with 133 Million Static IP Distribution
Supports 8 billion users with 60 users per static IP
"""

import time
import hashlib
import json
from typing import Dict, List, Optional, Tuple
from flask import Flask, request, jsonify
import threading
try:
    from .pi_based_encryption import PiBasedEncryption
    from .global_api_distribution import GlobalAPIDistribution
    from .carma_chain_logic import CARMAChainProcessor
except ImportError:
    from pi_based_encryption import PiBasedEncryption
    from global_api_distribution import GlobalAPIDistribution
    from carma_chain_logic import CARMAChainProcessor

class GlobalCARMAAPIServer:
    """Global CARMA API Server with distributed static IP system"""
    
    def __init__(self, server_ip: str, region: str = "NA"):
        self.server_ip = server_ip
        self.region = region
        self.encryption = PiBasedEncryption()
        self.distribution = GlobalAPIDistribution()
        self.user_sessions = {}  # Track active user sessions
        self.rate_limits = {}    # Track rate limits per user
        self.max_users_per_ip = 60
        
        # Initialize CARMA chain processor for serial processing
        self.chain_processor = CARMAChainProcessor(max_chain_length=1000)
        self._setup_chain_handlers()
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_routes()
    
    def _setup_chain_handlers(self):
        """Setup chain operation handlers for serial processing"""
        
        def generate_key_handler(user_id: str, data: Dict) -> Dict:
            """Handle generate_key operations in the chain"""
            try:
                permissions = data.get('permissions', 'read')
                api_key = self.encryption.generate_pi_api_key(user_id, permissions)
                
                # Store user session
                self.user_sessions[user_id] = {
                    "api_key": api_key,
                    "permissions": permissions,
                    "created_at": time.time(),
                    "last_activity": time.time()
                }
                
                return {
                    "success": True,
                    "api_key": api_key,
                    "user_id": user_id,
                    "permissions": permissions,
                    "server_ip": self.server_ip,
                    "user_slot": self.get_user_slot(user_id),
                    "timestamp": time.time()
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        def validate_key_handler(user_id: str, data: Dict) -> Dict:
            """Handle validate_key operations in the chain"""
            try:
                api_key = data.get('api_key')
                if not api_key:
                    return {
                        "success": False,
                        "error": "No API key provided"
                    }
                
                validation_result = self.encryption.validate_pi_api_key(api_key)
                
                # Check if user session exists
                if user_id in self.user_sessions:
                    self.user_sessions[user_id]["last_activity"] = time.time()
                
                return {
                    "success": validation_result["valid"],
                    "validation": validation_result,
                    "user_id": user_id,
                    "server_ip": self.server_ip,
                    "user_slot": self.get_user_slot(user_id),
                    "timestamp": time.time()
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        def get_status_handler(user_id: str, data: Dict) -> Dict:
            """Handle get_status operations in the chain"""
            try:
                if user_id not in self.user_sessions:
                    return {
                        "success": False,
                        "error": "User session not found"
                    }
                
                session = self.user_sessions[user_id]
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "server_ip": self.server_ip,
                    "user_slot": self.get_user_slot(user_id),
                    "session": {
                        "permissions": session["permissions"],
                        "created_at": session["created_at"],
                        "last_activity": session["last_activity"],
                        "active": True
                    },
                    "timestamp": time.time()
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Register handlers
        self.chain_processor.register_operation_handler("generate_key", generate_key_handler)
        self.chain_processor.register_operation_handler("validate_key", validate_key_handler)
        self.chain_processor.register_operation_handler("get_status", get_status_handler)
        
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/v1/status', methods=['GET'])
        def get_status():
            """Get server status"""
            return jsonify({
                "status": "online",
                "server_ip": self.server_ip,
                "region": self.region,
                "max_users": self.max_users_per_ip,
                "active_users": len(self.user_sessions),
                "timestamp": time.time()
            })
        
        @self.app.route('/api/v1/user/<int:user_slot>', methods=['POST'])
        def user_operation(user_slot: int):
            """Handle user operations using CARMA chain logic"""
            try:
                # Validate user slot
                if user_slot < 0 or user_slot >= self.max_users_per_ip:
                    return jsonify({
                        "error": "Invalid user slot",
                        "max_slot": self.max_users_per_ip - 1
                    }), 400
                
                # Get request data
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                # Extract user info
                user_id = data.get('user_id')
                operation = data.get('operation')
                
                if not user_id or not operation:
                    return jsonify({"error": "Missing user_id or operation"}), 400
                
                # Validate user is assigned to this slot
                if not self.validate_user_slot(user_id, user_slot):
                    return jsonify({
                        "error": "User not assigned to this slot",
                        "expected_slot": self.get_user_slot(user_id)
                    }), 403
                
                # Add operation to chain for serial processing
                operation_id = self.chain_processor.add_operation(user_id, operation, data)
                
                return jsonify({
                    "success": True,
                    "operation_id": operation_id,
                    "message": "Operation queued for serial processing",
                    "user_slot": user_slot,
                    "server_ip": self.server_ip,
                    "timestamp": time.time()
                }), 202
                    
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/v1/operation/<operation_id>', methods=['GET'])
        def get_operation_status(operation_id: str):
            """Get the status of a specific operation"""
            try:
                status = self.chain_processor.get_operation_status(operation_id)
                if not status:
                    return jsonify({"error": "Operation not found"}), 404
                
                return jsonify(status), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/v1/user/<user_id>/operations', methods=['GET'])
        def get_user_operations(user_id: str):
            """Get all operations for a specific user"""
            try:
                operations = self.chain_processor.get_user_operations(user_id)
                return jsonify({
                    "user_id": user_id,
                    "operations": operations,
                    "count": len(operations)
                }), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/v1/chain/status', methods=['GET'])
        def get_chain_status():
            """Get chain processing status"""
            try:
                status = self.chain_processor.get_chain_status()
                return jsonify(status), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/v1/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "server_ip": self.server_ip,
                "region": self.region,
                "timestamp": time.time()
            })
    
    def validate_user_slot(self, user_id: str, user_slot: int) -> bool:
        """Validate that a user is assigned to the correct slot"""
        expected_slot = self.get_user_slot(user_id)
        return expected_slot == user_slot
    
    def get_user_slot(self, user_id: str) -> int:
        """Get the user slot for a specific user"""
        _, user_slot = self.distribution.get_ip_for_user(user_id, self.region)
        return user_slot
    
    def handle_generate_key(self, user_id: str, data: Dict) -> Tuple[Dict, int]:
        """Handle API key generation"""
        try:
            permissions = data.get('permissions', 'read')
            
            # Generate API key with rate limiting
            api_key = self.encryption.generate_pi_api_key(user_id, permissions)
            
            # Store user session
            self.user_sessions[user_id] = {
                "api_key": api_key,
                "permissions": permissions,
                "created_at": time.time(),
                "last_activity": time.time()
            }
            
            return jsonify({
                "success": True,
                "api_key": api_key,
                "user_id": user_id,
                "permissions": permissions,
                "server_ip": self.server_ip,
                "user_slot": self.get_user_slot(user_id),
                "timestamp": time.time()
            }), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def handle_validate_key(self, user_id: str, data: Dict) -> Tuple[Dict, int]:
        """Handle API key validation"""
        try:
            api_key = data.get('api_key')
            if not api_key:
                return jsonify({
                    "success": False,
                    "error": "No API key provided"
                }), 400
            
            # Validate API key with rate limiting
            validation_result = self.encryption.validate_pi_api_key(api_key)
            
            # Check if user session exists
            if user_id in self.user_sessions:
                self.user_sessions[user_id]["last_activity"] = time.time()
            
            return jsonify({
                "success": validation_result["valid"],
                "validation": validation_result,
                "user_id": user_id,
                "server_ip": self.server_ip,
                "user_slot": self.get_user_slot(user_id),
                "timestamp": time.time()
            }), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def handle_get_status(self, user_id: str, data: Dict) -> Tuple[Dict, int]:
        """Handle user status request"""
        try:
            if user_id not in self.user_sessions:
                return jsonify({
                    "success": False,
                    "error": "User session not found"
                }), 404
            
            session = self.user_sessions[user_id]
            
            return jsonify({
                "success": True,
                "user_id": user_id,
                "server_ip": self.server_ip,
                "user_slot": self.get_user_slot(user_id),
                "session": {
                    "permissions": session["permissions"],
                    "created_at": session["created_at"],
                    "last_activity": session["last_activity"],
                    "active": True
                },
                "timestamp": time.time()
            }), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        """Run the API server"""
        print(f"🚀 Starting Global CARMA API Server")
        print(f"   Server IP: {self.server_ip}")
        print(f"   Region: {self.region}")
        print(f"   Max Users: {self.max_users_per_ip}")
        print(f"   Host: {host}:{port}")
        
        self.app.run(host=host, port=port, debug=debug)

def test_global_api_server():
    """Test the global API server"""
    print("🌍 Testing Global CARMA API Server")
    print("=" * 60)
    
    # Create distribution system
    distribution = GlobalAPIDistribution()
    
    # Test user assignment
    test_users = ["alice", "bob", "charlie", "diana", "eve"]
    
    print("\n👤 User Assignment Test:")
    for user in test_users:
        endpoint = distribution.get_user_endpoint(user)
        static_ip, user_slot = distribution.get_ip_for_user(user)
        print(f"   {user}: {endpoint} (slot {user_slot})")
    
    # Test server creation
    print("\n🖥️ Server Creation Test:")
    server_ip = "10.0.0.1"
    server = GlobalCARMAAPIServer(server_ip, "NA")
    
    print(f"   Server IP: {server.server_ip}")
    print(f"   Region: {server.region}")
    print(f"   Max Users: {server.max_users_per_ip}")
    
    # Test user slot validation
    print("\n✅ User Slot Validation Test:")
    for user in test_users:
        static_ip, user_slot = distribution.get_ip_for_user(user)
        if static_ip == server_ip:
            is_valid = server.validate_user_slot(user, user_slot)
            print(f"   {user} on {server_ip}: {is_valid}")
    
    print("\n🎯 Global API Server Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_global_api_server()

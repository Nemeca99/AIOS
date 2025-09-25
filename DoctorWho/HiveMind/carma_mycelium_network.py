"""
CARMA Mycelium Network System
Each server block acts as a router with internal IPs
Automatic traffic monitoring and auto-blocking
"""

import time
import hashlib
import threading
import queue
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import json
import ipaddress

class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    BLOCKED = "blocked"
    SUSPICIOUS = "suspicious"

class TrafficType(Enum):
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"
    UNKNOWN = "unknown"

@dataclass
class UserConnection:
    """Represents a user connection to a server block"""
    user_id: str
    connection_id: str
    slot_number: int
    api_key: str
    connected_at: float
    last_activity: float
    status: ConnectionStatus
    internal_ip: str
    traffic_count: int = 0
    suspicious_activity: int = 0

@dataclass
class TrafficEvent:
    """Represents a traffic event for monitoring"""
    timestamp: float
    source_ip: str
    destination_ip: str
    user_id: str
    traffic_type: TrafficType
    data_size: int
    protocol: str
    suspicious_score: float = 0.0

@dataclass
class ServerBlock:
    """Represents a server block (router) in the mycelium network"""
    block_id: str
    external_ip: str
    internal_network: str
    max_users: int = 60
    connected_users: Dict[int, UserConnection] = None
    traffic_monitor: List[TrafficEvent] = None
    blocked_ips: Set[str] = None
    suspicious_ips: Set[str] = None
    
    def __post_init__(self):
        if self.connected_users is None:
            self.connected_users = {}
        if self.traffic_monitor is None:
            self.traffic_monitor = []
        if self.blocked_ips is None:
            self.blocked_ips = set()
        if self.suspicious_ips is None:
            self.suspicious_ips = set()

class CARMAMyceliumNetwork:
    """Mycelium-like internal network for CARMA system"""
    
    def __init__(self, num_initial_blocks: int = 20, users_per_block: int = 60):
        self.server_blocks: Dict[str, ServerBlock] = {}
        self.global_traffic_monitor: List[TrafficEvent] = []
        self.network_lock = threading.Lock()
        self.traffic_analysis_thread = None
        self.is_monitoring = False
        self.num_initial_blocks = num_initial_blocks
        self.users_per_block = users_per_block
        
        # Network configuration
        self.internal_network_base = "10.0.0.0/8"  # Internal network range
        self.max_traffic_history = 10000
        self.suspicious_threshold = 5.0
        self.auto_block_threshold = 10.0
        
    def create_server_block(self, block_id: str, external_ip: str) -> ServerBlock:
        """Create a new server block in the mycelium network"""
        # Generate internal network for this block
        internal_network = self._generate_internal_network(block_id)
        
        server_block = ServerBlock(
            block_id=block_id,
            external_ip=external_ip,
            internal_network=internal_network,
            max_users=60
        )
        
        with self.network_lock:
            self.server_blocks[block_id] = server_block
        
        print(f"🌐 Created Server Block: {block_id}")
        print(f"   External IP: {external_ip}")
        print(f"   Internal Network: {internal_network}")
        print(f"   Max Users: 60")
        
        return server_block
    
    def _generate_internal_network(self, block_id: str) -> str:
        """Generate internal network for a server block"""
        # Use block_id to generate deterministic internal network
        hash_value = hashlib.md5(block_id.encode()).hexdigest()
        network_id = int(hash_value[:4], 16) % 254 + 1  # 1-254
        return f"192.168.{network_id}.0/24"
    
    def connect_user(self, block_id: str, user_id: str, api_key: str) -> Optional[UserConnection]:
        """Connect a user to a server block"""
        with self.network_lock:
            if block_id not in self.server_blocks:
                return None
            
            server_block = self.server_blocks[block_id]
            
            # Check if user is already connected
            for conn in server_block.connected_users.values():
                if conn.user_id == user_id:
                    conn.last_activity = time.time()
                    return conn
            
            # Find next available slot
            available_slot = self._find_available_slot(server_block)
            if available_slot is None:
                return None
            
            # Generate internal IP for this user
            internal_ip = self._generate_internal_ip(server_block, available_slot)
            
            # Create connection
            connection_id = f"{block_id}_{user_id}_{int(time.time())}"
            connection = UserConnection(
                user_id=user_id,
                connection_id=connection_id,
                slot_number=available_slot,
                api_key=api_key,
                connected_at=time.time(),
                last_activity=time.time(),
                status=ConnectionStatus.CONNECTED,
                internal_ip=internal_ip
            )
            
            # Add to server block
            server_block.connected_users[available_slot] = connection
            
            print(f"🔗 User Connected: {user_id}")
            print(f"   Server Block: {block_id}")
            print(f"   Slot: {available_slot}")
            print(f"   Internal IP: {internal_ip}")
            print(f"   External IP: {server_block.external_ip}")
            
            return connection
    
    def disconnect_user(self, block_id: str, user_id: str) -> bool:
        """Disconnect a user from a server block"""
        with self.network_lock:
            if block_id not in self.server_blocks:
                return False
            
            server_block = self.server_blocks[block_id]
            
            # Find and remove user
            for slot, conn in list(server_block.connected_users.items()):
                if conn.user_id == user_id:
                    conn.status = ConnectionStatus.DISCONNECTED
                    del server_block.connected_users[slot]
                    
                    print(f"🔌 User Disconnected: {user_id}")
                    print(f"   Server Block: {block_id}")
                    print(f"   Slot: {slot}")
                    
                    return True
            
            return False
    
    def _find_available_slot(self, server_block: ServerBlock) -> Optional[int]:
        """Find next available slot in server block"""
        for slot in range(server_block.max_users):
            if slot not in server_block.connected_users:
                return slot
        return None
    
    def _generate_internal_ip(self, server_block: ServerBlock, slot: int) -> str:
        """Generate internal IP for user slot"""
        network = ipaddress.IPv4Network(server_block.internal_network)
        base_ip = str(network.network_address + 1)  # First usable IP
        base_parts = base_ip.split('.')
        return f"{base_parts[0]}.{base_parts[1]}.{base_parts[2]}.{slot + 1}"
    
    def route_traffic(self, source_ip: str, destination_ip: str, user_id: str, 
                     data_size: int, protocol: str = "HTTP") -> bool:
        """Route traffic through the mycelium network"""
        # Find source server block
        source_block = self._find_server_block_by_ip(source_ip)
        if not source_block:
            return False
        
        # Check if IP is blocked
        if source_ip in source_block.blocked_ips:
            self._log_traffic_event(source_ip, destination_ip, user_id, 
                                  TrafficType.MALICIOUS, data_size, protocol, 10.0)
            return False
        
        # Check if IP is suspicious
        if source_ip in source_block.suspicious_ips:
            self._log_traffic_event(source_ip, destination_ip, user_id, 
                                  TrafficType.SUSPICIOUS, data_size, protocol, 5.0)
        
        # Log traffic event
        self._log_traffic_event(source_ip, destination_ip, user_id, 
                              TrafficType.NORMAL, data_size, protocol, 0.0)
        
        # Update user activity
        self._update_user_activity(source_block, user_id)
        
        return True
    
    def _find_server_block_by_ip(self, ip: str) -> Optional[ServerBlock]:
        """Find server block by external IP"""
        for server_block in self.server_blocks.values():
            if server_block.external_ip == ip:
                return server_block
        return None
    
    def _log_traffic_event(self, source_ip: str, destination_ip: str, user_id: str,
                          traffic_type: TrafficType, data_size: int, protocol: str, 
                          suspicious_score: float):
        """Log traffic event for monitoring"""
        event = TrafficEvent(
            timestamp=time.time(),
            source_ip=source_ip,
            destination_ip=destination_ip,
            user_id=user_id,
            traffic_type=traffic_type,
            data_size=data_size,
            protocol=protocol,
            suspicious_score=suspicious_score
        )
        
        with self.network_lock:
            self.global_traffic_monitor.append(event)
            
            # Keep history manageable
            if len(self.global_traffic_monitor) > self.max_traffic_history:
                self.global_traffic_monitor = self.global_traffic_monitor[-self.max_traffic_history:]
    
    def _update_user_activity(self, server_block: ServerBlock, user_id: str):
        """Update user activity timestamp"""
        for conn in server_block.connected_users.values():
            if conn.user_id == user_id:
                conn.last_activity = time.time()
                conn.traffic_count += 1
                break
    
    def start_traffic_monitoring(self):
        """Start automatic traffic monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.traffic_analysis_thread = threading.Thread(target=self._monitor_traffic, daemon=True)
        self.traffic_analysis_thread.start()
        
        print("🔍 Started Traffic Monitoring")
    
    def stop_traffic_monitoring(self):
        """Stop traffic monitoring"""
        self.is_monitoring = False
        if self.traffic_analysis_thread:
            self.traffic_analysis_thread.join(timeout=5.0)
        
        print("🛑 Stopped Traffic Monitoring")
    
    def _monitor_traffic(self):
        """Monitor traffic for suspicious activity"""
        while self.is_monitoring:
            try:
                self._analyze_traffic()
                time.sleep(1.0)  # Check every second
            except Exception as e:
                print(f"Error in traffic monitoring: {e}")
    
    def _analyze_traffic(self):
        """Analyze traffic for suspicious patterns"""
        with self.network_lock:
            current_time = time.time()
            
            # Analyze recent traffic (last 60 seconds)
            recent_events = [
                event for event in self.global_traffic_monitor
                if current_time - event.timestamp < 60
            ]
            
            # Group by source IP
            ip_traffic = {}
            for event in recent_events:
                if event.source_ip not in ip_traffic:
                    ip_traffic[event.source_ip] = []
                ip_traffic[event.source_ip].append(event)
            
            # Check each IP for suspicious activity
            for source_ip, events in ip_traffic.items():
                suspicious_score = self._calculate_suspicious_score(events)
                
                if suspicious_score > self.auto_block_threshold:
                    self._auto_block_ip(source_ip, "High suspicious activity")
                elif suspicious_score > self.suspicious_threshold:
                    self._mark_ip_suspicious(source_ip, "Suspicious activity detected")
    
    def _calculate_suspicious_score(self, events: List[TrafficEvent]) -> float:
        """Calculate suspicious score for IP events"""
        if not events:
            return 0.0
        
        score = 0.0
        
        # High traffic volume
        total_data = sum(event.data_size for event in events)
        if total_data > 1000000:  # 1MB in 60 seconds
            score += 3.0
        
        # High request frequency
        if len(events) > 100:  # 100 requests in 60 seconds
            score += 2.0
        
        # Multiple destinations
        destinations = set(event.destination_ip for event in events)
        if len(destinations) > 10:
            score += 2.0
        
        # High suspicious score from events
        avg_suspicious = sum(event.suspicious_score for event in events) / len(events)
        score += avg_suspicious
        
        return score
    
    def _auto_block_ip(self, ip: str, reason: str):
        """Automatically block an IP"""
        for server_block in self.server_blocks.values():
            if ip in server_block.internal_network or ip == server_block.external_ip:
                server_block.blocked_ips.add(ip)
                print(f"🚫 AUTO-BLOCKED IP: {ip}")
                print(f"   Reason: {reason}")
                print(f"   Server Block: {server_block.block_id}")
                break
    
    def _mark_ip_suspicious(self, ip: str, reason: str):
        """Mark an IP as suspicious"""
        for server_block in self.server_blocks.values():
            if ip in server_block.internal_network or ip == server_block.external_ip:
                server_block.suspicious_ips.add(ip)
                print(f"⚠️ SUSPICIOUS IP: {ip}")
                print(f"   Reason: {reason}")
                print(f"   Server Block: {server_block.block_id}")
                break
    
    def unblock_ip(self, ip: str) -> bool:
        """Manually unblock an IP"""
        with self.network_lock:
            for server_block in self.server_blocks.values():
                if ip in server_block.blocked_ips:
                    server_block.blocked_ips.remove(ip)
                    print(f"✅ UNBLOCKED IP: {ip}")
                    print(f"   Server Block: {server_block.block_id}")
                    return True
            return False
    
    def get_network_status(self) -> Dict[str, any]:
        """Get overall network status"""
        with self.network_lock:
            total_blocks = len(self.server_blocks)
            total_connections = sum(len(block.connected_users) for block in self.server_blocks.values())
            total_blocked = sum(len(block.blocked_ips) for block in self.server_blocks.values())
            total_suspicious = sum(len(block.suspicious_ips) for block in self.server_blocks.values())
            
            return {
                "total_blocks": total_blocks,
                "total_connections": total_connections,
                "total_blocked_ips": total_blocked,
                "total_suspicious_ips": total_suspicious,
                "is_monitoring": self.is_monitoring,
                "traffic_events": len(self.global_traffic_monitor)
            }
    
    def get_server_block_status(self, block_id: str) -> Optional[Dict[str, any]]:
        """Get status of specific server block"""
        with self.network_lock:
            if block_id not in self.server_blocks:
                return None
            
            block = self.server_blocks[block_id]
            return {
                "block_id": block_id,
                "external_ip": block.external_ip,
                "internal_network": block.internal_network,
                "max_users": block.max_users,
                "connected_users": len(block.connected_users),
                "blocked_ips": list(block.blocked_ips),
                "suspicious_ips": list(block.suspicious_ips),
                "users": [
                    {
                        "user_id": conn.user_id,
                        "slot": conn.slot_number,
                        "internal_ip": conn.internal_ip,
                        "status": conn.status.value,
                        "connected_at": conn.connected_at,
                        "traffic_count": conn.traffic_count
                    }
                    for conn in block.connected_users.values()
                ]
            }
    
    def ping_network(self) -> Dict[str, any]:
        """Ping the entire network to show connectivity"""
        with self.network_lock:
            ping_results = {}
            
            for block_id, block in self.server_blocks.items():
                ping_results[block_id] = {
                    "external_ip": block.external_ip,
                    "internal_network": block.internal_network,
                    "connected_users": len(block.connected_users),
                    "status": "online",
                    "users": [
                        {
                            "user_id": conn.user_id,
                            "internal_ip": conn.internal_ip,
                            "status": conn.status.value
                        }
                        for conn in block.connected_users.values()
                    ]
                }
            
            return {
                "network_ping": "success",
                "timestamp": time.time(),
                "blocks": ping_results
            }

def test_mycelium_network():
    """Test the mycelium network system"""
    print("🍄 Testing CARMA Mycelium Network")
    print("=" * 50)
    
    # Create mycelium network
    network = CARMAMyceliumNetwork()
    
    # Test 1: Create server blocks
    print("\n🌐 Creating Server Blocks:")
    block1 = network.create_server_block("block_001", "203.0.113.1")
    block2 = network.create_server_block("block_002", "203.0.113.2")
    block3 = network.create_server_block("block_003", "203.0.113.3")
    
    # Test 2: Connect users
    print("\n🔗 Connecting Users:")
    users = ["alice", "bob", "charlie", "diana", "eve"]
    
    for i, user in enumerate(users):
        block_id = f"block_{i % 3 + 1:03d}"
        api_key = f"carma_{user}_{int(time.time())}"
        
        connection = network.connect_user(block_id, user, api_key)
        if connection:
            print(f"   {user} -> {block_id} (slot {connection.slot_number})")
    
    # Test 3: Start traffic monitoring
    print("\n🔍 Starting Traffic Monitoring:")
    network.start_traffic_monitoring()
    
    # Test 4: Simulate traffic
    print("\n📡 Simulating Traffic:")
    for i in range(10):
        source_ip = "203.0.113.1"
        dest_ip = "203.0.113.2"
        user_id = "alice"
        
        success = network.route_traffic(source_ip, dest_ip, user_id, 1024, "HTTP")
        print(f"   Traffic {i+1}: {'✅' if success else '❌'}")
        time.sleep(0.1)
    
    # Test 5: Check network status
    print("\n📊 Network Status:")
    status = network.get_network_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Test 6: Check server block status
    print("\n🖥️ Server Block Status:")
    for block_id in ["block_001", "block_002", "block_003"]:
        block_status = network.get_server_block_status(block_id)
        if block_status:
            print(f"   {block_id}:")
            print(f"      External IP: {block_status['external_ip']}")
            print(f"      Internal Network: {block_status['internal_network']}")
            print(f"      Connected Users: {block_status['connected_users']}")
            print(f"      Blocked IPs: {len(block_status['blocked_ips'])}")
            print(f"      Suspicious IPs: {len(block_status['suspicious_ips'])}")
    
    # Test 7: Ping network
    print("\n🏓 Network Ping:")
    ping_result = network.ping_network()
    print(f"   Network Status: {ping_result['network_ping']}")
    print(f"   Total Blocks: {len(ping_result['blocks'])}")
    
    # Test 8: Disconnect user
    print("\n🔌 Disconnecting User:")
    success = network.disconnect_user("block_001", "alice")
    print(f"   Alice disconnected: {'✅' if success else '❌'}")
    
    # Test 9: Final status
    print("\n📊 Final Network Status:")
    final_status = network.get_network_status()
    for key, value in final_status.items():
        print(f"   {key}: {value}")
    
    # Stop monitoring
    network.stop_traffic_monitoring()
    
    print("\n🎯 Mycelium Network Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_mycelium_network()

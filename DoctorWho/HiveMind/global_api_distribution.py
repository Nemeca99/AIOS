"""
Global API Distribution System
Supports 8 billion users with 60 users per static IP
Total: 133.3 million static IPs required
"""

import hashlib
import math
from typing import Dict, List, Tuple, Optional
import time

class GlobalAPIDistribution:
    """Manages global API distribution with 60 users per static IP"""
    
    def __init__(self):
        self.USERS_PER_IP = 60
        self.TOTAL_POPULATION = 8_000_000_000  # 8 billion
        self.TOTAL_IPS_NEEDED = math.ceil(self.TOTAL_POPULATION / self.USERS_PER_IP)  # 133,333,334 IPs
        self.IP_PREFIX = "carma.global"
        self.REGION_PREFIXES = {
            "NA": "na",  # North America
            "EU": "eu",  # Europe
            "AS": "as",  # Asia
            "AF": "af",  # Africa
            "SA": "sa",  # South America
            "OC": "oc",  # Oceania
            "AN": "an"   # Antarctica (for completeness)
        }
        
    def calculate_required_ips(self) -> Dict[str, int]:
        """Calculate the total number of IPs needed globally"""
        return {
            "users_per_ip": self.USERS_PER_IP,
            "total_population": self.TOTAL_POPULATION,
            "total_ips_needed": self.TOTAL_IPS_NEEDED,
            "coverage_percentage": (self.TOTAL_IPS_NEEDED / self.TOTAL_POPULATION) * 100
        }
    
    def generate_static_ip(self, ip_number: int, region: str = "NA") -> str:
        """Generate a static IP for a specific number and region"""
        if ip_number > self.TOTAL_IPS_NEEDED:
            raise ValueError(f"IP number {ip_number} exceeds maximum {self.TOTAL_IPS_NEEDED}")
        
        # Create deterministic IP based on number and region
        region_prefix = self.REGION_PREFIXES.get(region, "na")
        
        # Generate IP components
        ip_hash = hashlib.sha256(f"{ip_number}_{region}_{self.IP_PREFIX}".encode()).hexdigest()
        
        # Create IP address (using private IP ranges for demonstration)
        octet1 = 10 + (int(ip_hash[:2], 16) % 16)  # 10.0.0.0 to 10.255.255.255
        octet2 = int(ip_hash[2:4], 16) % 256
        octet3 = int(ip_hash[4:6], 16) % 256
        octet4 = int(ip_hash[6:8], 16) % 256
        
        return f"{octet1}.{octet2}.{octet3}.{octet4}"
    
    def get_ip_for_user(self, user_id: str, region: str = "NA") -> Tuple[str, int]:
        """Get the static IP and user slot for a specific user"""
        # Create deterministic hash for user
        user_hash = hashlib.sha256(f"{user_id}_{region}".encode()).hexdigest()
        
        # Calculate IP number (0 to TOTAL_IPS_NEEDED-1)
        ip_number = int(user_hash[:8], 16) % self.TOTAL_IPS_NEEDED
        
        # Calculate user slot within that IP (0 to USERS_PER_IP-1)
        user_slot = int(user_hash[8:12], 16) % self.USERS_PER_IP
        
        # Generate the static IP
        static_ip = self.generate_static_ip(ip_number, region)
        
        return static_ip, user_slot
    
    def get_user_endpoint(self, user_id: str, region: str = "NA") -> str:
        """Get the full API endpoint for a user"""
        static_ip, user_slot = self.get_ip_for_user(user_id, region)
        return f"https://{static_ip}/api/v1/user/{user_slot}"
    
    def validate_user_endpoint(self, user_id: str, endpoint: str, region: str = "NA") -> bool:
        """Validate that a user is calling the correct endpoint"""
        expected_endpoint = self.get_user_endpoint(user_id, region)
        return endpoint == expected_endpoint
    
    def get_ip_statistics(self, ip_number: int) -> Dict[str, any]:
        """Get statistics for a specific IP"""
        static_ip = self.generate_static_ip(ip_number)
        
        # Calculate which users would be assigned to this IP
        users_on_ip = []
        for user_slot in range(self.USERS_PER_IP):
            # This is a simplified calculation - in reality, you'd need to reverse-engineer
            # which user_ids map to this IP and slot
            users_on_ip.append(f"slot_{user_slot}")
        
        return {
            "ip_number": ip_number,
            "static_ip": static_ip,
            "max_users": self.USERS_PER_IP,
            "current_users": len(users_on_ip),
            "utilization": (len(users_on_ip) / self.USERS_PER_IP) * 100,
            "user_slots": users_on_ip
        }
    
    def get_global_coverage_map(self) -> Dict[str, any]:
        """Get global coverage statistics"""
        coverage_by_region = {}
        
        for region, prefix in self.REGION_PREFIXES.items():
            # Calculate IPs needed for this region (simplified)
            region_ips = self.TOTAL_IPS_NEEDED // len(self.REGION_PREFIXES)
            coverage_by_region[region] = {
                "prefix": prefix,
                "ips_allocated": region_ips,
                "max_users": region_ips * self.USERS_PER_IP,
                "coverage_percentage": (region_ips / self.TOTAL_IPS_NEEDED) * 100
            }
        
        return {
            "total_ips_needed": self.TOTAL_IPS_NEEDED,
            "users_per_ip": self.USERS_PER_IP,
            "total_capacity": self.TOTAL_IPS_NEEDED * self.USERS_PER_IP,
            "global_population": self.TOTAL_POPULATION,
            "coverage_percentage": (self.TOTAL_IPS_NEEDED * self.USERS_PER_IP / self.TOTAL_POPULATION) * 100,
            "regions": coverage_by_region
        }
    
    def generate_load_balancer_config(self, region: str = "NA") -> str:
        """Generate load balancer configuration for a region"""
        region_ips = self.TOTAL_IPS_NEEDED // len(self.REGION_PREFIXES)
        
        config = f"""
# Load Balancer Configuration for {region}
upstream carma_{region.lower()}_servers {{
"""
        
        for i in range(region_ips):
            ip = self.generate_static_ip(i, region)
            config += f"    server {ip}:443 weight=1 max_fails=3 fail_timeout=30s;\n"
        
        config += """}

server {
    listen 443 ssl;
    server_name carma.global;
    
    location /api/v1/ {
        proxy_pass http://carma_""" + region.lower() + """_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
        return config

def test_global_distribution():
    """Test the global API distribution system"""
    print("🌍 Testing Global API Distribution System")
    print("=" * 60)
    
    distribution = GlobalAPIDistribution()
    
    # Test 1: Calculate required IPs
    print("\n📊 Global Coverage Requirements:")
    stats = distribution.calculate_required_ips()
    for key, value in stats.items():
        print(f"   {key}: {value:,}")
    
    # Test 2: Generate some static IPs
    print("\n🔗 Sample Static IPs:")
    for i in range(10):
        ip = distribution.generate_static_ip(i)
        print(f"   IP {i}: {ip}")
    
    # Test 3: User endpoint assignment
    print("\n👤 User Endpoint Assignment:")
    test_users = ["alice", "bob", "charlie", "diana", "eve"]
    for user in test_users:
        endpoint = distribution.get_user_endpoint(user)
        print(f"   {user}: {endpoint}")
    
    # Test 4: Endpoint validation
    print("\n✅ Endpoint Validation:")
    user = "test_user"
    correct_endpoint = distribution.get_user_endpoint(user)
    wrong_endpoint = "https://wrong.ip/api/v1/user/0"
    
    print(f"   Correct endpoint: {correct_endpoint}")
    print(f"   Validation (correct): {distribution.validate_user_endpoint(user, correct_endpoint)}")
    print(f"   Validation (wrong): {distribution.validate_user_endpoint(user, wrong_endpoint)}")
    
    # Test 5: Global coverage map
    print("\n🗺️ Global Coverage Map:")
    coverage = distribution.get_global_coverage_map()
    print(f"   Total IPs needed: {coverage['total_ips_needed']:,}")
    print(f"   Total capacity: {coverage['total_capacity']:,}")
    print(f"   Global population: {coverage['global_population']:,}")
    print(f"   Coverage: {coverage['coverage_percentage']:.2f}%")
    
    print("\n🎯 Global Distribution Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_global_distribution()

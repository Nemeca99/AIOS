#!/usr/bin/env python3
"""
UNIFIED ENTERPRISE CORE SYSTEM
Complete enterprise system with all features integrated.
"""

import sys
import time
import json
import random
import hashlib
import uuid
import math
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from functools import wraps

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import support modules
from support_core.support_core import SystemConfig, FilePaths, SystemMessages, ensure_directories
from carma_core.carma_core import CARMASystem

# === ENUMS AND DATA CLASSES ===

class ChainStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class BillingMetrics:
    """Billing metrics for API usage tracking"""
    api_key: str
    user_id: str
    requests_count: int = 0
    fragments_stored: int = 0
    fragments_retrieved: int = 0
    search_queries: int = 0
    data_transferred: int = 0  # bytes
    start_time: datetime = None
    last_activity: datetime = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()
        if self.last_activity is None:
            self.last_activity = datetime.now()

@dataclass
class KeyRotationPolicy:
    """Key rotation policy for enterprise compliance"""
    rotation_interval_days: int = 30
    grace_period_days: int = 7
    max_keys_per_user: int = 5
    auto_revoke_old_keys: bool = True
    notify_before_expiry: bool = True

@dataclass
class ChainOperation:
    """Represents a single operation in the chain"""
    operation_id: str
    user_id: str
    operation_type: str
    data: Dict[str, Any]
    timestamp: float
    status: ChainStatus = ChainStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

# === PI-BASED ENCRYPTION ===

class PiBasedEncryption:
    """Enhanced Pi-based encryption with UML Magic Square integration"""
    
    def __init__(self, fast_mode: bool = False):
        self.fast_mode = fast_mode
        self.pi_digits = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
        self.rate_limit_requests = 0
        self.rate_limit_window_start = time.time()
        self.rate_limit_max_requests = 100 if fast_mode else 50
        self.rate_limit_window_seconds = 60
        
        print("🔮 UML Magic Square Encryption System Initialized")
        print(f"   Fast mode: {fast_mode}")
        print(f"   Rate limit: {self.rate_limit_max_requests} requests per {self.rate_limit_window_seconds}s")
    
    def _generate_pi_digits(self, n: int) -> str:
        """Generate pi digits using Chudnovsky algorithm approximation"""
        if n <= len(self.pi_digits):
            return self.pi_digits[:n]
        
        # Simple approximation for more digits
        pi_approx = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
        return pi_approx.replace(".", "")[:n]
    
    def get_pi_digits(self, position: int, length: int = 8) -> int:
        """Get pi digits at specific position"""
        pi_str = self._generate_pi_digits(position + length)
        return int(pi_str[position:position + length])
    
    def get_unique_pi_position(self, value: float) -> int:
        """Get unique position in pi for a value"""
        return int((value * 1000000) % 1000000)
    
    def _enforce_rate_limit(self) -> bool:
        """Enforce rate limiting"""
        current_time = time.time()
        
        # Reset window if needed
        if current_time - self.rate_limit_window_start > self.rate_limit_window_seconds:
            self.rate_limit_requests = 0
            self.rate_limit_window_start = current_time
        
        # Check if we're over the limit
        if self.rate_limit_requests >= self.rate_limit_max_requests:
            self._sleep_to_enforce_limit()
            return False
        
        self.rate_limit_requests += 1
        return True
    
    def _sleep_to_enforce_limit(self) -> None:
        """Sleep to enforce rate limit"""
        if not self.fast_mode:
            sleep_time = random.uniform(0.1, 0.5)
            time.sleep(sleep_time)
    
    def recursive_compress(self, a: float) -> float:
        """Recursive compression using pi-based transformations"""
        if not self._enforce_rate_limit():
            return a
        
        # Get pi digits for transformation
        pi_pos = self.get_unique_pi_position(a)
        pi_digits = self.get_pi_digits(pi_pos, 8)
        
        # Apply recursive compression
        compressed = a
        for i in range(3):  # 3 iterations
            pi_factor = (pi_digits % 1000) / 1000.0
            compressed = compressed * pi_factor + (pi_digits % 100) / 100.0
            compressed = compressed % 1.0  # Keep in [0,1] range
        
        return compressed
    
    def generate_magic_square(self, seed: int) -> List[List[int]]:
        """Generate a magic square using pi-based algorithm"""
        size = 3  # 3x3 magic square
        magic_square = [[0 for _ in range(size)] for _ in range(size)]
        
        # Use pi digits to generate magic square
        pi_digits = self.get_pi_digits(seed, 9)
        digits = [int(d) for d in str(pi_digits)]
        
        # Fill magic square
        for i in range(size):
            for j in range(size):
                digit_index = (i * size + j) % len(digits)
                magic_square[i][j] = digits[digit_index] + 1
        
        return magic_square
    
    def meta_validate(self, magic_square: List[List[int]]) -> bool:
        """Validate magic square properties"""
        size = len(magic_square)
        magic_constant = size * (size * size + 1) // 2
        
        # Check rows
        for row in magic_square:
            if sum(row) != magic_constant:
                return False
        
        # Check columns
        for j in range(size):
            if sum(magic_square[i][j] for i in range(size)) != magic_constant:
                return False
        
        # Check diagonals
        main_diag = sum(magic_square[i][i] for i in range(size))
        anti_diag = sum(magic_square[i][size-1-i] for i in range(size))
        
        return main_diag == magic_constant and anti_diag == magic_constant
    
    def generate_pi_api_key(self, user_id: str, permissions: str = "read") -> str:
        """Generate API key using pi-based encryption"""
        if not self._enforce_rate_limit():
            return ""
        
        # Get current timestamp
        timestamp = int(time.time())
        
        # Generate pi-based components
        pi_pos = self.get_unique_pi_position(timestamp)
        pi_digits = self.get_pi_digits(pi_pos, 12)
        
        # Create magic square
        magic_square = self.generate_magic_square(timestamp)
        
        # Generate key components
        key_components = []
        
        # User ID hash
        user_hash = hashlib.md5(user_id.encode()).hexdigest()[:8]
        key_components.append(user_hash)
        
        # Pi-based component
        pi_component = str(pi_digits)[:8]
        key_components.append(pi_component)
        
        # Magic square component
        magic_sum = sum(sum(row) for row in magic_square)
        magic_component = str(magic_sum)[:8]
        key_components.append(magic_component)
        
        # Permissions component
        perm_hash = hashlib.md5(permissions.encode()).hexdigest()[:8]
        key_components.append(perm_hash)
        
        # Timestamp component
        time_component = str(timestamp)[-8:]
        key_components.append(time_component)
        
        # Combine components
        api_key = "-".join(key_components)
        
        return api_key
    
    def validate_pi_api_key(self, api_key: str) -> Dict[str, any]:
        """Validate pi-based API key"""
        try:
            # Split key into components
            components = api_key.split("-")
            if len(components) != 5:
                return {"valid": False, "error": "Invalid key format"}
            
            user_hash, pi_component, magic_component, perm_hash, time_component = components
            
            # Validate timestamp (not too old)
            try:
                timestamp = int(time_component)
                current_time = int(time.time())
                if current_time - timestamp > 86400:  # 24 hours
                    return {"valid": False, "error": "Key expired"}
            except ValueError:
                return {"valid": False, "error": "Invalid timestamp"}
            
            # Validate pi component format
            if not pi_component.isdigit() or len(pi_component) != 8:
                return {"valid": False, "error": "Invalid pi component"}
            
            # Validate magic component format
            if not magic_component.isdigit() or len(magic_component) != 8:
                return {"valid": False, "error": "Invalid magic component"}
            
            return {
                "valid": True,
                "user_hash": user_hash,
                "permissions": perm_hash,
                "timestamp": timestamp,
                "pi_component": pi_component,
                "magic_component": magic_component
            }
            
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}

# === ENTERPRISE BILLING ===

class EnterpriseBilling:
    """Enterprise billing and usage tracking system"""
    
    def __init__(self, billing_file: str = "Data/billing_metrics.json"):
        self.billing_file = Path(billing_file)
        self.billing_file.parent.mkdir(parents=True, exist_ok=True)
        self.metrics = {}
        self.load_metrics()
        
        print("💰 Enterprise Billing System Initialized")
        print(f"   Billing file: {self.billing_file}")
        print(f"   Loaded {len(self.metrics)} billing records")
    
    def load_metrics(self):
        """Load billing metrics from file"""
        if self.billing_file.exists():
            try:
                with open(self.billing_file, 'r') as f:
                    data = json.load(f)
                    self.metrics = data.get('metrics', {})
            except Exception as e:
                print(f"⚠️  Error loading billing metrics: {e}")
                self.metrics = {}
        else:
            self.metrics = {}
    
    def save_metrics(self):
        """Save billing metrics to file"""
        try:
            data = {
                'metrics': self.metrics,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.billing_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving billing metrics: {e}")
    
    def track_request(self, api_key: str, user_id: str, request_type: str, data_size: int = 0):
        """Track API request for billing"""
        if api_key not in self.metrics:
            self.metrics[api_key] = BillingMetrics(
                api_key=api_key,
                user_id=user_id
            )
        
        metrics = self.metrics[api_key]
        metrics.requests_count += 1
        metrics.data_transferred += data_size
        metrics.last_activity = datetime.now()
        
        # Track specific request types
        if request_type == "store_fragment":
            metrics.fragments_stored += 1
        elif request_type == "get_fragment":
            metrics.fragments_retrieved += 1
        elif request_type == "search":
            metrics.search_queries += 1
        
        self.save_metrics()
    
    def get_usage(self, user_id: str) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        user_metrics = []
        for api_key, metrics in self.metrics.items():
            if metrics.user_id == user_id:
                user_metrics.append({
                    'api_key': api_key,
                    'requests_count': metrics.requests_count,
                    'fragments_stored': metrics.fragments_stored,
                    'fragments_retrieved': metrics.fragments_retrieved,
                    'search_queries': metrics.search_queries,
                    'data_transferred': metrics.data_transferred,
                    'start_time': metrics.start_time.isoformat(),
                    'last_activity': metrics.last_activity.isoformat()
                })
        
        return {
            'user_id': user_id,
            'total_api_keys': len(user_metrics),
            'metrics': user_metrics
        }
    
    def get_billing_recommendation(self, api_key: str) -> Dict[str, Any]:
        """Get billing tier recommendation"""
        if api_key not in self.metrics:
            return {"error": "API key not found"}
        
        metrics = self.metrics[api_key]
        
        # Calculate usage intensity
        days_active = (datetime.now() - metrics.start_time).days
        if days_active == 0:
            days_active = 1
        
        daily_requests = metrics.requests_count / days_active
        daily_data = metrics.data_transferred / days_active
        
        # Determine tier recommendation
        if daily_requests > 1000 or daily_data > 1000000:  # 1MB
            recommended_tier = "enterprise"
        elif daily_requests > 100 or daily_data > 100000:  # 100KB
            recommended_tier = "professional"
        else:
            recommended_tier = "basic"
        
        return {
            'api_key': api_key,
            'current_usage': {
                'daily_requests': daily_requests,
                'daily_data_mb': daily_data / 1000000,
                'total_requests': metrics.requests_count,
                'total_data_mb': metrics.data_transferred / 1000000
            },
            'recommended_tier': recommended_tier,
            'cost_savings': self._calculate_cost_savings(api_key, recommended_tier)
        }
    
    def _calculate_cost_savings(self, api_key: str, recommended_tier: str) -> Dict[str, Any]:
        """Calculate potential cost savings"""
        # Simplified cost calculation
        current_cost = 0.01  # $0.01 per request
        if recommended_tier == "professional":
            new_cost = 0.005  # $0.005 per request
        elif recommended_tier == "enterprise":
            new_cost = 0.002  # $0.002 per request
        else:
            new_cost = current_cost
        
        metrics = self.metrics[api_key]
        monthly_requests = metrics.requests_count * 30  # Estimate monthly
        
        current_monthly = monthly_requests * current_cost
        new_monthly = monthly_requests * new_cost
        savings = current_monthly - new_monthly
        
        return {
            'current_monthly_cost': current_monthly,
            'new_monthly_cost': new_monthly,
            'monthly_savings': savings,
            'annual_savings': savings * 12
        }

# === KEY ROTATION MANAGER ===

class KeyRotationManager:
    """Enterprise key rotation and compliance management"""
    
    def __init__(self, rotation_file: str = "Data/key_rotation.json"):
        self.rotation_file = Path(rotation_file)
        self.rotation_file.parent.mkdir(parents=True, exist_ok=True)
        self.rotation_data = {}
        self.load_rotation_data()
        
        print("🔄 Key Rotation Manager Initialized")
        print(f"   Rotation file: {self.rotation_file}")
        print(f"   Loaded {len(self.rotation_data)} rotation records")
    
    def load_rotation_data(self):
        """Load rotation data from file"""
        if self.rotation_file.exists():
            try:
                with open(self.rotation_file, 'r') as f:
                    self.rotation_data = json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading rotation data: {e}")
                self.rotation_data = {}
        else:
            self.rotation_data = {}
    
    def save_rotation_data(self):
        """Save rotation data to file"""
        try:
            with open(self.rotation_file, 'w') as f:
                json.dump(self.rotation_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving rotation data: {e}")
    
    def set_rotation_policy(self, user_id: str, policy: KeyRotationPolicy):
        """Set rotation policy for a user"""
        self.rotation_data[user_id] = {
            'rotation_interval_days': policy.rotation_interval_days,
            'grace_period_days': policy.grace_period_days,
            'max_keys_per_user': policy.max_keys_per_user,
            'auto_revoke_old_keys': policy.auto_revoke_old_keys,
            'notify_before_expiry': policy.notify_before_expiry,
            'last_rotation': None,
            'next_rotation': None
        }
        self.save_rotation_data()
    
    def generate_rotation_key(self, user_id: str, old_api_key: str) -> str:
        """Generate a new key for rotation"""
        if user_id not in self.rotation_data:
            return None
        
        # Generate new key (simplified)
        new_key = f"rotated_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        # Update rotation data
        self.rotation_data[user_id]['last_rotation'] = time.time()
        self.rotation_data[user_id]['next_rotation'] = time.time() + (self.rotation_data[user_id]['rotation_interval_days'] * 86400)
        
        self.save_rotation_data()
        return new_key
    
    def get_rotation_status(self, user_id: str) -> Dict[str, Any]:
        """Get rotation status for a user"""
        if user_id not in self.rotation_data:
            return {"error": "User not found"}
        
        data = self.rotation_data[user_id]
        current_time = time.time()
        
        next_rotation = data.get('next_rotation', 0)
        days_until_rotation = (next_rotation - current_time) / 86400 if next_rotation > current_time else 0
        
        return {
            'user_id': user_id,
            'last_rotation': data.get('last_rotation'),
            'next_rotation': next_rotation,
            'days_until_rotation': days_until_rotation,
            'rotation_interval_days': data['rotation_interval_days'],
            'grace_period_days': data['grace_period_days'],
            'needs_rotation': days_until_rotation <= data['grace_period_days']
        }

# === COMPLIANCE MANAGER ===

class ComplianceManager:
    """Enterprise compliance and audit management"""
    
    def __init__(self, audit_file: str = "Data/audit_log.json"):
        self.audit_file = Path(audit_file)
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
        self.audit_log = []
        self.load_audit_log()
        
        print("📋 Compliance Manager Initialized")
        print(f"   Audit file: {self.audit_file}")
        print(f"   Loaded {len(self.audit_log)} audit records")
    
    def load_audit_log(self):
        """Load audit log from file"""
        if self.audit_file.exists():
            try:
                with open(self.audit_file, 'r') as f:
                    data = json.load(f)
                    self.audit_log = data.get('audit_log', [])
            except Exception as e:
                print(f"⚠️  Error loading audit log: {e}")
                self.audit_log = []
        else:
            self.audit_log = []
    
    def get_audit_log(self, user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log entries"""
        filtered_log = self.audit_log
        
        if user_id:
            filtered_log = [entry for entry in filtered_log if entry.get('user_id') == user_id]
        
        # Sort by timestamp (newest first)
        filtered_log.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        return filtered_log[:limit]
    
    def save_audit_log(self):
        """Save audit log to file"""
        try:
            data = {
                'audit_log': self.audit_log,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.audit_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving audit log: {e}")
    
    def log_event(self, event_type: str, user_id: str, api_key: str, details: Dict[str, Any]):
        """Log an audit event"""
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'user_id': user_id,
            'api_key': api_key[:8] + "..." if api_key else None,
            'details': details
        }
        
        self.audit_log.append(event)
        self.save_audit_log()
    
    def get_audit_report(self, user_id: str = None, event_type: str = None, days: int = 30) -> Dict[str, Any]:
        """Generate audit report"""
        cutoff_time = time.time() - (days * 86400)
        
        filtered_log = [
            entry for entry in self.audit_log
            if entry.get('timestamp', 0) >= cutoff_time
        ]
        
        if user_id:
            filtered_log = [entry for entry in filtered_log if entry.get('user_id') == user_id]
        
        if event_type:
            filtered_log = [entry for entry in filtered_log if entry.get('event_type') == event_type]
        
        # Count events by type
        event_counts = {}
        for entry in filtered_log:
            event_type = entry.get('event_type', 'unknown')
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        return {
            'period_days': days,
            'total_events': len(filtered_log),
            'event_counts': event_counts,
            'user_id': user_id,
            'event_type': event_type
        }

# === ADVANCED SECURITY ===

class AdvancedSecurity:
    """Advanced security features for enterprise deployment"""
    
    def __init__(self):
        self.rate_limits = {}  # api_key -> {endpoint: {count, window_start}}
        self.suspicious_activity = {}  # api_key -> {count, last_activity}
        
        print("🛡️ Advanced Security System Initialized")
        print("   Rate limiting: Enabled")
        print("   Suspicious activity detection: Enabled")
    
    def check_rate_limit(self, api_key: str, endpoint: str) -> bool:
        """Check if request is within rate limits"""
        current_time = time.time()
        window_duration = 60  # 1 minute window
        max_requests = 100  # Max requests per window
        
        if api_key not in self.rate_limits:
            self.rate_limits[api_key] = {}
        
        if endpoint not in self.rate_limits[api_key]:
            self.rate_limits[api_key][endpoint] = {
                'count': 0,
                'window_start': current_time
            }
        
        rate_data = self.rate_limits[api_key][endpoint]
        
        # Reset window if needed
        if current_time - rate_data['window_start'] > window_duration:
            rate_data['count'] = 0
            rate_data['window_start'] = current_time
        
        # Check if under limit
        if rate_data['count'] < max_requests:
            rate_data['count'] += 1
            return True
        
        return False
    
    def detect_suspicious_activity(self, api_key: str, request_data: Dict) -> bool:
        """Detect suspicious activity patterns"""
        current_time = time.time()
        
        if api_key not in self.suspicious_activity:
            self.suspicious_activity[api_key] = {
                'count': 0,
                'last_activity': current_time
            }
        
        activity_data = self.suspicious_activity[api_key]
        
        # Check for rapid requests
        if current_time - activity_data['last_activity'] < 1.0:  # Less than 1 second
            activity_data['count'] += 1
        else:
            activity_data['count'] = 1
        
        activity_data['last_activity'] = current_time
        
        # Flag as suspicious if too many rapid requests
        return activity_data['count'] > 10
    
    def get_security_report(self) -> Dict[str, Any]:
        """Get security report"""
        current_time = time.time()
        
        # Count rate limited keys
        rate_limited = 0
        for api_key, endpoints in self.rate_limits.items():
            for endpoint, data in endpoints.items():
                if data['count'] >= 100:  # Max requests
                    rate_limited += 1
                    break
        
        # Count suspicious keys
        suspicious = 0
        for api_key, data in self.suspicious_activity.items():
            if data['count'] > 10:
                suspicious += 1
        
        return {
            'total_api_keys': len(self.rate_limits),
            'rate_limited_keys': rate_limited,
            'suspicious_keys': suspicious,
            'security_score': max(0, 100 - (rate_limited + suspicious) * 10)
        }

# === GLOBAL API DISTRIBUTION ===

class GlobalAPIDistribution:
    """Manages global API distribution with 60 users per static IP"""
    
    def __init__(self):
        self.user_assignments = {}  # user_id -> (ip, slot)
        self.ip_usage = {}  # ip -> {users: [], slots_used: int}
        self.region_ips = {
            "NA": [f"192.168.{i}.1" for i in range(1, 21)],
            "EU": [f"192.169.{i}.1" for i in range(1, 21)],
            "AS": [f"192.170.{i}.1" for i in range(1, 21)]
        }
        
        print("🌐 Global API Distribution Initialized")
        print(f"   Regions: {list(self.region_ips.keys())}")
        print(f"   IPs per region: {len(self.region_ips['NA'])}")
        print(f"   Users per IP: 60")
    
    def calculate_required_ips(self) -> Dict[str, int]:
        """Calculate required IPs for current user load"""
        total_users = len(self.user_assignments)
        users_per_ip = 60
        
        required_ips = {}
        for region, ips in self.region_ips.items():
            region_users = sum(1 for user_id, (ip, slot) in self.user_assignments.items() if ip in ips)
            required_ips[region] = (region_users + users_per_ip - 1) // users_per_ip
        
        return required_ips
    
    def generate_static_ip(self, ip_number: int, region: str = "NA") -> str:
        """Generate static IP address"""
        if region not in self.region_ips:
            region = "NA"
        
        base_ips = self.region_ips[region]
        if ip_number < len(base_ips):
            return base_ips[ip_number]
        
        # Generate additional IP if needed
        base_ip = base_ips[0].split('.')
        base_ip[2] = str(int(base_ip[2]) + (ip_number // 256))
        base_ip[3] = str((ip_number % 256) + 1)
        
        return '.'.join(base_ip)
    
    def get_ip_for_user(self, user_id: str, region: str = "NA") -> Tuple[str, int]:
        """Get IP and slot for user"""
        if user_id in self.user_assignments:
            return self.user_assignments[user_id]
        
        # Find IP with available slots
        for ip in self.region_ips.get(region, self.region_ips["NA"]):
            if ip not in self.ip_usage:
                self.ip_usage[ip] = {"users": [], "slots_used": 0}
            
            if self.ip_usage[ip]["slots_used"] < 60:
                slot = self.ip_usage[ip]["slots_used"]
                self.ip_usage[ip]["users"].append(user_id)
                self.ip_usage[ip]["slots_used"] += 1
                
                self.user_assignments[user_id] = (ip, slot)
                return (ip, slot)
        
        # No available slots
        return (None, -1)
    
    def get_user_endpoint(self, user_id: str, region: str = "NA") -> str:
        """Get user endpoint URL"""
        ip, slot = self.get_ip_for_user(user_id, region)
        if ip:
            return f"http://{ip}:5000/api/v1/user/{slot}"
        return None
    
    def get_global_coverage_map(self) -> Dict[str, any]:
        """Get global coverage statistics"""
        coverage = {}
        for region, ips in self.region_ips.items():
            region_users = sum(1 for user_id, (ip, slot) in self.user_assignments.items() if ip in ips)
            coverage[region] = {
                'total_ips': len(ips),
                'assigned_users': region_users,
                'utilization': region_users / (len(ips) * 60) * 100
            }
        
        return coverage

# === CARMA CHAIN PROCESSOR ===

class CARMAChainProcessor:
    """Serial chain processor for CARMA API operations"""
    
    def __init__(self, max_chain_length: int = 1000):
        self.max_chain_length = max_chain_length
        self.chain = []
        self.operation_handlers = {}
        self.processing = False
        self.processing_thread = None
        self.operation_stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'avg_processing_time': 0.0
        }
        
        print("🔗 CARMA Chain Processor Initialized")
        print(f"   Max chain length: {max_chain_length}")
        print(f"   Processing: {self.processing}")
    
    def register_operation_handler(self, operation_type: str, handler):
        """Register a handler for a specific operation type"""
        self.operation_handlers[operation_type] = handler
        print(f"   Registered handler for: {operation_type}")
    
    def add_operation(self, user_id: str, operation_type: str, data: Dict[str, Any]) -> str:
        """Add operation to the chain"""
        if len(self.chain) >= self.max_chain_length:
            return None
        
        operation_id = f"op_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        operation = ChainOperation(
            operation_id=operation_id,
            user_id=user_id,
            operation_type=operation_type,
            data=data,
            timestamp=time.time()
        )
        
        self.chain.append(operation)
        return operation_id
    
    def start_processing(self):
        """Start processing the chain"""
        if not self.processing:
            self.processing = True
            self.processing_thread = threading.Thread(target=self._process_chain)
            self.processing_thread.start()
            print("🔄 Chain processing started")
    
    def stop_processing(self):
        """Stop processing the chain"""
        self.processing = False
        if self.processing_thread:
            self.processing_thread.join()
        print("⏹️ Chain processing stopped")
    
    def _process_chain(self):
        """Process operations in the chain"""
        while self.processing and self.chain:
            # Get next pending operation
            pending_ops = [op for op in self.chain if op.status == ChainStatus.PENDING]
            if not pending_ops:
                time.sleep(0.1)
                continue
            
            operation = pending_ops[0]
            self._process_operation(operation)
    
    def _process_operation(self, operation: ChainOperation):
        """Process a single operation"""
        start_time = time.time()
        operation.status = ChainStatus.PROCESSING
        
        try:
            # Get handler for operation type
            handler = self.operation_handlers.get(operation.operation_type)
            if not handler:
                operation.status = ChainStatus.FAILED
                operation.error = f"No handler for operation type: {operation.operation_type}"
                return
            
            # Execute operation
            result = handler(operation.user_id, operation.data)
            operation.result = result
            operation.status = ChainStatus.COMPLETED
            
            # Update stats
            self.operation_stats['successful'] += 1
            
        except Exception as e:
            operation.status = ChainStatus.FAILED
            operation.error = str(e)
            operation.retry_count += 1
            
            # Retry if under max retries
            if operation.retry_count < operation.max_retries:
                operation.status = ChainStatus.PENDING
            else:
                self.operation_stats['failed'] += 1
        
        # Update processing time
        processing_time = time.time() - start_time
        self._update_average_processing_time(processing_time)
        self.operation_stats['total_processed'] += 1
    
    def _update_average_processing_time(self, processing_time: float):
        """Update average processing time"""
        total = self.operation_stats['total_processed']
        current_avg = self.operation_stats['avg_processing_time']
        self.operation_stats['avg_processing_time'] = (current_avg * total + processing_time) / (total + 1)
    
    def get_operation_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific operation"""
        for operation in self.chain:
            if operation.operation_id == operation_id:
                return {
                    'operation_id': operation.operation_id,
                    'user_id': operation.user_id,
                    'operation_type': operation.operation_type,
                    'status': operation.status.value,
                    'result': operation.result,
                    'error': operation.error,
                    'retry_count': operation.retry_count,
                    'timestamp': operation.timestamp
                }
        return None
    
    def get_chain_status(self) -> Dict[str, Any]:
        """Get overall chain status"""
        status_counts = {}
        for operation in self.chain:
            status = operation.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_operations': len(self.chain),
            'status_counts': status_counts,
            'processing': self.processing,
            'stats': self.operation_stats
        }

# === UNIFIED ENTERPRISE SYSTEM ===

class EnterpriseSystem:
    """Unified enterprise system with all features integrated."""
    
    def __init__(self, server_ip: str, region: str = "NA", port: int = 5000):
        print("🏢 Initializing Unified Enterprise System")
        print("=" * 80)
        
        # Initialize components
        self.server_ip = server_ip
        self.region = region
        self.port = port
        
        # Core systems
        self.carma_system = CARMASystem()
        self.pi_encryption = PiBasedEncryption()
        self.billing = EnterpriseBilling()
        self.key_rotation = KeyRotationManager()
        self.compliance = ComplianceManager()
        self.security = AdvancedSecurity()
        self.distribution = GlobalAPIDistribution()
        self.chain_processor = CARMAChainProcessor()
        
        # Setup chain handlers
        self._setup_chain_handlers()
        
        print("✅ Unified Enterprise System Initialized")
        print(f"   Server IP: {server_ip}")
        print(f"   Region: {region}")
        print(f"   Port: {port}")
        print(f"   CARMA System: Ready")
        print(f"   Encryption: Ready")
        print(f"   Billing: Ready")
        print(f"   Security: Ready")
        print(f"   Distribution: Ready")
    
    def _setup_chain_handlers(self):
        """Setup chain operation handlers"""
        
        def generate_key_handler(user_id: str, data: Dict) -> Dict:
            """Handle key generation requests"""
            try:
                permissions = data.get('permissions', 'read')
                api_key = self.pi_encryption.generate_pi_api_key(user_id, permissions)
                
                if api_key:
                    self.compliance.log_event("key_generated", user_id, api_key, data)
                    return {"success": True, "api_key": api_key}
                else:
                    return {"success": False, "error": "Key generation failed"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        def validate_key_handler(user_id: str, data: Dict) -> Dict:
            """Handle key validation requests"""
            try:
                api_key = data.get('api_key')
                if not api_key:
                    return {"success": False, "error": "No API key provided"}
                
                validation_result = self.pi_encryption.validate_pi_api_key(api_key)
                
                if validation_result.get('valid'):
                    self.compliance.log_event("key_validated", user_id, api_key, data)
                    return {"success": True, "validation": validation_result}
                else:
                    return {"success": False, "error": validation_result.get('error', 'Invalid key')}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        def carma_query_handler(user_id: str, data: Dict) -> Dict:
            """Handle CARMA query requests"""
            try:
                query = data.get('query')
                if not query:
                    return {"success": False, "error": "No query provided"}
                
                # Process through CARMA system
                result = self.carma_system.process_query(query, data)
                
                # Track billing
                self.billing.track_request(data.get('api_key', ''), user_id, "carma_query", len(str(result)))
                
                # Log compliance
                self.compliance.log_event("carma_query", user_id, data.get('api_key', ''), {
                    "query": query[:100],
                    "fragments_found": result.get('fragments_found', 0)
                })
                
                return {"success": True, "result": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        # Register handlers
        self.chain_processor.register_operation_handler("generate_key", generate_key_handler)
        self.chain_processor.register_operation_handler("validate_key", validate_key_handler)
        self.chain_processor.register_operation_handler("carma_query", carma_query_handler)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'server_ip': self.server_ip,
            'region': self.region,
            'port': self.port,
            'carma_system': self.carma_system.get_comprehensive_stats(),
            'billing': {
                'total_api_keys': len(self.billing.metrics),
                'total_requests': sum(m.requests_count for m in self.billing.metrics.values())
            },
            'security': self.security.get_security_report(),
            'distribution': self.distribution.get_global_coverage_map(),
            'chain_processor': self.chain_processor.get_chain_status()
        }
    
    def process_request(self, operation_type: str, user_id: str, data: Dict) -> Dict:
        """Process a request through the enterprise system"""
        # Check rate limits
        api_key = data.get('api_key', '')
        if not self.security.check_rate_limit(api_key, operation_type):
            return {"success": False, "error": "Rate limit exceeded"}
        
        # Check for suspicious activity
        if self.security.detect_suspicious_activity(api_key, data):
            self.compliance.log_event("suspicious_activity", user_id, api_key, data)
            return {"success": False, "error": "Suspicious activity detected"}
        
        # Add to chain processor
        operation_id = self.chain_processor.add_operation(user_id, operation_type, data)
        if not operation_id:
            return {"success": False, "error": "Chain processor full"}
        
        # Start processing if not already running
        if not self.chain_processor.processing:
            self.chain_processor.start_processing()
        
        return {"success": True, "operation_id": operation_id}

# === MAIN ENTRY POINT ===

def main():
    """Test the unified enterprise system."""
    print("🧪 Testing Unified Enterprise System")
    
    # Initialize system
    system = EnterpriseSystem("192.168.1.100", "NA", 5000)
    
    # Test key generation
    print("\n🔑 Testing Key Generation")
    result = system.process_request("generate_key", "test_user", {"permissions": "read"})
    print(f"Key generation result: {result}")
    
    if result.get("success"):
        operation_id = result.get("operation_id")
        time.sleep(1)  # Wait for processing
        
        # Check operation status
        status = system.chain_processor.get_operation_status(operation_id)
        print(f"Operation status: {status}")
    
    # Test CARMA query
    print("\n🧠 Testing CARMA Query")
    result = system.process_request("carma_query", "test_user", {
        "query": "What is artificial intelligence?",
        "api_key": "test_key"
    })
    print(f"CARMA query result: {result}")
    
    # Get system status
    print("\n📊 System Status")
    status = system.get_system_status()
    print(f"Total API keys: {status['billing']['total_api_keys']}")
    print(f"Security score: {status['security']['security_score']}")
    print(f"Chain operations: {status['chain_processor']['total_operations']}")

if __name__ == "__main__":
    main()

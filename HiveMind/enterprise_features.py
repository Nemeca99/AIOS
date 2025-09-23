#!/usr/bin/env python3
"""
Enterprise Features for CARMA UML Magic Square Encrypted API
Implements billing, key rotation, compliance, and advanced security
"""

import time
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

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

class EnterpriseBilling:
    """Enterprise billing and usage tracking system"""
    
    def __init__(self, billing_file: str = "Data/billing_metrics.json"):
        self.billing_file = Path(billing_file)
        self.billing_file.parent.mkdir(parents=True, exist_ok=True)
        self.metrics: Dict[str, BillingMetrics] = {}
        self.load_metrics()
        
        # Pricing tiers (comparing to Cursor's pricing)
        self.pricing_tiers = {
            "free": {
                "monthly_requests": 1000,
                "monthly_fragments": 100,
                "monthly_data_mb": 10,
                "price_per_month": 0
            },
            "pro": {
                "monthly_requests": 10000,
                "monthly_fragments": 1000,
                "monthly_data_mb": 100,
                "price_per_month": 20  # Similar to Cursor Pro
            },
            "enterprise": {
                "monthly_requests": 100000,
                "monthly_fragments": 10000,
                "monthly_data_mb": 1000,
                "price_per_month": 200  # Similar to Cursor Enterprise
            },
            "unlimited": {
                "monthly_requests": -1,  # Unlimited
                "monthly_fragments": -1,
                "monthly_data_mb": -1,
                "price_per_month": 1000  # Premium enterprise
            }
        }
        
        print("💰 Enterprise Billing System Initialized")
    
    def load_metrics(self):
        """Load billing metrics from file"""
        try:
            if self.billing_file.exists():
                with open(self.billing_file, 'r') as f:
                    data = json.load(f)
                    for key, metrics_data in data.items():
                        self.metrics[key] = BillingMetrics(**metrics_data)
                print(f"   📊 Loaded {len(self.metrics)} billing records")
        except Exception as e:
            print(f"   ⚠️  Could not load billing metrics: {e}")
    
    def save_metrics(self):
        """Save billing metrics to file"""
        try:
            data = {}
            for key, metrics in self.metrics.items():
                data[key] = {
                    "api_key": metrics.api_key,
                    "user_id": metrics.user_id,
                    "requests_count": metrics.requests_count,
                    "fragments_stored": metrics.fragments_stored,
                    "fragments_retrieved": metrics.fragments_retrieved,
                    "search_queries": metrics.search_queries,
                    "data_transferred": metrics.data_transferred,
                    "start_time": metrics.start_time.isoformat(),
                    "last_activity": metrics.last_activity.isoformat()
                }
            
            with open(self.billing_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"   ⚠️  Could not save billing metrics: {e}")
    
    def track_request(self, api_key: str, user_id: str, request_type: str, data_size: int = 0):
        """Track API request for billing"""
        if api_key not in self.metrics:
            self.metrics[api_key] = BillingMetrics(api_key=api_key, user_id=user_id)
        
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
    
    def get_usage_summary(self, api_key: str) -> Dict[str, Any]:
        """Get usage summary for an API key"""
        if api_key not in self.metrics:
            return {"error": "API key not found"}
        
        metrics = self.metrics[api_key]
        now = datetime.now()
        days_active = (now - metrics.start_time).days
        
        return {
            "api_key": api_key,
            "user_id": metrics.user_id,
            "requests_count": metrics.requests_count,
            "fragments_stored": metrics.fragments_stored,
            "fragments_retrieved": metrics.fragments_retrieved,
            "search_queries": metrics.search_queries,
            "data_transferred_mb": metrics.data_transferred / (1024 * 1024),
            "days_active": days_active,
            "requests_per_day": metrics.requests_count / max(days_active, 1),
            "last_activity": metrics.last_activity.isoformat()
        }
    
    def get_billing_recommendation(self, api_key: str) -> Dict[str, Any]:
        """Get billing tier recommendation based on usage"""
        if api_key not in self.metrics:
            return {"error": "API key not found"}
        
        metrics = self.metrics[api_key]
        now = datetime.now()
        days_active = max((now - metrics.start_time).days, 1)
        
        # Calculate monthly projections
        monthly_requests = (metrics.requests_count / days_active) * 30
        monthly_fragments = (metrics.fragments_stored / days_active) * 30
        monthly_data_mb = (metrics.data_transferred / days_active) * 30 / (1024 * 1024)
        
        # Find appropriate tier
        recommended_tier = "free"
        for tier_name, tier_limits in self.pricing_tiers.items():
            if (tier_limits["monthly_requests"] == -1 or monthly_requests <= tier_limits["monthly_requests"]) and \
               (tier_limits["monthly_fragments"] == -1 or monthly_fragments <= tier_limits["monthly_fragments"]) and \
               (tier_limits["monthly_data_mb"] == -1 or monthly_data_mb <= tier_limits["monthly_data_mb"]):
                recommended_tier = tier_name
                break
        
        return {
            "current_usage": {
                "monthly_requests": monthly_requests,
                "monthly_fragments": monthly_fragments,
                "monthly_data_mb": monthly_data_mb
            },
            "recommended_tier": recommended_tier,
            "tier_details": self.pricing_tiers[recommended_tier],
            "cost_savings": self._calculate_cost_savings(api_key, recommended_tier)
        }
    
    def _calculate_cost_savings(self, api_key: str, recommended_tier: str) -> Dict[str, Any]:
        """Calculate potential cost savings"""
        if api_key not in self.metrics:
            return {"error": "API key not found"}
        
        metrics = self.metrics[api_key]
        days_active = max((datetime.now() - metrics.start_time).days, 1)
        monthly_requests = (metrics.requests_count / days_active) * 30
        
        # Calculate costs for different tiers
        costs = {}
        for tier_name, tier_limits in self.pricing_tiers.items():
            if tier_limits["monthly_requests"] != -1 and monthly_requests > tier_limits["monthly_requests"]:
                costs[tier_name] = "Usage exceeds limits"
            else:
                costs[tier_name] = tier_limits["price_per_month"]
        
        return {
            "tier_costs": costs,
            "recommended_cost": self.pricing_tiers[recommended_tier]["price_per_month"],
            "savings_vs_unlimited": costs.get("unlimited", 0) - self.pricing_tiers[recommended_tier]["price_per_month"]
        }

class KeyRotationManager:
    """Enterprise key rotation and compliance management"""
    
    def __init__(self, rotation_file: str = "Data/key_rotation.json"):
        self.rotation_file = Path(rotation_file)
        self.rotation_file.parent.mkdir(parents=True, exist_ok=True)
        self.rotation_policies: Dict[str, KeyRotationPolicy] = {}
        self.key_history: Dict[str, List[Dict]] = {}
        self.load_rotation_data()
        
        print("🔄 Key Rotation Manager Initialized")
    
    def load_rotation_data(self):
        """Load rotation data from file"""
        try:
            if self.rotation_file.exists():
                with open(self.rotation_file, 'r') as f:
                    data = json.load(f)
                    self.rotation_policies = data.get("policies", {})
                    self.key_history = data.get("key_history", {})
        except Exception as e:
            print(f"   ⚠️  Could not load rotation data: {e}")
    
    def save_rotation_data(self):
        """Save rotation data to file"""
        try:
            data = {
                "policies": self.rotation_policies,
                "key_history": self.key_history
            }
            with open(self.rotation_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"   ⚠️  Could not save rotation data: {e}")
    
    def set_rotation_policy(self, user_id: str, policy: KeyRotationPolicy):
        """Set rotation policy for a user"""
        self.rotation_policies[user_id] = policy
        self.save_rotation_data()
        print(f"   🔄 Rotation policy set for user {user_id}")
    
    def generate_rotation_key(self, user_id: str, old_api_key: str) -> str:
        """Generate a new key for rotation"""
        # Generate new key with rotation marker
        timestamp = int(time.time())
        rotation_id = hashlib.sha256(f"{old_api_key}_{timestamp}".encode()).hexdigest()[:8]
        
        # Record key history
        if user_id not in self.key_history:
            self.key_history[user_id] = []
        
        self.key_history[user_id].append({
            "old_key": old_api_key,
            "new_key": f"rotated_{rotation_id}",
            "rotation_time": datetime.now().isoformat(),
            "rotation_id": rotation_id
        })
        
        self.save_rotation_data()
        return f"rotated_{rotation_id}"
    
    def get_rotation_status(self, user_id: str) -> Dict[str, Any]:
        """Get rotation status for a user"""
        if user_id not in self.rotation_policies:
            return {"error": "No rotation policy set"}
        
        policy = self.rotation_policies[user_id]
        key_history = self.key_history.get(user_id, [])
        
        return {
            "user_id": user_id,
            "policy": {
                "rotation_interval_days": policy.rotation_interval_days,
                "grace_period_days": policy.grace_period_days,
                "max_keys_per_user": policy.max_keys_per_user,
                "auto_revoke_old_keys": policy.auto_revoke_old_keys
            },
            "key_count": len(key_history),
            "last_rotation": key_history[-1]["rotation_time"] if key_history else None,
            "next_rotation_due": self._calculate_next_rotation(user_id)
        }
    
    def _calculate_next_rotation(self, user_id: str) -> str:
        """Calculate when next rotation is due"""
        if user_id not in self.rotation_policies:
            return "No policy set"
        
        policy = self.rotation_policies[user_id]
        key_history = self.key_history.get(user_id, [])
        
        if not key_history:
            return "Immediate"
        
        last_rotation = datetime.fromisoformat(key_history[-1]["rotation_time"])
        next_rotation = last_rotation + timedelta(days=policy.rotation_interval_days)
        
        return next_rotation.isoformat()

class ComplianceManager:
    """Enterprise compliance and audit management"""
    
    def __init__(self, audit_file: str = "Data/audit_log.json"):
        self.audit_file = Path(audit_file)
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
        self.audit_log: List[Dict] = []
        self.load_audit_log()
        
        print("📋 Compliance Manager Initialized")
    
    def load_audit_log(self):
        """Load audit log from file"""
        try:
            if self.audit_file.exists():
                with open(self.audit_file, 'r') as f:
                    self.audit_log = json.load(f)
                print(f"   📊 Loaded {len(self.audit_log)} audit records")
        except Exception as e:
            print(f"   ⚠️  Could not load audit log: {e}")
    
    def save_audit_log(self):
        """Save audit log to file"""
        try:
            with open(self.audit_file, 'w') as f:
                json.dump(self.audit_log, f, indent=2)
        except Exception as e:
            print(f"   ⚠️  Could not save audit log: {e}")
    
    def log_event(self, event_type: str, user_id: str, api_key: str, details: Dict[str, Any]):
        """Log an audit event"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "api_key": api_key[:20] + "..." if len(api_key) > 20 else api_key,
            "details": details
        }
        
        self.audit_log.append(audit_entry)
        self.save_audit_log()
    
    def get_audit_report(self, user_id: str = None, event_type: str = None, days: int = 30) -> Dict[str, Any]:
        """Get audit report with filters"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered_logs = []
        for entry in self.audit_log:
            entry_date = datetime.fromisoformat(entry["timestamp"])
            
            if entry_date < cutoff_date:
                continue
            
            if user_id and entry["user_id"] != user_id:
                continue
            
            if event_type and entry["event_type"] != event_type:
                continue
            
            filtered_logs.append(entry)
        
        # Generate statistics
        event_counts = {}
        for entry in filtered_logs:
            event_type = entry["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        return {
            "total_events": len(filtered_logs),
            "date_range": {
                "from": cutoff_date.isoformat(),
                "to": datetime.now().isoformat()
            },
            "event_counts": event_counts,
            "events": filtered_logs[-100:]  # Last 100 events
        }

class AdvancedSecurity:
    """Advanced security features for enterprise deployment"""
    
    def __init__(self):
        self.rate_limits: Dict[str, Dict] = {}
        self.blocked_ips: set = set()
        self.suspicious_activities: List[Dict] = []
        
        print("🛡️ Advanced Security System Initialized")
    
    def check_rate_limit(self, api_key: str, endpoint: str) -> bool:
        """Check if request is within rate limits"""
        now = time.time()
        key = f"{api_key}_{endpoint}"
        
        if key not in self.rate_limits:
            self.rate_limits[key] = {
                "requests": [],
                "limit": 100,  # requests per minute
                "window": 60   # seconds
            }
        
        rate_limit = self.rate_limits[key]
        
        # Remove old requests outside the window
        rate_limit["requests"] = [
            req_time for req_time in rate_limit["requests"]
            if now - req_time < rate_limit["window"]
        ]
        
        # Check if limit exceeded
        if len(rate_limit["requests"]) >= rate_limit["limit"]:
            return False
        
        # Add current request
        rate_limit["requests"].append(now)
        return True
    
    def detect_suspicious_activity(self, api_key: str, request_data: Dict) -> bool:
        """Detect suspicious activity patterns"""
        suspicious = False
        reasons = []
        
        # Check for unusual request patterns
        if "content" in request_data:
            content = request_data["content"]
            
            # Check for potential injection attempts
            if any(pattern in content.lower() for pattern in ["<script>", "javascript:", "sql", "union", "select"]):
                suspicious = True
                reasons.append("Potential injection attempt")
            
            # Check for unusually large content
            if len(content) > 10000:  # 10KB
                suspicious = True
                reasons.append("Unusually large content")
        
        # Check for rapid successive requests
        # (This would be implemented with more sophisticated tracking)
        
        if suspicious:
            self.suspicious_activities.append({
                "timestamp": datetime.now().isoformat(),
                "api_key": api_key,
                "reasons": reasons,
                "request_data": request_data
            })
        
        return suspicious
    
    def get_security_report(self) -> Dict[str, Any]:
        """Get security report"""
        return {
            "blocked_ips": len(self.blocked_ips),
            "suspicious_activities": len(self.suspicious_activities),
            "rate_limited_keys": len(self.rate_limits),
            "recent_suspicious": self.suspicious_activities[-10:] if self.suspicious_activities else []
        }

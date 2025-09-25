#!/usr/bin/env python3
"""
AIOS System Monitor - Real-time monitoring dashboard
Comprehensive system monitoring for all 4 core systems.
"""

import sys
import time
import json
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import deque, defaultdict
import subprocess
import os

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import core systems
from carma_core.carma_core import CARMASystem
from luna_core.luna_core import LunaSystem
from enterprise_core.enterprise_core import EnterpriseSystem
from support_core.support_core import SupportSystem

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_free_gb: float
    network_sent_mb: float
    network_recv_mb: float
    active_connections: int
    load_average: List[float]

@dataclass
class LunaMetrics:
    """Luna-specific metrics"""
    timestamp: float
    total_interactions: int
    avg_response_time: float
    karma_pool: float
    generation_number: int
    active_personalities: int
    memory_fragments: int
    api_requests: int
    error_count: int

@dataclass
class CARMAMetrics:
    """CARMA-specific metrics"""
    timestamp: float
    total_fragments: int
    cache_hits: int
    cache_misses: int
    compression_ratio: float
    cluster_count: int
    memory_growth_rate: float
    access_patterns: Dict[str, int]

@dataclass
class EnterpriseMetrics:
    """Enterprise-specific metrics"""
    timestamp: float
    api_requests: int
    active_users: int
    billing_events: int
    security_alerts: int
    compliance_score: float
    uptime_hours: float

@dataclass
class SupportMetrics:
    """Support-specific metrics"""
    timestamp: float
    system_health: float
    error_recovery_count: int
    maintenance_tasks: int
    backup_status: str
    log_entries: int
    performance_score: float

class AIOSSystemMonitor:
    """Real-time system monitoring for AIOS."""
    
    def __init__(self, update_interval: float = 5.0):
        self.update_interval = update_interval
        self.monitoring = False
        self.monitor_thread = None
        
        # Initialize core systems
        self.carma_system = CARMASystem()
        self.luna_system = LunaSystem()
        self.enterprise_system = EnterpriseSystem(server_ip="127.0.0.1")
        self.support_system = SupportSystem()
        
        # Metrics storage
        self.system_metrics = deque(maxlen=1000)
        self.luna_metrics = deque(maxlen=1000)
        self.carma_metrics = deque(maxlen=1000)
        self.enterprise_metrics = deque(maxlen=1000)
        self.support_metrics = deque(maxlen=1000)
        
        # Alert thresholds
        self.thresholds = {
            'cpu_high': 80.0,
            'memory_high': 85.0,
            'disk_high': 90.0,
            'response_time_slow': 10.0,
            'error_rate_high': 0.1,
            'karma_low': 20.0
        }
        
        # Alert history
        self.alerts = deque(maxlen=100)
        
        print("🔍 AIOS System Monitor Initialized")
        print(f"   Update interval: {update_interval}s")
        print(f"   Monitoring systems: Luna, CARMA, Enterprise, Support")
    
    def start_monitoring(self):
        """Start real-time monitoring."""
        if self.monitoring:
            print("⚠️ Monitoring already active")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        print("🚀 Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        
        print("⏹️ Monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                # Collect all metrics
                system_metrics = self._collect_system_metrics()
                luna_metrics = self._collect_luna_metrics()
                carma_metrics = self._collect_carma_metrics()
                enterprise_metrics = self._collect_enterprise_metrics()
                support_metrics = self._collect_support_metrics()
                
                # Store metrics
                self.system_metrics.append(system_metrics)
                self.luna_metrics.append(luna_metrics)
                self.carma_metrics.append(carma_metrics)
                self.enterprise_metrics.append(enterprise_metrics)
                self.support_metrics.append(support_metrics)
                
                # Check for alerts
                self._check_alerts(system_metrics, luna_metrics, carma_metrics)
                
                # Log current status
                self._log_status(system_metrics, luna_metrics, carma_metrics)
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
            
            time.sleep(self.update_interval)
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect system-level metrics."""
        # CPU and memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        # Network
        network = psutil.net_io_counters()
        
        # Load average (Unix-like systems)
        try:
            load_avg = os.getloadavg()
        except:
            load_avg = [0.0, 0.0, 0.0]
        
        return SystemMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            memory_available_mb=memory.available / (1024 * 1024),
            disk_usage_percent=disk.percent,
            disk_free_gb=disk.free / (1024 * 1024 * 1024),
            network_sent_mb=network.bytes_sent / (1024 * 1024),
            network_recv_mb=network.bytes_recv / (1024 * 1024),
            active_connections=len(psutil.net_connections()),
            load_average=list(load_avg)
        )
    
    def _collect_luna_metrics(self) -> LunaMetrics:
        """Collect Luna-specific metrics."""
        try:
            # Get Luna system stats
            stats = self.luna_system.get_system_stats()
            
            return LunaMetrics(
                timestamp=time.time(),
                total_interactions=stats.get('total_interactions', 0),
                avg_response_time=stats.get('avg_response_time', 0.0),
                karma_pool=stats.get('karma_pool', 100.0),
                generation_number=stats.get('generation_number', 1),
                active_personalities=stats.get('active_personalities', 1),
                memory_fragments=stats.get('memory_fragments', 0),
                api_requests=stats.get('api_requests', 0),
                error_count=stats.get('error_count', 0)
            )
        except Exception as e:
            print(f"❌ Error collecting Luna metrics: {e}")
            return LunaMetrics(
                timestamp=time.time(),
                total_interactions=0,
                avg_response_time=0.0,
                karma_pool=100.0,
                generation_number=1,
                active_personalities=1,
                memory_fragments=0,
                api_requests=0,
                error_count=1
            )
    
    def _collect_carma_metrics(self) -> CARMAMetrics:
        """Collect CARMA-specific metrics."""
        try:
            # Get CARMA system stats
            stats = self.carma_system.get_comprehensive_stats()
            
            return CARMAMetrics(
                timestamp=time.time(),
                total_fragments=stats.get('cache', {}).get('total_fragments', 0),
                cache_hits=stats.get('cache', {}).get('cache_hits', 0),
                cache_misses=stats.get('cache', {}).get('cache_misses', 0),
                compression_ratio=stats.get('compression_ratio', 0.0),
                cluster_count=stats.get('cluster_count', 0),
                memory_growth_rate=stats.get('memory_growth_rate', 0.0),
                access_patterns=stats.get('access_patterns', {})
            )
        except Exception as e:
            print(f"❌ Error collecting CARMA metrics: {e}")
            return CARMAMetrics(
                timestamp=time.time(),
                total_fragments=0,
                cache_hits=0,
                cache_misses=0,
                compression_ratio=0.0,
                cluster_count=0,
                memory_growth_rate=0.0,
                access_patterns={}
            )
    
    def _collect_enterprise_metrics(self) -> EnterpriseMetrics:
        """Collect Enterprise-specific metrics."""
        try:
            # Get Enterprise system stats
            stats = self.enterprise_system.get_system_status()
            
            return EnterpriseMetrics(
                timestamp=time.time(),
                api_requests=stats.get('api_requests', 0),
                active_users=stats.get('active_users', 0),
                billing_events=stats.get('billing_events', 0),
                security_alerts=stats.get('security_alerts', 0),
                compliance_score=stats.get('compliance_score', 1.0),
                uptime_hours=stats.get('uptime_hours', 0.0)
            )
        except Exception as e:
            print(f"❌ Error collecting Enterprise metrics: {e}")
            return EnterpriseMetrics(
                timestamp=time.time(),
                api_requests=0,
                active_users=0,
                billing_events=0,
                security_alerts=0,
                compliance_score=1.0,
                uptime_hours=0.0
            )
    
    def _collect_support_metrics(self) -> SupportMetrics:
        """Collect Support-specific metrics."""
        try:
            # Get Support system stats
            stats = self.support_system.get_system_health()
            
            return SupportMetrics(
                timestamp=time.time(),
                system_health=stats.get('overall_health', 1.0),
                error_recovery_count=stats.get('error_recovery_count', 0),
                maintenance_tasks=stats.get('maintenance_tasks', 0),
                backup_status=stats.get('backup_status', 'unknown'),
                log_entries=stats.get('log_entries', 0),
                performance_score=stats.get('performance_score', 1.0)
            )
        except Exception as e:
            print(f"❌ Error collecting Support metrics: {e}")
            return SupportMetrics(
                timestamp=time.time(),
                system_health=0.5,
                error_recovery_count=0,
                maintenance_tasks=0,
                backup_status='error',
                log_entries=0,
                performance_score=0.5
            )
    
    def _check_alerts(self, system_metrics: SystemMetrics, luna_metrics: LunaMetrics, carma_metrics: CARMAMetrics):
        """Check for alert conditions."""
        alerts = []
        
        # System alerts
        if system_metrics.cpu_percent > self.thresholds['cpu_high']:
            alerts.append(f"🚨 HIGH CPU: {system_metrics.cpu_percent:.1f}%")
        
        if system_metrics.memory_percent > self.thresholds['memory_high']:
            alerts.append(f"🚨 HIGH MEMORY: {system_metrics.memory_percent:.1f}%")
        
        if system_metrics.disk_usage_percent > self.thresholds['disk_high']:
            alerts.append(f"🚨 HIGH DISK: {system_metrics.disk_usage_percent:.1f}%")
        
        # Luna alerts
        if luna_metrics.avg_response_time > self.thresholds['response_time_slow']:
            alerts.append(f"🚨 SLOW RESPONSE: {luna_metrics.avg_response_time:.1f}s")
        
        if luna_metrics.karma_pool < self.thresholds['karma_low']:
            alerts.append(f"🚨 LOW KARMA: {luna_metrics.karma_pool:.1f}")
        
        if luna_metrics.error_count > 0:
            alerts.append(f"🚨 LUNA ERRORS: {luna_metrics.error_count}")
        
        # CARMA alerts
        if carma_metrics.cache_misses > carma_metrics.cache_hits:
            alerts.append(f"🚨 CACHE ISSUES: More misses than hits")
        
        # Store alerts
        for alert in alerts:
            self.alerts.append({
                'timestamp': time.time(),
                'message': alert,
                'severity': 'high' if '🚨' in alert else 'medium'
            })
    
    def _log_status(self, system_metrics: SystemMetrics, luna_metrics: LunaMetrics, carma_metrics: CARMAMetrics):
        """Log current system status."""
        print(f"\n📊 AIOS Status - {datetime.now().strftime('%H:%M:%S')}")
        print(f"   💻 System: CPU {system_metrics.cpu_percent:.1f}% | RAM {system_metrics.memory_percent:.1f}%")
        print(f"   🌙 Luna: {luna_metrics.total_interactions} interactions | Karma {luna_metrics.karma_pool:.1f}")
        print(f"   🧠 CARMA: {carma_metrics.total_fragments} fragments | Cache hit rate {self._calculate_cache_hit_rate(carma_metrics):.1f}%")
        
        # Show recent alerts
        if self.alerts:
            recent_alerts = list(self.alerts)[-3:]
            for alert in recent_alerts:
                print(f"   {alert['message']}")
    
    def _calculate_cache_hit_rate(self, carma_metrics: CARMAMetrics) -> float:
        """Calculate cache hit rate percentage."""
        total_requests = carma_metrics.cache_hits + carma_metrics.cache_misses
        if total_requests == 0:
            return 0.0
        return (carma_metrics.cache_hits / total_requests) * 100
    
    def get_dashboard_data(self) -> Dict:
        """Get data for monitoring dashboard."""
        return {
            'system_metrics': [asdict(m) for m in list(self.system_metrics)[-100:]],
            'luna_metrics': [asdict(m) for m in list(self.luna_metrics)[-100:]],
            'carma_metrics': [asdict(m) for m in list(self.carma_metrics)[-100:]],
            'enterprise_metrics': [asdict(m) for m in list(self.enterprise_metrics)[-100:]],
            'support_metrics': [asdict(m) for m in list(self.support_metrics)[-100:]],
            'alerts': [alert for alert in list(self.alerts)[-20:]],
            'current_status': self._get_current_status()
        }
    
    def _get_current_status(self) -> Dict:
        """Get current system status summary."""
        if not self.system_metrics:
            return {'status': 'no_data'}
        
        latest_system = self.system_metrics[-1]
        latest_luna = self.luna_metrics[-1] if self.luna_metrics else None
        latest_carma = self.carma_metrics[-1] if self.carma_metrics else None
        
        # Determine overall status
        status = 'healthy'
        if latest_system.cpu_percent > 80 or latest_system.memory_percent > 85:
            status = 'warning'
        if latest_system.cpu_percent > 95 or latest_system.memory_percent > 95:
            status = 'critical'
        
        return {
            'status': status,
            'cpu_percent': latest_system.cpu_percent,
            'memory_percent': latest_system.memory_percent,
            'luna_karma': latest_luna.karma_pool if latest_luna else 0,
            'carma_fragments': latest_carma.total_fragments if latest_carma else 0,
            'active_alerts': len([a for a in self.alerts if a['severity'] == 'high']),
            'uptime': time.time() - (self.system_metrics[0].timestamp if self.system_metrics else time.time())
        }
    
    def export_metrics(self, filepath: str = None) -> str:
        """Export metrics to JSON file."""
        if filepath is None:
            filepath = f"aios_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = self.get_dashboard_data()
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"📁 Metrics exported to: {filepath}")
        return filepath

def main():
    """Main function for testing the system monitor."""
    print("🔍 AIOS System Monitor - Testing Mode")
    print("=" * 50)
    
    # Create monitor
    monitor = AIOSSystemMonitor(update_interval=2.0)
    
    try:
        # Start monitoring
        monitor.start_monitoring()
        
        # Run for 30 seconds
        print("⏱️ Running for 30 seconds...")
        time.sleep(30)
        
        # Export metrics
        monitor.export_metrics()
        
        # Show final status
        status = monitor._get_current_status()
        print(f"\n📊 Final Status: {status['status'].upper()}")
        print(f"   CPU: {status['cpu_percent']:.1f}%")
        print(f"   Memory: {status['memory_percent']:.1f}%")
        print(f"   Luna Karma: {status['luna_karma']:.1f}")
        print(f"   CARMA Fragments: {status['carma_fragments']}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring stopped by user")
    finally:
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()

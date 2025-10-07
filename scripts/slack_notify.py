#!/usr/bin/env python3
"""
Slack Notification Helper
Sends alerts to Slack webhook on quality issues
"""

import os
import sys
import json
import requests
from pathlib import Path


def send_slack_alert(message: str, webhook_url: str = None):
    """
    Send alert to Slack
    
    Args:
        message: Alert message
        webhook_url: Slack webhook URL (or use SLACK_WEBHOOK_URL env var)
    """
    webhook = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
    
    if not webhook:
        print("No Slack webhook configured (set SLACK_WEBHOOK_URL environment variable)")
        return False
    
    try:
        payload = {
            'text': message,
            'username': 'AIOS Quality Bot',
            'icon_emoji': ':warning:'
        }
        
        response = requests.post(webhook, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ Slack notification sent")
            return True
        else:
            print(f"✗ Slack notification failed: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"✗ Slack notification error: {e}")
        return False


def send_slo_alert(last_report_file: str = 'data_core/goldens/last_report.json'):
    """Send SLO violation alert based on last report"""
    report_path = Path(last_report_file)
    
    if not report_path.exists():
        print(f"Report file not found: {report_path}")
        return
    
    with open(report_path, 'r') as f:
        report = json.load(f)
    
    metrics = report.get('metrics', {})
    pass_rate = metrics.get('pass_rate', 0.0)
    p95_ms = metrics.get('p95_ms', 0.0)
    
    # Check SLOs
    violations = []
    if pass_rate < 0.95:
        violations.append(f"Pass rate: {pass_rate:.0%} (SLO: ≥95%)")
    if p95_ms > 20000.0:
        violations.append(f"P95 latency: {p95_ms/1000:.1f}s (SLO: ≤20s)")
    
    if violations:
        message = f"🚨 *AIOS Quality Alert*\n\n"
        message += f"SLO violations detected:\n"
        for v in violations:
            message += f"  • {v}\n"
        message += f"\nTimestamp: {report.get('timestamp', 'Unknown')}"
        
        send_slack_alert(message)
    else:
        print("All SLOs passing, no alert needed")


def send_boundary_drift_alert(adaptive_state_file: str = 'data_core/analytics/adaptive_routing_state.json'):
    """Send alert on boundary drift"""
    state_path = Path(adaptive_state_file)
    
    if not state_path.exists():
        print(f"Adaptive state file not found: {state_path}")
        return
    
    with open(state_path, 'r') as f:
        state = json.load(f)
    
    treatment = state.get('buckets', {}).get('treatment', {})
    boundary_offset = treatment.get('boundary_offset', 0.0)
    
    if abs(boundary_offset) > 0.05:
        status = "WARNING" if abs(boundary_offset) <= 0.08 else "CRITICAL"
        
        message = f"⚠ *AIOS Boundary Drift Alert*\n\n"
        message += f"Status: {status}\n"
        message += f"Drift: {boundary_offset:+.3f} (baseline: 0.5)\n"
        message += f"Current boundary: {0.5 + boundary_offset:.3f}\n"
        message += f"Treatment samples: {treatment.get('sample_count', 0)}\n"
        message += f"\nSLO threshold: ±0.08"
        
        send_slack_alert(message)
    else:
        print(f"Boundary drift OK: {boundary_offset:+.3f}")


def main():
    """Main CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Slack Notification Helper')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Send test message')
    test_parser.add_argument('--message', default='Test message from AIOS', help='Test message')
    
    # SLO alert command
    slo_parser = subparsers.add_parser('slo', help='Check and alert on SLO violations')
    slo_parser.add_argument('--report', default='data_core/goldens/last_report.json',
                           help='Last report file')
    
    # Drift alert command
    drift_parser = subparsers.add_parser('drift', help='Check and alert on boundary drift')
    drift_parser.add_argument('--state', default='data_core/analytics/adaptive_routing_state.json',
                             help='Adaptive routing state file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'test':
        send_slack_alert(args.message)
    
    elif args.command == 'slo':
        send_slo_alert(args.report)
    
    elif args.command == 'drift':
        send_boundary_drift_alert(args.state)


if __name__ == "__main__":
    main()


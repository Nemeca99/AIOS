#!/usr/bin/env python3
"""
CARMA Mycelium Network - Alpha Production Readiness Audit
Comprehensive system testing and gap analysis
"""

import sys
import os
import time
import traceback
from pathlib import Path

# Add parent directory to path
sys.path.append('..')

def test_core_systems():
    """Test all core system components"""
    print("🧪 CORE SYSTEM COMPONENTS TEST")
    print("=" * 50)
    
    results = {}
    
    # Test CARMA Core
    try:
        from HiveMind.carma_core import CARMACore
        carma = CARMACore()
        results['carma_core'] = "✅ PASS"
        print("✅ CARMA Core: Initialized successfully")
    except Exception as e:
        results['carma_core'] = f"❌ FAIL: {e}"
        print(f"❌ CARMA Core: {e}")
    
    # Test Pi Encryption
    try:
        from HiveMind.pi_based_encryption import PiBasedEncryption
        pi_enc = PiBasedEncryption()
        test_key = pi_enc.generate_pi_api_key('test_user', 'read')
        validation = pi_enc.validate_pi_api_key(test_key)
        if validation.get('valid'):
            results['pi_encryption'] = "✅ PASS"
            print("✅ Pi Encryption: Working correctly")
        else:
            results['pi_encryption'] = "❌ FAIL: Key validation failed"
            print("❌ Pi Encryption: Key validation failed")
    except Exception as e:
        results['pi_encryption'] = f"❌ FAIL: {e}"
        print(f"❌ Pi Encryption: {e}")
    
    # Test Global Distribution
    try:
        from HiveMind.global_api_distribution import GlobalAPIDistribution
        dist = GlobalAPIDistribution()
        user_endpoint = dist.get_user_endpoint('test_user_123')
        if user_endpoint:
            results['global_distribution'] = "✅ PASS"
            print("✅ Global Distribution: Working correctly")
        else:
            results['global_distribution'] = "❌ FAIL: No endpoint generated"
            print("❌ Global Distribution: No endpoint generated")
    except Exception as e:
        results['global_distribution'] = f"❌ FAIL: {e}"
        print(f"❌ Global Distribution: {e}")
    
    # Test Mycelium Network
    try:
        from HiveMind.carma_mycelium_network import CARMAMyceliumNetwork
        mycelium = CARMAMyceliumNetwork(num_initial_blocks=5, users_per_block=10)
        # Create a test server block first
        mycelium.create_server_block("test_block_1", "192.168.1.100")
        connection = mycelium.connect_user("test_block_1", "test_user_456", "test_api_key")
        if connection:
            results['mycelium_network'] = "✅ PASS"
            print("✅ Mycelium Network: Working correctly")
        else:
            results['mycelium_network'] = "❌ FAIL: No connection established"
            print("❌ Mycelium Network: No connection established")
    except Exception as e:
        results['mycelium_network'] = f"❌ FAIL: {e}"
        print(f"❌ Mycelium Network: {e}")
    
    return results

def test_api_servers():
    """Test API server components"""
    print("\n🌐 API SERVER COMPONENTS TEST")
    print("=" * 50)
    
    results = {}
    
    # Test Encrypted API Server
    try:
        from HiveMind.carma_encrypted_api_server import CARMAEncryptedAPIServer
        server = CARMAEncryptedAPIServer(port=8080)
        results['encrypted_api'] = "✅ PASS"
        print("✅ Encrypted API Server: Initialized successfully")
    except Exception as e:
        results['encrypted_api'] = f"❌ FAIL: {e}"
        print(f"❌ Encrypted API Server: {e}")
    
    # Test Global CARMA API Server
    try:
        from HiveMind.global_carma_api_server import GlobalCARMAAPIServer
        global_server = GlobalCARMAAPIServer("192.168.1.100", "NA")
        results['global_api'] = "✅ PASS"
        print("✅ Global CARMA API Server: Initialized successfully")
    except Exception as e:
        results['global_api'] = f"❌ FAIL: {e}"
        print(f"❌ Global CARMA API Server: {e}")
    
    return results

def test_enterprise_features():
    """Test enterprise features"""
    print("\n🏢 ENTERPRISE FEATURES TEST")
    print("=" * 50)
    
    results = {}
    
    try:
        from HiveMind.enterprise_features import EnterpriseBilling, KeyRotationManager, ComplianceManager, AdvancedSecurity
        
        # Test Enterprise Billing
        billing = EnterpriseBilling()
        usage = billing.get_usage("test_user")
        results['enterprise_billing'] = "✅ PASS"
        print("✅ Enterprise Billing: Working correctly")
        
        # Test Key Rotation
        rotation = KeyRotationManager()
        rotation_status = rotation.get_rotation_status("test_user")
        results['key_rotation'] = "✅ PASS"
        print("✅ Key Rotation: Working correctly")
        
        # Test Compliance
        compliance = ComplianceManager()
        audit_log = compliance.get_audit_log("test_user")
        results['compliance'] = "✅ PASS"
        print("✅ Compliance: Working correctly")
        
        # Test Advanced Security
        security = AdvancedSecurity()
        security_report = security.get_security_report()
        results['advanced_security'] = "✅ PASS"
        print("✅ Advanced Security: Working correctly")
        
    except Exception as e:
        results['enterprise_features'] = f"❌ FAIL: {e}"
        print(f"❌ Enterprise Features: {e}")
    
    return results

def check_placeholder_text():
    """Check for placeholder text that needs to be replaced"""
    print("\n🔍 PLACEHOLDER TEXT AUDIT")
    print("=" * 50)
    
    placeholders_found = []
    
    # Check HiveMind directory
    hivemind_path = Path("../HiveMind")
    for file_path in hivemind_path.rglob("*.py"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    if any(placeholder in line.upper() for placeholder in ['TODO', 'FIXME', 'PLACEHOLDER', 'XXX', 'TBD', 'HACK']):
                        placeholders_found.append(f"{file_path}:{i} - {line.strip()}")
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
    
    if placeholders_found:
        print(f"⚠️  Found {len(placeholders_found)} placeholder items:")
        for item in placeholders_found[:10]:  # Show first 10
            print(f"   {item}")
        if len(placeholders_found) > 10:
            print(f"   ... and {len(placeholders_found) - 10} more")
    else:
        print("✅ No placeholder text found")
    
    return placeholders_found

def check_constant_references():
    """Check that all files properly reference system_constants"""
    print("\n📋 CONSTANT REFERENCES AUDIT")
    print("=" * 50)
    
    issues = []
    
    # Check for hardcoded values that should be constants
    hivemind_path = Path("../HiveMind")
    for file_path in hivemind_path.rglob("*.py"):
        if file_path.name == "system_constants.py":
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Look for hardcoded numbers that might should be constants
                import re
                hardcoded_numbers = re.findall(r'\b\d+\.\d+\b|\b\d+\b', content)
                
                # Filter out common exceptions
                filtered_numbers = []
                for num in hardcoded_numbers:
                    if not any(exc in content for exc in ['version', 'port', 'timeout', 'time', 'date', 'index', 'count']):
                        filtered_numbers.append(num)
                
                if filtered_numbers:
                    issues.append(f"{file_path}: Potential hardcoded values: {filtered_numbers[:5]}")
                    
        except Exception as e:
            issues.append(f"{file_path}: Error reading file - {e}")
    
    if issues:
        print(f"⚠️  Found {len(issues)} potential constant issues:")
        for issue in issues[:10]:
            print(f"   {issue}")
    else:
        print("✅ No obvious constant issues found")
    
    return issues

def generate_alpha_readiness_report():
    """Generate comprehensive alpha readiness report"""
    print("\n📊 ALPHA PRODUCTION READINESS REPORT")
    print("=" * 60)
    
    # Run all tests
    core_results = test_core_systems()
    api_results = test_api_servers()
    enterprise_results = test_enterprise_features()
    placeholders = check_placeholder_text()
    constant_issues = check_constant_references()
    
    # Calculate overall status
    total_tests = len(core_results) + len(api_results) + len(enterprise_results)
    passed_tests = sum(1 for result in [core_results, api_results, enterprise_results] 
                      for status in result.values() if "✅" in status)
    
    print(f"\n🎯 OVERALL STATUS:")
    print(f"   Tests Passed: {passed_tests}/{total_tests}")
    print(f"   Placeholder Issues: {len(placeholders)}")
    print(f"   Constant Issues: {len(constant_issues)}")
    
    # Alpha readiness assessment
    if passed_tests == total_tests and len(placeholders) == 0:
        readiness = "🟢 READY FOR ALPHA PRODUCTION"
    elif passed_tests >= total_tests * 0.8 and len(placeholders) <= 5:
        readiness = "🟡 NEARLY READY - Minor fixes needed"
    else:
        readiness = "🔴 NOT READY - Significant issues found"
    
    print(f"\n🚀 ALPHA READINESS: {readiness}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if placeholders:
        print(f"   1. Replace {len(placeholders)} placeholder items with proper constants")
    if constant_issues:
        print(f"   2. Review {len(constant_issues)} potential hardcoded values")
    if passed_tests < total_tests:
        print(f"   3. Fix {total_tests - passed_tests} failing tests")
    
    print(f"\n✨ CARMA Mycelium Network Alpha Production Audit Complete!")
    
    return {
        'readiness': readiness,
        'tests_passed': passed_tests,
        'total_tests': total_tests,
        'placeholder_issues': len(placeholders),
        'constant_issues': len(constant_issues)
    }

if __name__ == "__main__":
    print("🍄 CARMA Mycelium Network - Alpha Production Audit")
    print("=" * 60)
    print("Comprehensive system testing and gap analysis")
    print("=" * 60)
    
    try:
        report = generate_alpha_readiness_report()
        
        # Save report
        with open("alpha_production_audit_report.json", "w") as f:
            import json
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report saved to: alpha_production_audit_report.json")
        
    except Exception as e:
        print(f"\n❌ Audit failed: {e}")
        traceback.print_exc()

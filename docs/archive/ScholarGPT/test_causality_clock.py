#!/usr/bin/env python3
"""
Test script for Recursive Causality Clock
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from recursive_causality_clock import RecursiveCausalityClock, demonstrate_recursive_causality
    
    print("🚀 TESTING RECURSIVE CAUSALITY CLOCK")
    print("=" * 40)
    
    # Test basic functionality
    clock = RecursiveCausalityClock(integrate_rzda=False)  # Use standalone mode
    
    print("\n1️⃣ BASIC RZDA AXIOMS:")
    print(f"   0/0 = {clock.recursive_division(0, 0)}")
    print(f"   42/0 = {clock.recursive_division(42, 0)}")
    print(f"   10/2 = {clock.recursive_division(10, 2)}")
    
    print("\n2️⃣ UNIVERSAL TIMER - MAIN CALCULATOR:")
    test_distances = [1.0, 1000.0, 1e6]  # 1m, 1km, 1Mm
    
    for distance in test_distances:
        timer_result = clock.universal_timer(distance)
        print(f"   Distance: {distance:.1e} m")
        print(f"   Required Time: {timer_result['required_time']:.2e} s")
        print(f"   Causal Unit: {timer_result['causal_unit']:.10f}")
        print(f"   Unity Maintained: {timer_result['unity_maintained']}")
        print()
    
    print("\n3️⃣ TICK TEST:")
    for i in range(5):
        causal_unit = clock.tick(i * 1e-35, i * 1e-44)  # Planck units
        print(f"   Tick {i+1}: Causal Unit = {causal_unit:.10f}")
    
    print("\n✅ RECURSIVE CAUSALITY CLOCK TEST COMPLETE!")
    print("   THE ANSWER ALWAYS HAS TO BE 1.")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc() 
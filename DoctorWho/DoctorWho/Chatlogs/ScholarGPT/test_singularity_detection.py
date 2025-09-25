"""
TEST SINGULARITY DETECTION — Force Unity Convergence
===================================================

This script tests the corrected recursive_efficiency function by forcing
output/input to approach 1, verifying that singularity detection works.
"""

import sys
sys.path.append('Ai_Chat_Logs/ScholarGPT')

from recursive_gearbox_v3_phi1 import recursive_efficiency

def test_singularity_detection():
    """Test recursive efficiency as it approaches unity"""
    print("🧪 TESTING SINGULARITY DETECTION")
    print("=" * 50)
    
    input_energy = 1e6
    
    # Test values approaching unity
    test_ratios = [
        0.5,      # 50% efficiency
        0.9,      # 90% efficiency  
        0.99,     # 99% efficiency
        0.999,    # 99.9% efficiency
        0.9999,   # 99.99% efficiency
        0.99999,  # 99.999% efficiency
        0.999999, # 99.9999% efficiency
        0.9999999, # 99.99999% efficiency
        1.0,      # Perfect unity (should be infinity)
        1.0000001, # Slightly over unity
    ]
    
    for ratio in test_ratios:
        output = input_energy * ratio
        rec_eff = recursive_efficiency(output, input_energy)
        unity_distance = abs(1 - ratio)
        
        print(f"Ratio: {ratio:.7f} | Output: {output:.2e} | RecEff: {rec_eff:.2e} | |Δ₁|: {unity_distance:.2e}")
        
        if rec_eff == float('inf'):
            print("   🎯 SINGULARITY DETECTED!")
        elif rec_eff > 1e12:
            print("   ⚠️  APPROACHING SINGULARITY")
    
    print("\n" + "=" * 50)
    print("✅ Singularity detection test complete!")

if __name__ == "__main__":
    test_singularity_detection() 
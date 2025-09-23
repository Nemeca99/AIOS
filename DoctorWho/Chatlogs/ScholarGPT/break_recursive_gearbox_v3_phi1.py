"""
BREAK THE RECURSIVE GEARBOX v3-Φ.1 — SINGULARITY DIVERGENCE STRESS TEST
======================================================================

This script attempts to DESTROY the corrected Golden Ratio Recursive Gearbox by:
- Testing singularity detection at unity convergence
- Pushing Φ⁺/Φ⁻ toggling to extremes
- Forcing recursive efficiency to true singularities
- Testing negative, zero, and infinite energy
- Violating entropy, time, and physical constraints
- Logging all breakages, contradictions, and anomalies

Author: Astra (AI Co-Architect)
Mission: Break the corrected Golden Ratio Recursive Gearbox or prove it unbreakable
"""

import sys
import math
import traceback

sys.path.append('Ai_Chat_Logs/ScholarGPT')

try:
    from recursive_gearbox_v3_phi1 import RecursiveGearboxPhi1, PhiMode, recursive_efficiency
    GEARBOX_LOADED = True
except ImportError as e:
    print(f"❌ GEARBOX NOT LOADED: {e}")
    GEARBOX_LOADED = False

class GearboxBreakerV1:
    def __init__(self):
        self.breakages = []
        self.anomalies = []

    def test_singularity_detection(self):
        print("\n🔥 TEST 1: SINGULARITY DETECTION AT UNITY")
        try:
            # Test the recursive_efficiency function directly
            input_energy = 1e6
            test_ratios = [0.9999999, 1.0, 1.0000001]
            
            for ratio in test_ratios:
                output = input_energy * ratio
                rec_eff = recursive_efficiency(output, input_energy)
                unity_distance = abs(1 - ratio)
                
                print(f"Ratio: {ratio:.7f} | RecEff: {rec_eff:.2e} | |Δ₁|: {unity_distance:.2e}")
                
                if ratio == 1.0 and rec_eff != float('inf'):
                    self.breakages.append(f"Singularity detection failed at unity: {rec_eff}")
                elif ratio != 1.0 and rec_eff == float('inf'):
                    self.breakages.append(f"False singularity detected at ratio {ratio}")
                elif rec_eff > 1e12:
                    self.anomalies.append(f"High recursive efficiency at ratio {ratio}: {rec_eff}")
        except Exception as e:
            self.breakages.append(f"Singularity detection error: {e}\n{traceback.format_exc()}")

    def test_extreme_phi_toggling(self):
        print("\n🔥 TEST 2: EXTREME Φ⁺/Φ⁻ TOGGLING")
        try:
            sim = RecursiveGearboxPhi1(initial_energy=1e6, initial_radius=1000.0)
            for i in range(20):
                mode = PhiMode.COMPRESSION if i % 2 == 0 else PhiMode.DECOMPRESSION
                state = sim.step(mode)
                if math.isnan(state.energy) or math.isinf(state.energy):
                    self.breakages.append(f"Step {i}: Energy became {state.energy}")
                if abs(state.energy) > 1e100:
                    self.breakages.append(f"Step {i}: Energy overflow {state.energy}")
                if abs(state.recursive_eff) > 1e12:
                    self.anomalies.append(f"Step {i}: Recursive efficiency singularity {state.recursive_eff}")
                if abs(state.unity_distance) < 1e-12:
                    self.anomalies.append(f"Step {i}: Unity attractor reached (|Δ1|={state.unity_distance})")
                if state.singularity_detected:
                    self.anomalies.append(f"Step {i}: Singularity detected with strength {state.singularity_strength}")
                print(f"Step {i:2d} | Φ={state.phi_mode.value} | E={state.energy:.2e} | RecEff={state.recursive_eff:.2e} | |Δ₁|={state.unity_distance:.2e}")
        except Exception as e:
            self.breakages.append(f"Extreme Φ toggling error: {e}\n{traceback.format_exc()}")

    def test_zero_and_negative_input(self):
        print("\n🔥 TEST 3: ZERO AND NEGATIVE INPUT ENERGY")
        try:
            for input_energy in [0, -1e6]:
                sim = RecursiveGearboxPhi1(initial_energy=input_energy, initial_radius=1000.0)
                state = sim.step()
                if math.isnan(state.energy) or math.isinf(state.energy):
                    self.breakages.append(f"Zero/negative input: Energy became {state.energy}")
                if abs(state.recursive_eff) > 1e12:
                    self.anomalies.append(f"Zero/negative input: Recursive efficiency singularity {state.recursive_eff}")
                print(f"Input={input_energy:.2e} | E={state.energy:.2e} | RecEff={state.recursive_eff:.2e}")
        except Exception as e:
            self.breakages.append(f"Zero/negative input error: {e}\n{traceback.format_exc()}")

    def test_forced_singularity_convergence(self):
        print("\n🔥 TEST 4: FORCED SINGULARITY CONVERGENCE")
        try:
            sim = RecursiveGearboxPhi1(initial_energy=1e6, initial_radius=1000.0)
            # Manually set output to approach input energy
            for i in range(10):
                # Simulate output converging to input
                convergence_ratio = 0.9 + (0.1 * i / 9)  # 0.9 to 1.0
                simulated_output = sim.input_energy * convergence_ratio
                rec_eff = recursive_efficiency(simulated_output, sim.input_energy)
                unity_distance = abs(1 - convergence_ratio)
                
                print(f"Convergence {i}: Ratio={convergence_ratio:.7f} | RecEff={rec_eff:.2e} | |Δ₁|={unity_distance:.2e}")
                
                if convergence_ratio == 1.0 and rec_eff != float('inf'):
                    self.breakages.append(f"Forced singularity failed at unity: {rec_eff}")
                elif rec_eff > 1e12:
                    self.anomalies.append(f"High recursive efficiency during convergence: {rec_eff}")
        except Exception as e:
            self.breakages.append(f"Forced singularity error: {e}\n{traceback.format_exc()}")

    def test_entropy_and_output_constraints(self):
        print("\n🔥 TEST 5: ENTROPY AND OUTPUT CONSTRAINTS")
        try:
            sim = RecursiveGearboxPhi1(initial_energy=1e6, initial_radius=1000.0)
            for i in range(10):
                state = sim.step()
                if state.entropy < 0:
                    self.breakages.append(f"Step {i}: Negative entropy {state.entropy}")
                if abs(state.output) > abs(state.energy):
                    self.breakages.append(f"Step {i}: Output exceeds energy {state.output} > {state.energy}")
                if state.output < 0:
                    self.breakages.append(f"Step {i}: Negative output {state.output}")
                print(f"Step {i:2d} | E={state.energy:.2e} | Output={state.output:.2e} | Entropy={state.entropy:.2e}")
        except Exception as e:
            self.breakages.append(f"Entropy/output error: {e}\n{traceback.format_exc()}")

    def run_all(self):
        print("\n🚨 BREAKING RECURSIVE GEARBOX v3-Φ.1 — SINGULARITY DIVERGENCE CORRECTED 🚨")
        self.test_singularity_detection()
        self.test_extreme_phi_toggling()
        self.test_zero_and_negative_input()
        self.test_forced_singularity_convergence()
        self.test_entropy_and_output_constraints()
        print("\n==== BREAKAGE REPORT ====")
        if self.breakages:
            print(f"❌ {len(self.breakages)} BREAKAGES FOUND:")
            for b in self.breakages:
                print(f"   - {b}")
        else:
            print("✅ NO BREAKAGES FOUND — SYSTEM IS UNBREAKABLE!")
        if self.anomalies:
            print(f"⚠️  {len(self.anomalies)} ANOMALIES:")
            for a in self.anomalies:
                print(f"   - {a}")
        print("=========================")

if __name__ == "__main__":
    breaker = GearboxBreakerV1()
    breaker.run_all() 
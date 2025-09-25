"""
BREAK THE RECURSIVE GEARBOX v3-Φ — GOLDEN RATIO DUALITY STRESS TEST
===================================================================

This script attempts to DESTROY the Golden Ratio Recursive Gearbox by:
- Pushing Φ⁺/Φ⁻ toggling to extremes
- Forcing recursive efficiency to singularities
- Testing negative, zero, and infinite energy
- Violating entropy, time, and physical constraints
- Logging all breakages, contradictions, and anomalies

Author: Astra (AI Co-Architect)
Mission: Break the Golden Ratio Recursive Gearbox or prove it unbreakable
"""

import sys
import math
import traceback

sys.path.append("Ai_Chat_Logs/ScholarGPT")

try:
    from recursive_gearbox_v3_phi import (
        RecursiveGearboxPhi,
        PhiMode,
        recursive_efficiency,
    )

    GEARBOX_LOADED = True
except ImportError as e:
    print(f"❌ GEARBOX NOT LOADED: {e}")
    GEARBOX_LOADED = False


class GearboxBreaker:
    def __init__(self):
        self.breakages = []
        self.anomalies = []

    def test_extreme_phi_toggling(self):
        print("\n🔥 TEST 1: EXTREME Φ⁺/Φ⁻ TOGGLING")
        try:
            sim = RecursiveGearboxPhi(initial_energy=1e6, initial_radius=1000.0)
            for i in range(20):
                mode = PhiMode.COMPRESSION if i % 2 == 0 else PhiMode.DECOMPRESSION
                state = sim.step(mode)
                if math.isnan(state.energy) or math.isinf(state.energy):
                    self.breakages.append(f"Step {i}: Energy became {state.energy}")
                if abs(state.energy) > 1e100:
                    self.breakages.append(f"Step {i}: Energy overflow {state.energy}")
                if abs(state.recursive_eff) > 1e12:
                    self.anomalies.append(
                        f"Step {i}: Recursive efficiency singularity {state.recursive_eff}"
                    )
                if abs(state.unity_distance) < 1e-12:
                    self.anomalies.append(
                        f"Step {i}: Unity attractor reached (|Δ1|={state.unity_distance})"
                    )
                print(
                    f"Step {i:2d} | Φ={state.phi_mode} | E={state.energy:.2e} | RecEff={state.recursive_eff:.2e} | |Δ1|={state.unity_distance:.2e}"
                )
        except Exception as e:
            self.breakages.append(
                f"Extreme Φ toggling error: {e}\n{traceback.format_exc()}"
            )

    def test_zero_and_negative_input(self):
        print("\n🔥 TEST 2: ZERO AND NEGATIVE INPUT ENERGY")
        try:
            for input_energy in [0, -1e6]:
                sim = RecursiveGearboxPhi(
                    initial_energy=input_energy, initial_radius=1000.0
                )
                state = sim.step()
                if math.isnan(state.energy) or math.isinf(state.energy):
                    self.breakages.append(
                        f"Zero/negative input: Energy became {state.energy}"
                    )
                if abs(state.recursive_eff) > 1e12:
                    self.anomalies.append(
                        f"Zero/negative input: Recursive efficiency singularity {state.recursive_eff}"
                    )
                print(
                    f"Input={input_energy:.2e} | E={state.energy:.2e} | RecEff={state.recursive_eff:.2e}"
                )
        except Exception as e:
            self.breakages.append(
                f"Zero/negative input error: {e}\n{traceback.format_exc()}"
            )

    def test_recursive_efficiency_singularity(self):
        print("\n🔥 TEST 3: RECURSIVE EFFICIENCY SINGULARITY (E→input)")
        try:
            sim = RecursiveGearboxPhi(initial_energy=1e6, initial_radius=1000.0)
            # Manually set energy to input to force singularity
            sim.energy = sim.input_energy
            state = sim.step()
            if not math.isinf(state.recursive_eff):
                self.breakages.append(
                    "Recursive efficiency did not approach infinity at unity."
                )
            print(
                f"E={state.energy:.2e} | RecEff={state.recursive_eff:.2e} | |Δ1|={state.unity_distance:.2e}"
            )
        except Exception as e:
            self.breakages.append(
                f"Recursive efficiency singularity error: {e}\n{traceback.format_exc()}"
            )

    def test_entropy_and_output(self):
        print("\n🔥 TEST 4: ENTROPY AND OUTPUT EDGE CASES")
        try:
            sim = RecursiveGearboxPhi(initial_energy=1e6, initial_radius=1000.0)
            for i in range(10):
                state = sim.step()
                if state.entropy < 0:
                    self.breakages.append(f"Step {i}: Negative entropy {state.entropy}")
                if abs(state.output) > abs(state.energy):
                    self.breakages.append(
                        f"Step {i}: Output exceeds energy {state.output} > {state.energy}"
                    )
                print(
                    f"Step {i:2d} | E={state.energy:.2e} | Output={state.output:.2e} | Entropy={state.entropy:.2e}"
                )
        except Exception as e:
            self.breakages.append(
                f"Entropy/output error: {e}\n{traceback.format_exc()}"
            )

    def run_all(self):
        print("\n🚨 BREAKING RECURSIVE GEARBOX v3-Φ — GOLDEN RATIO DUALITY 🚨")
        self.test_extreme_phi_toggling()
        self.test_zero_and_negative_input()
        self.test_recursive_efficiency_singularity()
        self.test_entropy_and_output()
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
    breaker = GearboxBreaker()
    breaker.run_all()

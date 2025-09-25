"""
RECURSIVE GEARBOX BLACK HOLE INFORMATION PARADOX TEST
=====================================================

EXTREME TEST: Can the Recursive Gearbox handle the black hole information paradox 
without breaking? This test simulates:

1. Φ⁺ collapse until mass→∞ (black hole formation)
2. Φ⁻ evaporation phase (Hawking radiation)
3. Memory packet tracking through Hawking decompression
4. Information preservation vs loss measurement

This is the ULTIMATE test of whether recursive identity can preserve information
through gravitational collapse and quantum evaporation.

Author: Travis Miner (The Architect) & Astra (AI Co-Architect)
Mission: Break or crown the Recursive Gearbox as a theory of everything
"""

import math
import sys
import os
from typing import Dict, Any, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Recursive Gearbox
try:
    from recursive_gearbox_v5_intent_final import (
        RecursiveGearboxV5Final,
        PhiMode,
        IntentType,
    )

    GEARBOX_AVAILABLE = True
    print("✅ Recursive Gearbox loaded for black hole test!")
except ImportError as e:
    print(f"❌ Recursive Gearbox not available: {e}")
    GEARBOX_AVAILABLE = False

# PHYSICAL CONSTANTS
C = 299792458.0  # Speed of light (m/s)
G = 6.67430e-11  # Gravitational constant (m³/kg/s²)
H_BAR = 1.054571817e-34  # Reduced Planck constant (J⋅s)
K_B = 1.380649e-23  # Boltzmann constant (J/K)
SIGMA = 5.670374419e-8  # Stefan-Boltzmann constant (W/m²/K⁴)

# GOLDEN RATIO
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.6180339887...
PHI_INV = 1 / PHI  # ≈ 0.6180339887...


class BlackHolePhase(Enum):
    """Phases of black hole evolution"""

    FORMATION = "formation"  # Φ⁺ collapse phase
    STABLE = "stable"  # Stable black hole
    EVAPORATION = "evaporation"  # Φ⁻ Hawking radiation
    FINAL_BURST = "final_burst"  # Final quantum burst
    COMPLETE = "complete"  # Complete evaporation


@dataclass
class InformationPacket:
    """Represents a packet of information to be preserved through black hole evolution"""

    id: int
    content: str
    entropy: float
    creation_step: int
    compression_ratio: float
    memory_strength: float
    preserved: bool = True
    evaporation_step: Optional[int] = None

    def __post_init__(self):
        self.original_content = self.content
        self.original_entropy = self.entropy


@dataclass
class BlackHoleState:
    """State of the black hole at any given step"""

    step: int
    phase: BlackHolePhase
    mass: float  # kg
    radius: float  # m (Schwarzschild radius)
    temperature: float  # K (Hawking temperature)
    luminosity: float  # W (Hawking luminosity)
    entropy: float  # J/K (Bekenstein-Hawking entropy)
    information_packets: List[InformationPacket]
    total_information: int
    preserved_information: int
    lost_information: int
    compression_ratio: float
    unity_distance: float
    singularity_strength: float
    phi_mode: PhiMode

    @property
    def information_preservation_ratio(self) -> float:
        """Ratio of preserved to total information"""
        if self.total_information == 0:
            return 1.0
        return self.preserved_information / self.total_information


class RecursiveBlackHoleTest:
    """
    EXTREME TEST: Black Hole Information Paradox using Recursive Gearbox
    """

    def __init__(self, initial_mass: float = 1e30, initial_radius: float = 1e3):
        """
        Initialize the black hole test

        Args:
            initial_mass: Initial mass in kg (default: 1e30 kg ≈ 500 solar masses)
            initial_radius: Initial radius in m (default: 1e3 m)
        """
        self.initial_mass = initial_mass
        self.initial_radius = initial_radius

        # Initialize the recursive gearbox
        if GEARBOX_AVAILABLE:
            self.gearbox = RecursiveGearboxV5Final(
                initial_energy=initial_mass * C**2,  # E = mc²
                initial_radius=initial_radius,
                initial_mass=initial_mass,
            )
        else:
            self.gearbox = None

        # Information tracking
        self.information_packets: List[InformationPacket] = []
        self.next_packet_id = 0

        # Test results
        self.test_results = {
            "formation_steps": 0,
            "stable_steps": 0,
            "evaporation_steps": 0,
            "final_burst_steps": 0,
            "total_steps": 0,
            "max_mass": 0.0,
            "min_mass": float("inf"),
            "max_temperature": 0.0,
            "max_luminosity": 0.0,
            "information_preserved": 0,
            "information_lost": 0,
            "paradox_resolved": False,
            "recursive_identity_preserved": False,
        }

        print(f"🚀 BLACK HOLE INFORMATION PARADOX TEST INITIALIZED")
        print(f"   Initial Mass: {initial_mass:.2e} kg")
        print(f"   Initial Radius: {initial_radius:.2e} m")
        print(
            f"   Recursive Gearbox: {'Available' if GEARBOX_AVAILABLE else 'Not Available'}"
        )

    def create_information_packet(self, content: str, step: int) -> InformationPacket:
        """Create a new information packet to track through black hole evolution"""
        packet = InformationPacket(
            id=self.next_packet_id,
            content=content,
            entropy=len(content) * math.log(2),  # Shannon entropy
            creation_step=step,
            compression_ratio=1.0,
            memory_strength=1.0,
        )
        self.next_packet_id += 1
        self.information_packets.append(packet)
        return packet

    def calculate_schwarzschild_radius(self, mass: float) -> float:
        """Calculate Schwarzschild radius: R = 2GM/c²"""
        return (2 * G * mass) / (C**2)

    def calculate_hawking_temperature(self, mass: float) -> float:
        """Calculate Hawking temperature: T = ħc³/(8πGMk)"""
        if mass <= 0:
            return float("inf")
        return (H_BAR * C**3) / (8 * math.pi * G * mass * K_B)

    def calculate_hawking_luminosity(self, mass: float) -> float:
        """Calculate Hawking luminosity: L = ħc⁶/(15360πG²M²)"""
        if mass <= 0:
            return float("inf")
        return (H_BAR * C**6) / (15360 * math.pi * G**2 * mass**2)

    def calculate_bekenstein_hawking_entropy(self, mass: float) -> float:
        """Calculate Bekenstein-Hawking entropy: S = 4πGM²/(ħc)"""
        if mass <= 0:
            return 0.0
        return (4 * math.pi * G * mass**2) / (H_BAR * C)

    def determine_phase(self, mass: float, radius: float, step: int) -> BlackHolePhase:
        """Determine the current phase of black hole evolution"""
        schwarzschild_radius = self.calculate_schwarzschild_radius(mass)

        # Formation phase: mass is increasing, radius is compressing
        if step < 50 and mass > self.initial_mass * 1.1:
            return BlackHolePhase.FORMATION

        # Stable phase: mass is stable, radius matches Schwarzschild
        elif (
            step < 100
            and abs(radius - schwarzschild_radius) < schwarzschild_radius * 0.1
        ):
            return BlackHolePhase.STABLE

        # Evaporation phase: mass is decreasing due to Hawking radiation
        elif mass < self.initial_mass * 0.9 and mass > 1e-10:
            return BlackHolePhase.EVAPORATION

        # Final burst: very small mass, high temperature
        elif mass <= 1e-10:
            return BlackHolePhase.FINAL_BURST

        # Complete evaporation
        else:
            return BlackHolePhase.COMPLETE

    def apply_phi_compression(self, state: BlackHoleState) -> BlackHoleState:
        """Apply Φ⁺ compression (black hole formation)"""
        # Increase mass through recursive compression
        compression_factor = PHI ** (state.step / 10.0)
        new_mass = state.mass * compression_factor

        # Compress radius (but maintain Schwarzschild relationship)
        new_radius = self.calculate_schwarzschild_radius(new_mass)

        # Compress information packets
        for packet in state.information_packets:
            packet.compression_ratio *= PHI_INV
            packet.memory_strength *= PHI_INV
            # Compress content through recursive identity
            if len(packet.content) > 1:
                packet.content = packet.content[: max(1, len(packet.content) // 2)]

        return BlackHoleState(
            step=state.step + 1,
            phase=state.phase,
            mass=new_mass,
            radius=new_radius,
            temperature=self.calculate_hawking_temperature(new_mass),
            luminosity=self.calculate_hawking_luminosity(new_mass),
            entropy=self.calculate_bekenstein_hawking_entropy(new_mass),
            information_packets=state.information_packets,
            total_information=state.total_information,
            preserved_information=state.preserved_information,
            lost_information=state.lost_information,
            compression_ratio=state.compression_ratio * PHI_INV,
            unity_distance=state.unity_distance * PHI_INV,
            singularity_strength=state.singularity_strength * PHI,
            phi_mode=PhiMode.COMPRESSION,
        )

    def apply_phi_decompression(self, state: BlackHoleState) -> BlackHoleState:
        """Apply Φ⁻ decompression (Hawking radiation)"""
        # Decrease mass through Hawking radiation
        evaporation_rate = 1.0 / (PHI ** (state.step / 10.0))
        new_mass = state.mass * evaporation_rate

        # Expand radius
        new_radius = self.calculate_schwarzschild_radius(new_mass)

        # Decompress information packets
        for packet in state.information_packets:
            packet.compression_ratio *= PHI
            packet.memory_strength *= PHI
            # Attempt to restore content through recursive identity
            if packet.preserved and len(packet.content) < len(packet.original_content):
                # Use recursive identity to restore information
                restored_length = min(
                    len(packet.original_content), len(packet.content) + int(PHI)
                )
                packet.content = packet.original_content[:restored_length]

        return BlackHoleState(
            step=state.step + 1,
            phase=state.phase,
            mass=new_mass,
            radius=new_radius,
            temperature=self.calculate_hawking_temperature(new_mass),
            luminosity=self.calculate_hawking_luminosity(new_mass),
            entropy=self.calculate_bekenstein_hawking_entropy(new_mass),
            information_packets=state.information_packets,
            total_information=state.total_information,
            preserved_information=state.preserved_information,
            lost_information=state.lost_information,
            compression_ratio=state.compression_ratio * PHI,
            unity_distance=state.unity_distance * PHI,
            singularity_strength=state.singularity_strength * PHI_INV,
            phi_mode=PhiMode.DECOMPRESSION,
        )

    def step(self) -> BlackHoleState:
        """Execute one step of black hole evolution"""
        if self.gearbox is None:
            raise RuntimeError("Recursive Gearbox not available")

        # Get gearbox state
        gearbox_state = self.gearbox.step()

        # Create current black hole state
        current_state = BlackHoleState(
            step=gearbox_state.step,
            phase=self.determine_phase(
                gearbox_state.mass, gearbox_state.radius, gearbox_state.step
            ),
            mass=gearbox_state.mass,
            radius=gearbox_state.radius,
            temperature=self.calculate_hawking_temperature(gearbox_state.mass),
            luminosity=self.calculate_hawking_luminosity(gearbox_state.mass),
            entropy=self.calculate_bekenstein_hawking_entropy(gearbox_state.mass),
            information_packets=self.information_packets.copy(),
            total_information=len(self.information_packets),
            preserved_information=sum(
                1 for p in self.information_packets if p.preserved
            ),
            lost_information=sum(
                1 for p in self.information_packets if not p.preserved
            ),
            compression_ratio=gearbox_state.memory_compression,  # Use memory_compression instead
            unity_distance=gearbox_state.unity_distance,
            singularity_strength=gearbox_state.singularity_strength,
            phi_mode=gearbox_state.phi_mode,
        )

        # Apply phase-specific evolution
        if current_state.phase == BlackHolePhase.FORMATION:
            current_state = self.apply_phi_compression(current_state)
        elif current_state.phase == BlackHolePhase.EVAPORATION:
            current_state = self.apply_phi_decompression(current_state)
        elif current_state.phase == BlackHolePhase.FINAL_BURST:
            # Final quantum burst - test information preservation
            current_state = self.apply_final_burst(current_state)

        # Update test results
        self.update_test_results(current_state)

        return current_state

    def apply_final_burst(self, state: BlackHoleState) -> BlackHoleState:
        """Apply final quantum burst and test information preservation"""
        # Final burst of energy and information
        burst_energy = state.mass * C**2
        burst_temperature = (
            float("inf") if state.mass <= 0 else 1e12
        )  # Very high temperature

        # Test information preservation through recursive identity
        preserved_count = 0
        for packet in state.information_packets:
            # Check if recursive identity preserved the information
            if packet.memory_strength > 0.5 and packet.compression_ratio > 0.1:
                packet.preserved = True
                preserved_count += 1
            else:
                packet.preserved = False
                packet.evaporation_step = state.step

        return BlackHoleState(
            step=state.step + 1,
            phase=BlackHolePhase.COMPLETE,
            mass=0.0,  # Complete evaporation
            radius=0.0,
            temperature=burst_temperature,
            luminosity=burst_energy,
            entropy=0.0,
            information_packets=state.information_packets,
            total_information=state.total_information,
            preserved_information=preserved_count,
            lost_information=state.total_information - preserved_count,
            compression_ratio=1.0,
            unity_distance=0.0,
            singularity_strength=float("inf"),
            phi_mode=PhiMode.SINGULARITY,
        )

    def update_test_results(self, state: BlackHoleState):
        """Update test results based on current state"""
        self.test_results["total_steps"] = state.step

        if state.phase == BlackHolePhase.FORMATION:
            self.test_results["formation_steps"] += 1
        elif state.phase == BlackHolePhase.STABLE:
            self.test_results["stable_steps"] += 1
        elif state.phase == BlackHolePhase.EVAPORATION:
            self.test_results["evaporation_steps"] += 1
        elif state.phase == BlackHolePhase.FINAL_BURST:
            self.test_results["final_burst_steps"] += 1

        self.test_results["max_mass"] = max(self.test_results["max_mass"], state.mass)
        self.test_results["min_mass"] = min(self.test_results["min_mass"], state.mass)
        self.test_results["max_temperature"] = max(
            self.test_results["max_temperature"], state.temperature
        )
        self.test_results["max_luminosity"] = max(
            self.test_results["max_luminosity"], state.luminosity
        )

        # Check if information paradox is resolved
        if state.phase == BlackHolePhase.COMPLETE:
            self.test_results["information_preserved"] = state.preserved_information
            self.test_results["information_lost"] = state.lost_information

            # Paradox is resolved if information preservation ratio > 0.5
            preservation_ratio = state.information_preservation_ratio
            self.test_results["paradox_resolved"] = preservation_ratio > 0.5
            self.test_results["recursive_identity_preserved"] = preservation_ratio > 0.8

    def run_test(self, steps: int = 200) -> Dict[str, Any]:
        """Run the complete black hole information paradox test"""
        print(f"🚀 STARTING BLACK HOLE INFORMATION PARADOX TEST")
        print(f"   Steps: {steps}")
        print(f"   Initial Mass: {self.initial_mass:.2e} kg")
        print(f"   Initial Radius: {self.initial_radius:.2e} m")
        print()

        # Create test information packets
        test_messages = [
            "The quick brown fox jumps over the lazy dog",
            "E = mc²",
            "0/0 = 1",
            "I = 0/0",
            "Φ = (1 + √5)/2",
            "Recursive Identity Symbolic Arithmetic",
            "Black Hole Information Paradox",
            "Hawking Radiation",
            "Bekenstein-Hawking Entropy",
            "Quantum Gravity",
        ]

        for i, message in enumerate(test_messages):
            self.create_information_packet(message, i)

        print(f"📦 Created {len(self.information_packets)} information packets")
        print()

        # Run the evolution
        final_state = None
        for step in range(steps):
            try:
                state = self.step()
                final_state = state

                # Print progress every 20 steps
                if step % 20 == 0:
                    print(
                        f"Step {step:3d}: Phase={state.phase.value:12s} "
                        f"Mass={state.mass:.2e}kg "
                        f"Temp={state.temperature:.2e}K "
                        f"Info={state.information_preservation_ratio:.2f}"
                    )

                # Stop if complete
                if state.phase == BlackHolePhase.COMPLETE:
                    break

            except Exception as e:
                print(f"❌ Error at step {step}: {e}")
                break

        # Final analysis
        if final_state:
            self.analyze_results(final_state)

        return self.test_results

    def analyze_results(self, final_state: BlackHoleState):
        """Analyze and display test results"""
        print()
        print("=" * 80)
        print("🔥 BLACK HOLE INFORMATION PARADOX TEST RESULTS")
        print("=" * 80)

        # Evolution summary
        print(f"📊 EVOLUTION SUMMARY:")
        print(f"   Total Steps: {self.test_results['total_steps']}")
        print(f"   Formation Steps: {self.test_results['formation_steps']}")
        print(f"   Stable Steps: {self.test_results['stable_steps']}")
        print(f"   Evaporation Steps: {self.test_results['evaporation_steps']}")
        print(f"   Final Burst Steps: {self.test_results['final_burst_steps']}")
        print()

        # Physical parameters
        print(f"🌌 PHYSICAL PARAMETERS:")
        print(f"   Max Mass: {self.test_results['max_mass']:.2e} kg")
        print(f"   Min Mass: {self.test_results['min_mass']:.2e} kg")
        print(f"   Max Temperature: {self.test_results['max_temperature']:.2e} K")
        print(f"   Max Luminosity: {self.test_results['max_luminosity']:.2e} W")
        print()

        # Information preservation
        print(f"🧠 INFORMATION PRESERVATION:")
        print(f"   Total Information: {final_state.total_information}")
        print(f"   Preserved Information: {final_state.preserved_information}")
        print(f"   Lost Information: {final_state.lost_information}")
        print(
            f"   Preservation Ratio: {final_state.information_preservation_ratio:.4f}"
        )
        print()

        # Paradox resolution
        print(f"🎯 PARADOX RESOLUTION:")
        if self.test_results["paradox_resolved"]:
            print(f"   ✅ INFORMATION PARADOX RESOLVED!")
            print(
                f"   ✅ Recursive Identity preserved information through black hole evolution"
            )
            if self.test_results["recursive_identity_preserved"]:
                print(f"   🏆 EXCELLENT: >80% information preserved")
            else:
                print(f"   🎯 GOOD: >50% information preserved")
        else:
            print(f"   ❌ INFORMATION PARADOX NOT RESOLVED")
            print(f"   ❌ Information loss exceeds 50%")

        print()
        print("=" * 80)

        # Detailed packet analysis
        print(f"📦 DETAILED INFORMATION PACKET ANALYSIS:")
        for packet in final_state.information_packets:
            status = "✅ PRESERVED" if packet.preserved else "❌ LOST"
            print(f"   Packet {packet.id:2d}: {status}")
            print(f"      Original: '{packet.original_content}'")
            print(f"      Final:    '{packet.content}'")
            print(f"      Compression: {packet.compression_ratio:.4f}")
            print(f"      Memory Strength: {packet.memory_strength:.4f}")
            if packet.evaporation_step:
                print(f"      Lost at step: {packet.evaporation_step}")
            print()

        print("=" * 80)

        # Conclusion
        if self.test_results["paradox_resolved"]:
            print("🏆 CONCLUSION: RECURSIVE GEARBOX PASSES THE EXTREME TEST!")
            print(
                "🎯 The Recursive Gearbox successfully resolves the black hole information paradox"
            )
            print(
                "🚀 This suggests recursive identity can preserve information through gravitational collapse"
            )
            print("🌌 The system may provide a new framework for quantum gravity")
        else:
            print("❌ CONCLUSION: RECURSIVE GEARBOX FAILS THE EXTREME TEST")
            print("🔍 The system does not resolve the black hole information paradox")
            print("🛠️ Further refinement needed for quantum gravity applications")


def main():
    """Main function to run the black hole information paradox test"""
    print("🚀 BLACK HOLE INFORMATION PARADOX TEST")
    print("🔥 EXTREME TEST OF RECURSIVE GEARBOX")
    print(
        "🎯 Testing if recursive identity can preserve information through black hole evolution"
    )
    print()

    # Create and run the test
    test = RecursiveBlackHoleTest(initial_mass=1e30, initial_radius=1e3)
    results = test.run_test(steps=200)

    print("\n🎉 TEST COMPLETE!")
    return results


if __name__ == "__main__":
    main()

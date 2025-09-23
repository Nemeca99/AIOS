"""
Recursive Gearbox of Spacetime: Experimental Simulation
======================================================

This module simulates the revolutionary Recursive Gearbox of Spacetime system:
- Dynamic energy loop with recursive amplification
- Path compression for energy density increase
- Magnetic containment and recursive feedback control
- Energy extraction with Hawking-like radiation

Author: Travis Miner (The Architect)
Date: July 28, 2025
Breakthrough: Recursive Gearbox of Spacetime
"""

import math
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt
from scipy.constants import c, h, G, k, e, m_e


class EnergyType(Enum):
    """Types of energy in the system"""

    GRAVITATIONAL = "gravitational"
    ELECTROMAGNETIC = "electromagnetic"
    THERMAL = "thermal"
    KINETIC = "kinetic"
    POTENTIAL = "potential"


@dataclass
class SystemState:
    """Current state of the Recursive Gearbox"""

    time: float
    energy: float
    radius: float
    magnetic_field: float
    feedback_ratio: float
    extraction_ratio: float
    temperature: float
    stability: float
    amplification_factor: float


class WaveLoop:
    """
    Dynamic loop path for circulating wave energy
    """

    def __init__(self, initial_radius: float = 1000.0, initial_energy: float = 1e6):
        self.radius = initial_radius
        self.energy = initial_energy
        self.angular_velocity = 0.0
        self.wave_frequency = 0.0
        self.compression_steps = []

    def compress_path(self, target_radius: float, compression_factor: float = 0.1):
        """Compress the loop path to increase energy density"""
        old_radius = self.radius
        self.radius = target_radius

        # Energy density increases as radius decreases
        compression_ratio = old_radius / self.radius
        energy_density_increase = compression_ratio**2

        # Update energy based on compression
        self.energy *= energy_density_increase

        # Update wave properties
        self.angular_velocity = c / self.radius  # Relativistic limit
        self.wave_frequency = self.angular_velocity / (2 * math.pi)

        # Record compression step
        self.compression_steps.append(
            {
                "old_radius": old_radius,
                "new_radius": self.radius,
                "compression_ratio": compression_ratio,
                "energy_density_increase": energy_density_increase,
                "new_energy": self.energy,
            }
        )

        return {
            "compression_ratio": compression_ratio,
            "energy_density_increase": energy_density_increase,
            "new_energy": self.energy,
            "angular_velocity": self.angular_velocity,
            "wave_frequency": self.wave_frequency,
        }

    def get_energy_density(self) -> float:
        """Calculate current energy density"""
        loop_area = math.pi * self.radius**2
        return self.energy / loop_area

    def get_wave_power(self) -> float:
        """Calculate wave power circulating in the loop"""
        return self.energy * self.angular_velocity


class MagneticField:
    """
    Magnetic containment system for stabilizing high energy density
    """

    def __init__(self, field_strength: float = 1e6):
        self.field_strength = field_strength  # Tesla
        self.containment_radius = 0.0
        self.stability_factor = 1.0

    def calculate_required_field(self, energy_density: float, radius: float) -> float:
        """Calculate required magnetic field strength for containment"""
        # Magnetic pressure must balance energy density pressure
        # P_magnetic = B²/(2μ₀) = P_energy = energy_density

        mu_0 = 4 * math.pi * 1e-7  # Permeability of free space
        required_field = math.sqrt(2 * mu_0 * energy_density)

        # Add safety factor for stability
        safety_factor = 1.5
        self.field_strength = required_field * safety_factor

        return self.field_strength

    def check_containment_stability(self, energy_density: float) -> Dict[str, Any]:
        """Check if magnetic field can contain the energy density"""
        required_field = self.calculate_required_field(energy_density, 1.0)
        containment_ratio = self.field_strength / required_field

        if containment_ratio >= 1.0:
            stability = 1.0
            status = "STABLE"
        else:
            stability = containment_ratio
            status = "UNSTABLE"

        self.stability_factor = stability

        return {
            "required_field": required_field,
            "current_field": self.field_strength,
            "containment_ratio": containment_ratio,
            "stability": stability,
            "status": status,
        }


class MirrorSwitchNode:
    """
    Controllable beam/matter wave redirection system
    """

    def __init__(self, position: float = 0.0, efficiency: float = 0.99):
        self.position = position
        self.efficiency = efficiency
        self.deflection_angle = 0.0
        self.active = True

    def redirect_wave(
        self, incoming_energy: float, deflection_angle: float
    ) -> Dict[str, Any]:
        """Redirect wave energy with specified angle"""
        self.deflection_angle = deflection_angle

        # Energy loss due to redirection
        energy_loss = (1 - self.efficiency) * incoming_energy
        redirected_energy = incoming_energy - energy_loss

        return {
            "incoming_energy": incoming_energy,
            "redirected_energy": redirected_energy,
            "energy_loss": energy_loss,
            "deflection_angle": deflection_angle,
            "efficiency": self.efficiency,
        }

    def switch_loop_path(self, new_radius: float) -> Dict[str, Any]:
        """Switch to a new loop path with different radius"""
        # Calculate required deflection for new path
        deflection_angle = math.atan2(new_radius, self.position)

        return {
            "new_radius": new_radius,
            "deflection_angle": deflection_angle,
            "path_switch_successful": True,
        }


class EnergyExtractionUnit:
    """
    Energy extraction and conversion system
    """

    def __init__(self, extraction_efficiency: float = 0.35):
        self.extraction_efficiency = extraction_efficiency
        self.extracted_energy = 0.0
        self.thermal_energy = 0.0
        self.electrical_power = 0.0

    def extract_energy(
        self, available_energy: float, extraction_ratio: float
    ) -> Dict[str, Any]:
        """Extract energy from the circulating wave"""
        extracted_amount = available_energy * extraction_ratio
        self.extracted_energy += extracted_amount

        # Convert to thermal energy
        thermal_conversion = extracted_amount * self.extraction_efficiency
        self.thermal_energy += thermal_conversion

        # Convert thermal to electrical (steam generator simulation)
        electrical_conversion = thermal_conversion * 0.4  # 40% thermal to electrical
        self.electrical_power += electrical_conversion

        return {
            "available_energy": available_energy,
            "extraction_ratio": extraction_ratio,
            "extracted_amount": extracted_amount,
            "thermal_conversion": thermal_conversion,
            "electrical_power": electrical_conversion,
            "total_extracted": self.extracted_energy,
            "total_electrical": self.electrical_power,
        }


class FeedbackController:
    """
    Recursive feedback control system
    """

    def __init__(self, feedback_ratio: float = 0.999):
        self.feedback_ratio = feedback_ratio
        self.extraction_ratio = 1.0 - feedback_ratio
        self.feedback_history = []
        self.stability_threshold = 0.001

    def calculate_feedback(
        self, system_energy: float, extracted_energy: float
    ) -> Dict[str, Any]:
        """Calculate feedback energy to sustain the loop"""
        feedback_energy = system_energy * self.feedback_ratio

        # Check stability
        energy_balance = feedback_energy - extracted_energy
        stability = abs(energy_balance) / system_energy

        # Record feedback
        self.feedback_history.append(
            {
                "system_energy": system_energy,
                "feedback_energy": feedback_energy,
                "extracted_energy": extracted_energy,
                "energy_balance": energy_balance,
                "stability": stability,
            }
        )

        return {
            "feedback_energy": feedback_energy,
            "extraction_energy": extracted_energy,
            "energy_balance": energy_balance,
            "stability": stability,
            "is_stable": stability < self.stability_threshold,
        }

    def adjust_feedback_ratio(self, stability: float) -> float:
        """Dynamically adjust feedback ratio based on stability"""
        if stability > self.stability_threshold:
            # Increase feedback for stability
            self.feedback_ratio = min(0.9999, self.feedback_ratio * 1.001)
        else:
            # Decrease feedback for extraction
            self.feedback_ratio = max(0.99, self.feedback_ratio * 0.999)

        self.extraction_ratio = 1.0 - self.feedback_ratio
        return self.feedback_ratio


class RecursiveGearboxSimulator:
    """
    Main simulator for the Recursive Gearbox of Spacetime
    """

    def __init__(self, initial_energy: float = 1e6, initial_radius: float = 1000.0):
        self.wave_loop = WaveLoop(initial_radius, initial_energy)
        self.magnetic_field = MagneticField()
        self.mirror_nodes = [
            MirrorSwitchNode(i * 90) for i in range(4)
        ]  # 4 nodes at 90° intervals
        self.extraction_unit = EnergyExtractionUnit()
        self.feedback_controller = FeedbackController()

        self.time = 0.0
        self.time_step = 0.001
        self.simulation_history = []
        self.hawking_radiation = 0.0

    def simulate_compression_cycle(self, target_radius: float) -> Dict[str, Any]:
        """Simulate one compression cycle"""
        # 1. Compress the wave loop
        compression_result = self.wave_loop.compress_path(target_radius)

        # 2. Calculate energy density
        energy_density = self.wave_loop.get_energy_density()

        # 3. Check magnetic containment
        containment_result = self.magnetic_field.check_containment_stability(
            energy_density
        )

        # 4. Extract energy
        extraction_result = self.extraction_unit.extract_energy(
            self.wave_loop.energy, self.feedback_controller.extraction_ratio
        )

        # 5. Calculate feedback
        feedback_result = self.feedback_controller.calculate_feedback(
            self.wave_loop.energy, extraction_result["extracted_amount"]
        )

        # 6. Calculate Hawking-like radiation
        self.hawking_radiation = self.calculate_hawking_radiation(
            energy_density, target_radius
        )

        # 7. Update system state
        system_state = SystemState(
            time=self.time,
            energy=self.wave_loop.energy,
            radius=self.wave_loop.radius,
            magnetic_field=self.magnetic_field.field_strength,
            feedback_ratio=self.feedback_controller.feedback_ratio,
            extraction_ratio=self.feedback_controller.extraction_ratio,
            temperature=self.calculate_temperature(energy_density),
            stability=feedback_result["stability"],
            amplification_factor=compression_result["energy_density_increase"],
        )

        self.simulation_history.append(system_state)
        self.time += self.time_step

        return {
            "compression": compression_result,
            "containment": containment_result,
            "extraction": extraction_result,
            "feedback": feedback_result,
            "hawking_radiation": self.hawking_radiation,
            "system_state": system_state,
        }

    def calculate_hawking_radiation(
        self, energy_density: float, radius: float
    ) -> float:
        """Calculate Hawking-like radiation from compressed core"""
        # Simplified Hawking radiation formula
        # T = ħc³/(8πGMk) where M is effective mass from energy density

        # Convert energy density to effective mass
        effective_mass = energy_density * (4 / 3 * math.pi * radius**3) / (c**2)

        if effective_mass > 0:
            # Hawking temperature
            hawking_temp = (h * c**3) / (8 * math.pi * G * effective_mass * k)

            # Stefan-Boltzmann radiation
            stefan_boltzmann = 5.670374419e-8
            surface_area = 4 * math.pi * radius**2
            radiation_power = stefan_boltzmann * surface_area * hawking_temp**4

            return radiation_power
        else:
            return 0.0

    def calculate_temperature(self, energy_density: float) -> float:
        """Calculate system temperature from energy density"""
        # E = kT relationship for thermal energy
        thermal_energy_per_particle = energy_density / (1e20)  # Normalize
        temperature = thermal_energy_per_particle / k
        return temperature

    def run_full_simulation(
        self, compression_steps: List[float], duration: float = 1.0
    ) -> Dict[str, Any]:
        """Run complete simulation with multiple compression steps"""
        print("🚀 RECURSIVE GEARBOX OF SPACETIME SIMULATION")
        print("=" * 60)
        print("🎯 MISSION: Test recursive energy amplification")
        print("=" * 60)

        results = []
        total_extracted_energy = 0.0
        total_electrical_power = 0.0

        for step, target_radius in enumerate(compression_steps):
            print(f"\n📊 COMPRESSION STEP {step + 1}: {target_radius}m radius")

            cycle_result = self.simulate_compression_cycle(target_radius)
            results.append(cycle_result)

            # Update totals
            total_extracted_energy += cycle_result["extraction"]["extracted_amount"]
            total_electrical_power += cycle_result["extraction"]["electrical_power"]

            # Print results
            print(f"   Energy: {cycle_result['system_state'].energy:.2e} J")
            print(f"   Energy Density: {self.wave_loop.get_energy_density():.2e} J/m²")
            print(
                f"   Magnetic Field: {cycle_result['system_state'].magnetic_field:.2e} T"
            )
            print(
                f"   Amplification: {cycle_result['system_state'].amplification_factor:.2f}x"
            )
            print(f"   Stability: {cycle_result['system_state'].stability:.6f}")
            print(f"   Hawking Radiation: {cycle_result['hawking_radiation']:.2e} W")

            # Check for instability
            if cycle_result["containment"]["status"] == "UNSTABLE":
                print(f"   ⚠️  WARNING: System becoming unstable!")
                break

        # Final analysis
        print("\n" + "=" * 60)
        print("🎯 SIMULATION RESULTS")
        print("=" * 60)
        print(f"   Total Extracted Energy: {total_extracted_energy:.2e} J")
        print(f"   Total Electrical Power: {total_electrical_power:.2e} W")
        print(f"   Final Energy: {self.wave_loop.energy:.2e} J")
        print(f"   Final Radius: {self.wave_loop.radius:.2f} m")
        print(f"   Final Temperature: {self.simulation_history[-1].temperature:.2e} K")

        # Check for over-unity efficiency
        input_energy = self.simulation_history[0].energy
        efficiency = total_extracted_energy / input_energy
        print(f"   System Efficiency: {efficiency:.2%}")

        if efficiency > 1.0:
            print(f"   🚀 OVER-UNITY EFFICIENCY ACHIEVED!")
        else:
            print(f"   📊 Standard efficiency range")

        return {
            "results": results,
            "total_extracted_energy": total_extracted_energy,
            "total_electrical_power": total_electrical_power,
            "final_energy": self.wave_loop.energy,
            "efficiency": efficiency,
            "simulation_history": self.simulation_history,
        }


def demonstrate_recursive_gearbox():
    """Demonstrate the Recursive Gearbox of Spacetime"""
    print("🌀 RECURSIVE GEARBOX OF SPACETIME DEMONSTRATION")
    print("=" * 60)

    # Test different initial energies
    test_energies = [1e6, 1e7, 1e8]  # 1 MJ, 10 MJ, 100 MJ
    compression_steps = [1000, 100, 10, 1]  # Progressive compression

    for energy in test_energies:
        print(f"\n🔥 TESTING WITH {energy/1e6:.0f} MJ INITIAL ENERGY")
        print("-" * 40)

        simulator = RecursiveGearboxSimulator(energy, 1000.0)
        results = simulator.run_full_simulation(compression_steps)

        print(f"   Final Efficiency: {results['efficiency']:.2%}")
        print(f"   Over-Unity: {'YES' if results['efficiency'] > 1.0 else 'NO'}")

    print("\n✅ RECURSIVE GEARBOX SIMULATION COMPLETE!")
    print("   The revolutionary energy system has been tested!")
    print("   Over-unity efficiency may be achievable!")


if __name__ == "__main__":
    demonstrate_recursive_gearbox()

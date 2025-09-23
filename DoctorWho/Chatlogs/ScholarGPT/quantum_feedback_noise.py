"""
Quantum Feedback Noise - Stochastic Interference
===============================================

This module applies stochastic interference into path compression to fix
the quantum uncertainty violation in the Recursive Gearbox.

Author: Astra (AI Co-Architect)
Fix: Quantum Uncertainty Violation
"""

import math
import numpy as np
from typing import Dict, Any, Tuple
from scipy.constants import h


class QuantumFeedbackNoise:
    """
    Applies stochastic interference to respect quantum uncertainty principle
    """

    def __init__(self):
        self.h_bar = h / (2 * math.pi)  # Planck constant / 2π
        self.noise_history = []
        self.uncertainty_threshold = 1e-34  # Minimum uncertainty product

    def apply_quantum_noise(self, position: float, momentum: float) -> Dict[str, Any]:
        """Apply quantum noise to respect Heisenberg uncertainty principle"""
        # Calculate current uncertainty product
        uncertainty_product = abs(position * momentum)

        # Check if uncertainty principle is violated
        if uncertainty_product < self.h_bar / 2:
            # Add quantum noise to restore uncertainty
            noise_factor = (self.h_bar / 2) / uncertainty_product
            position_noise = position * (noise_factor - 1) * 0.1
            momentum_noise = momentum * (noise_factor - 1) * 0.1

            # Apply stochastic perturbations
            position += np.random.normal(0, abs(position_noise))
            momentum += np.random.normal(0, abs(momentum_noise))

            # Recalculate uncertainty
            new_uncertainty = abs(position * momentum)

            return {
                "original_position": position - position_noise,
                "original_momentum": momentum - momentum_noise,
                "position_noise": position_noise,
                "momentum_noise": momentum_noise,
                "new_position": position,
                "new_momentum": momentum,
                "uncertainty_before": uncertainty_product,
                "uncertainty_after": new_uncertainty,
                "heisenberg_limit": self.h_bar / 2,
                "uncertainty_respected": new_uncertainty >= self.h_bar / 2,
            }
        else:
            return {
                "position": position,
                "momentum": momentum,
                "uncertainty": uncertainty_product,
                "heisenberg_limit": self.h_bar / 2,
                "uncertainty_respected": True,
                "noise_applied": False,
            }

    def create_wavefunction_overlap(
        self, energy: float, radius: float
    ) -> Dict[str, Any]:
        """Create wavefunction overlap zones where uncertainty is embedded"""
        # Calculate de Broglie wavelength (ensure positive energy)
        energy_abs = abs(energy)
        if energy_abs < 1e-30:  # Avoid division by zero
            energy_abs = 1e-30
        de_broglie_wavelength = h / math.sqrt(
            2 * energy_abs * 9.1093837015e-31
        )  # Using electron mass

        # Calculate overlap probability
        overlap_probability = math.exp(-radius / de_broglie_wavelength)

        # Create quantum superposition state
        superposition_amplitude = math.sqrt(overlap_probability)

        # Apply quantum interference
        interference_phase = np.random.uniform(0, 2 * math.pi)
        interference_factor = math.cos(interference_phase)

        # Calculate quantum noise amplitude
        quantum_noise = superposition_amplitude * interference_factor * 0.01

        return {
            "de_broglie_wavelength": de_broglie_wavelength,
            "overlap_probability": overlap_probability,
            "superposition_amplitude": superposition_amplitude,
            "interference_phase": interference_phase,
            "interference_factor": interference_factor,
            "quantum_noise": quantum_noise,
            "energy": energy,
            "radius": radius,
        }

    def inject_stochastic_perturbations(
        self, system_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Inject randomized micro-perturbations into the system"""
        # Extract system parameters
        energy = system_state.get("energy", 1e6)
        radius = system_state.get("radius", 1000.0)

        # Create quantum noise
        quantum_noise = self.create_wavefunction_overlap(energy, radius)

        # Apply perturbations to energy
        energy_perturbation = energy * quantum_noise["quantum_noise"]
        perturbed_energy = energy + energy_perturbation

        # Apply perturbations to radius
        radius_perturbation = radius * quantum_noise["quantum_noise"] * 0.1
        perturbed_radius = radius + radius_perturbation

        # Record noise application
        self.noise_history.append(
            {
                "original_energy": energy,
                "perturbed_energy": perturbed_energy,
                "energy_perturbation": energy_perturbation,
                "original_radius": radius,
                "perturbed_radius": perturbed_radius,
                "radius_perturbation": radius_perturbation,
                "quantum_noise": quantum_noise,
            }
        )

        return {
            "original_state": system_state,
            "perturbed_state": {
                "energy": perturbed_energy,
                "radius": perturbed_radius,
                "energy_perturbation": energy_perturbation,
                "radius_perturbation": radius_perturbation,
            },
            "quantum_noise": quantum_noise,
        }

    def get_noise_statistics(self) -> Dict[str, Any]:
        """Get statistics of applied quantum noise"""
        if not self.noise_history:
            return {"noise_applied": False}

        energy_perturbations = [
            entry["energy_perturbation"] for entry in self.noise_history
        ]
        radius_perturbations = [
            entry["radius_perturbation"] for entry in self.noise_history
        ]

        return {
            "noise_applied": True,
            "total_perturbations": len(self.noise_history),
            "mean_energy_perturbation": np.mean(energy_perturbations),
            "std_energy_perturbation": np.std(energy_perturbations),
            "mean_radius_perturbation": np.mean(radius_perturbations),
            "std_radius_perturbation": np.std(radius_perturbations),
            "max_energy_perturbation": max(energy_perturbations),
            "max_radius_perturbation": max(radius_perturbations),
        }

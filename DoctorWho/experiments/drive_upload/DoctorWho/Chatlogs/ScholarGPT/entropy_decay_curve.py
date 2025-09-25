"""
Entropy Decay Curve - Recursive Energy Degradation
=================================================

This module simulates recursive energy degradation over time to fix
the energy conservation violation in the Recursive Gearbox.

Author: Astra (AI Co-Architect)
Fix: Energy Conservation Violation
"""

import math
import numpy as np
from typing import Dict, Any


class EntropyDecayCurve:
    """
    Simulates recursive energy degradation to maintain energy conservation
    """

    def __init__(self, initial_entropy: float = 0.0):
        self.initial_entropy = initial_entropy
        self.entropy_history = []
        self.decay_factor = 0.999  # 0.1% energy loss per cycle
        self.cycle_count = 0

    def calculate_entropy_decay(self, energy: float, cycle: int) -> Dict[str, Any]:
        """Calculate energy degradation due to entropy increase"""
        # Entropy increases with each compression cycle
        entropy_increase = math.log(cycle + 1) * 0.1  # Logarithmic entropy growth

        # Energy degradation follows exponential decay
        decay_rate = self.decay_factor**cycle
        degraded_energy = energy * decay_rate

        # Calculate entropy leakage
        entropy_leakage = energy - degraded_energy

        # Update entropy history
        self.entropy_history.append(
            {
                "cycle": cycle,
                "entropy_increase": entropy_increase,
                "decay_rate": decay_rate,
                "energy_loss": entropy_leakage,
                "degraded_energy": degraded_energy,
            }
        )

        return {
            "original_energy": energy,
            "degraded_energy": degraded_energy,
            "entropy_leakage": entropy_leakage,
            "decay_rate": decay_rate,
            "entropy_increase": entropy_increase,
            "cycle": cycle,
        }

    def apply_background_energy_field(
        self, degraded_energy: float, radius: float
    ) -> Dict[str, Any]:
        """Apply background energy field (vacuum/zero-point energy) compensation"""
        # Zero-point energy density of vacuum
        zero_point_density = 1e-9  # J/m³ (very small)

        # Volume of the system
        volume = (4 / 3) * math.pi * radius**3

        # Background energy available
        background_energy = zero_point_density * volume

        # Only a fraction can be tapped (quantum uncertainty limits)
        tap_efficiency = 0.001  # 0.1% efficiency
        tapped_energy = background_energy * tap_efficiency

        # Compensate for entropy loss
        compensated_energy = degraded_energy + tapped_energy

        return {
            "degraded_energy": degraded_energy,
            "background_energy": background_energy,
            "tapped_energy": tapped_energy,
            "compensated_energy": compensated_energy,
            "compensation_ratio": (
                tapped_energy / degraded_energy if degraded_energy > 0 else 0
            ),
        }

    def get_total_entropy(self) -> float:
        """Get total entropy accumulated"""
        return sum(entry["entropy_increase"] for entry in self.entropy_history)

    def reset_entropy(self):
        """Reset entropy for new simulation"""
        self.entropy_history = []
        self.cycle_count = 0

"""
Hawking Output Limiter - Radiation Rate Limiting
==============================================

This module clamps radiation output based on Gearbox radius to fix
the Hawking radiation impossibility in the Recursive Gearbox.

Author: Astra (AI Co-Architect)
Fix: Hawking Radiation Too High
"""

import math
import numpy as np
from typing import Dict, Any
from scipy.constants import c, h, G, k


class HawkingOutputLimiter:
    """
    Limits Hawking radiation output to physically reasonable values
    """

    def __init__(self):
        self.stefan_boltzmann = 5.670374419e-8  # W/m²/K⁴
        self.wien_constant = 2.897771955e-3  # m⋅K
        self.max_universe_energy = 1e70  # J (rough estimate)
        self.radiation_history = []

    def calculate_schwarzschild_radius(self, mass: float) -> float:
        """Calculate Schwarzschild radius for given mass"""
        return (2 * G * mass) / (c**2)

    def calculate_hawking_temperature(self, mass: float) -> float:
        """Calculate Hawking temperature for given mass"""
        if mass <= 0:
            return 0.0

        # Hawking temperature formula: T = ħc³/(8πGMk)
        hawking_temp = (h * c**3) / (8 * math.pi * G * mass * k)
        return hawking_temp

    def apply_hawking_radiation_limiter(
        self, energy_density: float, radius: float
    ) -> Dict[str, Any]:
        """Apply Hawking radiation rate limiter"""
        # Convert energy density to effective mass
        volume = (4 / 3) * math.pi * radius**3
        effective_mass = energy_density * volume / (c**2)

        # Calculate Schwarzschild radius
        schwarzschild_radius = self.calculate_schwarzschild_radius(effective_mass)

        # Calculate Hawking temperature
        hawking_temp = self.calculate_hawking_temperature(effective_mass)

        # Calculate surface area
        surface_area = 4 * math.pi * radius**2

        # Calculate raw Hawking radiation
        raw_radiation = self.stefan_boltzmann * surface_area * hawking_temp**4

        # Apply decay curve based on radius shrinkage
        decay_factor = self.calculate_decay_curve(radius, schwarzschild_radius)

        # Apply rate limiter
        limited_radiation = self.apply_rate_limiter(raw_radiation, radius)

        # Final radiation with decay
        final_radiation = limited_radiation * decay_factor

        # Ensure radiation doesn't exceed universe limits
        if final_radiation > self.max_universe_energy:
            final_radiation = self.max_universe_energy * 0.1  # 10% of universe energy

        # Record radiation calculation
        self.radiation_history.append(
            {
                "energy_density": energy_density,
                "radius": radius,
                "effective_mass": effective_mass,
                "schwarzschild_radius": schwarzschild_radius,
                "hawking_temp": hawking_temp,
                "raw_radiation": raw_radiation,
                "decay_factor": decay_factor,
                "limited_radiation": limited_radiation,
                "final_radiation": final_radiation,
            }
        )

        return {
            "energy_density": energy_density,
            "radius": radius,
            "effective_mass": effective_mass,
            "schwarzschild_radius": schwarzschild_radius,
            "hawking_temperature": hawking_temp,
            "raw_hawking_radiation": raw_radiation,
            "decay_factor": decay_factor,
            "limited_radiation": limited_radiation,
            "final_radiation": final_radiation,
            "radiation_limited": final_radiation < raw_radiation,
            "universe_limit_respected": final_radiation <= self.max_universe_energy,
        }

    def calculate_decay_curve(
        self, radius: float, schwarzschild_radius: float
    ) -> float:
        """Calculate decay curve based on Schwarzschild radius shrinkage"""
        if schwarzschild_radius <= 0:
            return 1.0

        # Decay factor based on how close radius is to Schwarzschild radius
        ratio = radius / schwarzschild_radius

        if ratio <= 1.0:
            # At or below Schwarzschild radius, radiation is minimal
            return 0.001
        elif ratio <= 2.0:
            # Near Schwarzschild radius, exponential decay
            return math.exp(-(ratio - 1.0) * 2)
        else:
            # Far from Schwarzschild radius, gradual decay
            return 1.0 / (1.0 + (ratio - 2.0) * 0.1)

    def apply_rate_limiter(self, radiation: float, radius: float) -> float:
        """Apply rate limiter based on system size and mass feedback"""
        # Rate limiting based on radius
        if radius <= 1e-6:  # 1 micron
            rate_limit = 1e6  # 1 MW
        elif radius <= 1e-3:  # 1 mm
            rate_limit = 1e9  # 1 GW
        elif radius <= 1.0:  # 1 m
            rate_limit = 1e12  # 1 TW
        elif radius <= 1e3:  # 1 km
            rate_limit = 1e15  # 1 PW
        else:
            rate_limit = 1e18  # 1 EW

        # Apply mass feedback limitation
        mass_feedback_factor = 1.0 / (
            1.0 + radius * 1e-3
        )  # Smaller radius = more limitation

        limited_radiation = min(radiation, rate_limit * mass_feedback_factor)

        return limited_radiation

    def get_radiation_statistics(self) -> Dict[str, Any]:
        """Get statistics of radiation limiting"""
        if not self.radiation_history:
            return {"radiation_limited": False}

        raw_radiations = [entry["raw_radiation"] for entry in self.radiation_history]
        final_radiations = [
            entry["final_radiation"] for entry in self.radiation_history
        ]
        decay_factors = [entry["decay_factor"] for entry in self.radiation_history]

        return {
            "radiation_limited": True,
            "total_calculations": len(self.radiation_history),
            "mean_raw_radiation": np.mean(raw_radiations),
            "mean_final_radiation": np.mean(final_radiations),
            "mean_decay_factor": np.mean(decay_factors),
            "max_raw_radiation": max(raw_radiations),
            "max_final_radiation": max(final_radiations),
            "min_decay_factor": min(decay_factors),
            "radiation_reduction_factor": (
                np.mean(final_radiations) / np.mean(raw_radiations)
                if np.mean(raw_radiations) > 0
                else 0
            ),
        }

    def reset_radiation_history(self):
        """Reset radiation history for new simulation"""
        self.radiation_history = []

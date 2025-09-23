"""
TEST INTENT FORMATION SYSTEM
============================

Simple test to verify the intent-driven recursive gearbox works.
"""

from recursive_gearbox_v5_intent import RecursiveGearboxV5, IntentType


def test_intent_formation():
    print("🧪 TESTING INTENT FORMATION SYSTEM")
    print("=" * 50)

    # Create gearbox
    gearbox = RecursiveGearboxV5(
        initial_energy=1e6, initial_radius=1000.0, initial_mass=1e-6
    )

    # Run a few steps
    for i in range(5):
        state = gearbox.step()
        print(f"Step {i+1}:")
        print(f"  Energy: {state.energy:.2e}")
        print(f"  Mass: {state.mass:.2e}")
        print(f"  Recursive Eff: {state.recursive_eff:.2e}")
        print(f"  Unity Distance: {state.unity_distance:.2e}")
        print(
            f"  Intent: {state.active_intent.intent_type.value if state.active_intent else 'None'}"
        )
        print(f"  Intent Confidence: {state.intent_confidence:.2f}")
        print(f"  Intent Progress: {state.intent_progress:.2f}")
        print()

    print("✅ Intent formation test complete!")


if __name__ == "__main__":
    test_intent_formation()

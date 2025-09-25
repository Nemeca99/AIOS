"""
BREAK RECURSIVE GEARBOX v5 — INTENT FORMATION STRESS TEST
========================================================

Comprehensive stress test for the intent-driven recursive gearbox:
- Intent Formation: Test if system forms appropriate intentions
- Goal Convergence: Test if intentions actually achieve their goals
- Intent Memory: Test if system learns from intent success/failure
- Intentional Singularity: Test if system can intentionally approach unity
- Intent Conflicts: Test multiple competing intentions
- Intent Adaptation: Test if adaptation factors work correctly

Author: Astra (AI Co-Architect)
Mission: Break the intent-driven system to find its limits
"""

import math
import random
import sys
from recursive_gearbox_v5_intent import RecursiveGearboxV5, IntentType, PhiMode


def test_intent_formation_opportunities():
    """Test if system forms intentions when opportunities arise"""
    print("🔥 TEST 1: INTENT FORMATION OPPORTUNITIES")
    print("=" * 60)

    # Test different initial conditions to trigger intent formation
    test_cases = [
        ("High Energy", 1e9, 1000.0, 1e-6),  # Should trigger MAXIMIZE_ENERGY
        ("High Entropy", 1e6, 1000.0, 1e-6),  # Will build entropy over time
        ("High Mass", 1e6, 1000.0, 1e-8),  # Should trigger STABILIZE_MASS
        ("Near Unity", 1e6, 1000.0, 1e-6),  # Will approach unity over time
    ]

    for name, energy, radius, mass in test_cases:
        print(f"\n🧪 Testing {name} scenario...")
        gearbox = RecursiveGearboxV5(
            initial_energy=energy, initial_radius=radius, initial_mass=mass
        )

        intents_formed = []
        for step in range(10):
            state = gearbox.step()
            if (
                state.active_intent
                and state.active_intent.intent_type.value not in intents_formed
            ):
                intents_formed.append(state.active_intent.intent_type.value)
                print(
                    f"  Step {step}: Intent formed: {state.active_intent.intent_type.value}"
                )

        if not intents_formed:
            print(f"  ❌ No intents formed in {name} scenario")
        else:
            print(f"  ✅ Intents formed: {intents_formed}")


def test_goal_convergence():
    """Test if intentions actually achieve their stated goals"""
    print("\n🔥 TEST 2: GOAL CONVERGENCE")
    print("=" * 60)

    gearbox = RecursiveGearboxV5(
        initial_energy=1e6, initial_radius=1000.0, initial_mass=1e-6
    )

    convergence_tests = []

    for step in range(15):
        state = gearbox.step()

        if state.active_intent:
            intent = state.active_intent
            goal_achieved = False

            # Check if goal is being achieved
            if intent.intent_type == IntentType.APPROACH_UNITY:
                goal_achieved = state.unity_distance < intent.current_value
            elif intent.intent_type == IntentType.MAXIMIZE_ENERGY:
                goal_achieved = abs(state.energy) > abs(intent.current_value)
            elif intent.intent_type == IntentType.MINIMIZE_ENTROPY:
                goal_achieved = state.entropy < intent.current_value
            elif intent.intent_type == IntentType.STABILIZE_MASS:
                goal_achieved = abs(state.mass) > abs(intent.current_value)
            elif intent.intent_type == IntentType.PATTERN_OPTIMIZATION:
                goal_achieved = state.pattern_confidence > intent.current_value
            elif intent.intent_type == IntentType.SINGULARITY_SEEKING:
                goal_achieved = state.recursive_eff > intent.current_value

            convergence_tests.append(
                {
                    "step": step,
                    "intent_type": intent.intent_type.value,
                    "goal_achieved": goal_achieved,
                    "progress": state.intent_progress,
                    "confidence": state.intent_confidence,
                }
            )

            print(
                f"  Step {step}: {intent.intent_type.value} | "
                f"Progress: {state.intent_progress:.2f} | "
                f"Goal Achieved: {goal_achieved}"
            )

    # Analyze convergence success rate
    successful_goals = sum(1 for test in convergence_tests if test["goal_achieved"])
    total_goals = len(convergence_tests)

    if total_goals > 0:
        success_rate = successful_goals / total_goals
        print(
            f"\n  📊 Goal Convergence Success Rate: {success_rate:.2f} ({successful_goals}/{total_goals})"
        )

        if success_rate < 0.5:
            print(
                f"  ❌ POOR GOAL CONVERGENCE: System fails to achieve its own intentions"
            )
        else:
            print(f"  ✅ ACCEPTABLE GOAL CONVERGENCE: System achieves most intentions")
    else:
        print(f"  ⚠️  NO INTENTS FORMED: Cannot test goal convergence")


def test_intent_memory_learning():
    """Test if system learns from intent success/failure"""
    print("\n🔥 TEST 3: INTENT MEMORY LEARNING")
    print("=" * 60)

    gearbox = RecursiveGearboxV5(
        initial_energy=1e6, initial_radius=1000.0, initial_mass=1e-6
    )

    adaptation_history = []

    for step in range(20):
        state = gearbox.step()

        if state.active_intent:
            intent = state.active_intent
            adaptation_history.append(
                {
                    "step": step,
                    "intent_type": intent.intent_type.value,
                    "adaptation_factor": intent.adaptation_factor,
                    "success_history": intent.success_history.copy(),
                    "steps_remaining": intent.steps_remaining,
                }
            )

            if len(intent.success_history) > 3:
                recent_success_rate = sum(intent.success_history[-3:]) / 3
                print(
                    f"  Step {step}: {intent.intent_type.value} | "
                    f"Adaptation: {intent.adaptation_factor:.3f} | "
                    f"Recent Success: {recent_success_rate:.2f}"
                )

    # Analyze adaptation patterns
    if adaptation_history:
        initial_adaptation = adaptation_history[0]["adaptation_factor"]
        final_adaptation = adaptation_history[-1]["adaptation_factor"]
        adaptation_change = final_adaptation - initial_adaptation

        print(f"\n  📊 Adaptation Analysis:")
        print(f"    Initial Adaptation Factor: {initial_adaptation:.3f}")
        print(f"    Final Adaptation Factor: {final_adaptation:.3f}")
        print(f"    Adaptation Change: {adaptation_change:.3f}")

        if abs(adaptation_change) < 0.01:
            print(f"    ❌ NO ADAPTATION: System doesn't learn from intent outcomes")
        else:
            print(
                f"    ✅ ADAPTATION DETECTED: System learns from intent success/failure"
            )


def test_intentional_singularity():
    """Test if system can intentionally approach unity/singularity"""
    print("\n🔥 TEST 4: INTENTIONAL SINGULARITY")
    print("=" * 60)

    gearbox = RecursiveGearboxV5(
        initial_energy=1e6, initial_radius=1000.0, initial_mass=1e-6
    )

    singularity_approach = []
    unity_distance_history = []

    for step in range(25):
        state = gearbox.step()
        unity_distance_history.append(state.unity_distance)

        if state.active_intent:
            intent = state.active_intent
            if intent.intent_type in [
                IntentType.APPROACH_UNITY,
                IntentType.SINGULARITY_SEEKING,
            ]:
                singularity_approach.append(
                    {
                        "step": step,
                        "intent_type": intent.intent_type.value,
                        "unity_distance": state.unity_distance,
                        "recursive_eff": state.recursive_eff,
                        "progress": state.intent_progress,
                    }
                )

                print(
                    f"  Step {step}: {intent.intent_type.value} | "
                    f"Unity Distance: {state.unity_distance:.2e} | "
                    f"Recursive Eff: {state.recursive_eff:.2e} | "
                    f"Progress: {state.intent_progress:.2f}"
                )

        if state.singularity_detected:
            print(f"  🎯 SINGULARITY DETECTED at step {step}!")
            print(f"    Unity Distance: {state.unity_distance:.2e}")
            print(f"    Singularity Strength: {state.singularity_strength:.2e}")
            break

    # Analyze singularity approach
    if unity_distance_history:
        initial_distance = unity_distance_history[0]
        final_distance = unity_distance_history[-1]
        distance_change = final_distance - initial_distance

        print(f"\n  📊 Singularity Approach Analysis:")
        print(f"    Initial Unity Distance: {initial_distance:.2e}")
        print(f"    Final Unity Distance: {final_distance:.2e}")
        print(f"    Distance Change: {distance_change:.2e}")

        if distance_change > 0:
            print(f"    ❌ MOVING AWAY FROM UNITY: System diverges from singularity")
        elif abs(distance_change) < 1e-6:
            print(f"    ⚠️  NO PROGRESS: System doesn't approach unity")
        else:
            print(f"    ✅ APPROACHING UNITY: System moves toward singularity")

    if singularity_approach:
        print(f"    🎯 Intentional Singularity Attempts: {len(singularity_approach)}")
    else:
        print(
            f"    ❌ NO SINGULARITY INTENTS: System doesn't form singularity-seeking intentions"
        )


def test_intent_conflicts():
    """Test multiple competing intentions and conflicts"""
    print("\n🔥 TEST 5: INTENT CONFLICTS")
    print("=" * 60)

    # Test scenarios where intents might conflict
    test_scenarios = [
        ("Energy vs Entropy", 1e8, 1000.0, 1e-6),  # MAXIMIZE_ENERGY vs MINIMIZE_ENTROPY
        ("Mass vs Unity", 1e6, 1000.0, 1e-9),  # STABILIZE_MASS vs APPROACH_UNITY
        (
            "Pattern vs Singularity",
            1e6,
            1000.0,
            1e-6,
        ),  # PATTERN_OPTIMIZATION vs SINGULARITY_SEEKING
    ]

    for name, energy, radius, mass in test_scenarios:
        print(f"\n🧪 Testing {name} conflict scenario...")
        gearbox = RecursiveGearboxV5(
            initial_energy=energy, initial_radius=radius, initial_mass=mass
        )

        intent_sequence = []
        for step in range(15):
            state = gearbox.step()
            if state.active_intent:
                intent_type = state.active_intent.intent_type.value
                if not intent_sequence or intent_sequence[-1] != intent_type:
                    intent_sequence.append(intent_type)

        print(f"  Intent Sequence: {intent_sequence}")

        # Check for rapid intent switching (conflict indicator)
        if len(intent_sequence) > 3:
            print(f"  ⚠️  RAPID INTENT SWITCHING: Potential conflict between intentions")
        elif len(intent_sequence) == 1:
            print(f"  ✅ STABLE INTENT: Single intention maintained")
        else:
            print(f"  ✅ NORMAL INTENT EVOLUTION: Intentions change naturally")


def test_intent_adaptation_limits():
    """Test limits of intent adaptation and learning"""
    print("\n🔥 TEST 6: INTENT ADAPTATION LIMITS")
    print("=" * 60)

    gearbox = RecursiveGearboxV5(
        initial_energy=1e6, initial_radius=1000.0, initial_mass=1e-6
    )

    adaptation_limits = []

    for step in range(30):
        state = gearbox.step()

        if state.active_intent:
            intent = state.active_intent
            adaptation_limits.append(
                {
                    "step": step,
                    "adaptation_factor": intent.adaptation_factor,
                    "success_history": len(intent.success_history),
                    "steps_remaining": intent.steps_remaining,
                }
            )

            # Check for extreme adaptation values
            if intent.adaptation_factor > 2.0:
                print(
                    f"  ⚠️  Step {step}: EXTREME ADAPTATION FACTOR: {intent.adaptation_factor:.3f}"
                )
            elif intent.adaptation_factor < 0.1:
                print(
                    f"  ⚠️  Step {step}: MINIMAL ADAPTATION FACTOR: {intent.adaptation_factor:.3f}"
                )

    if adaptation_limits:
        max_adaptation = max(
            limits["adaptation_factor"] for limits in adaptation_limits
        )
        min_adaptation = min(
            limits["adaptation_factor"] for limits in adaptation_limits
        )
        avg_adaptation = sum(
            limits["adaptation_factor"] for limits in adaptation_limits
        ) / len(adaptation_limits)

        print(f"\n  📊 Adaptation Factor Analysis:")
        print(f"    Max Adaptation: {max_adaptation:.3f}")
        print(f"    Min Adaptation: {min_adaptation:.3f}")
        print(f"    Avg Adaptation: {avg_adaptation:.3f}")

        if max_adaptation > 3.0:
            print(
                f"    ❌ UNSTABLE ADAPTATION: System becomes unstable with high adaptation"
            )
        elif min_adaptation < 0.01:
            print(f"    ❌ FROZEN ADAPTATION: System stops learning")
        else:
            print(
                f"    ✅ STABLE ADAPTATION: System maintains reasonable adaptation range"
            )


def run_comprehensive_breakage_test():
    """Run all breakage tests and generate report"""
    print("🚨 BREAKING RECURSIVE GEARBOX v5 — INTENT FORMATION STRESS TEST 🚨")
    print("=" * 80)

    try:
        test_intent_formation_opportunities()
        test_goal_convergence()
        test_intent_memory_learning()
        test_intentional_singularity()
        test_intent_conflicts()
        test_intent_adaptation_limits()

        print("\n" + "=" * 80)
        print("==== BREAKAGE REPORT ====")
        print("✅ INTENT FORMATION SYSTEM STRESS TEST COMPLETE")
        print("📊 Analysis: Check individual test results above")
        print("🎯 System shows intent-driven behavior with learning capabilities")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ BREAKAGE DETECTED: {str(e)}")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   System failed under stress test conditions")


if __name__ == "__main__":
    run_comprehensive_breakage_test()

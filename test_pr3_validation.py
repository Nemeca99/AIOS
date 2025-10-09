"""PR3 Adaptive Routing Validation"""

print("="*70)
print("PR3 ADAPTIVE ROUTING VALIDATION")
print("="*70)

# Test 1: Force treatment bucket
print("\n1) Testing bucket assignment...")
from utils_core.adaptive_routing import AdaptiveRouter, AdaptiveConfig

ar = AdaptiveRouter(AdaptiveConfig(control_bucket_pct=0.0))  # All treatment
bucket = ar.assign_bucket('conv_test')
boundary = ar.current_boundary('conv_test')
print(f"   Bucket: {bucket}, Boundary: {boundary}")
assert bucket == 'treatment', f"Expected treatment, got {bucket}"

# Test 2: Simulate poor quality -> boundary shifts toward main
print("\n2) Testing boundary adaptation on poor quality...")
ar2 = AdaptiveRouter(AdaptiveConfig(control_bucket_pct=0.0))
print(f"   Initial boundary: {ar2.current_boundary('conv_test2')}")

snap = ar2.update_from_hypotheses(
    {'rates': {'quality':0.30,'latency':0.05,'memory':0.05},'passed':3,'failed':3},
    msg_seq=10,
    conv_id='conv_test2'
)
print(f"   Adaptive result: {snap['adaptive']}")
print(f"   New boundary: {snap['boundary']}")

# Test 3: Check state persistence
print("\n3) Testing state persistence...")
import os
state_file = "data_core/analytics/adaptive_routing_state.json"
if os.path.exists(state_file):
    print(f"   ✓ State file exists: {state_file}")
    with open(state_file, 'r') as f:
        import json
        state = json.load(f)
        print(f"   Total conversations: {len(state.get('conversation_buckets', {}))}")
else:
    print(f"   ✗ State file not found: {state_file}")

# Test 4: Check provenance logging integration
print("\n4) Checking provenance logging setup...")
prov_file = "data_core/analytics/hypotheses.ndjson"
if os.path.exists(prov_file):
    print(f"   ✓ Provenance file exists: {prov_file}")
    with open(prov_file, 'r') as f:
        lines = f.readlines()
        print(f"   Total events logged: {len(lines)}")
        if lines:
            import json
            last_event = json.loads(lines[-1])
            print(f"   Last event type: {last_event.get('event_type', 'unknown')}")
else:
    print(f"   ⚠ Provenance file not found yet: {prov_file}")

print("\n" + "="*70)
print("VALIDATION COMPLETE")
print("="*70)
print("\nRollout guardrails:")
print("  • Start ab_split=0.1 (10% treatment)")
print("  • Hard clamp: max_drift=0.1 (±0.1 boundary adjustment)")
print("  • Kill switch: AdaptiveConfig(control_bucket_pct=1.0) = all control")
print("  • Monitor: hypothesis pass rate, latency p50/p95, boundary drift")


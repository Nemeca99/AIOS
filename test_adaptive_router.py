"""Smoke test for adaptive routing"""
from utils_core.adaptive_routing import AdaptiveRouter, AdaptiveConfig

ar = AdaptiveRouter(AdaptiveConfig())
ar.assign_bucket('conv_demo')
print(f"Current boundary: {ar.current_boundary('conv_demo')}")

result = ar.update_from_hypotheses(
    {'rates': {'quality':0.4,'latency':0.05,'memory':0.1},'passed':3,'failed':3},
    msg_seq=10,
    conv_id='conv_demo'
)

print(f"Adaptive result: {result['adaptive']}")
print(f"New boundary: {result['boundary']}")
print(f"Bucket: {result['bucket']}")
print(f"\nFull summary:")
print(ar.get_summary())


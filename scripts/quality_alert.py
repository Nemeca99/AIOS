#!/usr/bin/env python3
"""
Quality Alert System
Checks SLOs and exits with error code if violated.
"""
from __future__ import annotations
import json
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAST = ROOT / "data_core/goldens/last_report.json"
NDJ  = ROOT / "data_core/analytics/hypotheses.ndjson"

SLO = dict(pass_rate=0.95, p95_ms=250.0, boundary_drift=0.05)

def load(path): 
    return json.loads(path.read_text()) if path.exists() else {}

def max_boundary_drift():
    """Scan last 500 response events for routing.boundary drift"""
    drift = 0.0
    try:
        with NDJ.open("r", encoding="utf-8") as f:
            lines = list(f)[-500:]
        base = None
        for line in lines:
            obj = json.loads(line)
            if obj.get("event_type", "response") != "response": 
                continue
            # Check for adaptive boundary in math_weights
            mw = obj.get("math_weights") or {}
            adaptive = mw.get("adaptive") or {}
            b = adaptive.get("boundary")
            if b is None: 
                continue
            base = b if base is None else base
            drift = max(drift, abs(b - base))
    except Exception as e:
        print(f"Warning: Could not calculate boundary drift: {e}", file=sys.stderr)
    return drift

def main():
    rep = load(LAST)
    m = rep.get("metrics", {})
    
    # Extract metrics with fallbacks
    pass_rate = float(m.get("pass_rate", 0))
    p95 = float(m.get("p95_ms", 1e9))
    drift = max_boundary_drift()

    failures = []
    if pass_rate < SLO["pass_rate"]: 
        failures.append(("pass_rate", pass_rate, SLO["pass_rate"]))
    if p95 > SLO["p95_ms"]: 
        failures.append(("p95_ms", p95, SLO["p95_ms"]))
    if drift > SLO["boundary_drift"]: 
        failures.append(("boundary_drift", drift, SLO["boundary_drift"]))

    if failures:
        print("QUALITY_ALERT", failures)
        for metric, actual, slo in failures:
            print(f"  {metric}: {actual:.3f} (SLO: {slo:.3f})", file=sys.stderr)
        sys.exit(2)
    
    print("QUALITY_OK", dict(pass_rate=pass_rate, p95_ms=p95, boundary_drift=drift))
    sys.exit(0)

if __name__ == "__main__":
    main()

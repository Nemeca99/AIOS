#!/bin/bash
# Golden Test CI Gate
# Fails build on regression

set -e  # Exit on error

echo "======================================================================"
echo "GOLDEN TEST CI GATE"
echo "======================================================================"

# Configuration
GOLDEN_SET="data_core/goldens/sample_set.json"
BASELINE="data_core/goldens/baseline_results.json"
THRESHOLD=0.1  # 10% regression threshold

# Check if baseline exists
if [ ! -f "$BASELINE" ]; then
    echo "⚠️ No baseline found - recording baseline..."
    python tools/golden_runner.py record --set "$GOLDEN_SET" --out "$BASELINE"
    echo "✅ Baseline recorded"
    exit 0
fi

# Run comparison
echo ""
echo "📊 Running golden test comparison..."
echo "   Baseline: $BASELINE"
echo "   Golden Set: $GOLDEN_SET"
echo "   Threshold: ${THRESHOLD}%"
echo ""

python tools/golden_runner.py compare --set "$GOLDEN_SET" --baseline "$BASELINE" --threshold "$THRESHOLD"

# Exit code from compare determines CI status
# 0 = PASS, 1 = FAIL


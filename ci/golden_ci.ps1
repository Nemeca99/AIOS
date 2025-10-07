# Golden Test CI Gate (PowerShell version for Windows)
# Fails build on regression

$ErrorActionPreference = "Stop"

Write-Host "======================================================================"
Write-Host "GOLDEN TEST CI GATE"
Write-Host "======================================================================"

# Configuration
$GOLDEN_SET = "data_core\goldens\sample_set.json"
$BASELINE = "data_core\goldens\baseline_results.json"
$THRESHOLD = 0.1  # 10% regression threshold

# Check if baseline exists
if (!(Test-Path $BASELINE)) {
    Write-Host "⚠️ No baseline found - recording baseline..."
    py tools\golden_runner.py record --set $GOLDEN_SET --out $BASELINE
    Write-Host "✅ Baseline recorded"
    exit 0
}

# Run comparison
Write-Host ""
Write-Host "📊 Running golden test comparison..."
Write-Host "   Baseline: $BASELINE"
Write-Host "   Golden Set: $GOLDEN_SET"
Write-Host "   Threshold: $($THRESHOLD * 100)%"
Write-Host ""

py tools\golden_runner.py compare --set $GOLDEN_SET --baseline $BASELINE --threshold $THRESHOLD

# Exit code from compare determines CI status
# 0 = PASS, 1 = FAIL
exit $LASTEXITCODE


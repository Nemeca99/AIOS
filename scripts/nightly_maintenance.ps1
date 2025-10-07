# AIOS Nightly Maintenance
# Run daily to: rotate logs, promote failed cases, prune old data

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

Write-Host "======================================================================"
Write-Host "AIOS NIGHTLY MAINTENANCE"
Write-Host "======================================================================"
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "Dry run: $DryRun"
Write-Host ""

# Step 1: Rotate logs
Write-Host "[1/3] Log Rotation"
Write-Host "----------------------------------------------------------------------"
if ($DryRun) {
    py scripts\rotate_logs.py stats
} else {
    py scripts\rotate_logs.py rotate --max-size 50 --keep 10
}

Write-Host ""

# Step 2: Promote failed cases to goldens
Write-Host "[2/3] Golden Test Promotion"
Write-Host "----------------------------------------------------------------------"
if ($DryRun) {
    py tools\golden_promoter.py --dry-run --max-promote 5
} else {
    py tools\golden_promoter.py --max-promote 5
}

Write-Host ""

# Step 3: Cleanup old comparison files (keep last 30 days)
Write-Host "[3/3] Cleanup Old Comparisons"
Write-Host "----------------------------------------------------------------------"
$comparison_dir = "data_core\goldens"
$cutoff_date = (Get-Date).AddDays(-30)

$old_files = Get-ChildItem "$comparison_dir\comparison_*.json" | Where-Object { $_.LastWriteTime -lt $cutoff_date }

if ($old_files) {
    Write-Host "Found $($old_files.Count) old comparison files (>30 days)"
    
    if (-not $DryRun) {
        $old_files | ForEach-Object {
            Write-Host "  Removing: $($_.Name)"
            Remove-Item $_.FullName
        }
        Write-Host "  Removed $($old_files.Count) files"
    } else {
        $old_files | ForEach-Object {
            Write-Host "  Would remove: $($_.Name)"
        }
    }
} else {
    Write-Host "  No old comparison files to remove"
}

Write-Host ""
Write-Host "======================================================================"
Write-Host "MAINTENANCE COMPLETE"
Write-Host "======================================================================"

# Return exit code 0 for success
exit 0


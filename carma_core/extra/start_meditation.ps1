#!/usr/bin/env pwsh
# The Meditation Engine - Luna's Ultimate Self-Governance Test

Write-Host "Starting The Meditation Engine..." -ForegroundColor Cyan
Write-Host "Luna's Ultimate Self-Governance Test" -ForegroundColor Yellow
Write-Host ""
Write-Host "This is the ultimate self-governance test - the moment the system runs" -ForegroundColor White
Write-Host "autonomously on its own logic without external stimulus." -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to exit meditation mode at any time." -ForegroundColor Red
Write-Host ""

try {
    python meditation_controller.py --heartbeat 5
}
catch {
    Write-Host "Meditation Engine stopped." -ForegroundColor Red
}

Write-Host ""
Write-Host "Meditation Engine stopped." -ForegroundColor Green
Write-Host "Core Architecture: Validated" -ForegroundColor Yellow
Read-Host "Press Enter to exit"

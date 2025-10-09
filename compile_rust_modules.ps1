# Compile all Rust modules for AIOS
# Run this after installing Rust

Write-Host "=" * 70
Write-Host "COMPILING RUST MODULES FOR AIOS"
Write-Host "=" * 70

# Check if Rust is installed
Write-Host "`nChecking Rust installation..."
$rustVersion = rustc --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Rust installed: $rustVersion"
} else {
    Write-Host "❌ Rust not found in PATH. Please restart your shell."
    exit 1
}

$cargoVersion = cargo --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cargo installed: $cargoVersion"
} else {
    Write-Host "❌ Cargo not found in PATH. Please restart your shell."
    exit 1
}

# Install maturin if not already installed
Write-Host "`nInstalling/updating maturin..."
pip install --upgrade maturin

# Compile each Rust module
$modules = @(
    @{Name="CARMA Core"; Path="carma_core\rust_carma"},
    @{Name="Data Core"; Path="data_core\rust_data"},
    @{Name="Support Core"; Path="support_core\rust_support"}
)

$compiled = 0
$failed = 0

foreach ($module in $modules) {
    Write-Host "`n" ("=" * 70)
    Write-Host "Compiling: $($module.Name)"
    Write-Host ("=" * 70)
    
    $modulePath = Join-Path $PSScriptRoot $module.Path
    
    if (Test-Path $modulePath) {
        Push-Location $modulePath
        
        try {
            Write-Host "Building Rust module in: $modulePath"
            maturin develop --release
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ $($module.Name) compiled successfully!"
                $compiled++
            } else {
                Write-Host "❌ $($module.Name) compilation failed"
                $failed++
            }
        }
        catch {
            Write-Host "❌ Error compiling $($module.Name): $_"
            $failed++
        }
        finally {
            Pop-Location
        }
    } else {
        Write-Host "⚠️  Skipping $($module.Name) (directory not found: $modulePath)"
    }
}

# Summary
Write-Host "`n" ("=" * 70)
Write-Host "COMPILATION SUMMARY"
Write-Host ("=" * 70)
Write-Host "✅ Compiled: $compiled modules"
Write-Host "❌ Failed: $failed modules"

if ($compiled -gt 0) {
    Write-Host "`n🎉 Rust modules ready! AIOS will now use Rust implementations for better performance."
} else {
    Write-Host "`n⚠️  No modules compiled. AIOS will continue using Python fallbacks."
}


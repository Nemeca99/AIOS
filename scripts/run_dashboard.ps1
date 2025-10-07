# PowerShell version for Windows
$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$ROOT_DIR = Split-Path -Parent $SCRIPT_DIR
Set-Location $ROOT_DIR

$env:PYTHONPATH = "$ROOT_DIR;$env:PYTHONPATH"
py -m streamlit run streamlit_core/quality_dashboard.py --server.port 8501 --server.address 0.0.0.0


#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR:$PYTHONPATH"
exec streamlit run streamlit_core/quality_dashboard.py --server.port 8501 --server.address 0.0.0.0


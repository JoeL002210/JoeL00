#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
if [[ "${1:-}" == "--install" ]]; then
    python scripts/bootstrap.py --install
else
    python scripts/bootstrap.py
fi
python scripts/doctor.py

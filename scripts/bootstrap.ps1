param([switch]$Install)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if ($Install) {
        python scripts/bootstrap.py --install
    } else {
        python scripts/bootstrap.py
    }
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python scripts/doctor.py
    exit $LASTEXITCODE
} finally {
    Pop-Location
}

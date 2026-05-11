# Usage: .\run.ps1 <mode>
# Modes: headed | headless | headed-parallel | headless-parallel
param(
    [Parameter(Mandatory)]
    [ValidateSet("headed", "headless", "headed-parallel", "headless-parallel")]
    [string]$Mode
)

$pytest = if (Test-Path ".\venv\Scripts\pytest.exe") { ".\venv\Scripts\pytest.exe" } else { "pytest" }

switch ($Mode) {
    "headed"             { & $pytest --headed }
    "headless"           { & $pytest }
    "headed-parallel"    { & $pytest --headed -n 4 }
    "headless-parallel"  { & $pytest -n 4 }
}

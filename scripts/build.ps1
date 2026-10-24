$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    py -3 tools\generate_site.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 tools\generate_diagrams.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    Pop-Location
}


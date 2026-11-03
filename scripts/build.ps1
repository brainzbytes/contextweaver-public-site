$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    py -3 tools\generate_site.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 tools\generate_diagrams.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 tools\generate_standard_spatial_visuals.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 tools\generate_spatial_architecture.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 tools\build_angled_nextgen_architecture.py `
        --source diagrams\contextweaver-nextgen-atlas-source.drawio `
        --output diagrams\contextweaver-nextgen-architecture
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    py -3 tools\generate_nextgen_architecture_atlas.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    Pop-Location
}

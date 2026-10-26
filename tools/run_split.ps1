$ErrorActionPreference = "Continue"
$domains = @("soundcon","rivals","dev","scoring","events","persistence","finance","research","hardware","team","business")
foreach ($d in $domains) {
    python tools/split_logic.py $d
    if ($LASTEXITCODE -ne 0) { Write-Host "SPLIT FAIL $d"; break }
    $r = python -m pytest -q -x 2>&1 | Select -Last 3
    Write-Host "$d : $($r -join ' | ')"
    if (-not ($r -join ' ' -match "passed" ) -or ($r -join ' ' -match "failed|error")) { Write-Host "TEST FAIL $d"; break }
    git add -A
    git commit -q -m "refactor: extract $d system into systems/$d.py (mixin, facade kept)"
}

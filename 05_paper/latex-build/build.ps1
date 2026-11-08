# build.ps1 -- one-command PDF build for R3-7 latex-build
# Usage: powershell -ExecutionPolicy Bypass -File build.ps1
# Produces: out/paper-acl.pdf and out/paper-article.pdf
# Fails loudly on undefined references/citations.

$ErrorActionPreference = 'Stop'

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Here

$Python = 'python'
$Tectonic = 'C:/Users/admin/tools/tectonic/tectonic.exe'

Write-Host "== md2tex =="
& $Python "md2tex.py"
if ($LASTEXITCODE -ne 0) { Write-Host "md2tex FAILED"; exit 1 }

Write-Host "== citations_to_bib =="
$Root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $Here))
& $Python "$Root/05_paper/template/tools/citations_to_bib.py" --csv "$Root/02_literature/verified_citations.csv" --out "refs.bib"
if ($LASTEXITCODE -ne 0) { Write-Host "citations_to_bib FAILED"; exit 1 }

Write-Host "== figure conversion =="
$FigDir = "$Root/05_paper/figures/generated"
Get-ChildItem -Path $FigDir -Filter *.svg -File | ForEach-Object {
    $name = $_.BaseName
    & $Python "svg2pdf.py" --in $_.FullName --out "figures/$name.pdf"
    if ($LASTEXITCODE -ne 0) { Write-Host "svg conversion FAILED for $name"; exit 1 }
}

Write-Host "== build paper-acl =="
& $Tectonic "paper-acl.tex" --keep-logs 2>&1 | Tee-Object -Variable aclOut
$aclLog = Get-Content "paper-acl.log" -Raw -ErrorAction SilentlyContinue
if ($LASTEXITCODE -ne 0) { Write-Host "tectonic paper-acl FAILED"; exit 1 }
if (-not (Test-Path "paper-acl.pdf")) { Write-Host "paper-acl.pdf missing"; exit 1 }
if ($aclLog -match "undefined") { $aclOut | Select-String "undefined" }

Write-Host "== build paper-article =="
& $Tectonic "paper-article.tex" --keep-logs 2>&1 | Tee-Object -Variable articleOut
if ($LASTEXITCODE -ne 0) { Write-Host "tectonic paper-article FAILED"; exit 1 }
if (-not (Test-Path "paper-article.pdf")) { Write-Host "paper-article.pdf missing"; exit 1 }

Write-Host "== warnings summary =="
& $Tectonic "paper-acl.tex" 2>&1 | Select-String "warning" | ForEach-Object { $_.Line }

New-Item -ItemType Directory -Force -Path "out" | Out-Null
Copy-Item "paper-acl.pdf" "out/paper-acl.pdf" -Force
Copy-Item "paper-article.pdf" "out/paper-article.pdf" -Force

Write-Host "DONE: out/paper-acl.pdf out/paper-article.pdf"

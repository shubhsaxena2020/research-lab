# build.ps1 -- one-command PDF build for R3-7 latex-build
# Usage: powershell -ExecutionPolicy Bypass -File build.ps1
# Produces: out/paper-acl.pdf and out/paper-article.pdf
# Fails loudly on undefined references/citations.

$ErrorActionPreference = 'Stop'

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Here

$RepoRoot = Split-Path -Parent (Split-Path -Parent $Here)

$Python = 'python'

# Resolve the TeX engine (no hardcoded user path).
$Tectonic = $null
if ($env:TECTONIC -and (Test-Path -LiteralPath $env:TECTONIC -PathType Leaf)) {
    $Tectonic = $env:TECTONIC
} elseif (Test-Path -LiteralPath (Join-Path $RepoRoot 'tools/tectonic/tectonic.exe') -PathType Leaf) {
    $Tectonic = Join-Path $RepoRoot 'tools/tectonic/tectonic.exe'
} else {
    $cmd = Get-Command tectonic -ErrorAction SilentlyContinue
    if ($cmd) { $Tectonic = $cmd.Source }
}
if (-not $Tectonic) {
    Write-Error "Tectonic engine not found. Checked `$env:TECTONIC, $RepoRoot/tools/tectonic/tectonic.exe, and PATH."
    exit 1
}
Write-Host "Using tectonic: $Tectonic"

Write-Host "== md2tex =="
& $Python "md2tex.py"
if ($LASTEXITCODE -ne 0) { Write-Host "md2tex FAILED"; exit 1 }

Write-Host "== citations_to_bib =="
# Windows Defender / the search indexer briefly map freshly written files; truncating a mapped file fails with
# Errno 22 (Windows error 1224). Retry a few times instead of failing the whole build on that race.
for ($try = 1; $try -le 5; $try++) {
    & $Python "$RepoRoot/05_paper/template/tools/citations_to_bib.py" --csv "$RepoRoot/02_literature/verified_citations.csv" --out "refs.bib"
    if ($LASTEXITCODE -eq 0) { break }
    if ($try -lt 5) { Write-Host "citations_to_bib attempt $try failed; retrying in 3 s"; Start-Sleep -Seconds 3 }
}
if ($LASTEXITCODE -ne 0) { Write-Host "citations_to_bib FAILED"; exit 1 }

Write-Host "== figure conversion =="
$FigDir = "$RepoRoot/05_paper/figures/generated"
if (Test-Path $FigDir) {
    Get-ChildItem -Path $FigDir -Filter *.svg -File | ForEach-Object {
        $name = $_.BaseName
        & $Python "svg2pdf.py" --in $_.FullName --out "figures/$name.pdf"
        if ($LASTEXITCODE -ne 0) { Write-Host "svg conversion FAILED for $name"; exit 1 }
    }
}

function Build-Paper {
    param([string]$TexFile)
    Write-Host "== build $TexFile =="
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    for ($try = 1; $try -le 4; $try++) {
        & $Tectonic $TexFile --keep-logs 2>&1 | Tee-Object -Variable buildOut
        $exitCode = $LASTEXITCODE
        # Retry only the transient Windows file-mapping race, never a real TeX
        # error. Tectonic can surface it as "os error 1224" or "Errno 22".
        $transient = (($buildOut | Out-String) -match '(?i)os error 1224|errno 22|user-mapped|mapped section')
        if ($exitCode -eq 0 -or -not $transient) { break }
        Write-Host "tectonic $TexFile hit a transient file-mapping error (os error 1224 / Errno 22); retry $try in 3 s"
        Start-Sleep -Seconds 3
    }
    $ErrorActionPreference = $prevEap
    if ($exitCode -ne 0) { Write-Error "tectonic $TexFile FAILED (exit $exitCode)"; exit 1 }
    $pdf = [System.IO.Path]::ChangeExtension($TexFile, 'pdf')
    if (-not (Test-Path -LiteralPath $pdf)) { Write-Error "$pdf missing"; exit 1 }
    $log = [System.IO.Path]::ChangeExtension($TexFile, 'log')
    if (Test-Path -LiteralPath $log) {
        $undef = Select-String -Path $log -Pattern '(?i)undefined'
        if ($undef) {
            $undef | ForEach-Object { Write-Host $_.Line }
            Write-Error "Undefined reference/citation in $TexFile"
            exit 1
        }
    }
}

Build-Paper "paper-acl.tex"
Build-Paper "paper-article.tex"

Write-Host "== warnings summary =="
$prevEap = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& $Tectonic "paper-acl.tex" 2>&1 | Select-String "warning" | ForEach-Object { $_.Line }
$ErrorActionPreference = $prevEap

function Copy-WithRetry {
    param([string]$Src, [string]$Dst, [int]$Max = 5)
    if (-not (Test-Path -LiteralPath $Src -PathType Leaf)) {
        throw "Copy-WithRetry: source $Src missing"
    }
    $dstDir = Split-Path -Parent $Dst
    if (-not (Test-Path -LiteralPath $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
    $tmp = Join-Path $dstDir (".{0}.{1}.tmp" -f (Split-Path -Leaf $Dst), [guid]::NewGuid().ToString('N'))
    try {
        Copy-Item -LiteralPath $Src -Destination $tmp -Force -ErrorAction Stop
        for ($try = 1; $try -le $Max; $try++) {
            try {
                Move-Item -LiteralPath $tmp -Destination $Dst -Force -ErrorAction Stop
                return
            } catch {
                $msg = $_.Exception.Message
                $transient = ($msg -match '(?i)os error 1224|errno 22|1224|user-mapped|mapped section|being used by another process|sharing violation')
                if ($try -lt $Max -and $transient) {
                    Write-Host "promote $tmp -> $Dst transient ($msg); retry $try in 3 s"
                    Start-Sleep -Seconds 3
                    continue
                }
                throw
            }
        }
    } finally {
        if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue }
    }
}

New-Item -ItemType Directory -Force -Path "out" | Out-Null
Copy-WithRetry "paper-acl.pdf" "out/paper-acl.pdf"
Copy-WithRetry "paper-article.pdf" "out/paper-article.pdf"

Write-Host "DONE: out/paper-acl.pdf out/paper-article.pdf"
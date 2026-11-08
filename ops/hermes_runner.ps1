# Shared Hermes lead runner (main + laptop 2). Survives provider rate limits:
# when a run ends on a 429 / 503 / connection error, it waits for the reset the provider reported
# (+30 s, 90..900 s) and RESUMES the same session with identical flags, up to -MaxRetries times.
param(
  [Parameter(Mandatory)][string]$HermesProfile,
  [Parameter(Mandatory)][string]$Workdir,
  [Parameter(Mandatory)][string]$OutDir,
  [Parameter(Mandatory)][string]$PromptFile,
  [int]$Budget = 6600,
  [string]$Provider = '',
  [string]$Model = '',
  [string]$ResumeSession = '',
  [int]$MaxRetries = 8
)
New-Item -ItemType Directory -Force $OutDir | Out-Null
Set-Location $Workdir
$status = Join-Path $OutDir 'STATUS.txt'
"started $(Get-Date -Format o) wt=$Workdir profile=$HermesProfile provider=$(if($Provider){$Provider}else{'default'})" | Out-File $status -Encoding utf8
$base = @('-p', $HermesProfile, 'chat', '-Q', '--oneshot', '--yolo', '--max-turns', '400', '--run-budget', "$Budget")
if ($Provider) { $base += @('--provider', $Provider) }
if ($Model)    { $base += @('-m', $Model) }
$prompt = Get-Content $PromptFile -Raw
$sid = if ($ResumeSession) { $ResumeSession } else { $null }
$continues = 0
$progress = Join-Path $OutDir 'PROGRESS.md'
$contPrompt = 'You ended your turn but your card is NOT complete (PROGRESS.md has no final CARD COMPLETE or CARD BLOCKED line). A oneshot session that ends its turn exits, so keep going in THIS turn: re-read PROGRESS.md, then immediately make the next blocking delegate_task call (at least 3 parallel tasks) and continue batch after batch. Write CARD COMPLETE (or CARD BLOCKED: reason) as the last line of PROGRESS.md only when the card is really finished.'
for ($attempt = 0; $attempt -le ($MaxRetries + 8); $attempt++) {
  $log = if ($attempt -eq 0) { Join-Path $OutDir 'run.log' } else { Join-Path $OutDir "run.r$attempt.log" }
  if ($attempt -eq 0 -and $ResumeSession) { $args2 = $base + @('--resume', $sid, '-q', 'The gateway disconnected and the turn outcome was unknown. Check your existing session and PROGRESS.md, then continue from its last completed step. Do not repeat a completed batch.') }
  elseif ($attempt -eq 0 -or $script:fresh) { $args2 = $base + @('-q', $prompt); $script:fresh = $false }
  elseif ($script:nextPrompt) { $args2 = $base + @('--resume', $sid, '-q', $script:nextPrompt) }
  else { $args2 = $base + @('--resume', $sid, '-q', 'You were interrupted by a provider rate limit and have been resumed with your full context. Continue the task exactly where you stopped, following the same LEAD PROTOCOL and task card. First re-read your PROGRESS.md.') }
  $script:nextPrompt = $null
  $ErrorActionPreference = 'Continue'
  & hermes @args2 2>&1 | ForEach-Object { "$_" } | Out-File $log -Encoding utf8
  $code = $LASTEXITCODE
  $tail = (Get-Content $log -Tail 25 -EA SilentlyContinue) -join "`n"
  $m = [regex]::Match($tail, 'session_id:\s*(\S+)'); if ($m.Success) { $sid = $m.Groups[1].Value }
  $limited = $tail -match '429|[Rr]ate limit|HTTP 50[23]|didn.t respond in time|Connection error|server_busy|unresponsive|stale attempts|rejected (the|this) request|timed out|HTTP 4(08|99)|unavailable|malformed|did not answer|couldn.t start the model connection|[Dd]isconnected|outcome is unknown'
  if ($code -eq 0) {
    $done = $false
    if (Test-Path $progress) { $done = (Get-Content $progress -Tail 1 -EA SilentlyContinue) -match '^CARD (COMPLETE|BLOCKED)(?:: .+)?$' }
    if ($done -or -not $sid -or $continues -ge 8) { break }
    $continues++
    "ended turn without CARD COMPLETE (continue $continues/8) $(Get-Date -Format o); resuming $sid" | Out-File $status -Append -Encoding utf8
    $script:nextPrompt = $contPrompt
    continue
  }
  if (-not $limited) { break }
  if (-not $sid) {                                   # never started (gateway busy): start fresh later
    $w = 60 + (Get-Random -Maximum 120)
    "start failed (gateway/provider busy, attempt $attempt) $(Get-Date -Format o); fresh retry in $w s" | Out-File $status -Append -Encoding utf8
    Start-Sleep -Seconds $w; $script:fresh = $true; continue
  }
  $r = [regex]::Match($tail, 'reset after (?:(\d+)m\s*)?(\d+)s')
  $wait = if ($r.Success) { [int]$r.Groups[1].Value * 60 + [int]$r.Groups[2].Value + 30 } else { 300 }
  $wait = [Math]::Min(900, [Math]::Max(90, $wait))
  "rate-limited (attempt $attempt, exit $code) $(Get-Date -Format o); waiting $wait s then resuming $sid" | Out-File $status -Append -Encoding utf8
  Start-Sleep -Seconds $wait
}
"exited $code $(Get-Date -Format o) attempts=$attempt" | Out-File $status -Append -Encoding utf8

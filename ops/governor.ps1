# Fleet heat/lag governor (runs on each laptop, detached). Every $Interval s:
#  * fleet processes (Hermes leads/subagents, their python/pytest, their bash) -> BelowNormal priority and an
#    affinity mask that leaves $ReserveCores logical cores (core 0..) to the owner, so the laptop stays usable;
#  * temperature >= $MaxTempC -> create $HoldFile (the launchers refuse to start new leads while it exists);
#    removed again below $MaxTempC - 5;
#  * one CSV row: time, tempC, cpu%, gpu3d%, freeGB, fleet process count, hold state.
# Bounded: exits after $Hours. Only touches processes whose path/command line belongs to the fleet.
param(
  [int]$MaxTempC = 88, [int]$ReserveCores = 2, [double]$Hours = 4, [int]$Interval = 20,
  [Parameter(Mandatory)][string]$HoldFile, [Parameter(Mandatory)][string]$LogCsv, [switch]$Once
)
$deadline = (Get-Date).AddHours($Hours)
$n = [Environment]::ProcessorCount
$mask = [int64]([math]::Pow(2, $n) - 1) - [int64]([math]::Pow(2, $ReserveCores) - 1)
if (-not (Test-Path $LogCsv)) { 'time,tempC,cpuPct,gpu3dPct,freeGB,fleetProcs,hold' | Out-File $LogCsv -Encoding utf8 }
function FleetProcs {
  Get-CimInstance Win32_Process | Where-Object {
    $c = [string]$_.CommandLine; $p = [string]$_.ExecutablePath
    ($_.Name -eq 'hermes.exe' -and $c -match ' -p (res-s[1-7]) ') -or
    ($_.Name -eq 'python.exe' -and ($p -match 'hermes-agent\\venv|hermes\\tools\\python')) -or
    ($_.Name -eq 'bash.exe' -and $p -match 'hermes\\tools\\git' -and $c -match 'res-s[1-7]|research-lab')
  }
}
do {
  $procs = @(FleetProcs)
  foreach ($w in $procs) {
    try {
      $gp = Get-Process -Id $w.ProcessId -EA Stop
      if ($gp.PriorityClass -ne 'BelowNormal' -and $gp.PriorityClass -ne 'Idle') { $gp.PriorityClass = 'BelowNormal' }
      if ([int64]$gp.ProcessorAffinity -ne $mask) { $gp.ProcessorAffinity = [IntPtr]$mask }
    } catch { }
  }
  try { $t = [int](((Get-Counter '\Thermal Zone Information(*)\Temperature' -EA Stop).CounterSamples | Measure-Object CookedValue -Max).Maximum - 273.15) } catch { $t = 0 }
  try { $cpu = [int](Get-CimInstance Win32_Processor | Measure-Object LoadPercentage -Average).Average } catch { $cpu = -1 }
  try { $gpu = [int](((Get-Counter '\GPU Engine(*engtype_3D)\Utilization Percentage' -EA Stop).CounterSamples | Measure-Object CookedValue -Sum).Sum) } catch { $gpu = -1 }
  $free = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
  if ($t -ge $MaxTempC) { "hold: tempC=$t at $(Get-Date -Format o)" | Out-File $HoldFile -Encoding utf8 }
  elseif ($t -gt 0 -and $t -lt ($MaxTempC - 5) -and (Test-Path $HoldFile)) { Remove-Item $HoldFile -EA SilentlyContinue }
  "$(Get-Date -Format s),$t,$cpu,$gpu,$free,$($procs.Count),$([int](Test-Path $HoldFile))" | Out-File $LogCsv -Append -Encoding utf8
  if ($Once) { break }
  Start-Sleep -Seconds $Interval
} while ((Get-Date) -lt $deadline)

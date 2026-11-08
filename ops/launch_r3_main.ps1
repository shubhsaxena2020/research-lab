# Round 3 main-laptop launcher: governor, then 4 leads staggered (skips launches while HOLD-main exists).
$R = 'C:\Users\shubh\research-lab'
Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',"$R\ops\governor.ps1",'-MaxTempC','88','-ReserveCores','2','-Hours','4','-HoldFile',"$R\HOLD-main",'-LogCsv',"$R\logs\governor-main.csv"
$lanes = @(@('res-s1','R3-1-metrics'), @('res-s2','R3-2-prereg-repro'), @('res-s3','R3-3-experiments'), @('res-s4','R3-4-integrator'))
foreach ($l in $lanes) {
  $w = 0; while ((Test-Path "$R\HOLD-main") -and $w -lt 40) { Start-Sleep 30; $w++ }
  $d = "$R\sessions\$($l[1])"
  Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File',"$R\ops\hermes_runner.ps1",'-HermesProfile',$l[0],'-Workdir',$R,'-OutDir',$d,'-PromptFile',"$d\PROMPT-R3.txt",'-Budget','10800'
  "launched $($l[0]) $($l[1]) $(Get-Date -Format o)" | Out-File "$R\logs\launch-r3-main.txt" -Append -Encoding utf8
  Start-Sleep 45
}

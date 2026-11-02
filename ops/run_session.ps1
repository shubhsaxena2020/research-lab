param([Parameter(Mandatory)][ValidateSet('S1','S2','S3')][string]$Session, [int]$BudgetSeconds = 10800)
$map = @{ S1 = @('res-s1','S1-foundations'); S2 = @('res-s2','S2-literature'); S3 = @('res-s3','S3-experiments') }
$profile = $map[$Session][0]; $dir = $map[$Session][1]
Set-Location C:\Users\shubh\research-lab
$stamp = Get-Date -Format 'yyyyMMdd-HHmm'
hermes -p $profile chat -Q --oneshot --yolo --max-turns 700 --run-budget $BudgetSeconds -q "Read and execute C:\Users\shubh\research-lab\sessions\$dir\PROMPT.md exactly. Your working directory is C:\Users\shubh\research-lab." *> "logs\$Session-$stamp.log"

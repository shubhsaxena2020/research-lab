Set-Location C:\Users\shubh\research-lab
$stamp = Get-Date -Format 'yyyyMMdd-HHmm'
hermes -p res-s3 chat -Q --oneshot --yolo --max-turns 700 --run-budget 9000 -q "Read and execute C:\Users\shubh\research-lab\sessions\S3-experiments\PROMPT-S3b.md exactly. Your working directory is C:\Users\shubh\research-lab." *> "logs\S3b-$stamp.log"

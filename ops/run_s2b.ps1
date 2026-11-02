Set-Location C:\Users\shubh\research-lab
$stamp = Get-Date -Format 'yyyyMMdd-HHmm'
hermes -p res-s2 chat -Q --oneshot --yolo --max-turns 500 --run-budget 6000 -q "Read and execute C:\Users\shubh\research-lab\sessions\S2-literature\PROMPT-S2b-novelty-rerun.md exactly. Your working directory is C:\Users\shubh\research-lab." *> "logs\S2b-$stamp.log"

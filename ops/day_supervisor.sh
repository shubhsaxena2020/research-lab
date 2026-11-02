#!/usr/bin/env bash
# Runs for one research day-session (~3h05). Prints only alerts/changes. Never kills anything; touches STOP at the end/stress.
cd /c/Users/shubh/research-lab || exit 1
start=$(date +%s); did1=0; did2=0; did3=0; tick=0
while true; do
  tick=$((tick+1)); now=$(date +%s); el=$(( (now-start)/60 )); msg=""
  free=$(powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB)" 2>/dev/null | tr -d '\r')
  [ -n "$free" ] && [ "$free" -lt 5 ] && { touch STOP; msg="$msg LOW-RAM ${free}GB STOP-created"; }
  alive=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process -Filter \"Name='hermes.exe'\" | ? { \$_.CommandLine -match 'res-s' }).Count" 2>/dev/null | tr -d '\r')
  [ "$el" -ge 60 ]  && [ $did1 -eq 0 ] && { did1=1; powershell -NoProfile -File ops/codex_orchestrate.ps1 -Round 1 >/dev/null 2>&1 & msg="$msg CODEX-ROUND-1-started"; }
  [ "$el" -ge 120 ] && [ $did2 -eq 0 ] && { did2=1; powershell -NoProfile -File ops/codex_orchestrate.ps1 -Round 2 >/dev/null 2>&1 & msg="$msg CODEX-ROUND-2-started"; }
  [ "$el" -ge 170 ] && [ $did3 -eq 0 ] && { did3=1; powershell -NoProfile -File ops/codex_orchestrate.ps1 -Round 3 >/dev/null 2>&1 & msg="$msg CODEX-ROUND-3-started"; }
  [ "$el" -ge 185 ] && { touch STOP; echo "$(date +%H:%M) DAY-SESSION-WINDOW-ENDED (STOP created); hermes res-s procs alive=$alive"; exit 0; }
  [ "$alive" = "0" ] && [ "$el" -gt 5 ] && { echo "$(date +%H:%M) ALL-3-SESSIONS-EXITED after ${el}min"; exit 0; }
  if [ $((tick % 20)) -eq 1 ]; then s=""; for d in S1-foundations S2-literature S3-experiments; do s="$s $(grep -m1 -E '^state:' sessions/$d/STATUS.md | cut -c1-60)"; done; msg="$msg HEARTBEAT t+${el}min free=${free}GB sessions_alive=$alive |$s | files: 00=$(ls 00_foundations 2>/dev/null | wc -l) psit=$(find 01_psit_data -type f 2>/dev/null | wc -l) lit=$(ls 02_literature 2>/dev/null | wc -l) paper=$(find 05_paper 04_experiments -type f 2>/dev/null | wc -l)"; fi
  [ -n "$msg" ] && echo "$(date +%H:%M)$msg"
  sleep 180
done

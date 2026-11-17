#!/bin/bash
# first.sh — closezoom: באותו מקום בתור: צילום של דף הניסוי, czcheck, ואז הבדיקות החוסמות (gate.sh) — על try7882 (הארגומנט נשמר לתאימות)
cd /home/user/tc_root/tc/pkg/work; T=try7882; mkdir -p deliver/2026-11-17/closezoom/qa/$T
echo "lab start $(TZ=Asia/Jerusalem date +%H:%M)"; timeout 300 node deliver/2026-11-17/closezoom/tools/labshot.js deliver/2026-11-17/closezoom/Closezoom_lab.html /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/lab1 > deliver/2026-11-17/closezoom/qa/$T/lab.log 2>&1; echo "lab rc $?"; cut -c1-900 deliver/2026-11-17/closezoom/qa/$T/lab.log
echo "cz start $(TZ=Asia/Jerusalem date +%H:%M)"; bash deliver/2026-11-17/closezoom/tools/gate.sh $T cz; tail -1 deliver/2026-11-17/closezoom/qa/$T/runs.tsv
for w in ingame rules people stuck zc; do bash deliver/2026-11-17/closezoom/tools/gate.sh $T $w; tail -1 deliver/2026-11-17/closezoom/qa/$T/runs.tsv; done
echo "end $(TZ=Asia/Jerusalem date +%H:%M)"

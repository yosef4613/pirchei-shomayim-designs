#!/bin/bash
# all.sh <tryNNNN> [what...] — closezoom: באותו מקום בתור: צילום של דף הניסוי (לבדיקה עצמית), ואז gate.sh על הניסוי (ברירת מחדל: cz czn ingame rules people stuck zc)
cd /home/user/tc_root/tc/pkg/work; T=$1; shift; [ -s deliver/2026-11-17/closezoom/qa/next_try ] && T=$(cat deliver/2026-11-17/closezoom/qa/next_try); W="${*:-cz czn ingame rules people stuck zc}"; mkdir -p deliver/2026-11-17/closezoom/qa/$T
echo "lab $(TZ=Asia/Jerusalem date +%H:%M)"; timeout 300 node deliver/2026-11-17/closezoom/tools/labshot.js deliver/2026-11-17/closezoom/Closezoom_lab.html /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/lab_$T > deliver/2026-11-17/closezoom/qa/$T/lab.log 2>&1; echo "lab rc $?"; cut -c1-600 deliver/2026-11-17/closezoom/qa/$T/lab.log
for w in $W; do bash deliver/2026-11-17/closezoom/tools/gate.sh $T $w; tail -1 deliver/2026-11-17/closezoom/qa/$T/runs.tsv; done
echo "end $(TZ=Asia/Jerusalem date +%H:%M)"

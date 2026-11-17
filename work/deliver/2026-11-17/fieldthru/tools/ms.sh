#!/bin/bash
# ms.sh <from> <to> <order> — חיפוש עם כמה זרעים (סדר / שלב) — הטוב ביותר נבחר אחר כך
SP=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/ms
cd /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/fieldthru/tools
for s in $(seq $1 $2); do FT_SEED=$s FT_SHUF=1 FT_KEEP=${KEEP:-0} timeout 600 python3 ft_gen.py ${WORLD:-sim_base2.json} sim_base019l.json $SP/r$s.json $3 > $SP/r$s.log 2>&1; echo "$s $(tail -1 $SP/r$s.log)"; done

#!/bin/bash
# במקום אחד בתור: הכול על הניסיון ($1), ואחריו יום המשחק על הבסיס ($2 — S7F298 בלי שינוי) להשוואה
D=/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/missions; W=/home/user/tc_root/tc/pkg/work
bash $D/tools/run_all.sh $1
[ -n "$2" ] && { node $D/tools/mb_day.js $W/clean_r2b_025637/out/_try/try$2.html $D/runs/day_$2.json > $D/runs/day_$2.log 2>&1; echo "day rc=$?" >> $D/runs/day_$2.log; }

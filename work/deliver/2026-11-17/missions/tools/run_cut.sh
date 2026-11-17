#!/bin/bash
# במקום אחד בתור: הכרטיס מול סצנה (mb_cut.js) והדף החי (live_check.js). ‎$1 = מספר הניסיון, ‎$2 = הדף החי
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/missions; B=$W/clean_r2b_025637/out/_try/try$1.html; cd $W
node $D/tools/mb_cut.js $B $D/runs/cut_$1 > $D/runs/cut_$1.log 2>&1; echo "cut rc=$?" >> $D/runs/cut_$1.log
node $D/tools/live_check.js $2 $D/runs/live_$1.json > $D/runs/live_$1.log 2>&1; echo "live rc=$?" >> $D/runs/live_$1.log

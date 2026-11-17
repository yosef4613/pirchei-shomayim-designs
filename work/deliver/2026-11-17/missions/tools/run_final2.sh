#!/bin/bash
# במקום אחד בתור: הכול על הניסיון ($1), ואחריו הצילומים לבדיקה בעין (רק לעצמי)
D=/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/missions; W=/home/user/tc_root/tc/pkg/work
bash $D/tools/run_all.sh $1
node $D/tools/mb_shot.js $W/clean_r2b_025637/out/_try/try$1.html $D/runs/shot_$1 > $D/runs/shot_$1.log 2>&1; echo "shot rc=$?" >> $D/runs/shot_$1.log

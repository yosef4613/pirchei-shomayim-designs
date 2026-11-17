#!/bin/bash
# בדיקה מהירה (במקום אחד בתור): הבדיקות של הלוח והסיפור, ואז q_ingame. ‎$1 = מספר הניסיון
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/missions; B=$W/clean_r2b_025637/out/_try/try$1.html; cd $W
node qa_tools/probe_c2.js $B $D/tools/q_mb_smoke.js $D/runs/smoke_$1.json > $D/runs/smoke_$1.log 2>&1; echo "smoke rc=$?" >> $D/runs/smoke_$1.log
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $D/runs/qin_$1.json > $D/runs/qin_$1.log 2>&1; echo "q_ingame rc=$?" >> $D/runs/qin_$1.log

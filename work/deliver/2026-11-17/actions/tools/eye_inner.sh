#!/bin/bash
# מקום אחד: הבדיקה שלי בתוך המשחק + מקצה לקצה + הסריקה בעין (3 תמונות לכל אחת מ-140 הפעולות)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/actions/gate_$T; mkdir -p $O; cd $W
echo "קיבלתי מקום $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/probe_c2.js $B deliver/2026-11-17/actions/tools/q_actions.js $O/actions.json 2>$O/actions.err; echo "actions $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node deliver/2026-11-17/actions/tools/e2e_actions.js $B $O/e2e.json $W/deliver/2026-11-17/actions/shots > $O/e2e.out 2>&1; echo "e2e $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node deliver/2026-11-17/actions/tools/sweep_actions.js $B $W/deliver/2026-11-17/actions/sweep_$T > $O/sweep.out 2>&1; echo "sweep $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
echo "סוף $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt

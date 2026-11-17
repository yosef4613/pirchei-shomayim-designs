#!/bin/bash
# כמו gate_inner2.sh, ועוד בסוף: הסריקה בעין של כל 140 הפעולות (sweep_actions.js — 3 תמונות לשלב, jpeg קטן)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/actions/gate_$T; cd $W
echo "קיבלתי מקום $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/probe_c2.js $B deliver/2026-11-17/actions/tools/q_actions.js $O/actions.json 2>$O/actions.err; echo "actions $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/probe_c2.js $B deliver/2026-11-17/actions/tools/q_actions_busy.js $O/actions_busy.json 2>$O/actions_busy.err; echo "actions_busy $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node deliver/2026-11-17/actions/tools/e2e_actions.js $B $O/e2e.json $W/deliver/2026-11-17/actions/shots > $O/e2e.out 2>&1; echo "e2e $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err; echo "q_ingame $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; echo "people $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; echo "stuck $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node deliver/2026-11-17/actions/tools/sweep_actions.js $B $W/deliver/2026-11-17/actions/sweep_$T > $O/sweep.out 2>&1; echo "sweep $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt

#!/bin/bash
# island5: בתוך מקום אחד בתור — צילומים ושאילתות של מעבר השיט, ואז הסט החוסם: run5.sh tryNNNN [full]
# island5 16:28: המקום בתור של try8371 בודק את try8374 (שלב 1 + 2ג-2ב-2א + תיקון הבדיקות) — run5b
if [ "$1" = try8371 ]; then exec bash /home/user/tc_root/tc/pkg/work/deliver/2026-11-17/island/tools5/run5c.sh try8375 try8374; fi
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; mkdir -p $O; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
bash deliver/2026-11-17/island/tools5/shots.sh $TRY > $O/shots.out 2>&1; L "shots rc=$?"; cp /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl5/s_$TRY/*.json $O/ 2>/dev/null
if [ "$2" = full ]; then
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
fi
L "סוף"

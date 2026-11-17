#!/bin/bash
# מקום אחד בתור: try$1 — היבשה של E9 (q_e9) + השאילתות של האי + צילומים של E9, ואז הסט החוסם
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl/shots_$TRY; mkdir -p $O $SH; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
(cd deliver/2026-11-17/island/tools && node page_shot.js ../Island_D694_plan.html $SH/plan.jpg 1400 1) > /dev/null 2>&1; L "plan shot rc=$?"
(cd deliver/2026-11-17/island/tools && QMAX=9000 node isl_shot.js $B $SH --wait 20000 --q q_e9.js --q q_pole.js --q q_il.js --q q_east.js --q q_isl2.js --q q_freight.js "e9:5450,7350,0.55" "e9b:5600,7600,1.1" "e9n:5450,7350,0.55,1" "chan:5900,7300,0.8") > $O/q_e9.out 2>&1; L "q_e9 rc=$?"
[ "$2" = quick ] && { L "סוף (מהיר)"; exit 0; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
(cd deliver/2026-11-17/island/tools && node l5a_run.js $B $O/l5a_run.json 300 20) > $O/l5a_run.out 2>&1; L "l5a_run(300) rc=$?"
L "סוף"

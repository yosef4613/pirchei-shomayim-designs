#!/bin/bash
# מקום אחד בתור: השאילתות של האי + הסט החוסם לניסיון אחד ($1)
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl/shots_$TRY; mkdir -p $O $SH; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
(cd deliver/2026-11-17/island/tools && QMAX=8000 node isl_shot.js $B $SH --q q_east.js --q q_isl.js --q q_isl2.js --q q_train.js --q q_freight.js "park:9100,6720,1.1" "light:8760,6740,1.2") > $O/q_east.out 2>&1; L "q_east rc=$?"
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
L "סוף"

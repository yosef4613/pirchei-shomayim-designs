#!/bin/bash
# הבדיקות של הניסיון ברצף, בתוך מקום אחד בתור (run_suite.sh קורא לו דרך bslot.sh): השאילתות של האי והרכבת, ואז הבדיקות החוסמות (BRIEF_COMMON סעיף 5). דפדפן אחד בכל רגע.
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl/shots_$TRY; mkdir -p $O $SH; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
(cd deliver/2026-11-17/island/tools && QMAX=6000 node isl_shot.js $B $SH --q q_isl.js --q q_isl2.js --q q_train.js "h8:9000,6700,0.55" "cable:7650,7450,0.42" "port:5900,4700,0.8" "isl_st:8840,7260,0.6") > $O/q_isl.out 2>&1; L "q_isl rc=$?"
[ "$2" = quick ] && { L "סוף (מהיר)"; exit 0; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
L "סוף"

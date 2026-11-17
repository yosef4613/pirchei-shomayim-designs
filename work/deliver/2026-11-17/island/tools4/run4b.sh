#!/bin/bash
# island4: הרצה ישירה (בלי cur_try): try$1 — השאילתה + צילומים, ואז הסט החוסם
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl4/shots_$TRY; mkdir -p $O $SH; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
(cd deliver/2026-11-17/island/tools && QMAX=12000 SHOT_WAIT=1500 node isl_shot.js $B $SH --wait 25000 --q ../tools4/q_e9r.js --q q_e9.js "term:5470,7090,1.6" "termn:5470,7090,1.6,1" "plaza:6900,7330,1.0") > $O/q_e9r.out 2>&1; L "q_e9r rc=$?"
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
(cd deliver/2026-11-17/island/tools && QMAX=9000 node isl_shot.js $B $SH --wait 15000 --q ../tools4/q_fy.js "fyafter:5470,7060,1.2") > $O/q_fy.out 2>&1; L "q_fy rc=$?"
L "סוף"
# island4 14:21 — המשך באותו מקום בתור: המועמד try8007 (2ג-2א + ב-1)
if [ "$TRY" = try8004 ]; then TRY=try8007; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl4/shots_$TRY; mkdir -p $O $SH
L "התחלה (המשך של try8004)"
(cd deliver/2026-11-17/island/tools && QMAX=12000 SHOT_WAIT=1500 node isl_shot.js $B $SH --wait 25000 --q ../tools4/q_e9r.js --q q_e9.js "term:5470,7090,1.6" "hotel:6100,7400,0.9" "termn:5470,7090,1.6,1") > $O/q_e9r.out 2>&1; L "q_e9r rc=$?"
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
(cd deliver/2026-11-17/island/tools && QMAX=9000 node isl_shot.js $B $SH --wait 15000 --q ../tools4/q_fy.js "fyafter:5470,7060,1.2") > $O/q_fy.out 2>&1; L "q_fy rc=$?"
L "סוף"
fi

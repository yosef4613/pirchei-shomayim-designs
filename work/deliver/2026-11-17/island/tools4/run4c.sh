#!/bin/bash
# island4: try$1 — היציאה של "צוק הים" ב-L2 (q_ship + q_e9r + צילומים), הבדיקות של sealife (sl_ship, sl_tugs), ואז הסט החוסם
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl4/shots_$TRY; S=deliver/2026-11-17/sealife; mkdir -p $O $SH $O/shots; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
(cd deliver/2026-11-17/island/tools && QMAX=6000 SHOT_WAIT=1500 node isl_shot.js $B $SH --wait 25000 --q ../tools4/q_ship.js --q ../tools4/q_e9r.js "d8:4250,6990,0.45" "hotel:6100,7400,0.9") > $O/q_ship.out 2>&1; L "q_ship rc=$?"
timeout 900 node $S/tools/sl_ship.js $B $O/sl_ship.json > $O/sl_ship.out 2>&1; L "sl_ship rc=$?"
timeout 2400 node $S/tools/sl_tugs.js $B $O/sl_tugs.json 6000 $O/shots > $O/sl_tugs.out 2>&1; L "sl_tugs rc=$?"
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
L "סוף"
# island4 15:15 — המשך באותו מקום בתור: try8010 (התיקון של היציאה ב-L2); sl_ship / sl_tugs — מ-try8009 (הגוררות של sealife לא השתנו)
if [ "$TRY" = try8009 ]; then TRY=try8010; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl4/shots_$TRY; mkdir -p $O $SH
L "התחלה (המשך של try8009)"
(cd deliver/2026-11-17/island/tools && QMAX=3000 SHOT_WAIT=1500 node isl_shot.js $B $SH --wait 25000 --q ../tools4/q_ship.js --q ../tools4/q_e9r.js "d8:4250,6990,0.45") > $O/q_ship.out 2>&1; L "q_ship rc=$?"
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
L "סוף"
fi

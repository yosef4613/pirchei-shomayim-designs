#!/bin/bash
# island5: מקום אחד בתור — מעבר השיט (F6) והמרינה (½ D9): צילומים ושאילתות, ואז הסט החוסם: run5b.sh tryNNNN [full]
W=/home/user/tc_root/tc/pkg/work; TRY=$1; B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl5/s_$TRY; mkdir -p $O $SH; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
(cd deliver/2026-11-17/island/tools && QMAX=8000 SHOT_WAIT=1800 node isl_shot.js $B $SH --wait 9000 --q ../tools5/q_f6new.js --q ../tools5/q_marina.js "a:7000,5110,0.9" "b:7000,5110,0.45" "z:7000,5160,1.6" "n:7000,5110,0.9,1" "m:4600,7540,0.8" "m2:4600,7300,0.35" "mn:4600,7540,0.8,1" "c:6000,7150,0.5") > $O/shots.out 2>&1; L "shots rc=$?"
cp $SH/*.json $O/ 2>/dev/null
if [ "$2" = full ]; then
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
fi
L "סוף"

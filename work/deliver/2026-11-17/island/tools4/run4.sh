#!/bin/bash
# island4: מקום אחד בתור — try$1: השאילתה של הדרך אל E9 + צילומים (לעצמי); עם full — גם הסט החוסם
W=/home/user/tc_root/tc/pkg/work; TRY=$1; [ -f $W/deliver/2026-11-17/island/tools4/cur_try.txt ] && TRY=$(cat $W/deliver/2026-11-17/island/tools4/cur_try.txt); B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl4/shots_$TRY; mkdir -p $O $SH; cd $W
L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
L "התחלה (במקום בתור)"
(cd deliver/2026-11-17/island/tools && QMAX=12000 SHOT_WAIT=1500 node isl_shot.js $B $SH --wait 25000 --q ../tools4/q_e9r.js "e9:5420,7250,0.55" "term:5470,7090,1.6" "fill:6100,7520,0.9" "arena:5560,7380,1.2" "e9n:5420,7250,0.55,1") > $O/q_e9r.out 2>&1; L "q_e9r rc=$?"
[ "$2" = full ] || [ -f $W/deliver/2026-11-17/island/tools4/go_full.txt ] || { L "סוף (מהיר)"; exit 0; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
L "סוף"

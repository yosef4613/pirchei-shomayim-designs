#!/bin/bash
# island5: מקום אחד בתור — צילומים ושאילתות לניסיון הראשון ברשימה; אם אין שגיאות בדף והבדיקות של האי עוברות בשאילתה — הסט החוסם עליו, ואם לא — על הבא ברשימה
# run5c.sh tryA tryB ...
W=/home/user/tc_root/tc/pkg/work; cd $W
for TRY in "$@"; do
 B=$W/clean_r2b_025637/out/_try/$TRY.html; O=$W/deliver/2026-11-17/island/qa/$TRY; SH=/tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl5/s_$TRY; mkdir -p $O $SH
 L(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/log.txt; }
 L "התחלה (במקום בתור)"
 (cd deliver/2026-11-17/island/tools && QMAX=8000 SHOT_WAIT=1800 node isl_shot.js $B $SH --wait 9000 --q ../tools5/q_f6new.js --q ../tools5/q_marina.js "a:7000,5110,0.9" "b:7000,5110,0.45" "z:7000,5160,1.6" "n:7000,5110,0.9,1" "m:4600,7540,0.8" "m2:4600,7300,0.35" "mn:4600,7540,0.8,1" "c:6200,7230,0.5" "c2:5700,7230,0.8") > $O/shots.out 2>&1; L "shots rc=$?"
 cp $SH/*.json $O/ 2>/dev/null
 node deliver/2026-11-17/island/tools/page_shot.js /tmp/claude-0/-home-user-pirchei-shomayim-designs/59afe673-6e42-5712-9b20-6bf3463c6a6d/scratchpad/isl5/plan_check.html $SH/plan_check.jpg 1600 1 >/dev/null 2>&1
 if grep -q "שגיאות דף 0" $O/shots.out && python3 -c "import json,sys;d=json.load(open('$O/q_marina.json'));r=d.get('road',{});bad=[b for b in r.get('bad',[]) if b.split(':')[0] in ('isl17_e9_road','isl17_e9_land','edge_count','node_count','h8_rig_f6_span_s10b')];sys.exit(1 if bad else 0)" 2>/dev/null; then L "נבחר — הסט החוסם"; GO=$TRY; break; else L "לא נבחר (שגיאות בדף / בדיקות האי) — הבא ברשימה"; fi
done
[ -z "$GO" ] && { L "אין ניסיון שעבר את השאילתה"; exit 1; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.out 2>&1; L "q_ingame rc=$?"
node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; L "rules_gate rc=$?"
node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.out 2>&1; L "people_on_road rc=$?"
node qa_tools/stuckmax.js $B 150 isl_$TRY > $O/stuckmax.out 2>&1; L "stuckmax rc=$?"
L "סוף"

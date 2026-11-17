#!/bin/bash
# מקום אחד בתור לשני מועמדים: קודם הבדיקות של הפעולות על החדש (A); אם עברו — כל הסט החוסם עליו, אחרת — כל הסט על הקודם (B).
# שימוש: bash gate_combo.sh tryA tryB      (רץ בתוך bslot)
W=/home/user/tc_root/tc/pkg/work; cd $W; A=$1; B=$2; L=$W/deliver/2026-11-17/actions/gate_combo_$A.log
echo "קיבלתי מקום $(TZ=Asia/Jerusalem date +%H:%M)" >> $L
one(){ T=$1; O=$W/deliver/2026-11-17/actions/gate_$T; mkdir -p $O; BH=$W/clean_r2b_025637/out/_try/$T.html
  node qa_tools/probe_c2.js $BH deliver/2026-11-17/actions/tools/q_actions.js $O/actions.json 2>$O/actions.err; echo "$T actions $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $L
  node deliver/2026-11-17/actions/tools/e2e_actions.js $BH $O/e2e.json $W/deliver/2026-11-17/actions/shots > $O/e2e.out 2>&1; echo "$T e2e $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $L
  python3 -c "
import json,sys
a=json.load(open('$O/actions.json'));a=a.get('result',a) if isinstance(a,dict) else a
e=json.load(open('$O/e2e.json'))
ok=bool((a.get('ok') if isinstance(a,dict) else False) and e.get('ok'))
sys.exit(0 if ok else 1)" 2>>$L; }
rest(){ T=$1; O=$W/deliver/2026-11-17/actions/gate_$T; BH=$W/clean_r2b_025637/out/_try/$T.html
  node qa_tools/probe_c2.js $BH qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err; echo "$T q_ingame $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $L
  node qa_tools/rules_gate.js $BH $O/rules.json > $O/rules.out 2>&1; echo "$T rules $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $L
  node qa_tools/people_on_road.js $BH $O/people.json > $O/people.out 2>&1; echo "$T people $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $L
  node qa_tools/stuckmax.js $BH 150 $T > $O/stuck.out 2>&1; echo "$T stuck $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $L; }
if one $A; then echo "$A — הפעולות עברו; כל הסט על $A" >> $L; rest $A; else echo "$A — הפעולות לא עברו; כל הסט על $B" >> $L; one $B; rest $B; fi
echo "סוף $(TZ=Asia/Jerusalem date +%H:%M)" >> $L

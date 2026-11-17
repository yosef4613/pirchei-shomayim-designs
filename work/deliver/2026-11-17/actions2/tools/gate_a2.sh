#!/bin/bash
# actions2: כל הסט במקום אחד בתור — הבדיקה שלי, מקצה לקצה, q_ingame, rules_gate, people_on_road, stuckmax 150
W=/home/user/tc_root/tc/pkg/work; T=$1; N=$W/deliver/2026-11-17/actions2/gate_next; [ -s $N ] && T=$(cat $N) && : > $N;   # הניסיון האחרון שנבנה בזמן ההמתנה בתור
 B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/actions2/gate_$T; mkdir -p $O; cd $W
echo "קיבלתי מקום $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/probe_c2.js $B deliver/2026-11-17/actions2/tools/q_actions2.js $O/actions2.json 2>$O/actions2.err; echo "actions2 $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node deliver/2026-11-17/actions2/tools/e2e_actions2.js $B $O/e2e.json $W/deliver/2026-11-17/actions2/shots > $O/e2e.out 2>&1; echo "e2e $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
[ "$2" = "mine" ] && exit 0
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err; echo "q_ingame $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; echo "people $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; echo "stuck $? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt
echo "סוף $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/log.txt

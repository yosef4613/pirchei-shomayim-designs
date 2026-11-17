#!/bin/bash
# הבדיקות החוסמות (במקום אחד בתור, אחת אחרי השנייה): הכללים, אנשים בכביש, stuckmax 150, ויום המשחק של הלוח. ‎$1 = מספר הניסיון; ‎$2=skipday — בלי יום המשחק
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/missions; B=$W/clean_r2b_025637/out/_try/try$1.html; cd $W
node qa_tools/rules_gate.js $B $D/runs/rules_$1.json > $D/runs/rules_$1.log 2>&1; echo "rules rc=$?" >> $D/runs/rules_$1.log
node qa_tools/people_on_road.js $B $D/runs/por_$1.json > $D/runs/por_$1.log 2>&1; echo "people rc=$?" >> $D/runs/por_$1.log
node qa_tools/stuckmax.js $B 150 try$1 > $D/runs/stuck_$1.json 2> $D/runs/stuck_$1.log; echo "stuck rc=$?" >> $D/runs/stuck_$1.log
[ "$2" = skipday ] || { node $D/tools/mb_day.js $B $D/runs/day_$1.json > $D/runs/day_$1.log 2>&1; echo "day rc=$?" >> $D/runs/day_$1.log; }

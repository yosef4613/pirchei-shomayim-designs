#!/bin/bash
# story2 (17.11): הכול במקום אחד בתור — הבדיקה המהירה (q_s2: המפה שלי, הלוח, הסיפור); נכשלת → עוצרים; אחרת q_ingame, הכללים, אנשים בכביש, stuckmax 150, יום המשחק (s2_day).
# ‎$1 = מספר הניסיון (הבנייה: clean_r2b_025637/out/_try/try$1.html). שימוש: bash W/tools_pack/bslot.sh bash run_all.sh 7601
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/story2; B=$W/clean_r2b_025637/out/_try/try$1.html; R=$D/runs; cd $W
node $D/tools/q_s2.js $B $R/q_s2_$1.json shots > $R/q_s2_$1.log 2>&1; echo "q_s2 rc=$?" >> $R/q_s2_$1.log
python3 -c "import json,sys;d=json.load(open('$R/q_s2_$1.json'));sys.exit(0 if d.get('ok') else 3)" || { echo "stop: q_s2" >> $R/q_s2_$1.log; exit 3; }
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $R/qin_$1.json > $R/qin_$1.log 2>&1; echo "q_ingame rc=$?" >> $R/qin_$1.log
node qa_tools/rules_gate.js $B $R/rules_$1.json > $R/rules_$1.log 2>&1; echo "rules rc=$?" >> $R/rules_$1.log
node qa_tools/people_on_road.js $B $R/por_$1.json > $R/por_$1.log 2>&1; echo "people rc=$?" >> $R/por_$1.log
node qa_tools/stuckmax.js $B 150 try$1 > $R/stuck_$1.json 2> $R/stuck_$1.log; echo "stuck rc=$?" >> $R/stuck_$1.log
node $D/tools/s2_day.js $B $R/day_$1.json > $R/day_$1.log 2>&1; echo "day rc=$?" >> $R/day_$1.log
echo "done $1" >> $R/all_$1.log

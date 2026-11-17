#!/bin/bash
# story2: החלק השני של הסט (אנשים בכביש, stuckmax 150, יום המשחק) — במקום אחד בתור. ‎$1 = מספר הניסיון
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/story2; B=$W/clean_r2b_025637/out/_try/try$1.html; R=$D/runs; cd $W
node qa_tools/people_on_road.js $B $R/por_$1.json > $R/por_$1.log 2>&1; echo "people rc=$?" >> $R/por_$1.log
node qa_tools/stuckmax.js $B 150 try$1 > $R/stuck_$1.json 2> $R/stuck_$1.log; echo "stuck rc=$?" >> $R/stuck_$1.log
node $D/tools/s2_day.js $B $R/day_$1.json > $R/day_$1.log 2>&1; echo "day rc=$?" >> $R/day_$1.log
echo "done $1" >> $R/all_$1.log

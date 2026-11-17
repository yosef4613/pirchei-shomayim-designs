#!/bin/bash
# gates.sh <tryNNNN> — story56: הבדיקות החוסמות (BRIEF_COMMON §5) + הבדיקה של הסעיף (הסיפור כולו מההתחלה עד הסוף), אחת אחרי השנייה דרך התור (כלל 18)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/story56/qa/$T; mkdir -p $O; cd $W; : > $O/summary.txt
run(){ local n=$1; shift; bash tools_pack/bslot.sh "$@" > $O/$n.log 2>&1; echo "$n rc=$?" >> $O/summary.txt; }
run story_full env MAXSEC=2400 node deliver/2026-11-17/story56/tools/story_full56.js $B $O/story_full.json
run q_ingame node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json
run rules node qa_tools/rules_gate.js $B $O/rules.json
run stuckmax node qa_tools/stuckmax.js $B 150 s56_$T
run people node qa_tools/people_on_road.js $B $O/people.json
run q_s56 node qa_tools/probe_c2.js $B deliver/2026-11-17/story56/tools/q_s56.js $O/q_s56.json
grep -c 'data:image' $B >> $O/summary.txt
echo ALLDONE >> $O/summary.txt

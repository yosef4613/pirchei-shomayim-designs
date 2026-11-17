#!/bin/bash
# gates.sh <tryNNNN> — הבדיקות החוסמות (BRIEF_COMMON §5), אחת אחרי השנייה דרך התור (כלל 18)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/locks/qa/$T; mkdir -p $O; cd $W
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B deliver/2026-11-17/locks/qa/q_locks.js $O/q_locks.json > $O/q_locks.log 2>&1; echo "q_locks rc=$?" >> $O/summary.txt
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.log 2>&1; echo "q_ingame rc=$?" >> $O/summary.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; echo "rules rc=$?" >> $O/summary.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 locks_$T > $O/stuckmax.log 2>&1; echo "stuckmax rc=$?" >> $O/summary.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; echo "people rc=$?" >> $O/summary.txt
echo ALLDONE >> $O/summary.txt

#!/bin/bash
# mapfix: הבדיקות החוסמות על ניסיון אחד — gates.sh tryNNNN
T=$1; W=/home/user/tc_root/tc/pkg/work; B=$W/clean_r2b_025637/out/_try/$T.html; O=/home/user/tc_root/tc/pkg/work/deliver/2026-11-17/mapfix/qa/$T; mkdir -p $O; cd $W
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.log 2>&1; echo "q_ingame rc=$?" >> $O/summary.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; echo "rules rc=$?" >> $O/summary.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; echo "people rc=$?" >> $O/summary.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T > $O/stuck.json 2> $O/stuck.err; echo "stuck rc=$?" >> $O/summary.txt
echo done >> $O/summary.txt

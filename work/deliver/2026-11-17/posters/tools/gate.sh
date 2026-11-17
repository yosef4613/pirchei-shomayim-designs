#!/bin/bash
# הבדיקות החוסמות על ניסיון אחד: gate.sh <tryNNNN>
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/posters/qa/$T; mkdir -p $O; cd $W
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B deliver/2026-11-17/posters/tools/q_icon.js $O/icon.json 2>$O/icon.err
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2>$O/q_ingame.err
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json >$O/rules.out 2>&1
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json >$O/people.out 2>&1
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T >$O/stuck.out 2>&1
echo DONE > $O/done

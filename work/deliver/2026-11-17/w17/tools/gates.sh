#!/bin/bash
# הבדיקות החוסמות בתור אחד: bash bslot.sh bash gates.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/w17/qa/$T; mkdir -p $O; cd $W
L=$O/gates.log; echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $L
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json > $O/ingame.out 2> $O/ingame.err; echo "ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/stuckmax.js $B 150 $T > $O/stuck.json 2> $O/stuck.err; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/people_on_road.js $B $O/por.json > $O/por.out 2>&1; echo "por rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
echo "data:image $(grep -c 'data:image' $B)" >> $L
echo ALLDONE >> $L

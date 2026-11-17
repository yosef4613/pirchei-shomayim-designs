#!/bin/bash
# gates5.sh <try> — buses (17.11 16:50): רק הבדיקות החוסמות (המכסה — מצמצמים).
W=/home/user/tc_root/tc/pkg/work; T=$1; D=$W/deliver/2026-11-17/buses; Q=$D/qa; cd $W
B=$W/clean_r2b_025637/out/_try/$T.html; G=$Q/${T}_gate.txt
r(){ local name=$1; shift; local t0=$(date +%s); timeout 2400 "$@"; echo "$name rc=$? $(( $(date +%s)-t0 ))s $(TZ=Asia/Jerusalem date +%H:%M)" >> $G; }
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
r ingame node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/${T}_ingame.json > $Q/${T}_ingame.log 2>&1
r rules node qa_tools/rules_gate.js $B $Q/${T}_rules.json > $Q/${T}_rules.log 2>&1
r stuck150 node qa_tools/stuckmax.js $B 150 $T > $Q/${T}_stuck150.json 2>&1
r people node qa_tools/people_on_road.js $B $Q/${T}_people.json > $Q/${T}_people.log 2>&1
echo "chain-done $(TZ=Asia/Jerusalem date +%H:%M)" >> $G

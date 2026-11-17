#!/bin/bash
# הבדיקות החוסמות של ניסיון אחד (כל דפדפן דרך התור): bash gates.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/cutscenes/qa/$T; mkdir -p $O
cd $W
echo "== q_ingame $(TZ=Asia/Jerusalem date +%H:%M)"; bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json > $O/ingame.log 2>&1; echo rc=$?
echo "== rules $(TZ=Asia/Jerusalem date +%H:%M)"; bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; echo rc=$?
echo "== people $(TZ=Asia/Jerusalem date +%H:%M)"; bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; echo rc=$?
echo "== stuck $(TZ=Asia/Jerusalem date +%H:%M)"; bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T > $O/stuck.log 2>&1; echo rc=$?
echo "== done $(TZ=Asia/Jerusalem date +%H:%M)"

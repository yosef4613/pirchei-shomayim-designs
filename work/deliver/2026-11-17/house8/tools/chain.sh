#!/bin/bash
# chain.sh <tryNNNN> — כל הבדיקות של house8 על ניסיון אחד, בזו אחר זו, במקום אחד בתור (bslot).
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/house8/qa/$T; mkdir -p $O; cd $W
echo "== h8_q $(TZ=Asia/Jerusalem date +%H:%M)"; node deliver/2026-11-17/house8/tools/h8_q.js $B $O/h8_q.json; echo "rc=$?"
echo "== q_ingame $(TZ=Asia/Jerusalem date +%H:%M)"; node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json > $O/q_ingame.log 2>&1; echo "rc=$?"; tail -c 600 $O/q_ingame.log
echo "== rules_gate $(TZ=Asia/Jerusalem date +%H:%M)"; node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.log 2>&1; echo "rc=$?"; tail -c 600 $O/rules_gate.log
echo "== people_on_road $(TZ=Asia/Jerusalem date +%H:%M)"; node qa_tools/people_on_road.js $B $O/people_on_road.json > $O/people_on_road.log 2>&1; echo "rc=$?"; tail -c 400 $O/people_on_road.log
echo "== stuckmax 150 $(TZ=Asia/Jerusalem date +%H:%M)"; node qa_tools/stuckmax.js $B 150 h8_$T > $O/stuckmax.log 2>&1; echo "rc=$?"; tail -c 600 $O/stuckmax.log
echo "== shots $(TZ=Asia/Jerusalem date +%H:%M)"; node deliver/2026-11-17/house8/tools/h8_shots.js $B $O/shots 1.0 7-8 > $O/shots.log 2>&1; echo "rc=$?"; tail -c 300 $O/shots.log
echo "== done $(TZ=Asia/Jerusalem date +%H:%M)"

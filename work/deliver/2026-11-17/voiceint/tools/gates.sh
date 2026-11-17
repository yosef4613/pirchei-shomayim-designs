#!/bin/bash
# הבדיקות החוסמות (BRIEF_COMMON 5) לניסיון אחד, דרך התור: gates.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; Q=$W/deliver/2026-11-17/voiceint/qa/$T; mkdir -p $Q; cd $W
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame.json > $Q/q_ingame.log 2>&1; echo "q_ingame $?"
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $Q/rules.json > $Q/rules.log 2>&1; echo "rules $?"
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $Q/people.json > $Q/people.log 2>&1; echo "people $?"
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 voiceint_$T > $Q/stuck.log 2>&1; echo "stuck $?"
echo "סוף $(TZ=Asia/Jerusalem date +%H:%M)"

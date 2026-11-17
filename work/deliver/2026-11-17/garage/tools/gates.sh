#!/bin/bash
# הבדיקות החוסמות (garage, 17.11) על ניסיון אחד, אחת אחרי השנייה, דרך התור
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/garage/qa/$T; mkdir -p $O; cd $W
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" > $O/gates.log
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_ingame.json 2> $O/q_ingame.err; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules_gate.json > $O/rules_gate.out 2>&1; echo "rules_gate rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json > $O/people.out 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T > $O/stuck.out 2>&1; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M)" >> $O/gates.log
echo done >> $O/gates.log

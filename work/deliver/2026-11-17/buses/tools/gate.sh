#!/bin/bash
# gate.sh <tryNNNN> — הבדיקות החוסמות (BRIEF_COMMON 5) אחת אחרי השנייה, כל אחת דרך התור. התוצאות: deliver/2026-11-17/buses/qa/<try>_*.json
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; Q=$W/deliver/2026-11-17/buses/qa; cd $W
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/${T}_ingame.json > $Q/${T}_ingame.log 2>&1; echo "ingame rc=$?" >> $Q/${T}_gate.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $Q/${T}_rules.json > $Q/${T}_rules.log 2>&1; echo "rules rc=$?" >> $Q/${T}_gate.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 $T > $Q/${T}_stuck150.json 2>&1; echo "stuck150 rc=$?" >> $Q/${T}_gate.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $Q/${T}_people.json > $Q/${T}_people.log 2>&1; echo "people rc=$?" >> $Q/${T}_gate.txt
echo done >> $Q/${T}_gate.txt

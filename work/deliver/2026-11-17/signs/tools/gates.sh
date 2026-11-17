#!/bin/bash
# gates.sh <build> <tag> — הבדיקות החוסמות (BRIEF_COMMON 5), אחת אחרי השנייה, כל אחת דרך התור
cd /home/user/tc_root/tc/pkg/work; B=$1; t=$2; O=deliver/2026-11-17/signs/out
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_$t.json > $O/q_$t.log 2>&1; echo "q_ingame rc=$?" >> $O/gates_$t.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules_$t.json > $O/rules_$t.log 2>&1; echo "rules_gate rc=$?" >> $O/gates_$t.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people_$t.json > $O/people_$t.log 2>&1; echo "people_on_road rc=$?" >> $O/gates_$t.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 s12_$t > $O/stuck_$t.log 2>&1; echo "stuckmax rc=$?" >> $O/gates_$t.txt
bash tools_pack/bslot.sh node qa_tools/rule30_gate.js $B $O/rule30_$t.json > $O/rule30_$t.log 2>&1; echo "rule30_gate rc=$?" >> $O/gates_$t.txt
echo DONE >> $O/gates_$t.txt

#!/bin/bash
# gates2.sh <build> <tag> — הבדיקות החוסמות בשתי שרשראות במקביל (כל הרצה דרך התור)
cd /home/user/tc_root/tc/pkg/work; B=$1; t=$2; O=deliver/2026-11-17/signs/out; G=$O/gates_$t.txt; : > $G
( bash tools_pack/bslot.sh node deliver/2026-11-17/signs/tools/signs12_kiosk.js $B $O/kiosk_$t.json $O/kiosk_$t > $O/kiosk_$t.log 2>&1; echo "signs12_kiosk rc=$?" >> $G
  bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/q_$t.json > $O/q_$t.log 2>&1; echo "q_ingame rc=$?" >> $G
  bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 s12_$t > $O/stuck_$t.log 2>&1; echo "stuckmax rc=$?" >> $G
  bash tools_pack/bslot.sh node deliver/2026-11-17/signs/tools/signs12_probe.js $B $O/probe_$t.json deliver/2026-11-17/signs/tools/review_ids.json > $O/probe_$t.log 2>&1; echo "signs12_probe rc=$?" >> $G ) &
( bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules_$t.json > $O/rules_$t.log 2>&1; echo "rules_gate rc=$?" >> $G
  bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people_$t.json > $O/people_$t.log 2>&1; echo "people_on_road rc=$?" >> $G
  bash tools_pack/bslot.sh node qa_tools/rule30_gate.js $B $O/rule30_$t.json > $O/rule30_$t.log 2>&1; echo "rule30_gate rc=$?" >> $G ) &
wait; echo DONE >> $G

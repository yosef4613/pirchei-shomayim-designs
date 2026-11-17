#!/bin/bash
# gates.sh <tryNNNN> — airlogos: הבדיקות החוסמות על ניסיון (כל אחת דרך התור), הפלטים ב-out/
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/airlogos/out; cd $W
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/qin_$T.json > $O/qin_$T.log 2>&1; echo "q_ingame rc=$?" >> $O/gates_$T.txt
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules_$T.json > $O/rules_$T.log 2>&1; echo "rules_gate rc=$?" >> $O/gates_$T.txt
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/por_$T.json > $O/por_$T.log 2>&1; echo "people_on_road rc=$?" >> $O/gates_$T.txt
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 al_$T > $O/stuck_$T.log 2>&1; echo "stuckmax rc=$?" >> $O/gates_$T.txt
echo done >> $O/gates_$T.txt

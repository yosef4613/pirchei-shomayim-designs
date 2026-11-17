#!/bin/bash
# all.sh <tryNNNN> — airlogos: כל הבדיקות ברצף בתוך מקום אחד בתור (bash W/tools_pack/bslot.sh bash all.sh tryNNNN)
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/airlogos/out; cd $W; : > $O/all_$T.txt
node deliver/2026-11-17/airlogos/tools/airlogos_probe.js $B $O/probe_$T.json $O/shots_$T > $O/probe_$T.log 2>&1; echo "airlogos_probe rc=$? $(tail -c 600 $O/probe_$T.log)" >> $O/all_$T.txt
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/qin_$T.json > $O/qin_$T.log 2>&1; echo "q_ingame rc=$?" >> $O/all_$T.txt
node qa_tools/rules_gate.js $B $O/rules_$T.json > $O/rules_$T.log 2>&1; echo "rules_gate rc=$?" >> $O/all_$T.txt
node qa_tools/people_on_road.js $B $O/por_$T.json > $O/por_$T.log 2>&1; echo "people_on_road rc=$?" >> $O/all_$T.txt
node qa_tools/stuckmax.js $B 150 al_$T > $O/stuck_$T.log 2>&1; echo "stuckmax rc=$? $(tail -c 300 $O/stuck_$T.log)" >> $O/all_$T.txt
echo done >> $O/all_$T.txt

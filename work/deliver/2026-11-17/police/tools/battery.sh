#!/bin/bash
# הבדיקות החוסמות של police, בזו אחר זו דרך התור: battery.sh <tryNNNN> [רשימה]
W=/home/user/tc_root/tc/pkg/work; T=$1; G=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/police/qa/$T; mkdir -p $O
Q=$W/qa_tools; M=$W/deliver/2026-11-17/police/tools
L=${2:-"ingame rules stuck road police"}
for k in $L; do s=$(date +%s); case $k in
 ingame) bash $W/tools_pack/bslot.sh timeout 1500 node $Q/probe_c2.js $G $Q/q_ingame.js $O/ingame.json > $O/ingame.log 2>&1;;
 rules)  bash $W/tools_pack/bslot.sh timeout 1500 node $Q/rules_gate.js $G $O/rules.json > $O/rules.log 2>&1;;
 stuck)  (cd $O && bash $W/tools_pack/bslot.sh timeout 2400 node $Q/stuckmax.js $G 150 police_$T > $O/stuck.log 2>&1);;
 road)   bash $W/tools_pack/bslot.sh timeout 1500 node $Q/people_on_road.js $G $O/road.json > $O/road.log 2>&1;;
 police) bash $W/tools_pack/bslot.sh timeout 2400 node $Q/probe_c2.js $G $M/q_police.js $O/police.json > $O/police.log 2>&1;;
 *) [ -f $M/q_$k.js ] && bash $W/tools_pack/bslot.sh timeout 2400 node $Q/probe_c2.js $G $M/q_$k.js $O/$k.json > $O/$k.log 2>&1;;
 esac; echo "$k rc=$? $(( $(date +%s)-s ))s" >> $O/done.txt; done
echo ALL >> $O/done.txt

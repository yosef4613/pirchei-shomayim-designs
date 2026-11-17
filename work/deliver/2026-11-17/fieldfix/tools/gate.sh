#!/bin/bash
# gate.sh <tryNNNN> — fieldfix: הבדיקות החוסמות, אחת אחרי השנייה דרך התור (דפדפן אחד בכל פעם)
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/fieldfix; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$D/qa/$T; mkdir -p $O; cd $W
echo "data:image $(grep -c 'data:image' $B) · <img $(grep -o '<img' $B | wc -l)" > $O/static.txt
st(){ echo "$1 $(TZ=Asia/Jerusalem date +%H:%M:%S) rc=$2" >> $O/runs.tsv; }
bash tools_pack/bslot.sh node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json > $O/ingame.log 2>&1; st ingame $?
bash tools_pack/bslot.sh node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; st rules $?
bash tools_pack/bslot.sh node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; st people $?
bash tools_pack/bslot.sh node qa_tools/stuckmax.js $B 150 ff_$T > $O/stuck.log 2>&1; st stuck $?
bash tools_pack/bslot.sh node deliver/2026-11-10/s15e/tools/q_airfield.js $B $O/airfield --only plane,veh,overlap --tag $T > $O/airfield.log 2>&1; st airfield $?
echo done >> $O/runs.tsv

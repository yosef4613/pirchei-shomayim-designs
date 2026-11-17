#!/bin/bash
# gate3.sh <tryNNNN> — fieldthru2: הסט החוסם במקום אחד בתור (qa/next3.txt גובר): q_ingame, המדידה, ‏rules_gate, ‏people_on_road, ‏stuckmax 150
W=/home/user/tc_root/tc/pkg/work; T=$1; [ -f $W/deliver/2026-11-17/fieldthru2/qa/next3.txt ] && T=$(cat $W/deliver/2026-11-17/fieldthru2/qa/next3.txt); B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/deliver/2026-11-17/fieldthru2/qa/$T; mkdir -p $O; cd $W
echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $O/runs.tsv
echo "data:image $(grep -c 'data:image' $B) · <img $(grep -o '<img' $B | wc -l)" > $O/static.txt
timeout 1500 node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json > $O/ingame.log 2>&1; echo "$T ingame $(TZ=Asia/Jerusalem date +%H:%M:%S) rc=$?" >> $O/runs.tsv
st(){ echo "$T $1 $(TZ=Asia/Jerusalem date +%H:%M:%S) rc=$2" >> $O/runs.tsv; }
FT2_DISPATCH=0 timeout 900 node deliver/2026-11-17/fieldthru2/tools/ft2_probe.js $B $O/probe.json > $O/probe.log 2>&1; st probe $?
timeout 900 node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.log 2>&1; st rules $?
timeout 1200 node qa_tools/people_on_road.js $B $O/people.json > $O/people.log 2>&1; st people $?
timeout 1500 node qa_tools/stuckmax.js $B 150 ft2_$T > $O/stuck.log 2>&1; st stuck $?
# P6 (try8092): הפירוט המלא של s15pax / fc_bridge_types
[ -f $W/clean_r2b_025637/out/_try/try8092.html ] && { timeout 900 node deliver/2026-11-17/fieldthru2/tools/ft2_paxprobe.js $W/clean_r2b_025637/out/_try/try8092.html $O/pax8092.json > $O/pax8092.log 2>&1; st pax8092 $?; }
echo done >> $O/runs.tsv

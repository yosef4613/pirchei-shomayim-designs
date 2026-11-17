#!/bin/bash
# כמו gates1.sh, אבל בדיקת האירועים קודם: bash bslot.sh bash gates2.sh tryNNNN [hourSecs] [maxF9]
W=/home/user/tc_root/tc/pkg/work; T=$1; B=$W/clean_r2b_025637/out/_try/$T.html; O=$W/qa/events/$T; mkdir -p $O; cd $W
L=$O/gates.log; echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node deliver/2026-11-17/events/tools/evt_test.js $B $O/evt.json $O/shots ${2:-130} ${3:-420} > $O/evt.log 2>&1; echo "evt rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $O/ingame.json 2> $O/ingame.err; echo "ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/rules_gate.js $B $O/rules.json > $O/rules.out 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/stuckmax.js $B 150 $T > $O/stuck.json 2> $O/stuck.err; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
node qa_tools/people_on_road.js $B $O/por.json > $O/por.out 2>&1; echo "por rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $L
echo "data:image $(grep -c 'data:image' $B)" >> $L
echo ALLDONE >> $L

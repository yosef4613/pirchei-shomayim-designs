#!/bin/bash
W=/home/user/tc_root/tc/pkg/work; N=$1; B=$W/clean_r2b_025637/out/_try/$N.html; Q=$W/deliver/2026-11-17/nfkiss/qa/$N; mkdir -p $Q; cd $W
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame.json 2> $Q/q_ingame.err; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/glog.txt
node qa_tools/rules_gate.js $B $Q/rules.json > $Q/rules.out 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/glog.txt
node qa_tools/people_on_road.js $B $Q/people.json > $Q/people.out 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/glog.txt
node qa_tools/stuckmax.js $B 150 $N > $Q/stuck.out 2>&1; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/glog.txt
echo end >> $Q/glog.txt

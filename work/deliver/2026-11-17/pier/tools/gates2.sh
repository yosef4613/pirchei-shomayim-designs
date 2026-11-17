#!/bin/bash
# הבדיקות החוסמות + הבדיקות של pier, בתור אחד (מקום אחד בתור, דפדפן אחד בכל פעם): bash gates.sh tryNNNN [all]
W=/home/user/tc_root/tc/pkg/work; N=$1; B=$W/clean_r2b_025637/out/_try/$N.html; Q=$W/deliver/2026-11-17/pier/qa/$N; mkdir -p $Q; cd $W
echo "start $(TZ=Asia/Jerusalem date +%H:%M:%S)" > $Q/log.txt
node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/pier/tools/q_clean.js $Q/clean.json 2>> $Q/clean.err; echo "clean rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt
node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/pier/tools/q_all.js $Q/pier_all.json 2>> $Q/pier_all.err; echo "pier_all rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt
node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame.json 2> $Q/q_ingame.err; echo "q_ingame rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt
node qa_tools/rules_gate.js $B $Q/rules.json > $Q/rules.out 2>&1; echo "rules rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt
node qa_tools/people_on_road.js $B $Q/people.json > $Q/people.out 2>&1; echo "people rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt
node qa_tools/stuckmax.js $B 150 $N > $Q/stuck.out 2>&1; echo "stuck rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt
echo "end" >> $Q/log.txt

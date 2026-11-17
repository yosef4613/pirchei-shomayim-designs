#!/bin/bash
# nfkiss: כל הבדיקות של המועמד במקום אחד בתור: bash bslot.sh bash all.sh cand301x
W=/home/user/tc_root/tc/pkg/work; N=$1; B=$W/clean_r2b_025637/out/_try/$N.html; Q=$W/deliver/2026-11-17/nfkiss/qa/$N; T=$W/deliver/2026-11-17/nfkiss/tools; mkdir -p $Q; cd $W
P=${2:-all}
L(){ echo "$1 rc=$2 $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt; }
[ "$P" != gates ] && { timeout 900 node qa_tools/probe_c2.js $B $T/q_nv.js $Q/nv.json > $Q/nv.err 2>&1; L nv $?; }
[ "$P" != gates ] && { timeout 900 node deliver/2026-11-17/voiceint/tools/q_voiceint.js $B $Q/voiceint.json > $Q/voiceint.err 2>&1; L voiceint $?; }
[ "$P" != gates ] && { timeout 600 node qa_tools/probe_c2.js $B $T/q_oldsave.js $Q/oldsave.json > $Q/oldsave.err 2>&1; L oldsave $?; }
[ "$P" != gates ] && { timeout 1200 node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/pier/tools/q_f2e2e.js $Q/f2e2e.json > $Q/f2e2e.err 2>&1; L f2e2e $?; }
[ "$P" != mine ] && { node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/q_ingame.json 2> $Q/q_ingame.err; L q_ingame $?; }
[ "$P" != mine ] && { node qa_tools/rules_gate.js $B $Q/rules.json > $Q/rules.out 2>&1; L rules $?; }
[ "$P" != mine ] && { node qa_tools/people_on_road.js $B $Q/people.json > $Q/people.out 2>&1; L people $?; }
[ "$P" != mine ] && { node qa_tools/stuckmax.js $B 150 $N > $Q/stuck.out 2>&1; L stuck $?; }
echo "end $P" >> $Q/log.txt

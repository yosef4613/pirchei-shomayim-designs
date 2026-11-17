#!/bin/bash
# inslot4.sh <try> — buses (17.11 16:05): הכיכרות (q_rb) ← המדידה ← הלילה של הקווים ← החוסמות.
W=/home/user/tc_root/tc/pkg/work; T=$1; [ "$T" = try6934 ] && T=try6936;   # 16:15: במקום try6934 — try6936 (waitBy כבוי; הכיכרות כבויות בו)
W=/home/user/tc_root/tc/pkg/work; D=$W/deliver/2026-11-17/buses; Q=$D/qa; cd $W
B=$W/clean_r2b_025637/out/_try/$T.html; G=$Q/${T}_gate.txt
r(){ local name=$1; shift; local t0=$(date +%s); timeout 2400 "$@"; echo "$name rc=$? $(( $(date +%s)-t0 ))s $(TZ=Asia/Jerusalem date +%H:%M)" >> $G; }
echo "start $(TZ=Asia/Jerusalem date +%H:%M)" >> $G
r beh node $D/tools/q_busbeh.js $B $Q/beh_${T}.json 420 600 > $Q/beh_${T}.log 2>&1
r night node $D/tools/lines_night_tr2.js $B $Q/${T}_night.json > $Q/${T}_night.log 2>&1
r ingame node qa_tools/probe_c2.js $B qa_tools/q_ingame.js $Q/${T}_ingame.json > $Q/${T}_ingame.log 2>&1
r rules node qa_tools/rules_gate.js $B $Q/${T}_rules.json > $Q/${T}_rules.log 2>&1
r stuck150 node qa_tools/stuckmax.js $B 150 $T > $Q/${T}_stuck150.json 2>&1
r people node qa_tools/people_on_road.js $B $Q/${T}_people.json > $Q/${T}_people.log 2>&1
echo "chain-done $(TZ=Asia/Jerusalem date +%H:%M)" >> $G

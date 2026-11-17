#!/bin/bash
# pier: הבדיקות שלי (המזח, F מתוך רכב מהשמירה הנקייה) ואחריהן החוסמות — במקום אחד בתור: bash bslot.sh bash run.sh tryNNNN
W=/home/user/tc_root/tc/pkg/work; N=$1; Q=$W/deliver/2026-11-17/pier/qa/$N; mkdir -p $Q; cd $W; B=clean_r2b_025637/out/_try/$N.html
timeout 900 node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/pier/tools/q_pier2.js $Q/pier2.json > $Q/pier2.err 2>&1; echo "pier2 rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/pre.log
timeout 900 node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/pier/tools/q_tug2.js $Q/tug2.json > $Q/tug2.err 2>&1; echo "tug2 rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/pre.log
timeout 1500 node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/pier/tools/q_fv2e.js $Q/fv2e.json > $Q/fv2e.err 2>&1; echo "fv2e rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/pre.log
bash $W/deliver/2026-11-17/pier/tools/gates2.sh $N

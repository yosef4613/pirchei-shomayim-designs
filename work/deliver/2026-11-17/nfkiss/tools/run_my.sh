#!/bin/bash
W=/home/user/tc_root/tc/pkg/work; B=$W/clean_r2b_025637/out/_try/$1.html; Q=$W/deliver/2026-11-17/nfkiss/qa/$1; mkdir -p $Q; cd $W
timeout 600 node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/nfkiss/tools/q_oldsave.js $Q/oldsave.json > $Q/oldsave.err 2>&1; echo "oldsave rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt
timeout 1200 node qa_tools/probe_c2.js $B $W/deliver/2026-11-17/pier/tools/q_f2e2e.js $Q/f2e2e.json > $Q/f2e2e.err 2>&1; echo "f2e2e rc=$? $(TZ=Asia/Jerusalem date +%H:%M:%S)" >> $Q/log.txt

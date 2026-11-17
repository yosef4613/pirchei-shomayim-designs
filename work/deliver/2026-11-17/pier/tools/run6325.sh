#!/bin/bash
W=/home/user/tc_root/tc/pkg/work; N=${1:-try6325}; Q=$W/deliver/2026-11-17/pier/qa/$N; mkdir -p $Q; cd $W
timeout 900 node qa_tools/probe_c2.js clean_r2b_025637/out/_try/$N.html $W/deliver/2026-11-17/pier/tools/q_b7e.js $Q/b7e.json > $Q/b7e.err 2>&1
bash $W/deliver/2026-11-17/pier/tools/gates2.sh $N

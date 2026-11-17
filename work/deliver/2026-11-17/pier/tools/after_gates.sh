#!/bin/bash
W=/home/user/tc_root/tc/pkg/work; Q=$W/deliver/2026-11-17/pier/qa/try6324
until grep -q '^end' $Q/log.txt 2>/dev/null; do sleep 15; done
cd $W && timeout 3000 bash tools_pack/bslot.sh node qa_tools/probe_c2.js clean_r2b_025637/out/_try/try6324.html $W/deliver/2026-11-17/pier/tools/q_b7e.js $Q/b7e.json > $Q/b7e.err 2>&1
